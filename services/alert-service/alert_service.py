from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.models import models, schemas
from app.core.celery_config import celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class AlertService:
    def __init__(self, db: Session):
        self.db = db

    def create_alert(self, alert_data: schemas.AlertCreate) -> models.Alert:
        """Create a new alert"""
        db_alert = models.Alert(**alert_data.dict())
        self.db.add(db_alert)
        self.db.commit()
        self.db.refresh(db_alert)
        
        # Queue alert for processing
        process_alert_task.delay(str(db_alert.id))
        
        return db_alert

    def get_alerts(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[models.Alert]:
        """Get alerts for an organization"""
        try:
            org_uuid = uuid.UUID(organization_id)
            return (self.db.query(models.Alert)
                   .filter(models.Alert.organization_id == org_uuid)
                   .order_by(models.Alert.created_at.desc())
                   .offset(skip)
                   .limit(limit)
                   .all())
        except ValueError:
            return []

    def acknowledge_alert(self, alert_id: str, user_id: str) -> Optional[models.Alert]:
        """Acknowledge an alert"""
        try:
            alert_uuid = uuid.UUID(alert_id)
            user_uuid = uuid.UUID(user_id)
            
            alert = self.db.query(models.Alert).filter(models.Alert.id == alert_uuid).first()
            if alert:
                alert.acknowledged = True
                alert.acknowledged_by = user_uuid
                alert.acknowledged_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(alert)
                return alert
            return None
        except ValueError:
            return None

    def resolve_alert(self, alert_id: str) -> Optional[models.Alert]:
        """Mark an alert as resolved"""
        try:
            alert_uuid = uuid.UUID(alert_id)
            alert = self.db.query(models.Alert).filter(models.Alert.id == alert_uuid).first()
            if alert:
                alert.resolved = True
                alert.resolved_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(alert)
                return alert
            return None
        except ValueError:
            return None

    def check_device_thresholds(self, device: models.Device, metric_type: str, value: float) -> Optional[models.Alert]:
        """Check if device metrics exceed thresholds and create alerts"""
        
        # Define thresholds (should be configurable in production)
        thresholds = {
            'cpu': {'warning': 70, 'critical': 90},
            'memory': {'warning': 80, 'critical': 95},
            'ping': {'warning': 1000, 'critical': 5000},  # Response time in ms
        }
        
        if metric_type not in thresholds:
            return None
            
        threshold = thresholds[metric_type]
        severity = None
        
        if value >= threshold['critical']:
            severity = 'critical'
        elif value >= threshold['warning']:
            severity = 'warning'
        
        if severity:
            # Check if similar alert already exists and is not resolved
            existing_alert = (self.db.query(models.Alert)
                            .filter(
                                models.Alert.device_id == device.id,
                                models.Alert.alert_type == f'high_{metric_type}',
                                models.Alert.resolved == False
                            )
                            .first())
            
            if not existing_alert:
                alert_data = {
                    'device_id': device.id,
                    'organization_id': device.organization_id,
                    'alert_type': f'high_{metric_type}',
                    'severity': severity,
                    'message': f'{device.name} - {metric_type.upper()} usage is {severity}: {value}%'
                }
                
                return self.create_alert(schemas.AlertCreate(**alert_data))
        
        return None


@celery_app.task(name="process_alert_task")
def process_alert_task(alert_id: str):
    """Process individual alert and trigger notifications"""
    from app.core.database import SessionLocal
    from app.services.notification_service import send_notification_task
    
    db = SessionLocal()
    try:
        alert_uuid = uuid.UUID(alert_id)
        alert = db.query(models.Alert).filter(models.Alert.id == alert_uuid).first()
        
        if alert:
            logger.info(f"Processing alert {alert_id}: {alert.message}")
            
            # Send notifications based on severity
            if alert.severity == 'critical':
                # Send immediate notifications via all channels
                send_notification_task.delay(alert_id, 'email')
                send_notification_task.delay(alert_id, 'sms')
                send_notification_task.delay(alert_id, 'webhook')
            elif alert.severity == 'warning':
                # Send email notification only
                send_notification_task.delay(alert_id, 'email')
            
            logger.info(f"Alert {alert_id} processed successfully")
        else:
            logger.error(f"Alert {alert_id} not found")
            
    except Exception as e:
        logger.error(f"Error processing alert {alert_id}: {str(e)}")
    finally:
        db.close()


@celery_app.task(name="process_alert_queue_task")
def process_alert_queue_task():
    """Process pending alerts in batches"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Find unprocessed alerts (you might want to add a 'processed' field to track this)
        pending_alerts = (db.query(models.Alert)
                         .filter(models.Alert.acknowledged == False)
                         .filter(models.Alert.created_at > datetime.utcnow().replace(hour=0, minute=0, second=0))
                         .limit(50)
                         .all())
        
        logger.info(f"Found {len(pending_alerts)} pending alerts to process")
        
        for alert in pending_alerts:
            process_alert_task.delay(str(alert.id))
            
    except Exception as e:
        logger.error(f"Error in alert queue processing: {str(e)}")
    finally:
        db.close()

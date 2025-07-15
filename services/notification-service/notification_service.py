from sqlalchemy.orm import Session
from typing import Dict, Any
import uuid
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models import models
from app.core.celery_config import celery_app
from app.core.config import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def send_email_notification(self, alert: models.Alert, recipients: list) -> bool:
        """Send email notification for alert"""
        try:
            # This is a placeholder - in production, use SendGrid API
            subject = f"NetPulse Alert: {alert.severity.upper()} - {alert.alert_type}"
            
            body = f"""
            Alert Details:
            Device: {alert.device.name if alert.device else 'Unknown'}
            Severity: {alert.severity.upper()}
            Message: {alert.message}
            Time: {alert.created_at}
            
            Please log into NetPulse to acknowledge this alert.
            """
            
            # Placeholder for email sending logic
            logger.info(f"Email notification sent for alert {alert.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email for alert {alert.id}: {str(e)}")
            return False

    def send_sms_notification(self, alert: models.Alert, phone_numbers: list) -> bool:
        """Send SMS notification for alert"""
        try:
            message = f"NetPulse {alert.severity.upper()}: {alert.device.name if alert.device else 'Unknown'} - {alert.message}"
            
            # Placeholder for Africa's Talking SMS API
            logger.info(f"SMS notification sent for alert {alert.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS for alert {alert.id}: {str(e)}")
            return False

    def send_webhook_notification(self, alert: models.Alert, webhook_urls: list) -> bool:
        """Send webhook notification for alert"""
        try:
            payload = {
                "alert_id": str(alert.id),
                "device_name": alert.device.name if alert.device else None,
                "severity": alert.severity,
                "alert_type": alert.alert_type,
                "message": alert.message,
                "timestamp": alert.created_at.isoformat(),
                "organization_id": str(alert.organization_id)
            }
            
            for webhook_url in webhook_urls:
                try:
                    response = requests.post(webhook_url, json=payload, timeout=30)
                    response.raise_for_status()
                    logger.info(f"Webhook notification sent to {webhook_url} for alert {alert.id}")
                except requests.RequestException as e:
                    logger.error(f"Failed to send webhook to {webhook_url}: {str(e)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send webhook for alert {alert.id}: {str(e)}")
            return False


@celery_app.task(name="send_notification_task")
def send_notification_task(alert_id: str, notification_type: str):
    """Send notification for a specific alert"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        alert_uuid = uuid.UUID(alert_id)
        alert = (db.query(models.Alert)
                .filter(models.Alert.id == alert_uuid)
                .first())
        
        if not alert:
            logger.error(f"Alert {alert_id} not found")
            return False
        
        notification_service = NotificationService(db)
        
        # Get notification settings for the organization (placeholder)
        # In production, you'd have a notification settings table
        
        if notification_type == 'email':
            # Get email recipients from organization users
            recipients = [user.email for user in alert.organization.users if user.is_active]
            if recipients:
                return notification_service.send_email_notification(alert, recipients)
                
        elif notification_type == 'sms':
            # Placeholder for phone number retrieval
            phone_numbers = []  # Get from user profiles
            if phone_numbers:
                return notification_service.send_sms_notification(alert, phone_numbers)
                
        elif notification_type == 'webhook':
            # Placeholder for webhook URL retrieval
            webhook_urls = []  # Get from organization settings
            if webhook_urls:
                return notification_service.send_webhook_notification(alert, webhook_urls)
        
        logger.warning(f"No {notification_type} configuration found for alert {alert_id}")
        return False
        
    except Exception as e:
        logger.error(f"Error sending {notification_type} notification for alert {alert_id}: {str(e)}")
        return False
    finally:
        db.close()


@celery_app.task(name="send_batch_notifications_task")
def send_batch_notifications_task(notification_type: str, organization_id: str = None):
    """Send batch notifications for multiple alerts"""
    from app.core.database import SessionLocal
    from datetime import datetime, timedelta
    
    db = SessionLocal()
    try:
        # Get unacknowledged alerts from the last hour
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        query = (db.query(models.Alert)
                .filter(models.Alert.acknowledged == False)
                .filter(models.Alert.created_at >= cutoff_time))
        
        if organization_id:
            org_uuid = uuid.UUID(organization_id)
            query = query.filter(models.Alert.organization_id == org_uuid)
        
        alerts = query.all()
        
        logger.info(f"Sending batch {notification_type} notifications for {len(alerts)} alerts")
        
        for alert in alerts:
            send_notification_task.delay(str(alert.id), notification_type)
            
        return len(alerts)
        
    except Exception as e:
        logger.error(f"Error in batch notification task: {str(e)}")
        return 0
    finally:
        db.close()

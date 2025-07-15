from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid

from app.models import models, schemas


class ReportingService:
    def __init__(self, db: Session):
        self.db = db

    def get_device_uptime_report(self, organization_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Generate device uptime report for the last N days"""
        try:
            org_uuid = uuid.UUID(organization_id)
            start_date = datetime.utcnow() - timedelta(days=days)
            
            devices = (self.db.query(models.Device)
                      .filter(models.Device.organization_id == org_uuid)
                      .all())
            
            report = []
            for device in devices:
                # Calculate uptime based on device status changes
                # This is simplified - in production, you'd track status change events
                total_hours = days * 24
                
                # Count downtime alerts
                downtime_alerts = (self.db.query(models.Alert)
                                 .filter(models.Alert.device_id == device.id)
                                 .filter(models.Alert.alert_type.like('%down%'))
                                 .filter(models.Alert.created_at >= start_date)
                                 .count())
                
                # Estimate uptime (simplified calculation)
                estimated_downtime_hours = downtime_alerts * 0.5  # Assume 30min avg downtime per alert
                uptime_percentage = max(0, (total_hours - estimated_downtime_hours) / total_hours * 100)
                
                report.append({
                    "device_id": str(device.id),
                    "device_name": device.name,
                    "device_type": device.device_type,
                    "location": device.location,
                    "uptime_percentage": round(uptime_percentage, 2),
                    "total_alerts": downtime_alerts,
                    "current_status": device.status,
                    "last_seen": device.last_seen
                })
            
            return report
            
        except ValueError:
            return []

    def get_alert_summary_report(self, organization_id: str, days: int = 30) -> Dict[str, Any]:
        """Generate alert summary report"""
        try:
            org_uuid = uuid.UUID(organization_id)
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Total alerts
            total_alerts = (self.db.query(models.Alert)
                           .filter(models.Alert.organization_id == org_uuid)
                           .filter(models.Alert.created_at >= start_date)
                           .count())
            
            # Alerts by severity
            critical_alerts = (self.db.query(models.Alert)
                             .filter(models.Alert.organization_id == org_uuid)
                             .filter(models.Alert.severity == 'critical')
                             .filter(models.Alert.created_at >= start_date)
                             .count())
            
            warning_alerts = (self.db.query(models.Alert)
                            .filter(models.Alert.organization_id == org_uuid)
                            .filter(models.Alert.severity == 'warning')
                            .filter(models.Alert.created_at >= start_date)
                            .count())
            
            info_alerts = (self.db.query(models.Alert)
                         .filter(models.Alert.organization_id == org_uuid)
                         .filter(models.Alert.severity == 'info')
                         .filter(models.Alert.created_at >= start_date)
                         .count())
            
            # Resolved alerts
            resolved_alerts = (self.db.query(models.Alert)
                             .filter(models.Alert.organization_id == org_uuid)
                             .filter(models.Alert.resolved == True)
                             .filter(models.Alert.created_at >= start_date)
                             .count())
            
            # Average resolution time (for resolved alerts)
            resolved_with_times = (self.db.query(models.Alert)
                                 .filter(models.Alert.organization_id == org_uuid)
                                 .filter(models.Alert.resolved == True)
                                 .filter(models.Alert.resolved_at.isnot(None))
                                 .filter(models.Alert.created_at >= start_date)
                                 .all())
            
            avg_resolution_time = None
            if resolved_with_times:
                total_resolution_time = sum(
                    (alert.resolved_at - alert.created_at).total_seconds() 
                    for alert in resolved_with_times
                )
                avg_resolution_time = total_resolution_time / len(resolved_with_times) / 60  # in minutes
            
            return {
                "period_days": days,
                "total_alerts": total_alerts,
                "alerts_by_severity": {
                    "critical": critical_alerts,
                    "warning": warning_alerts,
                    "info": info_alerts
                },
                "resolution_stats": {
                    "total_resolved": resolved_alerts,
                    "resolution_rate": round(resolved_alerts / total_alerts * 100, 2) if total_alerts > 0 else 0,
                    "avg_resolution_time_minutes": round(avg_resolution_time, 2) if avg_resolution_time else None
                }
            }
            
        except ValueError:
            return {}

    def get_device_metrics_report(self, device_id: str, metric_type: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get device metrics for reporting"""
        try:
            device_uuid = uuid.UUID(device_id)
            start_time = datetime.utcnow() - timedelta(hours=hours)
            
            metrics = (self.db.query(models.DeviceMetric)
                      .filter(models.DeviceMetric.device_id == device_uuid)
                      .filter(models.DeviceMetric.metric_type == metric_type)
                      .filter(models.DeviceMetric.time >= start_time)
                      .order_by(models.DeviceMetric.time)
                      .all())
            
            return [
                {
                    "timestamp": metric.time.isoformat(),
                    "value": metric.value,
                    "unit": metric.unit
                }
                for metric in metrics
            ]
            
        except ValueError:
            return []

    def get_organization_overview(self, organization_id: str) -> Dict[str, Any]:
        """Get high-level organization overview"""
        try:
            org_uuid = uuid.UUID(organization_id)
            
            # Device counts
            total_devices = (self.db.query(models.Device)
                           .filter(models.Device.organization_id == org_uuid)
                           .count())
            
            online_devices = (self.db.query(models.Device)
                            .filter(models.Device.organization_id == org_uuid)
                            .filter(models.Device.status == 'online')
                            .count())
            
            # Recent alerts (last 24 hours)
            recent_alerts = (self.db.query(models.Alert)
                           .filter(models.Alert.organization_id == org_uuid)
                           .filter(models.Alert.created_at >= datetime.utcnow() - timedelta(hours=24))
                           .count())
            
            # Critical unresolved alerts
            critical_unresolved = (self.db.query(models.Alert)
                                 .filter(models.Alert.organization_id == org_uuid)
                                 .filter(models.Alert.severity == 'critical')
                                 .filter(models.Alert.resolved == False)
                                 .count())
            
            return {
                "organization_id": organization_id,
                "device_stats": {
                    "total_devices": total_devices,
                    "online_devices": online_devices,
                    "offline_devices": total_devices - online_devices,
                    "uptime_percentage": round(online_devices / total_devices * 100, 2) if total_devices > 0 else 0
                },
                "alert_stats": {
                    "recent_alerts_24h": recent_alerts,
                    "critical_unresolved": critical_unresolved
                },
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except ValueError:
            return {}

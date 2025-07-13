from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
from datetime import datetime

from app.core.database import get_db
from app.models import models
from app.core.dependencies import get_current_active_user

router = APIRouter()

# Prometheus metrics
device_status_gauge = Gauge('device_status', 'Device status (1=online, 0=offline)', ['device_name', 'ip_address', 'device_type', 'location'])
device_response_time_histogram = Histogram('device_response_time_ms', 'Device response time in milliseconds', ['device_name', 'ip_address'])
device_uptime_gauge = Gauge('device_uptime_seconds', 'Device uptime in seconds', ['device_name', 'ip_address'])
device_packet_loss_gauge = Gauge('device_packet_loss_percent', 'Device packet loss percentage', ['device_name', 'ip_address'])
device_info_gauge = Gauge('device_info', 'Device information', ['device_name', 'ip_address', 'device_type', 'location', 'status', 'last_seen'])

# Counters for events
device_status_changes = Counter('device_status_changes_total', 'Total device status changes', ['device_name', 'old_status', 'new_status'])
monitoring_checks_total = Counter('monitoring_checks_total', 'Total monitoring checks performed', ['device_name'])
monitoring_errors_total = Counter('monitoring_errors_total', 'Total monitoring errors', ['device_name', 'error_type'])

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """
    Prometheus metrics endpoint for device monitoring data.
    This endpoint is public (no authentication required) as it's accessed by Prometheus.
    """
    devices = db.query(models.Device).all()
    
    for device in devices:
        labels = {
            'device_name': device.name,
            'ip_address': device.ip_address,
            'device_type': device.device_type,
            'location': device.location or 'Unknown'
        }
        
        # Set device status (1 for online, 0 for offline)
        status_value = 1 if device.status == 'online' else 0
        device_status_gauge.labels(**labels).set(status_value)
        
        # Calculate uptime
        if device.last_seen and device.status == 'online':
            uptime_seconds = (datetime.utcnow() - device.created_at).total_seconds()
            device_uptime_gauge.labels(
                device_name=device.name,
                ip_address=device.ip_address
            ).set(uptime_seconds)
        
        # Set device info metric (always 1, used for metadata)
        device_info_gauge.labels(
            device_name=device.name,
            ip_address=device.ip_address,
            device_type=device.device_type,
            location=device.location or 'Unknown',
            status=device.status,
            last_seen=device.last_seen.isoformat() if device.last_seen else 'Never'
        ).set(1)
        
        # Simulate response time and packet loss metrics
        # In a real implementation, these would come from actual monitoring data
        if device.status == 'online':
            # Simulate response time between 10-100ms for online devices
            import random
            response_time = random.uniform(10, 100)
            device_response_time_histogram.labels(
                device_name=device.name,
                ip_address=device.ip_address
            ).observe(response_time)
            
            # Simulate packet loss (0-2% for healthy devices)
            packet_loss = random.uniform(0, 2)
            device_packet_loss_gauge.labels(
                device_name=device.name,
                ip_address=device.ip_address
            ).set(packet_loss)
        else:
            # Offline devices have high response time and packet loss
            device_response_time_histogram.labels(
                device_name=device.name,
                ip_address=device.ip_address
            ).observe(5000)  # 5 second timeout
            
            device_packet_loss_gauge.labels(
                device_name=device.name,
                ip_address=device.ip_address
            ).set(100)  # 100% packet loss
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.get("/devices")
def get_device_metrics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get device metrics in JSON format for authenticated users.
    """
    devices = db.query(models.Device).all()
    metrics = []
    
    for device in devices:
        uptime_seconds = 0
        if device.last_seen and device.status == 'online':
            uptime_seconds = (datetime.utcnow() - device.created_at).total_seconds()
        
        device_metric = {
            'device_name': device.name,
            'ip_address': device.ip_address,
            'device_type': device.device_type,
            'location': device.location,
            'status': device.status,
            'last_seen': device.last_seen.isoformat() if device.last_seen else None,
            'uptime_seconds': uptime_seconds,
            'created_at': device.created_at.isoformat(),
            'updated_at': device.updated_at.isoformat()
        }
        metrics.append(device_metric)
    
    return {
        'total_devices': len(devices),
        'online_devices': len([d for d in devices if d.status == 'online']),
        'offline_devices': len([d for d in devices if d.status == 'offline']),
        'devices': metrics
    }

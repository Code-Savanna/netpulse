from celery_app import celery_app
from database import SessionLocal
from monitoring_service import MonitoringService
import httpx
import asyncio
import os

DEVICE_SERVICE_URL = os.getenv("DEVICE_SERVICE_URL", "http://device-service:8002")

@celery_app.task(name="monitor_devices_task")
def monitor_devices_task():
    """Celery task to monitor all devices"""
    db = SessionLocal()
    try:
        monitoring_service = MonitoringService(db)
        
        # This would typically get devices from device service
        # For now, we'll implement a simple version
        print("Monitoring devices task executed")
        
        return {"status": "completed", "devices_checked": 0}
    except Exception as e:
        print(f"Error in monitoring task: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

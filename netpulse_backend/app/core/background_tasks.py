import asyncio
from app.core.celery_config import celery_app
from app.core.database import SessionLocal
from app.services.monitoring_service import MonitoringService
from app.api.endpoints.websocket import broadcast_device_update
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery_app.task(name="monitor_devices_task")
def monitor_devices_task():
    """
    Celery task to monitor devices and broadcast status changes.
    """
    logger.info("Starting device monitoring task...")
    db = SessionLocal()
    monitoring_service = MonitoringService(db)
    
    async def run_monitoring():
        updated_devices = await monitoring_service.monitor_all_devices()
        if updated_devices:
            logger.info(f"Found {len(updated_devices)} devices with status changes.")
            await broadcast_device_update(updated_devices)
        else:
            logger.info("No device status changes detected.")

    try:
        asyncio.run(run_monitoring())
    finally:
        db.close()
        logger.info("Device monitoring task finished.")


@celery_app.task(name="sample_task")
def sample_task(x: int, y: int) -> int:
    """
    A sample background task that adds two numbers.
    """
    logger.info(f"Adding {x} and {y}")
    result = x + y
    logger.info(f"Result is {result}")
    return result

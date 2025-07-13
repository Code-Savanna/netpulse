import asyncio
import subprocess
import platform
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List

from app.models import models
from app.services.device_service import DeviceService


class MonitoringService:
    def __init__(self, db: Session):
        self.db = db
        self.device_service = DeviceService(self.db)

    async def ping_device(self, ip_address: str) -> bool:
        """Ping a device to check if it's online"""
        try:
            # Different ping commands for different OS
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", ip_address]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except Exception:
            return False

    async def check_device_status(self, device: models.Device) -> models.Device | None:
        """
        Check the status of a single device.
        Returns the device if status changed, otherwise None.
        """
        is_online = await self.ping_device(device.ip_address)
        new_status = "online" if is_online else "offline"

        if device.status != new_status:
            device.status = new_status
            device.last_seen = datetime.utcnow()
            self.db.commit()
            self.db.refresh(device)
            return device
        
        if is_online:
            device.last_seen = datetime.utcnow()
            self.db.commit()

        return None

    async def monitor_all_devices(self) -> List[models.Device]:
        """
        Monitor all devices and update their status.
        Returns a list of devices whose status has changed.
        """
        devices = self.device_service.get_devices()
        
        tasks = [self.check_device_status(device) for device in devices]
        results = await asyncio.gather(*tasks)
        
        # Filter out None results to get only updated devices
        updated_devices = [res for res in results if res is not None]
        return updated_devices

    async def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring with specified interval in seconds"""
        while True:
            try:
                await self.monitor_all_devices()
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(interval)

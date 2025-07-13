from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.models import models, schemas


class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def get_devices(self, skip: int = 0, limit: int = 100) -> List[models.Device]:
        """Get all devices with pagination"""
        return self.db.query(models.Device).offset(skip).limit(limit).all()

    def get_device(self, device_id: str) -> Optional[models.Device]:
        """Get a specific device by ID"""
        try:
            device_uuid = uuid.UUID(device_id)
            return self.db.query(models.Device).filter(models.Device.id == device_uuid).first()
        except ValueError:
            return None

    def create_device(self, device: schemas.DeviceCreate) -> models.Device:
        """Create a new device"""
        db_device = models.Device(**device.dict())
        self.db.add(db_device)
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def update_device(self, device_id: str, device: schemas.DeviceUpdate) -> Optional[models.Device]:
        """Update a device"""
        db_device = self.get_device(device_id)
        if db_device is None:
            return None
        
        update_data = device.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_device, field, value)
        
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def delete_device(self, device_id: str) -> bool:
        """Delete a device"""
        db_device = self.get_device(device_id)
        if db_device is None:
            return False
        
        self.db.delete(db_device)
        self.db.commit()
        return True

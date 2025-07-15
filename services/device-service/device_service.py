from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from models import Device
from schemas import DeviceCreate, DeviceUpdate


class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def get_devices_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Device]:
        """Get all devices for an organization with pagination"""
        try:
            org_uuid = uuid.UUID(organization_id)
            return (self.db.query(Device)
                   .filter(Device.organization_id == org_uuid)
                   .offset(skip)
                   .limit(limit)
                   .all())
        except ValueError:
            return []

    def get_device(self, device_id: str) -> Optional[Device]:
        """Get a specific device by ID"""
        try:
            device_uuid = uuid.UUID(device_id)
            return self.db.query(Device).filter(Device.id == device_uuid).first()
        except ValueError:
            return None

    def create_device(self, device: DeviceCreate) -> Device:
        """Create a new device"""
        db_device = Device(**device.dict())
        self.db.add(db_device)
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def update_device(self, device_id: str, device: DeviceUpdate) -> Optional[Device]:
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

    def update_device_status(self, device_id: str, status: str, last_seen: datetime = None) -> Optional[Device]:
        """Update device status and last seen timestamp"""
        from datetime import datetime
        
        db_device = self.get_device(device_id)
        if db_device is None:
            return None
        
        db_device.status = status
        if last_seen:
            db_device.last_seen = last_seen
        else:
            db_device.last_seen = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

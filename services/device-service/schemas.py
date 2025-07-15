from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class DeviceBase(BaseModel):
    name: str
    ip_address: str
    device_type: str
    location: Optional[str] = None


class DeviceCreate(DeviceBase):
    organization_id: Optional[uuid.UUID] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    device_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


class DeviceResponse(DeviceBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    status: str
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

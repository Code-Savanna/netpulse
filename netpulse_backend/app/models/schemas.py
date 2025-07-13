from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class DeviceBase(BaseModel):
    name: str
    ip_address: str
    device_type: str
    location: Optional[str] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    device_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


class Device(DeviceBase):
    id: uuid.UUID
    status: str
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DeviceMetricBase(BaseModel):
    metric_type: str
    value: float
    unit: Optional[str] = None


class DeviceMetricCreate(DeviceMetricBase):
    device_id: uuid.UUID


class DeviceMetric(DeviceMetricBase):
    id: uuid.UUID
    device_id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

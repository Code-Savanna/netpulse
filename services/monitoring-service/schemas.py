from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class DeviceMetricBase(BaseModel):
    metric_type: str
    value: float
    unit: Optional[str] = None


class DeviceMetricCreate(DeviceMetricBase):
    device_id: uuid.UUID
    time: Optional[datetime] = None


class DeviceMetricResponse(DeviceMetricBase):
    device_id: uuid.UUID
    time: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class AlertBase(BaseModel):
    alert_type: str
    severity: str = Field(..., regex="^(info|warning|critical)$")
    message: str


class AlertCreate(AlertBase):
    device_id: Optional[uuid.UUID] = None
    organization_id: uuid.UUID


class AlertUpdate(BaseModel):
    acknowledged: Optional[bool] = None
    resolved: Optional[bool] = None


class AlertResponse(AlertBase):
    id: uuid.UUID
    device_id: Optional[uuid.UUID] = None
    organization_id: uuid.UUID
    acknowledged: bool
    acknowledged_by: Optional[uuid.UUID] = None
    acknowledged_at: Optional[datetime] = None
    resolved: bool
    resolved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

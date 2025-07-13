from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    device_type = Column(String, nullable=False)  # router, switch, server, etc.
    location = Column(String)
    status = Column(String, default="unknown")  # online, offline, unknown
    last_seen = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to metrics
    metrics = relationship("DeviceMetric", back_populates="device")


class DeviceMetric(Base):
    __tablename__ = "device_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    metric_type = Column(String, nullable=False)  # cpu, memory, network, ping
    value = Column(Float, nullable=False)
    unit = Column(String)  # %, MB, ms, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to device
    device = relationship("Device", back_populates="metrics")

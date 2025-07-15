from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from database import Base


class DeviceMetric(Base):
    __tablename__ = "device_metrics"

    # Composite primary key for time-series data
    time = Column(DateTime(timezone=True), primary_key=True)
    device_id = Column(UUID(as_uuid=True), primary_key=True)
    metric_type = Column(String, primary_key=True, nullable=False)  # cpu, memory, network, ping
    value = Column(Float, nullable=False)
    unit = Column(String)  # %, MB, ms, etc.

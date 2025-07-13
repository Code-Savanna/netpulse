from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models import models, schemas
from app.services.device_service import DeviceService
from app.core.dependencies import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[schemas.Device])
def read_devices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all devices"""
    device_service = DeviceService(db)
    devices = device_service.get_devices(skip=skip, limit=limit)
    return devices


@router.post("/", response_model=schemas.Device)
def create_device(
    device: schemas.DeviceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new device"""
    device_service = DeviceService(db)
    return device_service.create_device(device)


@router.get("/{device_id}", response_model=schemas.Device)
def read_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get a specific device"""
    device_service = DeviceService(db)
    device = device_service.get_device(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=schemas.Device)
def update_device(
    device_id: str,
    device: schemas.DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update a device"""
    device_service = DeviceService(db)
    updated_device = device_service.update_device(device_id, device)
    if updated_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device


@router.delete("/{device_id}")
def delete_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete a device"""
    device_service = DeviceService(db)
    if not device_service.delete_device(device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}

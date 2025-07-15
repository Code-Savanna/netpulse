from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx
import os

from database import get_db, engine
from models import Device, Base
from schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from device_service import DeviceService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NetPulse Device Management Service",
    description="Device Management and Configuration Service",
    version="1.0.0"
)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")


async def get_current_user(authorization: str = Header(...)):
    """Get current user from auth service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/verify-token",
                headers={"Authorization": authorization}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth service unavailable")


@app.get("/devices", response_model=List[DeviceResponse])
def get_devices(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get devices for user's organization"""
    if not current_user.get("organization_id"):
        raise HTTPException(status_code=403, detail="User not associated with organization")
    
    device_service = DeviceService(db)
    devices = device_service.get_devices_by_organization(
        organization_id=current_user["organization_id"],
        skip=skip,
        limit=limit
    )
    return devices


@app.post("/devices", response_model=DeviceResponse)
def create_device(
    device: DeviceCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new device"""
    if not current_user.get("organization_id"):
        raise HTTPException(status_code=403, detail="User not associated with organization")
    
    # Set organization_id from current user
    device.organization_id = current_user["organization_id"]
    
    device_service = DeviceService(db)
    return device_service.create_device(device)


@app.get("/devices/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific device"""
    device_service = DeviceService(db)
    device = device_service.get_device(device_id)
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Check organization access
    if str(device.organization_id) != current_user.get("organization_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return device


@app.put("/devices/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: str,
    device_update: DeviceUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a device"""
    device_service = DeviceService(db)
    
    # Check if device exists and user has access
    device = device_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if str(device.organization_id) != current_user.get("organization_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    updated_device = device_service.update_device(device_id, device_update)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return updated_device


@app.delete("/devices/{device_id}")
def delete_device(
    device_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a device"""
    device_service = DeviceService(db)
    
    # Check if device exists and user has access
    device = device_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if str(device.organization_id) != current_user.get("organization_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    success = device_service.delete_device(device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return {"message": "Device deleted successfully"}


@app.get("/devices/{device_id}/status")
def get_device_status(
    device_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get device status"""
    device_service = DeviceService(db)
    device = device_service.get_device(device_id)
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if str(device.organization_id) != current_user.get("organization_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "device_id": device_id,
        "status": device.status,
        "last_seen": device.last_seen,
        "ip_address": device.ip_address
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "device-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

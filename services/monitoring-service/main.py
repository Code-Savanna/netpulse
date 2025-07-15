from fastapi import FastAPI, HTTPException, Depends, Header, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
import httpx
import os
import asyncio
import json

from database import get_db, engine
from models import DeviceMetric, Base
from schemas import DeviceMetricCreate, DeviceMetricResponse
from monitoring_service import MonitoringService
from celery_app import celery_app

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NetPulse Monitoring Service",
    description="Device Monitoring and Metrics Collection Service",
    version="1.0.0"
)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
DEVICE_SERVICE_URL = os.getenv("DEVICE_SERVICE_URL", "http://device-service:8002")


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


# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections[:]:  # Create a copy to avoid modification during iteration
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.disconnect(connection)

manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time monitoring updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(30)
            await websocket.send_text(json.dumps({"type": "heartbeat", "data": "alive"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/metrics/{device_id}", response_model=List[DeviceMetricResponse])
def get_device_metrics(
    device_id: str,
    metric_type: str = None,
    hours: int = 24,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get metrics for a specific device"""
    monitoring_service = MonitoringService(db)
    metrics = monitoring_service.get_device_metrics(device_id, metric_type, hours)
    return metrics


@app.post("/metrics", response_model=DeviceMetricResponse)
def create_metric(
    metric: DeviceMetricCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new metric (typically called by monitoring agents)"""
    monitoring_service = MonitoringService(db)
    return monitoring_service.create_metric(metric)


@app.get("/devices/{device_id}/status")
async def check_device_status(
    device_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check and update device status"""
    monitoring_service = MonitoringService(db)
    
    # Get device info from device service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DEVICE_SERVICE_URL}/devices/{device_id}/status",
                headers={"Authorization": f"Bearer {current_user.get('token', '')}"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Device not found")
            device_info = response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Device service unavailable")
    
    # Perform ping check
    is_online = await monitoring_service.ping_device(device_info["ip_address"])
    new_status = "online" if is_online else "offline"
    
    # Update device status if changed
    if device_info["status"] != new_status:
        # Update via device service
        try:
            async with httpx.AsyncClient() as client:
                await client.put(
                    f"{DEVICE_SERVICE_URL}/devices/{device_id}",
                    json={"status": new_status},
                    headers={"Authorization": f"Bearer {current_user.get('token', '')}"}
                )
        except httpx.RequestError:
            pass  # Log error in production
        
        # Broadcast status change
        await manager.broadcast(json.dumps({
            "type": "device_status_change",
            "data": {
                "device_id": device_id,
                "status": new_status,
                "timestamp": "now"
            }
        }))
    
    return {
        "device_id": device_id,
        "status": new_status,
        "is_online": is_online,
        "ip_address": device_info["ip_address"]
    }


@app.post("/trigger-monitoring")
def trigger_monitoring(current_user: dict = Depends(get_current_user)):
    """Manually trigger device monitoring"""
    # Send monitoring task to queue
    celery_app.send_task("monitor_devices_task", queue="monitoring")
    return {"message": "Monitoring task triggered"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "monitoring-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

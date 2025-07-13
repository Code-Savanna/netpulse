from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

from app.models.models import Device

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

async def broadcast_device_update(updated_devices: List[Device]):
    """
    Broadcasts updates for specific devices to all connected clients.
    """
    if not updated_devices:
        return

    device_data = []
    for device in updated_devices:
        device_data.append({
            "id": str(device.id),
            "name": device.name,
            "ip_address": device.ip_address,
            "status": device.status,
            "last_seen": device.last_seen.isoformat() if device.last_seen else None
        })

    await manager.broadcast(json.dumps({
        "type": "device_update",
        "data": device_data
    }))

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(10)
            await manager.send_personal_message("ping", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

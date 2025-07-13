from fastapi import APIRouter

from app.api.endpoints import users, devices, websocket, auth, metrics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

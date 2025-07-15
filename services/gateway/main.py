from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import httpx
import os
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NetPulse API Gateway",
    description="Central API Gateway for NetPulse Microservices",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Service URLs from environment
SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001"),
    "devices": os.getenv("DEVICE_SERVICE_URL", "http://device-service:8002"),
    "monitoring": os.getenv("MONITORING_SERVICE_URL", "http://monitoring-service:8003"),
    "alerts": os.getenv("ALERT_SERVICE_URL", "http://alert-service:8004"),
    "notifications": os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8005"),
    "reporting": os.getenv("REPORTING_SERVICE_URL", "http://reporting-service:8006"),
}

# Service routing configuration
ROUTES = {
    "/auth": "auth",
    "/users": "auth",
    "/devices": "devices", 
    "/alerts": "alerts",
    "/notifications": "notifications",
    "/reports": "reporting",
    "/metrics": "monitoring",
    "/ws": "monitoring",  # WebSocket for real-time updates
}


async def verify_token(request: Request) -> Dict[str, Any]:
    """Verify JWT token with auth service"""
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['auth']}/verify-token",
                headers={"Authorization": auth_header}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth service unavailable")


async def route_request(request: Request, path: str):
    """Route request to appropriate microservice"""
    # Determine target service
    service_name = None
    for route_prefix, service in ROUTES.items():
        if path.startswith(route_prefix):
            service_name = service
            break
    
    if not service_name:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service_url = SERVICES.get(service_name)
    if not service_url:
        raise HTTPException(status_code=503, detail=f"Service {service_name} unavailable")
    
    # Skip auth verification for auth endpoints
    if not path.startswith("/auth/login") and not path.startswith("/auth/register"):
        await verify_token(request)
    
    # Forward request to microservice
    try:
        async with httpx.AsyncClient() as client:
            # Preserve all headers, body, and query parameters
            headers = dict(request.headers)
            headers.pop("host", None)  # Remove host header
            
            response = await client.request(
                method=request.method,
                url=f"{service_url}{path}",
                headers=headers,
                params=request.query_params,
                content=await request.body(),
                timeout=30.0
            )
            
            return response
            
    except httpx.RequestError as e:
        logger.error(f"Error routing to {service_name}: {e}")
        raise HTTPException(status_code=503, detail=f"Service {service_name} unavailable")


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_route(request: Request, path: str):
    """Main gateway routing function"""
    response = await route_request(request, f"/{path}")
    
    # Return response with same status code and headers
    return {
        "status_code": response.status_code,
        "content": response.content,
        "headers": dict(response.headers)
    }


@app.get("/health")
async def health_check():
    """Gateway health check"""
    service_health = {}
    
    async with httpx.AsyncClient() as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(f"{service_url}/health", timeout=5.0)
                service_health[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_url
                }
            except httpx.RequestError:
                service_health[service_name] = {
                    "status": "unavailable",
                    "url": service_url
                }
    
    return {
        "gateway": "healthy",
        "services": service_health
    }


@app.get("/")
async def root():
    """Gateway info"""
    return {
        "service": "NetPulse API Gateway",
        "version": "1.0.0",
        "available_routes": list(ROUTES.keys()),
        "services": list(SERVICES.keys())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

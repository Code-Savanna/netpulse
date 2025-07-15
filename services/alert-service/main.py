from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List
import httpx
import os

from database import get_db, engine
from models import Alert, Base
from schemas import AlertCreate, AlertUpdate, AlertResponse
from alert_service import AlertService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NetPulse Alert Service",
    description="Alert Management and Processing Service",
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


@app.get("/alerts", response_model=List[AlertResponse])
def get_alerts(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get alerts for user's organization"""
    if not current_user.get("organization_id"):
        raise HTTPException(status_code=403, detail="User not associated with organization")
    
    alert_service = AlertService(db)
    alerts = alert_service.get_alerts(
        organization_id=current_user["organization_id"],
        skip=skip,
        limit=limit
    )
    return alerts


@app.post("/alerts", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    alert_service = AlertService(db)
    return alert_service.create_alert(alert)


@app.put("/alerts/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Acknowledge an alert"""
    alert_service = AlertService(db)
    updated_alert = alert_service.acknowledge_alert(alert_id, current_user["user_id"])
    
    if not updated_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return updated_alert


@app.put("/alerts/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resolve an alert"""
    alert_service = AlertService(db)
    updated_alert = alert_service.resolve_alert(alert_id)
    
    if not updated_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return updated_alert


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "alert-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

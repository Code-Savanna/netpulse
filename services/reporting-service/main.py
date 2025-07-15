from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
import httpx
import os

from database import get_db, engine
from models import Base
from schemas import ReportRequest, ReportResponse
from reporting_service import ReportingService

app = FastAPI(
    title="NetPulse Reporting Service",
    description="Analytics and Reporting Service",
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


@app.get("/uptime-report/{organization_id}")
def get_uptime_report(
    organization_id: str,
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get device uptime report"""
    reporting_service = ReportingService(db)
    report = reporting_service.get_device_uptime_report(organization_id, days)
    return report


@app.get("/alert-summary/{organization_id}")
def get_alert_summary(
    organization_id: str,
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get alert summary report"""
    reporting_service = ReportingService(db)
    report = reporting_service.get_alert_summary_report(organization_id, days)
    return report


@app.get("/overview/{organization_id}")
def get_organization_overview(
    organization_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get organization overview"""
    reporting_service = ReportingService(db)
    overview = reporting_service.get_organization_overview(organization_id)
    return overview


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "reporting-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)

from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
import httpx
import os

from database import get_db, engine
from models import Base
from schemas import NotificationRequest, NotificationResponse
from notification_service import NotificationService

app = FastAPI(
    title="NetPulse Notification Service",
    description="Multi-channel Notification Service",
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


@app.post("/send", response_model=NotificationResponse)
def send_notification(
    notification: NotificationRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a notification"""
    notification_service = NotificationService(db)
    result = notification_service.send_notification(notification)
    return result


@app.post("/send-email")
def send_email(
    recipients: list,
    subject: str,
    body: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send email notification"""
    notification_service = NotificationService(db)
    result = notification_service.send_email(recipients, subject, body)
    return {"status": "sent", "recipients": len(recipients)}


@app.post("/send-sms")
def send_sms(
    phone_numbers: list,
    message: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send SMS notification"""
    notification_service = NotificationService(db)
    result = notification_service.send_sms(phone_numbers, message)
    return {"status": "sent", "recipients": len(phone_numbers)}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "notification-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)

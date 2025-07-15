from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class NotificationRequest(BaseModel):
    type: str  # email, sms, webhook
    recipients: List[str]
    subject: Optional[str] = None
    message: str
    data: Optional[Dict[str, Any]] = None


class NotificationResponse(BaseModel):
    status: str
    message: str
    sent_count: int
    failed_count: int

from pydantic import BaseModel
from typing import Dict, List, Any


class ReportRequest(BaseModel):
    report_type: str
    organization_id: str
    parameters: Dict[str, Any]


class ReportResponse(BaseModel):
    report_type: str
    data: Dict[str, Any]
    generated_at: str

from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class CertificationBase(BaseModel):
    title: str
    issuer: str
    issue_date: date
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None

class CertificationCreate(CertificationBase):
    pass

class CertificationUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    issue_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None

class CertificationResponse(CertificationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

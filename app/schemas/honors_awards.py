from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class HonorAwardBase(BaseModel):
    title: str
    issuer: str
    date_received: date
    image: Optional[str] = None
    description: Optional[str] = None

class HonorAwardCreate(HonorAwardBase):
    pass

class HonorAwardUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    date_received: Optional[date] = None
    image: Optional[str] = None
    description: Optional[str] = None

class HonorAwardResponse(HonorAwardBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

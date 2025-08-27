from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class ExperienceBase(BaseModel):
    role: str
    company: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None
    logo: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    role: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    logo: Optional[str] = None

class ExperienceResponse(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

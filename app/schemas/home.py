from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HomeBase(BaseModel):
    name: str
    headline: str
    about: str
    profile_image: Optional[str] = None
    resume_link: Optional[str] = None

class HomeCreate(HomeBase):
    pass

class HomeUpdate(BaseModel):
    name: Optional[str] = None
    headline: Optional[str] = None
    about: Optional[str] = None
    profile_image: Optional[str] = None
    resume_link: Optional[str] = None

class HomeResponse(HomeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

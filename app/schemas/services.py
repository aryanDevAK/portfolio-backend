from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ServiceBase(BaseModel):
    title: str
    description: str
    icon: Optional[str] = None
    price: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    price: Optional[str] = None

class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

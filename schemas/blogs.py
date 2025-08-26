from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BlogBase(BaseModel):
    title: str
    slug: str
    content: str
    banner_image: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    banner_image: Optional[str] = None

class BlogResponse(BlogBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

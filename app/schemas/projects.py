from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: str
    tech_stack: Optional[str] = None
    project_url: Optional[str] = None
    repo_url: Optional[str] = None
    thumbnail: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    project_url: Optional[str] = None
    repo_url: Optional[str] = None
    thumbnail: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.projects import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectResponse
from app.auth.dependencies import verify_api_key_header

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectResponse])
async def get_all_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    projects = db.query(Project).filter(Project.is_active == True).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.is_active == True).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    project = db.query(Project).filter(Project.id == project_id, Project.is_active == True).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    project = db.query(Project).filter(Project.id == project_id, Project.is_active == True).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.is_active = False
    db.commit()
    return {"message": "Project deleted successfully"}

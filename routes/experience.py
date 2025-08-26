from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse
from app.auth.dependencies import verify_api_key_header

router = APIRouter()

@router.post("/", response_model=ExperienceResponse)
async def create_experience(
    experience: ExperienceCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    db_experience = Experience(**experience.dict())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience

@router.get("/", response_model=List[ExperienceResponse])
async def get_all_experiences(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    experiences = db.query(Experience).filter(Experience.is_active == True).offset(skip).limit(limit).all()
    return experiences

@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience(experience_id: int, db: Session = Depends(get_db)):
    experience = db.query(Experience).filter(Experience.id == experience_id, Experience.is_active == True).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

@router.put("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: int,
    experience_update: ExperienceUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    experience = db.query(Experience).filter(Experience.id == experience_id, Experience.is_active == True).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    update_data = experience_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(experience, field, value)
    
    db.commit()
    db.refresh(experience)
    return experience

@router.delete("/{experience_id}")
async def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    experience = db.query(Experience).filter(Experience.id == experience_id, Experience.is_active == True).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    experience.is_active = False
    db.commit()
    return {"message": "Experience deleted successfully"}

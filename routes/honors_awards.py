from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.honors_awards import HonorAward
from app.schemas.honors_awards import HonorAwardCreate, HonorAwardUpdate, HonorAwardResponse
from app.auth.dependencies import verify_api_key_header

router = APIRouter()

@router.post("/", response_model=HonorAwardResponse)
async def create_honor_award(
    honor_award: HonorAwardCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    db_honor_award = HonorAward(**honor_award.dict())
    db.add(db_honor_award)
    db.commit()
    db.refresh(db_honor_award)
    return db_honor_award

@router.get("/", response_model=List[HonorAwardResponse])
async def get_all_honors_awards(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    honors_awards = db.query(HonorAward).filter(HonorAward.is_active == True).offset(skip).limit(limit).all()
    return honors_awards

@router.get("/{honor_award_id}", response_model=HonorAwardResponse)
async def get_honor_award(honor_award_id: int, db: Session = Depends(get_db)):
    honor_award = db.query(HonorAward).filter(HonorAward.id == honor_award_id, HonorAward.is_active == True).first()
    if not honor_award:
        raise HTTPException(status_code=404, detail="Honor/Award not found")
    return honor_award

@router.put("/{honor_award_id}", response_model=HonorAwardResponse)
async def update_honor_award(
    honor_award_id: int,
    honor_award_update: HonorAwardUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    honor_award = db.query(HonorAward).filter(HonorAward.id == honor_award_id, HonorAward.is_active == True).first()
    if not honor_award:
        raise HTTPException(status_code=404, detail="Honor/Award not found")
    
    update_data = honor_award_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(honor_award, field, value)
    
    db.commit()
    db.refresh(honor_award)
    return honor_award

@router.delete("/{honor_award_id}")
async def delete_honor_award(
    honor_award_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    honor_award = db.query(HonorAward).filter(HonorAward.id == honor_award_id, HonorAward.is_active == True).first()
    if not honor_award:
        raise HTTPException(status_code=404, detail="Honor/Award not found")
    
    honor_award.is_active = False
    db.commit()
    return {"message": "Honor/Award deleted successfully"}

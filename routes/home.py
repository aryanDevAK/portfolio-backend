from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.home import Home
from app.schemas.home import HomeCreate, HomeUpdate, HomeResponse
from app.auth.dependencies import verify_api_key_header

router = APIRouter()

@router.post("/", response_model=HomeResponse)
async def create_home(
    home: HomeCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    db_home = Home(**home.dict())
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home

@router.get("/", response_model=List[HomeResponse])
async def get_all_home(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    homes = db.query(Home).filter(Home.is_active == True).offset(skip).limit(limit).all()
    return homes

@router.get("/{home_id}", response_model=HomeResponse)
async def get_home(home_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id, Home.is_active == True).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home record not found")
    return home

@router.put("/{home_id}", response_model=HomeResponse)
async def update_home(
    home_id: int,
    home_update: HomeUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    home = db.query(Home).filter(Home.id == home_id, Home.is_active == True).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home record not found")
    
    update_data = home_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(home, field, value)
    
    db.commit()
    db.refresh(home)
    return home

@router.delete("/{home_id}")
async def delete_home(
    home_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    home = db.query(Home).filter(Home.id == home_id, Home.is_active == True).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home record not found")
    
    home.is_active = False
    db.commit()
    return {"message": "Home record deleted successfully"}

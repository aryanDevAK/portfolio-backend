from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.certifications import Certification
from app.schemas.certifications import CertificationCreate, CertificationUpdate, CertificationResponse
from app.auth.dependencies import verify_api_key_header

router = APIRouter()

@router.post("/", response_model=CertificationResponse)
async def create_certification(
    certification: CertificationCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    db_certification = Certification(**certification.dict())
    db.add(db_certification)
    db.commit()
    db.refresh(db_certification)
    return db_certification

@router.get("/", response_model=List[CertificationResponse])
async def get_all_certifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    certifications = db.query(Certification).filter(Certification.is_active == True).offset(skip).limit(limit).all()
    return certifications

@router.get("/{certification_id}", response_model=CertificationResponse)
async def get_certification(certification_id: int, db: Session = Depends(get_db)):
    certification = db.query(Certification).filter(Certification.id == certification_id, Certification.is_active == True).first()
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification

@router.put("/{certification_id}", response_model=CertificationResponse)
async def update_certification(
    certification_id: int,
    certification_update: CertificationUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    certification = db.query(Certification).filter(Certification.id == certification_id, Certification.is_active == True).first()
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    
    update_data = certification_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(certification, field, value)
    
    db.commit()
    db.refresh(certification)
    return certification

@router.delete("/{certification_id}")
async def delete_certification(
    certification_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    certification = db.query(Certification).filter(Certification.id == certification_id, Certification.is_active == True).first()
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    
    certification.is_active = False
    db.commit()
    return {"message": "Certification deleted successfully"}

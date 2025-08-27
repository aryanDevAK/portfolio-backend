from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.services import Service
from app.schemas.services import ServiceCreate, ServiceUpdate, ServiceResponse
from app.auth.dependencies import verify_api_key_header

router = APIRouter()

@router.post("/", response_model=ServiceResponse)
async def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.get("/", response_model=List[ServiceResponse])
async def get_all_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    services = db.query(Service).filter(Service.is_active == True).offset(skip).limit(limit).all()
    return services

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id, Service.is_active == True).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_update: ServiceUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    service = db.query(Service).filter(Service.id == service_id, Service.is_active == True).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    update_data = service_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    
    db.commit()
    db.refresh(service)
    return service

@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    service = db.query(Service).filter(Service.id == service_id, Service.is_active == True).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service.is_active = False
    db.commit()
    return {"message": "Service deleted successfully"}

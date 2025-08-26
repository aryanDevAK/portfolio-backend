from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from app.auth.dependencies import verify_api_key_header
from app.config import settings

router = APIRouter()

async def send_contact_email(contact_data: ContactCreate):
    """Send contact form submission via email"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.mail_from
        msg['To'] = "aryankhatri.forwork@gmail.com"
        msg['Subject'] = f"Portfolio Contact: {contact_data.subject}"
        
        # Email body
        body = f"""
        New contact form submission:
        
        Name: {contact_data.name}
        Email: {contact_data.email}
        Subject: {contact_data.subject}
        
        Message:
        {contact_data.message}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(settings.mail_server, settings.mail_port)
        server.starttls()
        server.login(settings.mail_username, settings.mail_password)
        text = msg.as_string()
        server.sendmail(settings.mail_from, "aryankhatri.forwork@gmail.com", text)
        server.quit()
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

@router.post("/", response_model=ContactResponse)
async def create_contact(
    contact: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save to database
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    # Send email in background
    background_tasks.add_task(send_contact_email, contact)
    
    return db_contact

@router.get("/", response_model=List[ContactResponse])
async def get_all_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    contacts = db.query(Contact).filter(Contact.is_active == True).offset(skip).limit(limit).all()
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.is_active == True).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.is_active == True).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    update_data = contact_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.is_active == True).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    contact.is_active = False
    db.commit()
    return {"message": "Contact deleted successfully"}

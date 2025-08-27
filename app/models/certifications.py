from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date
from sqlalchemy.sql import func
from app.database import Base

class Certification(Base):
    __tablename__ = "certifications"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(Text, nullable=False)
    issuer = Column(Text, nullable=False)
    issue_date = Column(Date, nullable=False)
    credential_id = Column(Text, nullable=True)
    credential_url = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

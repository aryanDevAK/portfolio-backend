from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date
from sqlalchemy.sql import func
from app.database import Base

class Experience(Base):
    __tablename__ = "experience"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
    location = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Nullable for ongoing positions
    description = Column(Text, nullable=True)
    logo = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

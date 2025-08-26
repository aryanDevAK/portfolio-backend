from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.database import engine, Base
from app.auth.dependencies import verify_api_key
from app.routes import (
    home, certifications, honors_awards, experience, 
    projects, services, blogs, contact, upload
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio Backend API",
    description="Complete backend for personal portfolio website",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Mount static files for media serving
app.mount("/media", StaticFiles(directory="uploads"), name="media")

# Include routers
app.include_router(home.router, prefix="/api/home", tags=["Home"])
app.include_router(certifications.router, prefix="/api/certifications", tags=["Certifications"])
app.include_router(honors_awards.router, prefix="/api/honors-awards", tags=["Honors & Awards"])
app.include_router(experience.router, prefix="/api/experience", tags=["Experience"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(blogs.router, prefix="/api/blogs", tags=["Blogs"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])

@app.get("/")
async def root():
    return {"message": "Portfolio Backend API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

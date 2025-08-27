from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.blogs import Blog
from app.schemas.blogs import BlogCreate, BlogUpdate, BlogResponse
from app.auth.dependencies import verify_api_key_header

router = APIRouter()

@router.post("/", response_model=BlogResponse)
async def create_blog(
    blog: BlogCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    # Check if slug already exists
    existing_blog = db.query(Blog).filter(Blog.slug == blog.slug, Blog.is_active == True).first()
    if existing_blog:
        raise HTTPException(status_code=400, detail="Blog with this slug already exists")
    
    db_blog = Blog(**blog.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

@router.get("/", response_model=List[BlogResponse])
async def get_all_blogs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    blogs = db.query(Blog).filter(Blog.is_active == True).offset(skip).limit(limit).all()
    return blogs

@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id, Blog.is_active == True).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.get("/slug/{slug}", response_model=BlogResponse)
async def get_blog_by_slug(slug: str, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.slug == slug, Blog.is_active == True).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int,
    blog_update: BlogUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    blog = db.query(Blog).filter(Blog.id == blog_id, Blog.is_active == True).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Check if new slug conflicts with existing blogs
    if blog_update.slug and blog_update.slug != blog.slug:
        existing_blog = db.query(Blog).filter(Blog.slug == blog_update.slug, Blog.is_active == True).first()
        if existing_blog:
            raise HTTPException(status_code=400, detail="Blog with this slug already exists")
    
    update_data = blog_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(blog, field, value)
    
    db.commit()
    db.refresh(blog)
    return blog

@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key_header)
):
    blog = db.query(Blog).filter(Blog.id == blog_id, Blog.is_active == True).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    blog.is_active = False
    db.commit()
    return {"message": "Blog deleted successfully"}

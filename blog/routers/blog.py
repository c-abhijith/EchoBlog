from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import cloudinary
import cloudinary.uploader

from blog.database import get_db
from blog.models import Blog, User
from blog.schemas.blog import BlogCreate, BlogResponse, BlogUpdate
from blog.utils import get_current_user
from config import settings

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: str,
    description: str,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result.get("secure_url")

        # Create new blog
        new_blog = Blog(
            title=title,
            description=description,
            image_url=image_url,
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        
        return new_blog
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.get("/", response_model=List[BlogResponse])
async def list_blogs(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Blog)
        
        if search:
            query = query.filter(Blog.title.ilike(f"%{search}%"))
        
        blogs = query.order_by(Blog.created_at.desc()).offset(skip).limit(limit).all()
        return blogs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Blog not found"}
            )
        return blog
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Blog not found"}
            )
            
        if blog.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"status": "error", "message": "Not authorized to update this blog"}
            )

        if title:
            blog.title = title
        if description:
            blog.description = description
        if image:
            # Upload new image to Cloudinary
            upload_result = cloudinary.uploader.upload(image.file)
            blog.image_url = upload_result.get("secure_url")

        blog.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(blog)
        
        return blog
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Blog not found"}
            )
            
        if blog.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"status": "error", "message": "Not authorized to delete this blog"}
            )

        # Delete image from Cloudinary if exists
        if blog.image_url:
            public_id = blog.image_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)

        db.delete(blog)
        db.commit()
        
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.get("/user/{user_id}", response_model=List[BlogResponse])
async def get_user_blogs(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        blogs = db.query(Blog)\
            .filter(Blog.user_id == user_id)\
            .order_by(Blog.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        return blogs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        ) 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from blog.database import get_db
from blog.models import Comment, Blog, User
from blog.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from blog.utils import get_current_user

router = APIRouter(
    prefix="/blogs/{blog_id}/comments",
    tags=["Comments"]
)

@router.post("/", response_model=CommentResponse)
async def create_comment(
    blog_id: UUID,
    comment: CommentCreate,
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

        new_comment = Comment(
            content=comment.content,
            blog_id=blog_id,
            user_id=current_user.id
        )
        
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
        return new_comment
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.get("/", response_model=List[CommentResponse])
async def list_comments(
    blog_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        comments = db.query(Comment).filter(Comment.blog_id == blog_id).all()
        
        # Add like information
        for comment in comments:
            comment.like_count = db.query(Like).filter(Like.comment_id == comment.id).count()
            comment.is_liked_by_user = db.query(Like).filter(
                Like.comment_id == comment.id,
                Like.user_id == current_user.id
            ).first() is not None
            
        return comments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        ) 
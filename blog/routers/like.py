from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from blog.database import get_db
from blog.models import Like, Blog, Comment, User
from blog.utils import get_current_user

router = APIRouter(
    tags=["Likes"]
)

@router.post("/blogs/{blog_id}/like")
async def like_blog(
    blog_id: UUID,
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

        # Check if already liked
        existing_like = db.query(Like).filter(
            Like.blog_id == blog_id,
            Like.user_id == current_user.id
        ).first()
        
        if existing_like:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "error", "message": "Blog already liked"}
            )

        new_like = Like(
            user_id=current_user.id,
            blog_id=blog_id
        )
        
        db.add(new_like)
        db.commit()
        
        return {"status": "success", "message": "Blog liked successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": "Already liked"}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.delete("/blogs/{blog_id}/unlike")
async def unlike_blog(
    blog_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        like = db.query(Like).filter(
            Like.blog_id == blog_id,
            Like.user_id == current_user.id
        ).first()
        
        if not like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Like not found"}
            )

        db.delete(like)
        db.commit()
        
        return {"status": "success", "message": "Blog unliked successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.post("/comments/{comment_id}/like")
async def like_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Comment not found"}
            )

        existing_like = db.query(Like).filter(
            Like.comment_id == comment_id,
            Like.user_id == current_user.id
        ).first()
        
        if existing_like:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "error", "message": "Comment already liked"}
            )

        new_like = Like(
            user_id=current_user.id,
            comment_id=comment_id
        )
        
        db.add(new_like)
        db.commit()
        
        return {"status": "success", "message": "Comment liked successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        )

@router.delete("/comments/{comment_id}/unlike")
async def unlike_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        like = db.query(Like).filter(
            Like.comment_id == comment_id,
            Like.user_id == current_user.id
        ).first()
        
        if not like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Like not found"}
            )

        db.delete(like)
        db.commit()
        
        return {"status": "success", "message": "Comment unliked successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": str(e)}
        ) 
from fastapi import APIRouter, Depends, HTTPException, status
from blog.dependencies import get_current_user
from blog.models import User
from typing import List
from blog.schemas import UserBase,UserUpdate
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.repository.error_response import *
from uuid import UUID

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("",  response_model=List[UserBase],status_code=status.HTTP_200_OK)
async def user(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise_error(e)
        
@router.get("/details", response_model=UserBase,status_code=status.HTTP_200_OK)
async def get__details(db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
        user = db. query(User).filter(User.id==current_user.id).first()
        if not user:
            raise_404()
        return user
    except Exception as e:
        raise_error(e)

@router.get("/details/{user_id}", response_model=UserBase,status_code=status.HTTP_200_OK)
async def get_user_details(user_id:UUID,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
        user = db. query(User).filter(User.id==user_id).first()
        if not user:
            raise_404()
        return user("/det")
    except Exception as e:
        raise_error(e)

@router.get("/details/{user_id}", response_model=UserBase,status_code=status.HTTP_200_OK)
async def get_user_details(user_id:UUID,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
        user = db. query(User).filter(User.id==user_id).first()
        if not user:
            raise_404()
        return user("/det")
    except Exception as e:
        raise_error(e)


@router.put("/details", response_model=UserBase,status_code=status.HTTP_200_OK)
async def get_user_update(user_update: UserUpdate,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
        if current_user.id != current_user.id:
            raise_403()
        user = db.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise_404()
        if user_update.bio is not None:
            user.bio = user_update.bio
        if user_update.title is not None:
            user.title = user_update.title
        if user_update.twitter_url is not None:
            user.twitter_url = user_update.twitter_url
        if user_update.instagram_url is not None:
            user.instagram_url = user_update.instagram_url
        if user_update.linkedin_url is not None:
                user.linkedin_url = user_update.linkedin_url
                
        db.commit()
        db.refresh(user)
        
        return user
    except Exception as e:
        raise_error(e)


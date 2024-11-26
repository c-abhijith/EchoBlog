from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.models import User
from blog.schemas import UserCreate, UserLogin, Token, RefreshToken,SuccessResponse
from blog.utils import (get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_token
)
from blog.repository.auth_validation import signup_validation
from blog.repository.success_response import *
from blog.repository.error_response import *

router = APIRouter(
    tags=["/auth"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED,response_model=SuccessResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = signup_validation(user, db)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return singup_response(new_user)
    except Exception as e:
        db.rollback()
        raise_error(e)

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user:
            raise_400("username")
        if not verify_password(user.password, db_user.password):
            raise_400("password")
        
        token_data = {
            "sub": db_user.username,
            "user_id": str(db_user.id),
            "role": db_user.role.value
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return login_response(access_token,refresh_token)
    except Exception as e:
        raise_error(e)
        
@router.post("/refresh", response_model=Token)
async def refresh_token(token: RefreshToken, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token.refresh_token, "refresh")
        
        db_user = db.query(User).filter(User.username == payload["sub"]).first()
        if not db_user:
            raise_401()
    
        token_data = {
            "sub": db_user.username,
            "user_id": str(db_user.id),
            "role": db_user.role.value
        }
        
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        return login_response(new_access_token,new_refresh_token)
    except Exception as e:
        raise_error(e)
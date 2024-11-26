from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.models import User
from blog.schemas import UserCreate, UserLogin, Token, RefreshToken
from blog.utils import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_token
)
from blog.repository.auth_validation import signup_validation

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = signup_validation(user, db)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "status": "success",
            "message": "User registered successfully",
            "data": {
                "id": str(new_user.id),
                "username": new_user.username,
                "role": new_user.role
            }
        }
    except HTTPException as error:
        raise error
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "An unexpected error occurred",
                "error": str(e)
            }
        )

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "status": "error",
                    "message": "Invalid credentials",
                    "field": "username"
                }
            )
        
        if not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "status": "error",
                    "message": "Invalid credentials",
                    "field": "password"
                }
            )
        
        # Create token data
        token_data = {
            "sub": db_user.username,
            "user_id": str(db_user.id),
            "role": db_user.role.value
        }
        
        # Generate both tokens
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return {
            "status": "success",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "An unexpected error occurred",
                "error": str(e)
            }
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(token: RefreshToken, db: Session = Depends(get_db)):
    try:
        # Verify refresh token
        payload = verify_token(token.refresh_token, "refresh")
        
        # Get user from database
        db_user = db.query(User).filter(User.username == payload["sub"]).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "status": "error",
                    "message": "User not found"
                }
            )
        
        # Create new token data
        token_data = {
            "sub": db_user.username,
            "user_id": str(db_user.id),
            "role": db_user.role.value
        }
        
        # Generate new tokens
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        return {
            "status": "success",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "An unexpected error occurred",
                "error": str(e)
            }
        )

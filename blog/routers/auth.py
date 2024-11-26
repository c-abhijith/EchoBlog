from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.schemas import UserCreate
from blog.models import User, UserRole
from blog.utils import get_password_hash
import uuid

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=dict)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if phone number already exists
    if db.query(User).filter(User.phonenumber == user.phonenumber).first():
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered"
        )
    
    # Create new user with default role
    db_user = User(
        id=uuid.uuid4(),
        username=user.username,
        phonenumber=user.phonenumber,
        password=get_password_hash(user.password),
        role=UserRole.user,  # Default role
        followers=[],
        following=[],
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "message": "User created successfully",
            "username": db_user.username,
            "role": db_user.role
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        ) 
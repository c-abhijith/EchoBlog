from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog.models import User, UserRole
from blog.schemas import UserCreate
from blog.utils import get_password_hash
import uuid

def signup_validation(user: UserCreate, db: Session):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Username already exists",
                "field": "username"
            }
        )
    if db.query(User).filter(User.phonenumber == user.phonenumber).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Phone number already exists",
                "field": "phonenumber"
            }
        )

    if user.role not in [role.value for role in UserRole]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": f"Invalid role. Must be one of: {[role.value for role in UserRole]}",
                "field": "role"
            }
        )

    try:
        new_user = User(
            id=uuid.uuid4(),
            username=user.username,
            phonenumber=user.phonenumber,
            password=get_password_hash(user.password),
            role=user.role,
            followers=[],
            following=[]
        )
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Error creating user",
                "error": str(e)
            }
        )
from fastapi import APIRouter, Depends, HTTPException, status
from blog.dependencies import get_current_user
from blog.models import User
from typing import Dict

router = APIRouter(
    prefix="/home",
    tags=["Home"]
)

@router.get("/", 
    response_model=Dict,
    description="Welcome message for authenticated users"
)
async def home(current_user: User = Depends(get_current_user)):
    try:
        return {
            "status": "success",
            "message": f"Welcome {current_user.username}!",
            "data": {
                "user": {
                    "id": str(current_user.id),
                    "username": current_user.username,
                    "role": current_user.role.value,
                    "verified": current_user.verified
                }
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "An unexpected error occurred",
                "error": str(e)
            }
        ) 
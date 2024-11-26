from fastapi import HTTPException, status

def raise_error(exception: Exception):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "status": "error",
            "message": "An unexpected error occurred",
            "error": str(exception)  
        }
    )

def raise_400(message):
    raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "status": "error",
                    "message": "Invalid credentials",
                    "field": message
                }
            )

def raise_401():
    raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "status": "error",
                    "message": "User not found"
                }
            )
def raise_404():
    raise HTTPException(
                status_code=404,
                detail="User not found"
            )

def raise_403():
    raise HTTPException(
                status_code=403,
                detail="You are not authorized to update this user's details"
            )
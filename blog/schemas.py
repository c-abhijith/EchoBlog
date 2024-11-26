from pydantic import BaseModel, Field, constr
import re

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    phonenumber: str = Field(..., regex=r"^\+?[1-9]\d{1,14}$")  # E.164 format
    password: constr(min_length=8, regex=r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}") 

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "phonenumber": "+1234567890",
                "password": "Secure@1234",
            }
        }
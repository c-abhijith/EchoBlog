from pydantic import BaseModel, Field
from blog.models import UserRole
from typing import Optional

class UserCreate(BaseModel):
    username: str
    phonenumber: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None
    user_id: str | None = None
    role: str | None = None
    token_type: str | None = None

class RefreshToken(BaseModel):
    refresh_token: str

from pydantic import BaseModel, HttpUrl
from blog.models import UserRole
from typing import Optional,List
from uuid import UUID
from typing import Any



class SuccessResponse(BaseModel):
    message: str
    data: Any

    class Config:
        from_attributes = True
        
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
    
class BlogBase(BaseModel):
    id: UUID
    title: str
    content: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: UUID
    username: str
    phonenumber: str
    role: str
    bio: Optional[str] = None
    title: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    verified: bool


    blog: List[BlogBase] = []

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    linkedin_url: Optional[str] = None
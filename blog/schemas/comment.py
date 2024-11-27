from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: UUID
    user_id: UUID
    blog_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    like_count: int = 0
    is_liked_by_user: bool = False

    class Config:
        from_attributes = True 
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Text, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from blog.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class LikeType(str, enum.Enum):
    blog = "blog"
    comment = "comment"



class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    phonenumber = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    followers = Column(ARRAY(UUID(as_uuid=True)), default=[])
    following = Column(ARRAY(UUID(as_uuid=True)), default=[])
    bio = Column(Text, nullable=True)
    title = Column(String, nullable=True)
    twitter_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    
    blog = relationship("Blog", back_populates="user")


class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    user =relationship("User", back_populates="blog")


class Like(Base):
    __tablename__ = "likes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(Enum(LikeType), nullable=False)
    type_id = Column(UUID(as_uuid=True), nullable=False) 


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    comment_text = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id"), nullable=False)

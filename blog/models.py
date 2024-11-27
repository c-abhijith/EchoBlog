import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Text, Enum, ARRAY,DateTime, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from blog.database import Base
import enum
from datetime import datetime


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
    otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    
    blog = relationship("Blog", back_populates="user")


class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    user = relationship("User", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="blog", cascade="all, delete-orphan")


class Like(Base):
    __tablename__ = "likes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id"), nullable=True)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    
    user = relationship("User", back_populates="likes")
    blog = relationship("Blog", back_populates="likes")
    comment = relationship("Comment", back_populates="likes")

    __table_args__ = (
        # Ensure user can only like a blog once
        UniqueConstraint('user_id', 'blog_id', name='unique_blog_like'),
        # Ensure user can only like a comment once
        UniqueConstraint('user_id', 'comment_id', name='unique_comment_like'),
    )


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id"), nullable=False)
    
    user = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    likes = relationship("Like", back_populates="comment", cascade="all, delete-orphan")

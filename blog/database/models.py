class User(Base):
    __tablename__ = "users"
    
    # ... other fields ...
    otp = Column(String)
    verified = Column(Boolean, default=False) 
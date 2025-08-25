from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

# User registration schema
class UserSignup(BaseModel):
    name: str
    email: str
    organization_name: str
    domain: str
    location: str
    organization_url: Optional[str] = None
    password: str

# User login schema
class UserLogin(BaseModel):
    email: str
    password: str

# User response schema (without password)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    organization_name: str
    domain: str
    location: str
    organization_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Token response schema
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Message response schema
class MessageResponse(BaseModel):
    message: str
    success: bool = True

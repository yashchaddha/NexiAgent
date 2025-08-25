from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from the root directory
load_dotenv("../.env")

# Import local modules
from database import get_db, engine, Base
from models import User
from schemas import UserSignup, UserLogin, UserResponse, TokenResponse, MessageResponse
from auth import get_password_hash, verify_password, create_access_token, verify_token

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app for authentication
auth_app = FastAPI(title="ISO 27001:2022 Auditor Authentication", version="1.0.0")

# Add CORS middleware
auth_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme for JWT tokens
security = HTTPBearer()

# Dependency to get current user from token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

# Root endpoint
@auth_app.get("/")
async def root():
    return {"message": "ISO 27001:2022 Auditor Authentication API"}

# User signup endpoint
@auth_app.post("/signup", response_model=MessageResponse)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        organization_name=user_data.organization_name,
        domain=user_data.domain,
        location=user_data.location,
        organization_url=user_data.organization_url,
        password_hash=hashed_password
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return MessageResponse(
            message="User registered successfully",
            success=True
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

# User login endpoint
@auth_app.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    
    # Find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # Create user response (without password)
    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        organization_name=user.organization_name,
        domain=user.domain,
        location=user.location,
        organization_url=user.organization_url,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

# Get current user profile
@auth_app.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's profile"""
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        organization_name=current_user.organization_name,
        domain=current_user.domain,
        location=current_user.location,
        organization_url=current_user.organization_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

# Update user profile
@auth_app.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserSignup,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    
    # Check if email is being changed and if it's already taken
    if user_data.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken by another user"
            )
    
    # Update user fields
    current_user.name = user_data.name
    current_user.email = user_data.email
    current_user.organization_name = user_data.organization_name
    current_user.domain = user_data.domain
    current_user.location = user_data.location
    current_user.organization_url = user_data.organization_url
    
    # Update password if provided
    if user_data.password:
        current_user.password_hash = get_password_hash(user_data.password)
    
    try:
        db.commit()
        db.refresh(current_user)
        
        return UserResponse(
            id=current_user.id,
            name=current_user.name,
            email=current_user.email,
            organization_name=current_user.organization_name,
            domain=current_user.domain,
            location=current_user.location,
            organization_url=current_user.organization_url,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}"
        )

# Delete user account
@auth_app.delete("/profile", response_model=MessageResponse)
async def delete_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete current user's account"""
    
    try:
        db.delete(current_user)
        db.commit()
        
        return MessageResponse(
            message="User account deleted successfully",
            success=True
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting account: {str(e)}"
        )

# Health check endpoint
@auth_app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ISO 27001:2022 Auditor Authentication",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(auth_app, host="0.0.0.0", port=8001)

"""
Shared dependencies and utilities for the ISO 27001:2022 Auditor Agent
"""

import os
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Import authentication utilities
from auth import verify_token

# Load environment variables
load_dotenv()

# Security scheme for JWT tokens
security = HTTPBearer()

# Dependency to get current user from token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
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
    
    return user_id

# Initialize OpenAI model
def get_llm():
    """Get the OpenAI language model instance"""
    return ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )

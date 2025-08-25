"""
Main FastAPI application for ISO 27001:2022 Auditor Agent
This file now serves as the entry point and orchestrates the modular components
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our modular components
from api_routes import router

# Create FastAPI application
app = FastAPI(
    title="ISO 27001:2022 Auditor Agent", 
    version="1.0.0",
    description="Expert ISO 27001:2022 compliance guidance with user-specific memory"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "ISO 27001:2022 Auditor Agent API",
        "version": "1.0.0",
        "features": [
            "User-specific memory and conversation history",
            "ISO 27001:2022 compliance guidance",
            "Learning progress tracking",
            "Session management"
        ],
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ISO 27001:2022 Auditor Agent",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

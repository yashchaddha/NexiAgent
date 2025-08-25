"""
API Routes for ISO 27001:2022 Auditor Agent
Contains all the endpoint handlers and business logic
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
from datetime import datetime

from dependencies import get_current_user
from database import get_db
from conversation_service import UserConversationService
from agent_graph import app_state, AgentState

# Create router
router = APIRouter()

# API Models
class QueryRequest(BaseModel):
    query: str
    session_id: str = ""

class QueryResponse(BaseModel):
    response: str
    query: str
    session_id: str
    conversation_history: List[Dict[str, str]] = []

class SessionResponse(BaseModel):
    session_id: str
    message: str

# API Endpoints
@router.get("/")
async def root():
    return {"message": "ISO 27001:2022 Auditor Agent API with User-Specific Memory"}

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest, 
    current_user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    """Process a query about ISO 27001:2022 compliance with user-specific memory"""
    
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Initialize conversation service
        conversation_service = UserConversationService(db)
        
        # Get or create user-specific memory for this session
        memory = conversation_service.create_user_memory(current_user_id, request.session_id, k=20)
        
        # Get user's conversation summary for context
        conversation_summary = conversation_service.get_user_conversation_summary(current_user_id, request.session_id)
        
        # Initialize state with user-specific memory
        initial_state = AgentState(
            session_id=request.session_id,
            current_query=request.query,
            response="",
            conversation_history=[],
            memory=memory
        )
        
        # Execute the workflow
        result = app_state.invoke(initial_state)
        
        # Extract response from result
        if hasattr(result, 'response'):
            response_text = result.response
        elif isinstance(result, dict) and 'response' in result:
            response_text = result['response']
        elif hasattr(result, '__dict__'):
            response_text = getattr(result, 'response', str(result))
        else:
            response_text = str(result)
        
        # Store the conversation in database
        conversation_service.store_conversation(
            user_id=current_user_id,
            session_id=request.session_id,
            query=request.query,
            response=response_text
        )
        
        # Get updated conversation history for this session
        session_conversations = conversation_service.get_session_conversations(current_user_id, request.session_id)
        conversation_history = [
            {
                "role": "user" if i % 2 == 0 else "assistant",
                "content": conv.query if i % 2 == 0 else conv.response,
                "timestamp": conv.timestamp.isoformat()
            }
            for i, conv in enumerate(session_conversations)
        ]
        
        return QueryResponse(
            response=response_text,
            query=request.query,
            session_id=request.session_id,
            conversation_history=conversation_history
        )
        
    except Exception as e:
        print(f"DEBUG: Exception occurred: {e}")
        print(f"DEBUG: Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/session/new", response_model=SessionResponse)
async def create_new_session():
    """Create a new conversation session"""
    session_id = str(uuid.uuid4())
    return SessionResponse(
        session_id=session_id,
        message="New session created successfully"
    )

@router.get("/session/{session_id}/history")
async def get_session_history(
    session_id: str, 
    current_user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get conversation history for a specific user session"""
    conversation_service = UserConversationService(db)
    
    # Get conversations for this user and session
    conversations = conversation_service.get_session_conversations(current_user_id, session_id)
    
    if not conversations:
        raise HTTPException(status_code=404, detail="Session not found or no conversations")
    
    # Format conversation history
    conversation_history = [
        {
            "role": "user" if i % 2 == 0 else "assistant",
            "content": conv.query if i % 2 == 0 else conv.response,
            "timestamp": conv.timestamp.isoformat()
        }
        for i, conv in enumerate(conversations)
    ]
    
    return {
        "session_id": session_id,
        "conversation_history": conversation_history,
        "created_at": conversations[0].timestamp.isoformat() if conversations else None,
        "total_exchanges": len(conversations)
    }

@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str, 
    current_user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    """Delete a conversation session for the current user"""
    conversation_service = UserConversationService(db)
    
    try:
        success = conversation_service.delete_user_session(current_user_id, session_id)
        if success:
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

@router.get("/sessions")
async def list_sessions(
    current_user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    """List all conversation sessions for the current user"""
    conversation_service = UserConversationService(db)
    
    # Get all conversations for the user
    all_conversations = conversation_service.get_user_conversations(current_user_id, limit=100)
    
    # Group by session
    sessions = {}
    for conv in all_conversations:
        if conv.session_id not in sessions:
            sessions[conv.session_id] = {
                "session_id": conv.session_id,
                "created_at": conv.timestamp.isoformat(),
                "message_count": 0,
                "last_activity": conv.timestamp.isoformat()
            }
        sessions[conv.session_id]["message_count"] += 1
        if conv.timestamp > datetime.fromisoformat(sessions[conv.session_id]["last_activity"].replace('Z', '+00:00')):
            sessions[conv.session_id]["last_activity"] = conv.timestamp.isoformat()
    
    return {"sessions": list(sessions.values())}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "ISO 27001:2022 Auditor Agent with User-Specific Memory",
        "active_sessions": 0  # This will be updated when we remove the old conversation_sessions
    }

@router.get("/user/progress")
async def get_user_progress(
    current_user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get user's learning progress and conversation summary"""
    conversation_service = UserConversationService(db)
    
    try:
        progress = conversation_service.get_user_learning_progress(current_user_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user progress: {str(e)}")

@router.get("/user/sessions/{session_id}/summary")
async def get_session_summary(
    session_id: str,
    current_user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get a summary of a specific user session"""
    conversation_service = UserConversationService(db)
    
    try:
        summary = conversation_service.get_user_conversation_summary(current_user_id, session_id)
        return {
            "session_id": session_id,
            "user_id": current_user_id,
            **summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session summary: {str(e)}")

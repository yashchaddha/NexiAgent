from sqlalchemy.orm import Session
from models import UserConversation, User
from langchain.memory import ConversationBufferWindowMemory
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class UserConversationService:
    """Service for managing user conversations and memory"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def store_conversation(self, user_id: int, session_id: str, query: str, response: str) -> UserConversation:
        """Store a new conversation exchange for a user"""
        conversation = UserConversation(
            user_id=user_id,
            session_id=session_id,
            query=query,
            response=response,
            timestamp=datetime.now()
        )
        
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation
    
    def get_user_conversations(self, user_id: int, limit: int = 50) -> List[UserConversation]:
        """Get recent conversations for a specific user"""
        return self.db.query(UserConversation)\
            .filter(UserConversation.user_id == user_id)\
            .order_by(UserConversation.timestamp.desc())\
            .limit(limit)\
            .all()
    
    def get_session_conversations(self, user_id: int, session_id: str) -> List[UserConversation]:
        """Get conversations for a specific session of a user"""
        return self.db.query(UserConversation)\
            .filter(
                UserConversation.user_id == user_id,
                UserConversation.session_id == session_id
            )\
            .order_by(UserConversation.timestamp.asc())\
            .all()
    
    def create_user_memory(self, user_id: int, session_id: str, k: int = 20) -> ConversationBufferWindowMemory:
        """Create a memory instance for a specific user session"""
        memory = ConversationBufferWindowMemory(
            k=k,
            return_messages=True,
            memory_key="chat_history"
        )
        
        # Load previous conversations into memory
        conversations = self.get_session_conversations(user_id, session_id)
        
        for conv in conversations:
            # Add user message
            memory.chat_memory.add_user_message(conv.query)
            # Add AI response
            memory.chat_memory.add_ai_message(conv.response)
        
        return memory
    
    def get_user_conversation_summary(self, user_id: int, session_id: str) -> Dict[str, Any]:
        """Get a summary of user's conversation for context"""
        conversations = self.get_session_conversations(user_id, session_id)
        
        if not conversations:
            return {
                "total_exchanges": 0,
                "session_start": None,
                "topics_discussed": [],
                "compliance_focus": None
            }
        
        # Analyze conversation topics
        topics = []
        compliance_keywords = [
            "risk assessment", "control", "policy", "procedure", "audit",
            "compliance", "security", "incident", "business continuity",
            "access control", "data protection", "asset management"
        ]
        
        compliance_focus = None
        for conv in conversations:
            query_lower = conv.query.lower()
            response_lower = conv.response.lower()
            
            # Check for compliance topics
            for keyword in compliance_keywords:
                if keyword in query_lower or keyword in response_lower:
                    if keyword not in topics:
                        topics.append(keyword)
            
            # Determine primary compliance focus
            if "risk assessment" in query_lower or "risk assessment" in response_lower:
                compliance_focus = "Risk Assessment"
            elif "control" in query_lower or "control" in response_lower:
                compliance_focus = "Control Implementation"
            elif "policy" in query_lower or "policy" in response_lower:
                compliance_focus = "Policy Development"
            elif "audit" in query_lower or "audit" in response_lower:
                compliance_focus = "Audit Preparation"
        
        return {
            "total_exchanges": len(conversations),
            "session_start": conversations[0].timestamp.isoformat() if conversations else None,
            "topics_discussed": topics[:10],  # Top 10 topics
            "compliance_focus": compliance_focus,
            "recent_queries": [conv.query[:100] + "..." if len(conv.query) > 100 else conv.query 
                              for conv in conversations[-5:]]  # Last 5 queries
        }
    
    def delete_user_session(self, user_id: int, session_id: str) -> bool:
        """Delete all conversations for a specific user session"""
        try:
            conversations = self.db.query(UserConversation)\
                .filter(
                    UserConversation.user_id == user_id,
                    UserConversation.session_id == session_id
                ).all()
            
            for conv in conversations:
                self.db.delete(conv)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_user_learning_progress(self, user_id: int) -> Dict[str, Any]:
        """Get user's learning progress based on conversation history"""
        all_conversations = self.get_user_conversations(user_id, limit=100)
        
        if not all_conversations:
            return {
                "total_conversations": 0,
                "learning_level": "Beginner",
                "topics_covered": [],
                "suggested_next_steps": []
            }
        
        # Analyze learning progress
        topics_covered = set()
        for conv in all_conversations:
            query_lower = conv.query.lower()
            response_lower = conv.response.lower()
            
            # Extract topics from conversations
            if "risk assessment" in query_lower or "risk assessment" in response_lower:
                topics_covered.add("Risk Assessment")
            if "control" in query_lower or "control" in response_lower:
                topics_covered.add("Control Implementation")
            if "policy" in query_lower or "policy" in response_lower:
                topics_covered.add("Policy Development")
            if "audit" in query_lower or "audit" in response_lower:
                topics_covered.add("Audit Preparation")
            if "incident" in query_lower or "incident" in response_lower:
                topics_covered.add("Incident Management")
            if "business continuity" in query_lower or "business continuity" in response_lower:
                topics_covered.add("Business Continuity")
        
        # Determine learning level
        total_topics = len(topics_covered)
        if total_topics <= 2:
            learning_level = "Beginner"
        elif total_topics <= 5:
            learning_level = "Intermediate"
        else:
            learning_level = "Advanced"
        
        # Suggest next steps
        all_possible_topics = [
            "Risk Assessment", "Control Implementation", "Policy Development",
            "Audit Preparation", "Incident Management", "Business Continuity",
            "Asset Management", "Access Control", "Data Protection", "Training & Awareness"
        ]
        
        suggested_next_steps = [topic for topic in all_possible_topics if topic not in topics_covered]
        
        return {
            "total_conversations": len(all_conversations),
            "learning_level": learning_level,
            "topics_covered": list(topics_covered),
            "suggested_next_steps": suggested_next_steps[:3]  # Top 3 suggestions
        }

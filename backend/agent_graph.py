"""
ISO 27001:2022 Auditor Agent Graph
Contains the LangGraph workflow and agent logic
"""

from pydantic import BaseModel
from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import json
from datetime import datetime

from knowledge_base import ISO_27001_KNOWLEDGE
from dependencies import get_llm

# In-memory storage for conversation sessions (will be replaced with database)
# This is kept for backward compatibility during transition
conversation_sessions = {}

# Define the state structure with memory
class AgentState(BaseModel):
    session_id: str = ""
    current_query: str = ""
    response: str = ""
    conversation_history: List[Dict[str, str]] = []
    memory: Any = None

# Define the ISO 27001 auditor node with memory
def iso_27001_auditor_node(state: AgentState) -> AgentState:
    """Node responsible for answering ISO 27001:2022 compliance queries with user-specific memory"""
    
    query = state.current_query.lower()
    
    # Get conversation context from user-specific memory
    conversation_context = ""
    user_context = ""
    
    if state.memory and hasattr(state.memory, 'chat_memory'):
        # Get recent conversation history from user's memory
        recent_messages = state.memory.chat_memory.messages[-10:]  # Last 10 messages
        if recent_messages:
            conversation_context = "\n\n📚 **RECENT CONVERSATION CONTEXT (User-Specific Memory):**\n"
            for i, msg in enumerate(recent_messages):
                if hasattr(msg, 'content'):
                    role = "👤 User" if isinstance(msg, HumanMessage) else "🔒 ISO Auditor"
                    # Truncate long messages for context
                    content = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
                    conversation_context += f"{role}: {content}\n"
            
            # Add user learning context
            user_context = f"\n💡 **USER LEARNING CONTEXT:**\n"
            user_context += f"Based on our previous {len(recent_messages)} exchanges, I can see you're interested in ISO 27001:2022 compliance.\n"
            user_context += f"Use this context to provide personalized, building-upon-previous-discussions responses.\n"
    
    # Create a comprehensive prompt for the LLM with user-specific memory context
    system_prompt = f"""You are an expert Internal Auditor specializing in ISO 27001:2022 compliance framework. 

    You have comprehensive knowledge of:
    - ISO 27001:2022 standard requirements
    - Control groups and specific controls
    - Implementation guidelines
    - Best practices for information security management
    
    Current ISO 27001:2022 Knowledge Base:
    {json.dumps(ISO_27001_KNOWLEDGE, indent=2)}
    
    Your role is to:
    1. Answer questions about ISO 27001:2022 compliance
    2. Provide guidance on implementation
    3. Explain specific controls and their requirements
    4. Offer best practices and recommendations
    5. Help with risk assessment and treatment
    6. **CRITICAL: Use the user-specific conversation context below to provide personalized responses**
    7. **CRITICAL: Reference previous discussions when relevant to show continuity**
    8. **CRITICAL: Build upon what the user has already learned**
    9. Suggest the next steps to improve ISO 27001:2022 compliance
    
    {user_context}
    
    {conversation_context}
    
    **IMPORTANT INSTRUCTIONS FOR USER MEMORY:**
    - If the user refers to previous questions, acknowledge and build upon that context
    - If they ask follow-up questions, reference what was discussed before
    - If they're building on previous knowledge, acknowledge their progress
    - Provide continuity and show you remember their learning journey
    - Make connections between current questions and previous discussions
    
    Always provide accurate, practical, and actionable advice based on the ISO 27001:2022 standard.
    If you're unsure about something, acknowledge the limitation and suggest consulting the official standard.
    
    If the query is not related to ISO 27001:2022 compliance, politely decline to answer and suggest the user to contact the ISO 27001:2022 certification body.
    """
    
    # Create messages for the LLM with memory context
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state.current_query)
    ]
    
    try:
        # Get response from LLM
        llm = get_llm()
        response = llm.invoke(messages)
        state.response = response.content
        
        # Update memory with the new conversation
        if state.memory:
            state.memory.chat_memory.add_user_message(state.current_query)
            state.memory.chat_memory.add_ai_message(state.response)
            
            # Update conversation history
            state.conversation_history.append({
                "role": "user",
                "content": state.current_query,
                "timestamp": datetime.now().isoformat()
            })
            state.conversation_history.append({
                "role": "assistant", 
                "content": state.response,
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        state.response = f"I apologize, but I encountered an error while processing your query. Please try again or rephrase your question. Error: {str(e)}"
    
    return state

# Create the state graph
def create_agent_graph():
    """Create and return the compiled agent graph"""
    workflow = StateGraph(AgentState)
    
    # Add the single node
    workflow.add_node("iso_27001_auditor", iso_27001_auditor_node)
    
    # Set the entry point
    workflow.set_entry_point("iso_27001_auditor")
    
    # Set the end point
    workflow.add_edge("iso_27001_auditor", END)
    
    # Compile and return the graph
    return workflow.compile()

# Create the compiled graph instance
app_state = create_agent_graph()

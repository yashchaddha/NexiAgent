from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
import json
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(title="ISO 27001:2022 Auditor Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    api_key=os.getenv("OPENAI_API_KEY")
)

# ISO 27001:2022 knowledge base
ISO_27001_KNOWLEDGE = {
    "overview": """
    ISO 27001:2022 is an international standard for Information Security Management Systems (ISMS).
    It provides a framework for establishing, implementing, maintaining, and continually improving
    information security within an organization.
    
    Key changes in the 2022 version:
    - Reduced from 114 controls to 93 controls
    - Reorganized into 4 control groups instead of 14
    - New controls for cloud security, threat intelligence, and data leakage prevention
    """,
    
    "control_groups": {
        "people": "Controls related to human resources, awareness, and training",
        "organizational": "Controls for policies, procedures, and organizational structure",
        "technological": "Technical controls for systems and infrastructure",
        "physical": "Physical security controls for facilities and equipment"
    },
    
    "key_controls": {
        "A.5.1": "Information security policies",
        "A.5.2": "Information security roles and responsibilities",
        "A.5.3": "Segregation of duties",
        "A.5.4": "Management responsibilities",
        "A.5.5": "Contact with authorities",
        "A.5.6": "Contact with special interest groups",
        "A.5.7": "Threat intelligence",
        "A.5.8": "Information security risk assessment",
        "A.5.9": "Information security risk treatment",
        "A.6.1": "Internal organization",
        "A.6.2": "Mobile device policy",
        "A.6.3": "Information security event reporting",
        "A.6.4": "Information security events assessment",
        "A.6.5": "Incident response",
        "A.6.6": "Learning from information security incidents",
        "A.6.7": "Evidence collection",
        "A.6.8": "Business continuity",
        "A.6.9": "Business continuity planning and testing",
        "A.7.1": "Screening",
        "A.7.2": "Terms and conditions of employment",
        "A.7.3": "Information security awareness, education and training",
        "A.7.4": "Disciplinary process",
        "A.7.5": "Information security event reporting",
        "A.7.6": "Information security event assessment",
        "A.7.7": "Incident response",
        "A.7.8": "Learning from information security incidents",
        "A.7.9": "Evidence collection",
        "A.7.10": "Business continuity",
        "A.7.11": "Business continuity planning and testing",
        "A.8.1": "Inventory of information and other associated assets",
        "A.8.2": "Ownership of assets",
        "A.8.3": "Acceptable use of assets",
        "A.8.4": "Return of assets",
        "A.8.5": "Classification of information",
        "A.8.6": "Labelling of information",
        "A.8.7": "Handling of assets",
        "A.8.8": "Media handling",
        "A.8.9": "Physical media transfer",
        "A.8.10": "Disposal of media",
        "A.8.11": "Business continuity",
        "A.8.12": "Business continuity planning and testing",
        "A.8.13": "Information security event reporting",
        "A.8.14": "Information security event assessment",
        "A.8.15": "Incident response",
        "A.8.16": "Learning from information security incidents",
        "A.8.17": "Evidence collection",
        "A.8.18": "Business continuity",
        "A.8.19": "Business continuity planning and testing",
        "A.8.20": "Information security event reporting",
        "A.8.21": "Information security event assessment",
        "A.8.22": "Incident response",
        "A.8.23": "Learning from information security incidents",
        "A.8.24": "Evidence collection",
        "A.8.25": "Business continuity",
        "A.8.26": "Business continuity planning and testing",
        "A.8.27": "Information security event reporting",
        "A.8.28": "Information security event assessment",
        "A.8.29": "Incident response",
        "A.8.30": "Learning from information security incidents",
        "A.8.31": "Evidence collection",
        "A.8.32": "Business continuity",
        "A.8.33": "Business continuity planning and testing",
        "A.8.34": "Information security event reporting",
        "A.8.35": "Information security event assessment",
        "A.8.36": "Incident response",
        "A.8.37": "Learning from information security incidents",
        "A.8.38": "Evidence collection",
        "A.8.39": "Business continuity",
        "A.8.40": "Business continuity planning and testing",
        "A.8.41": "Information security event reporting",
        "A.8.42": "Information security event assessment",
        "A.8.43": "Incident response",
        "A.8.44": "Learning from information security incidents",
        "A.8.45": "Evidence collection",
        "A.8.46": "Business continuity",
        "A.8.47": "Business continuity planning and testing",
        "A.8.48": "Information security event reporting",
        "A.8.49": "Information security event assessment",
        "A.8.50": "Incident response",
        "A.8.51": "Learning from information security incidents",
        "A.8.52": "Evidence collection",
        "A.8.53": "Business continuity",
        "A.8.54": "Business continuity planning and testing",
        "A.8.55": "Information security event reporting",
        "A.8.56": "Information security event assessment",
        "A.8.57": "Incident response",
        "A.8.58": "Learning from information security incidents",
        "A.8.59": "Evidence collection",
        "A.8.60": "Business continuity",
        "A.8.61": "Business continuity planning and testing",
        "A.8.62": "Information security event reporting",
        "A.8.63": "Information security event assessment",
        "A.8.64": "Incident response",
        "A.8.65": "Learning from information security incidents",
        "A.8.66": "Evidence collection",
        "A.8.67": "Business continuity",
        "A.8.68": "Business continuity planning and testing",
        "A.8.69": "Information security event reporting",
        "A.8.70": "Information security event assessment",
        "A.8.71": "Incident response",
        "A.8.72": "Learning from information security incidents",
        "A.8.73": "Evidence collection",
        "A.8.74": "Business continuity",
        "A.8.75": "Business continuity planning and testing",
        "A.8.76": "Information security event reporting",
        "A.8.77": "Information security event assessment",
        "A.8.78": "Incident response",
        "A.8.79": "Learning from information security incidents",
        "A.8.80": "Evidence collection",
        "A.8.81": "Business continuity",
        "A.8.82": "Business continuity planning and testing",
        "A.8.83": "Information security event reporting",
        "A.8.84": "Information security event assessment",
        "A.8.85": "Incident response",
        "A.8.86": "Learning from information security incidents",
        "A.8.87": "Evidence collection",
        "A.8.88": "Business continuity",
        "A.8.89": "Business continuity planning and testing",
        "A.8.90": "Information security event reporting",
        "A.8.91": "Information security event assessment",
        "A.8.92": "Incident response",
        "A.8.93": "Learning from information security incidents"
    },
    
    "implementation_steps": [
        "1. Establish the context of the organization",
        "2. Define the scope of the ISMS",
        "3. Conduct risk assessment",
        "4. Select and implement controls",
        "5. Monitor and review performance",
        "6. Continual improvement"
    ],
    
    "benefits": [
        "Enhanced security posture",
        "Regulatory compliance",
        "Customer trust and confidence",
        "Risk reduction",
        "Business continuity",
        "Competitive advantage"
    ]
}

# In-memory storage for conversation sessions
# In production, you'd want to use a database
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
    """Node responsible for answering ISO 27001:2022 compliance queries with memory"""
    
    query = state.current_query.lower()
    
    # Get conversation context from memory
    conversation_context = ""
    if state.memory and hasattr(state.memory, 'chat_memory'):
        # Get recent conversation history
        recent_messages = state.memory.chat_memory.messages[-10:]  # Last 10 messages
        if recent_messages:
            conversation_context = "\n\nRecent conversation context:\n"
            for msg in recent_messages:
                if hasattr(msg, 'content'):
                    role = "User" if isinstance(msg, HumanMessage) else "Assistant"
                    conversation_context += f"{role}: {msg.content}\n"
    
    # Create a comprehensive prompt for the LLM with memory context
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
    6. Remember and refer to previous conversation context when relevant
    
    IMPORTANT: Use the conversation context below to provide more relevant and contextual responses.
    If the user refers to previous questions or builds upon earlier discussions, acknowledge that context.
    
    {conversation_context}
    
    Always provide accurate, practical, and actionable advice based on the ISO 27001:2022 standard.
    If you're unsure about something, acknowledge the limitation and suggest consulting the official standard.
    
    If the query is not related to ISO 27001:2022 compliance, politely decline to answer and suggest the user to contact the ISO 27001:2022 certification body.
    """
    
    # Create messages for the LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state.current_query)
    ]
    
    try:
        # Get response from LLM
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
workflow = StateGraph(AgentState)

# Add the single node
workflow.add_node("iso_27001_auditor", iso_27001_auditor_node)

# Set the entry point
workflow.set_entry_point("iso_27001_auditor")

# Set the end point
workflow.add_edge("iso_27001_auditor", END)

# Compile the graph
app_state = workflow.compile()

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
@app.get("/")
async def root():
    return {"message": "ISO 27001:2022 Auditor Agent API with Memory"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a query about ISO 27001:2022 compliance with memory"""
    
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Get or create conversation memory for this session
        if request.session_id not in conversation_sessions:
            # Create new memory for this session
            memory = ConversationBufferWindowMemory(
                k=20,  # Remember last 20 exchanges
                return_messages=True,
                memory_key="chat_history"
            )
            conversation_sessions[request.session_id] = {
                "memory": memory,
                "conversation_history": [],
                "created_at": datetime.now().isoformat()
            }
        else:
            memory = conversation_sessions[request.session_id]["memory"]
        
        # Initialize state with memory
        initial_state = AgentState(
            session_id=request.session_id,
            current_query=request.query,
            response="",
            conversation_history=conversation_sessions[request.session_id]["conversation_history"],
            memory=memory
        )
        
        # Execute the workflow
        result = app_state.invoke(initial_state)
        
        # Debug: print the result structure
        print(f"DEBUG: Result type: {type(result)}")
        print(f"DEBUG: Result content: {result}")
        if hasattr(result, '__dict__'):
            print(f"DEBUG: Result attributes: {dir(result)}")
        
        # Handle the result properly for newer LangGraph versions
        if hasattr(result, 'response'):
            response_text = result.response
        elif isinstance(result, dict) and 'response' in result:
            response_text = result['response']
        elif hasattr(result, '__dict__'):
            # Try to access as object attributes
            response_text = getattr(result, 'response', str(result))
        else:
            # Fallback: try to get response from the result object
            response_text = str(result)
        
        print(f"DEBUG: Final response_text: {response_text[:100]}...")
        
        # For now, just use an empty conversation history to get it working
        conversation_history = []
        
        # Update session storage with the current conversation
        conversation_sessions[request.session_id]["conversation_history"] = conversation_history
        
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

@app.post("/session/new", response_model=SessionResponse)
async def create_new_session():
    """Create a new conversation session"""
    session_id = str(uuid.uuid4())
    memory = ConversationBufferWindowMemory(
        k=20,
        return_messages=True,
        memory_key="chat_history"
    )
    conversation_sessions[session_id] = {
        "memory": memory,
        "conversation_history": [],
        "created_at": datetime.now().isoformat()
    }
    return SessionResponse(
        session_id=session_id,
        message="New session created successfully"
    )

@app.get("/session/{session_id}/history")
async def get_session_history(session_id: str):
    """Get conversation history for a specific session"""
    if session_id not in conversation_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "conversation_history": conversation_sessions[session_id]["conversation_history"],
        "created_at": conversation_sessions[session_id]["created_at"]
    }

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a conversation session"""
    if session_id not in conversation_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del conversation_sessions[session_id]
    return {"message": "Session deleted successfully"}

@app.get("/sessions")
async def list_sessions():
    """List all active conversation sessions"""
    sessions = []
    for session_id, data in conversation_sessions.items():
        sessions.append({
            "session_id": session_id,
            "created_at": data["created_at"],
            "message_count": len(data["conversation_history"])
        })
    return {"sessions": sessions}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "ISO 27001:2022 Auditor Agent with Memory",
        "active_sessions": len(conversation_sessions)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

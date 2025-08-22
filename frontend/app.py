import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="ISO 27001:2022 Auditor Agent",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and better styling
st.markdown("""
<style>
    /* Dark theme background */
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Chat message styling with dark theme */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .user-message {
        background-color: #1e3a8a;
        border-left-color: #3b82f6;
        margin-left: 2rem;
        color: #ffffff;
    }
    
    .assistant-message {
        background-color: #581c87;
        border-left-color: #a855f7;
        margin-right: 2rem;
        color: #ffffff;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        background-color: #1e293b;
        border: 2px solid #475569;
        color: #ffffff;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        padding: 0.75rem 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1565c0, #f57c00);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e293b;
    }
    
    .sidebar-info {
        background-color: #334155;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #ffffff;
        border: 1px solid #475569;
    }
    
    .control-group {
        background-color: #065f46;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #ffffff;
    }
    
    /* Text color overrides for dark theme */
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Divider styling */
    hr {
        border-color: #475569;
        margin: 2rem 0;
    }
    
    /* Footer styling */
    .footer {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
        color: #94a3b8;
        border: 1px solid #475569;
    }
    
    /* Better contrast for all text */
    p, h1, h2, h3, h4, h5, h6, span, div {
        color: #ffffff !important;
    }
    
    /* Streamlit specific overrides */
    .stTextInput label {
        color: #ffffff !important;
    }
    
    .stButton label {
        color: #ffffff !important;
    }
    
    /* Session info styling */
    .session-info {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #475569;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

if 'session_id' not in st.session_state:
    st.session_state.session_id = ""

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Function to create a new session
def create_new_session():
    try:
        response = requests.post(f"{st.session_state.api_url}/session/new", timeout=10)
        if response.status_code == 200:
            result = response.json()
            st.session_state.session_id = result["session_id"]
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.success("🆕 New conversation session created!")
            return True
        else:
            st.error(f"Failed to create session: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error creating session: {str(e)}")
        return False

# Function to get session history
def get_session_history(session_id):
    try:
        response = requests.get(f"{st.session_state.api_url}/session/{session_id}/history", timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result["conversation_history"]
        else:
            return []
    except Exception as e:
        st.error(f"Error getting session history: {str(e)}")
        return []

# Sidebar
with st.sidebar:
    st.markdown("## 🔒 ISO 27001:2022 Auditor")
    st.markdown("---")
    
    # Session Management
    st.markdown("### 💬 Session Management")
    
    if st.button("🆕 New Session"):
        create_new_session()
    
    if st.button("🗑️ Clear Current Session"):
        if st.session_state.session_id:
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.success("Current session cleared!")
        else:
            st.warning("No active session to clear")
    
    # Display current session info
    if st.session_state.session_id:
        st.markdown("""
        <div class="session-info">
            <strong>Current Session:</strong><br>
            <small>ID: {}</small><br>
            <small>Messages: {}</small>
        </div>
        """.format(
            st.session_state.session_id[:8] + "...",
            len(st.session_state.messages)
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Configuration
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input(
        "API URL",
        value=st.session_state.api_url,
        help="Backend API endpoint"
    )
    
    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url
        st.rerun()
    
    # Test API connection
    if st.button("🔗 Test Connection"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ API Connected! Active sessions: {result.get('active_sessions', 0)}")
            else:
                st.error("❌ API Error")
        except Exception as e:
            st.error(f"❌ Connection Failed: {str(e)}")
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("📋 Show Control Groups"):
        if not st.session_state.session_id:
            create_new_session()
        st.session_state.messages.append({
            "role": "user",
            "content": "What are the main control groups in ISO 27001:2022?"
        })
        st.rerun()
    
    if st.button("🔍 Risk Assessment"):
        if not st.session_state.session_id:
            create_new_session()
        st.session_state.messages.append({
            "role": "user",
            "content": "How do I conduct a risk assessment for ISO 27001:2022?"
        })
        st.rerun()
    
    if st.button("📚 Implementation Steps"):
        if not st.session_state.session_id:
            create_new_session()
        st.session_state.messages.append({
            "role": "user",
            "content": "What are the key steps to implement ISO 27001:2022?"
        })
        st.rerun()
    
    st.markdown("---")
    
    # Information
    st.markdown("### ℹ️ About")
    st.markdown("""
    This agent provides expert guidance on ISO 27001:2022 compliance, 
    including implementation strategies, control requirements, and best practices.
    
    **New Feature:** The agent now remembers conversation context and can refer to previous messages!
    """)
    
    # Clear all data button
    if st.button("🗑️ Clear All Data"):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.session_state.session_id = ""
        st.success("All data cleared!")

# Main content
st.markdown("""
<div class="main-header">
    <h1>🔒 ISO 27001:2022 Auditor Agent</h1>
    <p>Your expert guide to information security management compliance with Memory</p>
</div>
""", unsafe_allow_html=True)

# Auto-create session if none exists
if not st.session_state.session_id:
    if st.button("🚀 Start New Conversation"):
        create_new_session()
    else:
        st.info("💡 Click 'Start New Conversation' to begin chatting with the ISO Auditor Agent!")
        st.stop()

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🔒 ISO Auditor:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# Input area
st.markdown("---")
input_container = st.container()

with input_container:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask me about ISO 27001:2022 compliance...",
            key="user_input",
            placeholder="e.g., How do I implement access control policies?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True)

# Process user input
if send_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show typing indicator
    with st.spinner("🔒 ISO Auditor is thinking..."):
        try:
            # Send query to API with session ID
            response = requests.post(
                f"{st.session_state.api_url}/query",
                json={
                    "query": user_input,
                    "session_id": st.session_state.session_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Add assistant response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["response"]
                })
                
                # Update conversation history
                st.session_state.conversation_history = result.get("conversation_history", [])
                
                # Clear input
                st.session_state.user_input = ""
                
            else:
                st.error(f"API Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {str(e)}")
            st.info("Please check if the backend API is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Rerun to update the chat
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🔒 ISO 27001:2022 Auditor Agent with Memory | Built with Streamlit, FastAPI & LangGraph</p>
    <p>💡 The agent now remembers your conversation context!</p>
    <p>For official ISO standards, please refer to ISO.org</p>
</div>
""", unsafe_allow_html=True)

# Auto-scroll to bottom
st.markdown("""
<script>
    // Auto-scroll to bottom of chat
    window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True)

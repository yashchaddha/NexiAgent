import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="ISO 27001:2022 Auditor with Authentication",
    page_icon="🔐",
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
    
    /* Form styling */
    .auth-form {
        background-color: #1e293b;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #475569;
        margin: 2rem auto;
        max-width: 500px;
    }
    
    .auth-form h2 {
        color: #ffffff;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        background-color: #334155;
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
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1565c0, #f57c00);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Chat message styling with dark theme */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
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
    
    /* Typing animation */
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 1rem;
        background-color: #581c87;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #a855f7;
        color: #ffffff;
    }
    
    .typing-dots {
        display: inline-flex;
        align-items: center;
        margin-left: 10px;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        margin: 0 2px;
        background-color: #ffffff;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
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
    
    /* Auto-scroll container */
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding-right: 10px;
        scroll-behavior: smooth;
    }
    
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Auth form specific styling */
    .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 60vh;
    }
    
    .form-field {
        margin-bottom: 1rem;
    }
    
    .form-field label {
        color: #ffffff !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_token' not in st.session_state:
    st.session_state.user_token = None

if 'user_info' not in st.session_state:
    st.session_state.user_info = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

if 'auth_api_url' not in st.session_state:
    st.session_state.auth_api_url = "http://localhost:8001"

if 'session_id' not in st.session_state:
    st.session_state.session_id = ""

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'is_typing' not in st.session_state:
    st.session_state.is_typing = False

# Authentication functions
def login_user(email: str, password: str):
    """Login user and get JWT token"""
    try:
        response = requests.post(
            f"{st.session_state.auth_api_url}/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            st.session_state.user_token = result["access_token"]
            st.session_state.user_info = result["user"]
            st.session_state.authenticated = True
            return True, "Login successful!"
        else:
            return False, f"Login failed: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def signup_user(user_data: dict):
    """Sign up new user"""
    try:
        response = requests.post(
            f"{st.session_state.auth_api_url}/signup",
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Registration successful! Please login."
        else:
            return False, f"Registration failed: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def logout_user():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user_token = None
    st.session_state.user_info = None
    st.session_state.messages = []
    st.session_state.session_id = ""
    st.session_state.conversation_history = []

# Main application
st.write("🔍 Debug: Authentication check")
st.write(f"Session state 'authenticated': {st.session_state.authenticated}")
st.write(f"Session state 'user_info': {st.session_state.user_info}")

if not st.session_state.authenticated:
    st.info("🔐 User is NOT authenticated - showing login/signup forms")
    
    # Authentication page
    st.markdown("""
    <div class="main-header">
        <h1>🔐 ISO 27001:2022 Auditor</h1>
        <p>Secure Access to Expert Compliance Guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        st.header("🔐 Login")
        st.write("Please enter your credentials to access the ISO 27001:2022 Auditor")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if email and password:
                    success, message = login_user(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.header("📝 Create Account")
        st.write("Please fill in the form below to create your account")
        
        with st.form("signup_form"):
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email")
            organization_name = st.text_input("Organization Name", placeholder="Enter organization name")
            domain = st.selectbox("Domain", ["Technology", "Healthcare", "Finance", "Manufacturing", "Education", "Government", "Other"])
            location = st.text_input("Location", placeholder="City, Country")
            organization_url = st.text_input("Organization URL (Optional)", placeholder="https://example.com")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            submit_button = st.form_submit_button("Sign Up")
            
            if submit_button:
                if not all([name, email, organization_name, domain, location, password, confirm_password]):
                    st.error("Please fill in all required fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long")
                else:
                    user_data = {
                        "name": name,
                        "email": email,
                        "organization_name": organization_name,
                        "domain": domain,
                        "location": location,
                        "organization_url": organization_url if organization_url else None,
                        "password": password
                    }
                    
                    success, message = signup_user(user_data)
                    if success:
                        st.success(message)
                        st.info("Please switch to the Login tab to sign in")
                    else:
                        st.error(message)

else:
    st.success("🔒 User IS authenticated - showing chatbot interface")
    
    # Main chatbot interface (only accessible after authentication)
    
    # Header with user info
    st.markdown(f"""
    <div class="main-header">
        <h1>🔒 ISO 27001:2022 Auditor</h1>
        <p>Welcome back, {st.session_state.user_info['name']} from {st.session_state.user_info['organization_name']}</p>
        <p><small>Domain: {st.session_state.user_info['domain']} | Location: {st.session_state.user_info['location']}</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔐 User Profile")
        
        # User information
        st.markdown(f"""
        <div class="sidebar-info">
            <strong>👤 {st.session_state.user_info['name']}</strong><br>
            📧 {st.session_state.user_info['email']}<br>
            🏢 {st.session_state.user_info['organization_name']}<br>
            🌍 {st.session_state.user_info['domain']}<br>
            📍 {st.session_state.user_info['location']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Session management
        st.markdown("## 🗂️ Session Management")
        
        if st.button("🆕 New Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = ""
            st.session_state.conversation_history = []
            st.success("New conversation started!")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.success("Chat cleared!")
        
        # Show user's learning progress
        if st.button("📊 Show My Progress", use_container_width=True):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.user_token}"}
                response = requests.get(
                    f"{st.session_state.api_url}/user/progress",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    progress = response.json()
                    st.markdown("### 📊 Your Learning Progress")
                    st.markdown(f"**Level:** {progress['learning_level']}")
                    st.markdown(f"**Total Conversations:** {progress['total_conversations']}")
                    st.markdown(f"**Topics Covered:** {', '.join(progress['topics_covered'])}")
                    if progress['suggested_next_steps']:
                        st.markdown(f"**Suggested Next Steps:** {', '.join(progress['suggested_next_steps'])}")
                    
                    # Show progress in chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"📊 **Your Learning Progress:**\n\n**Level:** {progress['learning_level']}\n**Total Conversations:** {progress['total_conversations']}\n**Topics Covered:** {', '.join(progress['topics_covered'])}\n\n**Suggested Next Steps:** {', '.join(progress['suggested_next_steps'])}"
                    })
                    st.rerun()
                else:
                    st.error("Failed to load progress")
            except Exception as e:
                st.error(f"Error loading progress: {str(e)}")
        
        # Show user's sessions
        if st.button("📋 My Sessions", use_container_width=True):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.user_token}"}
                response = requests.get(
                    f"{st.session_state.api_url}/sessions",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    sessions = response.json()["sessions"]
                    if sessions:
                        st.markdown("### 📋 Your Conversation Sessions")
                        for session in sessions:
                            st.markdown(f"""
                            **Session:** {session['session_id'][:8]}...
                            **Messages:** {session['message_count']}
                            **Created:** {session['created_at'][:10]}
                            """)
                    else:
                        st.info("No conversation sessions found")
                else:
                    st.error("Failed to load sessions")
            except Exception as e:
                st.error(f"Error loading sessions: {str(e)}")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        
        if st.button("📋 Show Control Groups", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "What are the main control groups in ISO 27001:2022?"
            })
            st.rerun()
        
        if st.button("🔍 Risk Assessment", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "How do I conduct a risk assessment for ISO 27001:2022?"
            })
            st.rerun()
        
        if st.button("📚 Implementation Steps", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "What are the key steps to implement ISO 27001:2022?"
            })
            st.rerun()
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.success("Logged out successfully!")
            st.rerun()
        
        st.markdown("---")
        
        # About
        st.markdown("## ℹ️ About")
        st.markdown("""
        <div class="sidebar-info">
            <strong>ISO 27001:2022 Auditor</strong><br>
            Expert guidance on information security management systems and compliance.
        </div>
        """, unsafe_allow_html=True)
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Show session info if available
        if st.session_state.session_id:
            st.info(f"📝 **Active Session:** {st.session_state.session_id[:8]}... | Messages: {len(st.session_state.messages)} | 🔐 **Memory Active**")
        else:
            st.info("🆕 **New Conversation** - Starting fresh session")
        
        # Create a scrollable container for chat messages
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
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
        
        # Show typing indicator if processing
        if st.session_state.is_typing:
            st.markdown("""
            <div class="typing-indicator">
                <strong>🔒 ISO Auditor is thinking</strong>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area with form for better handling
    st.markdown("---")
    input_container = st.container()
    
    with input_container:
        # Use a form for better input handling
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_input(
                    "Ask me about ISO 27001:2022 compliance...",
                    key="user_input",
                    placeholder="e.g., How do I implement access control policies?",
                    label_visibility="collapsed"
                )
            
            with col2:
                send_button = st.form_submit_button("Send", use_container_width=True)
    
    # Process user input
    if send_button and user_input:
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Set typing indicator
        st.session_state.is_typing = True
        
        # Rerun to show typing indicator
        st.rerun()
    
    # Process typing and API call
    if st.session_state.is_typing and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        # Get the last user message
        last_user_message = st.session_state.messages[-1]["content"]
        
        # Process the API call
        try:
            # Send query to API with session ID and authentication
            headers = {"Authorization": f"Bearer {st.session_state.user_token}"}
            response = requests.post(
                f"{st.session_state.api_url}/query",
                json={
                    "query": last_user_message,
                    "session_id": st.session_state.session_id
                },
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Update session ID if provided (important for memory continuity)
                if result.get("session_id"):
                    st.session_state.session_id = result["session_id"]
                
                # Add assistant response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["response"]
                })
                
                # Update conversation history
                st.session_state.conversation_history = result.get("conversation_history", [])
                
            else:
                st.error(f"API Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {str(e)}")
            st.info("Please check if the backend API is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        # Clear typing indicator
        st.session_state.is_typing = False
        
        # Rerun to update the chat
        st.rerun()
    
    # JavaScript for auto-scroll to bottom
    st.markdown("""
    <script>
        // Auto-scroll to bottom of chat container
        function scrollToBottom() {
            const chatContainer = document.querySelector('.chat-container');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
        
        // Scroll on page load
        window.addEventListener('load', scrollToBottom);
        
        // Scroll when new messages are added
        const observer = new MutationObserver(scrollToBottom);
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            observer.observe(chatContainer, { childList: true, subtree: true });
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🔐 ISO 27001:2022 Auditor with Authentication | Secure • Reliable • Expert</p>
    </div>
    """, unsafe_allow_html=True)

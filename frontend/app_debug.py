import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="ISO 27001:2022 Auditor Debug",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_token' not in st.session_state:
    st.session_state.user_token = None

if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# Debug information
st.title("🔍 Debug: Authentication Status")
st.write("Current session state:")
st.json({
    "authenticated": st.session_state.authenticated,
    "user_token": st.session_state.user_token,
    "user_info": st.session_state.user_info
})

# Test authentication endpoints
st.header("🔐 Test Authentication Endpoints")

# Test auth server health
if st.button("Test Auth Server Health"):
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            st.success(f"Auth server healthy: {response.json()}")
        else:
            st.error(f"Auth server error: {response.status_code}")
    except Exception as e:
        st.error(f"Auth server connection failed: {e}")

# Test main server health
if st.button("Test Main Server Health"):
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            st.success(f"Main server healthy: {response.json()}")
        else:
            st.error(f"Main server error: {response.status_code}")
    except Exception as e:
        st.error(f"Main server connection failed: {e}")

# Manual authentication test
st.header("🧪 Manual Authentication Test")

# Test signup
st.subheader("Test Signup")
with st.form("test_signup"):
    test_name = st.text_input("Test Name", value="Test User")
    test_email = st.text_input("Test Email", value="test@example.com")
    test_org = st.text_input("Test Organization", value="Test Corp")
    test_domain = st.selectbox("Test Domain", ["Technology", "Healthcare"])
    test_location = st.text_input("Test Location", value="Test City")
    test_password = st.text_input("Test Password", value="TestPass123!", type="password")
    
    if st.form_submit_button("Test Signup"):
        try:
            user_data = {
                "name": test_name,
                "email": test_email,
                "organization_name": test_org,
                "domain": test_domain,
                "location": test_location,
                "password": test_password
            }
            
            response = requests.post(
                "http://localhost:8001/signup",
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                st.success(f"Signup successful: {response.json()}")
            else:
                st.error(f"Signup failed: {response.status_code} - {response.json()}")
                
        except Exception as e:
            st.error(f"Signup error: {e}")

# Test login
st.subheader("Test Login")
with st.form("test_login"):
    login_email = st.text_input("Login Email", value="test@example.com")
    login_password = st.text_input("Login Password", value="TestPass123!", type="password")
    
    if st.form_submit_button("Test Login"):
        try:
            login_data = {
                "email": login_email,
                "password": login_password
            }
            
            response = requests.post(
                "http://localhost:8001/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success(f"Login successful!")
                st.json(result)
                
                # Update session state
                st.session_state.user_token = result["access_token"]
                st.session_state.user_info = result["user"]
                st.session_state.authenticated = True
                st.success("Session state updated!")
                
            else:
                st.error(f"Login failed: {response.status_code} - {response.json()}")
                
        except Exception as e:
            st.error(f"Login error: {e}")

# Show current state after any updates
st.header("📊 Updated Session State")
st.json({
    "authenticated": st.session_state.authenticated,
    "user_token": st.session_state.user_token,
    "user_info": st.session_state.user_info
})

# Force authentication state
st.header("🔧 Force Authentication State")
if st.button("Force Authenticated = True"):
    st.session_state.authenticated = True
    st.session_state.user_info = {"name": "Debug User", "email": "debug@test.com"}
    st.success("Forced authentication state!")
    st.rerun()

if st.button("Force Authenticated = False"):
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.success("Forced unauthenticated state!")
    st.rerun()

# Show the main app logic
st.header("🎯 Main App Logic")
st.write("This is what the main app checks:")

if not st.session_state.authenticated:
    st.info("🔐 User is NOT authenticated - should show login/signup forms")
    st.write("This is the authentication page that should be visible")
else:
    st.success("🔒 User IS authenticated - should show chatbot interface")
    st.write("This is the chatbot interface that should be visible")

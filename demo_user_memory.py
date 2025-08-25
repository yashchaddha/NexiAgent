#!/usr/bin/env python3
"""
Demo script showing how the User Memory System works
"""

import requests
import json
import time

# Configuration
AUTH_API_URL = "http://localhost:8001"
MAIN_API_URL = "http://localhost:8000"

def demo_user_memory():
    """Demonstrate the user memory system with a conversation flow"""
    
    print("🎭 User Memory System Demonstration")
    print("=" * 60)
    print("This demo shows how the agent remembers user conversations")
    print("and provides personalized, contextual responses.")
    print()
    
    # Step 1: User Registration
    print("1️⃣ **User Registration**")
    print("-" * 30)
    
    user_data = {
        "name": "Demo User",
        "email": "demo@example.com",
        "organization_name": "Demo Corp",
        "domain": "Technology",
        "location": "Demo City",
        "password": "demopassword123"
    }
    
    try:
        response = requests.post(f"{AUTH_API_URL}/signup", json=user_data)
        if response.status_code == 200:
            print("✅ User registered successfully")
        else:
            print(f"⚠️  User registration: {response.status_code} (may already exist)")
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 2: User Login
    print("\n2️⃣ **User Login**")
    print("-" * 30)
    
    login_data = {
        "email": "demo@example.com",
        "password": "demopassword123"
    }
    
    try:
        response = requests.post(f"{AUTH_API_URL}/login", json=login_data)
        if response.status_code == 200:
            result = response.json()
            token = result["access_token"]
            user_id = result["user"]["id"]
            print(f"✅ Login successful - User ID: {user_id}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 3: First Query (New Session)
    print("\n3️⃣ **First Query - New Session**")
    print("-" * 30)
    
    headers = {"Authorization": f"Bearer {token}"}
    query_data = {
        "query": "What is ISO 27001:2022?",
        "session_id": ""
    }
    
    try:
        response = requests.post(f"{MAIN_API_URL}/query", json=query_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            session_id = result["session_id"]
            print(f"✅ First query successful")
            print(f"📝 Session ID: {session_id}")
            print(f"💬 Response: {result['response'][:100]}...")
            print(f"📊 Conversation history: {len(result['conversation_history'])} exchanges")
        else:
            print(f"❌ First query failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ First query error: {e}")
        return
    
    # Step 4: Second Query (Same Session - Testing Memory)
    print("\n4️⃣ **Second Query - Same Session (Testing Memory)**")
    print("-" * 30)
    
    query_data = {
        "query": "What are the main control groups in this standard?",
        "session_id": session_id
    }
    
    try:
        response = requests.post(f"{MAIN_API_URL}/query", json=query_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Second query successful")
            print(f"💬 Response: {result['response'][:100]}...")
            print(f"📊 Conversation history: {len(result['conversation_history'])} exchanges")
            
            # Check if response shows memory of previous conversation
            if "ISO 27001:2022" in result['response'] or "standard" in result['response'].lower():
                print("🔐 **Memory Working:** Agent referenced the standard from previous conversation")
            else:
                print("⚠️  **Memory Check:** Response doesn't clearly show memory usage")
        else:
            print(f"❌ Second query failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Second query error: {e}")
        return
    
    # Step 5: Third Query (Same Session - Building on Knowledge)
    print("\n5️⃣ **Third Query - Building on Previous Knowledge**")
    print("-" * 30)
    
    query_data = {
        "query": "How do I implement the controls you mentioned?",
        "session_id": session_id
    }
    
    try:
        response = requests.post(f"{MAIN_API_URL}/query", json=query_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Third query successful")
            print(f"💬 Response: {result['response'][:100]}...")
            print(f"📊 Conversation history: {len(result['conversation_history'])} exchanges")
            
            # Check for memory indicators
            memory_indicators = ["control", "groups", "mentioned", "previous", "earlier", "discussed"]
            memory_detected = any(indicator in result['response'].lower() for indicator in memory_indicators)
            
            if memory_detected:
                print("🔐 **Memory Working:** Agent is building on previous knowledge")
            else:
                print("⚠️  **Memory Check:** Response may not be using context effectively")
        else:
            print(f"❌ Third query failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Third query error: {e}")
        return
    
    # Step 6: Check User Progress
    print("\n6️⃣ **Check User Learning Progress**")
    print("-" * 30)
    
    try:
        response = requests.get(f"{MAIN_API_URL}/user/progress", headers=headers)
        if response.status_code == 200:
            progress = response.json()
            print(f"✅ Progress retrieved successfully")
            print(f"📊 Learning Level: {progress['learning_level']}")
            print(f"📝 Total Conversations: {progress['total_conversations']}")
            print(f"🎯 Topics Covered: {', '.join(progress['topics_covered'])}")
            print(f"🚀 Suggested Next Steps: {', '.join(progress['suggested_next_steps'])}")
        else:
            print(f"❌ Progress check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Progress check error: {e}")
    
    # Step 7: New Session (Testing Session Isolation)
    print("\n7️⃣ **New Session - Testing Session Isolation**")
    print("-" * 30)
    
    query_data = {
        "query": "What is risk assessment in ISO 27001?",
        "session_id": ""
    }
    
    try:
        response = requests.post(f"{MAIN_API_URL}/query", json=query_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            new_session_id = result["session_id"]
            print(f"✅ New session query successful")
            print(f"📝 New Session ID: {new_session_id}")
            print(f"💬 Response: {result['response'][:100]}...")
            print(f"📊 Conversation history: {len(result['conversation_history'])} exchanges")
            
            # Verify session isolation
            if new_session_id != session_id:
                print("🔐 **Session Isolation Working:** New session created successfully")
            else:
                print("⚠️  **Session Issue:** Same session ID returned")
        else:
            print(f"❌ New session query failed: {response.status_code}")
    except Exception as e:
        print(f"❌ New session query error: {e}")
    
    # Step 8: Check All Sessions
    print("\n8️⃣ **Check All User Sessions**")
    print("-" * 30)
    
    try:
        response = requests.get(f"{MAIN_API_URL}/sessions", headers=headers)
        if response.status_code == 200:
            sessions = response.json()["sessions"]
            print(f"✅ Sessions retrieved successfully")
            print(f"📊 Total Sessions: {len(sessions)}")
            for session in sessions:
                print(f"  - Session {session['session_id'][:8]}...: {session['message_count']} messages")
        else:
            print(f"❌ Sessions check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Sessions check error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 User Memory System Demonstration Complete!")
    print()
    print("🔐 **What We Demonstrated:**")
    print("  ✅ User-specific conversation storage")
    print("  ✅ Session-based memory management")
    print("  ✅ Context-aware responses")
    print("  ✅ Learning progress tracking")
    print("  ✅ Session isolation")
    print()
    print("💡 **To Test Further:**")
    print("  - Start the frontend: streamlit run frontend/app_with_auth.py")
    print("  - Login with demo@example.com / demopassword123")
    print("  - Have a conversation and see memory in action!")
    print()
    print("📚 **Key Features:**")
    print("  - Each user has their own conversation history")
    print("  - Sessions maintain context within conversations")
    print("  - Agent remembers what you've discussed")
    print("  - Learning progress is tracked over time")

if __name__ == "__main__":
    print("🚀 Starting User Memory System Demo...")
    print("Make sure both backend services are running:")
    print("  - Authentication: python backend/login.py")
    print("  - Main API: python backend/main.py")
    print()
    
    try:
        demo_user_memory()
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Check if both backend services are running")

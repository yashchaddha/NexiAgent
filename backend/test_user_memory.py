#!/usr/bin/env python3
"""
Test script for user memory system
"""

import requests
import json
import time

# Configuration
AUTH_API_URL = "http://localhost:8001"
MAIN_API_URL = "http://localhost:8000"

def test_user_memory_system():
    """Test the complete user memory system"""
    
    print("🧪 Testing User Memory System")
    print("=" * 50)
    
    # Test 1: User Registration
    print("\n1. Testing User Registration...")
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "organization_name": "Test Corp",
        "domain": "Technology",
        "location": "Test City",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{AUTH_API_URL}/signup", json=user_data)
        if response.status_code == 200:
            print("✅ User registration successful")
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 2: User Login
    print("\n2. Testing User Login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{AUTH_API_URL}/login", json=login_data)
        if response.status_code == 200:
            result = response.json()
            token = result["access_token"]
            user_id = result["user"]["id"]
            print("✅ User login successful")
            print(f"User ID: {user_id}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 3: Send First Query
    print("\n3. Testing First Query...")
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
            print("✅ First query successful")
            print(f"Session ID: {session_id}")
            print(f"Response length: {len(result['response'])} characters")
        else:
            print(f"❌ First query failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ First query error: {e}")
        return
    
    # Test 4: Send Second Query (same session)
    print("\n4. Testing Second Query (same session)...")
    query_data = {
        "query": "What are the main control groups?",
        "session_id": session_id
    }
    
    try:
        response = requests.post(f"{MAIN_API_URL}/query", json=query_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ Second query successful")
            print(f"Response length: {len(result['response'])} characters")
            print(f"Conversation history length: {len(result['conversation_history'])}")
        else:
            print(f"❌ Second query failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Second query error: {e}")
        return
    
    # Test 5: Send Third Query (same session)
    print("\n5. Testing Third Query (same session)...")
    query_data = {
        "query": "Tell me more about risk assessment",
        "session_id": session_id
    }
    
    try:
        response = requests.post(f"{MAIN_API_URL}/query", json=query_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ Third query successful")
            print(f"Response length: {len(result['response'])} characters")
            print(f"Conversation history length: {len(result['conversation_history'])}")
        else:
            print(f"❌ Third query failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Third query error: {e}")
        return
    
    # Test 6: Get Session History
    print("\n6. Testing Session History...")
    try:
        response = requests.get(f"{MAIN_API_URL}/session/{session_id}/history", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ Session history retrieved")
            print(f"Total exchanges: {result['total_exchanges']}")
            print(f"History length: {len(result['conversation_history'])}")
        else:
            print(f"❌ Session history failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Session history error: {e}")
    
    # Test 7: Get User Progress
    print("\n7. Testing User Progress...")
    try:
        response = requests.get(f"{MAIN_API_URL}/user/progress", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ User progress retrieved")
            print(f"Learning level: {result['learning_level']}")
            print(f"Total conversations: {result['total_conversations']}")
            print(f"Topics covered: {result['topics_covered']}")
        else:
            print(f"❌ User progress failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ User progress error: {e}")
    
    # Test 8: Get User Sessions
    print("\n8. Testing User Sessions...")
    try:
        response = requests.get(f"{MAIN_API_URL}/sessions", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ User sessions retrieved")
            print(f"Total sessions: {len(result['sessions'])}")
            for session in result['sessions']:
                print(f"  - Session {session['session_id'][:8]}...: {session['message_count']} messages")
        else:
            print(f"❌ User sessions failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ User sessions error: {e}")
    
    # Test 9: Get Session Summary
    print("\n9. Testing Session Summary...")
    try:
        response = requests.get(f"{MAIN_API_URL}/user/sessions/{session_id}/summary", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ Session summary retrieved")
            print(f"Total exchanges: {result['total_exchanges']}")
            print(f"Topics discussed: {result['topics_discussed']}")
            print(f"Compliance focus: {result['compliance_focus']}")
        else:
            print(f"❌ Session summary failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Session summary error: {e}")
    
    # Test 10: New Session
    print("\n10. Testing New Session...")
    query_data = {
        "query": "What are the benefits of ISO 27001:2022?",
        "session_id": ""
    }
    
    try:
        response = requests.post(f"{MAIN_API_URL}/query", json=query_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            new_session_id = result["session_id"]
            print("✅ New session query successful")
            print(f"New Session ID: {new_session_id}")
            print(f"Different from previous: {new_session_id != session_id}")
        else:
            print(f"❌ New session query failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ New session query error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 User Memory System Test Complete!")
    print(f"📝 Test user: {user_data['email']}")
    print(f"🔑 User ID: {user_id}")
    print(f"📊 Total conversations: 4 queries across 2 sessions")

if __name__ == "__main__":
    test_user_memory_system()

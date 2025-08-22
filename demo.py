#!/usr/bin/env python3
"""
Demo script for ISO 27001:2022 Auditor Agent with Memory
This script demonstrates the agent's capabilities with conversation memory.
"""

import requests
import json
import time

def demo_iso_auditor_with_memory():
    """Demonstrate the ISO 27001:2022 Auditor Agent capabilities with memory"""
    
    base_url = "http://localhost:8000"
    
    print("🔒 ISO 27001:2022 Auditor Agent with Memory - Demo")
    print("=" * 60)
    print("This demo showcases the agent's expertise in ISO compliance WITH MEMORY")
    print("Make sure the backend is running on http://localhost:8000")
    print("")
    
    # Create a new session
    print("🚀 Creating new conversation session...")
    try:
        session_response = requests.post(f"{base_url}/session/new", timeout=10)
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session created: {session_id[:8]}...")
        else:
            print("❌ Failed to create session")
            return
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return
    
    # Demo conversation flow that demonstrates memory
    conversation_flow = [
        {
            "step": 1,
            "query": "What is ISO 27001:2022?",
            "description": "Initial question about the standard"
        },
        {
            "step": 2,
            "query": "What are the main control groups you mentioned?",
            "description": "Follow-up question referencing previous response"
        },
        {
            "step": 3,
            "query": "Can you elaborate on the organizational controls?",
            "description": "Building on previous conversation context"
        },
        {
            "step": 4,
            "query": "How do these controls relate to what we discussed earlier?",
            "description": "Explicitly referencing conversation history"
        },
        {
            "step": 5,
            "query": "Based on our discussion, what would be the first step for implementation?",
            "description": "Synthesizing information from the entire conversation"
        }
    ]
    
    print("\n💬 Starting conversation flow to demonstrate memory...")
    print("")
    
    for step in conversation_flow:
        print(f"📋 Step {step['step']}: {step['description']}")
        print(f"   Query: {step['query']}")
        print("")
        
        try:
            print("   🔍 Processing query...")
            response = requests.post(
                f"{base_url}/query",
                json={
                    "query": step['query'],
                    "session_id": session_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ Query processed successfully")
                print(f"   📝 Response length: {len(result['response'])} characters")
                
                # Show a preview of the response
                preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
                print(f"   📖 Response preview: {preview}")
                
                # Show memory context
                if result.get('conversation_history'):
                    print(f"   💾 Memory: {len(result['conversation_history'])} messages stored")
                
            else:
                print(f"   ❌ Query failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("   " + "-" * 50)
        print("")
        
        # Small delay between queries
        time.sleep(2)
    
    # Test session history retrieval
    print("📚 Testing session history retrieval...")
    try:
        history_response = requests.get(f"{base_url}/session/{session_id}/history", timeout=10)
        if history_response.status_code == 200:
            history_data = history_response.json()
            print(f"✅ Session history retrieved: {len(history_data['conversation_history'])} messages")
            print(f"   Session created: {history_data['created_at']}")
        else:
            print(f"❌ Failed to get session history: {history_response.status_code}")
    except Exception as e:
        print(f"❌ Error getting session history: {e}")
    
    print("\n🎉 Memory demo completed!")
    print("")
    print("💡 The agent demonstrated:")
    print("   • ISO 27001:2022 standard knowledge")
    print("   • Conversation memory and context awareness")
    print("   • Ability to reference previous discussions")
    print("   • Session management capabilities")
    print("   • Contextual responses based on conversation history")
    print("")
    print("🚀 You can now interact with the agent through the Streamlit UI!")
    print("   Frontend: http://localhost:8501")
    print(f"   Session ID: {session_id[:8]}...")

def test_memory_features():
    """Test specific memory features"""
    
    base_url = "http://localhost:8000"
    
    print("\n🧠 Testing Memory Features")
    print("=" * 40)
    
    # Test session creation
    print("1. Testing session creation...")
    try:
        response = requests.post(f"{base_url}/session/new", timeout=10)
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data["session_id"]
            print(f"   ✅ Session created: {session_id[:8]}...")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test multiple queries in same session
    print("\n2. Testing conversation memory...")
    queries = [
        "What is control A.5.1?",
        "How does this relate to A.5.2?",
        "Can you summarize what we've discussed about these controls?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"   Query {i}: {query}")
        try:
            response = requests.post(
                f"{base_url}/query",
                json={"query": query, "session_id": session_id},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Response: {len(result['response'])} chars")
                print(f"   💾 Memory: {len(result.get('conversation_history', []))} messages")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test session listing
    print("\n3. Testing session management...")
    try:
        response = requests.get(f"{base_url}/sessions", timeout=10)
        if response.status_code == 200:
            sessions = response.json()
            print(f"   ✅ Active sessions: {len(sessions['sessions'])}")
            for session in sessions['sessions']:
                print(f"      - {session['session_id'][:8]}... ({session['message_count']} messages)")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Clean up - delete session
    print("\n4. Cleaning up test session...")
    try:
        response = requests.delete(f"{base_url}/session/{session_id}", timeout=10)
        if response.status_code == 200:
            print("   ✅ Session deleted")
        else:
            print(f"   ❌ Failed to delete: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error deleting: {e}")

def interactive_demo():
    """Interactive demo where user can ask custom questions with memory"""
    
    base_url = "http://localhost:8000"
    
    print("🎯 Interactive Demo Mode with Memory")
    print("=" * 40)
    print("Ask your own ISO 27001:2022 questions!")
    print("The agent will remember your conversation context.")
    print("Type 'quit' to exit the interactive demo")
    print("")
    
    # Create session
    try:
        session_response = requests.post(f"{base_url}/session/new", timeout=10)
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ New session created: {session_id[:8]}...")
        else:
            print("❌ Failed to create session")
            return
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return
    
    print("")
    
    while True:
        try:
            user_query = input("🔒 Your question: ").strip()
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("👋 Exiting interactive demo...")
                break
            
            if not user_query:
                print("⚠️  Please enter a question")
                continue
            
            print("   🔍 Processing your question...")
            
            response = requests.post(
                f"{base_url}/query",
                json={"query": user_query, "session_id": session_id},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ Response received:")
                print("   " + "=" * 40)
                print(f"   {result['response']}")
                print("   " + "=" * 40)
                print(f"   💾 Memory: {len(result.get('conversation_history', []))} messages stored")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting interactive demo...")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("")
    
    # Clean up
    try:
        requests.delete(f"{base_url}/session/{session_id}", timeout=10)
        print("🧹 Session cleaned up")
    except:
        pass

if __name__ == "__main__":
    print("Welcome to the ISO 27001:2022 Auditor Agent with Memory Demo!")
    print("Choose your demo mode:")
    print("1. Automated memory demo (predefined conversation flow)")
    print("2. Memory features testing")
    print("3. Interactive demo (ask your own questions with memory)")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                demo_iso_auditor_with_memory()
                break
            elif choice == "2":
                test_memory_features()
                break
            elif choice == "3":
                interactive_demo()
                break
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("⚠️  Please enter 1, 2, 3, or 4")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

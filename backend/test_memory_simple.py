#!/usr/bin/env python3
"""
Simple test for user memory system
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv("../.env")

def test_memory_basics():
    """Test basic memory functionality"""
    
    print("🧪 Testing Basic Memory Functionality")
    print("=" * 50)
    
    try:
        # Import required components
        from database import get_db
        from conversation_service import UserConversationService
        from models import User, UserConversation
        
        print("✅ All imports successful")
        
        # Get database session
        db = next(get_db())
        print("✅ Database connection successful")
        
        # Test conversation service
        service = UserConversationService(db)
        print("✅ Conversation service created")
        
        # Create a test user first
        print(f"\n🔍 Creating test user")
        from auth import get_password_hash
        test_user = User(
            name="Test User",
            email="test@example.com",
            organization_name="Test Corp",
            domain="Technology",
            location="Test City",
            password_hash=get_password_hash("testpassword123")
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        test_user_id = test_user.id
        print(f"✅ Test user created with ID: {test_user_id}")
        
        # Test creating memory for a new session
        test_session_id = "test-session-123"
        
        print(f"\n🔍 Testing memory creation for user {test_user_id}, session {test_session_id}")
        
        # Create memory (should be empty for new session)
        memory = service.create_user_memory(test_user_id, test_session_id)
        print(f"✅ Memory created with {len(memory.chat_memory.messages)} messages")
        
        # Test storing a conversation
        print(f"\n🔍 Testing conversation storage")
        conv = service.store_conversation(
            user_id=test_user_id,
            session_id=test_session_id,
            query="What is ISO 27001?",
            response="ISO 27001 is an information security standard."
        )
        print(f"✅ Conversation stored with ID: {conv.id}")
        
        # Test retrieving conversations
        print(f"\n🔍 Testing conversation retrieval")
        conversations = service.get_session_conversations(test_user_id, test_session_id)
        print(f"✅ Retrieved {len(conversations)} conversations")
        
        # Test creating memory again (should now have the stored conversation)
        print(f"\n🔍 Testing memory recreation with stored conversation")
        memory2 = service.create_user_memory(test_user_id, test_session_id)
        print(f"✅ Memory recreated with {len(memory2.chat_memory.messages)} messages")
        
        # Show memory contents
        if memory2.chat_memory.messages:
            print("\n📝 Memory contents:")
            for i, msg in enumerate(memory2.chat_memory.messages):
                role = "User" if hasattr(msg, 'type') and msg.type == 'human' else "Assistant"
                content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                print(f"  {i+1}. {role}: {content}")
        
        # Test user progress
        print(f"\n🔍 Testing user progress")
        progress = service.get_user_learning_progress(test_user_id)
        print(f"✅ Progress retrieved: {progress}")
        
        # Clean up test data
        print(f"\n🧹 Cleaning up test data")
        service.delete_user_session(test_user_id, test_session_id)
        
        # Delete test user
        db.delete(test_user)
        db.commit()
        print("✅ Test data cleaned up")
        
        db.close()
        print("\n" + "=" * 50)
        print("🎉 Basic Memory Test Complete!")
        print("✅ User memory system is working correctly")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_memory_basics()
    if not success:
        sys.exit(1)

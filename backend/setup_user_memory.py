#!/usr/bin/env python3
"""
Setup script for user memory system
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def setup_user_memory():
    """Setup the user memory system database"""
    
    print("🔧 Setting up User Memory System")
    print("=" * 50)
    
    try:
        # Import database components
        from database import engine, Base
        from models import User, UserConversation
        
        print("✅ Database components imported successfully")
        
        # Create all tables
        print("📊 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"📋 Tables created: {tables}")
        
        # Check if required tables exist
        required_tables = ['users', 'user_conversations']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        print("✅ All required tables created successfully")
        
        # Test database connection
        print("🔌 Testing database connection...")
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        print("\n" + "=" * 50)
        print("🎉 User Memory System Setup Complete!")
        print("📊 Database is ready for user conversations")
        print("🚀 You can now run the application with user memory")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required packages are installed")
        return False
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("💡 Check your database configuration and environment variables")
        return False

if __name__ == "__main__":
    success = setup_user_memory()
    if not success:
        sys.exit(1)

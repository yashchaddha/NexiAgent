#!/usr/bin/env python3
"""
Fix database schema by dropping and recreating the users table
"""

from database import engine, Base
from models import User
from sqlalchemy import text

def fix_database():
    """Drop and recreate the users table with correct schema"""
    
    print("🔧 Fixing database schema...")
    
    try:
        # Drop existing users table
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            conn.commit()
            print("✅ Old users table dropped")
        
        # Create new users table with correct schema
        Base.metadata.create_all(bind=engine)
        print("✅ New users table created with correct schema")
        
        # Verify the table structure
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            print("\n📋 New users table structure:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        return False

if __name__ == "__main__":
    fix_database()

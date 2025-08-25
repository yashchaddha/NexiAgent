#!/usr/bin/env python3
"""
Startup script for ISO 27001:2022 Auditor with Authentication
This script helps you get everything running properly.
"""

import subprocess
import time
import signal
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import psycopg2
        print("✅ psycopg2 installed")
    except ImportError:
        print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy installed")
    except ImportError:
        print("❌ SQLAlchemy not installed. Run: pip install sqlalchemy")
        return False
    
    try:
        import passlib
        print("✅ passlib installed")
    except ImportError:
        print("❌ passlib not installed. Run: pip install passlib")
        return False
    
    try:
        import jose
        print("✅ python-jose installed")
    except ImportError:
        print("❌ python-jose not installed. Run: pip install python-jose[cryptography]")
        return False
    
    return True

def check_environment():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    # Load .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['POSTGRES_URI', 'SECRET_KEY', 'OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"❌ {var} not set")
        else:
            print(f"✅ {var} is set")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    
    return True

def initialize_database():
    """Initialize the database"""
    print("\n🗄️ Initializing database...")
    
    try:
        backend_dir = Path("backend")
        if not backend_dir.exists():
            print("❌ Backend directory not found!")
            return False
        
        os.chdir(backend_dir)
        
        # Run database initialization
        result = subprocess.run([sys.executable, "init_db.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Database initialized successfully")
            return True
        else:
            print(f"❌ Database initialization failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    finally:
        # Go back to root directory
        os.chdir("..")

def start_servers():
    """Start both authentication and main auditor servers"""
    print("\n🚀 Starting servers...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    os.chdir(backend_dir)
    
    try:
        # Start authentication server
        print("🔐 Starting Authentication Server on port 8001...")
        auth_process = subprocess.Popen(
            [sys.executable, "login.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Authentication Server started with PID: {auth_process.pid}")
        
        # Wait for auth server to start
        time.sleep(5)
        
        # Start main auditor server
        print("🔒 Starting Main Auditor Server on port 8000...")
        main_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Main Auditor Server started with PID: {main_process.pid}")
        
        # Wait for main server to start
        time.sleep(5)
        
        print("\n🎉 Both servers are running successfully!")
        print("=" * 50)
        print("📱 Authentication Server: http://localhost:8001")
        print("🔒 Main Auditor Server: http://localhost:8000")
        print("📚 Auth API Docs: http://localhost:8001/docs")
        print("📚 Main API Docs: http://localhost:8000/docs")
        print("\n🌐 To start the frontend, run in a new terminal:")
        print("   cd frontend")
        print("   streamlit run app_with_auth.py")
        print("\n🛑 Press Ctrl+C to stop both servers")
        
        # Signal handler for graceful shutdown
        def signal_handler(sig, frame):
            print("\n\n🛑 Shutting down servers...")
            if main_process:
                main_process.terminate()
                print("✅ Main auditor server stopped")
            if auth_process:
                auth_process.terminate()
                print("✅ Authentication server stopped")
            print("👋 Goodbye!")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if main_process and main_process.poll() is not None:
                print("❌ Main auditor server stopped unexpectedly")
                break
            if auth_process and auth_process.poll() is not None:
                print("❌ Authentication server stopped unexpectedly")
                break
                
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        return False
    finally:
        # Go back to root directory
        os.chdir("..")

def main():
    """Main function"""
    print("🔐 ISO 27001:2022 Auditor with Authentication - Setup")
    print("=" * 60)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        return
    
    # Step 2: Check environment
    if not check_environment():
        print("\n❌ Please fix environment variables and try again")
        return
    
    # Step 3: Initialize database
    if not initialize_database():
        print("\n❌ Database initialization failed")
        return
    
    # Step 4: Start servers
    if not start_servers():
        print("\n❌ Failed to start servers")
        return

if __name__ == "__main__":
    main()

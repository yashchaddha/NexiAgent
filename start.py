#!/usr/bin/env python3
"""
Startup script for ISO 27001:2022 Auditor Agent
This script helps you start both the backend and frontend services.
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def print_banner():
    """Print the application banner"""
    print("""
🔒 ISO 27001:2022 Auditor Agent
=====================================
Built with FastAPI, LangGraph & Streamlit
""")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import streamlit
        import langgraph
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has OpenAI API key"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Please copy env.example to .env and add your OpenAI API key")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_openai_api_key_here" in content:
            print("⚠️  Please update your OpenAI API key in .env file")
            return False
    
    print("✅ Environment configuration found")
    return True

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return None
    
    try:
        # Change to backend directory and start the server
        os.chdir(backend_dir)
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Backend started successfully on http://localhost:8000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None
    finally:
        # Return to root directory
        os.chdir("..")

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return None
    
    try:
        # Change to frontend directory and start Streamlit
        os.chdir(frontend_dir)
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Frontend started successfully on http://localhost:8501")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None
    finally:
        # Return to root directory
        os.chdir("..")

def main():
    """Main function to start the application"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment configuration
    if not check_env_file():
        print("Please configure your environment before starting the application")
        sys.exit(1)
    
    print("\n🚀 Starting ISO 27001:2022 Auditor Agent...")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Stopping backend...")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n🎉 Application started successfully!")
    print("📱 Frontend: http://localhost:8501")
    print("🔌 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()

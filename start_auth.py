#!/usr/bin/env python3
"""
Startup script for ISO 27001:2022 Auditor with Authentication
This script starts both the main auditor server and the authentication server.
"""

import subprocess
import time
import signal
import sys
import os
from pathlib import Path

def start_server(script_path, port, name):
    """Start a server process"""
    try:
        print(f"🚀 Starting {name} on port {port}...")
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ {name} started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def check_server_health(url, name):
    """Check if server is responding"""
    try:
        import requests
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name} is healthy and responding")
            return True
        else:
            print(f"⚠️ {name} responded with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name} health check failed: {e}")
        return False

def main():
    """Main function to start both servers"""
    print("🔐 ISO 27001:2022 Auditor with Authentication")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return
    
    os.chdir(backend_dir)
    
    # Start authentication server
    auth_process = start_server("login.py", 8001, "Authentication Server")
    if not auth_process:
        print("❌ Failed to start authentication server")
        return
    
    # Wait a bit for auth server to start
    time.sleep(3)
    
    # Check auth server health
    if not check_server_health("http://localhost:8001/health", "Authentication Server"):
        print("❌ Authentication server is not responding")
        auth_process.terminate()
        return
    
    # Start main auditor server
    main_process = start_server("main.py", 8000, "Main Auditor Server")
    if not main_process:
        print("❌ Failed to start main auditor server")
        auth_process.terminate()
        return
    
    # Wait a bit for main server to start
    time.sleep(3)
    
    # Check main server health
    if not check_server_health("http://localhost:8000/health", "Main Auditor Server"):
        print("❌ Main auditor server is not responding")
        main_process.terminate()
        auth_process.terminate()
        return
    
    print("\n🎉 Both servers are running successfully!")
    print("=" * 50)
    print("📱 Authentication Server: http://localhost:8001")
    print("🔒 Main Auditor Server: http://localhost:8000")
    print("📚 Auth API Docs: http://localhost:8001/docs")
    print("📚 Main API Docs: http://localhost:8000/docs")
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
    
    try:
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
                
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()

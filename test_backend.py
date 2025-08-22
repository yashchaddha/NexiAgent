#!/usr/bin/env python3
"""
Test script for the ISO 27001:2022 Auditor Agent backend
"""

import requests
import json
import time

def test_backend():
    """Test the backend API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ISO 27001:2022 Auditor Agent Backend")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test 3: Query endpoint with ISO 27001 question
    print("\n3. Testing query endpoint...")
    test_queries = [
        "What are the main control groups in ISO 27001:2022?",
        "How do I conduct a risk assessment?",
        "Explain control A.5.1"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Testing query {i}: {query}")
        try:
            response = requests.post(
                f"{base_url}/query",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Query {i} passed")
                print(f"   Response length: {len(result['response'])} characters")
                print(f"   Response preview: {result['response'][:100]}...")
            else:
                print(f"   ❌ Query {i} failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Query {i} error: {e}")
            return False
    
    print("\n🎉 All tests passed! Backend is working correctly.")
    return True

def test_api_documentation():
    """Test if the API documentation is accessible"""
    print("\n4. Testing API documentation...")
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation accessible")
            print("   📚 Swagger UI: http://localhost:8000/docs")
            print("   📖 ReDoc: http://localhost:8000/redoc")
        else:
            print(f"❌ API documentation not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ API documentation error: {e}")

if __name__ == "__main__":
    print("Starting backend tests...")
    print("Make sure the backend is running on http://localhost:8000")
    print("You can start it with: cd backend && python main.py")
    
    # Wait a moment for user to read
    time.sleep(2)
    
    try:
        success = test_backend()
        if success:
            test_api_documentation()
            print("\n🚀 Backend is ready for use!")
        else:
            print("\n❌ Backend tests failed. Please check the backend service.")
    except KeyboardInterrupt:
        print("\n\n🛑 Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")

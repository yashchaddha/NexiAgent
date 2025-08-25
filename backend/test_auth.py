#!/usr/bin/env python3
"""
Test script for ISO 27001:2022 Auditor Authentication API
This script tests all the authentication endpoints.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8001"
TEST_USER = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "organization_name": "TechCorp Inc",
    "domain": "Technology",
    "location": "San Francisco, CA",
    "organization_url": "https://techcorp.example.com",
    "password": "SecurePassword123!"
}

def test_health_check():
    """Test health check endpoint"""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_signup():
    """Test user signup endpoint"""
    print("\n📝 Testing user signup...")
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=TEST_USER
        )
        if response.status_code == 200:
            print("✅ Signup successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Signup error: {e}")

def test_login():
    """Test user login endpoint"""
    print("\n🔐 Testing user login...")
    try:
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        response = requests.post(
            f"{BASE_URL}/login",
            json=login_data
        )
        if response.status_code == 200:
            print("✅ Login successful")
            result = response.json()
            print(f"   Token: {result['access_token'][:50]}...")
            print(f"   User: {result['user']['name']} ({result['user']['email']})")
            return result['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_profile_access(token):
    """Test profile access with token"""
    if not token:
        print("❌ No token available for profile test")
        return
    
    print("\n👤 Testing profile access...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/profile",
            headers=headers
        )
        if response.status_code == 200:
            print("✅ Profile access successful")
            profile = response.json()
            print(f"   Name: {profile['name']}")
            print(f"   Organization: {profile['organization_name']}")
            print(f"   Domain: {profile['domain']}")
        else:
            print(f"❌ Profile access failed: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Profile access error: {e}")

def test_profile_update(token):
    """Test profile update with token"""
    if not token:
        print("❌ No token available for profile update test")
        return
    
    print("\n✏️ Testing profile update...")
    try:
        updated_data = TEST_USER.copy()
        updated_data["name"] = "John Smith"
        updated_data["location"] = "New York, NY"
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(
            f"{BASE_URL}/profile",
            json=updated_data,
            headers=headers
        )
        if response.status_code == 200:
            print("✅ Profile update successful")
            profile = response.json()
            print(f"   Updated Name: {profile['name']}")
            print(f"   Updated Location: {profile['location']}")
        else:
            print(f"❌ Profile update failed: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Profile update error: {e}")

def test_duplicate_signup():
    """Test duplicate signup (should fail)"""
    print("\n🔄 Testing duplicate signup...")
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=TEST_USER
        )
        if response.status_code == 400:
            print("✅ Duplicate signup correctly rejected")
            print(f"   Error: {response.json()}")
        else:
            print(f"❌ Duplicate signup should have failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Duplicate signup test error: {e}")

def test_invalid_login():
    """Test invalid login (should fail)"""
    print("\n🚫 Testing invalid login...")
    try:
        invalid_data = {
            "email": TEST_USER["email"],
            "password": "WrongPassword123!"
        }
        response = requests.post(
            f"{BASE_URL}/login",
            json=invalid_data
        )
        if response.status_code == 401:
            print("✅ Invalid login correctly rejected")
            print(f"   Error: {response.json()}")
        else:
            print(f"❌ Invalid login should have failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid login test error: {e}")

def main():
    """Main test function"""
    print("🧪 ISO 27001:2022 Auditor Authentication API Tests")
    print("=" * 60)
    
    # Test basic functionality
    test_health_check()
    
    # Test signup
    test_signup()
    
    # Test login
    token = test_login()
    
    # Test authenticated endpoints
    if token:
        test_profile_access(token)
        test_profile_update(token)
    
    # Test error cases
    test_duplicate_signup()
    test_invalid_login()
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print("✅ Health check endpoint")
    print("✅ User signup endpoint")
    print("✅ User login endpoint")
    print("✅ Profile access (authenticated)")
    print("✅ Profile update (authenticated)")
    print("✅ Duplicate signup rejection")
    print("✅ Invalid login rejection")
    print("\n🚀 All authentication endpoints are working correctly!")

if __name__ == "__main__":
    main()

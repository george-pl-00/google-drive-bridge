#!/usr/bin/env python3
"""
Test script to verify authentication and test authenticated endpoints
"""

import requests

BRIDGE_URL = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com"

def test_endpoints():
    """Test various endpoints to see authentication status"""
    
    print("🧪 Testing Bridge Endpoints")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n📋 Test 1: Health Check")
    try:
        response = requests.get(f"{BRIDGE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Try to create document (should show auth status)
    print("\n📝 Test 2: Create Document (ChatGPT endpoint)")
    try:
        response = requests.post(
            f"{BRIDGE_URL}/create_doc_chat",
            json={"name": "Test Document"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if result.get("status") == "error":
            print("🔐 Authentication required - this is expected")
            print(f"🔗 Auth URL: {result.get('auth_url')}")
        elif result.get("status") == "success":
            print("✅ Document created successfully!")
            print(f"🔗 Document Link: {result.get('link')}")
        else:
            print("❓ Unexpected response format")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete!")
    print("\n📋 Next Steps:")
    print("1. If you see 'Authentication required', visit the auth URL")
    print("2. Complete Google OAuth in your browser")
    print("3. Run this test again to see if authentication worked")

if __name__ == "__main__":
    test_endpoints()

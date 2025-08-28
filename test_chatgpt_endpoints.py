#!/usr/bin/env python3
"""
Test script for the new ChatGPT-friendly endpoints
Tests /create_doc_chat and /create_sheet_chat
"""

import requests
import json

# Your Heroku app URL
HEROKU_URL = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com"

def test_chatgpt_endpoints():
    """Test the new ChatGPT-friendly endpoints"""
    
    print("🧪 Testing ChatGPT-Friendly Endpoints")
    print("=" * 50)
    
    # Test 1: Create Document (should return auth error)
    print("\n📝 Testing /create_doc_chat...")
    try:
        response = requests.post(
            f"{HEROKU_URL}/create_doc_chat",
            json={"name": "Test Document from ChatGPT"},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "error":
                print("✅ Correctly returned authentication error")
                print(f"🔗 Auth URL: {data.get('auth_url')}")
            else:
                print("❌ Unexpected response format")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing /create_doc_chat: {e}")
    
    # Test 2: Create Sheet (should return auth error)
    print("\n📊 Testing /create_sheet_chat...")
    try:
        response = requests.post(
            f"{HEROKU_URL}/create_sheet_chat",
            json={"name": "Test Sheet from ChatGPT"},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "error":
                print("✅ Correctly returned authentication error")
                print(f"🔗 Auth URL: {data.get('auth_url')}")
            else:
                print("❌ Unexpected response format")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing /create_sheet_chat: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete!")
    print("\n📋 Expected Behavior:")
    print("✅ Both endpoints should return status 200")
    print("✅ Both should return authentication error messages")
    print("✅ Both should include auth_url for redirect")

if __name__ == "__main__":
    test_chatgpt_endpoints()

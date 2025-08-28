#!/usr/bin/env python3
"""
Simple script to test individual API endpoints on Heroku
Update the HEROKU_URL variable with your actual Heroku app URL
"""

import requests
import json

# Your Heroku app URL
HEROKU_URL = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a specific API endpoint"""
    url = f"{HEROKU_URL}{endpoint}"
    
    print(f"\n🔍 Testing {method} {endpoint}")
    print(f"📡 URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        else:
            print(f"❌ Unsupported method: {method}")
            return
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            try:
                result = response.json()
                print(f"📄 Response: {json.dumps(result, indent=2)}")
            except:
                print(f"📄 Response: {response.text}")
        else:
            print("❌ Failed!")
            try:
                error = response.json()
                print(f"🚨 Error: {json.dumps(error, indent=2)}")
            except:
                print(f"🚨 Error: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot reach the API")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

def main():
    """Test all available endpoints"""
    print("🚀 Testing Google Drive Bridge API on Heroku")
    print("=" * 60)
    
    # Test health check
    test_endpoint("/")
    
    # Test authentication endpoint
    test_endpoint("/auth")
    
    # Test document creation (this will fail without auth, but shows the endpoint exists)
    test_endpoint("/create_doc", "POST", {"name": "Test Document"})
    
    # Test sheet creation (this will fail without auth, but shows the endpoint exists)
    test_endpoint("/create_sheet", "POST", {"name": "Test Sheet"})
    
    print("\n" + "=" * 60)
    print("✅ Endpoint testing complete!")
    print("\n📝 Notes:")
    print("1. Update HEROKU_URL variable with your actual Heroku app URL")
    print("2. Authentication endpoints will redirect to Google OAuth")
    print("3. Create endpoints will fail without proper authentication")
    print("4. Check Heroku logs for any server-side errors")

if __name__ == "__main__":
    main()

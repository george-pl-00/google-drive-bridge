#!/usr/bin/env python3
"""
Test script that simulates ChatGPT function calling
Shows the complete flow from user request to bridge response
"""

from middleware import chat_with_gpt

def test_chatgpt_requests():
    """Test various ChatGPT requests to see function calling in action"""
    
    print("🧪 Testing ChatGPT Function Calling")
    print("=" * 50)
    
    # Test 1: Create a Google Document
    print("\n📝 Test 1: Create Google Document")
    print("User: Create a Google Doc called Meeting Notes")
    
    try:
        result = chat_with_gpt("Create a Google Doc called Meeting Notes")
        print("ChatGPT Response:", result)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Create a Google Sheet
    print("\n📊 Test 2: Create Google Sheet")
    print("User: Make me a spreadsheet for Inventory Tracking")
    
    try:
        result = chat_with_gpt("Make me a spreadsheet for Inventory Tracking")
        print("ChatGPT Response:", result)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Regular conversation (should not trigger function)
    print("\n💬 Test 3: Regular Conversation")
    print("User: Hello, how are you?")
    
    try:
        result = chat_with_gpt("Hello, how are you?")
        print("ChatGPT Response:", result)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete!")
    print("\n📋 Expected Results:")
    print("✅ Test 1 & 2: Should call functions and return bridge responses")
    print("✅ Test 3: Should return normal ChatGPT conversation")

if __name__ == "__main__":
    test_chatgpt_requests()

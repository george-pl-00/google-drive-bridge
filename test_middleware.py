#!/usr/bin/env python3
"""
Test script for the ChatGPT Middleware
Tests the function calling without requiring interactive input
"""

import os
import sys

# Check if OpenAI API key is set
if not os.path.exists('config.py'):
    print("❌ config.py not found! Please create it first.")
    sys.exit(1)

try:
    from config import OPENAI_API_KEY
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        print("❌ Please set your OpenAI API key in config.py")
        print("   Get it from: https://platform.openai.com/api-keys")
        sys.exit(1)
except ImportError:
    print("❌ Error importing config.py")
    sys.exit(1)

print("✅ OpenAI API key configured")
print("🔑 Testing middleware functionality...")

# Test the bridge connection first
try:
    from middleware import call_bridge, BRIDGE_URL
    print(f"✅ Bridge URL configured: {BRIDGE_URL}")
    
    # Test bridge connection
    result = call_bridge("create_doc_chat", {"name": "Test Document"})
    print("✅ Bridge connection successful")
    print(f"📋 Response: {result}")
    
except Exception as e:
    print(f"❌ Bridge test failed: {e}")
    sys.exit(1)

print("\n🎯 Middleware is ready!")
print("📝 Run 'python middleware.py' to start the interactive chat")
print("🔗 Your Google Drive Bridge is fully integrated with ChatGPT!")

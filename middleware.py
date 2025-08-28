import os
import requests
from openai import OpenAI
from config_new import OPENAI_API_KEY, BRIDGE_URL, MODEL

# 🔑 Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

client = OpenAI()

# Define functions ChatGPT can call
functions = [
    {
        "name": "create_google_doc",
        "description": "Create a new Google Document in Drive",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the document"}
            },
            "required": ["name"],
        },
    },
    {
        "name": "create_google_sheet",
        "description": "Create a new Google Sheet in Drive",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the sheet"}
            },
            "required": ["name"],
        },
    },
]

def call_bridge(endpoint: str, payload: dict):
    """Helper to call your bridge endpoints"""
    url = f"{BRIDGE_URL}/{endpoint}"
    r = requests.post(url, json=payload)
    return r.json()

def chat_with_gpt(user_message: str):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_message}],
        functions=functions,
    )

    msg = response.choices[0].message

    # Case 1: GPT wants to call a function
    if msg.function_call:
        func_name = msg.function_call.name
        args = eval(msg.function_call.arguments)

        if func_name == "create_google_doc":
            result = call_bridge("create_doc_chat", args)
            if result.get("status") == "error":
                return f"⚠️ Please authenticate first: {result['auth_url']}"
            return f"✅ Document created: {result['link']}"

        elif func_name == "create_google_sheet":
            result = call_bridge("create_sheet_chat", args)
            if result.get("status") == "error":
                return f"⚠️ Please authenticate first: {result['auth_url']}"
            return f"✅ Sheet created: {result['link']}"

    # Case 2: Normal text response
    return msg.content


if __name__ == "__main__":
    print("🤖 ChatGPT + Google Drive Bridge")
    print("=" * 40)
    print("💡 Try: 'Create a Google Doc called Meeting Notes'")
    print("💡 Try: 'Make me a spreadsheet for Budget 2024'")
    print("💡 Try: 'Hello, how are you?'")
    print("=" * 40)
    
    while True:
        user_input = input("You: ")
        print("Assistant:", chat_with_gpt(user_input))
        print()

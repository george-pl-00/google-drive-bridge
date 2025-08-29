import os
import json
import requests
from openai import OpenAI

# 🔑 API key - Import from config file
from config import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

BRIDGE_URL = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com"

# -------------------------------
# Function schemas
# -------------------------------
functions = [
    {
        "name": "create_google_doc",
        "description": "Create a new Google Document",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
    },
    {
        "name": "append_text_doc",
        "description": "Append text into an existing Google Doc",
        "parameters": {"type": "object", "properties": {"doc_id": {"type": "string"}, "text": {"type": "string"}}, "required": ["doc_id","text"]},
    },
    {
        "name": "create_google_sheet",
        "description": "Create a new Google Sheet",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
    },
    {
        "name": "populate_google_sheet",
        "description": "Populate a Google Sheet with tabular data",
        "parameters": {
            "type": "object",
            "properties": {
                "sheet_id": {"type": "string"},
                "values": {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "string"}},
                },
            },
            "required": ["sheet_id","values"],
        },
    }
]

# -------------------------------
# Helper for bridge calls
# -------------------------------
def call_bridge(endpoint, payload):
    url = f"{BRIDGE_URL}/{endpoint}"
    r = requests.post(url, json=payload)
    return r.json()

# -------------------------------
# Generate structured 30-day content plan
# -------------------------------
def generate_content_plan():
    plan_prompt = """
    Generate a 30-day Instagram parenting content plan.
    Format the response as valid JSON ONLY.
    JSON structure: [["Day","Format","Caption","Image Idea","Tool"], [...next rows...]]
    Do not include text outside of the JSON.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": plan_prompt}],
    )
    raw = completion.choices[0].message.content.strip()

    try:
        values = json.loads(raw)
    except json.JSONDecodeError:
        # fallback: wrap manually if GPT outputs something odd
        cleaned = raw.strip().replace("```json","").replace("```","")
        values = json.loads(cleaned)

    return values

# -------------------------------
# Main agent loop
# -------------------------------
def chat_with_agent(user_message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        functions=functions,
    )

    msg = response.choices[0].message

    if msg.function_call:
        func_name = msg.function_call.name
        args = eval(msg.function_call.arguments)

        if func_name == "create_google_sheet":
            result = call_bridge("create_sheet_chat", args)
            return result

        elif func_name == "populate_google_sheet":
            result = call_bridge("populate_google_sheet", args)
            return result

        elif func_name == "create_google_doc":
            result = call_bridge("create_doc_chat", args)
            return result

        elif func_name == "append_text_doc":
            result = call_bridge("append_text_doc", args)
            return result

    return msg.content

# -------------------------------
# Custom flow for content plan
# -------------------------------
if __name__ == "__main__":
    print("🤖 Enhanced Google Drive Bridge Agent")
    print("=" * 50)
    print("💡 Try: 'Create a Google Doc called Meeting Notes'")
    print("💡 Try: 'Make me a spreadsheet for Budget 2024'")
    print("💡 Try: 'Generate a 30-day content plan for my parenting Instagram'")
    print("=" * 50)
    
    while True:
        user_input = input("You: ")

        if "content plan" in user_input.lower() and "sheet" in user_input.lower():
            # Step 1: create sheet
            sheet = chat_with_agent("Create a Google Sheet called Content Plan")
            print("Assistant:", sheet)

            if sheet.get("status") == "success":
                sheet_id = sheet["sheet_id"]

                # Step 2: generate structured plan
                rows = generate_content_plan()

                # Step 3: populate sheet
                payload = {"sheet_id": sheet_id, "values": rows}
                filled = call_bridge("populate_google_sheet", payload)
                print("Assistant:", filled)
                print("✅ Content Plan created & filled:", sheet["link"])

        else:
            result = chat_with_agent(user_input)
            print("Assistant:", result)

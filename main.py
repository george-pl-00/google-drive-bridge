#!/usr/bin/env python3
"""
Complete Google Drive Bridge - Full API service with OAuth
Handles Google Drive integration directly without external dependencies
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os, json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
app = FastAPI()
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
REDIRECT_URI = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com/oauth2callback"
TOKEN_FILE = "/tmp/token.json"

# -------------------------------------------------------------------
# MODELS
# -------------------------------------------------------------------
class DocRequest(BaseModel):
    name: str

class SheetRequest(BaseModel):
    name: str

# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------
def save_credentials(creds: Credentials):
    """Save OAuth credentials to file"""
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"✅ Tokens saved to {TOKEN_FILE}")
    except Exception as e:
        print(f"❌ Error saving tokens: {e}")
        raise

def load_credentials() -> Credentials:
    """Load credentials from file and refresh if needed"""
    try:
        if not os.path.exists(TOKEN_FILE):
            print(f"📁 Token file not found: {TOKEN_FILE}")
            return None

        print(f"📁 Loading tokens from: {TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(GoogleRequest())
            save_credentials(creds)

        return creds
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None

def get_docs_service():
    creds = load_credentials()
    if not creds:
        return None
    return build("docs", "v1", credentials=creds)

def get_sheets_service():
    creds = load_credentials()
    if not creds:
        return None
    return build("sheets", "v4", credentials=creds)

# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Google Drive Bridge is running!",
        "endpoints": {
            "auth": "GET /auth - Start OAuth authentication",
            "create_doc": "POST /create_doc - Create a Google Document",
            "create_sheet": "POST /create_sheet - Create a Google Spreadsheet",
            "create_doc_chat": "POST /create_doc_chat - ChatGPT-friendly document creation",
            "create_sheet_chat": "POST /create_sheet_chat - ChatGPT-friendly sheet creation"
        }
    }

@app.get("/auth")
def auth():
    # Use Heroku environment variables for OAuth credentials
    client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return {"status": "error", "message": "OAuth credentials not configured"}
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline", include_granted_scopes="true")
    return {"auth_url": auth_url}

@app.get("/oauth2callback")
def oauth2callback(request: Request):
    # Use Heroku environment variables for OAuth credentials
    client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return {"status": "error", "message": "OAuth credentials not configured"}
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    flow.fetch_token(authorization_response=str(request.url))

    creds = flow.credentials
    save_credentials(creds)

    return {"status": "ok", "message": "Authentication successful! Tokens saved."}

@app.post("/create_doc")
def create_doc(req: DocRequest):
    try:
        print(f"📝 Creating document: {req.name}")
        service = get_docs_service()
        if not service:
            print("❌ No docs service - authentication required")
            return {"status": "error", "message": "Authentication required. Visit /auth first."}

        print("✅ Docs service obtained, creating document...")
        doc = service.documents().create(body={"title": req.name}).execute()
        doc_id = doc.get("documentId")
        print(f"✅ Document created with ID: {doc_id}")
        return {"status": "success", "link": f"https://docs.google.com/document/d/{doc_id}"}
    except Exception as e:
        print(f"❌ Error creating document: {e}")
        return {"status": "error", "message": f"Failed to create document: {str(e)}"}

@app.post("/create_sheet")
def create_sheet(req: SheetRequest):
    service = get_sheets_service()
    if not service:
        return {"status": "error", "message": "Authentication required. Visit /auth first."}

    sheet = service.spreadsheets().create(body={"properties": {"title": req.name}}).execute()
    sheet_id = sheet.get("spreadsheetId")
    return {"status": "success", "link": f"https://docs.google.com/spreadsheets/d/{sheet_id}"}

# -------------------------------------------------------------------
# CHATGPT-FRIENDLY ENDPOINTS
# -------------------------------------------------------------------
@app.post("/create_doc_chat")
def create_doc_chat(req: DocRequest):
    result = create_doc(req)
    if result.get("status") == "error":
        return {
            "status": "error",
            "message": "Authentication required. Please visit:",
            "auth_url": f"{REDIRECT_URI.replace('/oauth2callback','/auth')}"
        }
    return result

@app.post("/create_sheet_chat")
def create_sheet_chat(req: SheetRequest):
    result = create_sheet(req)
    if result.get("status") == "error":
        return {
            "status": "error",
            "message": "Authentication required. Please visit:",
            "auth_url": f"{REDIRECT_URI.replace('/oauth2callback','/auth')}"
        }
    return result

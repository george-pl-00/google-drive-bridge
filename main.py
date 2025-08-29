#!/usr/bin/env python3
"""
Complete Google Drive Bridge - Full API service with OAuth
Handles Google Drive integration directly without external dependencies
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest

app = FastAPI()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]
REDIRECT_URI = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com/oauth2callback"
TOKEN_FILE = "token.json"


# ----------------------------
# Request Models
# ----------------------------
class DocRequest(BaseModel):
    name: str

class SheetRequest(BaseModel):
    name: str

class AppendRequest(BaseModel):
    doc_id: str
    text: str

class PopulateSheetRequest(BaseModel):
    sheet_id: str
    values: list  # 2D array of rows


# ----------------------------
# Helpers
# ----------------------------
def save_credentials(creds: Credentials):
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

def load_credentials() -> Credentials:
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            save_credentials(creds)
        return creds
    except Exception as e:
        # Scope mismatch or invalid token → reset
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        print(f"⚠️ Token invalid or scope mismatch, deleted token.json: {str(e)}")
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


# ----------------------------
# Root & Auth
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Google Drive Bridge is running!",
        "endpoints": {
            "auth": "GET /auth",
            "create_doc_chat": "POST /create_doc_chat",
            "append_text_doc": "POST /append_text_doc",
            "create_sheet_chat": "POST /create_sheet_chat",
            "populate_google_sheet": "POST /populate_google_sheet"
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
    auth_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="true",
        approval_prompt="force"
    )
    return {"auth_url": auth_url}

@app.get("/oauth2callback")
def oauth2callback(request: Request):
    try:
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
        
    except Exception as e:
        # If scope mismatch or invalid grant → force reset
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        return {
            "status": "error",
            "message": f"Authentication failed: {str(e)}",
            "next_step": f"Visit /auth again to re-authorize with the correct scopes"
        }


# ----------------------------
# Docs
# ----------------------------
@app.post("/create_doc_chat")
def create_doc_chat(req: DocRequest):
    service = get_docs_service()
    if not service:
        return {"status": "error", "auth_url": f"{REDIRECT_URI.replace('/oauth2callback','/auth')}"}

    doc = service.documents().create(body={"title": req.name}).execute()
    doc_id = doc.get("documentId")
    return {"status": "success", "doc_id": doc_id,
            "link": f"https://docs.google.com/document/d/{doc_id}"}

@app.post("/append_text_doc")
def append_text_doc(req: AppendRequest):
    service = get_docs_service()
    if not service:
        return {"status": "error", "auth_url": f"{REDIRECT_URI.replace('/oauth2callback','/auth')}"}

    requests_body = [{
        "insertText": {
            "location": {"index": 1},
            "text": req.text + "\n"
        }
    }]
    service.documents().batchUpdate(
        documentId=req.doc_id, body={"requests": requests_body}
    ).execute()
    return {"status": "success", "doc_id": req.doc_id, "appended_text": req.text}


# ----------------------------
# Sheets
# ----------------------------
@app.post("/create_sheet_chat")
def create_sheet_chat(req: SheetRequest):
    service = get_sheets_service()
    if not service:
        return {"status": "error", "auth_url": f"{REDIRECT_URI.replace('/oauth2callback','/auth')}"}

    sheet = service.spreadsheets().create(body={"properties": {"title": req.name}}).execute()
    sheet_id = sheet.get("spreadsheetId")
    return {"status": "success", "sheet_id": sheet_id,
            "link": f"https://docs.google.com/spreadsheets/d/{sheet_id}"}

@app.post("/populate_google_sheet")
def populate_google_sheet(req: PopulateSheetRequest):
    service = get_sheets_service()
    if not service:
        return {"status": "error", "auth_url": f"{REDIRECT_URI.replace('/oauth2callback','/auth')}"}

    body = {"values": req.values}
    service.spreadsheets().values().update(
        spreadsheetId=req.sheet_id,
        range="A1",
        valueInputOption="RAW",
        body=body
    ).execute()

    return {"status": "success", "sheet_id": req.sheet_id, "rows_added": len(req.values)}

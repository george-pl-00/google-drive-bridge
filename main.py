#!/usr/bin/env python3
"""
Complete Google Drive Bridge - Full API service with OAuth
Handles Google Drive integration directly without external dependencies
"""

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
import os
import pickle
import secrets
import jwt
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json
import requests

# OAuth 2.0 scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets"
]

# JWT secret for session management
JWT_SECRET = os.environ.get('JWT_SECRET', secrets.token_urlsafe(32))

# Initialize FastAPI app
app = FastAPI(
    title="Google Drive Bridge",
    description="Complete Google Drive API with OAuth integration and ChatGPT-friendly endpoints",
    version="1.0.0"
)

# Global services
drive_service = None
docs_service = None

# In-memory token storage
STORED_CREDENTIALS = None

# Request models
class DocRequest(BaseModel):
    name: str

class SheetRequest(BaseModel):
    name: str

# ChatGPT-friendly API base (your own Heroku app)
CHATGPT_API_BASE = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com"

def create_session_token(creds_data: dict) -> str:
    """Create a JWT token for session management."""
    payload = {
        'creds': creds_data,
        'exp': datetime.utcnow() + timedelta(days=7)  # 7 days expiry
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_session_token(token: str) -> dict:
    """Verify and decode a JWT session token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload.get('creds')
    except:
        return None

def save_tokens_to_memory(creds):
    """Save OAuth tokens to in-memory storage."""
    global STORED_CREDENTIALS
    try:
        # Store the credentials object directly in memory
        STORED_CREDENTIALS = creds
        return True
    except Exception as e:
        print(f"Error saving tokens to memory: {e}")
        return False

def load_tokens_from_memory():
    """Load OAuth tokens from in-memory storage."""
    global STORED_CREDENTIALS
    return STORED_CREDENTIALS

def clear_tokens_from_memory():
    """Clear OAuth tokens from in-memory storage."""
    global STORED_CREDENTIALS
    STORED_CREDENTIALS = None

def get_oauth_flow():
    """Create OAuth flow for web application."""
    # Check if we're in production (Heroku) or local
    if os.environ.get('HEROKU_APP_NAME'):
        # Production - use environment variables
        client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
        redirect_uri = f"https://{os.environ.get('HEROKU_APP_NAME')}.herokuapp.com/oauth2callback"
        
        # Create flow with production credentials
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            SCOPES,
            redirect_uri=redirect_uri
        )
    else:
        # Local development - use oauth_credentials.json
        if not os.path.exists('oauth_credentials.json'):
            raise HTTPException(
                status_code=500, 
                detail="oauth_credentials.json not found! Please ensure you have the OAuth credentials file."
            )
        
        flow = Flow.from_client_secrets_file(
            'oauth_credentials.json', 
            SCOPES,
            redirect_uri='http://localhost:8000/oauth2callback'
        )
    
    return flow

def get_authenticated_services():
    """Get authenticated Google services using saved tokens."""
    global drive_service, docs_service
    
    # Try to load tokens from in-memory storage
    creds = load_tokens_from_memory()
    if not creds:
        raise HTTPException(
            status_code=401,
            detail="Google authentication required. Please visit /auth to authenticate."
        )
    
    try:
        # Check if credentials are valid
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                # Refresh expired credentials
                creds.refresh(GoogleRequest())
                # Save refreshed credentials
                save_tokens_to_memory(creds)
            else:
                # Credentials are invalid and can't be refreshed
                clear_tokens_from_memory()
                raise HTTPException(
                    status_code=401,
                    detail="Google authentication expired. Please visit /auth to re-authenticate."
                )
        
        # Build services with valid credentials
        drive_service = build("drive", "v3", credentials=creds)
        docs_service = build("docs", "v1", credentials=creds)
        return drive_service, docs_service
        
    except Exception as e:
        # If there's any error with the token, clear memory and ask for re-authentication
        clear_tokens_from_memory()
        raise HTTPException(
            status_code=401,
            detail=f"Google authentication failed: {str(e)}. Please visit /auth to re-authenticate."
        )

def authenticate_google_services(request: Request):
    """Authenticate with Google services using OAuth 2.0 (legacy method with cookies)."""
    global drive_service, docs_service
    
    # Get session token from cookie
    session_token = request.cookies.get('session_token')
    
    if session_token:
        creds_data = verify_session_token(session_token)
        if creds_data:
            try:
                # Try to use stored credentials
                from google.oauth2.credentials import Credentials
                
                creds = Credentials(
                    token=creds_data['token'],
                    refresh_token=creds_data.get('refresh_token'),
                    token_uri=creds_data['token_uri'],
                    client_id=creds_data['client_id'],
                    client_secret=creds_data.get('client_secret'),
                    scopes=creds_data['scopes']
                )
                
                # Check if credentials are valid
                if creds and creds.valid:
                    # Build services with valid credentials
                    drive_service = build("drive", "v3", credentials=creds)
                    docs_service = build("docs", "v1", credentials=creds)
                    return drive_service, docs_service
                elif creds and creds.expired and creds.refresh_token:
                    # Refresh expired credentials
                    creds.refresh(GoogleRequest())
                    # Update session with new token
                    new_creds_data = {
                        'token': creds.token,
                        'refresh_token': creds.refresh_token,
                        'token_uri': creds.token_uri,
                        'client_id': creds.client_id,
                        'client_secret': creds.client_secret,
                        'scopes': creds.scopes
                    }
                    
                    # Build services with refreshed credentials
                    drive_service = build("drive", "v3", credentials=creds)
                    docs_service = build("docs", "v1", credentials=creds)
                    return drive_service, docs_service
                    
            except Exception as e:
                # Clear invalid credentials
                pass
    
    # No valid credentials - need to authenticate
    raise HTTPException(
        status_code=401,
        detail="Google authentication required. Please visit /auth to authenticate."
    )

@app.get("/")
def root():
    """Health check endpoint."""
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
async def start_oauth_flow():
    """Start OAuth 2.0 flow."""
    try:
        flow = get_oauth_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return RedirectResponse(url=authorization_url)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start OAuth flow: {str(e)}"
        )

@app.get("/oauth2callback")
async def oauth2_callback(code: str, state: str):
    """Handle OAuth 2.0 callback and save tokens to in-memory storage."""
    try:
        # Get the flow
        flow = get_oauth_flow()
        flow.fetch_token(code=code)
        
        # Get credentials
        creds = flow.credentials
        
        # Save credentials to in-memory storage
        if save_tokens_to_memory(creds):
            # Also create session token for browser users (backward compatibility)
            creds_data = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes
            }
            
            session_token = create_session_token(creds_data)
            
            # Create response with cookie
            response = JSONResponse(content={
                "message": "Authentication successful! Tokens saved to memory for API access.",
                "status": "authenticated",
                "note": "You can now use the API endpoints directly or through ChatGPT"
            })
            
            # Set cookie with session token (for browser users)
            response.set_cookie(
                key="session_token",
                value=session_token,
                httponly=True,
                secure=os.environ.get('HEROKU_APP_NAME') is not None,  # HTTPS only in production
                max_age=604800  # 7 days
            )
            
            return response
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to save authentication tokens"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OAuth callback failed: {str(e)}"
        )

@app.post("/create_doc")
async def create_doc(request: DocRequest, http_request: Request):
    """Create a Google Document in Drive."""
    try:
        # Try to get authenticated services using saved tokens first
        try:
            drive_service, docs_service = get_authenticated_services()
        except HTTPException:
            # Fall back to cookie-based authentication for backward compatibility
            drive_service, docs_service = authenticate_google_services(http_request)
        
        # 1. Create the Google Doc file in Drive
        file_metadata = {
            "name": request.name,
            "mimeType": "application/vnd.google-apps.document",
            "parents": ["root"]  # or a folder ID if you want
        }
        
        file = drive_service.files().create(
            body=file_metadata,
            fields="id, webViewLink"
        ).execute()

        return JSONResponse(content={
            "success": True,
            "docId": file["id"],
            "link": file["webViewLink"],
            "name": request.name,
            "message": f"Google Document '{request.name}' created successfully!"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create document: {str(e)}"
        )

@app.post("/create_sheet")
async def create_sheet(request: SheetRequest, http_request: Request):
    """Create a Google Sheet in Drive."""
    try:
        # Try to get authenticated services using saved tokens first
        try:
            drive_service, docs_service = get_authenticated_services()
        except HTTPException:
            # Fall back to cookie-based authentication for backward compatibility
            drive_service, docs_service = authenticate_google_services(http_request)
        
        # Create empty Google Sheet
        file_metadata = {
            'name': request.name,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        
        file = drive_service.files().create(
            body=file_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        sheet_id = file.get('id')
        sheet_name = file.get('name')
        sheet_link = file.get('webViewLink')
        
        return JSONResponse(content={
            "success": True,
            "sheetId": sheet_id,
            "name": sheet_name,
            "link": sheet_link,
            "message": f"Google Sheet '{request.name}' created successfully!"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create sheet: {str(e)}"
        )

# ChatGPT-friendly endpoints
@app.post("/create_doc_chat")
def create_doc_chat(req: DocRequest):
    """ChatGPT-friendly endpoint for creating documents."""
    url = f"{CHATGPT_API_BASE}/create_doc"
    response = requests.post(url, json={"name": req.name})

    if response.status_code == 401:  # Unauthorized
        return {
            "status": "error",
            "message": "Authentication required. Please visit:",
            "auth_url": f"{CHATGPT_API_BASE}/auth"
        }

    return response.json()

@app.post("/create_sheet_chat")
def create_sheet_chat(req: SheetRequest):
    """ChatGPT-friendly endpoint for creating sheets."""
    url = f"{CHATGPT_API_BASE}/create_sheet"
    response = requests.post(url, json={"name": req.name})

    if response.status_code == 401:
        return {
            "status": "error",
            "message": "Authentication required. Please visit:",
            "auth_url": f"{CHATGPT_API_BASE}/auth"
        }

    return response.json()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Google Drive Bridge...")
    print("📝 Complete API with OAuth integration and ChatGPT-friendly endpoints!")
    uvicorn.run(app, host="0.0.0.0", port=8000)

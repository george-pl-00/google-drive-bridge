#!/usr/bin/env python3
"""
Clean Google Drive Bridge - Minimal FastAPI service
Forwards requests to your authenticated Heroku API
"""

from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Google Drive Bridge",
    description="Minimal bridge for creating Google Docs and Sheets",
    version="1.0.0"
)

# Your authenticated Heroku API
API_BASE = "https://google-drive-chatgpt-api-4f8a9bfe61b3.herokuapp.com"

# Request models
class DocRequest(BaseModel):
    name: str

class SheetRequest(BaseModel):
    name: str

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "ok", 
        "message": "Bridge server is running!",
        "endpoints": {
            "create_doc": "POST /create_doc",
            "create_sheet": "POST /create_sheet"
        }
    }

@app.post("/create_doc")
def create_doc(req: DocRequest):
    """Create a Google Document by forwarding to Heroku API."""
    try:
        url = f"{API_BASE}/create_doc"
        response = requests.post(url, json={"name": req.name}, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": f"Document '{req.name}' created successfully!",
                "document_id": result.get("docId"),
                "link": result.get("link"),
                "full_response": result
            }
        else:
            error_detail = response.json() if response.content else response.text
            return {
                "success": False,
                "error": f"Failed to create document: {error_detail}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

@app.post("/create_sheet")
def create_sheet(req: SheetRequest):
    """Create a Google Spreadsheet by forwarding to Heroku API."""
    try:
        url = f"{API_BASE}/create_sheet"
        response = requests.post(url, json={"name": req.name}, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": f"Spreadsheet '{req.name}' created successfully!",
                "sheet_id": result.get("sheetId"),
                "link": result.get("link"),
                "full_response": result
            }
        else:
            error_detail = response.json() if response.content else response.text
            return {
                "success": False,
                "error": f"Failed to create spreadsheet: {error_detail}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Google Drive Bridge...")
    print("📝 Ready to forward requests to your Heroku API!")
    uvicorn.run(app, host="0.0.0.0", port=8000)

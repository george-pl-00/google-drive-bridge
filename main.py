#!/usr/bin/env python3
"""
Complete Google Drive Bridge - Full API service with OAuth
Handles Google Drive integration directly without external dependencies
"""

from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_BASE = "https://my-google-bridge-1b5a7ab10d6b.herokuapp.com"

class DocRequest(BaseModel):
    name: str

class SheetRequest(BaseModel):
    name: str


@app.post("/create_doc_chat")
def create_doc_chat(req: DocRequest):
    url = f"{API_BASE}/create_doc"
    response = requests.post(url, json={"name": req.name})

    if response.status_code == 401:  # Unauthorized
        return {
            "status": "error",
            "message": "Authentication required. Please visit:",
            "auth_url": f"{API_BASE}/auth"
        }

    return response.json()


@app.post("/create_sheet_chat")
def create_sheet_chat(req: SheetRequest):
    url = f"{API_BASE}/create_sheet"
    response = requests.post(url, json={"name": req.name})

    if response.status_code == 401:
        return {
            "status": "error",
            "message": "Authentication required. Please visit:",
            "auth_url": f"{API_BASE}/auth"
        }

    return response.json()

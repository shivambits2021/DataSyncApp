# app/auth.py
import os
from fastapi import APIRouter, HTTPException, Query
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode
from logging_service.log_config import logger
from schemas.source_schema import SheetDataCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from database_manager.sync_data import sync_data_to_db
from database_manager.connections.connect_to_postgres import get_db
# Load environment variables from the .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = (
    "https://www.googleapis.com/auth/spreadsheets.readonly "
    "https://www.googleapis.com/auth/drive.readonly"
)
TOKEN_URL = "https://oauth2.googleapis.com/token"
DRIVE_FILES_API_URL = "https://www.googleapis.com/drive/v3/files"

router = APIRouter()


@router.get("/get-auth-url")
async def get_auth_url():
    logger.info("Requesting Google OAuth URL.")
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    })
    logger.info("Generated Google OAuth URL.")
    return {"auth_url": auth_url}

@router.get("/auth/callback")
async def auth_callback(code: str):
    logger.info("Received callback with authorization code.")
    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(TOKEN_URL, data=token_data)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve access token. Status code: {response.status_code}")
        raise HTTPException(status_code=500, detail="Failed to retrieve access token")

    token_info = response.json()
    access_token = token_info["access_token"]
    logger.info("Access token retrieved successfully.")
    return {"message": "Authenticated successfully", "access_token": access_token}

@router.get("/list-sheets")
async def list_sheets(access_token: str = Query(...)):
    logger.info("Listing sheets from Google Drive.")
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": "mimeType='application/vnd.google-apps.spreadsheet'"}
    response = requests.get(DRIVE_FILES_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"Failed to list sheets. Status code: {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail=response.json())

    files = response.json().get("files", [])
    logger.info(f"Found {len(files)} files.")
    return {"files": [{"id": file["id"], "name": file["name"]} for file in files]}

@router.get("/fetch-data")
async def fetch_data(sheet_id: str, access_token: str, db: Session = Depends(get_db)):
    """
    Fetch data from Google Sheets and sync it to the PostgreSQL database.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    SHEET_API_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1"

    # Fetch data from Google Sheets API
    response = requests.get(SHEET_API_URL, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    sheet_values = response.json().get("values", [])

    # Skip header row and validate data
    sheet_data = []
    for row in sheet_values[1:]:  # Skip the header row
        try:
            # Convert Google Sheets row data to Pydantic models
            sheet_data.append(
                SheetDataCreate(
                    campaign_name=row[0],
                    channel=row[1],
                    impressions=int(row[2]),
                    ctr_percent=float(row[3]),
                    conversions=int(row[4]),
                    cpa_dollars=float(row[5]),
                )
            )
        except (ValueError, IndexError) as e:
            print(f"Skipping row due to error: {e}, Row: {row}")

    # Sync validated data to PostgreSQL
    result = sync_data_to_db(sheet_data, db)

    return result

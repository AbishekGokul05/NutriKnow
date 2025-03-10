# backend/app/api/v1/endpoints/profile.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from app.services.profile_service import (
    get_user_profile,
    update_user_profile,
    update_user_preferences,
    get_user_preferences,
)
from app.database.session import get_db
from sqlalchemy.orm import Session

# Initialize router
router = APIRouter(prefix="/profile", tags=["profile"])

# Pydantic models for request/response
class ProfileRequest(BaseModel):
    name: Optional[str] = None
    profile_picture: Optional[str] = None  # URL or base64 encoded image
    preferences: Optional[dict] = None  # User preferences (e.g., dietary restrictions, allergies, habits)

class ProfileResponse(BaseModel):
    name: str
    profile_picture: Optional[str] = None
    preferences: dict

# Get profile endpoint
@router.get("/{username}", response_model=ProfileResponse)
async def get_profile(username: str, db: Session = Depends(get_db)):
    try:
        profile = get_user_profile(db, username)
        if not profile:
            raise HTTPException(status_code=404, detail="User not found")
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update profile endpoint
@router.put("/{username}", response_model=ProfileResponse)
async def update_profile(username: str, request: ProfileRequest, db: Session = Depends(get_db)):
    try:
        updated_profile = update_user_profile(db, username, request.name, request.profile_picture, request.preferences)
        return updated_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update profile picture endpoint
@router.post("/{username}/profile-picture")
async def update_profile_picture(username: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Save the file (e.g., to a cloud storage service or local storage)
        # For simplicity, we'll assume the file is saved and a URL is returned
        file_url = f"https://example.com/profile-pictures/{file.filename}"
        updated_profile = update_user_profile(db, username, profile_picture=file_url)
        return {"message": "Profile picture updated successfully", "profile_picture": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get user preferences endpoint
@router.get("/{username}/preferences", response_model=dict)
async def get_preferences(username: str, db: Session = Depends(get_db)):
    try:
        preferences = get_user_preferences(db, username)
        if not preferences:
            raise HTTPException(status_code=404, detail="Preferences not found")
        return preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update user preferences endpoint
@router.put("/{username}/preferences", response_model=dict)
async def update_preferences(username: str, preferences: dict, db: Session = Depends(get_db)):
    try:
        updated_preferences = update_user_preferences(db, username, preferences)
        return updated_preferences
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# backend/app/models/profile.py
from pydantic import BaseModel
from typing import Optional, Dict

# Request model for the profile endpoint
class ProfileRequest(BaseModel):
    name: Optional[str] = None  # User's name
    profile_picture: Optional[str] = None  # URL or base64 encoded image
    preferences: Optional[Dict[str, List[str]]] = None  # User preferences (e.g., dietary restrictions, allergies, habits)

# Response model for the profile endpoint
class ProfileResponse(BaseModel):
    name: str  # User's name
    profile_picture: Optional[str] = None  # URL or base64 encoded image
    preferences: Dict[str, List[str]]  # User preferences (e.g., dietary restrictions, allergies, habits)
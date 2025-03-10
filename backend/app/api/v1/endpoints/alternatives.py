# backend/app/api/v1/endpoints/alternatives.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences  # Optional: For user preferences
from app.database.session import get_db  # Optional: For database session
from sqlalchemy.orm import Session  # Optional: For SQLAlchemy Session

# Initialize router
router = APIRouter(prefix="/alternatives", tags=["alternatives"])

# Pydantic models for request/response
class AlternativesRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Optional: Username to fetch user preferences

class AlternativesResponse(BaseModel):
    has_harmful_substances: bool  # Whether harmful substances are present
    alternatives: List[str]  # List of harm-free alternatives or generic recommendations

# Alternatives endpoint
@router.post("/suggest", response_model=AlternativesResponse)
async def suggest_alternatives(request: AlternativesRequest, db: Session = Depends(get_db)):  # Optional: Add db session
    try:
        # Fetch user preferences (if username is provided)
        preferences = None
        if request.username:
            preferences = get_user_preferences(db, request.username)

        # Prepare the prompt for Gemini API
        prompt = f"""
        Here is a list of ingredients extracted from a product: {request.ocr_text}
        User preferences: {preferences if preferences else "Not provided"}

        Analyze the ingredients and determine if any harmful substances are present.
        If harmful substances are present, suggest harm-free alternatives (e.g., "Use paraben-free products").
        If no harmful substances are found, recommend similar products in a generic way (e.g., "Look for sulfate-free shampoos").
        Do not promote any specific product or brand.
        Format the response as a JSON object with keys: has_harmful_substances, alternatives.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)

        # Parse the response into the AlternativesResponse model
        return AlternativesResponse(
            has_harmful_substances=response.get("has_harmful_substances", False),
            alternatives=response.get("alternatives", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
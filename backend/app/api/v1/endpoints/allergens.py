# backend/app/api/v1/endpoints/allergens.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences  # New: Import profile service
from app.database.session import get_db  # New: Import database session
from sqlalchemy.orm import Session  # New: Import SQLAlchemy Session

# Initialize router
router = APIRouter(prefix="/allergens", tags=["allergens"])

# Pydantic models for request/response
class AllergenDetectionRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: str  # New: Username to fetch user preferences

class AllergenInfo(BaseModel):
    ingredient: str  # Ingredient that may cause allergies
    warning: str  # Polite warning about the allergen

class AllergenDetectionResponse(BaseModel):
    allergens: List[AllergenInfo]  # List of allergens and warnings

# Allergen detection endpoint
@router.post("/detect", response_model=AllergenDetectionResponse)
async def detect_allergens(request: AllergenDetectionRequest, db: Session = Depends(get_db)):  # New: Add db session
    try:
        # Fetch user preferences
        preferences = None
        if request.username:  # New: Check if username is provided
            preferences = get_user_preferences(db, request.username)

        # Prepare the prompt for Gemini API
        prompt = f"""
        Here is a list of ingredients extracted from a product: {request.ocr_text}
        User preferences: {preferences}  # New: Include user preferences
        Identify any ingredients that may cause allergies in people.
        For each allergen, provide:
        1. The name of the ingredient.
        2. A polite warning about the allergen.
        Format the response as a JSON list with keys: ingredient, warning.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)

        # Parse the response into a list of AllergenInfo objects
        allergens = []
        for item in response:
            allergens.append(
                AllergenInfo(
                    ingredient=item.get("ingredient", ""),
                    warning=item.get("warning", ""),
                )
            )

        return AllergenDetectionResponse(allergens=allergens)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
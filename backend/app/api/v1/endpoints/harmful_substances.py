# backend/app/api/v1/endpoints/harmful_substances.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences  # New: Import profile service
from app.database.session import get_db  # New: Import database session
from sqlalchemy.orm import Session  # New: Import SQLAlchemy Session

# Initialize router
router = APIRouter(prefix="/harmful-substances", tags=["harmful-substances"])

# Pydantic models for request/response
class HarmfulSubstanceDetectionRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: str  # New: Username to fetch user preferences

class HarmfulSubstanceInfo(BaseModel):
    ingredient: str  # Ingredient that is potentially harmful
    reason: str  # Reason why the ingredient is harmful
    level: str  # Level of the ingredient (e.g., "safe", "above safe limit")

class HarmfulSubstanceDetectionResponse(BaseModel):
    harmful_substances: List[HarmfulSubstanceInfo]  # List of harmful substances and their details

# Harmful substances detection endpoint
@router.post("/detect", response_model=HarmfulSubstanceDetectionResponse)
async def detect_harmful_substances(request: HarmfulSubstanceDetectionRequest, db: Session = Depends(get_db)):  # New: Add db session
    try:
        # Fetch user preferences
        preferences = None
        if request.username:  # New: Check if username is provided
            preferences = get_user_preferences(db, request.username)  # New: Get user preferences


        # Prepare the prompt for Gemini API
        prompt = f"""
        Here is a list of ingredients extracted from a product: {request.ocr_text}
        User preferences: {preferences}  # New: Include user preferences
        Identify any ingredients that are potentially harmful to humans.
        Ignore ingredients that are present in limited amounts and are not harmful.
        For each harmful ingredient, provide:
        1. The name of the ingredient.
        2. The reason why it is harmful.
        3. The level of the ingredient (e.g., "safe", "above safe limit").
        Format the response as a JSON list with keys: ingredient, reason, level.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)

        # Parse the response into a list of HarmfulSubstanceInfo objects
        harmful_substances = []
        for item in response:
            harmful_substances.append(
                HarmfulSubstanceInfo(
                    ingredient=item.get("ingredient", ""),
                    reason=item.get("reason", ""),
                    level=item.get("level", ""),
                )
            )

        return HarmfulSubstanceDetectionResponse(harmful_substances=harmful_substances)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
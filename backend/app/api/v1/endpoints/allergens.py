# backend/app/api/v1/endpoints/allergens.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences
from app.database.session import get_db
from sqlalchemy.orm import Session

# Initialize router
router = APIRouter(prefix="/allergens", tags=["allergens"])

# Pydantic models for request/response
class AllergenDetectionRequest(BaseModel):
    ocr_text: str
    username: Optional[str] = None  # Make username optional with default None

class AllergenInfo(BaseModel):
    ingredient: str
    warning: str

class AllergenDetectionResponse(BaseModel):
    allergens: List[AllergenInfo]

@router.post("/detect", response_model=AllergenDetectionResponse)
async def detect_allergens(request: AllergenDetectionRequest, db: Session = Depends(get_db)):
    try:
        # Validate OCR text
        if not request.ocr_text.strip():
            raise HTTPException(status_code=400, detail="OCR text cannot be empty")

        # Fetch user preferences if username is provided
        preferences = None
        if request.username:
            try:
                preferences = get_user_preferences(db, request.username)
            except Exception as e:
                raise HTTPException(
                    status_code=404,
                    detail=f"Could not fetch preferences for user {request.username}: {str(e)}"
                )

        # Prepare the prompt for Gemini API
        preferences_text = f"User preferences: {preferences}" if preferences else "No specific user preferences provided"
        prompt = f"""
        Here is a list of ingredients extracted from a product: {request.ocr_text}
        {preferences_text}
        Identify any ingredients that may cause allergies in people.
        For each allergen, provide:
        1. The name of the ingredient.
        2. A polite warning about the allergen.
        Format the response as a JSON list with keys: ingredient, warning.
        """

        # Generate response using Gemini API
        try:
            response_text = generate_text(prompt)
            # Parse the response as JSON
            response_data = json.loads(response_text)
            
            if not isinstance(response_data, list):
                raise ValueError("Expected JSON array response")

            # Parse the response into a list of AllergenInfo objects
            allergens = [
                AllergenInfo(
                    ingredient=item.get("ingredient", "Unknown ingredient"),
                    warning=item.get("warning", "No specific warning provided")
                )
                for item in response_data
            ]

            return AllergenDetectionResponse(allergens=allergens)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="Failed to parse allergen detection response"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing allergen detection: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during allergen detection: {str(e)}"
        )
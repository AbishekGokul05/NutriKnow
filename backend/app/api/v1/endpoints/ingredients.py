# backend/app/api/v1/endpoints/ingredient_insight.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger
from app.services.gemini_service import generate_text, parse_json_response
from app.services.profile_service import get_user_preferences
from app.database.session import get_db
from sqlalchemy.orm import Session

# Initialize router
router = APIRouter(prefix="/ingredient-insight", tags=["ingredient-insight"])

# Pydantic models for request/response
class IngredientInsightRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Make username optional with default None

class IngredientInfo(BaseModel):
    ingredient: str  # Common name of the ingredient
    description: str  # Description of the ingredient
    purpose: str  # Purpose of the ingredient in the product

class IngredientInsightResponse(BaseModel):
    ingredients: List[IngredientInfo]  # List of analyzed ingredients

# Ingredient insight endpoint
@router.post("/analyze", response_model=IngredientInsightResponse)
async def analyze_ingredients(request: IngredientInsightRequest, db: Session = Depends(get_db)):
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
                logger.warning(f"Could not fetch preferences for user {request.username}: {str(e)}")
                # Continue without preferences rather than failing

        # Generate response using Gemini API
        response = generate_text(f"""
        Analyze these ingredients and respond with a valid JSON object:
        Product ingredients: {request.ocr_text}
        User preferences: {preferences if preferences else "Not provided"}

        Provide a JSON response in this exact format:
        {{
            "ingredients": [
                {{
                    "ingredient": "name of ingredient",
                    "description": "brief description",
                    "purpose": "purpose in product"
                }}
            ]
        }}
        """)
        
        parsed_response = parse_json_response(response)

        if not isinstance(parsed_response.get("ingredients", []), list):
            raise HTTPException(
                status_code=500,
                detail="Invalid response format from analysis service"
            )

        # Parse the response into a list of IngredientInfo objects
        ingredients = [
            IngredientInfo(
                ingredient=item.get("ingredient", "Unknown ingredient"),
                description=item.get("description", "No description available"),
                purpose=item.get("purpose", "Purpose not specified")
            )
            for item in parsed_response.get("ingredients", [])
        ]

        return IngredientInsightResponse(ingredients=ingredients)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
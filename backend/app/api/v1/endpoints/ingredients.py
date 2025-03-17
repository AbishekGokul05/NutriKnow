# backend/app/api/v1/endpoints/ingredient_insight.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences  # New: Import profile service
from app.database.session import get_db  # New: Import database session
from sqlalchemy.orm import Session  # New: Import SQLAlchemy Session

# Initialize router
router = APIRouter(prefix="/ingredient-insight", tags=["ingredient-insight"])

# Pydantic models for request/response
class IngredientInsightRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: str  # New: Username to fetch user preferences

class IngredientInfo(BaseModel):
    ingredient: str  # Common name of the ingredient
    description: str  # Description of the ingredient
    purpose: str  # Purpose of the ingredient in the product

class IngredientInsightResponse(BaseModel):
    ingredients: List[IngredientInfo]  # List of analyzed ingredients

# Ingredient insight endpoint
@router.post("/analyze", response_model=IngredientInsightResponse)
async def analyze_ingredients(request: IngredientInsightRequest, db: Session = Depends(get_db)):  # New: Add db session
    try:
        # Fetch user preferences
        preferences = None
        if request.username:  # New: Check if username is provided
            preferences = get_user_preferences(db, request.username)  # New: Get user preferences


        # Prepare the prompt for Gemini API
        prompt = f"""
        Here is a list of ingredients extracted from a product: {request.ocr_text}
        User preferences: {preferences}  # New: Include user preferences
        For each ingredient, provide:
        1. The common name of the ingredient.
        2. A brief description of the ingredient.
        3. The purpose of the ingredient in the product.
        Format the response as a JSON list with keys: ingredient, description, purpose.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)

        # Parse the response into a list of IngredientInfo objects
        ingredients = []
        for item in response:
            ingredients.append(
                IngredientInfo(
                    ingredient=item.get("ingredient", ""),
                    description=item.get("description", ""),
                    purpose=item.get("purpose", ""),
                )
            )

        return IngredientInsightResponse(ingredients=ingredients)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
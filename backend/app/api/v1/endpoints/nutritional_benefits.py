# backend/app/api/v1/endpoints/nutritional_benefits.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional  # New: Import Optional
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences  # New: Import profile service
from app.database.session import get_db  # New: Import database session
from sqlalchemy.orm import Session  # New: Import SQLAlchemy Session

# Initialize router
router = APIRouter(prefix="/nutritional-benefits", tags=["nutritional-benefits"])

# Pydantic models for request/response
class NutritionalBenefitsRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # New: Make username optional

class NutritionalBenefitsResponse(BaseModel):
    product_type: str  # Type of product (e.g., "food", "non-food")
    benefits: List[str]  # List of nutritional or usage benefits

# Nutritional benefits endpoint
@router.post("/analyze", response_model=NutritionalBenefitsResponse)
async def analyze_nutritional_benefits(request: NutritionalBenefitsRequest, db: Session = Depends(get_db)):  # New: Add db session
    try:
        # Fetch user preferences (if username is provided)
        preferences = None
        if request.username:  # New: Check if username is provided
            preferences = get_user_preferences(db, request.username)

        # Prepare the prompt for Gemini API
        prompt = f"""
        Here is a list of ingredients extracted from a product: {request.ocr_text}
        User preferences: {preferences if preferences else "Not provided"}  # New: Include preferences if available

        Analyze the ingredients and determine if the product is a food item or non-food item.
        If it is a food item, provide a list of nutritional benefits.
        If it is a non-food item, provide a list of usage benefits.
        Format the response as a JSON object with keys: product_type, benefits.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)

        # Parse the response into the NutritionalBenefitsResponse model
        return NutritionalBenefitsResponse(
            product_type=response.get("product_type", ""),
            benefits=response.get("benefits", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
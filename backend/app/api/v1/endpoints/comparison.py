# backend/app/api/v1/endpoints/comparison.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences  # New: Import profile service
from app.database.session import get_db  # New: Import database session
from sqlalchemy.orm import Session  # New: Import SQLAlchemy Session

# Initialize router
router = APIRouter(prefix="/comparison", tags=["comparison"])

# Pydantic models for request/response
class ProductComparisonRequest(BaseModel):
    ocr_text_1: str  # Extracted text from the first product image
    ocr_text_2: str  # Extracted text from the second product image
    username: str  # New: Username to fetch user preferences

class ProductComparisonResponse(BaseModel):
    better_product: str  # Which product is better (e.g., "Product 1" or "Product 2")
    drawbacks_1: List[str]  # Drawbacks of the first product
    drawbacks_2: List[str]  # Drawbacks of the second product
    insights: str  # Detailed comparison insights

# Product comparison endpoint
@router.post("/compare", response_model=ProductComparisonResponse)
async def compare_products(request: ProductComparisonRequest, db: Session = Depends(get_db)):  # New: Add db session
    try:
        # Fetch user preferences
        preferences = None
        if request.username:  # New: Check if username is provided
            preferences = get_user_preferences(db, request.username)

        # Prepare the prompt for Gemini API
        prompt = f"""
        Here are the ingredients of two products:
        Product 1: {request.ocr_text_1}
        Product 2: {request.ocr_text_2}
        User preferences: {preferences}  # New: Include user preferences

        Compare the two products and provide the following:
        1. Which product is better and why?
        2. List the drawbacks of Product 1.
        3. List the drawbacks of Product 2.
        4. Provide detailed insights about the comparison.
        Format the response as a JSON object with keys: better_product, drawbacks_1, drawbacks_2, insights.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)

        # Parse the response into the ProductComparisonResponse model
        return ProductComparisonResponse(
            better_product=response.get("better_product", ""),
            drawbacks_1=response.get("drawbacks_1", []),
            drawbacks_2=response.get("drawbacks_2", []),
            insights=response.get("insights", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
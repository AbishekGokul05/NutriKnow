# backend/app/models/ingredients.py
from pydantic import BaseModel
from typing import List, Optional

# Request model for the ingredients analysis endpoint
class IngredientAnalysisRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Model for individual ingredient details
class IngredientInfo(BaseModel):
    ingredient: str  # Common name of the ingredient
    description: str  # Description of the ingredient
    purpose: str  # Purpose of the ingredient in the product

# Response model for the ingredients analysis endpoint
class IngredientAnalysisResponse(BaseModel):
    ingredients: List[IngredientInfo]  # List of analyzed ingredients
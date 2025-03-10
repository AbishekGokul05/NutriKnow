# backend/app/models/allergens.py
from pydantic import BaseModel
from typing import List, Optional

# Request model for the allergen detection endpoint
class AllergenDetectionRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Model for individual allergen details
class AllergenInfo(BaseModel):
    ingredient: str  # Ingredient that may cause allergies
    warning: str  # Polite warning about the allergen

# Response model for the allergen detection endpoint
class AllergenDetectionResponse(BaseModel):
    allergens: List[AllergenInfo]  # List of allergens and warnings
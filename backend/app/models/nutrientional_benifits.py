# backend/app/models/nutritional_benefits.py
from pydantic import BaseModel
from typing import List, Optional

# Request model for the nutritional benefits endpoint
class NutritionalBenefitsRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Response model for the nutritional benefits endpoint
class NutritionalBenefitsResponse(BaseModel):
    product_type: str  # Type of product (e.g., "food", "non-food")
    benefits: List[str]  # List of nutritional or usage benefits
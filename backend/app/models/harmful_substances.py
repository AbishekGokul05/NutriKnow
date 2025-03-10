# backend/app/models/harmful_substances.py
from pydantic import BaseModel
from typing import List, Optional

# Request model for the harmful substances detection endpoint
class HarmfulSubstanceDetectionRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Model for individual harmful substance details
class HarmfulSubstanceInfo(BaseModel):
    ingredient: str  # Ingredient that is potentially harmful
    reason: str  # Reason why the ingredient is harmful
    level: str  # Level of the ingredient (e.g., "safe", "above safe limit")

# Response model for the harmful substances detection endpoint
class HarmfulSubstanceDetectionResponse(BaseModel):
    harmful_substances: List[HarmfulSubstanceInfo]  # List of harmful substances and their details
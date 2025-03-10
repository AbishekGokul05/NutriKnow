# backend/app/models/alternatives.py
from pydantic import BaseModel
from typing import List, Optional

# Request model for the alternatives endpoint
class AlternativesRequest(BaseModel):
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Response model for the alternatives endpoint
class AlternativesResponse(BaseModel):
    has_harmful_substances: bool  # Whether harmful substances are present
    alternatives: List[str]  # List of harm-free alternatives or generic recommendations
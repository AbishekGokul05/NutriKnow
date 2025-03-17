from pydantic import BaseModel
from typing import List, Optional

class IngredientInfo(BaseModel):
    name: str
    description: str
    purpose: str

class IngredientAnalysisRequest(BaseModel):
    ocr_text: str
    username: Optional[str] = None

class IngredientAnalysisResponse(BaseModel):
    ingredients: List[IngredientInfo] 
from pydantic import BaseModel
from typing import List, Optional

class NutritionalBenefitsRequest(BaseModel):
    ocr_text: str
    username: Optional[str] = None

class NutritionalBenefitsResponse(BaseModel):
    product_type: str
    benefits: List[str] 
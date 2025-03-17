from pydantic import BaseModel
from typing import List, Optional

class ProductComparisonRequest(BaseModel):
    ocr_text_1: str
    ocr_text_2: str
    username: Optional[str] = None

class ProductComparisonResponse(BaseModel):
    better_product: str
    drawbacks_1: List[str]
    drawbacks_2: List[str]
    insights: str 
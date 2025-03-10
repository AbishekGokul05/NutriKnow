# backend/app/models/comparison.py
from pydantic import BaseModel
from typing import List, Optional

# Request model for the product comparison endpoint
class ProductComparisonRequest(BaseModel):
    ocr_text_1: str  # Extracted text from the first product image
    ocr_text_2: str  # Extracted text from the second product image
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Response model for the product comparison endpoint
class ProductComparisonResponse(BaseModel):
    better_product: str  # Which product is better (e.g., "Product 1" or "Product 2")
    drawbacks_1: List[str]  # Drawbacks of the first product
    drawbacks_2: List[str]  # Drawbacks of the second product
    insights: str  # Detailed comparison insights
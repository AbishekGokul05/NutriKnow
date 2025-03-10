# backend/app/models/history.py
from pydantic import BaseModel
from typing import List, Dict

# Model for a single history entry
class HistoryEntry(BaseModel):
    product_name: str  # Name of the product
    analysis: Dict[str, List[str]]  # Analysis results for the product (e.g., ingredients, allergens, harmful substances)

# Response model for the history endpoint
class HistoryResponse(BaseModel):
    history: List[HistoryEntry]  # List of history entries
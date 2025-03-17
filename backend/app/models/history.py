# backend/app/models/history.py
from app.database.models import History  # Import History from database.models
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Add any Pydantic models related to history here if needed
class HistoryEntry(BaseModel):
    id: int
    user_id: int
    product_name: str
    analysis: Dict[str, Any]
    created_at: Optional[str] = None
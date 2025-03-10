# backend/app/api/v1/endpoints/history.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.history_service import add_to_history, get_history
from app.database.session import get_db
from sqlalchemy.orm import Session

# Initialize router
router = APIRouter(prefix="/history", tags=["history"])

# Pydantic models for request/response
class HistoryEntry(BaseModel):
    product_name: str  # Name of the product
    analysis: dict  # Analysis results for the product

class HistoryResponse(BaseModel):
    history: List[HistoryEntry]  # List of history entries

# Add to history endpoint
@router.post("/add", response_model=HistoryEntry)
async def add_history_entry(user_id: int, product_name: str, analysis: dict, db: Session = Depends(get_db)):
    try:
        # Add the new entry to the history
        new_entry = add_to_history(db, user_id, product_name, analysis)
        return new_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get history endpoint
@router.get("/{user_id}", response_model=HistoryResponse)
async def get_user_history(user_id: int, db: Session = Depends(get_db)):
    try:
        # Fetch the last 10 history entries for the user
        history = get_history(db, user_id)
        return HistoryResponse(history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
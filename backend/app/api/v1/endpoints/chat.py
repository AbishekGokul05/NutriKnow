# backend/app/api/v1/endpoints/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences  # New: Import profile service
from app.database.session import get_db  # New: Import database session
from sqlalchemy.orm import Session  # New: Import SQLAlchemy Session

# Initialize router
router = APIRouter(prefix="/chat", tags=["chat"])

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str  # User's chat message
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: str  # New: Username to fetch user preferences

class ChatResponse(BaseModel):
    response: str  # AI-generated response

# Chat endpoint
@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):  # New: Add db session
    try:
        # Fetch user preferences
        preferences = None
        if request.username:  # New: Check if username is provided
            preferences = get_user_preferences(db, request.username)

        # Combine OCR text, user message, and preferences for context
        prompt = f"""
        Here is the text extracted from the product image: {request.ocr_text}
        User preferences: {preferences}  # New: Include user preferences
        User's question: {request.message}
        Please provide a detailed response.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
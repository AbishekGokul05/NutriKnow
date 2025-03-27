# backend/app/api/v1/endpoints/chat.py
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from app.services.gemini_service import generate_text
from app.services.profile_service import get_user_preferences
from app.database.session import get_db
from sqlalchemy.orm import Session
import easyocr
from PIL import Image
import io
import numpy as np
from typing import Optional

# Initialize router
router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize EasyOCR reader (do this only once to optimize performance)
reader = easyocr.Reader(['en'])

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    username: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

# Chat endpoint
@router.post("/", response_model=ChatResponse)
async def chat(
    message: str = Form(...),
    file: UploadFile = File(...),
    username: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Read image file and convert to numpy array for EasyOCR
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Extract text using EasyOCR
        results = reader.readtext(image_np)
        ocr_text = ' '.join([result[1] for result in results])  # Extract text from results
        
        # Fetch user preferences if username is provided
        preferences = None
        if username:
            try:
                preferences = get_user_preferences(db, username)
            except Exception as e:
                # Just log the error and continue without preferences
                print(f"Could not fetch preferences for user {username}: {str(e)}")
        
        # Combine OCR text, user message, and preferences for context
        prompt = f"""
        Here is the text extracted from the product image: {ocr_text}
        User preferences: {preferences if preferences else "Not provided"}
        User's question: {message}
        Please provide a detailed response.
        """

        # Generate response using Gemini API
        response = generate_text(prompt)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
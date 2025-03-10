# backend/app/models/chat.py
from pydantic import BaseModel

# Request model for the chat endpoint
class ChatRequest(BaseModel):
    message: str  # User's chat message
    ocr_text: str  # Extracted text from the uploaded image (ingredients list)
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Response model for the chat endpoint
class ChatResponse(BaseModel):
    response: str  # AI-generated response
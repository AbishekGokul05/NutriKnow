# backend/app/models/chat.py
from pydantic import BaseModel
from typing import Optional

# Request model for the chat endpoint
class ChatRequest(BaseModel):
    message: str  # User's chat message
    username: Optional[str] = None  # Optional: Username to fetch user preferences

# Response model for the chat endpoint
class ChatResponse(BaseModel):
    response: str  # AI-generated response
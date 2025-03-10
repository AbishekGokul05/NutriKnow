# backend/app/services/__init__.py
from .gemini_service import generate_text
from .ocr_service import extract_text_from_image
from .profile_service import (
    get_user_profile,
    update_user_profile,
    get_user_preferences,
    update_user_preferences,
)
from .history_service import add_to_history, get_history

# Expose all services for easy access
__all__ = [
    # Gemini service
    "generate_text",

    # OCR service
    "extract_text_from_image",

    # Profile services
    "get_user_profile",
    "update_user_profile",
    "get_user_preferences",
    "update_user_preferences",

    # History services
    "add_to_history",
    "get_history",
]
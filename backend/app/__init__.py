# backend/app/__init__.py
from .main import app  # Expose the FastAPI app instance
from .api.v1.endpoints import (
    chat,
    ingredients,
    comparison,
    allergens,
    harmful_substances,
    nutritional_benefits,
    alternatives,
    profile,  # New: Profile endpoint
    history,  # New: History endpoint
)

# Optional: Expose commonly used models and services
from .models import (
    chat as chat_models,
    ingredients as ingredient_models,
    profile as profile_models,  # New: Profile models
    history as history_models,  # New: History models
)
from .services import (
    gemini_service,
    ocr_service,
    profile_service,  # New: Profile service
    history_service,  # New: History service
)

__all__ = [
    "app",
    "chat",
    "ingredients",
    "comparison",
    "allergens",
    "harmful_substances",
    "nutritional_benefits",
    "alternatives",
    "profile",  # New: Profile endpoint
    "history",  # New: History endpoint
    "chat_models",
    "ingredient_models",
    "profile_models",  # New: Profile models
    "history_models",  # New: History models
    "gemini_service",
    "ocr_service",
    "profile_service",  # New: Profile service
    "history_service",  # New: History service
]
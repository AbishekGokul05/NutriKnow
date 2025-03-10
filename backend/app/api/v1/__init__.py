# backend/app/api/v1/__init__.py
from .endpoints import (
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

# Expose all routers for easy access
__all__ = [
    "chat",
    "ingredients",
    "comparison",
    "allergens",
    "harmful_substances",
    "nutritional_benefits",
    "alternatives",
    "profile",  # New: Profile endpoint
    "history",  # New: History endpoint
]
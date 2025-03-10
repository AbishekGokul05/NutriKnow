# backend/app/api/__init__.py
from .v1.endpoints import (
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
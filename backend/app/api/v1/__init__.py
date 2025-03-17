# backend/app/api/v1/__init__.py
from fastapi import APIRouter
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

# Create v1 router
router = APIRouter()

# Include all endpoint routers
router.include_router(chat.router, tags=["chat"])
router.include_router(ingredients.router, tags=["ingredients"])
router.include_router(comparison.router, tags=["comparison"])
router.include_router(allergens.router, tags=["allergens"])
router.include_router(harmful_substances.router, tags=["harmful_substances"])
router.include_router(nutritional_benefits.router, tags=["nutritional_benefits"])
router.include_router(alternatives.router, tags=["alternatives"])
router.include_router(profile.router, tags=["profile"])
router.include_router(history.router, tags=["history"])

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
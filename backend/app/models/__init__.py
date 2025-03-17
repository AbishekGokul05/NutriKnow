# backend/app/models/__init__.py
from app.database.models import User, Profile, History
from .chat import ChatRequest, ChatResponse
from .ingredients import IngredientAnalysisRequest, IngredientInfo, IngredientAnalysisResponse
from .comparison import ProductComparisonRequest, ProductComparisonResponse
from .allergens import AllergenDetectionRequest, AllergenInfo, AllergenDetectionResponse
from .harmful_substances import HarmfulSubstanceDetectionRequest, HarmfulSubstanceInfo, HarmfulSubstanceDetectionResponse
from .nutritional_benefits import NutritionalBenefitsRequest, NutritionalBenefitsResponse
from .alternatives import AlternativesRequest, AlternativesResponse
from .profile import ProfileRequest, ProfileResponse

# Expose all models for easy access
__all__ = [
    # Database Models
    "User",
    "Profile",
    "History",

    # Chat Models
    "ChatRequest",
    "ChatResponse",

    # Ingredients Models
    "IngredientAnalysisRequest",
    "IngredientInfo",
    "IngredientAnalysisResponse",

    # Comparison Models
    "ProductComparisonRequest",
    "ProductComparisonResponse",

    # Allergens Models
    "AllergenDetectionRequest",
    "AllergenInfo",
    "AllergenDetectionResponse",

    # Harmful Substances Models
    "HarmfulSubstanceDetectionRequest",
    "HarmfulSubstanceInfo",
    "HarmfulSubstanceDetectionResponse",

    # Nutritional Benefits Models
    "NutritionalBenefitsRequest",
    "NutritionalBenefitsResponse",

    # Alternatives Models
    "AlternativesRequest",
    "AlternativesResponse",

    # Profile Models
    "ProfileRequest",
    "ProfileResponse"
]
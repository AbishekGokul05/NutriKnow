# backend/app/models/__init__.py
from .chat import ChatRequest, ChatResponse
from .ingredients import IngredientAnalysisRequest, IngredientInfo, IngredientAnalysisResponse
from .comparison import ProductComparisonRequest, ProductComparisonResponse
from .allergens import AllergenDetectionRequest, AllergenInfo, AllergenDetectionResponse
from .harmful_substances import HarmfulSubstanceDetectionRequest, HarmfulSubstanceInfo, HarmfulSubstanceDetectionResponse
from .nutritional_benefits import NutritionalBenefitsRequest, NutritionalBenefitsResponse
from .alternatives import AlternativesRequest, AlternativesResponse
from .profile import ProfileRequest, ProfileResponse
from .history import HistoryEntry, HistoryResponse

# Expose all models for easy access
__all__ = [
    # Chat models
    "ChatRequest",
    "ChatResponse",

    # Ingredients models
    "IngredientAnalysisRequest",
    "IngredientInfo",
    "IngredientAnalysisResponse",

    # Comparison models
    "ProductComparisonRequest",
    "ProductComparisonResponse",

    # Allergens models
    "AllergenDetectionRequest",
    "AllergenInfo",
    "AllergenDetectionResponse",

    # Harmful substances models
    "HarmfulSubstanceDetectionRequest",
    "HarmfulSubstanceInfo",
    "HarmfulSubstanceDetectionResponse",

    # Nutritional benefits models
    "NutritionalBenefitsRequest",
    "NutritionalBenefitsResponse",

    # Alternatives models
    "AlternativesRequest",
    "AlternativesResponse",

    # Profile models
    "ProfileRequest",
    "ProfileResponse",

    # History models
    "HistoryEntry",
    "HistoryResponse",
]
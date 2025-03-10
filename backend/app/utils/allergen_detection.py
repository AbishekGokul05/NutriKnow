# backend/app/utils/allergen_detection.py

from typing import List, Dict, Optional
import logging
from app.utils.gemini_integration import call_gemini_api

# Set up logging
logger = logging.getLogger(__name__)

async def detect_allergens(ingredients: List[str], user_allergens: Optional[List[str]] = None) -> Dict[str, List[str]]:
    """
    Detect allergens in a list of ingredients and compare them with user allergens.

    Args:
        ingredients (List[str]): List of product ingredients.
        user_allergens (Optional[List[str]]): List of allergens the user is sensitive to.

    Returns:
        Dict[str, List[str]]: Dictionary containing detected allergens and warnings.
    """
    try:
        detected_allergens = []
        warnings = []

        # Fetch known allergens from Gemini API
        known_allergens = await get_known_allergens_from_gemini()
        if not known_allergens:
            logger.error("Failed to fetch known allergens from Gemini API")
            return {"error": "Failed to fetch known allergens"}

        # Check for allergens in ingredients
        for ingredient in ingredients:
            for allergen in known_allergens:
                if allergen.lower() in ingredient.lower():
                    detected_allergens.append(allergen)

        # Check for user-specific allergens
        if user_allergens:
            for allergen in user_allergens:
                if allergen.lower() in [ing.lower() for ing in ingredients]:
                    warnings.append(f"Contains {allergen} (user allergen)")

        logger.info("Allergen detection completed successfully")
        return {
            "detected_allergens": detected_allergens,
            "warnings": warnings,
        }

    except Exception as e:
        logger.error(f"Error detecting allergens: {e}")
        return {"error": "Failed to detect allergens"}

async def get_known_allergens_from_gemini() -> Optional[List[str]]:
    """
    Fetch a list of known allergens from the Gemini API.

    Returns:
        Optional[List[str]]: List of known allergens, or None if the request fails.
    """
    try:
        # Call Gemini API to get known allergens
        payload = {
            "query": "Provide a list of common food allergens."
        }
        response = await call_gemini_api("/query", payload)
        if response and "response" in response:
            # Parse the response to extract allergens (assuming response is a comma-separated list)
            allergens = response["response"].split(",")
            return [allergen.strip() for allergen in allergens]
        return None
    except Exception as e:
        logger.error(f"Error fetching known allergens from Gemini API: {e}")
        return None
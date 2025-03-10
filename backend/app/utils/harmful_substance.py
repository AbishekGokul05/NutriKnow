# backend/app/utils/harmful_substance_detection.py

from typing import List, Dict, Optional
import logging
from app.utils.gemini_integration import call_gemini_api

# Set up logging
logger = logging.getLogger(__name__)

async def detect_harmful_substances(ingredients: List[str], user_restrictions: Optional[List[str]] = None) -> Dict[str, List[str]]:
    """
    Detect harmful substances in a list of ingredients and compare them with user restrictions.

    Args:
        ingredients (List[str]): List of product ingredients.
        user_restrictions (Optional[List[str]]): List of harmful substances the user wants to avoid.

    Returns:
        Dict[str, List[str]]: Dictionary containing detected harmful substances and warnings.
    """
    try:
        detected_substances = []
        warnings = []

        # Fetch known harmful substances from Gemini API
        known_substances = await get_known_harmful_substances_from_gemini()
        if not known_substances:
            logger.error("Failed to fetch known harmful substances from Gemini API")
            return {"error": "Failed to fetch known harmful substances"}

        # Check for harmful substances in ingredients
        for ingredient in ingredients:
            for substance in known_substances:
                if substance.lower() in ingredient.lower():
                    detected_substances.append(substance)

        # Check for user-specific restrictions
        if user_restrictions:
            for substance in user_restrictions:
                if substance.lower() in [ing.lower() for ing in ingredients]:
                    warnings.append(f"Contains {substance} (user restriction)")

        logger.info("Harmful substance detection completed successfully")
        return {
            "detected_substances": detected_substances,
            "warnings": warnings,
        }

    except Exception as e:
        logger.error(f"Error detecting harmful substances: {e}")
        return {"error": "Failed to detect harmful substances"}

async def get_known_harmful_substances_from_gemini() -> Optional[List[str]]:
    """
    Fetch a list of known harmful substances from the Gemini API.

    Returns:
        Optional[List[str]]: List of known harmful substances, or None if the request fails.
    """
    try:
        # Call Gemini API to get known harmful substances
        payload = {
            "query": "Provide a list of common harmful substances in food and consumer products."
        }
        response = await call_gemini_api("/query", payload)
        if response and "response" in response:
            # Parse the response to extract harmful substances (assuming response is a comma-separated list)
            substances = response["response"].split(",")
            return [substance.strip() for substance in substances]
        return None
    except Exception as e:
        logger.error(f"Error fetching known harmful substances from Gemini API: {e}")
        return None
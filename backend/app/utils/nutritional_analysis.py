# backend/app/utils/nutritional_analysis.py

from typing import Dict, List, Optional
import logging
from app.utils.gemini_integration import call_gemini_api

# Set up logging
logger = logging.getLogger(__name__)

def calculate_nutritional_benefits(nutrition_data: Dict[str, float], user_restrictions: Optional[Dict[str, List[str]]] = None) -> Dict[str, Any]:
    """
    Calculate nutritional benefits based on product nutrition data and user restrictions.

    Args:
        nutrition_data (Dict[str, float]): Nutritional data for the product (e.g., {"calories": 150, "protein": 10}).
        user_restrictions (Optional[Dict[str, List[str]]]): User dietary restrictions (e.g., {"allergens": ["gluten"], "diet": ["low-sodium"]}).

    Returns:
        Dict[str, Any]: Analysis results including benefits, warnings, and RDI comparison.
    """
    try:
        analysis_results = {
            "benefits": [],
            "warnings": [],
            "rdi_comparison": {},
        }

        # Calculate RDI percentages
        for nutrient, value in nutrition_data.items():
            rdi_value = get_rdi_from_gemini(nutrient)
            if rdi_value:
                rdi_percentage = (value / rdi_value) * 100
                analysis_results["rdi_comparison"][nutrient] = f"{rdi_percentage:.2f}%"
                if rdi_percentage > 100:
                    analysis_results["warnings"].append(f"High {nutrient} ({rdi_percentage:.2f}% of RDI)")
                elif rdi_percentage < 20:
                    analysis_results["benefits"].append(f"Low {nutrient} ({rdi_percentage:.2f}% of RDI)")

        # Check for user restrictions
        if user_restrictions:
            if "allergens" in user_restrictions:
                for allergen in user_restrictions["allergens"]:
                    if allergen.lower() in str(nutrition_data).lower():
                        analysis_results["warnings"].append(f"Contains {allergen}")

            if "diet" in user_restrictions:
                for diet in user_restrictions["diet"]:
                    diet_analysis = get_diet_analysis_from_gemini(nutrition_data, diet)
                    if diet_analysis:
                        analysis_results["warnings"].extend(diet_analysis)

        logger.info("Nutritional analysis completed successfully")
        return analysis_results

    except Exception as e:
        logger.error(f"Error performing nutritional analysis: {e}")
        return {"error": "Failed to perform nutritional analysis"}

async def get_rdi_from_gemini(nutrient: str) -> Optional[float]:
    """
    Fetch the Recommended Daily Intake (RDI) for a nutrient from the Gemini API.

    Args:
        nutrient (str): Nutrient name (e.g., "calories", "protein").

    Returns:
        Optional[float]: RDI value for the nutrient, or None if not available.
    """
    try:
        # Call Gemini API to get RDI for the nutrient
        payload = {
            "query": f"What is the Recommended Daily Intake (RDI) for {nutrient} for an average adult?"
        }
        response = await call_gemini_api("/query", payload)
        if response and "response" in response:
            # Extract RDI value from the response (assuming the response contains a numeric value)
            rdi_value = float(response["response"].split()[0])  # Example: "2000 calories" -> 2000
            return rdi_value
        return None
    except Exception as e:
        logger.error(f"Error fetching RDI from Gemini API: {e}")
        return None

async def get_diet_analysis_from_gemini(nutrition_data: Dict[str, float], diet: str) -> Optional[List[str]]:
    """
    Fetch diet-specific analysis from the Gemini API.

    Args:
        nutrition_data (Dict[str, float]): Nutritional data for the product.
        diet (str): Diet type (e.g., "low-sodium", "low-sugar").

    Returns:
        Optional[List[str]]: List of warnings or recommendations, or None if not available.
    """
    try:
        # Call Gemini API to get diet-specific analysis
        payload = {
            "query": f"Is this product suitable for a {diet} diet? Nutritional data: {nutrition_data}"
        }
        response = await call_gemini_api("/query", payload)
        if response and "response" in response:
            # Parse the response for warnings or recommendations
            return [response["response"]]
        return None
    except Exception as e:
        logger.error(f"Error fetching diet analysis from Gemini API: {e}")
        return None
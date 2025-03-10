# backend/app/utils/product_comparison.py

from typing import Dict, List, Optional
import logging
from app.utils.gemini_integration import call_gemini_api

# Set up logging
logger = logging.getLogger(__name__)

async def compare_products(
    product1: Dict[str, Any],
    product2: Dict[str, Any],
    user_restrictions: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, Any]:
    """
    Compare two products based on nutritional data, allergens, and harmful substances.

    Args:
        product1 (Dict[str, Any]): First product's data (e.g., {"name": "Product A", "nutrition": {...}, "allergens": [...], "harmful_substances": [...]}).
        product2 (Dict[str, Any]): Second product's data.
        user_restrictions (Optional[Dict[str, List[str]]]): User dietary restrictions and preferences.

    Returns:
        Dict[str, Any]: Comparison results including scores, insights, and recommendations.
    """
    try:
        comparison_results = {
            "product1": product1["name"],
            "product2": product2["name"],
            "scores": {},
            "insights": [],
            "recommendation": None,
        }

        # Compare nutritional data
        nutrition_comparison = await compare_nutrition(product1["nutrition"], product2["nutrition"])
        comparison_results["scores"]["nutrition"] = nutrition_comparison["score"]
        comparison_results["insights"].extend(nutrition_comparison["insights"])

        # Compare allergens
        allergen_comparison = await compare_allergens(product1["allergens"], product2["allergens"], user_restrictions)
        comparison_results["scores"]["allergens"] = allergen_comparison["score"]
        comparison_results["insights"].extend(allergen_comparison["insights"])

        # Compare harmful substances
        harmful_substance_comparison = await compare_harmful_substances(
            product1["harmful_substances"], product2["harmful_substances"], user_restrictions
        )
        comparison_results["scores"]["harmful_substances"] = harmful_substance_comparison["score"]
        comparison_results["insights"].extend(harmful_substance_comparison["insights"])

        # Generate overall recommendation
        overall_score = (
            comparison_results["scores"]["nutrition"]
            + comparison_results["scores"]["allergens"]
            + comparison_results["scores"]["harmful_substances"]
        )
        if overall_score > 0:
            comparison_results["recommendation"] = product1["name"]
        else:
            comparison_results["recommendation"] = product2["name"]

        logger.info("Product comparison completed successfully")
        return comparison_results

    except Exception as e:
        logger.error(f"Error comparing products: {e}")
        return {"error": "Failed to compare products"}

async def compare_nutrition(nutrition1: Dict[str, float], nutrition2: Dict[str, float]) -> Dict[str, Any]:
    """
    Compare nutritional data of two products.

    Args:
        nutrition1 (Dict[str, float]): Nutritional data of the first product.
        nutrition2 (Dict[str, float]): Nutritional data of the second product.

    Returns:
        Dict[str, Any]: Comparison results including score and insights.
    """
    try:
        insights = []
        score = 0

        # Fetch RDI values from Gemini API
        rdi_values = await get_rdi_values_from_gemini()

        # Compare each nutrient
        for nutrient, value1 in nutrition1.items():
            value2 = nutrition2.get(nutrient, 0)
            rdi_value = rdi_values.get(nutrient, 1)  # Default to 1 to avoid division by zero

            # Calculate percentage of RDI
            percent1 = (value1 / rdi_value) * 100
            percent2 = (value2 / rdi_value) * 100

            # Compare percentages
            if percent1 < percent2:
                insights.append(f"{nutrient}: {product1['name']} has lower {nutrient} ({percent1:.2f}% vs {percent2:.2f}% of RDI)")
                score += 1
            elif percent1 > percent2:
                insights.append(f"{nutrient}: {product2['name']} has lower {nutrient} ({percent2:.2f}% vs {percent1:.2f}% of RDI)")
                score -= 1

        return {"score": score, "insights": insights}

    except Exception as e:
        logger.error(f"Error comparing nutrition: {e}")
        return {"score": 0, "insights": []}

async def compare_allergens(allergens1: List[str], allergens2: List[str], user_restrictions: Optional[Dict[str, List[str]]] = None) -> Dict[str, Any]:
    """
    Compare allergens of two products.

    Args:
        allergens1 (List[str]): Allergens in the first product.
        allergens2 (List[str]): Allergens in the second product.
        user_restrictions (Optional[Dict[str, List[str]]]): User dietary restrictions.

    Returns:
        Dict[str, Any]: Comparison results including score and insights.
    """
    try:
        insights = []
        score = 0

        # Check for user-specific allergens
        if user_restrictions and "allergens" in user_restrictions:
            user_allergens = user_restrictions["allergens"]
            for allergen in user_allergens:
                if allergen in allergens1:
                    insights.append(f"{product1['name']} contains {allergen} (user allergen)")
                    score -= 1
                if allergen in allergens2:
                    insights.append(f"{product2['name']} contains {allergen} (user allergen)")
                    score += 1

        return {"score": score, "insights": insights}

    except Exception as e:
        logger.error(f"Error comparing allergens: {e}")
        return {"score": 0, "insights": []}

async def compare_harmful_substances(substances1: List[str], substances2: List[str], user_restrictions: Optional[Dict[str, List[str]]] = None) -> Dict[str, Any]:
    """
    Compare harmful substances of two products.

    Args:
        substances1 (List[str]): Harmful substances in the first product.
        substances2 (List[str]): Harmful substances in the second product.
        user_restrictions (Optional[Dict[str, List[str]]]): User restrictions.

    Returns:
        Dict[str, Any]: Comparison results including score and insights.
    """
    try:
        insights = []
        score = 0

        # Check for user-specific restrictions
        if user_restrictions and "harmful_substances" in user_restrictions:
            user_substances = user_restrictions["harmful_substances"]
            for substance in user_substances:
                if substance in substances1:
                    insights.append(f"{product1['name']} contains {substance} (user restriction)")
                    score -= 1
                if substance in substances2:
                    insights.append(f"{product2['name']} contains {substance} (user restriction)")
                    score += 1

        return {"score": score, "insights": insights}

    except Exception as e:
        logger.error(f"Error comparing harmful substances: {e}")
        return {"score": 0, "insights": []}

async def get_rdi_values_from_gemini() -> Dict[str, float]:
    """
    Fetch Recommended Daily Intake (RDI) values from the Gemini API.

    Returns:
        Dict[str, float]: Dictionary of RDI values for nutrients.
    """
    try:
        payload = {
            "query": "Provide the Recommended Daily Intake (RDI) values for common nutrients."
        }
        response = await call_gemini_api("/query", payload)
        if response and "response" in response:
            # Parse the response to extract RDI values (assuming response is a dictionary)
            return response["response"]
        return {}
    except Exception as e:
        logger.error(f"Error fetching RDI values from Gemini API: {e}")
        return {}
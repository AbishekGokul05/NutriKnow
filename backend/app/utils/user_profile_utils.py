# backend/app/utils/user_profile_utils.py

from typing import Dict, List, Optional
import logging
from app.utils.gemini_integration import call_gemini_api

# Set up logging
logger = logging.getLogger(__name__)

async def update_user_preferences(user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update user preferences in the database or external service.

    Args:
        user_id (str): Unique identifier for the user.
        preferences (Dict[str, Any]): User preferences to update (e.g., {"diet": "vegetarian", "allergens": ["gluten"]}).

    Returns:
        Dict[str, Any]: Confirmation of the update.
    """
    try:
        # Simulate updating preferences in a database or external service
        logger.info(f"Updating preferences for user {user_id}: {preferences}")

        # Call Gemini API to get personalized recommendations based on updated preferences
        payload = {
            "query": f"Provide personalized recommendations for a user with preferences: {preferences}"
        }
        response = await call_gemini_api("/query", payload)
        if response and "response" in response:
            recommendations = response["response"]
        else:
            recommendations = "No recommendations available."

        return {
            "status": "success",
            "message": "Preferences updated successfully",
            "recommendations": recommendations,
        }

    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        return {"status": "error", "message": "Failed to update preferences"}

async def get_user_preferences(user_id: str) -> Dict[str, Any]:
    """
    Retrieve user preferences from the database or external service.

    Args:
        user_id (str): Unique identifier for the user.

    Returns:
        Dict[str, Any]: User preferences.
    """
    try:
        # Simulate fetching preferences from a database or external service
        logger.info(f"Fetching preferences for user {user_id}")

        # Example preferences (replace with actual database query)
        preferences = {
            "diet": "vegetarian",
            "allergens": ["gluten", "nuts"],
            "harmful_substances": ["sodium benzoate"],
        }

        return {
            "status": "success",
            "preferences": preferences,
        }

    except Exception as e:
        logger.error(f"Error fetching user preferences: {e}")
        return {"status": "error", "message": "Failed to fetch preferences"}

async def get_personalized_recommendations(user_id: str) -> Dict[str, Any]:
    """
    Get personalized recommendations for a user based on their profile.

    Args:
        user_id (str): Unique identifier for the user.

    Returns:
        Dict[str, Any]: Personalized recommendations.
    """
    try:
        # Fetch user preferences
        preferences = await get_user_preferences(user_id)
        if preferences["status"] != "success":
            return {"status": "error", "message": "Failed to fetch preferences"}

        # Call Gemini API to get personalized recommendations
        payload = {
            "query": f"Provide personalized recommendations for a user with preferences: {preferences['preferences']}"
        }
        response = await call_gemini_api("/query", payload)
        if response and "response" in response:
            recommendations = response["response"]
        else:
            recommendations = "No recommendations available."

        return {
            "status": "success",
            "recommendations": recommendations,
        }

    except Exception as e:
        logger.error(f"Error getting personalized recommendations: {e}")
        return {"status": "error", "message": "Failed to get recommendations"}
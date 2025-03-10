# backend/app/utils/gemini_integration.py

import os
import httpx
from typing import Dict, Any, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Load Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://api.gemini.com/v1")

async def call_gemini_api(endpoint: str, payload: Dict[str, Any], method: str = "POST") -> Optional[Dict[str, Any]]:
    """
    Call the Gemini API with the specified endpoint and payload.

    Args:
        endpoint (str): API endpoint to call (e.g., "/chat").
        payload (Dict[str, Any]): Payload to send with the request.
        method (str): HTTP method to use ("POST" or "GET"). Defaults to "POST".

    Returns:
        Optional[Dict[str, Any]]: JSON response from the API, or None if the request fails.
    """
    if not GEMINI_API_KEY:
        logger.error("Gemini API key is not set in environment variables")
        return None

    url = f"{GEMINI_API_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "POST":
                response = await client.post(url, json=payload, headers=headers)
            elif method.upper() == "GET":
                response = await client.get(url, params=payload, headers=headers)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None

            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Successfully called Gemini API: {url}")
            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error calling Gemini API: {e}")
    except httpx.RequestError as e:
        logger.error(f"Request error calling Gemini API: {e}")
    except Exception as e:
        logger.error(f"Unexpected error calling Gemini API: {e}")

    return None
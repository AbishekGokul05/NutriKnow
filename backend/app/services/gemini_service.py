# backend/app/services/gemini_service.py
import google.generativeai as genai
from app.config import get_settings
from typing import Dict, List, Optional
import json
from loguru import logger

# Get settings
settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_text(prompt: str) -> str:
    """
    Generates text using the Gemini API.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating text with Gemini API: {str(e)}")
        return f"Error generating response: {str(e)}"

def parse_json_response(response: str) -> Dict:
    """
    Safely parses JSON response from Gemini API.
    """
    try:
        # Try to find JSON content between triple backticks if present
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            if end != -1:
                response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            if end != -1:
                response = response[start:end].strip()
        
        # Remove any leading/trailing whitespace and newlines
        response = response.strip()
        
        # Parse the JSON
        return json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {str(e)}")
        return {"error": "Failed to parse response", "raw_response": response}

def analyze_ingredients(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Analyzes ingredients and provides insights.
    """
    prompt = f"""
    Analyze these ingredients and respond with a valid JSON object:
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Provide a JSON response in this exact format:
    {{
        "ingredients": [
            {{
                "ingredient": "name of ingredient",
                "description": "brief description",
                "purpose": "purpose in product"
            }}
        ]
    }}
    """
    response = generate_text(prompt)
    return parse_json_response(response)

def compare_products(ocr_text_1: str, ocr_text_2: str, username: Optional[str] = None) -> Dict[str, str]:
    """
    Compares two products and provides insights.
    """
    prompt = f"""
    Here are the ingredients of two products:
    Product 1: {ocr_text_1}
    Product 2: {ocr_text_2}
    User preferences: {username if username else "Not provided"}

    Compare the two products and provide the following:
    1. Which product is better and why?
    2. List the drawbacks of Product 1.
    3. List the drawbacks of Product 2.
    4. Provide detailed insights about the comparison.
    Format the response as a JSON object with keys: better_product, drawbacks_1, drawbacks_2, insights.
    """
    response = generate_text(prompt)
    return response

def detect_allergens(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Detects allergens in the ingredients.
    """
    prompt = f"""
    Analyze these ingredients for allergens and respond with a valid JSON object:
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Provide a JSON response in this exact format:
    {{
        "allergens": [
            {{
                "ingredient": "name of allergen",
                "warning": "polite warning about the allergen"
            }}
        ]
    }}
    """
    response = generate_text(prompt)
    return parse_json_response(response)

def detect_harmful_substances(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Detects harmful substances in the ingredients.
    """
    prompt = f"""
    Analyze these ingredients for harmful substances and respond with a valid JSON object:
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Provide a JSON response in this exact format:
    {{
        "harmful_substances": [
            {{
                "ingredient": "name of substance",
                "reason": "why it is harmful",
                "level": "safe or above safe limit"
            }}
        ]
    }}
    """
    response = generate_text(prompt)
    return parse_json_response(response)

def analyze_nutritional_benefits(ocr_text: str, username: Optional[str] = None) -> Dict[str, str]:
    """
    Analyzes nutritional benefits or usage benefits.
    """
    prompt = f"""
    Analyze these ingredients for benefits and respond with a valid JSON object:
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Provide a JSON response in this exact format:
    {{
        "product_type": "food or non-food",
        "benefits": ["benefit 1", "benefit 2", "benefit 3"]
    }}
    """
    response = generate_text(prompt)
    return parse_json_response(response)

def suggest_alternatives(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Suggests harm-free alternatives or similar products.
    """
    prompt = f"""
    Analyze these ingredients and suggest alternatives in a valid JSON object:
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Provide a JSON response in this exact format:
    {{
        "has_harmful_substances": true or false,
        "alternatives": ["alternative 1", "alternative 2", "alternative 3"]
    }}
    """
    response = generate_text(prompt)
    return parse_json_response(response)
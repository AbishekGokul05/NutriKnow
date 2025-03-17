# backend/app/services/gemini_service.py
import google.generativeai as genai
import os
from typing import Dict, List, Optional

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_text(prompt: str) -> str:
    """
    Generates text using the Gemini API.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def analyze_ingredients(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Analyzes ingredients and provides insights.
    """
    prompt = f"""
    Here is a list of ingredients extracted from a product: {ocr_text}
    User preferences: {username if username else "Not provided"}

    For each ingredient, provide:
    1. The common name of the ingredient.
    2. A brief description of the ingredient.
    3. The purpose of the ingredient in the product.
    Format the response as a JSON list with keys: ingredient, description, purpose.
    """
    response = generate_text(prompt)
    return response

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
    Here is a list of ingredients extracted from a product: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Identify any ingredients that may cause allergies in people.
    For each allergen, provide:
    1. The name of the ingredient.
    2. A polite warning about the allergen.
    Format the response as a JSON list with keys: ingredient, warning.
    """
    response = generate_text(prompt)
    return response

def detect_harmful_substances(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Detects harmful substances in the ingredients.
    """
    prompt = f"""
    Here is a list of ingredients extracted from a product: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Identify any ingredients that are potentially harmful to humans.
    Ignore ingredients that are present in limited amounts and are not harmful.
    For each harmful ingredient, provide:
    1. The name of the ingredient.
    2. The reason why it is harmful.
    3. The level of the ingredient (e.g., "safe", "above safe limit").
    Format the response as a JSON list with keys: ingredient, reason, level.
    """
    response = generate_text(prompt)
    return response

def analyze_nutritional_benefits(ocr_text: str, username: Optional[str] = None) -> Dict[str, str]:
    """
    Analyzes nutritional benefits or usage benefits.
    """
    prompt = f"""
    Here is a list of ingredients extracted from a product: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Analyze the ingredients and determine if the product is a food item or non-food item.
    If it is a food item, provide a list of nutritional benefits.
    If it is a non-food item, provide a list of usage benefits.
    Format the response as a JSON object with keys: product_type, benefits.
    """
    response = generate_text(prompt)
    return response

def suggest_alternatives(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Suggests harm-free alternatives or similar products.
    """
    prompt = f"""
    Here is a list of ingredients extracted from a product: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Analyze the ingredients and determine if any harmful substances are present.
    If harmful substances are present, suggest harm-free alternatives (e.g., "Use paraben-free products").
    If no harmful substances are found, recommend similar products in a generic way (e.g., "Look for sulfate-free shampoos").
    Do not promote any specific product or brand.
    Format the response as a JSON object with keys: has_harmful_substances, alternatives.
    """
    response = generate_text(prompt)
    return response
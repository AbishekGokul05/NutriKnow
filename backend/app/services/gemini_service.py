# backend/app/services/gemini_service.py
import google.generativeai as genai
from app.config import get_settings
from typing import Dict, List, Optional
import json
from loguru import logger
import os

# Get settings
settings = get_settings()

# Define the model name to use throughout the service
MODEL_NAME = 'gemini-2.0-flash'  # Using a widely available model

# Hardcoded API key for testing
HARDCODED_API_KEY = "AIzaSyAB5jKOflFnIQ5-4bPoYKbeDIr9DZ-f3Lc"  # Your API key from .env

# Configure Gemini
try:
    # Use hardcoded API key
    api_key = HARDCODED_API_KEY
    
    if not api_key:
        logger.error("API key is missing.")
    else:
        # Configure the genai library with the API key
        genai.configure(api_key=api_key)
        logger.info(f"API key configured successfully. Using model: {MODEL_NAME}")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")

def generate_text(prompt: str) -> str:
    """
    Generates text using the Gemini API.
    """
    try:
        # Create model instance
        model = genai.GenerativeModel(
            model_name=MODEL_NAME
        )
        
        # Generate content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating text with Gemini API: {str(e)}")
        
        # For authentication errors
        if "credentials" in str(e).lower() or "authentication" in str(e).lower() or "api key" in str(e).lower():
            return f"""
Error: Authentication failed. 

To fix this issue:
1. Get a valid API key from https://makersuite.google.com/app/apikey
2. You might need to enable the Gemini API for your Google Cloud project
3. Ensure the key has permission to access the Gemini API
"""
        # For model not found errors
        elif "not found" in str(e).lower():
            return f"Error: Model '{MODEL_NAME}' not found. Try using 'gemini-pro' instead."
        else:
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
    You are a professional nutritionist and ingredient analyst. Carefully analyze these ingredients and provide accurate, factual information:
    
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Rules:
    1. Only analyze ingredients that are actually present in the text
    2. Provide factual, scientific descriptions
    3. Do not make assumptions about ingredients not listed
    4. If an ingredient's purpose is unclear, state that explicitly
    5. Base all analysis on verified nutritional and scientific data

    Provide a JSON response in this exact format:
    {{
        "ingredients": [
            {{
                "ingredient": "name of ingredient",
                "description": "scientific description of the ingredient",
                "purpose": "verified purpose in product",
                "category": "preservative/nutrient/flavor/color/etc"
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
    You are a professional allergen specialist. Analyze these ingredients specifically for common allergens and provide accurate warnings:
    
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Rules:
    1. Only identify allergens that are actually present in the ingredients
    2. Include both direct allergens and derived ingredients
    3. Cross-contamination warnings should only be included if explicitly stated in the text
    4. Focus on the major allergen categories: milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, and soybeans
    5. Include any other scientifically verified allergens found

    Provide a JSON response in this exact format:
    {{
        "allergens": [
            {{
                "ingredient": "name of allergen",
                "category": "major allergen category",
                "warning": "specific warning about this allergen",
                "severity": "high/medium/low"
            }}
        ],
        "cross_contamination_risks": ["risk 1", "risk 2"],
        "safe_for_allergies": ["allergy 1", "allergy 2"]
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
    Analyzes nutritional benefits based on ingredients.
    """
    prompt = f"""
    You are a professional nutritionist. Analyze these ingredients for specific nutritional benefits:
    
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Rules:
    1. Only analyze ingredients that are actually present
    2. Provide specific, scientifically-verified nutritional benefits
    3. Include potential nutritional concerns
    4. Quantify benefits where possible
    5. Consider standard serving sizes
    6. Do not make assumptions about processing methods unless specified

    Provide a JSON response in this exact format:
    {{
        "product_type": "food or non-food",
        "nutritional_content": {{
            "proteins": "amount and quality",
            "carbohydrates": "amount and type",
            "fats": "amount and type",
            "vitamins": ["vitamin 1", "vitamin 2"],
            "minerals": ["mineral 1", "mineral 2"]
        }},
        "health_benefits": [
            {{
                "benefit": "specific health benefit",
                "source_ingredient": "ingredient providing this benefit",
                "scientific_basis": "brief explanation of the mechanism"
            }}
        ],
        "dietary_considerations": {{
            "vegan": true/false,
            "vegetarian": true/false,
            "gluten_free": true/false,
            "keto_friendly": true/false
        }}
    }}
    """
    response = generate_text(prompt)
    return parse_json_response(response)

def suggest_alternatives(ocr_text: str, username: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Suggests alternatives based on ingredient analysis.
    """
    prompt = f"""
    You are a product formulation expert. Analyze these ingredients and suggest specific, relevant alternatives:
    
    Product ingredients: {ocr_text}
    User preferences: {username if username else "Not provided"}

    Rules:
    1. Only suggest alternatives based on actual ingredients present
    2. Consider the product type and purpose
    3. Provide healthier or allergen-free alternatives where applicable
    4. Explain why each alternative is suggested
    5. Consider user preferences if provided
    6. Focus on scientific and nutritional equivalence

    Provide a JSON response in this exact format:
    {{
        "product_category": "category of the product",
        "alternatives": [
            {{
                "name": "alternative product or ingredient",
                "reason": "specific reason for suggesting this alternative",
                "benefits": ["benefit 1", "benefit 2"],
                "suitable_for": ["dietary preference 1", "dietary preference 2"]
            }}
        ],
        "substitution_notes": [
            {{
                "ingredient": "original ingredient",
                "substitutes": ["substitute 1", "substitute 2"],
                "notes": "important considerations for substitution"
            }}
        ]
    }}
    """
    response = generate_text(prompt)
    return parse_json_response(response)

def generate_health_fact(previous_facts: List[str] = None) -> str:
    """Generate a random health fact using Gemini."""
    try:
        # Create a prompt that includes previous facts to avoid repetition
        previous_facts_str = "\n".join(previous_facts) if previous_facts else "No previous facts."
        prompt = f"""Generate a unique, interesting, and scientifically accurate health fact. 
        The fact should be concise (1-2 sentences) and engaging.
        Make sure it's different from these previous facts:
        {previous_facts_str}
        
        Format the response as just the fact, without any additional text or formatting."""

        # Generate the response using the same model configuration as other functions
        response = generate_text(prompt)
        
        if response and response.strip():
            return response.strip()
        else:
            return "Regular exercise can improve both physical and mental health."
            
    except Exception as e:
        logger.error(f"Error generating health fact: {str(e)}")
        return "Regular exercise can improve both physical and mental health."
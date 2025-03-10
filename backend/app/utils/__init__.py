# backend/app/utils/__init__.py

# Expose key utility functions/modules for easier imports
from .image_processing import preprocess_image
from .data_validation import validate_input, validate_payload
from .api_response_formatter import format_success_response, format_error_response
from .gemini_integration import call_gemini_api
from .ocr_service import extract_text_from_image
from .nutritional_analysis import analyze_nutritional_data
from .allergen_detection import detect_allergens
from .harmful_substance_detection import detect_harmful_substances
from .product_comparison import compare_products
from .user_profile_utils import update_user_preferences, get_user_preferences
from .history_utils import add_to_history, get_user_history
from .logging_utils import setup_logger
from .error_handlers import handle_exception
from .config_loader import load_config
from .file_utils import save_uploaded_file, validate_file

# Optional: Define __all__ to control what gets imported with `from utils import *`
__all__ = [
    "preprocess_image",
    "validate_input",
    "validate_payload",
    "format_success_response",
    "format_error_response",
    "call_gemini_api",
    "extract_text_from_image",
    "analyze_nutritional_data",
    "detect_allergens",
    "detect_harmful_substances",
    "compare_products",
    "update_user_preferences",
    "get_user_preferences",
    "add_to_history",
    "get_user_history",
    "setup_logger",
    "handle_exception",
    "load_config",
    "save_uploaded_file",
    "validate_file",
]
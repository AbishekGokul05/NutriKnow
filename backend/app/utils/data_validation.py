# backend/app/utils/data_validation.py

import re
from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Define a Pydantic model for validating user profile data
class UserProfile(BaseModel):
    user_id: str
    dietary_restrictions: Optional[list] = []
    allergens: Optional[list] = []

def validate_input(data: Dict[str, Any], required_fields: list) -> bool:
    """
    Validate that the input data contains all required fields.

    Args:
        data (Dict[str, Any]): Input data to validate.
        required_fields (list): List of required fields.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    try:
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False
        logger.info("Input data validation successful")
        return True
    except Exception as e:
        logger.error(f"Error validating input data: {e}")
        return False

def validate_payload(payload: Dict[str, Any], model: BaseModel) -> bool:
    """
    Validate the payload against a Pydantic model.

    Args:
        payload (Dict[str, Any]): Payload to validate.
        model (BaseModel): Pydantic model to validate against.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    try:
        model(**payload)
        logger.info("Payload validation successful")
        return True
    except ValidationError as e:
        logger.error(f"Payload validation failed: {e}")
        return False

def validate_email(email: str) -> bool:
    """
    Validate an email address using regex.

    Args:
        email (str): Email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(email_regex, email):
        logger.info("Email validation successful")
        return True
    logger.error(f"Invalid email: {email}")
    return False
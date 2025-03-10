# backend/app/utils/api_response_formatter.py

from typing import Dict, Any, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

def format_success_response(data: Optional[Dict[str, Any]] = None, message: Optional[str] = "Success") -> Dict[str, Any]:
    """
    Format a successful API response.

    Args:
        data (Optional[Dict[str, Any]]): Data to include in the response. Defaults to None.
        message (Optional[str]): Success message. Defaults to "Success".

    Returns:
        Dict[str, Any]: Formatted success response.
    """
    response = {
        "status": "success",
        "message": message,
        "data": data if data is not None else {},
    }
    logger.info(f"Formatted success response: {response}")
    return response

def format_error_response(message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Format an error API response.

    Args:
        message (str): Error message.
        error_code (Optional[str]): Custom error code. Defaults to None.
        details (Optional[Dict[str, Any]]): Additional error details. Defaults to None.

    Returns:
        Dict[str, Any]: Formatted error response.
    """
    response = {
        "status": "error",
        "message": message,
        "error_code": error_code if error_code is not None else "GENERIC_ERROR",
        "details": details if details is not None else {},
    }
    logger.error(f"Formatted error response: {response}")
    return response
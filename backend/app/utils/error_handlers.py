# backend/app/utils/error_handlers.py

import logging
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

# Set up logging
logger = logging.getLogger(__name__)

class CustomError(Exception):
    """
    Custom error class for application-specific errors.
    """
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details

async def custom_error_handler(request: Request, exc: CustomError) -> JSONResponse:
    """
    Handle CustomError exceptions and return a JSON response.

    Args:
        request (Request): The incoming request.
        exc (CustomError): The exception instance.

    Returns:
        JSONResponse: A JSON response with the error details.
    """
    logger.error(f"CustomError: {exc.message}", exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "details": exc.details,
        },
    )

async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTPException and return a JSON response.

    Args:
        request (Request): The incoming request.
        exc (HTTPException): The exception instance.

    Returns:
        JSONResponse: A JSON response with the error details.
    """
    logger.error(f"HTTPException: {exc.detail}", exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
        },
    )

async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all other exceptions and return a JSON response.

    Args:
        request (Request): The incoming request.
        exc (Exception): The exception instance.

    Returns:
        JSONResponse: A JSON response with the error details.
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An unexpected error occurred.",
            "details": str(exc),
        },
    )
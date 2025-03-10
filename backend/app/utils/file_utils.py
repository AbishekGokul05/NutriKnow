# backend/app/utils/file_utils.py

import os
import logging
from typing import Optional, Tuple
from fastapi import UploadFile
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

# File storage settings
UPLOAD_DIR = "uploads"
ALLOWED_FILE_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def validate_file(file: UploadFile) -> Tuple[bool, Optional[str]]:
    """
    Validate an uploaded file based on its type and size.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing a boolean indicating success and an optional error message.
    """
    try:
        # Check file type
        if file.content_type not in ALLOWED_FILE_TYPES:
            return False, f"File type {file.content_type} is not allowed."

        # Check file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        if file_size > MAX_FILE_SIZE:
            return False, f"File size {file_size} exceeds the maximum allowed size of {MAX_FILE_SIZE} bytes."

        return True, None

    except Exception as e:
        logger.error(f"Error validating file: {e}")
        return False, "An error occurred while validating the file."

def save_uploaded_file(file: UploadFile, subdir: Optional[str] = None) -> Optional[str]:
    """
    Save an uploaded file to the upload directory.

    Args:
        file (UploadFile): The uploaded file.
        subdir (Optional[str]): Subdirectory within the upload directory to save the file. Defaults to None.

    Returns:
        Optional[str]: The path to the saved file, or None if the file could not be saved.
    """
    try:
        # Validate the file
        is_valid, error_message = validate_file(file)
        if not is_valid:
            logger.error(f"File validation failed: {error_message}")
            return None

        # Create subdirectory if specified
        save_dir = Path(UPLOAD_DIR)
        if subdir:
            save_dir = save_dir / subdir
            os.makedirs(save_dir, exist_ok=True)

        # Save the file
        file_path = save_dir / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        logger.info(f"File saved successfully: {file_path}")
        return str(file_path)

    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return None

def delete_file(file_path: str) -> bool:
    """
    Delete a file from the upload directory.

    Args:
        file_path (str): The path to the file to delete.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted successfully: {file_path}")
            return True
        else:
            logger.warning(f"File not found: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return False
# backend/app/utils/ocr_service.py

import easyocr
import logging
from typing import List, Optional

# Set up logging
logger = logging.getLogger(__name__)

# Initialize EasyOCR reader (load only English by default)
reader = easyocr.Reader(["en"])

def extract_text_from_image(image_path: str, languages: List[str] = ["en"]) -> Optional[str]:
    """
    Extract text from an image using EasyOCR.

    Args:
        image_path (str): Path to the image file.
        languages (List[str]): List of languages to use for OCR. Defaults to ["en"].

    Returns:
        Optional[str]: Extracted text as a single string, or None if OCR fails.
    """
    try:
        # Initialize the reader with the specified languages
        global reader
        if reader.lang_list != languages:
            reader = easyocr.Reader(languages)
            logger.info(f"Initialized EasyOCR reader for languages: {languages}")

        # Perform OCR on the image
        results = reader.readtext(image_path)
        logger.info(f"Successfully extracted text from image: {image_path}")

        # Combine all detected text into a single string
        extracted_text = " ".join([result[1] for result in results])
        logger.info("Text extraction successful")

        return extracted_text.strip()  # Remove leading/trailing whitespace

    except Exception as e:
        logger.error(f"Error extracting text from image: {e}")
        return None
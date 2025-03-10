# backend/app/services/ocr_service.py
import easyocr
import numpy as np
import cv2

# Initialize the OCR reader
reader = easyocr.Reader(['en'])  # Supports English language

def extract_text_from_image(image: bytes) -> str:
    """
    Extracts text from an image using EasyOCR.
    
    Args:
        image (bytes): The image file in bytes format.
        
    Returns:
        str: The extracted text as a single string.
    """
    try:
        # Convert image bytes to a numpy array
        image_np = np.frombuffer(image, np.uint8)
        image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Perform OCR
        results = reader.readtext(image_np)

        # Combine all detected text into a single string
        extracted_text = " ".join([result[1] for result in results])
        return extracted_text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from image: {str(e)}")
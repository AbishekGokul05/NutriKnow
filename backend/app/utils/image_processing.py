# backend/app/utils/image_processing.py

from PIL import Image
import numpy as np
import logging

# Set up logging
logger = logging.getLogger(__name__)

def preprocess_image(image_path: str, target_size: tuple = (800, 800)) -> np.ndarray:
    """
    Preprocess an image for OCR by resizing and converting it to grayscale.

    Args:
        image_path (str): Path to the image file.
        target_size (tuple): Desired size of the image (width, height). Default is (800, 800).

    Returns:
        np.ndarray: Preprocessed image as a NumPy array.
    """
    try:
        # Open the image
        image = Image.open(image_path)
        logger.info(f"Successfully opened image: {image_path}")

        # Resize the image
        image = image.resize(target_size, Image.ANTIALIAS)
        logger.info(f"Resized image to: {target_size}")

        # Convert to grayscale
        image = image.convert("L")
        logger.info("Converted image to grayscale")

        # Convert to NumPy array
        image_array = np.array(image)
        logger.info("Converted image to NumPy array")

        return image_array

    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise
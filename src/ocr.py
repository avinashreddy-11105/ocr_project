"""Tesseract OCR wrapper."""
import pytesseract
from PIL import Image
import numpy as np


def run_ocr(image, config: str = "") -> str:
    """Run Tesseract on an image (PIL Image, file path, or numpy array)."""
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    elif isinstance(image, str):
        image = Image.open(image)
    return pytesseract.image_to_string(image, config=config)
"""Image preprocessing for OCR on scanned financial documents."""
import cv2
import numpy as np


def to_grayscale_binary(image_path: str) -> np.ndarray:
    """Load an image and convert to binary using Otsu's threshold."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def remove_horizontal_lines(binary_img: np.ndarray, min_line_width: int = 40) -> np.ndarray:
    """Remove horizontal lines (e.g., underlines under totals) that confuse Tesseract.

    Financial documents use horizontal rules to separate sections and underline
    totals. These lines often touch the digits above them, causing OCR errors.
    """
    inverted = cv2.bitwise_not(binary_img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (min_line_width, 1))
    detected_lines = cv2.morphologyEx(inverted, cv2.MORPH_OPEN, kernel, iterations=2)
    cleaned = cv2.bitwise_or(binary_img, detected_lines)
    return cleaned


def preprocess(image_path: str, remove_lines: bool = True) -> np.ndarray:
    """Full preprocessing pipeline: grayscale → binary → line removal."""
    binary = to_grayscale_binary(image_path)
    if remove_lines:
        binary = remove_horizontal_lines(binary)
    return binary
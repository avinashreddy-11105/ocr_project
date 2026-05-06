"""Extract structured numeric data from OCR text."""
import re


def extract_dollar_amounts(text: str) -> list[str]:
    """Find numbers that look like dollar amounts.

    Matches:
    - Numbers with thousands separators (e.g., 21,909,567)
    - Bare integers of 4+ digits (e.g., 21909567)
    Returns numbers normalized (commas stripped).
    """
    pattern = r'\b\d{1,3}(?:,\d{3})+\b|\b\d{4,}\b'
    return [re.sub(r'[,\s]', '', n) for n in re.findall(pattern, text)]


def filter_likely_years(numbers: list[str], min_value: int = 100000) -> list[str]:
    """Remove 4-digit values that look like years (e.g., 1974, 1975)
    rather than dollar amounts."""
    return [n for n in numbers if int(n) >= min_value]
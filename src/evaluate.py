"""Evaluate OCR output against ground truth."""
from .extract import extract_dollar_amounts, filter_likely_years


def compute_f1(ground_truth: set[str], predicted: set[str]) -> dict:
    """Compute precision, recall, and F1 for a set of predicted numbers."""
    matched = ground_truth & predicted
    precision = len(matched) / len(predicted) * 100 if predicted else 0
    recall = len(matched) / len(ground_truth) * 100 if ground_truth else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "matched": len(matched),
        "total_truth": len(ground_truth),
        "total_predicted": len(predicted),
        "missed": ground_truth - predicted,
        "extras": predicted - ground_truth,
    }


def evaluate_ocr_output(ocr_text: str, ground_truth_path: str) -> dict:
    """Run end-to-end evaluation against a ground truth file."""
    with open(ground_truth_path) as f:
        truth = set(line.strip() for line in f if line.strip())

    predicted_raw = extract_dollar_amounts(ocr_text)
    predicted = set(filter_likely_years(predicted_raw))

    return compute_f1(truth, predicted)
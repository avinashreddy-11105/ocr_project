"""End-to-end pipeline: PDF → preprocessing → OCR → evaluation."""
import argparse
from pathlib import Path
from pdf2image import convert_from_path

from .preprocess import preprocess
from .ocr import run_ocr
from .evaluate import evaluate_ocr_output


def process_page(pdf_path: str, page_num: int, output_dir: Path) -> str:
    """Convert a single PDF page to image, preprocess, and OCR."""
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=300, first_page=page_num, last_page=page_num)
    image_path = output_dir / f"page{page_num}_raw.png"
    pages[0].save(image_path)

    processed = preprocess(str(image_path))
    ocr_text = run_ocr(processed)

    text_path = output_dir / f"page{page_num}_ocr.txt"
    text_path.write_text(ocr_text)

    return ocr_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to PDF")
    parser.add_argument("--page", type=int, default=15, help="Page to process")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--ground-truth", help="Optional ground truth file for F1 eval")
    args = parser.parse_args()

    print(f"Processing {args.input} page {args.page}...")
    ocr_text = process_page(args.input, args.page, Path(args.output))
    print(f"Extracted {len(ocr_text)} characters.")

    if args.ground_truth:
        results = evaluate_ocr_output(ocr_text, args.ground_truth)
        print(f"\nF1 score: {results['f1']:.1f}%")
        print(f"Precision: {results['precision']:.1f}%")
        print(f"Recall: {results['recall']:.1f}%")


if __name__ == "__main__":
    main()
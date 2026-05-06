# Financial Statement OCR Pipeline

OCR pipeline for extracting structured financial data from scanned historical
annual reports, with validation via accounting identities.

## Status

Early-stage project. Baseline established on a single document (Coca-Cola
1975 balance sheet); preprocessing improvements and multi-document evaluation
in progress.

## Motivation

Historical corporate financial data is locked in scanned PDFs across archives
like Internet Archive, Mergent, and pre-1996 SEC filings. Commercial
extraction (AlphaSense, Daloopa) costs tens of thousands per year for what
is fundamentally OCR + schema reconciliation. This project demonstrates a
reproducible open-source pipeline for the same task.

## Current results

Tested on Coca-Cola Company 1975 annual report, page 15 (Consolidated
Balance Sheet — Liabilities), sourced from the Internet Archive scanned
collection.

| Stage                  | Precision | Recall | F1    |
|------------------------|-----------|--------|-------|
| Tesseract baseline     | 93.9%     | 93.9%  | 93.9% |

Failure modes identified:
- Double-underlined grand totals (accounting convention) are missed by
  default Tesseract — addressed via OpenCV horizontal-line removal in
  `src/preprocess.py`
- 4-digit year column headers are extracted as dollar amounts — filtered
  in `src/extract.py`

## Architecture

    PDF
     ├─ rasterization (pdf2image, 300 DPI)
     ├─ preprocessing (OpenCV: binarization, line removal)
     ├─ OCR (Tesseract via pytesseract)
     ├─ number extraction (regex + filtering)
     └─ validation (accounting identity checks)

## Tech stack

Python 3.11, Tesseract OCR, OpenCV, pdf2image, pdfplumber, pandas, pytest.

## Repo structure

    .
    ├── src/
    │   ├── preprocess.py    # OpenCV preprocessing
    │   ├── ocr.py           # Tesseract wrapper
    │   ├── extract.py       # Number extraction
    │   ├── validate.py      # Accounting identity checks
    │   ├── evaluate.py      # F1 evaluation against ground truth
    │   └── pipeline.py      # End-to-end orchestration
    ├── tests/
    │   └── test_validate.py
    ├── notebooks/
    │   └── 01_baseline_evaluation.ipynb
    ├── data/                # PDFs (gitignored — see data/README.md)
    ├── output/              # Generated images, OCR text, ground truth
    ├── requirements.txt
    └── README.md

## How to run

    # 1. Install Tesseract (system-level)
    sudo apt install tesseract-ocr poppler-utils    # Linux/Colab
    # brew install tesseract poppler                # Mac

    # 2. Install Python deps
    pip install -r requirements.txt

    # 3. Get a sample PDF
    mkdir -p data
    wget --user-agent="Mozilla/5.0" \
      -O data/cocacola_1975.pdf \
      "https://archive.org/download/cocacolacoannualreports/cocacola1975.pdf"

    # 4. Run pipeline
    python -m src.pipeline \
      --input data/cocacola_1975.pdf \
      --page 15 \
      --output output/ \
      --ground-truth output/page15_ground_truth.txt

## Tests

    pytest tests/

## Roadmap

- [x] Baseline Tesseract evaluation (93.9% F1)
- [x] Accounting-identity validation
- [ ] Horizontal-line removal preprocessing — measure F1 delta
- [ ] Process additional Coca-Cola reports (1980, 1985) for cross-document
      consistency
- [ ] Compare against EasyOCR and PaddleOCR backends
- [ ] Layout-aware extraction (associate numbers with line-item labels)

## Limitations

- Tested on one document; generalization unverified
- English-language reports only
- No handling of multi-column layouts beyond two-year comparatives
- Library stamps and handwritten annotations not addressed
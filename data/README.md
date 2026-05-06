# Data sources

PDFs are not committed to this repo (too large, copyright varies).

## Sources used

- **Coca-Cola annual reports (1920–2017)**: 
  https://archive.org/details/cocacolacoannualreports

## To reproduce

Download the relevant PDFs into this folder. The pipeline expects:

    data/cocacola_1975.pdf

Download command (Colab/Linux):

    wget --user-agent="Mozilla/5.0" \
      -O data/cocacola_1975.pdf \
      "https://archive.org/download/cocacolacoannualreports/cocacola1975.pdf"
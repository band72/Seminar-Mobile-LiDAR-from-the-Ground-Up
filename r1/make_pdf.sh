#!/usr/bin/env bash
# Build the compressed R1 course text: generate, verify, compile, compress.
# Output: docs/LiDAR_from_the_Ground_Up_R1.pdf
# Requires: python3, latexmk + TeX Live, ghostscript (gs).
set -euo pipefail
cd "$(dirname "$0")"

python3 build_r1.py
python3 check_boxes.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main_r1.tex

# Downsample figures to 120 dpi JPEG (q80). Text stays vector and searchable.
# On R0 this gives 11 MB -> 2.8 MB, versus 6.1 MB for the stock /ebook preset.
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.6 -dPDFSETTINGS=/ebook \
   -dDownsampleColorImages=true -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=120 -dGrayImageResolution=120 \
   -dAutoFilterColorImages=false -dColorImageFilter=/DCTEncode -dJPEGQ=80 \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=../docs/LiDAR_from_the_Ground_Up_R1.pdf main_r1.pdf

ls -lh main_r1.pdf ../docs/LiDAR_from_the_Ground_Up_R1.pdf

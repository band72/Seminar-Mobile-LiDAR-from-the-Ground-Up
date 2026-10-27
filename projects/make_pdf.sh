#!/usr/bin/env bash
# Build the compressed Projects download (Capstone + Hands-On Labs from R0).
# Output: docs/LiDAR_Projects_R0.pdf
# Requires: python3, latexmk + TeX Live, ghostscript (gs).
set -euo pipefail
cd "$(dirname "$0")"

python3 build_projects.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main_projects.tex

# Same compression as the R1 build: figures at 120 dpi JPEG, text stays vector.
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.6 -dPDFSETTINGS=/ebook \
   -dDownsampleColorImages=true -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=120 -dGrayImageResolution=120 \
   -dAutoFilterColorImages=false -dColorImageFilter=/DCTEncode -dJPEGQ=80 \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=../docs/LiDAR_Projects_R0.pdf main_projects.pdf

ls -lh main_projects.pdf ../docs/LiDAR_Projects_R0.pdf

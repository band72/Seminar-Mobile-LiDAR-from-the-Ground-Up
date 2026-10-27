"""Build one PDF per module from the R0 sources (the Reference Book).

R0 files are only read, never written. Each module PDF holds one R0 chapter,
unchanged, with its R0 module number. References to other modules resolve to
the Reference Book's section and page numbers, taken from a full R0 build.

Writes modules/build/Module_NN.tex and the compressed PDFs to
docs/modules/Module_NN_R0.pdf.
Requires: python3, latexmk + TeX Live, ghostscript (gs).
Usage: python3 modules/build_modules.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
R0 = HERE.parent
BUILD = HERE / "build"
OUT = R0 / "docs" / "modules"

# In R0 order: Module 1 = ch01_intro ... Module 21 = ch15_capstone.
CHAPTERS = [
    "ch01_intro", "ch02_math", "ch03_tof", "ch04_beam", "ch05_polar",
    "ch06_rotation", "ch07_imu", "ch08_timing", "ch09_calib", "ch10_slam",
    "ch11_scanmatch", "ch12_factor", "ch13_accuracy", "ch13b_errprop",
    "ch13c_os0", "ch13d_gx5", "ch13e_riegl", "ch14_processing",
    "ch14b_florida", "ch14c_practice", "ch15_capstone",
]

# Same compression as the R1 and Projects builds: figures at 120 dpi JPEG, text stays vector.
GS = ["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.6", "-dPDFSETTINGS=/ebook",
      "-dDownsampleColorImages=true", "-dColorImageDownsampleType=/Bicubic",
      "-dColorImageResolution=120", "-dGrayImageResolution=120",
      "-dAutoFilterColorImages=false", "-dColorImageFilter=/DCTEncode", "-dJPEGQ=80",
      "-dNOPAUSE", "-dQUIET", "-dBATCH"]


def latexmk(tex, outdir):
    subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                    f"-outdir={outdir}", tex.name], cwd=tex.parent, check=True,
                   stdout=subprocess.DEVNULL)


def r0_labels():
    """Build the full Reference Book and return its \\newlabel lines by label name."""
    latexmk(R0 / "main.tex", BUILD / "r0")
    aux = (BUILD / "r0" / "main.aux").read_text()
    return {m.group(1): m.group(0) for m in re.finditer(r"\\newlabel\{([^}]*)\}.*", aux)}


def preamble():
    src = (R0 / "main.tex").read_text()
    pre = src[:src.index("\\begin{document}")]
    pre = pre.replace("\\graphicspath{{figs/}}", "\\graphicspath{{../../figs/}}")
    # Try It answers are in the Reference Book, not in the module PDF.
    pre = pre.replace("``Answers to Try It Yourself,'' starting on page",
                      "``Answers to Try It Yourself,'' of the Reference Book, starting on page")
    return pre


def module_tex(num, name, labels, pre):
    own = set(re.findall(r"\\label\{([^}]*)\}", (R0 / f"{name}.tex").read_text()))
    external = "\n".join(line for label, line in labels.items() if label not in own)
    title = f"LiDAR from the Ground Up: Module {num}"
    return (pre.replace("pdftitle={LiDAR from the Ground Up}", f"pdftitle={{{title} (R0)}}")
            + "\\makeatletter\\AtBeginDocument{" + external + "}\\makeatother\n"
            + "\\begin{document}\n"
            + f"\\setcounter{{chapter}}{{{num - 1}}}\n\\input{{../../{name}}}\n"
            + "\\end{document}\n")


def main():
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    labels = r0_labels()
    pre = preamble()
    for num, name in enumerate(CHAPTERS, 1):
        tex = BUILD / f"Module_{num:02d}.tex"
        tex.write_text(module_tex(num, name, labels, pre))
        latexmk(tex, BUILD)
        pdf = OUT / f"Module_{num:02d}_R0.pdf"
        subprocess.run(GS + [f"-sOutputFile={pdf}", str(tex.with_suffix(".pdf"))], check=True)
        print(f"Module {num:2d}  {name:18s} -> {pdf.relative_to(R0)}  {pdf.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

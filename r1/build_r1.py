"""Generate the R1 "Surveying Concepts" edition from the R0 sources.

R0 files are only read, never written. For each module chapter this keeps,
in their original order:
  - the chapter, section and subsection headings (empty sections are dropped)
  - the SIMPLE APPROACH, BIG IDEA, SURVEYOR'S FIELD TIP and WARNING boxes,
    copied word for word
  - the figures (\\fig calls)
Everything else (engineering boxes, equations, worked examples, exercises,
tables, lists, prose and back matter) is left out.

Writes r1/ch*.tex, r1/ch00_front.tex and r1/main_r1.tex.
Usage: python3 r1/build_r1.py
"""
import re
from pathlib import Path

R1 = Path(__file__).resolve().parent
R0 = R1.parent

KEEP_BOXES = "kid|bigidea|tip|warning"
CHAPTERS = [
    "ch01_intro", "ch02_math", "ch03_tof", "ch04_beam", "ch05_polar",
    "ch06_rotation", "ch07_imu", "ch08_timing", "ch09_calib", "ch10_slam",
    "ch11_scanmatch", "ch12_factor", "ch13_accuracy", "ch13b_errprop",
    "ch13c_os0", "ch13d_gx5", "ch13e_riegl", "ch14_processing",
    "ch14b_florida", "ch14c_practice", "ch15_capstone",
]
LEVEL = {"chapter": 0, "section": 1, "subsection": 2}


def brace_end(text, i):
    """Index just past the {...} group starting at text[i] == '{'."""
    depth = 0
    while True:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        depth += {"{": 1, "}": -1}.get(c, 0)
        i += 1
        if depth == 0:
            return i


def items(text):
    """Yield (kind, source) for headings, kept boxes and figures, in order."""
    pattern = re.compile(
        r"\\(chapter|section|subsection)\*?(?=\{)"
        r"|\\begin\{(%s)\}" % KEEP_BOXES
        + r"|\\fig(?=[\[{])")
    pos = 0
    while (m := pattern.search(text, pos)):
        start = m.start()
        if m.group(1):
            end = brace_end(text, m.end())
            label = re.match(r"\s*\\label\{[^}]*\}", text[end:])
            if label:
                end += label.end()
            yield m.group(1), text[start:end]
        elif m.group(2):
            end = text.index("\\end{%s}" % m.group(2), m.end()) + len("\\end{%s}" % m.group(2))
            yield "box", text[start:end]
        else:
            end = m.end()
            if text[end] == "[":
                end = text.index("]", end) + 1
            end = brace_end(text, end)
            end = brace_end(text, end)
            yield "fig", text[start:end]
        pos = end


def condense(text):
    out = list(items(text))
    # Drop headings with no content before the next heading of the same or higher level.
    kept = []
    for i, (kind, src) in enumerate(out):
        if kind in LEVEL and kind != "chapter":
            has_content = False
            for kind2, _ in out[i + 1:]:
                if kind2 in LEVEL:
                    if LEVEL[kind2] <= LEVEL[kind]:
                        break
                    continue
                has_content = True
                break
            if not has_content:
                continue
        kept.append(src)
    return "\n\n".join(kept) + "\n"


FRONT = r"""\frontmatter
\begin{titlepage}
\begin{tikzpicture}[remember picture,overlay]
\fill[fill={rgb,255:red,26;green,50;blue,99}] (current page.south west) rectangle (current page.north east);
\node[anchor=center] at ([yshift=-0.9in]current page.center) {\includegraphics[width=\paperwidth]{cover}};
\fill[orange] ([yshift=-3.05in]current page.north west) rectangle ([yshift=-3.12in]current page.north east);
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-0.8in]current page.north west)
 {\color{white}\sffamily\bfseries\fontsize{40}{46}\selectfont\spaceskip=0.28em LiDAR from the Ground Up};
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-1.65in]current page.north west)
 {\color{orange!60}\sffamily\Large Surveying Concepts Edition};
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-2.05in]current page.north west)
 {\color{white}\sffamily\bfseries\LARGE D.S. Banks, PSM};
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-2.55in]current page.north west)
 {\color{white!85}\sffamily\large The core ideas of mobile LiDAR in plain language,\\ with field tips for surveyors.};
\node[anchor=south west,text width=7in,align=left] at ([xshift=0.75in,yshift=0.8in]current page.south west)
 {\color{white}\sffamily\large 21 modules \textbullet\ concepts, field tips and illustrations\\[6pt]
 \color{white!70}\sffamily\normalsize Course Text R1};
\end{tikzpicture}
\end{titlepage}

\chapter*{About This Edition}
\markboth{About This Edition}{}
This is the Surveying Concepts edition (R1) of \emph{LiDAR from the Ground Up}. It keeps the plain-language track of the full course: every green \textbf{Simple Approach} box, every \textbf{Big Idea}, every \textbf{Surveyor's Field Tip} and \textbf{Warning}, and the illustrations, in the same order and with the same module numbers as the full text.

The engineering track --- equations, worked examples, exercises, reference tables, labs, the sample SOP and the appendices --- is in the full course text (R0).

{\makeatletter\renewcommand*\l@chapter{\@dottedtocline{0}{0em}{1.8em}}\makeatother
\tableofcontents}
\clearpage\pagenumbering{arabic}\makeatletter\@mainmattertrue\@openrightfalse\makeatother
"""


def main_tex():
    src = (R0 / "main.tex").read_text()
    preamble = src[:src.index("\\begin{document}")]
    preamble = preamble.replace("\\graphicspath{{figs/}}", "\\graphicspath{{../figs/}}")
    preamble = preamble.replace("pdftitle={LiDAR from the Ground Up}",
                                "pdftitle={LiDAR from the Ground Up: Surveying Concepts Edition (R1)}")
    preamble = preamble.replace("LiDAR from the Ground Up}\n\\fancyhead[R]",
                                "LiDAR from the Ground Up: Surveying Concepts}\n\\fancyhead[R]")
    # With little text between figures, floats drift past their headings: pin them in place.
    preamble = preamble.replace("\\begin{figure}[htbp]", "\\begin{figure}[H]")
    preamble = preamble.replace("\\usepackage{caption}", "\\usepackage{float}\\usepackage{caption}")
    preamble += "\\setcounter{tocdepth}{0}\n"
    inputs = "".join("\\input{%s}\n" % c for c in ["ch00_front"] + CHAPTERS)
    return preamble + "\\begin{document}\n" + inputs + "\\end{document}\n"


def main():
    for old in R1.glob("ch*.tex"):
        old.unlink()
    for name in CHAPTERS:
        (R1 / f"{name}.tex").write_text(condense((R0 / f"{name}.tex").read_text()))
    (R1 / "ch00_front.tex").write_text(FRONT)
    (R1 / "main_r1.tex").write_text(main_tex())
    print(f"Wrote {len(CHAPTERS)} chapters, ch00_front.tex and main_r1.tex to {R1}")


if __name__ == "__main__":
    main()

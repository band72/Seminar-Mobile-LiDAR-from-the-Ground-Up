"""Build the one-page Simple Concept notes, one per module.

Each page has a big idea, a drawn picture (TikZ), a short explanation, three
points to remember and a hands-on activity. The wording follows each
module's Simple Approach boxes. Content lives in notes/content.py.

Writes notes/build/Simple_Concept_NN.tex and docs/notes/Simple_Concept_NN.pdf.
Requires: python3, latexmk + TeX Live.
Usage: python3 notes/build_notes.py [module numbers ...]
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content import NOTES  # noqa: E402

BUILD = HERE / "build"
OUT = HERE.parent / "docs" / "notes"

PREAMBLE = r"""\documentclass[12pt,letterpaper]{article}
\usepackage[T1]{fontenc}
\usepackage[scaled=0.95]{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[margin=0.65in,top=0.55in,bottom=0.55in]{geometry}
\usepackage{amssymb}
\usepackage{xcolor,tikz,enumitem,adjustbox}
\usetikzlibrary{arrows.meta,decorations.pathmorphing,decorations.pathreplacing,calc,shapes.geometric}
\usepackage[most]{tcolorbox}
\usepackage[hidelinks,pdfauthor={D.S. Banks, PSM}]{hyperref}
\pagestyle{empty}\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}
\hyphenpenalty=10000 \exhyphenpenalty=10000 \pgfmathsetseed{7}
\definecolor{navy}{HTML}{1F3B73}\definecolor{teal}{HTML}{138D75}\definecolor{orange}{HTML}{E67E22}
\definecolor{red}{HTML}{C0392B}\definecolor{purple}{HTML}{7D3C98}\definecolor{gold}{HTML}{B7950B}
\definecolor{kid}{HTML}{1E8449}\definecolor{grayx}{HTML}{5D6D7E}\definecolor{skin}{HTML}{F0C8A0}
\tcbset{note/.style={enhanced,boxrule=1pt,arc=4pt,left=8pt,right=8pt,top=5pt,bottom=5pt,
  fonttitle=\bfseries\large,before skip=7pt,after skip=7pt,before upper=\raggedright}}
\newtcolorbox{bigidea}{note,colback=gold!12,colframe=gold,title={BIG IDEA},fontupper=\Large\bfseries}
\newtcolorbox{idea}{note,colback=kid!6,colframe=kid,title={THE IDEA},fontupper=\large}
\newtcolorbox{remember}{note,colback=navy!4,colframe=navy,title={REMEMBER},fontupper=\large}
\newtcolorbox{trythis}{note,colback=purple!5,colframe=purple,title={TRY THIS},fontupper=\large}
\newcommand{\lbl}[1]{{\sffamily\bfseries\small #1}}
\tikzset{
 every picture/.style={line cap=round,line join=round},
 ray/.style={red!80!black,line width=1.2pt,-{Stealth[length=7pt]}},
 back/.style={teal,line width=1.2pt,-{Stealth[length=7pt]}},
 arr/.style={line width=1.4pt,-{Stealth[length=8pt]}},
 car/.pic={\fill[navy] (-1.1,0.15) rectangle (1.1,0.6); \fill[navy] (-0.65,0.6) rectangle (0.55,1.0);
   \fill[white] (-0.55,0.66) rectangle (-0.08,0.92); \fill[white] (0.02,0.66) rectangle (0.45,0.92);
   \fill[black] (-0.65,0.15) circle (0.24); \fill[black] (0.65,0.15) circle (0.24);
   \fill[gray!40] (-0.65,0.15) circle (0.1); \fill[gray!40] (0.65,0.15) circle (0.1);},
 scanner/.pic={\fill[orange] (-0.17,0) rectangle (0.17,0.34); \fill[red!70!black] (0,0.34) circle (0.09);},
 tree/.pic={\fill[brown!70!black] (-0.12,0) rectangle (0.12,0.9); \fill[kid!80] (0,1.35) circle (0.6);},
 house/.pic={\fill[orange!25] (-0.8,0) rectangle (0.8,1.1); \fill[red!70!black] (-0.95,1.1) -- (0,1.75) -- (0.95,1.1) -- cycle;
   \fill[navy!60] (-0.17,0) rectangle (0.17,0.55); \fill[white] (0.35,0.55) rectangle (0.62,0.85);},
 person/.pic={\fill[skin] (0,1.6) circle (0.22); \draw[line width=2.4pt,navy] (0,1.38)--(0,0.72) (0,0.72)--(-0.27,0) (0,0.72)--(0.27,0)
   (0,1.22)--(-0.33,0.86) (0,1.22)--(0.33,0.86);},
 satellite/.pic={\fill[gray!70] (-0.22,-0.22) rectangle (0.22,0.22); \fill[navy!60] (-0.85,-0.13) rectangle (-0.28,0.13);
   \fill[navy!60] (0.28,-0.13) rectangle (0.85,0.13);},
 imu/.pic={\fill[purple!20,draw=purple,line width=1pt,rounded corners=2pt] (-0.35,-0.25) rectangle (0.35,0.25); \node[purple] at (0,0) {\lbl{IMU}};},
}
\begin{document}
"""

PAGE = r"""{\color{grayx}\small\bfseries SIMPLE CONCEPT \textbullet\ MODULE %(num)d}\par\vspace{-2pt}
{\raggedright\color{navy}\fontsize{24}{28}\selectfont\bfseries %(title)s\par}\vspace{-4pt}
{\color{orange}\rule{\linewidth}{2pt}}
\begin{bigidea}%(bigidea)s\end{bigidea}
\begin{center}
\begin{adjustbox}{width=0.96\linewidth,max height=%(height)s}
%(picture)s
\end{adjustbox}
\end{center}
\begin{idea}%(idea)s\end{idea}
\begin{remember}
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,label={\color{navy}$\checkmark$}]
%(remember)s
\end{itemize}
\end{remember}
\begin{trythis}%(trythis)s\end{trythis}
\vfill
{\color{grayx}\small LiDAR from the Ground Up \textbullet\ D.S. Banks, PSM \hfill The full module is in the Reference Book.}
\end{document}
"""


def page(num, note):
    return PREAMBLE.replace("pdfauthor=", "pdftitle={Simple Concept: Module %d},pdfauthor=" % num) + PAGE % {
        "num": num, "title": note["title"], "bigidea": note["bigidea"], "picture": note["picture"].strip(),
        "height": note.get("height", "7.2cm"),
        "idea": note["idea"], "trythis": note["trythis"],
        "remember": "\n".join(f"\\item {r}" for r in note["remember"]),
    }


def main():
    wanted = {int(a) for a in sys.argv[1:]} or set(range(1, len(NOTES) + 1))
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for num, note in enumerate(NOTES, 1):
        if num not in wanted:
            continue
        tex = BUILD / f"Simple_Concept_{num:02d}.tex"
        tex.write_text(page(num, note))
        subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                       cwd=BUILD, check=True, stdout=subprocess.DEVNULL)
        pdf = OUT / tex.with_suffix(".pdf").name
        shutil.copy(tex.with_suffix(".pdf"), pdf)
        print(f"Module {num:2d}  {note['title']:40s} -> {pdf.relative_to(HERE.parent)}  {pdf.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

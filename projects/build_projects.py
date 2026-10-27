"""Generate the stand-alone Projects download from the R0 sources.

R0 files are only read, never written. The Projects PDF contains, unchanged:
  - Module 21, Capstone and Sample Project Dataset (ch15_capstone.tex)
  - Appendix D, Hands-On Labs (ch16b_labs.tex)
with their R0 module and appendix numbers, so they match the Reference Book.

Writes projects/main_projects.tex.
Usage: python3 projects/build_projects.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
R0 = HERE.parent

FRONT = r"""\frontmatter
\begin{titlepage}
\begin{tikzpicture}[remember picture,overlay]
\fill[fill={rgb,255:red,26;green,50;blue,99}] (current page.south west) rectangle (current page.north east);
\node[anchor=center] at ([yshift=-0.9in]current page.center) {\includegraphics[width=\paperwidth]{cover}};
\fill[orange] ([yshift=-3.05in]current page.north west) rectangle ([yshift=-3.12in]current page.north east);
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-0.8in]current page.north west)
 {\color{white}\sffamily\bfseries\fontsize{40}{46}\selectfont\spaceskip=0.28em LiDAR from the Ground Up};
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-1.65in]current page.north west)
 {\color{orange!60}\sffamily\Large Projects: Capstone and Hands-On Labs};
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-2.05in]current page.north west)
 {\color{white}\sffamily\bfseries\LARGE D.S. Banks, PSM};
\node[anchor=north west,text width=7in,align=left] at ([xshift=0.75in,yshift=-2.55in]current page.north west)
 {\color{white!85}\sffamily\large Module 21 and Appendix D of the Reference Book,\\ with the sample project dataset.};
\node[anchor=south west,text width=7in,align=left] at ([xshift=0.75in,yshift=0.8in]current page.south west)
 {\color{white!70}\sffamily\normalsize Companion to the Reference Book (R0)};
\end{tikzpicture}
\end{titlepage}
\clearpage\pagenumbering{arabic}\makeatletter\@mainmattertrue\@openrightfalse\makeatother
"""

APPENDIX = r"""\appendix
\titleformat{\chapter}[display]{\sffamily\bfseries\color{navy}}{\large APPENDIX \thechapter}{4pt}{\Huge}[\vspace{2pt}{\color{orange}\titlerule[2pt]}]
\renewcommand{\chaptermark}[1]{\markboth{Appendix \thechapter: #1}{}}
\setcounter{chapter}{3}
"""


def main():
    src = (R0 / "main.tex").read_text()
    preamble = src[:src.index("\\begin{document}")]
    preamble = preamble.replace("\\graphicspath{{figs/}}", "\\graphicspath{{../figs/}}")
    preamble = preamble.replace("pdftitle={LiDAR from the Ground Up}",
                                "pdftitle={LiDAR from the Ground Up: Projects (R0)}")
    preamble = preamble.replace("LiDAR from the Ground Up}\n\\fancyhead[R]",
                                "LiDAR from the Ground Up: Projects}\n\\fancyhead[R]")
    # The capstone cites an error-budget section that lives in Module 14 of the Reference Book.
    preamble += ("\\makeatletter\\AtBeginDocument{\\newlabel{sec:bud-cap}"
                 "{{14.11.4 of the Reference Book}{102}{}{}{}}}\\makeatother\n")
    body = (FRONT
            + "\\setcounter{chapter}{20}\n\\input{../ch15_capstone}\n"
            + APPENDIX + "\\input{../ch16b_labs}\n")
    (HERE / "main_projects.tex").write_text(preamble + "\\begin{document}\n" + body + "\\end{document}\n")
    print(f"Wrote {HERE / 'main_projects.tex'}")


if __name__ == "__main__":
    main()

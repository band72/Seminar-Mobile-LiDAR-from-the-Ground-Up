"""Build a seminar slide deck and its speaker-notes pages.

Slides are 960 x 540 pt (16:9) in the style of the Seminar 1 deck: cream
content slides, navy section slides and orange takeaway slides. The notes
PDF repeats each slide at the top of a page with the speaker notes below.

Slide content lives in a module that defines TITLE and SLIDES (for example
slides/seminar2.py). Each slide is a dict with a "kind":
  title    kicker, title, sub, author
  section  kicker, title, sub
  fig      kicker, title, fig, [big, biglabel], points, foot
  eq       kicker, title, eq, [steps], [big, biglabel], points, foot
  table    kicker, title, cols, head, rows, [hi], foot
  bullets  kicker, title, items (one list, set in two columns), foot
  take     kicker, nums [(number, caption), ...], line
and a "notes" string. Text is LaTeX.

Writes slides/build/<name>.tex and <name>_notes.tex, and the PDFs
docs/<out>.pdf and docs/<out>_with_Notes.pdf.
Requires: python3, latexmk + TeX Live, ghostscript (gs).
Usage: python3 slides/build_slides.py seminar2 Seminar_2_Slides
"""
import importlib
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
DOCS = HERE.parent / "docs"

PREAMBLE = r"""\documentclass[12pt]{article}
\usepackage[paperwidth=960bp,paperheight=540bp,margin=0pt]{geometry}
\usepackage[T1]{fontenc}
\usepackage[sfdefault]{plex-sans}
\usepackage{sourceserifpro}
\usepackage{amsmath,amssymb,bm,textcomp}
\usepackage[tracking=true]{microtype}
\usepackage{xcolor,graphicx,tikz,array,booktabs,colortbl,enumitem,multicol}
\usepackage[hidelinks,pdftitle={%(title)s},pdfauthor={D.S. Banks, PSM}]{hyperref}
\graphicspath{{../../figs/}}
\pagestyle{empty}\setlength{\parindent}{0pt}\hyphenpenalty=10000 \exhyphenpenalty=10000 \raggedright
\definecolor{cream}{HTML}{F4F1EA}\definecolor{navy}{HTML}{16213E}\definecolor{accent}{HTML}{B8611B}
\definecolor{take}{HTML}{E9A55C}\definecolor{mute}{HTML}{6B6B6B}\definecolor{rule}{HTML}{D9D4C7}
\definecolor{hi}{HTML}{FBE3C8}\definecolor{headbg}{HTML}{E4E0D8}
\newcommand{\vect}[1]{\mathbf{#1}}
\newcommand{\kick}[1]{{\sffamily\bfseries\fontsize{9}{11}\selectfont\textls[140]{\MakeUppercase{#1}}}}
\newcommand{\ttl}[1]{{\rmfamily\bfseries\fontsize{27}{31}\selectfont #1}}
\newcommand{\bignum}[1]{{\sffamily\bfseries\fontsize{46}{50}\selectfont #1}}
\newcommand{\body}{\sffamily\fontsize{15}{20.5}\selectfont}
\newcommand{\smalltxt}{\sffamily\fontsize{14}{19}\selectfont}
\setlist[itemize]{leftmargin=1.1em,itemsep=5pt,topsep=0pt,parsep=0pt,label={\color{accent}\textbullet}}
\newenvironment{slide}[1]{\begin{tikzpicture}[remember picture,overlay,x=1bp,y=1bp,shift={(current page.south west)}]
  \fill[#1] (0,0) rectangle (960,540);}{\end{tikzpicture}\newpage}
\newcommand{\head}[2]{\node[anchor=north west,text=accent,inner sep=0] at (64,486) {\kick{#1}};
  \node[anchor=north west,text=navy,inner sep=0,text width=832pt] at (64,466) {\ttl{#2}};}
\newcommand{\foot}[1]{\node[anchor=south west,text=mute,inner sep=0] at (64,34) {\sffamily\fontsize{9}{11}\selectfont #1};}
\newcommand{\card}[4]{\fill[white,rounded corners=6pt] (#1,#2) rectangle (#3,#4);}
\begin{document}
"""

TOP = 405  # top of the content area, below the title


def fit(num, width, top=66):
    """Largest font size (pt) at which a takeaway number fits its column."""
    chars = len(re.sub(r"\\[a-zA-Z]+|[{}$^_]", "", num))
    return max(30, min(top, int(width / (0.62 * max(chars, 1)))))


def right_column(s, x=592, width=304):
    """Big number, its label and bullet points in the right-hand column."""
    out, y = [], TOP
    if s.get("big"):
        out.append(r"\node[anchor=north west,text=accent,inner sep=0] at (%d,%d) {\bignum{%s}};" % (x, y, s["big"]))
        y -= 58
        out.append(r"\node[anchor=north west,text=navy,inner sep=0,text width=%dpt] at (%d,%d) {\body %s\par};"
                   % (width, x, y, s.get("biglabel", "")))
        y -= 26 + 21 * (len(s.get("biglabel", "")) // 38)
    if s.get("points"):
        items = "".join(r"\item %s" % p for p in s["points"])
        out.append(r"\node[anchor=north west,text=navy,inner sep=0,text width=%dpt] at (%d,%d) "
                   r"{\body\begin{itemize}%s\end{itemize}};" % (width, x, y - 6, items))
    return "\n".join(out)


def render(s):
    k = s["kind"]
    if k == "title":
        return (r"\begin{slide}{navy}" "\n"
                r"\begin{scope}\clip (500,0) rectangle (960,540);"
                r"\node[anchor=center,inner sep=0] at (730,270) {\includegraphics[height=540pt]{cover}};\end{scope}" "\n"
                r"\fill[navy,opacity=0.35] (500,0) rectangle (960,540);" "\n"
                r"\node[anchor=north west,text=take,inner sep=0] at (64,372) {\kick{%s}};" "\n"
                r"\node[anchor=north west,text=white,inner sep=0,text width=410pt] at (64,348) {\rmfamily\bfseries\fontsize{36}{41}\selectfont %s};" "\n"
                r"\node[anchor=north west,text=white!85!navy,inner sep=0,text width=400pt] at (64,206) {\body %s\par};" "\n"
                r"\node[anchor=north west,text=white,inner sep=0] at (64,150) {\sffamily\bfseries\fontsize{13}{16}\selectfont %s};" "\n"
                r"\end{slide}") % (s["kicker"], s["title"], s["sub"], s["author"])
    if k == "section":
        return (r"\begin{slide}{navy}" "\n"
                r"\node[anchor=north west,text=take,inner sep=0] at (64,366) {\kick{%s}};" "\n"
                r"\node[anchor=north west,text=white,inner sep=0,text width=700pt] at (64,342) {\rmfamily\bfseries\fontsize{38}{44}\selectfont %s};" "\n"
                r"\node[anchor=north west,text=white!80!navy,inner sep=0,text width=640pt] at (64,%d) {\body %s\par};" "\n"
                r"\end{slide}") % (s["kicker"], s["title"], 342 - 56 - 44 * (len(s["title"]) // 34), s["sub"])
    if k == "take":
        n = len(s["nums"])
        w = 832 // n
        nums = "\n".join(
            r"\node[anchor=north west,text=navy,inner sep=0] at (%d,340) {\sffamily\bfseries\fontsize{%d}{%d}\selectfont %s};"
            r"\node[anchor=north west,text=navy,inner sep=0,text width=%dpt] at (%d,258) {\smalltxt %s\par};"
            % (64 + i * w, fit(num, w - 28), 70, num, w - 24, 64 + i * w, cap)
            for i, (num, cap) in enumerate(s["nums"]))
        return (r"\begin{slide}{take}" "\n"
                r"\node[anchor=north west,text=navy,inner sep=0] at (64,376) {\kick{%s}};" "\n%s\n"
                r"\node[anchor=north west,text=navy,inner sep=0,text width=832pt] at (64,190) {\body %s\par};" "\n"
                r"\end{slide}") % (s["kicker"], nums, s["line"])
    out = [r"\begin{slide}{cream}", r"\head{%s}{%s}" % (s["kicker"], s["title"])]
    if k == "fig":
        out.append(r"\card{64}{62}{566}{%d}" % TOP)
        out.append(r"\node[anchor=center,inner sep=0] at (315,%d) {\includegraphics[width=478pt,height=%dpt,keepaspectratio]{%s}};"
                   % ((62 + TOP) // 2, TOP - 62 - 24, s["fig"]))
        out.append(right_column(s))
    elif k == "eq":
        out.append(r"\card{64}{62}{566}{%d}" % TOP)
        steps = ""
        if s.get("steps"):
            rows = "".join(r"\textbf{%s} & \raggedright\arraybackslash %s\tabularnewline[6pt]" % (a, b) for a, b in s["steps"])
            steps = r"\par\vspace{10pt}{\color{rule}\rule{\linewidth}{0.8pt}}\par\vspace{8pt}{\smalltxt\begin{tabular}{@{}p{118pt}p{330pt}@{}}%s\end{tabular}}" % rows
        out.append(r"\node[anchor=north west,text=navy,inner sep=0,text width=462pt] at (84,%d) "
                   r"{\body\begin{center}{\fontsize{%s}{28}\selectfont$\displaystyle %s$}\end{center}%s};" % (TOP - 16, s.get("eqsize", "24"), s["eq"], steps))
        out.append(right_column(s))
    elif k == "table":
        head = " & ".join(r"\textbf{%s}" % h for h in s["head"])
        rows = ""
        for i, r in enumerate(s["rows"]):
            pre = r"\rowcolor{hi}" if i in s.get("hi", ()) else ""
            rows += pre + " & ".join(r"\raggedright\arraybackslash " + c if i_c == len(r) - 1 else c for i_c, c in enumerate(r)) + r"\\\arrayrulecolor{rule}\hline" + "\n"
        out.append(r"\node[anchor=north west,text=navy,inner sep=0] at (64,%d) {\sffamily\fontsize{%s}{%s}\selectfont"
                   r"\renewcommand{\arraystretch}{%s}\setlength{\tabcolsep}{8pt}\begin{tabular}{%s}\rowcolor{headbg}%s\\\arrayrulecolor{rule}\hline %s\end{tabular}};"
                   % (TOP, s.get("size", "15.5"), s.get("lead", "20"), s.get("stretch", "1.7"), s["cols"], head, rows))
    elif k == "bullets":
        items = "".join(r"\item %s" % p for p in s["items"])
        out.append(r"\node[anchor=north west,text=navy,inner sep=0,text width=832pt] at (64,%d) "
                   r"{\body\setlength{\columnsep}{36pt}\begin{multicols}{2}\begin{itemize}[itemsep=9pt]%s\end{itemize}\end{multicols}};" % (TOP, items))
    if s.get("foot"):
        out.append(r"\foot{%s}" % s["foot"])
    out.append(r"\end{slide}")
    return "\n".join(out)


NOTES = r"""\documentclass[12pt]{article}
\usepackage[paperwidth=960bp,paperheight=540bp,margin=0pt]{geometry}
\usepackage[T1]{fontenc}
\usepackage[sfdefault]{plex-sans}
\usepackage{graphicx,tikz,xcolor,amsmath,amssymb,bm}
\newcommand{\vect}[1]{\mathbf{#1}}
\usepackage[hidelinks,pdftitle={%(title)s (with speaker notes)},pdfauthor={D.S. Banks, PSM}]{hyperref}
\pagestyle{empty}\setlength{\parindent}{0pt}
\begin{document}
%(pages)s
\end{document}
"""

NOTE_PAGE = r"""\begin{tikzpicture}[remember picture,overlay,x=1bp,y=1bp,shift={(current page.south west)}]
\node[anchor=north,inner sep=0] at (480,524) {\includegraphics[page=%d,width=336pt]{%s}};
\node[anchor=north west,inner sep=0,text width=904pt] at (28,310) {\sffamily\fontsize{13}{18.5}\selectfont %s\par};
\end{tikzpicture}\newpage
"""


def latexmk(tex):
    subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                   cwd=tex.parent, check=True, stdout=subprocess.DEVNULL)


def compress(src, dst, dpi):
    """Downsample figures to JPEG at the given resolution; text stays vector."""
    subprocess.run(["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.6", "-dPDFSETTINGS=/ebook",
                    "-dDownsampleColorImages=true", "-dColorImageDownsampleType=/Bicubic",
                    f"-dColorImageResolution={dpi}", f"-dGrayImageResolution={dpi}",
                    "-dAutoFilterColorImages=false", "-dColorImageFilter=/DCTEncode", "-dJPEGQ=85",
                    "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-sOutputFile={dst}", str(src)], check=True)


def main():
    name, out = sys.argv[1], sys.argv[2]
    sys.path.insert(0, str(HERE))
    deck = importlib.import_module(name)
    BUILD.mkdir(exist_ok=True)
    tex = BUILD / f"{name}.tex"
    tex.write_text(PREAMBLE % {"title": deck.TITLE} + "\n".join(render(s) for s in deck.SLIDES) + "\n\\end{document}\n")
    latexmk(tex)
    notes = BUILD / f"{name}_notes.tex"
    pages = "".join(NOTE_PAGE % (i, tex.with_suffix(".pdf").name, s["notes"]) for i, s in enumerate(deck.SLIDES, 1))
    notes.write_text(NOTES % {"title": deck.TITLE, "pages": pages})
    latexmk(notes)
    compress(tex.with_suffix(".pdf"), DOCS / f"{out}.pdf", 200)
    compress(notes.with_suffix(".pdf"), DOCS / f"{out}_with_Notes.pdf", 150)
    print(f"{len(deck.SLIDES)} slides -> docs/{out}.pdf and docs/{out}_with_Notes.pdf")


if __name__ == "__main__":
    main()

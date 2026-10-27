"""Verify the R1 chapters against R0.

For each r1/ch*.tex module, checks that the SIMPLE APPROACH, BIG IDEA,
SURVEYOR'S FIELD TIP and WARNING boxes and the \\fig figures are exactly the
ones in the matching R0 chapter, word for word and in the same order, and
that no box type outside that set slipped in. Also checks that every
\\ref/\\pageref/\\eqref in R1 points to a \\label that exists in R1.

Usage: python3 r1/check_boxes.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_r1 import CHAPTERS, KEEP_BOXES, items  # noqa: E402

R1 = Path(__file__).resolve().parent
R0 = R1.parent
OTHER_BOXES = re.compile(r"\\begin\{(eng|worked|tryit|improve|keyeq|seminar|tcolorbox)\}|\\sources\{")


def content(text):
    return [src for kind, src in items(text) if kind in ("box", "fig")]


def main():
    failed = 0
    labels, refs = set(), set()
    for name in CHAPTERS:
        r0 = (R0 / f"{name}.tex").read_text()
        r1 = (R1 / f"{name}.tex").read_text()
        labels |= set(re.findall(r"\\label\{([^}]*)\}", r1))
        refs |= set(re.findall(r"\\(?:page|eq)?ref\{([^}]*)\}", r1))
        problems = []
        a, b = content(r0), content(r1)
        if a != b:
            problems.append(f"boxes/figures differ: R0 has {len(a)}, R1 has {len(b)}")
        if OTHER_BOXES.search(r1):
            problems.append("contains a box type that R1 should drop")
        nbox = sum(s.startswith("\\begin") for s in b)
        status = "FAIL" if problems else "PASS"
        failed += bool(problems)
        print(f"{status}  {name:20s} boxes {nbox:3d}  figures {len(b) - nbox:3d}  "
              f"size {len(r1) * 100 // len(r0):3d}% of R0")
        for p in problems:
            print(f"      {p}")
    dangling = refs - labels
    if dangling:
        failed += 1
        print(f"FAIL  references with no label in R1: {sorted(dangling)}")
    print(f"\n{failed} problem(s)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

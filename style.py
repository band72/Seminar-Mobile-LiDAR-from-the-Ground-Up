import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch, Polygon, Arc, Ellipse

NAVY = "#1f3b73"; TEAL = "#138d75"; ORANGE = "#e67e22"; RED = "#c0392b"
GRAY = "#7f8c8d"; LIGHT = "#ecf0f1"; PURPLE = "#7d3c98"; GOLD = "#d4ac0d"; SKY = "#5dade2"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.titlesize": 11,
    "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#555555", "axes.labelcolor": "#222222", "savefig.dpi": 200,
    "savefig.bbox": "tight", "mathtext.fontset": "dejavusans",
})

def save(fig, name):
    fig.savefig(f"figs/{name}.png")
    plt.close(fig)

def arrow(ax, p0, p1, color=NAVY, lw=2, style="-|>", ms=14, ls="-", **kw):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, linestyle=ls, **kw)
    ax.add_patch(a)
    return a

def box(ax, xy, w, h, text, fc=LIGHT, ec=NAVY, fs=9, tc="#111", r=0.03, bold=False):
    b = FancyBboxPatch(xy, w, h, boxstyle=f"round,pad=0.01,rounding_size={r}", fc=fc, ec=ec, lw=1.5)
    ax.add_patch(b)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            weight="bold" if bold else "normal", wrap=True)
    return b

def blank(w=7, h=3.5):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax

def car(ax, x, y, s=1.0, color=NAVY, sensor=True):
    ax.add_patch(FancyBboxPatch((x - 1.2 * s, y), 2.4 * s, 0.6 * s, boxstyle="round,pad=0.02,rounding_size=0.15", fc=color, ec="k", lw=1))
    ax.add_patch(FancyBboxPatch((x - 0.7 * s, y + 0.6 * s), 1.3 * s, 0.45 * s, boxstyle="round,pad=0.02,rounding_size=0.12", fc=color, ec="k", lw=1))
    for dx in (-0.7, 0.7):
        ax.add_patch(Circle((x + dx * s, y), 0.25 * s, fc="#222", ec="k"))
    if sensor:
        ax.add_patch(Rectangle((x - 0.15 * s, y + 1.05 * s), 0.3 * s, 0.25 * s, fc=ORANGE, ec="k"))

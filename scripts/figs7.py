from style import *
from matplotlib.patches import FancyArrowPatch, Ellipse
SKIN = "#f2c9a0"; SKIN_D = "#b9875c"

def finger(ax, p0, p1, lw=17):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=SKIN_D, lw=lw + 3, solid_capstyle="round", zorder=3)
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=SKIN, lw=lw, solid_capstyle="round", zorder=4)

# projection: x toward viewer (lower-left), y right, z up  -> right-handed
PX = np.array([-0.62, -0.48]); PY = np.array([1.0, 0.0]); PZ = np.array([0.0, 1.0])

# ---------- Figure 1: right-hand rule for axes ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.6))
for a in (a1, a2): a.set_aspect("equal"); a.axis("off")
o = np.array([0.0, 0.0])
# palm
a1.add_patch(Ellipse(o + np.array([0.05, -0.05]), 0.95, 0.75, angle=20, fc=SKIN, ec=SKIN_D, lw=2.5, zorder=2))
# curled ring & pinky
for off in (np.array([0.25, -0.35]), np.array([0.38, -0.2])):
    a1.add_patch(Ellipse(o + off, 0.32, 0.22, angle=-20, fc=SKIN, ec=SKIN_D, lw=2, zorder=5))
finger(a1, o + np.array([-0.15, -0.15]), o + 1.25 * PX)           # index -> X
finger(a1, o + np.array([0.3, 0.05]), o + 1.55 * PY + np.array([0, 0.05]))  # middle -> Y
finger(a1, o + np.array([0.1, 0.25]), o + 1.45 * PZ + np.array([0.1, 0]))   # THUMB -> Z
for v, c, lab, sub, off in [(PX, RED, "X", "index finger = forward,\npointing OUT of the page toward you", (-0.4, -0.95)), (PY, TEAL, "Y", "middle finger\n= left", (0.1, -0.45)),
                            (PZ, NAVY, "Z", "THUMB = up\n(always Z)", (-1.6, -0.65))]:
    tip = 2.15 * v if lab != "Y" else 2.3 * v
    arrow(a1, (0, 0), tuple(tip), c, lw=3, ms=22)
    a1.text(tip[0] - (0.35 if lab == "X" else -0.05), tip[1] + 0.12, lab, color=c, fontsize=18, weight="bold")
    a1.text(tip[0] + off[0], tip[1] + off[1], sub, color=c, fontsize=9, ha="left")
a1.add_patch(FancyArrowPatch(tuple(1.05 * PX + np.array([0.05, -0.1])), tuple(1.2 * PY + np.array([0, -0.35])), connectionstyle="arc3,rad=0.45", arrowstyle="-|>", mutation_scale=16, color=PURPLE, lw=2, zorder=8))
a1.text(0.55, -1.35, "fingers curl from X toward Y\n→ thumb points to +Z", color=PURPLE, fontsize=8.5)
# inset: front view, X out of page shown as dot-in-circle (unambiguous)
ins = a1.inset_axes([0.70, 0.66, 0.30, 0.34]); ins.set_aspect("equal"); ins.axis("off")
ins.add_patch(Rectangle((-1.15, -1.15), 2.6, 2.6, fill=False, ec=GRAY, lw=0.8))
arrow(ins, (0, 0), (1.1, 0), TEAL, lw=2, ms=12); ins.text(1.0, 0.15, "Y", color=TEAL, fontsize=10, weight="bold")
arrow(ins, (0, 0), (0, 1.1), NAVY, lw=2, ms=12); ins.text(0.12, 1.0, "Z", color=NAVY, fontsize=10, weight="bold")
ins.add_patch(Circle((0, 0), 0.22, fc="white", ec=RED, lw=2, zorder=5)); ins.plot(0, 0, "o", color=RED, ms=4, zorder=6)
ins.text(-1.05, -0.55, "X \u2299 out of page", color=RED, fontsize=7.5)
ins.text(-1.05, -0.95, "front view", color=GRAY, fontsize=7)
ins.set_xlim(-1.2, 1.5); ins.set_ylim(-1.2, 1.5)
a1.set_xlim(-2.0, 3.0); a1.set_ylim(-2.0, 2.7)
a1.set_title("1. Axes: RIGHT hand — the thumb is always Z", fontsize=10)

# ---------- curl rule panel ----------
def proj(v): return v[0] * PX + v[1] * PY + v[2] * PZ
def curl(ax, c0, a3, u3, color, name, r=0.42):
    a3 = np.array(a3, float); u3 = np.array(u3, float); w3 = np.cross(a3, u3)
    tip = c0 + 1.5 * proj(a3) / np.linalg.norm(proj(a3))
    arrow(ax, tuple(c0 - 0.35 * proj(a3) / np.linalg.norm(proj(a3))), tuple(tip), color, lw=3, ms=18)
    ctr = c0 + 0.75 * proj(a3) / np.linalg.norm(proj(a3))
    t = np.linspace(0.1 * np.pi, 1.75 * np.pi, 90)
    pts = np.array([ctr + r * (proj(u3) * np.cos(tt) + proj(w3) * np.sin(tt)) for tt in t])
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=2.2)
    ax.add_patch(FancyArrowPatch(tuple(pts[-4]), tuple(pts[-1]), arrowstyle="-|>", mutation_scale=16, color=color, lw=2))
    ax.text(tip[0] + (0.1 if name != "X" else -0.35), tip[1] + 0.08, name, color=color, fontsize=12, weight="bold")

c = np.array([0.0, 0.0])
curl(a2, c + np.array([-0.1, -0.1]), (1, 0, 0), (0, 1, 0), RED, "X")
curl(a2, c + np.array([0.3, -0.1]), (0, 1, 0), (0, 0, 1), TEAL, "Y")
curl(a2, c + np.array([0.0, 0.2]), (0, 0, 1), (1, 0, 0), NAVY, "Z")
a2.text(-1.9, 2.85, "2. Rotations: point the RIGHT thumb along an axis;\n    the fingers curl in the POSITIVE direction", fontsize=9.5, va="top")
a2.text(-1.9, -1.55, "ROLL = about X     PITCH = about Y     YAW = about Z", fontsize=9.5, weight="bold")
a2.text(-1.9, -1.95, "Looking from the arrow tip back toward the origin, positive = counter-clockwise", fontsize=8.5, color=GRAY)
# little curled-hand icon
ic = np.array([2.6, 1.15])
a2.add_patch(Ellipse(ic, 0.6, 0.45, fc=SKIN, ec=SKIN_D, lw=2))
for k, dy in enumerate([0.12, 0.0, -0.12]):
    a2.add_patch(Ellipse(ic + np.array([0.22, dy]), 0.28, 0.14, fc=SKIN, ec=SKIN_D, lw=1.5, zorder=5))
finger(a2, ic + np.array([-0.05, 0.1]), ic + np.array([-0.05, 0.85]), lw=12)
arrow(a2, tuple(ic + np.array([-0.05, 0.95])), tuple(ic + np.array([-0.05, 1.25])), "k", lw=2, ms=14)
a2.text(ic[0] + 0.25, ic[1] + 0.95, "thumb\n= axis", fontsize=8)
a2.add_patch(FancyArrowPatch(tuple(ic + np.array([-0.45, -0.12])), tuple(ic + np.array([0.48, -0.12])), connectionstyle="arc3,rad=0.45", arrowstyle="-|>", mutation_scale=14, color="k", lw=1.5, zorder=7))
a2.text(ic[0] - 0.6, ic[1] - 0.95, "fingers curl = +rotation\n(counter-clockwise seen\nfrom the thumb tip)", fontsize=7.5)
a2.set_xlim(-2.0, 3.2); a2.set_ylim(-2.1, 3.0)
save(fig, "righthand")

# ---------- Figure 2: vehicle FLU vs FRD ----------
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.2))
for ax, conv in zip(axs, ["FLU", "FRD"]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3.2, 3.6); ax.set_ylim(-3.1, 2.8)
    # car body in iso (x toward viewer-left)
    def P(x, y, z): return x * PX + y * PY + z * PZ
    body = [P(1.4, -0.7, 0), P(1.4, 0.7, 0), P(-1.4, 0.7, 0), P(-1.4, -0.7, 0)]
    ax.add_patch(Polygon(body, fc="#d6eaf8", ec=NAVY, lw=1.5))
    top = [P(0.6, -0.55, 0.6), P(0.6, 0.55, 0.6), P(-0.9, 0.55, 0.6), P(-0.9, -0.55, 0.6)]
    ax.add_patch(Polygon(top, fc="#aed6f1", ec=NAVY, lw=1.2))
    if conv == "FLU":
        axes = [(P(1, 0, 0), RED, "X forward"), (P(0, 1, 0), TEAL, "Y left"), (P(0, 0, 1), NAVY, "Z up")]
        notes = ["+roll: LEFT side up,\n  right side down", "+pitch: nose DOWN", "+yaw: nose turns LEFT\n  (counter-clockwise from above)"]
        title = "FLU (robotics / ROS / LIO-SAM)"
    else:
        axes = [(P(1, 0, 0), RED, "X forward"), (P(0, -1, 0), TEAL, "Y right"), (P(0, 0, -1), NAVY, "Z down")]
        notes = ["+roll: RIGHT side down", "+pitch: nose UP", "+yaw: nose turns RIGHT\n  (clockwise from above, like azimuth)"]
        title = "FRD (aerospace / many INS units)"
    for v, c, lab in axes:
        tip = 2.0 * v / np.linalg.norm(v) if lab != "Y left" and lab != "Y right" else 2.2 * v / np.linalg.norm(v)
        arrow(ax, (0, 0.3), (tip[0], tip[1] + 0.3), c, lw=3, ms=18)
        ax.text(tip[0] + (0.1 if tip[0] >= 0 else -1.3), tip[1] + (0.45 if "X" not in lab else 0.0), lab, color=c, fontsize=10, weight="bold")
    for i, n in enumerate(notes):
        ax.text(-3.1, -1.55 - 0.62 * i, n, fontsize=8.5, color=[RED, TEAL, NAVY][i], va="top")
    ax.set_title(title + "\n(car nose points toward you)", fontsize=10)
save(fig, "rhr_vehicle")
print("figs7 done")

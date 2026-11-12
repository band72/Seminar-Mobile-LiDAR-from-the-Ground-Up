from style import *
rng = np.random.default_rng(11)

def cov_ellipse(ax, mu, P, k=2.0, **kw):
    w, V = np.linalg.eigh(P); ang = np.degrees(np.arctan2(V[1, 1], V[0, 1]))
    ax.add_patch(Ellipse(mu, 2 * k * np.sqrt(w[1]), 2 * k * np.sqrt(w[0]), angle=ang, **kw))

# SLAM chicken & egg
fig, ax = blank(7.5, 3)
box(ax, (0, 0.8), 2.6, 1.2, "MAP\n'where are the walls?'", fc="#d6eaf8", fs=9)
box(ax, (4.6, 0.8), 2.6, 1.2, "LOCALIZATION\n'where am I?'", fc="#fdebd0", ec=ORANGE, fs=9)
arrow(ax, (2.7, 1.75), (4.5, 1.75), NAVY, connectionstyle="arc3,rad=-0.3"); arrow(ax, (4.5, 1.05), (2.7, 1.05), ORANGE, connectionstyle="arc3,rad=-0.3")
ax.text(3.6, 2.45, "need a map to know where you are", ha="center", fontsize=8); ax.text(3.6, 0.25, "need your position to draw the map", ha="center", fontsize=8)
ax.text(3.6, 1.4, "SLAM: solve\nboth at once", ha="center", va="center", fontsize=9, weight="bold", color=RED)
ax.set_xlim(-0.2, 7.4); ax.set_ylim(0, 2.8); save(fig, "chicken")

# motion model arc (schematic, exaggerated)
fig, ax = blank(6, 3.6)
w = 0.6; a = np.radians(40); Rt = 1.6; c = np.array([0, Rt + w / 2])
for rad, col, lab, lw, ls in [(Rt, NAVY, "left track travels L", 3, "-"), (Rt + w, ORANGE, "right track travels R (longer)", 3, "-"), (Rt + w / 2, RED, "path of the center", 1.5, "--")]:
    th = np.linspace(-np.pi / 2, -np.pi / 2 + a, 50); ax.plot(c[0] + rad * np.cos(th), c[1] + rad * np.sin(th), color=col, lw=lw, ls=ls, label=lab)
for ang in (-np.pi/2, -np.pi/2 + a):
    ax.plot([c[0], c[0] + (Rt + w) * np.cos(ang)], [c[1], c[1] + (Rt + w) * np.sin(ang)], color=GRAY, lw=1)
ax.add_patch(Arc(c, 0.9, 0.9, theta1=-90, theta2=-90 + 40, color="k")); ax.text(0.12, c[1] - 0.75, r"$\alpha$", fontsize=13)
ax.plot(*c, "ko"); ax.text(c[0] - 0.08, c[1] + 0.05, "center of turn", fontsize=8, ha="right")
ax.annotate("", (0, Rt + w / 2 - Rt), (0, w / 2 - w + Rt + w / 2 - Rt - w/2 + 0.0001), arrowprops=dict(arrowstyle="-"))
ax.annotate("", (-0.15, 0.3 - 0.0), (-0.15, -0.3), arrowprops=dict(arrowstyle="<->")); ax.text(-0.25, 0.0, "w", ha="right", va="center")
ax.text(1.0, -0.55, "(angle exaggerated for clarity)", fontsize=7, color=GRAY)
ax.legend(loc="upper right", fontsize=8, frameon=False)
ax.set_xlim(-1.0, 2.6); ax.set_ylim(-0.7, 3.0); save(fig, "motionmodel")

# uncertainty growth
fig, ax = plt.subplots(figsize=(8, 3)); ax.set_aspect("equal")
P = np.diag([0.002, 0.002]); xs = np.linspace(0, 10, 11)
for i, x in enumerate(xs):
    y = 0.3 * np.sin(x / 3)
    if i == 7: P = P * 0.15; ax.plot([x, 8.5], [y, 2.3], color=TEAL, ls=":"); ax.plot(8.5, 2.3, "^", color=TEAL, ms=12); ax.text(8.7, 2.3, "landmark seen!", color=TEAL, fontsize=9)
    cov_ellipse(ax, (x, y), P, fc=ORANGE if i < 7 else TEAL, alpha=.35, ec="k"); ax.plot(x, y, "k.")
    P = P + np.diag([0.012, 0.006]) * (i + 1) * 0.6
ax.set_xlim(-1, 11.5); ax.set_ylim(-1.8, 2.8); ax.axis("off")
ax.set_title("Moving makes the 'where am I?' blob grow; seeing a landmark shrinks it", fontsize=10)
save(fig, "uncertainty")

# Gaussian fusion 1D Kalman
fig, ax = plt.subplots(figsize=(7, 3))
x = np.linspace(98.5, 101.5, 600)
def g(m, s): return np.exp(-(x - m) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi))
ax.plot(x, g(100, 0.5), color=ORANGE, lw=2.5, label="prediction  100.0 ± 0.50 m")
ax.plot(x, g(100.4, 0.2), color=NAVY, lw=2.5, label="measurement 100.4 ± 0.20 m")
ax.plot(x, g(100.345, 0.1857), color=RED, lw=3, ls="--", label="combined   100.345 ± 0.186 m")
ax.set_yticks([]); ax.set_xlabel("position (m)"); ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.set_title("Kalman update: blend two guesses, trust the sharper one more"); save(fig, "kalman1d")

# particles
fig, ax = plt.subplots(figsize=(7, 3)); ax.set_aspect("equal")
for yc in (0, 3): ax.add_patch(Rectangle((0, yc - 0.6), 12, 1.2, fc="#eaecee", ec=GRAY))
for yc, n in ((0, 140), (3, 110)):
    px = rng.normal(6, 0.9, n); py = rng.normal(yc, 0.2, n); wts = rng.uniform(5, 30, n); ax.scatter(px, py, s=wts, color=PURPLE, alpha=.5)
ax.text(12.3, 0, "corridor A", va="center", fontsize=9); ax.text(12.3, 3, "corridor B", va="center", fontsize=9)
ax.set_xlim(-0.5, 15); ax.set_ylim(-1, 4); ax.axis("off"); ax.set_title("Particle filter: many guesses can live in two places at once", fontsize=10)
save(fig, "particles")

# EKF ellipse before/after (from computed numbers)
Pb = np.array([[0.012, -0.00001], [-0.00001, 0.01218]]); Pa = np.array([[0.00244, -0.00182], [-0.00182, 0.011]])
fig, ax = plt.subplots(figsize=(5.8, 3.6)); ax.set_aspect("equal")
cov_ellipse(ax, (10.423, 5.035), Pb, fc=ORANGE, alpha=.3, ec=ORANGE, lw=2); cov_ellipse(ax, (10.363, 5.021), Pa, fc=TEAL, alpha=.4, ec=TEAL, lw=2)
ax.plot(10.423, 5.035, "o", color=ORANGE, label="predicted (10.423, 5.035)"); ax.plot(10.363, 5.021, "o", color=TEAL, label="corrected (10.363, 5.021)")
arrow(ax, (10.6, 5.07), (11.0, 5.15), NAVY); ax.text(10.75, 5.22, "to landmark\n(25, 8)", fontsize=8, color=NAVY)
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.legend(fontsize=8, frameon=False, loc="lower left"); ax.set_xlim(10.0, 11.2); ax.set_ylim(4.65, 5.45)
ax.set_title("EKF: the 2σ blob shrinks along the range direction", fontsize=10); save(fig, "ekf")

# ICP iterations (real NN ICP)
def icp_step(Pp, Qq):
    from numpy.linalg import svd, det
    d = ((Pp[:, None, :] - Qq[None, :, :]) ** 2).sum(-1); idx = d.argmin(1); M = Qq[idx]
    pb, qb = Pp.mean(0), M.mean(0); H = (Pp - pb).T @ (M - qb); U, S, Vt = svd(H); R = Vt.T @ U.T
    if det(R) < 0: Vt[-1] *= -1; R = Vt.T @ U.T
    t = qb - R @ pb; return Pp @ R.T + t, M, np.sqrt(d.min(1).mean())
s = np.linspace(0, 1, 40)
shape = np.vstack([np.c_[s * 6, 0 * s], np.c_[6 + 0 * s, s * 3], np.c_[6 - s * 2.5, 3 + 0 * s], np.c_[3.5 + 0 * s, 3 + s * 1.5]])
Qq = shape + 0.02 * rng.standard_normal(shape.shape)
th = np.radians(14); R0 = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]); Pp = (shape - 3) @ R0.T + 3 + [0.9, -0.6]
fig, axs = plt.subplots(1, 4, figsize=(9.5, 2.6)); cur = Pp.copy()
for k, ax in enumerate(axs):
    ax.plot(Qq[:, 0], Qq[:, 1], ".", color=NAVY, ms=3); ax.plot(cur[:, 0], cur[:, 1], ".", color=RED, ms=3)
    nxt, M, err = icp_step(cur, Qq)
    if k == 0:
        for a, b in zip(cur[::4], M[::4]): ax.plot([a[0], b[0]], [a[1], b[1]], color=GRAY, lw=0.6)
    ax.set_title(f"iteration {k}\nRMS gap {err*100:.0f} cm", fontsize=9); ax.set_aspect("equal"); ax.axis("off")
    for _ in range(1 if k < 2 else 6): cur, M, err = icp_step(cur, Qq)
save(fig, "icp_iters")

# ICP 4-point example
P4 = np.array([[0, 0], [2, 0], [2, 1], [0, 3]], float); th = np.radians(10); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]); Q4 = P4 @ R.T + [1, 0.5]
fig, ax = plt.subplots(figsize=(5.5, 3.6)); ax.set_aspect("equal")
ax.add_patch(Polygon(P4, fill=False, ec=RED, lw=2)); ax.add_patch(Polygon(Q4, fill=False, ec=NAVY, lw=2))
for i, (p, q) in enumerate(zip(P4, Q4)):
    ax.plot(*p, "o", color=RED); ax.plot(*q, "s", color=NAVY); ax.text(p[0] - 0.35, p[1] - 0.25, f"p{i+1}", color=RED, fontsize=9); ax.text(q[0] + 0.08, q[1] + 0.08, f"q{i+1}", color=NAVY, fontsize=9)
    arrow(ax, p, q, GRAY, lw=0.8, ms=8)
ax.plot(1, 1, "x", color=RED, ms=10, mew=2); ax.plot(1.811, 1.658, "x", color=NAVY, ms=10, mew=2); ax.text(0.5, 1.15, "p̄", color=RED); ax.text(1.9, 1.75, "q̄", color=NAVY)
ax.grid(alpha=.3); ax.set_xlim(-0.7, 3.6); ax.set_ylim(-0.5, 3.8); ax.set_title("Source (red) and target (blue) scans", fontsize=10); save(fig, "icp4")

# point-to-point vs point-to-plane
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 2.8))
for a, ttl in [(a1, "point-to-point"), (a2, "point-to-plane")]:
    xs = np.arange(0, 6.1, 1.0); a.plot(xs, 0 * xs, "s", color=NAVY); a.plot([-0.3, 6.3], [0, 0], color=NAVY, lw=1, alpha=.4)
    ps = np.c_[xs[:-1] + 0.45, 0.6 + 0 * xs[:-1]]; a.plot(ps[:, 0], ps[:, 1], "o", color=RED)
    for p in ps:
        if a is a1:
            n = xs[np.argmin(abs(xs - p[0]))]; a.plot([p[0], n], [p[1], 0], color=GRAY)
        else:
            a.plot([p[0], p[0]], [p[1], 0], color=GRAY)
    a.set_title(ttl, fontsize=10); a.set_aspect("equal"); a.axis("off")
a2.set_ylim(-1.3, 1); a1.set_ylim(-1.3, 1)
a2.text(0, -1.2, "only the gap perpendicular to the surface counts\n-> points may slide along walls; converges faster", fontsize=8)
a1.text(0, -1.2, "pulls toward sampled points\n-> zig-zag, slow on flat surfaces", fontsize=8)
save(fig, "p2plane")

# NDT
fig, ax = plt.subplots(figsize=(5.5, 3.6)); ax.set_aspect("equal")
pts = np.vstack([np.c_[rng.uniform(0, 8, 300), 0.05 * rng.standard_normal(300)], np.c_[8 + 0.05 * rng.standard_normal(200), rng.uniform(0, 6, 200)], np.c_[rng.uniform(2, 4, 120), 3 + rng.uniform(0, 2, 120) * 0.7]])
ax.plot(pts[:, 0], pts[:, 1], ".", ms=1.5, color=NAVY)
for gx in range(0, 10, 2):
    for gy in range(-2, 8, 2):
        m = (pts[:, 0] >= gx) & (pts[:, 0] < gx + 2) & (pts[:, 1] >= gy) & (pts[:, 1] < gy + 2)
        ax.add_patch(Rectangle((gx, gy), 2, 2, fill=False, ec=GRAY, lw=.5))
        if m.sum() > 5: cov_ellipse(ax, pts[m].mean(0), np.cov(pts[m].T) + 1e-4 * np.eye(2), fc=ORANGE, alpha=.35, ec=ORANGE)
ax.set_xlim(-0.5, 10); ax.set_ylim(-2, 8); ax.axis("off"); ax.set_title("NDT: each grid cell becomes a little bell-curve blob", fontsize=10); save(fig, "ndt")

# LOAM features
fig, ax = plt.subplots(figsize=(6.5, 3.4)); ax.set_aspect("equal")
ang = np.linspace(-np.pi * 0.9, np.pi * 0.9, 400)
def ray(a):
    d = []
    for (x0, y0, x1, y1) in [(-6, 4, 6, 4), (6, 4, 6, -4), (6, -4, -6, -4), (-6, -4, -6, 4), (2, 1.5, 3, 1.5), (3, 1.5, 3, 2.5), (2, 2.5, 3, 2.5), (2, 1.5, 2, 2.5)]:
        ex, ey = x1 - x0, y1 - y0; dx, dy = np.cos(a), np.sin(a); den = dx * ey - dy * ex
        if abs(den) < 1e-9: continue
        t = (x0 * ey - y0 * ex) / den; u = (x0 * dy - y0 * dx) / den
        if t > 0 and 0 <= u <= 1: d.append(t)
    return min(d)
r = np.array([ray(a) for a in ang]); P = np.c_[r * np.cos(ang), r * np.sin(ang)]
cv = np.array([abs(sum(r[j] - r[i] for j in range(i - 3, i + 4) if j != i and 0 <= j < len(r))) / (6 * r[i]) for i in range(len(r))])
edge = cv > 0.02
ax.plot(P[~edge, 0], P[~edge, 1], ".", color=NAVY, ms=4, label="planar (smooth) points")
ax.plot(P[edge, 0], P[edge, 1], "o", color=RED, ms=4, label="edge (sharp) points")
ax.plot(0, 0, "^", color="k", ms=9); ax.legend(fontsize=8, frameon=False, loc="lower left", bbox_to_anchor=(0, -0.22))
ax.axis("off"); ax.set_title("Feature extraction: sharp corners vs flat walls", fontsize=10); save(fig, "loam")

# edge/plane distance geometry
fig = plt.figure(figsize=(8, 3.2))
a1 = fig.add_subplot(121); a1.set_aspect("equal"); a1.axis("off")
a1.plot([0, 2.6], [0, 0], color=NAVY, lw=2); a1.plot([0, 2], [0, 0], "s", color=NAVY); a1.text(-0.1, -0.25, "a=(0,0,0)", fontsize=8); a1.text(1.8, -0.25, "b=(2,0,0)", fontsize=8)
a1.plot(1, 1, "o", color=RED); a1.text(1.05, 1.08, "p=(1, 0.6, 0.8)", color=RED, fontsize=8); a1.plot([1, 1], [0, 1], "--", color=RED); a1.text(1.05, 0.45, "d = 1.0", color=RED)
a1.set_title("distance to an edge line", fontsize=10); a1.set_xlim(-0.4, 2.8); a1.set_ylim(-0.5, 1.4)
a2 = fig.add_subplot(122, projection="3d")
xx, yy = np.meshgrid([0, 1], [0, 1]); a2.plot_surface(xx, yy, 0 * xx, alpha=.3, color=SKY)
a2.scatter([0, 1, 0], [0, 0, 1], [0, 0, 0], color=NAVY, s=25); a2.scatter([0.3], [0.4], [0.12 * 4], color=RED, s=30)
a2.plot([0.3, 0.3], [0.4, 0.4], [0, 0.48], "r--"); a2.text(0.35, 0.4, 0.5, "p, d = 0.12", color=RED, fontsize=8)
a2.set_title("distance to a plane patch", fontsize=10); a2.set_zlim(0, 0.6); a2.axis("off"); a2.view_init(20, -60)
save(fig, "edgeplane")

# hallway
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.5, 2.6), gridspec_kw=dict(width_ratios=[1.6, 1]))
a1.add_patch(Rectangle((0, 0), 14, 2, fc="#f4f6f7", ec=NAVY, lw=2)); a1.plot(3, 1, "^", ms=10, color=ORANGE)
a1.annotate("", (3, 0.15), (3, 1.85), arrowprops=dict(arrowstyle="<->", color=TEAL, lw=2)); a1.text(3.2, 1.45, "walls pin\nleft/right", color=TEAL, fontsize=8)
a1.annotate("", (1.2, 1), (6.5, 1), arrowprops=dict(arrowstyle="<->", color=RED, lw=2, ls="--")); a1.text(4.5, 0.4, "forward/back: nothing to grab", color=RED, fontsize=8)
a1.set_xlim(-0.3, 14.3); a1.set_ylim(-0.3, 2.3); a1.axis("off"); a1.set_aspect("equal"); a1.set_title("Long blank corridor", fontsize=10)
x = np.linspace(-1, 1, 200); a2.plot(x, 0 * x + 0.05, color=RED, lw=2.5, label="along-track: flat valley")
a2.plot(x, x ** 2 * 3, color=TEAL, lw=2.5, label="across-track: sharp bowl"); a2.set_ylim(-0.2, 3); a2.set_xlabel("shift (m)"); a2.set_ylabel("matching error")
a2.legend(fontsize=7, frameon=False); a2.set_title("Error surface", fontsize=10); save(fig, "hallway")

# drift & loop closure
fig, ax = plt.subplots(figsize=(7, 3.6)); ax.set_aspect("equal")
t = np.linspace(0, 2 * np.pi, 300); tx, ty = 10 * np.cos(t), 5 * np.sin(t)
dr = np.c_[tx + 0.25 * t ** 1.8, ty + 0.2 * t ** 1.6]
ax.plot(tx, ty, color=GRAY, lw=4, alpha=.5, label="true path"); ax.plot(dr[:, 0], dr[:, 1], color=RED, lw=2, ls="--", label="drifting estimate")
w = (t / (2 * np.pi))[:, None]; corr = dr - w * (dr[-1] - np.array([tx[-1], ty[-1]])); ax.plot(corr[:, 0], corr[:, 1], color=TEAL, lw=2, label="after loop closure")
ax.annotate("", (tx[-1], ty[-1]), dr[-1], arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=2)); ax.text(dr[-1][0] - 3.6, dr[-1][1] + 1.5, "loop closure:\n'I've been here!'", color=PURPLE, fontsize=9)
ax.plot([10], [0], "*", ms=14, color=GOLD, mec="k"); ax.legend(fontsize=8, frameon=False, loc="center"); ax.axis("off")
save(fig, "loop")

# factor graph
fig, ax = blank(8.5, 3)
xs = np.arange(5) * 1.8
for i, x in enumerate(xs):
    ax.add_patch(Circle((x, 1), 0.33, fc="#d6eaf8", ec=NAVY, lw=2)); ax.text(x, 1, f"x{i}", ha="center", va="center", weight="bold")
    if i < 4:
        ax.plot([x + 0.33, x + 1.47], [1, 1], color="k"); ax.add_patch(Rectangle((x + 0.8, 0.88), 0.22, 0.22, fc=ORANGE))
        ax.plot([x + 0.2, x + 1.6], [0.7, 0.7], color="k", lw=0.8); ax.add_patch(Rectangle((x + 0.8, 0.6), 0.2, 0.2, fc=TEAL))
for i in (1, 3):
    ax.plot([xs[i], xs[i]], [1.33, 1.9], color="k"); ax.add_patch(Rectangle((xs[i] - 0.11, 1.9), 0.22, 0.22, fc=GOLD))
ax.plot([xs[0], xs[0], xs[4], xs[4]], [0.67, -0.1, -0.1, 0.67], color="k", lw=0.8); ax.add_patch(Rectangle((xs[2] - 0.11, -0.21), 0.22, 0.22, fc=PURPLE))
for (c, lab), yy in zip([(ORANGE, "IMU preintegration factor"), (TEAL, "LiDAR odometry factor"), (GOLD, "GPS / control factor"), (PURPLE, "loop-closure factor")], [2.3, 1.9, 1.5, 1.1]):
    ax.add_patch(Rectangle((8.2, yy), 0.2, 0.2, fc=c)); ax.text(8.5, yy + 0.1, lab, va="center", fontsize=8)
ax.set_xlim(-0.5, 11.5); ax.set_ylim(-0.4, 2.6); save(fig, "factorgraph")

# 1D factor graph example
fig, ax = blank(8.5, 2.2)
vals = [0, 1.05, 2.2, 3.15]
for i, v in enumerate(vals):
    ax.add_patch(Circle((i * 2.4, 0.8), 0.38, fc="#d6eaf8", ec=NAVY, lw=2)); ax.text(i * 2.4, 0.8, f"x{i}\n{v:.2f}", ha="center", va="center", fontsize=8)
for i, z in enumerate([1.0, 1.1, 0.9]):
    ax.plot([i * 2.4 + 0.38, i * 2.4 + 2.02], [0.8, 0.8], "k"); ax.add_patch(Rectangle((i * 2.4 + 1.1, 0.7), 0.2, 0.2, fc=TEAL)); ax.text(i * 2.4 + 1.2, 1.05, f"odo {z}", ha="center", fontsize=8)
ax.plot([7.2, 7.2], [1.18, 1.6], "k"); ax.add_patch(Rectangle((7.1, 1.6), 0.2, 0.2, fc=GOLD)); ax.text(7.5, 1.7, "GPS says 3.2", fontsize=8)
ax.add_patch(Rectangle((-0.1, 1.25), 0.2, 0.2, fc=GRAY)); ax.text(0.2, 1.4, "prior x0 = 0", fontsize=8)
ax.text(3.6, 0.0, "odometry adds to 3.0, GPS says 3.2 -> share the 0.2 m disagreement", ha="center", fontsize=8.5, color=RED)
ax.set_xlim(-0.6, 9); ax.set_ylim(-0.2, 2.0); save(fig, "fg1d")

# keyframes sliding window
fig, ax = blank(8.5, 2.3)
for i in range(12):
    c = NAVY if i >= 7 and i < 11 else ("#bdc3c7" if i < 7 else RED)
    ax.add_patch(Rectangle((i * 0.7, 0.4), 0.5, 0.7, fc=c, ec="k"))
ax.text(11 * 0.7 + 0.25, 1.25, "new\nkeyframe", ha="center", fontsize=8, color=RED)
ax.add_patch(FancyBboxPatch((7 * 0.7 - 0.08, 0.3), 4 * 0.7 - 0.05, 0.9, boxstyle="round,pad=0.02", fill=False, ec=ORANGE, lw=2, ls="--"))
ax.text(8.4 * 0.7 + 0.2, 0.05, "local map = last n sub-keyframes", ha="center", fontsize=8, color=ORANGE)
ax.text(2.4, 0.05, "old keyframes: kept in graph, not re-matched", ha="center", fontsize=8, color=GRAY)
arrow(ax, (11 * 0.7, 0.75), (10 * 0.7 + 0.55, 0.75), RED, lw=1.5, ms=10)
ax.set_xlim(-0.2, 8.6); ax.set_ylim(-0.1, 1.7); save(fig, "keyframes")

# control vs checkpoints map
fig, ax = plt.subplots(figsize=(7, 3.2)); ax.set_aspect("equal")
t = np.linspace(0, 1, 200); ax.plot(t * 100, 8 * np.sin(t * 6), color=GRAY, lw=12, alpha=.3)
ax.plot(t * 100, 8 * np.sin(t * 6), color=NAVY, lw=1.5, ls="--")
ctl = [(0, 0), (33, 7.5), (66, -6.5), (100, -2)]; chk = [(16, 6), (50, 1.3), (83, -7.5), (25, 9.5), (75, -4)]
for p in ctl: ax.plot(*p, "^", ms=11, color=RED, mec="k")
for p in chk: ax.plot(*p, "s", ms=9, color=TEAL, mec="k")
ax.plot([], [], "^", color=RED, label="control (used to adjust)"); ax.plot([], [], "s", color=TEAL, label="checkpoint (held out to test)")
ax.legend(fontsize=8, frameon=False, loc="lower left", ncol=2, bbox_to_anchor=(0, -0.3)); ax.axis("off"); ax.set_title("Corridor survey: alternate control and checkpoints", fontsize=10)
save(fig, "control")

# residual bars
dz = np.array([0.021, -0.034, 0.012, 0.045, -0.008, 0.027, -0.019, 0.031, 0.004, -0.026])
fig, ax = plt.subplots(figsize=(6.8, 2.8))
ax.bar(range(1, 11), dz * 100, color=[TEAL if v > 0 else ORANGE for v in dz]); ax.axhline(0, color="k", lw=.8)
ax.axhline(2.56, color=RED, ls="--"); ax.axhline(-2.56, color=RED, ls="--"); ax.text(10.6, 2.7, "±RMSE\n2.56 cm", color=RED, fontsize=8)
ax.set_xticks(range(1, 11)); ax.set_xlabel("checkpoint"); ax.set_ylabel("LiDAR − survey (cm)"); ax.set_title("Vertical checkpoint residuals"); save(fig, "residuals")

# error budget
fig, ax = plt.subplots(figsize=(6.8, 3))
names = ["range +\nangle", "lever arm +\nboresight", "trajectory\n(SLAM)", "timing", "control /\ngeoref", "RSS\nTOTAL"]
vals = [2.0, 1.5, 3.0, 0.5, 1.5, 4.21]
ax.bar(names, vals, color=[SKY, ORANGE, RED, GRAY, TEAL, NAVY]); ax.axhline(5, color="k", ls="--"); ax.text(5.45, 5.15, "spec 5 cm", fontsize=8, ha="right")
for i, v in enumerate(vals): ax.text(i, v + 0.1, f"{v:.1f}", ha="center", fontsize=9)
ax.set_ylabel("1σ contribution (cm)"); ax.set_ylim(0, 6); ax.set_title("Error budget: total is NOT the sum (2+1.5+3+0.5+1.5 = 8.5)"); ax.tick_params(axis="x", labelsize=8)
save(fig, "budget")

# SOR
fig, ax = plt.subplots(figsize=(6.5, 3))
x = rng.uniform(0, 10, 400); y = 0.1 * np.sin(x) + 0.03 * rng.standard_normal(400); ox = rng.uniform(0, 10, 15); oy = rng.uniform(0.6, 2.5, 15)
ax.plot(x, y, ".", color=NAVY, ms=3, label="kept"); ax.plot(ox, oy, "x", color=RED, ms=7, mew=2, label="removed: far from neighbors (birds, dust, rain)")
ax.legend(fontsize=8, frameon=False, loc="upper left"); ax.set_xlabel("m"); ax.set_ylabel("height (m)"); ax.set_ylim(-0.5, 3.2); ax.set_title("Statistical outlier removal"); save(fig, "sor")

# voxel
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3))
pts = np.vstack([rng.normal([2, 2], 0.6, (500, 2)), rng.normal([5, 4], 0.4, (300, 2))])
a1.plot(pts[:, 0], pts[:, 1], ".", ms=2, color=NAVY); a1.set_title(f"{len(pts)} points", fontsize=10)
keys = np.floor(pts / 0.5); u, inv = np.unique(keys, axis=0, return_inverse=True); cen = np.array([pts[inv.ravel() == k].mean(0) for k in range(len(u))])
for a in (a1, a2):
    for g in np.arange(0, 7.01, 0.5): a.axvline(g, color=GRAY, lw=.3); a.axhline(g, color=GRAY, lw=.3)
    a.set_xlim(0, 7); a.set_ylim(0, 6); a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
a2.plot(cen[:, 0], cen[:, 1], "o", ms=3, color=ORANGE); a2.set_title(f"{len(cen)} voxel centroids (0.5 m)", fontsize=10); save(fig, "voxel")

# ground & DTM
fig, ax = plt.subplots(figsize=(7.5, 2.8))
x = np.linspace(0, 40, 800); gnd = 0.5 * np.sin(x / 7) + 0.02 * x
ax.plot(x, gnd + 0.03 * rng.standard_normal(800), ".", ms=2, color="#8d6e63", label="ground")
for cx in (8, 22, 31):
    m = 60; ax.plot(rng.uniform(cx - 1.5, cx + 1.5, m), np.interp(cx, x, gnd) + rng.uniform(1.5, 4, m), ".", ms=3, color="#27ae60")
ax.add_patch(Rectangle((14, np.interp(14, x, gnd)), 4, 1.5, fc=GRAY, alpha=.6)); ax.text(16, np.interp(14, x, gnd) + 1.7, "car", ha="center", fontsize=8)
ax.plot(x, gnd, color=RED, lw=1.5, label="DTM surface (bare earth)")
ax.legend(fontsize=8, frameon=False, loc="upper left"); ax.set_xlabel("distance (m)"); ax.set_ylabel("elev (m)"); ax.set_title("Ground classification -> bare-earth surface"); save(fig, "ground")

# volume grid
fig = plt.figure(figsize=(5.5, 3.6)); ax = fig.add_subplot(111, projection="3d")
Z = np.array([[1.2, 1.5, 1.1], [1.8, 2.4, 1.6], [1.0, 1.3, 0.9]])
for i in range(3):
    for j in range(3):
        ax.bar3d(i * 2, j * 2, 0, 1.9, 1.9, Z[i, j], color=plt.cm.YlOrBr(Z[i, j] / 2.6), alpha=.85, edgecolor="k", lw=.3)
        ax.text(i * 2 + 1, j * 2 + 1, Z[i, j] + 0.15, f"{Z[i,j]}", fontsize=7, ha="center")
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.set_zlabel("height (m)"); ax.set_title("Stockpile on a 2 m grid", fontsize=10); ax.view_init(28, -55)
save(fig, "volume")

# workflow
fig, ax = blank(9, 2.6)
steps = ["Plan +\nerror budget", "Set control\n& checkpoints", "Calibrate +\nwarm-up", "Collect\n(steady speed)", "Trajectory\n(SLAM+GNSS)", "Clean +\nclassify", "QA/QC\nreport", "CAD /\nCivil 3D"]
for i, s in enumerate(steps):
    r, c = divmod(i, 4); x = c * 2.25; y = 1.3 - r * 1.3
    box(ax, (x, y), 1.8, 0.9, s, fc=[SKY, TEAL, ORANGE, RED, PURPLE, GOLD, NAVY, "#2e4053"][i], ec="k", fs=8, tc="w")
    if c < 3: arrow(ax, (x + 1.8, y + 0.45), (x + 2.25, y + 0.45), "k", lw=1.2, ms=10)
arrow(ax, (3 * 2.25 + 0.9, 1.3), (0.9, 1.0), "k", lw=1.2, ms=10, connectionstyle="arc3,rad=0")
ax.set_xlim(-0.1, 9); ax.set_ylim(-0.1, 2.3); save(fig, "workflow")

# cloud to cloud diff heatmap
fig, ax = plt.subplots(figsize=(7, 2.5))
xx, yy = np.meshgrid(np.linspace(0, 200, 200), np.linspace(-6, 6, 30)); dd = 0.01 * rng.standard_normal(xx.shape) + 0.03 * np.exp(-((xx - 140) / 25) ** 2)
im = ax.imshow(dd * 100, extent=[0, 200, -6, 6], aspect="auto", cmap="RdBu_r", vmin=-4, vmax=4); fig.colorbar(im, ax=ax, label="strip A − strip B (cm)")
ax.set_xlabel("along road (m)"); ax.set_ylabel("across (m)"); ax.set_title("Cloud-to-cloud check: a 3 cm hot spot near 140 m = trajectory problem"); save(fig, "c2c")
print("figs3 done")

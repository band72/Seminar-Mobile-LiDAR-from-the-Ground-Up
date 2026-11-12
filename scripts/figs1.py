from style import *
rng = np.random.default_rng(7)

# ---------- cover: synthetic street point cloud ----------
def street_cloud(n=60000):
    pts = []
    # road
    x = rng.uniform(0, 60, n // 3); y = rng.uniform(-5, 5, n // 3); z = 0.02 * rng.standard_normal(n // 3) + 0.01 * np.abs(y)
    pts.append(np.c_[x, y, z])
    # sidewalks/curbs
    for side in (-1, 1):
        x = rng.uniform(0, 60, n // 10); y = side * rng.uniform(5.15, 8, n // 10); z = 0.15 + 0.01 * rng.standard_normal(n // 10)
        pts.append(np.c_[x, y, z])
    # building facades
    for side in (-1, 1):
        m = n // 6
        x = rng.uniform(0, 60, m); y = side * (8 + 0.03 * rng.standard_normal(m)); z = rng.uniform(0, 9 + 3 * (np.sin(x / 6) > 0), m)
        pts.append(np.c_[x, y, z])
    # poles + trees
    for px in np.arange(4, 60, 10):
        for side in (-1, 1):
            m = 400; t = rng.uniform(0, 2 * np.pi, m)
            pts.append(np.c_[px + 0.12 * np.cos(t), side * 6.2 + 0.12 * np.sin(t), rng.uniform(0, 6, m)])
            m = 700; u = rng.standard_normal((m, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
            r = 1.4 * rng.uniform(0.7, 1, m)[:, None]
            pts.append(np.c_[px + 5, side * 6.8, 4.5] + u * r)
    return np.vstack(pts)

P = street_cloud()
BG = "#1a3263"
fig = plt.figure(figsize=(8.5, 5.5), facecolor=BG); ax = fig.add_axes([-0.15, -0.25, 1.3, 1.5], projection="3d", facecolor=BG)
ax.scatter(P[:, 0], P[:, 1], P[:, 2], c=P[:, 2], cmap="turbo", vmin=-3, vmax=10, s=0.7, linewidths=0)
ax.view_init(elev=24, azim=-58); ax.set_box_aspect((60, 16, 10), zoom=1.1); ax.axis("off")
ax.set_xlim(0, 60); ax.set_ylim(-8, 8); ax.set_zlim(0, 10)
fig.savefig("figs/cover.png", dpi=250, facecolor=BG); plt.close(fig)
fig = plt.figure(figsize=(10, 6)); ax = fig.add_axes([-0.15, -0.25, 1.3, 1.5], projection="3d")
ax.scatter(P[:, 0], P[:, 1], P[:, 2], c=P[:, 2], cmap="turbo", s=0.5, linewidths=0)
ax.view_init(elev=24, azim=-58); ax.set_box_aspect((60, 16, 10), zoom=1.4); ax.axis("off")
fig.savefig("figs/pointcloud.png", dpi=220); plt.close(fig)

# ---------- LiDAR family ----------
fig, axs = plt.subplots(1, 4, figsize=(9, 2.6))
titles = ["Airborne", "Terrestrial (tripod)", "Mobile (vehicle)", "Backpack / handheld"]
for ax, t in zip(axs, titles):
    ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(t, fontsize=9)
    ax.plot([0, 4], [0.3, 0.3], color="#6e4b2a", lw=3)
ax = axs[0]
ax.add_patch(Polygon([[1, 3.3], [3, 3.3], [3.3, 3.5], [0.8, 3.5]], fc=NAVY))
for x in np.linspace(0.6, 3.4, 6): ax.plot([2, x], [3.3, 0.35], color=RED, lw=0.8, alpha=0.7)
ax = axs[1]
ax.plot([1.6, 2, 2.4], [0.3, 1.6, 0.3], color="k", lw=1.5); ax.plot([2, 2], [0.3, 1.6], "k", lw=1.5)
ax.add_patch(Rectangle((1.8, 1.6), 0.4, 0.5, fc=ORANGE, ec="k"))
for a in np.linspace(-0.6, 1.0, 7): ax.plot([2, 2 + 2 * np.cos(a)], [1.85, 1.85 + 2 * np.sin(a)], color=RED, lw=0.8, alpha=.7)
ax = axs[2]; car(ax, 2, 0.55, 0.9)
for a in np.linspace(0.2, 2.9, 8): ax.plot([2, 2 + 2 * np.cos(a)], [1.75, 1.75 + 2 * np.sin(a)], color=RED, lw=0.8, alpha=.7)
ax = axs[3]
ax.add_patch(Circle((2, 2.4), 0.25, fc="#f0c27b", ec="k")); ax.plot([2, 2], [2.15, 1.1], "k", lw=3)
ax.plot([2, 1.7], [1.1, 0.3], "k", lw=3); ax.plot([2, 2.3], [1.1, 0.3], "k", lw=3)
ax.add_patch(Rectangle((1.55, 1.3), 0.35, 0.7, fc=NAVY, ec="k")); ax.add_patch(Rectangle((1.6, 2.0), 0.25, 0.9, fc="#444")); ax.add_patch(Rectangle((1.55, 2.9), 0.35, 0.2, fc=ORANGE, ec="k"))
for a in np.linspace(-0.3, 3.4, 8): ax.plot([1.72, 1.72 + 1.6 * np.cos(a)], [3.0, 3.0 + 1.6 * np.sin(a)], color=RED, lw=0.7, alpha=.6)
save(fig, "family")

# ---------- Time of flight ----------
fig, ax = blank(8, 3.2)
ax.set_xlim(0, 12); ax.set_ylim(-0.5, 4)
ax.add_patch(FancyBboxPatch((0.2, 1.2), 1.4, 1.2, boxstyle="round,pad=0.05", fc=NAVY, ec="k"))
ax.text(0.9, 1.8, "LiDAR", color="w", ha="center", va="center", weight="bold")
ax.add_patch(Rectangle((10.8, 0), 0.5, 3.6, fc="#b8977e", ec="k", hatch="//")); ax.text(11.05, 3.8, "Wall", ha="center")
xs = np.linspace(1.8, 10.6, 400)
ax.plot(xs, 2.6 + 0.12 * np.sin(xs * 9), color=RED, lw=1.8); arrow(ax, (9.8, 2.6), (10.7, 2.6), RED)
ax.plot(xs, 1.0 + 0.12 * np.sin(xs * 9), color=ORANGE, lw=1.8); arrow(ax, (2.6, 1.0), (1.7, 1.0), ORANGE)
ax.text(6.2, 3.05, "1. pulse goes OUT", ha="center", color=RED, weight="bold")
ax.text(6.2, 0.35, "2. echo comes BACK", ha="center", color=ORANGE, weight="bold")
ax.annotate("", (1.6, -0.3), (10.8, -0.3), arrowprops=dict(arrowstyle="<->", color="k"))
ax.text(6.2, -0.55, "distance d  (we want this)", ha="center", va="top")
save(fig, "tof")

fig, ax = plt.subplots(figsize=(6.5, 3))
t_ns = np.linspace(0, 10, 200); ax.plot(t_ns, 0.1499 * t_ns * 100, color=NAVY, lw=2.5)
for tt in (0.1, 1, 3.3):
    ax.plot(tt, 14.99 * tt, "o", color=RED); ax.annotate(f"{tt:g} ns -> {14.99*tt:.1f} cm", (tt, 14.99 * tt), (tt + 0.5, 14.99 * tt - 18), fontsize=9, arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("Timing error  (nanoseconds)"); ax.set_ylabel("Range error  (cm)"); ax.set_title("Every 1 ns of clock error = 15 cm of distance error")
ax.grid(alpha=.3); save(fig, "timing_error")

# pulse ambiguity
fig, ax = plt.subplots(figsize=(7.5, 2.6))
for k in range(4):
    ax.add_patch(Rectangle((k * 1.0, 0), 0.04, 1, color=NAVY))
    ax.add_patch(Rectangle((k * 1.0 + 0.6, 0), 0.04, 0.45, color=ORANGE))
ax.set_xlim(-0.1, 4); ax.set_ylim(0, 1.4); ax.set_yticks([]); ax.set_xlabel("time  (microseconds, PRF = 1 MHz)")
ax.annotate("", (0, 1.15), (1, 1.15), arrowprops=dict(arrowstyle="<->")); ax.text(0.5, 1.22, "1 µs between shots", ha="center", fontsize=9)
ax.text(0.68, 0.3, "echo of\nshot 1", color=ORANGE, fontsize=8)
ax.text(2.08, 0.62, "is this shot 2's echo\nor shot 1 from far away?", color=RED, fontsize=8)
ax.set_title("Range ambiguity: the next pulse leaves before a far echo returns")
save(fig, "ambiguity")

# phase shift
fig, ax = plt.subplots(figsize=(7, 2.8))
x = np.linspace(0, 4 * np.pi, 500)
ax.plot(x, np.sin(x), color=NAVY, lw=2, label="sent wave")
ax.plot(x, 0.6 * np.sin(x - np.pi / 2), color=ORANGE, lw=2, label="returned wave (weaker, shifted)")
ax.annotate("", (np.pi / 2, 1.1), (np.pi, 1.1), arrowprops=dict(arrowstyle="<->", color=RED))
ax.text(3 * np.pi / 4, 1.2, r"$\Delta\varphi = 90^\circ$", ha="center", color=RED)
ax.set_ylim(-1.3, 1.5); ax.set_yticks([]); ax.set_xticks([]); ax.legend(loc="lower right", fontsize=8, frameon=False)
ax.set_title("Phase-shift ranging: measure how far the wave has slid")
save(fig, "phase")

# multi-return
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3.3), gridspec_kw=dict(width_ratios=[1, 1.4]))
a1.set_xlim(-2, 2); a1.set_ylim(0, 10); a1.axis("off"); a1.set_aspect("equal")
a1.add_patch(Polygon([[-0.15, 10], [0.15, 10], [0.9, 0], [-0.9, 0]], fc=RED, alpha=0.15))
a1.add_patch(Ellipse((0.3, 5.5), 2.6, 2.4, fc="#27ae60", alpha=.7)); a1.plot([0.2, 0.2], [0, 4.5], color="#6e4b2a", lw=5)
a1.add_patch(Ellipse((-0.2, 3), 1.5, 1.2, fc="#2ecc71", alpha=.6))
a1.plot([-2, 2], [0, 0], color="#6e4b2a", lw=3)
for yv, lab in [(6.6, "1st"), (3.5, "2nd"), (0.05, "last")]:
    a1.plot(0.6, yv, "o", color=ORANGE, ms=8); a1.text(1.0, yv, lab, va="center", fontsize=9)
a1.set_title("One pulse, three surfaces", fontsize=10)
t = np.linspace(0, 100, 600)
w = 0.8 * np.exp(-(t - 25) ** 2 / 8) + 0.45 * np.exp(-(t - 48) ** 2 / 10) + 1.0 * np.exp(-(t - 80) ** 2 / 6)
a2.plot(t, w, color=NAVY, lw=2); a2.fill_between(t, w, alpha=.15, color=NAVY)
for tp, lab in [(25, "canopy"), (48, "branch"), (80, "ground")]:
    a2.annotate(lab, (tp, 0.05 + w[np.argmin(abs(t - tp))]), (tp, 1.15), ha="center", arrowprops=dict(arrowstyle="->"), fontsize=9)
a2.set_xlabel("time after firing (ns)"); a2.set_ylabel("received power"); a2.set_ylim(0, 1.35); a2.set_title("Return waveform", fontsize=10)
save(fig, "multireturn")

# ---------- footprint ----------
fig, ax = plt.subplots(figsize=(7.5, 2.8))
R = np.linspace(0, 100, 50); D = 0.005 + 0.0003 * R
ax.fill_between(R, -D / 2 * 100, D / 2 * 100, color=RED, alpha=.25); ax.plot(R, D / 2 * 100, color=RED); ax.plot(R, -D / 2 * 100, color=RED)
for r in (10, 50, 100):
    d = (0.005 + 0.0003 * r) * 100; ax.plot([r, r], [-d / 2, d / 2], color="k"); ax.text(r, d / 2 + 0.3, f"{d:.1f} cm", ha="center", fontsize=9)
ax.set_xlabel("range (m)"); ax.set_ylabel("beam width (cm)"); ax.set_title("Beam divergence: the dot grows with distance (0.3 mrad)")
ax.set_ylim(-2.5, 2.8); save(fig, "footprint")

# inverse square & incidence
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3))
R = np.linspace(5, 100, 200); a1.plot(R, (10 / R) ** 2, color=NAVY, lw=2.5); a1.set_yscale("log")
a1.plot([10, 50], [1, 1 / 25], "o", color=RED); a1.annotate("25x weaker", (50, 0.04), (55, 0.2), arrowprops=dict(arrowstyle="->"))
a1.set_xlabel("range R (m)"); a1.set_ylabel("power relative to 10 m"); a1.set_title(r"Return power $\propto 1/R^2$"); a1.grid(alpha=.3, which="both")
th = np.linspace(0, 89, 100); a2.plot(th, np.cos(np.radians(th)), color=TEAL, lw=2.5); a2.plot(60, 0.5, "o", color=RED)
a2.annotate("60° -> half", (60, 0.5), (25, 0.25), arrowprops=dict(arrowstyle="->"))
a2.set_xlabel("incidence angle (deg)"); a2.set_ylabel(r"$\cos\theta$"); a2.set_title("Glancing hits return less light"); a2.grid(alpha=.3)
save(fig, "power")

# ---------- polar 3D ----------
fig = plt.figure(figsize=(5.5, 4.4)); ax = fig.add_subplot(111, projection="3d")
Rr, H, V = 25, np.radians(40), np.radians(15)
X, Y, Z = Rr * np.cos(V) * np.cos(H), Rr * np.cos(V) * np.sin(H), Rr * np.sin(V)
for v, c, l in [((22, 0, 0), "k", "X (forward)"), ((0, 20, 0), "k", "Y"), ((0, 0, 9), "k", "Z (up)")]:
    ax.quiver(0, 0, 0, *v, color=c, arrow_length_ratio=0.06, lw=1); ax.text(*np.array(v) * 1.08, l, fontsize=9)
ax.plot([0, X], [0, Y], [0, Z], color=RED, lw=3); ax.scatter([X], [Y], [Z], color=RED, s=40)
ax.plot([0, X], [0, Y], [0, 0], color=GRAY, ls="--"); ax.plot([X, X], [Y, Y], [0, Z], color=GRAY, ls="--")
ax.plot([X, X], [0, Y], [0, 0], color=TEAL, ls=":"); ax.plot([0, X], [Y, Y], [0, 0], color=TEAL, ls=":")
a = np.linspace(0, H, 30); ax.plot(6 * np.cos(a), 6 * np.sin(a), 0, color=NAVY, lw=2); ax.text(7, 3, 0, "H = 40°", color=NAVY)
b = np.linspace(0, V, 20); ax.plot(9 * np.cos(b) * np.cos(H), 9 * np.cos(b) * np.sin(H), 9 * np.sin(b), color=ORANGE, lw=2); ax.text(8, 7.5, 2.5, "V = 15°", color=ORANGE)
ax.text(X, Y, Z + 1, "point\n(18.50, 15.52, 6.47)", fontsize=8, color=RED)
ax.text(X / 2, Y / 2, Z / 2 + 1.5, "range 25 m", color=RED, fontsize=9)
ax.set_xlim(0, 22); ax.set_ylim(0, 20); ax.set_zlim(0, 9); ax.view_init(18, -60); ax.axis("off")
save(fig, "polar3d")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3.2))
for a in (a1, a2): a.set_aspect("equal"); a.axis("off")
a1.plot([0, 24.15], [0, 0], color=TEAL, lw=3); a1.plot([0, 24.15], [0, 6.47], color=RED, lw=3); a1.plot([24.15, 24.15], [0, 6.47], color=ORANGE, lw=3)
a1.text(12, -1.8, r"horizontal part = $R\cos V$ = 24.15", ha="center", color=TEAL); a1.text(25, 3, r"$Z=R\sin V$" + "\n= 6.47", color=ORANGE)
a1.text(9, 4.2, "R = 25", color=RED); a1.add_patch(Arc((0, 0), 10, 10, theta1=0, theta2=15, color="k")); a1.text(5.6, 0.6, "V", fontsize=10)
a1.set_title("Step A: side view (tilt)", fontsize=10); a1.set_xlim(-1, 32); a1.set_ylim(-3, 9)
a2.plot([0, 18.5], [0, 0], color=NAVY, lw=3); a2.plot([0, 18.5], [0, 15.52], color=TEAL, lw=3); a2.plot([18.5, 18.5], [0, 15.52], color=PURPLE, lw=3)
a2.text(9, -2.2, r"$X = 24.15\cos H$ = 18.50", ha="center", color=NAVY); a2.text(19, 7, r"$Y = 24.15\sin H$" + "\n= 15.52", color=PURPLE)
a2.add_patch(Arc((0, 0), 10, 10, theta1=0, theta2=40, color="k")); a2.text(5.5, 1.6, "H")
a2.set_title("Step B: top view (turn)", fontsize=10); a2.set_xlim(-1, 30); a2.set_ylim(-3.5, 17)
save(fig, "polar_steps")

# scanner patterns
fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(9, 3))
az = np.linspace(-np.pi, np.pi, 720)
for el in np.linspace(-15, 15, 16):
    a1.plot(np.degrees(az), np.full_like(az, el), ".", ms=0.8, color=NAVY)
a1.set_title("Spinning, 16 rings\n360° wide, fixed lines", fontsize=9); a1.set_xlabel("horizontal angle (°)"); a1.set_ylabel("vertical angle (°)")
t = np.linspace(0, 0.1, 20000); r = np.sin(2 * np.pi * 37 * t * 10) * 35; ang = 2 * np.pi * 11 * t * 10
a2.plot(r * np.cos(ang), r * np.sin(ang), lw=0.25, color=TEAL); a2.set_aspect("equal"); a2.set_title("Solid-state rosette\n(non-repeating)", fontsize=9); a2.set_xlabel("°")
xx, yy = np.meshgrid(np.linspace(-60, 60, 120), np.linspace(-12, 12, 40)); a3.plot(xx, yy, ".", ms=0.7, color=ORANGE)
a3.set_title("Solid-state raster / flash\n(forward-looking)", fontsize=9); a3.set_xlabel("°")
save(fig, "patterns")

# point spacing along road
fig, ax = plt.subplots(figsize=(7.5, 3))
ax.add_patch(Rectangle((0, -4), 12, 8, fc="#d5d8dc"))
for k, xs in enumerate(np.arange(0.5, 12, 1.5)):
    yy = np.linspace(-4, 4, 40); ax.plot(np.full_like(yy, xs) + 0.04 * yy, yy, ".", ms=2.5, color=NAVY)
ax.annotate("", (2.0, 4.4), (3.5, 4.4), arrowprops=dict(arrowstyle="<->")); ax.text(2.75, 4.6, "1.5 m", ha="center")
ax.annotate("", (12.4, 0), (12.4, 0.2), arrowprops=dict(arrowstyle="<->")); ax.text(12.6, 0, "across-track\nspacing = R·Δθ", fontsize=8, va="center")
car(ax, -1.5, -0.4, 0.8); ax.set_xlim(-3.5, 15); ax.set_ylim(-4.5, 5.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("At 15 m/s a 10 Hz scanner lays a new line every 1.5 m", fontsize=10)
save(fig, "spacing")
print("figs1 done")

from style import *
rng = np.random.default_rng(21)
d = np.deg2rad

# 1. propagation chain
fig, ax = blank(9, 1.9)
items = [("input errors\n" + r"$\sigma_\rho$, $\sigma_H$, $\sigma_V$, pose", SKY),
         ("model\n" + r"$\mathbf{y}=f(\mathbf{x})$", ORANGE),
         ("sensitivities\n" + r"Jacobian $\mathbf{J}=\partial f/\partial\mathbf{x}$", TEAL),
         ("output covariance\n" + r"$\Sigma_y=\mathbf{J}\Sigma_x\mathbf{J}^T$", NAVY)]
for i, (t, c) in enumerate(items):
    box(ax, (i * 2.35, 0), 2.0, 1.0, t, fc=c, ec="k", fs=9, tc="w" if c in (NAVY, TEAL) else "#111")
    if i < 3: arrow(ax, (i * 2.35 + 2.0, 0.5), (i * 2.35 + 2.35, 0.5), "k", lw=1.3, ms=11)
ax.set_xlim(-0.1, 9.2); ax.set_ylim(-0.1, 1.1); save(fig, "ep_chain")

# 2. linearization
fig, ax = plt.subplots(figsize=(6.4, 4.2))
x = np.linspace(0, 1.6, 300); f = lambda t: 20 * np.sin(t)
x0 = 0.6; s = 0.08
ax.plot(x, f(x), color=NAVY, lw=2.5, label=r"true model $z=\rho\sin V$ ($\rho=20$ m)")
ax.plot(x, f(x0) + 20 * np.cos(x0) * (x - x0), color=RED, ls="--", lw=1.8, label="tangent line (linearization)")
g = np.exp(-(x - x0) ** 2 / (2 * s * s)); ax.fill_between(x, 0, 3 * g, color=ORANGE, alpha=.4, label=r"input spread $\sigma_V$")
zz = np.linspace(0, 20, 400); sz = 20 * np.cos(x0) * s; gz = np.exp(-(zz - f(x0)) ** 2 / (2 * sz * sz))
ax.fill_betweenx(zz, 0, 0.25 * gz, color=TEAL, alpha=.45, label=r"output spread $\sigma_z=|dz/dV|\,\sigma_V$")
ax.plot([x0, x0], [0, f(x0)], color=GRAY, ls=":"); ax.plot([0, x0], [f(x0), f(x0)], color=GRAY, ls=":")
ax.set_xlabel("input  V  (rad)"); ax.set_ylabel("output  z  (m)"); ax.set_xlim(0, 1.6); ax.set_ylim(0, 21)
ax.legend(fontsize=7.5, frameon=False, loc="lower right"); ax.set_title("The slope of the model scales the input error")
save(fig, "ep_linear")

# 3. horizontal error ellipse at 30 m
C = np.array([[81.58, 31.34], [31.34, 45.39]])
fig, ax = plt.subplots(figsize=(5.8, 4.3)); ax.set_aspect("equal")
w, V = np.linalg.eigh(C); ang = np.degrees(np.arctan2(V[1, 1], V[0, 1]))
for k, c, lab in [(2.4477, TEAL, "95% ellipse (x 2.448)"), (1, NAVY, "1-sigma ellipse")]:
    ax.add_patch(Ellipse((0, 0), 2 * k * np.sqrt(w[1]), 2 * k * np.sqrt(w[0]), angle=ang, fc=c, alpha=.25, ec=c, lw=2, label=lab))
ax.plot([-30, 30], [-30 * np.tan(d(30)), 30 * np.tan(d(30))], color=RED, ls="--", lw=1.2, label="laser beam direction (H = 30°)")
ax.set_xlim(-30, 30); ax.set_ylim(-22, 22); ax.set_xlabel("x error (mm)"); ax.set_ylabel("y error (mm)"); ax.grid(alpha=.3)
ax.legend(fontsize=8, frameon=False, loc="lower right"); ax.set_title("Point at 30 m: long along the beam, narrow across it", fontsize=10)
save(fig, "ep_ellipse")

# 4. Monte Carlo histogram
dz = np.load("figs/mc_dz.npy") * 100
fig, ax = plt.subplots(figsize=(6.6, 3.0))
ax.hist(dz, bins=80, density=True, color=SKY, alpha=.7, label="100,000 Monte Carlo points")
xx = np.linspace(-9, 9, 300); sg = 2.18
ax.plot(xx, np.exp(-xx ** 2 / (2 * sg * sg)) / (sg * np.sqrt(2 * np.pi)), color=RED, lw=2.5, label="linear propagation, σ = 2.18 cm")
ax.set_xlabel("vertical error of a point 20 m away (cm)"); ax.set_yticks([]); ax.legend(fontsize=8, frameon=False)
ax.set_title("Two methods, one answer: simulation agrees with the Jacobian"); save(fig, "ep_mc")

# 5. budget vs range (horizontal), quadrature contributions
r = np.linspace(1, 35, 200)
rr = np.array([1, 5, 10, 15, 20, 25, 30, 35.]); pc = np.array([0.25, 0.25, 0.25, 0.28, 0.40, 0.65, 1.0, 1.5])
prec = np.interp(r, rr, pc)
terms = {"trajectory position": np.full_like(r, 2.12), "attitude (yaw 0.05°)": r * d(0.05) * 100,
         "range accuracy + precision": np.hypot(1.25, prec), "boresight 0.01°": r * d(0.01) * 100,
         "angle encoders 0.01°": r * d(0.01) * 100, "lever arm": np.full_like(r, 0.28)}
cols = [GRAY, RED, NAVY, ORANGE, PURPLE, TEAL]
fig, ax = plt.subplots(figsize=(7.2, 3.6))
for (k, v), c in zip(terms.items(), cols): ax.plot(r, v, color=c, lw=2, label=k)
tot = np.sqrt(sum(v ** 2 for v in terms.values())); ax.plot(r, tot, color="k", lw=3, label="TOTAL (root-sum-square)")
ax.set_xlabel("range (m)"); ax.set_ylabel("horizontal 1σ (cm)"); ax.grid(alpha=.3); ax.legend(fontsize=7.5, frameon=False, ncol=2, loc="upper left")
ax.set_ylim(0, 7.5); ax.set_title("Backpack with an OS0: which error wins at each range?"); save(fig, "ep_budget_range")

# 6. correlated errors (curb height)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 2.9))
for a, shift, ttl in [(a1, True, "Absolute heights: shared bias shows"), (a2, False, "Height difference: shared bias cancels")]:
    a.plot([0, 2], [0.15, 0.15], color="k", lw=3); a.plot([2, 2], [0.15, 0], color="k", lw=3); a.plot([2, 4], [0, 0], color="k", lw=3)
    b = 0.0125 if shift else 0
    a.plot([0, 2], [0.15 + b, 0.15 + b], color=RED, lw=2, ls="--"); a.plot([2, 4], [b, b], color=RED, lw=2, ls="--")
    a.annotate("", (3.2, 0), (3.2, b + 0.0001), arrowprops=dict(arrowstyle="<->", color=RED)) if shift else None
    a.annotate("", (2.6, 0 + b), (2.6, 0.15 + b), arrowprops=dict(arrowstyle="<->", color=TEAL, lw=2)); a.text(2.7, 0.07, "curb\nheight", color=TEAL, fontsize=8)
    a.set_title(ttl, fontsize=10); a.set_ylim(-0.03, 0.22); a.set_xticks([]); a.set_ylabel("m")
a1.text(3.3, 0.02, "bias\n1.25 cm", color=RED, fontsize=8)
save(fig, "ep_corr")

# 7. averaging floor
n = np.logspace(0, 4, 200)
fig, ax = plt.subplots(figsize=(6.6, 2.9))
ax.plot(n, 0.25 / np.sqrt(n), color=TEAL, lw=2, label=r"random part $\sigma/\sqrt{n}$")
ax.plot(n, np.full_like(n, 1.25), color=RED, lw=2, ls="--", label="systematic bias (does not average out)")
ax.plot(n, np.sqrt(1.25 ** 2 + 0.0625 / n), color="k", lw=2.5, label="total RMSE")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("number of points averaged (n)"); ax.set_ylabel("cm"); ax.grid(alpha=.3, which="both")
ax.legend(fontsize=8, frameon=False); ax.set_title("Averaging beats noise, never bias"); save(fig, "ep_avg")

# 8. OS0 point spacing
r = np.linspace(0.5, 35, 200)
fig, ax = plt.subplots(figsize=(7.2, 3.8))
for N, c in [(512, RED), (1024, ORANGE), (2048, TEAL), (4096, NAVY)]:
    ax.plot(r, r * d(360 / N) * 100, color=c, lw=2, label=f"horizontal, {N} columns ({360/N:.3f}°)")
ax.plot(r, r * d(90 / 127) * 100, color=PURPLE, lw=2.5, ls="-.", label="vertical, 128 channels (0.709°)")
ax.plot(r, (0.005 + r * d(0.35)) * 100, color="k", lw=2, ls="--", label="beam footprint, 0.35° FWHM")
ax.set_xlabel("range (m)"); ax.set_ylabel("spacing / spot size (cm)"); ax.set_ylim(0, 45); ax.grid(alpha=.3)
ax.legend(fontsize=7.5, frameon=False, loc="upper left"); ax.set_title("Ouster OS0 Rev8: point spacing versus beam size")
save(fig, "os0_spacing")

# 9. OS0 precision/accuracy
r = np.linspace(1, 35, 200)
fig, ax = plt.subplots(figsize=(7.2, 3.6))
p10 = np.interp(r, rr, pc)
ax.plot(r, p10, color=ORANGE, lw=2.5, ls=":", label="precision, 10% target (1σ)")
ax.plot(r, np.full_like(r, 0.25), color=TEAL, lw=2, ls="--", label="precision, 90% target")
ax.plot(r, np.full_like(r, 1.0), color=PURPLE, lw=2, label="precision, retroreflector")
ax.plot(r, np.full_like(r, 1.25), color=RED, lw=1.5, ls="-.", label="accuracy (bias), Lambertian ±1.25 cm")
ax.plot(r, np.full_like(r, 2.5), color=GRAY, lw=1.5, ls="-.", label="accuracy (bias), retroreflector ±2.5 cm")
ax.plot(r, np.hypot(1.25, p10), color="k", lw=3, label="total range error, 10% target")
ax.set_xlabel("target distance (m)"); ax.set_ylabel("cm"); ax.set_ylim(0, 4.2); ax.grid(alpha=.3)
ax.legend(fontsize=7.5, frameon=False, loc="upper left", ncol=2); ax.set_title("OS0 Rev8 range error (values read from the datasheet charts)")
save(fig, "os0_range")

# 10. beam overlap at 20 m
fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.5, 2.8))
fp = (0.005 + 20 * d(0.35)) * 100
for a, N, ttl in [(a1, 1024, "1024 columns: samples 12.3 cm apart, spots 12.7 cm wide (just touching)"),
                  (a2, 4096, "4096 columns: samples 3.1 cm apart, spots still 12.7 cm wide (4x overlap)")]:
    sp = 20 * d(360 / N) * 100
    for k in range(int(70 // sp) + 1):
        a.add_patch(Circle((k * sp, 0), fp / 2, fc=ORANGE, alpha=.18, ec=ORANGE)); a.plot(k * sp, 0, "k.", ms=3)
    a.set_xlim(-8, 75); a.set_ylim(-8, 8); a.set_aspect("equal"); a.axis("off"); a.set_title(ttl, fontsize=8.5)
save(fig, "os0_beams")

# 11. clock drift
t = np.linspace(0, 600, 200)
fig, ax = plt.subplots(figsize=(6.8, 2.9))
for v, c, lab in [(1.5, TEAL, "walking 1.5 m/s"), (15, RED, "driving 15 m/s")]:
    ax.plot(t / 60, 20e-6 * t * v * 100, color=c, lw=2.5, label=f"free-running clock (20 ppm), {lab}")
    ax.axhline(1e-3 * v * 100, color=c, ls="--", lw=1.2)
ax.text(6.2, 2.2, "PTP/PPS-synced bound (1 ms), driving", fontsize=8, color=RED); ax.text(6.2, -1.0, "synced bound, walking (0.15 cm)", fontsize=8, color=TEAL); ax.set_ylim(-1.6, 19)
ax.set_xlabel("minutes since last sync"); ax.set_ylabel("along-track error (cm)"); ax.grid(alpha=.3); ax.legend(fontsize=8, frameon=False, loc="upper left")
ax.set_title("Why the OS0 must be time-synchronized"); save(fig, "os0_clock")
print("figs4 done")

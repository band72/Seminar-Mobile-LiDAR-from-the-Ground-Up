from style import *
rng = np.random.default_rng(3)

# radians / arc
fig, ax = blank(6, 3.2)
th = np.radians(50); ax.plot([0, 4], [0, 0], color=NAVY, lw=2); ax.plot([0, 4 * np.cos(th)], [0, 4 * np.sin(th)], color=NAVY, lw=2)
ax.add_patch(Arc((0, 0), 8, 8, theta1=0, theta2=50, color=RED, lw=4))
ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=0, theta2=50, color="k")); ax.text(0.95, 0.35, r"$\theta$", fontsize=13)
ax.text(2, -0.4, "radius r", ha="center", color=NAVY); ax.text(3.9, 2.0, r"arc $s = r\,\theta$", color=RED, fontsize=12)
ax.text(5.6, 3.3, "1 radian = the angle where\narc length equals radius\n= 57.2958°", fontsize=9, va="top")
ax.set_xlim(-0.3, 9); ax.set_ylim(-0.7, 3.6); save(fig, "radians")

# unit circle
fig, ax = blank(4.2, 4.2)
t = np.linspace(0, 2 * np.pi, 200); ax.plot(np.cos(t), np.sin(t), color=GRAY)
th = np.radians(35); ax.plot([0, np.cos(th)], [0, np.sin(th)], color=NAVY, lw=2.5)
ax.plot([0, np.cos(th)], [0, 0], color=TEAL, lw=4); ax.plot([np.cos(th)] * 2, [0, np.sin(th)], color=ORANGE, lw=4)
ax.text(0.4, -0.13, r"$\cos\theta$", color=TEAL, fontsize=12, ha="center"); ax.text(np.cos(th) + 0.05, 0.25, r"$\sin\theta$", color=ORANGE, fontsize=12)
ax.text(0.3, 0.45, "1", fontsize=12, color=NAVY); ax.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=35)); ax.text(0.3, 0.07, r"$\theta$")
ax.axhline(0, color="k", lw=.6); ax.axvline(0, color="k", lw=.6); ax.set_xlim(-1.2, 1.3); ax.set_ylim(-1.2, 1.2)
save(fig, "unitcircle")

# vectors add
fig, ax = blank(5.5, 3.2)
arrow(ax, (0, 0), (3, 1), NAVY); arrow(ax, (3, 1), (4, 3), ORANGE); arrow(ax, (0, 0), (4, 3), RED, ls="--")
ax.text(1.4, 0.15, "a = (3, 1)", color=NAVY); ax.text(3.6, 1.8, "b = (1, 2)", color=ORANGE); ax.text(1.0, 1.8, "a + b = (4, 3)", color=RED)
ax.set_xlim(-0.3, 5.5); ax.set_ylim(-0.4, 3.4); save(fig, "vectors")

# gaussian / sigma
fig, ax = plt.subplots(figsize=(6.5, 2.8))
x = np.linspace(-4, 4, 400); y = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi); ax.plot(x, y, color=NAVY, lw=2)
for k, c, lab in [(1.96, "#d6eaf8", "95%  (±1.96σ)"), (1, "#85c1e9", "68%  (±1σ)")]:
    m = abs(x) <= k; ax.fill_between(x[m], y[m], color=c)
ax.text(0, 0.17, "68%", ha="center"); ax.text(1.5, 0.03, "95%\nzone", ha="center", fontsize=8)
ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_xticklabels([r"$-2\sigma$", r"$-\sigma$", r"$\mu$", r"$+\sigma$", r"$+2\sigma$"])
ax.set_yticks([]); ax.set_title("The bell curve (Gaussian): how measurement errors usually spread"); save(fig, "gaussian")

# 2D rotation
fig, ax = blank(4.5, 4.2)
p = np.array([3, 4]); th = np.radians(30); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]); q = R @ p
arrow(ax, (0, 0), p, NAVY); arrow(ax, (0, 0), q, RED)
ax.add_patch(Arc((0, 0), 3, 3, theta1=np.degrees(np.arctan2(4, 3)), theta2=np.degrees(np.arctan2(q[1], q[0])), color="k"))
ax.text(3.05, 3.7, "p = (3, 4)", color=NAVY); ax.text(-0.6, 5.15, "p' = (0.60, 4.96)", color=RED); ax.text(0.2, 1.75, "30°")
ax.axhline(0, color="k", lw=.6); ax.axvline(0, color="k", lw=.6); ax.set_xlim(-1, 5); ax.set_ylim(-0.5, 5.6)
save(fig, "rot2d")

# roll pitch yaw vehicle
fig, axs = plt.subplots(1, 3, figsize=(9, 2.9))
for ax in axs: ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3, 3); ax.set_ylim(-1.5, 3)
ax = axs[0]; ax.set_title("ROLL  (about X, forward)\ntips side to side", fontsize=9)
ax.add_patch(Polygon([[-1.5, 0], [1.5, 0.5], [1.5, 1.4], [-1.5, 0.9]], fc=NAVY, alpha=.85)); ax.add_patch(Arc((0, 0.7), 4.2, 3.2, theta1=20, theta2=160, color=RED, lw=2))
arrow(ax, (-1.85, 1.3), (-1.95, 1.0), RED); ax.text(0, -0.8, "rear view", ha="center", fontsize=8, color=GRAY)
ax = axs[1]; ax.set_title("PITCH  (about Y, sideways)\nnose up / down", fontsize=9)
ax.add_patch(Polygon([[-2, 0], [2, 0.8], [2, 1.5], [-2, 0.7]], fc=TEAL, alpha=.85)); ax.add_patch(Arc((0, 0.75), 5, 3.4, theta1=10, theta2=60, color=RED, lw=2))
arrow(ax, (1.4, 2.2), (1.0, 2.4), RED); ax.text(2.1, 1.2, "nose", fontsize=8); ax.text(0, -0.8, "side view", ha="center", fontsize=8, color=GRAY)
ax = axs[2]; ax.set_title("YAW  (about Z, vertical)\nheading / azimuth", fontsize=9)
ax.add_patch(Polygon([[-0.7, -0.6], [0.7, -0.6], [0.7, 1.8], [0, 2.5], [-0.7, 1.8]], fc=ORANGE, alpha=.9))
ax.add_patch(Arc((0, 0.6), 4, 4, theta1=60, theta2=130, color=RED, lw=2)); arrow(ax, (-1.2, 2.2), (-1.5, 1.95), RED)
ax.text(0, -1.2, "top view", ha="center", fontsize=8, color=GRAY)
save(fig, "rpy")

# small angle lateral error
fig, ax = plt.subplots(figsize=(6.8, 3))
R = np.linspace(0, 150, 100)
for a, c in [(0.01, TEAL), (0.05, ORANGE), (0.10, RED)]:
    ax.plot(R, R * np.radians(a) * 100, color=c, lw=2.5, label=f"{a}° error")
ax.axhline(5, color=GRAY, ls="--"); ax.text(2, 5.6, "typical 5 cm tolerance", color=GRAY, fontsize=8)
ax.plot([80], [6.98], "o", color=ORANGE); ax.annotate("0.05° at 80 m = 7.0 cm", (80, 6.98), (90, 2), arrowprops=dict(arrowstyle="->"), fontsize=9)
ax.set_xlabel("range (m)"); ax.set_ylabel("sideways error (cm)"); ax.legend(frameon=False); ax.grid(alpha=.3)
ax.set_title(r"Small-angle rule: error = range $\times$ angle (in radians)"); save(fig, "smallangle")

# IMU parts
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3))
for a in (a1, a2): a.set_aspect("equal"); a.axis("off")
a1.add_patch(Rectangle((0, 0), 6, 2.4, fill=False, lw=2)); a1.add_patch(Rectangle((2.6, 0.7), 1.0, 1.0, fc=NAVY))
zz = np.linspace(0, 2.6, 60); a1.plot(zz, 1.2 + 0.25 * np.sin(zz * 15) * (zz > 0.2) * (zz < 2.4), "k")
zz = np.linspace(3.6, 6, 60); a1.plot(zz, 1.2 + 0.25 * np.sin(zz * 15) * (zz > 3.8) * (zz < 5.8), "k")
arrow(a1, (3.1, 2.8), (4.6, 2.8), RED); a1.text(3.0, 3.1, "box speeds up -> mass lags", color=RED, fontsize=9)
a1.set_title("Accelerometer: a mass on springs", fontsize=10); a1.set_xlim(-0.3, 6.3); a1.set_ylim(-0.6, 3.6)
a1.text(3.1, -0.45, "spring stretch = force -> acceleration (F = m a)", ha="center", fontsize=8)
a2.add_patch(Circle((0, 0), 1.6, fill=False, lw=2)); a2.add_patch(Circle((0, 0), 1.0, fill=False, lw=2, ls="--"))
a2.add_patch(Arc((0, 0), 3.9, 3.9, theta1=20, theta2=110, color=RED, lw=2)); arrow(a2, (-0.6, 1.88), (-0.95, 1.73), RED)
a2.text(2.0, 1.0, "how FAST\nit turns\n(°/s)", color=RED, fontsize=9)
a2.set_title("Gyroscope: measures turning rate", fontsize=10); a2.set_xlim(-2.4, 3.6); a2.set_ylim(-2, 2.5)
save(fig, "imuparts")

# dead reckoning integration staircase
fig, axs = plt.subplots(3, 1, figsize=(6.8, 4.6), sharex=True)
t = np.arange(0, 5.01, 0.25); a = np.where(t < 2, 1.0, np.where(t < 3, 0, -0.5))
v = np.concatenate([[0], np.cumsum(a[:-1] * 0.25)]); p = np.concatenate([[0], np.cumsum(v[:-1] * 0.25)])
axs[0].step(t, a, where="post", color=RED, lw=2); axs[0].set_ylabel("accel\n(m/s²)")
axs[1].bar(t, v, width=0.24, align="edge", color=ORANGE, alpha=.7); axs[1].set_ylabel("velocity\n(m/s)")
axs[2].plot(t, p, "o-", color=NAVY); axs[2].set_ylabel("position\n(m)"); axs[2].set_xlabel("time (s)")
axs[0].set_title("Integration: add up little pieces, step after step")
for ax in axs: ax.grid(alpha=.3)
save(fig, "integrate")

# bias growth
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.5, 3.1))
t = np.linspace(0, 120, 300); v = 15
for bdeg, c, lab in [(100, RED, "consumer 100°/h"), (10, ORANGE, "industrial 10°/h"), (1, TEAL, "tactical 1°/h"), (0.01, NAVY, "navigation 0.01°/h")]:
    bg = np.radians(bdeg) / 3600; a1.plot(t, 0.5 * v * bg * t ** 2, color=c, lw=2, label=lab)
a1.set_yscale("log"); a1.set_ylim(1e-4, 1e3); a1.set_xlabel("seconds with no help"); a1.set_ylabel("sideways error (m)")
a1.set_title("Gyro bias at 15 m/s", fontsize=10); a1.legend(fontsize=7, frameon=False); a1.grid(alpha=.3, which="both")
for mg, c, lab in [(10, RED, "consumer 10 mg"), (1, ORANGE, "industrial 1 mg"), (0.5, TEAL, "tactical 0.5 mg"), (0.025, NAVY, "navigation 25 µg")]:
    ba = mg * 1e-3 * 9.80665; a2.plot(t, 0.5 * ba * t ** 2, color=c, lw=2, label=lab)
a2.set_yscale("log"); a2.set_ylim(1e-4, 1e4); a2.set_xlabel("seconds with no help"); a2.set_title("Accelerometer bias", fontsize=10)
a2.legend(fontsize=7, frameon=False); a2.grid(alpha=.3, which="both"); a2.set_ylabel("position error (m)")
save(fig, "biasgrowth")

# tilt leaks gravity
fig, ax = blank(6.2, 3)
ax.plot([-3, 3], [0, 0], color="#6e4b2a", lw=3)
c, s = np.cos(np.radians(12)), np.sin(np.radians(12))
ax.add_patch(Polygon([[-1, 0.1], [1, 0.1], [1, 1.1], [-1, 1.1]], fc=NAVY, alpha=.3, ls="--", ec=NAVY))
pts = np.array([[-1, 0], [1, 0], [1, 1], [-1, 1]]) @ np.array([[c, s], [-s, c]]) + [0, 0.35]; ax.add_patch(Polygon(pts, fc=NAVY, alpha=.85))
arrow(ax, (0, 0.85), (0, -0.9), "k"); ax.text(0.1, -0.7, "g = 9.81 m/s²", fontsize=9)
arrow(ax, (0, 0.85), (-1.3 * c, 0.85 - 1.3 * s), RED); ax.text(-2.9, 0.15, "leaked part\n= g·sin(tilt)", color=RED, fontsize=9)
ax.text(1.4, 1.5, "If the computer thinks it is level\nbut it is tilted, a slice of gravity\nlooks like the car is speeding up.", fontsize=8.5)
ax.set_xlim(-3.2, 5.5); ax.set_ylim(-1.1, 2.3); save(fig, "tilt")

# grades bar
fig, ax = plt.subplots(figsize=(6.8, 2.8))
names = ["Consumer\nMEMS", "Industrial\nMEMS", "Tactical\n(FOG/high MEMS)", "Navigation"]
lo = [10, 1, 0.1, 0.001]; hi = [100, 10, 1, 0.01]
for i, (l, h) in enumerate(zip(lo, hi)): ax.bar(i, h - l, bottom=l, color=[RED, ORANGE, TEAL, NAVY][i], width=0.55)
ax.set_yscale("log"); ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=8); ax.set_ylabel("gyro bias (°/h)")
ax.set_title("IMU grades: each step is ~10x better (and pricier)"); ax.grid(alpha=.3, axis="y", which="both"); save(fig, "grades")

# preintegration timeline
fig, ax = blank(8, 2.0)
ax.plot([0, 10], [0, 0], color="k", lw=1)
for x in np.arange(0, 10.01, 0.25): ax.plot([x, x], [-0.12, 0.12], color=GRAY, lw=1)
for x, lab in [(0, "keyframe i"), (5, "keyframe j"), (10, "keyframe k")]:
    ax.add_patch(Circle((x, 0), 0.28, fc=NAVY)); ax.text(x, -0.7, lab, ha="center", fontsize=9)
ax.add_patch(FancyBboxPatch((0.4, 0.45), 4.2, 0.55, boxstyle="round,pad=0.02", fc="#fdebd0", ec=ORANGE))
ax.text(2.5, 0.72, r"20 IMU ticks summed once: $\Delta v_{ij},\ \Delta p_{ij},\ \Delta R_{ij}$", ha="center", fontsize=9)
ax.set_xlim(-0.6, 10.6); ax.set_ylim(-1, 1.2); save(fig, "preint")

# GNSS vs IMU vs fused
fig, ax = plt.subplots(figsize=(7, 3))
t = np.linspace(0, 120, 600); imu = 0.0004 * t ** 2 + 0.01
g = 0.03 + 0.02 * np.abs(rng.standard_normal(600)); g[(t > 50) & (t < 75)] = np.nan
fused = np.where((t > 50) & (t < 75), 0.03 + 0.0004 * (t - 50) ** 2, 0.025)
ax.plot(t, imu, color=RED, lw=2, label="IMU alone (drifts)"); ax.plot(t, g, ".", ms=2, color=ORANGE, label="GNSS alone (noisy, gaps)")
ax.plot(t, fused, color=NAVY, lw=2.5, label="IMU + GNSS fused"); ax.axvspan(50, 75, color=GRAY, alpha=.15); ax.text(62.5, 3.0, "tunnel:\nno GNSS", ha="center", fontsize=8)
ax.set_yscale("log"); ax.set_xlabel("time (s)"); ax.set_ylabel("position error (m)"); ax.legend(fontsize=8, frameon=False, loc="upper left"); ax.grid(alpha=.3)
ax.set_title("Two sensors with opposite weaknesses make a strong team"); save(fig, "gnssimu")

# PPS timing
fig, ax = plt.subplots(figsize=(7.5, 2.6))
t = np.linspace(0, 3, 3000)
ax.plot(t, 3 + 0.4 * ((t % 1) < 0.02), color=NAVY, lw=1.5); ax.text(-0.05, 3.1, "GNSS PPS", ha="right", fontsize=9)
ax.plot(t, 2 + 0.3 * ((t * 10 % 1) < 0.1), color=ORANGE, lw=1.2); ax.text(-0.05, 2.1, "LiDAR 10 Hz", ha="right", fontsize=9)
ax.plot(t, 1 + 0.2 * ((t * 100 % 1) < 0.3), color=TEAL, lw=0.6); ax.text(-0.05, 1.05, "IMU 100 Hz", ha="right", fontsize=9)
for k in range(4): ax.axvline(k, color=RED, ls=":", lw=1)
ax.set_yticks([]); ax.set_xlabel("time (s)"); ax.set_xlim(-0.05, 3); ax.set_title("One shared clock: every sensor lines up on the PPS tick")
save(fig, "pps")

# deskew wall
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3.1))
ang = np.linspace(-np.pi / 3, np.pi / 3, 120); tt = (ang - ang.min()) / (ang.max() - ang.min()) * 0.1
y = 10 * np.tan(ang) / 3; x = np.full_like(y, 10.0)
for a, xm, ttl in [(a1, x - 15 * tt, "Raw: assumes sensor stood still"), (a2, x, "De-skewed with IMU motion")]:
    a.plot(xm, y, ".", color=RED if a is a1 else TEAL, ms=4); a.plot([10, 10], [-6, 6], color=GRAY, ls="--", lw=1)
    a.set_title(ttl, fontsize=10); a.set_xlim(7.5, 11); a.set_xlabel("distance ahead (m)"); a.set_ylabel("sideways (m)")
a1.text(10.1, -6, "true\nwall", fontsize=8, color=GRAY); a1.annotate("1.5 m slant", (8.6, 5.5), (7.6, 1), arrowprops=dict(arrowstyle="->"), fontsize=8)
save(fig, "deskew")

# bird's nest vs clean
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3.2))
def scene():
    pts = []
    for yv in (-4, 4):
        xx = rng.uniform(0, 30, 600); pts.append(np.c_[xx, yv + 0.03 * rng.standard_normal(600)])
    for px in range(3, 30, 6):
        t = rng.uniform(0, 2 * np.pi, 60); pts.append(np.c_[px + 0.3 * np.cos(t), 2.5 + 0.3 * np.sin(t)])
    return np.vstack(pts)
S = scene()
for k in range(10):
    th = rng.normal(0, 0.12); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]); sh = rng.normal(0, 1.2, 2)
    Q = S @ R.T + sh; a1.plot(Q[:, 0], Q[:, 1], ".", ms=0.6, color=plt.cm.tab10(k))
a2.plot(S[:, 0], S[:, 1], ".", ms=0.8, color=NAVY)
for a, ttl in [(a1, "Bad trajectory: 'bird's nest'"), (a2, "Good trajectory: crisp map")]:
    a.set_aspect("equal"); a.axis("off"); a.set_title(ttl, fontsize=10)
save(fig, "birdsnest")

# lever arm
fig, ax = blank(7, 3)
ax.add_patch(Rectangle((0, 0), 6, 0.3, fc="#95a5a6", ec="k")); ax.text(3, -0.35, "rigid mounting plate", ha="center", fontsize=8)
ax.add_patch(Rectangle((0.8, 0.3), 1.0, 0.7, fc=NAVY)); ax.text(1.3, 0.65, "IMU", color="w", ha="center", va="center", weight="bold")
ax.add_patch(Rectangle((4.0, 0.3), 0.9, 1.4, fc=ORANGE)); ax.text(4.45, 1.0, "LiDAR", ha="center", va="center", weight="bold", rotation=90)
ax.plot(1.3, 0.65, "k+", ms=12); ax.plot(4.45, 1.4, "k+", ms=12)
arrow(ax, (1.3, 0.65), (4.45, 1.4), RED, lw=2.5); ax.text(1.6, 1.55, "lever arm  l = (dx, dy, dz)", color=RED)
ax.annotate("", (1.3, 2.3), (4.45, 2.3), arrowprops=dict(arrowstyle="<->")); ax.text(2.87, 2.4, "dx = 0.120 m", ha="center", fontsize=9)
ax.annotate("", (5.3, 0.65), (5.3, 1.4), arrowprops=dict(arrowstyle="<->")); ax.text(5.4, 1.0, "dz = 0.085 m", fontsize=9)
ax.set_xlim(-0.2, 7); ax.set_ylim(-0.6, 2.8); save(fig, "leverarm")

# boresight two-pass
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3))
for a, off, ttl in [(a1, 0.35, "Bad boresight: passes disagree"), (a2, 0, "Calibrated: passes agree")]:
    x = np.linspace(-3, 3, 200); roof = np.clip(2 - np.abs(x), 0, None) + 1
    a.plot(x + off, roof, color=RED, lw=2, label="pass driving north"); a.plot(x - off, roof, color=NAVY, lw=2, ls="--", label="pass driving south")
    a.set_title(ttl, fontsize=10); a.set_ylim(0.5, 3.4); a.set_xlabel("across-track (m)"); a.set_yticks([])
a1.legend(fontsize=7, frameon=False, loc="upper right"); a1.annotate("", (-0.35, 3.1), (0.35, 3.1), arrowprops=dict(arrowstyle="<->", color="k")); a1.text(0, 3.2, "2 x error", ha="center", fontsize=8)
save(fig, "boresight_cal")

# georef chain
fig, ax = blank(9, 1.9)
steps = ["time of\nflight", "polar ->\nX,Y,Z", "boresight\nrotation", "+ lever\narm", "attitude\n(R,P,Y)", "+ trajectory\nposition", "map\npoint"]
cols = [SKY, SKY, ORANGE, ORANGE, TEAL, TEAL, NAVY]
for i, (s, c) in enumerate(zip(steps, cols)):
    box(ax, (i * 1.3, 0), 1.1, 0.9, s, fc=c, ec="k", fs=8, tc="w" if c == NAVY else "#111")
    if i < 6: arrow(ax, (i * 1.3 + 1.1, 0.45), (i * 1.3 + 1.3, 0.45), "k", lw=1.2, ms=10)
ax.set_xlim(-0.1, 9.1); ax.set_ylim(-0.1, 1.0); save(fig, "chain")
print("figs2 done")

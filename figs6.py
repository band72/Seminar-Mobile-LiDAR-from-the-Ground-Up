from style import *
rng = np.random.default_rng(12)
d = np.deg2rad

# ---------- 1. reflectivity chart ----------
mats = [  # name, low, high (%), color
    ("Clear water (calm)", 1, 5, SKY), ("Black tire / rubber", 2, 5, "#2c3e50"), ("Black car paint", 3, 8, "#34495e"),
    ("Fresh asphalt", 4, 8, "#5d6d7e"), ("Wet soil / wet asphalt", 4, 12, "#6e4b2a"), ("Aged asphalt", 10, 20, "#7f8c8d"),
    ("Dark rock / basalt", 5, 15, "#4d5656"), ("Tree bark / wood", 20, 45, "#8d6e63"), ("Dry soil", 15, 35, "#a0522d"),
    ("Concrete", 25, 50, "#aab7b8"), ("Dry sand", 30, 55, GOLD), ("Grass / green leaves", 40, 60, "#27ae60"),
    ("White paint / road striping", 60, 85, "#d5d8dc"), ("Fresh snow (865-905 nm)", 75, 95, "#ecf0f1"),
    ("Retroreflective sign / tape", 100, 300, ORANGE)]
fig, ax = plt.subplots(figsize=(7.6, 5.4))
for i, (n, lo, hi, c) in enumerate(mats):
    ax.barh(i, hi - lo, left=lo, color=c, ec="k", lw=0.6, height=0.6)
ax.set_yticks(range(len(mats))); ax.set_yticklabels([m[0] for m in mats], fontsize=8.5)
ax.set_xscale("log"); ax.set_xlim(0.8, 400); ax.set_xlabel("typical near-infrared reflectivity (%, log scale)")
ax.axvline(10, color=RED, ls="--", lw=1.2); ax.text(10.5, -0.9, "10%: OS0 range 35 m", color=RED, fontsize=8)
ax.axvline(80, color=TEAL, ls="--", lw=1.2); ax.text(84, -0.9, "80%: 75 m", color=TEAL, fontsize=8)
ax.text(95, len(mats) - 2.5, ">100%: light is sent\nback toward the source", fontsize=7.5, color=ORANGE, ha="right")
ax.set_ylim(-1.3, len(mats) - 0.4); ax.grid(alpha=.3, axis="x", which="both")
ax.set_title("How bright common surfaces look to an 865-905 nm laser (approximate)")
save(fig, "reflectivity")

# ---------- 2. penetration panels ----------
fig, axs = plt.subplots(1, 5, figsize=(10, 2.9))
titles = ["Tree canopy:\nthrough the GAPS", "Clear glass:\nmostly THROUGH", "Water (NIR):\nSTOPS at surface", "Fog / rain / dust:\nPARTLY, with noise", "Wall / soil:\nNO penetration"]
for ax, t in zip(axs, titles):
    ax.set_xlim(0, 4); ax.set_ylim(0, 5); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(t, fontsize=8.5)
    ax.add_patch(Rectangle((1.75, 4.5), 0.5, 0.35, fc=NAVY))
# canopy
a = axs[0]; a.add_patch(Ellipse((2, 2.9), 3.2, 1.6, fc="#27ae60", alpha=.6)); a.plot([2.6, 2.6], [0.3, 2.3], color="#6e4b2a", lw=4)
for x0, xe, ye in [(1.85, 1.2, 0.35), (2.0, 2.0, 3.5), (2.15, 2.8, 0.35)]:
    a.plot([x0, xe], [4.5, ye], color=RED, lw=1)
a.plot([1.2, 2.8], [0.35, 0.35], "o", color=ORANGE, ms=5); a.plot(2.0, 3.5, "o", color=ORANGE, ms=5); a.plot([0, 4], [0.3, 0.3], color="#6e4b2a", lw=2)
# glass
a = axs[1]; a.add_patch(Rectangle((0.6, 1.8), 2.8, 0.15, fc=SKY, alpha=.5, ec=SKY)); a.plot([2, 2], [4.5, 0.4], color=RED, lw=1)
a.plot(2, 0.4, "o", color=ORANGE, ms=5); a.plot([0, 4], [0.3, 0.3], color="k", lw=2); a.plot(2, 1.95, "o", color=ORANGE, ms=3, alpha=.5)
a.text(2.1, 2.1, "weak/none", fontsize=7)
# water
a = axs[2]; a.add_patch(Rectangle((0, 0.3), 4, 1.8, fc=SKY, alpha=.5)); a.plot([2, 2], [4.5, 2.1], color=RED, lw=1); a.plot([2, 2], [2.1, 1.6], color=RED, lw=1, ls=":")
a.plot(2, 2.1, "o", color=ORANGE, ms=5); a.plot([0, 4], [0.3, 0.3], color="#6e4b2a", lw=2); a.text(0.15, 0.9, "bottom unseen\n(green 532 nm\nbathymetric can)", fontsize=6.5)
# fog
a = axs[3]
for _ in range(60): a.plot(rng.uniform(0.3, 3.7), rng.uniform(1.0, 4.0), ".", color=GRAY, ms=2)
a.plot([2, 2], [4.5, 0.4], color=RED, lw=1, alpha=.6); a.plot(2, 0.4, "o", color=ORANGE, ms=5); a.plot([2, 2], [3.6, 3.0], "o", color=PURPLE, ms=3)
a.plot([0, 4], [0.3, 0.3], color="k", lw=2); a.text(2.15, 3.2, "false\nreturns", fontsize=6.5, color=PURPLE)
# wall
a = axs[4]; a.add_patch(Rectangle((0.5, 1.2), 3, 1.0, fc="#b8977e", ec="k", hatch="//")); a.plot([2, 2], [4.5, 2.2], color=RED, lw=1)
a.plot(2, 2.2, "o", color=ORANGE, ms=5); a.plot([0, 4], [0.3, 0.3], color="k", lw=2); a.text(0.7, 0.6, "nothing behind\nis measured", fontsize=6.5)
save(fig, "penetration")

# ---------- 3. sensor timeline ----------
fig, ax = plt.subplots(figsize=(9, 3.6))
T = 1.0
rows = [("IMU 200 Hz", 200, TEAL, 0.25), ("LiDAR sweeps 10 Hz", 10, ORANGE, 0.6), ("Camera images 2 Hz", 2, PURPLE, 0.6), ("GNSS fixes 5 Hz", 5, GOLD, 0.6)]
for k, (lab, f, c, h) in enumerate(rows[::-1]):
    y = k
    ts = np.arange(0, T + 1e-9, 1 / f)
    if f == 10:
        for t0 in ts[:-1]: ax.add_patch(Rectangle((t0 + 0.003, y - 0.25), 0.094, 0.5, fc=c, alpha=.55, ec=c))
    else:
        for t0 in ts: ax.plot([t0, t0], [y - h / 2, y + h / 2], color=c, lw=1 if f > 50 else 3)
    ax.text(-0.02, y, lab, ha="right", va="center", fontsize=9)
yk = len(rows)
ax.plot([0, T], [yk, yk], color="k", lw=1)
ax.plot(np.arange(0, T + 1e-9, 0.1), np.full(11, yk), "o", ms=11, mfc="#d6eaf8", mec=NAVY, mew=1.5)
ax.text(-0.02, yk, "Poses (trajectory)", ha="right", va="center", fontsize=9, weight="bold")
for t0 in (0.5,):
    ax.annotate("image at 0.50 s gets its pose\nby interpolating the trajectory", (t0, 1.3), (0.62, 2.4), fontsize=8, color=PURPLE, arrowprops=dict(arrowstyle="->", color=PURPLE))
ax.set_xlim(-0.01, 1.01); ax.set_ylim(-0.6, yk + 0.6); ax.set_yticks([]); ax.set_xlabel("time (s)")
for s in ("left",): ax.spines[s].set_visible(False)
ax.set_aspect(0.08)
ax.set_title("One second of data: every sensor ticks at its own rate; the trajectory ties them together", fontsize=10)
save(fig, "traj_timeline")

# ---------- 4. trajectory map with contributions ----------
fig, ax = plt.subplots(figsize=(9, 5.2)); ax.set_aspect("equal")
s = np.linspace(0, 1, 400); X = 100 * s; Y = 18 * np.sin(2.2 * s) + 4 * s
ax.add_patch(Rectangle((52, -20), 22, 50, fc=GRAY, alpha=.15)); ax.text(63, -17, "tunnel / underpass:\nno GNSS", ha="center", fontsize=8)
# scans (lidar footprints)
for i in range(0, 400, 40):
    ax.add_patch(Circle((X[i], Y[i]), 9, fc=ORANGE, alpha=.07, ec=ORANGE, lw=0.5))
# walls
xx = np.linspace(0, 100, 300); ax.plot(xx, 18 * np.sin(2.2 * xx / 100) + 4 * xx / 100 + 7, ".", color="#7f8c8d", ms=1.5)
ax.plot(xx, 18 * np.sin(2.2 * xx / 100) + 4 * xx / 100 - 7, ".", color="#7f8c8d", ms=1.5)
ax.plot(X, Y, color=NAVY, lw=2.5, label="trajectory (continuous poses)")
# poses triads
for i in range(0, 400, 25):
    th = np.arctan2(np.gradient(Y)[i], np.gradient(X)[i])
    ax.arrow(X[i], Y[i], 5.5 * np.cos(th), 5.5 * np.sin(th), head_width=1.2, color=RED, lw=1.6, zorder=6)
    ax.arrow(X[i], Y[i], -3.5 * np.sin(th), 3.5 * np.cos(th), head_width=1.0, color=TEAL, lw=1.2, zorder=6)
# GNSS fixes outside tunnel
gi = [i for i in range(0, 400, 12) if not (52 <= X[i] <= 74)]
ax.plot(X[gi] + rng.normal(0, 0.8, len(gi)), Y[gi] + rng.normal(0, 0.8, len(gi)), "s", color=GOLD, ms=5, mec="k", mew=0.5, label="GNSS fixes (absolute)")
# camera frustums
for i in (60, 160, 260, 360):
    th = np.arctan2(np.gradient(Y)[i], np.gradient(X)[i]) + np.pi / 2
    p = np.array([X[i], Y[i]]); a1 = th - 0.35; a2 = th + 0.35
    ax.add_patch(Polygon([p, p + 8 * np.array([np.cos(a1), np.sin(a1)]), p + 8 * np.array([np.cos(a2), np.sin(a2)])], fc=PURPLE, alpha=.3, ec=PURPLE))
ax.plot([], [], color=RED, lw=2, label="pose axes: forward (red) / left (teal)")
ax.add_patch(Polygon([[0, 0]], fc=PURPLE, alpha=.3, label="camera image + its interpolated pose"))
ax.add_patch(Circle((0, 0), 0.01, fc=ORANGE, alpha=.2, label="LiDAR scan coverage (scan matching)"))
ax.text(2, 26, "start: GNSS + IMU alignment", fontsize=8)
ax.annotate("in the tunnel, LiDAR scan\nmatching + IMU carry the poses", (63, Y[250]), (68, 32), fontsize=8, arrowprops=dict(arrowstyle="->"))
ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False); ax.set_xlim(-3, 108); ax.set_ylim(-22, 38); ax.set_xlabel("Easting (m)"); ax.set_ylabel("Northing (m)")
ax.set_title("Building the path: poses, scans, images and GNSS on one trajectory", fontsize=10)
save(fig, "traj_map")

# ---------- 5. who holds the trajectory (contribution bands) ----------
t = np.linspace(0, 120, 600)
gnss = np.where((t > 50) & (t < 75), 0.02, 1.0)
lidar = np.where((t > 90) & (t < 105), 0.2, 1.0)
imu = np.ones_like(t)
fig, ax = plt.subplots(figsize=(8.5, 2.9))
w_imu = 0.25 + 0 * t; w_l = 0.45 * lidar; w_g = 0.45 * gnss
tot = w_imu + w_l + w_g
ax.stackplot(t, w_imu / tot, w_l / tot, w_g / tot, colors=[TEAL, ORANGE, GOLD], alpha=.8, labels=["IMU (always on, short-term)", "LiDAR scan matching", "GNSS (absolute)"])
ax.text(62.5, 0.5, "tunnel:\nno GNSS", ha="center", fontsize=8); ax.text(97.5, 0.15, "featureless\nfield:\nweak LiDAR", ha="center", fontsize=7.5)
ax.set_xlim(0, 120); ax.set_ylim(0, 1); ax.set_xlabel("time along the route (s)"); ax.set_ylabel("share of\ninformation")
ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=3, frameon=False)
ax.set_title("Which sensor is holding the trajectory? (conceptual)", fontsize=10)
save(fig, "traj_share")
print("figs6 done")

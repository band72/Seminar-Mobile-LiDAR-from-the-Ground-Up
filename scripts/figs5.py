from style import *
d = np.deg2rad
rng = np.random.default_rng(8)
A = np.array([1000., 1000.])
legs = [(200, 90), (150, 180), (200, 270), (150, 0)]

def trav(dh=None, scale=0.0):
    p = A.copy(); pts = [p.copy()]
    for i, (L, az) in enumerate(legs):
        a = az + (dh[i] if dh is not None else 0)
        p = p + L * (1 + scale) * np.array([np.sin(d(a)), np.cos(d(a))]); pts.append(p.copy())
    return np.array(pts)

T = trav(); S0 = trav([0.8] * 4, 0.002); R0 = trav([0.8, -1.2, 0.8, 0.8], 0.002)
EX = 8
S = T + EX * (S0 - T); R = T + EX * (R0 - T)
names = "ABCDA"

# --- traverse sketch: AHRS runs ---
fig, ax = plt.subplots(figsize=(7.6, 5.6)); ax.set_aspect("equal")
ax.add_patch(Rectangle((1015, 865), 170, 120, fc="#eaecee", ec="none")); ax.text(1100, 925, "city block", ha="center", color=GRAY, fontsize=10)
ax.plot(T[:, 0], T[:, 1], color="k", lw=3, label="true traverse (surveyed control)")
ax.plot(S[:, 0], S[:, 1], color=TEAL, lw=2, ls="--", label="Run 1: constant 0.8° heading bias + 0.2% odometer")
ax.plot(R[:, 0], R[:, 1], color=RED, lw=2, label="Run 2: same + steel bridge on leg B-C (-2°)")
for i in range(4):
    ax.plot(*T[i], "^", ms=11, color=GOLD, mec="k", zorder=5); ax.text(T[i][0] - 9, T[i][1] + 6, names[i], fontsize=12, weight="bold")
ax.annotate("", R[-1], A, arrowprops=dict(arrowstyle="<->", color=RED, lw=2)); ax.text(1012, 1012, "misclosure 5.25 m", color=RED, fontsize=9)
ax.annotate("Run 1 closes perfectly\nbut B is 2.8 m off!", S[1], (1120, 1030), color=TEAL, fontsize=9, arrowprops=dict(arrowstyle="->", color=TEAL))
ax.add_patch(Rectangle((1193, 905), 14, 20, fc="#7f8c8d", alpha=.6)); ax.text(1212, 912, "steel\nbridge", fontsize=8)
for i in range(3):
    m = (T[i] + T[i + 1]) / 2; L, az = legs[i]; ax.text(m[0] + (8 if az in (0, 180) else 0), m[1] + (-14 if az == 90 else 4), f"{L} m @ {az:03d}°", fontsize=8, color=NAVY)
ax.text(985, 925, "150 m @ 000°", fontsize=8, color=NAVY, rotation=90, va="center")
arrow(ax, (1235, 960), (1235, 990), "k"); ax.text(1231, 993, "N", fontsize=11, weight="bold")
ax.set_xlim(955, 1260); ax.set_ylim(805, 1060); ax.set_xlabel("Easting (m)"); ax.set_ylabel("Northing (m)")
ax.legend(fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=1, frameon=False)
ax.set_title("The Block Loop: AHRS + odometer traverse (errors drawn 8x actual size)", fontsize=10)
save(fig, "trav_ahrs")

# --- GNSS/INS run ---
fig, ax = plt.subplots(figsize=(7.6, 5.2)); ax.set_aspect("equal")
ax.plot(T[:, 0], T[:, 1], color="k", lw=3, label="true traverse")
# dense true path
path = []
for i in range(4):
    for s in np.linspace(0, 1, 40, endpoint=False): path.append(T[i] + s * (T[i + 1] - T[i]))
path = np.array(path)
ins = path + 5 * rng.normal(0, 2 / np.sqrt(2), path.shape)  # 2 m RMS horizontal, drawn 5x
# tunnel on leg C-D: indices 80..120, coast with drift
tun = np.arange(90, 110)
drift = np.zeros_like(path); k = np.arange(len(tun)); drift[tun, 1] = -5 * 2.0 * (k / (len(tun) - 1)) ** 2; drift[tun, 0] = 5 * 0.8 * (k / (len(tun) - 1)) ** 2
ins[tun] = path[tun] + ins[89] - path[89] + drift[tun]
ax.plot(ins[:, 0], ins[:, 1], ".", color=PURPLE, ms=4, label="3DM-GX5-45 GNSS/INS positions (±2 m RMS)")
ax.annotate("INS coasting:\ndrift grows", (1060, 858), (1040, 880), fontsize=8, color=PURPLE, arrowprops=dict(arrowstyle="->", color=PURPLE)); ax.text(1100, 968, "dashed circles: 95% (3.5 m)\nat each control point", fontsize=8, color=PURPLE, ha="center")
ax.add_patch(Rectangle((1058, 838), 70, 24, fc=GRAY, alpha=.25)); ax.text(1093, 832, "underpass: no GNSS", ha="center", fontsize=8)
for i in range(4):
    ax.plot(*T[i], "^", ms=11, color=GOLD, mec="k", zorder=5); ax.text(T[i][0] - 9, T[i][1] + 6, names[i], fontsize=12, weight="bold")
    ax.add_patch(Circle(T[i], 5 * 2 * 2.448 / np.sqrt(2), fill=False, ec=PURPLE, ls="--"))
ax.set_xlim(955, 1245); ax.set_ylim(815, 1040); ax.set_xlabel("Easting (m)"); ax.set_ylabel("Northing (m)")
ax.legend(fontsize=8, loc="center", frameon=False); ax.set_title("Same loop with the GNSS/INS (errors drawn 5x): bounded, but meter-level", fontsize=10)
save(fig, "trav_ins")

# --- pure inertial drift for GX5 IMU ---
t = np.linspace(0, 70, 300); g = 9.80665
fig, ax = plt.subplots(figsize=(7.2, 3.6))
for lab, a, c in [("0.25° tilt error leaks gravity", g * np.sin(d(0.25)), RED), ("2 mg initial accel bias (uncalibrated)", 2e-3 * g, ORANGE),
                  ("0.04 mg accel bias instability (best case)", 0.04e-3 * g, TEAL)]:
    ax.plot(t, 0.5 * a * t ** 2, color=c, lw=2.5, label=lab)
ax.plot(t, 0.5 * 10 * d(0.04) * t ** 2, color=PURPLE, lw=2, ls="--", label="0.04°/s initial gyro bias -> sideways at 10 m/s")
ax.plot(t, 0.5 * 10 * d(8 / 3600) * t ** 2, color=NAVY, lw=2, ls=":", label="8°/h gyro bias instability -> sideways")
ax.set_yscale("log"); ax.set_ylim(1e-3, 300); ax.set_xlabel("seconds driving with the IMU alone"); ax.set_ylabel("position error (m)")
ax.grid(alpha=.3, which="both"); ax.legend(fontsize=7.5, frameon=False, loc="lower right")
ax.axvline(70, color=GRAY, ls=":"); ax.text(68, 150, "one lap = 70 s", ha="right", fontsize=8)
ax.set_title("3DM-GX5 MEMS IMU, no aiding: how fast each error grows"); save(fig, "gx5_drift")

# --- LiDAR point error vs range for each unit ---
r = np.linspace(1, 35, 100)
fig, ax = plt.subplots(figsize=(7.2, 3.4))
ax.plot(r, r * d(0.8) * 100, color=RED, lw=2.5, label="heading 0.8° RMS (GX5-25 / GX5-45 EKF)")
ax.plot(r, r * d(0.5) * 100, color=ORANGE, lw=2, ls="--", label="heading 0.5° (GX5-45 GNSS heading, moving)")
ax.plot(r, r * d(0.25) * 100, color=PURPLE, lw=2, label="roll/pitch 0.25° RMS (both)")
ax.plot(r, r * d(0.25) * 100, color=NAVY, lw=2.5, ls="-.", label="heading 0.25° (GQ7 dual antenna, 1.5 m baseline)")
ax.plot(r, r * d(0.05) * 100, color=TEAL, lw=2, ls=":", label="roll/pitch 0.05° (GQ7) = SLAM-aided heading 0.05°")
ax.axhline(3, color="k", ls="--", lw=1); ax.text(1, 3.8, "3 cm survey spec", fontsize=8)
ax.set_xlabel("range to the LiDAR point (m)"); ax.set_ylabel("point error (cm)"); ax.set_ylim(0, 50); ax.grid(alpha=.3)
ax.legend(fontsize=7.5, frameon=False, loc="upper left"); ax.set_title("Attitude error, propagated to a LiDAR point")
save(fig, "gx5_point")

# --- coast error vs outage time ---
t = np.linspace(0, 60, 300)
def coast(sv, ba_ug, bg_dph):
    return np.sqrt((sv * t) ** 2 + (0.5 * ba_ug * 1e-6 * g * t * t) ** 2 + (g * d(bg_dph / 3600) * t ** 3 / 6) ** 2)
fig, ax = plt.subplots(figsize=(7.2, 3.5))
ax.plot(t, coast(0.1, 40, 8), color=PURPLE, lw=2.5, label="3DM-GX5-45 (0.1 m/s, 0.04 mg, 8°/h)")
ax.plot(t, coast(0.05, 5, 1.5), color=NAVY, lw=2.5, label="3DM-GQ7, datasheet velocity (0.05 m/s, 5 µg, 1.5°/h)")
ax.plot(t, coast(0.01, 5, 1.5), color=TEAL, lw=2.5, ls="--", label="3DM-GQ7 after RTK (velocity 0.01 m/s, assumed)")
ax.axvspan(0, 20, color=GRAY, alpha=.12); ax.text(10, 20, "20 s underpass", ha="center", fontsize=8)
ax.set_yscale("log"); ax.set_ylim(1e-3, 40); ax.set_xlabel("seconds without GNSS"); ax.set_ylabel("horizontal coast error (m)")
ax.grid(alpha=.3, which="both"); ax.legend(fontsize=7.5, frameon=False, loc="lower right"); ax.set_title("Coasting through a GNSS outage: velocity, accel bias and gyro bias terms")
save(fig, "gq7_coast")

# --- heading vs antenna baseline ---
b = np.linspace(0.3, 3, 200); sig_rel = 1.5 * d(0.25)
fig, ax = plt.subplots(figsize=(6.8, 3.0))
ax.plot(b, np.degrees(sig_rel / b), color=NAVY, lw=2.5)
for bb, lab in [(0.5, "backpack\n0.5 m"), (1.5, "datasheet\n1.5 m"), (2.5, "vehicle roof\n2.5 m")]:
    v = np.degrees(sig_rel / bb); ax.plot(bb, v, "o", color=RED); ax.annotate(f"{lab}: {v:.2f}°", (bb, v), (bb + 0.12, v + 0.12), fontsize=8)
ax.set_xlabel("antenna baseline (m)"); ax.set_ylabel("heading 1σ (deg)"); ax.grid(alpha=.3); ax.set_ylim(0, 1.4)
ax.set_title("Dual-antenna heading improves with a longer baseline"); save(fig, "gq7_baseline")

# --- three-sensor comparison ---
labels = ["roll/pitch\n(deg)", "heading\n(deg)", "abs. horizontal\nposition (m)", "20-s coast\nerror (m)", "point at 20 m,\nhorizontal (m)"]
vals = {"3DM-GX5-25 AHRS": [0.25, 0.8, np.nan, 48, np.nan], "3DM-GX5-45 GNSS/INS": [0.25, 0.8, 2.0, 2.1, 2.02], "3DM-GQ7 (RTK)": [0.05, 0.25, 0.02, 1.0, 0.090]}
fig, ax = plt.subplots(figsize=(7.6, 3.4)); x = np.arange(len(labels)); w = 0.26
for i, ((k, v), c) in enumerate(zip(vals.items(), [ORANGE, PURPLE, NAVY])):
    ax.bar(x + (i - 1) * w, v, w, color=c, label=k)
ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8); ax.set_ylabel("1σ error (log scale)")
ax.text(2 - w, 0.012, "n/a", ha="center", fontsize=8, color=ORANGE); ax.text(4 - w, 0.012, "n/a", ha="center", fontsize=8, color=ORANGE)
ax.legend(fontsize=8, frameon=False, loc="upper left"); ax.grid(alpha=.3, axis="y", which="both"); ax.set_ylim(0.01, 200)
ax.set_title("Three sensors side by side (smaller is better)"); save(fig, "imu_compare")
print("figs5 done")

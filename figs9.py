from style import *
import csv, json
rng = np.random.default_rng(2026)
FT = 0.3048

# ---------------- NSRS timeline ----------------
fig, ax = plt.subplots(figsize=(9.5, 2.9))
events = [(2022.99, "Dec 31, 2022\nU.S. survey foot\ndeprecated", GRAY, 1),
          (2024.77, "Oct 9, 2024\nFederal Register:\nupdated timeline", NAVY, -1),
          (2025.5, "2025-2026\nbeta release and\npublic testing", TEAL, 1),
          (2026.9, "late 2026 / early 2027\nFGCS vote expected", ORANGE, -1),
          (2027.3, "early 2027\nadoption may extend\ninto this period", RED, 1),
          (2029.5, "within ~5 years\ntools and services\ncompleted", PURPLE, -1)]
ax.plot([2022.5, 2031], [0, 0], color="k", lw=2)
ax.axvspan(2025.0, 2027.0, ymin=0.45, ymax=0.55, color=TEAL, alpha=.35)
for x, t, c, s in events:
    ax.plot(x, 0, "o", color=c, ms=10, mec="k")
    ax.plot([x, x], [0, 0.55 * s], color=c, lw=1.2)
    ax.text(x, 0.6 * s + (0.0 if s > 0 else -0.05), t, ha="center", va="bottom" if s > 0 else "top", fontsize=8, color=c)
for y in range(2023, 2031):
    ax.text(y, -0.12, str(y), ha="center", va="top", fontsize=7.5, color=GRAY)
ax.text(2022.55, 0.12, "NAD 83 / NAVD 88 remain official until adoption", fontsize=8, color=NAVY)
ax.set_xlim(2022.4, 2031); ax.set_ylim(-1.4, 1.4); ax.axis("off")
ax.set_title("NSRS modernization: NATRF2022, NAPGD2022 (GEOID2022), SPCS2022", fontsize=10)
save(fig, "nsrs_timeline")

# ---------------- sample dataset ----------------
L = 2000.0
s = np.linspace(0, L, 2001)
E0, N0 = 165200.0, 402300.0
E = E0 + s * np.cos(np.radians(20)) + 40 * np.sin(s / 300)
N = N0 + s * np.sin(np.radians(20)) + 25 * np.sin(s / 450)
under = (s > 1100) & (s < 1400)
# trajectory standard deviations (cm)
sdH = 1.4 + 0.15 * rng.standard_normal(len(s)).cumsum() * 0 + 0.1 * np.sin(s / 90)
sdH = np.full_like(s, 1.4) + 0.1 * np.sin(s / 90)
sdV = np.full_like(s, 1.8) + 0.1 * np.cos(s / 120)
# growth inside underpass, reset by mid-point control at 1250
for a, b in [(1100, 1250), (1250, 1400)]:
    m = (s > a) & (s < b); u = (s[m] - a) / (b - a)
    bump = 2.2 * np.sin(np.pi * u)
    sdH[m] += bump; sdV[m] += 0.8 * bump
t0 = 0.0; v = 13.0
time = t0 + s / v
heading = np.degrees(np.arctan2(np.gradient(N), np.gradient(E)))
with open("figs/sample_trajectory.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["time_s", "station_m", "easting_m", "northing_m", "ellip_height_m", "heading_deg_ENU", "sd_horiz_cm", "sd_vert_cm", "gnss_status"])
    for i in range(0, len(s), 5):
        w.writerow([f"{time[i]:.2f}", f"{s[i]:.1f}", f"{E[i]:.3f}", f"{N[i]:.3f}", f"{-24.0 + 0.002*s[i]:.3f}", f"{heading[i]:.3f}", f"{sdH[i]:.2f}", f"{sdV[i]:.2f}", "OUTAGE" if under[i] else "RTK_FIXED"])

# control and checkpoints
ctrl_s = np.array([0, 250, 500, 750, 1000, 1100, 1250, 1400, 1650, 2000.])
chk_s = np.sort(np.r_[np.linspace(33, 1967, 30)])
def pos(st, side):
    i = np.searchsorted(s, st); i = min(i, len(s) - 1)
    hd = np.radians(heading[i]); off = side * 9.0
    return E[i] - off * np.sin(hd), N[i] + off * np.cos(hd)

# residuals with exact target statistics
def make(n, rmse, mean):
    x = rng.standard_normal(n); x = (x - x.mean()) / x.std()
    sd = np.sqrt(rmse ** 2 - mean ** 2)
    return np.round(mean + sd * x, 1)
dz = make(30, 1.9, 0.3); dx = make(30, 2.0, 0.1); dy = make(30, 1.7, -0.1)
rows = []
for k, st in enumerate(chk_s):
    side = 1 if k % 2 == 0 else -1
    e, n = pos(st, side)
    zs = 6.10 + 0.0025 * st + 0.15 * np.sin(st / 200)
    rows.append(dict(id=f"CP{k+1:02d}", station=st, e=e, n=n, side="R" if side > 0 else "L",
                     z_survey=zs, dz=dz[k], dx=dx[k], dy=dy[k]))
with open("figs/sample_checkpoints.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "station_m", "station_ft", "easting_m", "northing_m", "side", "survey_elev_m", "lidar_elev_m", "dZ_cm", "dZ_ft", "dE_cm", "dN_cm"])
    for r in rows:
        w.writerow([r["id"], f"{r['station']:.1f}", f"{r['station']/FT:.1f}", f"{r['e']:.3f}", f"{r['n']:.3f}", r["side"], f"{r['z_survey']:.3f}",
                    f"{r['z_survey'] + r['dz']/100:.3f}", f"{r['dz']:.1f}", f"{r['dz']/30.48:.3f}", f"{r['dx']:.1f}", f"{r['dy']:.1f}"])

stats = dict(n=30, mean_dz=float(np.mean(dz)), sd_dz=float(np.std(dz, ddof=1)), rmse_z=float(np.sqrt(np.mean(dz ** 2))),
             rmse_x=float(np.sqrt(np.mean(dx ** 2))), rmse_y=float(np.sqrt(np.mean(dy ** 2))), max_abs_dz=float(np.max(np.abs(dz))),
             sum_sq=float(np.sum(dz ** 2)))
stats["rmse_h"] = float(np.hypot(stats["rmse_x"], stats["rmse_y"]))
stats["rmse_z_final"] = float(np.hypot(stats["rmse_z"], 0.8)); stats["rmse_h_final"] = float(np.hypot(stats["rmse_h"], 1.0))
json.dump(stats, open("figs/sample_stats.json", "w"), indent=1)
print(stats)

# LaTeX table of checkpoints
with open("sample_table.tex", "w") as f:
    for r in rows:
        f.write(f"{r['id']} & {r['station']:.0f} / {r['station']/FT:.0f} & {r['side']} & {r['z_survey']:.3f} / {r['z_survey']/FT:.3f} & "
                f"{r['dz']:+.1f} / {r['dz']/30.48:+.3f} & {r['dx']:+.1f} & {r['dy']:+.1f}\\\\\n")

# ---------- trajectory figure ----------
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6.2), gridspec_kw=dict(height_ratios=[1.25, 1]))
a1.plot(E - E0, N - N0, color=NAVY, lw=2.5, label="trajectory (13 m/s, 2.0 km)")
a1.plot(E[under] - E0, N[under] - N0, color=RED, lw=4, label="underpass: GNSS outage (300 m)")
for st in ctrl_s:
    e, n = pos(st, 1 if st % 500 else -1); a1.plot(e - E0, n - N0, "^", color=GOLD, ms=9, mec="k")
for r in rows:
    a1.plot(r["e"] - E0, r["n"] - N0, "s", color=TEAL, ms=5, mec="k", mew=0.4)
a1.plot([], [], "^", color=GOLD, mec="k", label="control (10)"); a1.plot([], [], "s", color=TEAL, mec="k", label="checkpoints (30)")
a1.set_aspect("equal"); a1.set_xlabel("Easting offset (m)"); a1.set_ylabel("Northing offset (m)")
a1.legend(fontsize=8, loc="upper left", frameon=False); a1.grid(alpha=.3)
a1.set_title("Sample project: Main Street corridor (simulated dataset)", fontsize=10)
a2.fill_between(s, 0, 8, where=under, color=GRAY, alpha=.15)
a2.plot(s, sdH, color=NAVY, lw=2, label="trajectory 1σ horizontal"); a2.plot(s, sdV, color=ORANGE, lw=2, label="trajectory 1σ vertical")
a2.axvline(1250, color=GOLD, ls="--", lw=1); a2.text(1410, 4.4, "mid-underpass\ncontrol target", fontsize=8, color="#8a6d00")
a2.set_xlabel("station (m)   [0-2000 m = 0-6,562 ft]"); a2.set_ylabel("cm"); a2.set_ylim(0, 7); a2.grid(alpha=.3)
a2.legend(fontsize=8, frameon=False, loc="upper left"); a2.text(1250, 6.55, "underpass (GNSS outage)", ha="center", fontsize=8)
sec = a2.secondary_yaxis("right", functions=(lambda c: c / 30.48, lambda f: f * 30.48)); sec.set_ylabel("ft")
save(fig, "sample_trajectory")

# ---------- residual plot ----------
fig, ax = plt.subplots(figsize=(8.5, 2.9))
ax.bar(range(1, 31), dz, color=[TEAL if v >= 0 else ORANGE for v in dz])
ax.axhline(stats["rmse_z"], color=RED, ls="--"); ax.axhline(-stats["rmse_z"], color=RED, ls="--")
ax.text(0.3, stats["rmse_z"] + 0.2, f"±RMSE {stats['rmse_z']:.2f} cm", color=RED, fontsize=8, ha="left", bbox=dict(fc="white", ec="none", pad=1))
ax.set_xticks(range(1, 31)); ax.tick_params(axis="x", labelsize=7); ax.set_xlabel("checkpoint"); ax.set_ylabel("LiDAR - survey (cm)")
sec = ax.secondary_yaxis("right", functions=(lambda c: c / 30.48, lambda f: f * 30.48)); sec.set_ylabel("ft")
ax.set_title("Sample project: 30 vertical checkpoint residuals"); save(fig, "sample_residuals")
print("figs9 done")

from style import *
d = np.deg2rad; R = 152.4; FT = 0.3048

def plane(ax, x, y, s=1.0):
    ax.add_patch(Polygon([[x - 14 * s, y], [x + 14 * s, y + 1.5 * s], [x + 14 * s, y - 1.5 * s]], fc=NAVY))
    ax.add_patch(Polygon([[x - 3 * s, y], [x + 4 * s, y + 9 * s], [x + 6 * s, y + 9 * s], [x + 3 * s, y]], fc=NAVY))
    ax.add_patch(Rectangle((x - 3 * s, y - 4 * s), 6 * s, 3.5 * s, fc=ORANGE, ec="k"))

# ---------- geometry ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.4))
for ax, H, title in [(a1, R, "Case A: nadir return, 500 ft (152.4 m) AGL"), (a2, R * np.cos(d(37.5)), "Case B: 500 ft slant return at the 37.5° FOV edge")]:
    ax.set_aspect("equal"); ax.axis("off")
    ax.plot([-140, 140], [0, 0], color="#6e4b2a", lw=3)
    ax.fill_between([-140, 140], -12, 0, color="#d7ccc8")
    plane(ax, 0, H + 6, 1.4)
    for a in np.linspace(-37.5, 37.5, 13):
        ax.plot([0, H * np.tan(d(a))], [H, 0], color=RED, lw=0.6, alpha=.35)
    if ax is a1:
        ax.plot([0, 0], [H, 0], color=RED, lw=2.5); ax.text(4, H / 2, "range = 500 ft\n(152.4 m)", color=RED, fontsize=9)
        ax.add_patch(Ellipse((0, 0), 5.3, 2.0, fc=ORANGE, ec="k")); ax.text(8, 5, "spot 5.3 cm wide", fontsize=7.5)
    else:
        xe = H * np.tan(d(37.5)); ax.plot([0, xe], [H, 0], color=RED, lw=2.5)
        ax.text(xe / 2 + 6, H / 2, "slant range\n= 500 ft", color=RED, fontsize=9)
        ax.plot([0, 0], [H, 0], color=GRAY, ls="--"); ax.text(-135, H * 0.8, f"AGL = {H/FT:.0f} ft\n({H:.1f} m)", fontsize=8.5, color=GRAY)
        ax.add_patch(Arc((0, H), 60, 60, theta1=270, theta2=270 + 37.5, color="k")); ax.text(3, H - 40, "37.5°", fontsize=8.5)
    ax.annotate("", (-H * np.tan(d(37.5)), -6), (H * np.tan(d(37.5)), -6), arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -11.5, f"swath {2*H*np.tan(d(37.5)):.0f} m", ha="center", fontsize=8)
    ax.set_xlim(-140, 140); ax.set_ylim(-16, R + 25); ax.set_title(title, fontsize=9.5)
save(fig, "riegl_geometry")

# ---------- attitude -> ground displacement ----------
opts = ["RiLOC-F", "AP+30", "AP+50", "AP+60"]
rp = [0.005, 0.010, 0.005, 0.0025]; hd = [0.005, 0.025, 0.010, 0.005]
fig, ax = plt.subplots(figsize=(7.2, 3.3)); x = np.arange(4); w = 0.36
b1 = ax.bar(x - w / 2, [R * d(v) * 100 for v in rp], w, color=PURPLE, label="roll / pitch accuracy")
b2 = ax.bar(x + w / 2, [R * d(v) * 100 for v in hd], w, color=TEAL, label="heading accuracy")
for bars, vals in [(b1, rp), (b2, hd)]:
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.1, f"{v}°\n{R*d(v)*100:.1f} cm", ha="center", fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels(opts); ax.set_ylabel("displacement at 500 ft (cm)"); ax.set_ylim(0, 8.5)
ax.legend(fontsize=8, frameon=False, loc="upper right"); ax.grid(alpha=.3, axis="y")
ax.set_title("Post-processed IMU attitude accuracy, projected to a 500 ft return"); save(fig, "riegl_imu")

# ---------- error budget bars (RiLOC-F) ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
names = ["GNSS\nposition", "roll/\npitch", "heading", "laser\nrange", "bore-\nsight", "lever\narm", "angle\nencoder", "TOTAL\n(RSS)"]
nadirH = [2.5, 1.88, 0.0, 0.0, 1.88, 0.71, 0.08, 3.72]; nadirV = [3.75, 0.0, 0.0, 2.5, 0.0, 0.5, 0.0, 4.53]
edgeH = [2.5, 1.49, 0.81, 1.52, 1.70, 0.71, 0.06, 3.85]; edgeV = [3.75, 0.81, 0.0, 1.98, 0.81, 0.5, 0.05, 4.42]
for ax, Hh, Vv, t in [(a1, nadirH, nadirV, "Case A: nadir"), (a2, edgeH, edgeV, "Case B: 37.5° edge")]:
    xx = np.arange(len(names)); ww = 0.38
    ax.bar(xx - ww / 2, Hh, ww, color=NAVY, label="horizontal")
    ax.bar(xx + ww / 2, Vv, ww, color=ORANGE, label="vertical")
    ax.set_xticks(xx); ax.set_xticklabels(names, fontsize=7.5); ax.set_title(t + " (RiLOC-F, 500 ft return)", fontsize=9.5); ax.grid(alpha=.3, axis="y")
    ax.axhline(5, color="k", ls="--", lw=1); ax.text(-0.4, 5.15, "5 cm class", fontsize=7.5)
a1.set_ylabel("1σ (cm)"); a1.legend(fontsize=8, frameon=False, loc="upper center"); a1.set_ylim(0, 6)
save(fig, "riegl_budget")

# ---------- totals per IMU option ----------
totH = {"RiLOC-F": (3.72, 3.85), "AP+30": (5.52, 6.58), "AP+50": (4.45, 4.77), "AP+60": (4.14, 4.38)}
totV = {"RiLOC-F": (4.53, 4.42), "AP+30": (5.84, 5.92), "AP+50": (5.84, 5.75), "AP+60": (5.84, 5.71)}
fig, ax = plt.subplots(figsize=(7.4, 3.3)); x = np.arange(4); w = 0.2
for k, (lab, c, data, idx) in enumerate([("H nadir", NAVY, totH, 0), ("H edge", SKY, totH, 1), ("V nadir", ORANGE, totV, 0), ("V edge", GOLD, totV, 1)]):
    ax.bar(x + (k - 1.5) * w, [data[o][idx] for o in opts], w, color=c, label=lab)
ax.axhline(5, color="k", ls="--", lw=1)
ax.set_xticks(x); ax.set_xticklabels(opts); ax.set_ylabel("total 1σ (cm)"); ax.set_ylim(0, 7.5); ax.grid(alpha=.3, axis="y")
ax.legend(fontsize=8, frameon=False, ncol=4, loc="upper left"); ax.set_title("Direct-georeferencing totals at 500 ft (before control / strip adjustment)", fontsize=10)
save(fig, "riegl_totals")

# ---------- MTA ----------
fig, ax = plt.subplots(figsize=(8, 2.4))
c = 299792458 / 1.0003; zone = c / (2 * 2.4e6)
for k in range(4):
    ax.axvspan(k * zone, (k + 1) * zone, color=[SKY, TEAL, ORANGE, PURPLE][k], alpha=.18)
    ax.text((k + 0.5) * zone, 0.75, f"MTA zone {k+1}\n{k*zone:.0f}-{(k+1)*zone:.0f} m", ha="center", fontsize=8)
ax.plot([152.4], [0.3], "v", ms=14, color=RED); ax.text(152.4, 0.1, "target at 500 ft (152.4 m)\n= zone 3", ha="center", fontsize=8, color=RED)
ax.set_xlim(0, 4 * zone); ax.set_ylim(0, 1.05); ax.set_yticks([]); ax.set_xlabel("range (m) at 2,400 kHz pulse rate")
ax.set_title("Multiple-time-around: two earlier pulses are still in the air when this echo returns", fontsize=10)
save(fig, "riegl_mta")
print("figs8 done")

def rot_zyx(B, p, roll, pitch, yaw, label):
    """Add the 9 entries of R = Rz(yaw) Ry(pitch) Rx(roll); angle placeholders in degrees."""
    cf, sf = f"COS(RADIANS({{{roll}}}))", f"SIN(RADIANS({{{roll}}}))"
    ct, st = f"COS(RADIANS({{{pitch}}}))", f"SIN(RADIANS({{{pitch}}}))"
    cp, sp = f"COS(RADIANS({{{yaw}}}))", f"SIN(RADIANS({{{yaw}}}))"
    E = {"11": f"{cp}*{ct}", "12": f"{cp}*{st}*{sf}-{sp}*{cf}", "13": f"{cp}*{st}*{cf}+{sp}*{sf}",
         "21": f"{sp}*{ct}", "22": f"{sp}*{st}*{sf}+{cp}*{cf}", "23": f"{sp}*{st}*{cf}-{cp}*{sf}",
         "31": f"-{st}", "32": f"{ct}*{sf}", "33": f"{ct}*{cf}"}
    return E


def add(B):
    # ================= Module 2 =================
    B.sheet("M02 Math", "Module 2 — Math Toolkit: worked examples", "2")
    B.ex("multiplying with powers of ten", "c = 2.997×10⁸ m/s, t = 4.00×10⁻⁷ s. Find c×t.")
    B.I("c", "Speed c", 2.997e8, "m/s"); B.I("t", "Time t", 4.0e-7, "s")
    B.C("ct", "c × t", "{c}*{t}", "m", "c·t = 2.997×4.00 × 10^(8−7)", 119.88, 0.005, "0.000")

    B.ex("a tiny angle at a long range", "Aiming error 20 arc-seconds at 100 m.")
    B.I("a", "Angle", 20, "arc-sec"); B.I("d", "Distance", 100, "m")
    B.C("deg", "Seconds to degrees", "{a}/3600", "deg", "a/3600", 0.005556, 1e-6, "0.000000")
    B.C("rad", "Degrees to radians", "RADIANS({deg})", "rad", "deg × π/180", 9.70e-5, 5e-7, "0.000E+00")
    B.C("s", "Arc length (sideways)", "{d}*{rad}", "m", "s = d·θ (rad)", 0.0097, 5e-5, "0.0000")

    B.ex("a 3-4-5 triangle", "Slope distance 5.000 m at 36.87° above horizontal.")
    B.I("L", "Slope distance", 5.0, "m"); B.I("ang", "Angle above horizontal", 36.87, "deg")
    B.C("x", "Across", "{L}*COS(RADIANS({ang}))", "m", "L cos θ", 4.000, 0.0005, "0.000")
    B.C("z", "Up", "{L}*SIN(RADIANS({ang}))", "m", "L sin θ", 3.000, 0.0005, "0.000")
    B.C("chk", "Check: length", "SQRT({x}^2+{z}^2)", "m", "√(x²+z²)", 5.000, 0.0005, "0.000")

    B.ex("dot and cross products", "a = (1, 2, 0), b = (3, 0, 0).")
    for i, v in zip("123", (1, 2, 0)): B.I("a" + i, f"a{i}", v)
    for i, v in zip("123", (3, 0, 0)): B.I("b" + i, f"b{i}", v)
    B.C("dot", "Dot product a·b", "{a1}*{b1}+{a2}*{b2}+{a3}*{b3}", "", "a1b1+a2b2+a3b3", 3, 1e-9, "0.00")
    B.C("cx", "Cross x", "{a2}*{b3}-{a3}*{b2}", "", "a2b3 − a3b2", 0, 1e-9, "0.00")
    B.C("cy", "Cross y", "{a3}*{b1}-{a1}*{b3}", "", "a3b1 − a1b3", 0, 1e-9, "0.00")
    B.C("cz", "Cross z", "{a1}*{b2}-{a2}*{b1}", "", "a1b2 − a2b1", -6, 1e-9, "0.00")
    B.C("area", "Parallelogram area |a×b|", "SQRT({cx}^2+{cy}^2+{cz}^2)", "", "‖a×b‖", 6, 1e-9, "0.00")
    B.C("nb", "Base |b|", "SQRT({b1}^2+{b2}^2+{b3}^2)", "", "‖b‖", 3, 1e-9, "0.00")
    B.C("h", "Point-to-line distance (height)", "{area}/{nb}", "", "‖a×b‖/‖b‖", 2, 1e-9, "0.00")

    B.ex("matrix times vector", "M = [[2,0,1],[0,1,0],[1,0,3]], v = (1, 4, 2).")
    M = [[2, 0, 1], [0, 1, 0], [1, 0, 3]]
    for i in range(3):
        for j in range(3):
            B.I(f"m{i+1}{j+1}", f"M{i+1}{j+1}", M[i][j])
    for i, v in enumerate((1, 4, 2)): B.I(f"v{i+1}", f"v{i+1}", v)
    for i, bk in enumerate((4, 4, 7)):
        B.C(f"r{i+1}", f"Result row {i+1}", "+".join(f"{{m{i+1}{j+1}}}*{{v{j+1}}}" for j in range(3)), "",
            f"Σ M{i+1}j·vj", bk, 1e-9, "0.00")

    B.ex("five elevation errors", "Errors +2, −1, +3, 0, +1 cm.")
    for i, v in enumerate((2, -1, 3, 0, 1)): B.I(f"e{i+1}", f"Error {i+1}", v, "cm")
    B.C("n", "Count n", "COUNT({e1:e5})", "", "n", 5, 1e-9, "0")
    B.C("mean", "Mean (bias)", "AVERAGE({e1:e5})", "cm", "ē = Σe/n", 1.0, 0.005, "0.00")
    B.C("s", "Standard deviation (n−1)", "STDEV({e1:e5})", "cm", "s = √(Σ(e−ē)²/(n−1))", 1.58, 0.005, "0.00")
    B.C("rmse", "RMSE", "SQRT(SUMSQ({e1:e5})/{n})", "cm", "√(Σe²/n)", 1.73, 0.005, "0.00")
    B.C("chk", "Check: ē² + s²(n−1)/n", "{mean}^2+{s}^2*({n}-1)/{n}", "cm²", "= RMSE²", 3.0, 1e-6, "0.000")

    # ================= Module 3 =================
    B.sheet("M03 Time of Flight", "Module 3 — Time of Flight and Phase: worked examples", "3")
    B.ex("range from a 400 ns echo", "Δt = 400 ns; standard air n = 1.000300.")
    B.I("c0", "Speed of light in vacuum", 299792458, "m/s"); B.I("n", "Refractive index of air", 1.0003)
    B.I("dt", "Round-trip time", 400, "ns")
    B.C("c", "Speed of light in air", "{c0}/{n}", "m/s", "c = c0/n", 299702547, 1, "#,##0")
    B.C("dts", "Time in seconds", "{dt}*1E-9", "s", "ns × 10⁻⁹", 4.0e-7, 1e-12, "0.00E+00")
    B.C("path", "Round-trip path", "{c}*{dts}", "m", "c·Δt", 119.881, 0.0005, "0.000")
    B.C("rho", "Range", "{path}/2", "m", "ρ = c·Δt/2", 59.941, 0.0005, "0.000")

    B.ex("how fast can we fire?", "PRF = 1 MHz, c = 2.997×10⁸ m/s.")
    B.I("prf", "Pulse repetition frequency", 1e6, "Hz"); B.I("c", "Speed of light", 2.997e8, "m/s")
    B.C("T", "Time between pulses", "1/{prf}", "s", "1/PRF", 1e-6, 1e-12, "0.00E+00")
    B.C("rmax", "Maximum unambiguous range", "{c}/(2*{prf})", "m", "ρmax = c/(2·PRF)", 149.9, 0.051, "0.0")
    B.C("rmax2", "At double the rate (2 MHz)", "{c}/(2*2*{prf})", "m", "c/(2·2PRF)", 74.9, 0.05, "0.0")

    B.ex("phase measurement", "fm = 10 MHz, Δφ = 90°, c = 2.997×10⁸ m/s, N = 0.")
    B.I("fm", "Modulation frequency", 1e7, "Hz"); B.I("dphi", "Phase difference", 90, "deg")
    B.I("c", "Speed of light", 2.997e8, "m/s"); B.I("N", "Whole cycles N", 0)
    B.C("lam", "Modulation wavelength", "{c}/{fm}", "m", "λm = c/fm", 29.97, 0.005, "0.000")
    B.C("half", "Half-wavelength", "{lam}/2", "m", "λm/2", 14.985, 0.0005, "0.000")
    B.C("frac", "Fraction of a cycle", "{dphi}/360", "", "Δφ/2π", 0.25, 1e-9, "0.00")
    B.C("rho", "Range", "{half}*({N}+{frac})", "m", "ρ = (λm/2)(N + Δφ/2π)", 3.746, 0.0005, "0.000")
    B.C("alt1", "Ambiguous alternative N+1", "{rho}+{half}", "m", "ρ + λm/2", 18.731, 0.0005, "0.000")
    B.C("alt2", "Ambiguous alternative N+2", "{rho}+2*{half}", "m", "ρ + 2·λm/2", 33.716, 0.0005, "0.000")

    # ================= Module 4 =================
    B.sheet("M04 Beam", "Module 4 — Beam, Footprint and Reflectivity: worked examples", "4")
    B.ex("spot size at 50 m and 100 m", "d0 = 5 mm, γ = 0.3 mrad.")
    B.I("d0", "Exit diameter", 0.005, "m"); B.I("g", "Divergence", 0.3, "mrad")
    B.I("R1", "Range 1", 50, "m"); B.I("R2", "Range 2", 100, "m")
    B.C("D1", "Footprint at range 1", "{d0}+{R1}*{g}/1000", "m", "D = d0 + ρ·γ", 0.020, 0.0005, "0.000")
    B.C("D2", "Footprint at range 2", "{d0}+{R2}*{g}/1000", "m", "D = d0 + ρ·γ", 0.035, 0.0005, "0.000")

    B.ex("comparing two targets", "A: white concrete 0.6 at 10 m head-on; B: asphalt 0.1 at 50 m, 60° incidence.")
    B.I("rA", "Reflectivity A", 0.6); B.I("RA", "Range A", 10, "m"); B.I("iA", "Incidence A", 0, "deg")
    B.I("rB", "Reflectivity B", 0.1); B.I("RB", "Range B", 50, "m"); B.I("iB", "Incidence B", 60, "deg")
    B.C("ratio", "Power ratio PB/PA", "({rB}/{rA})*(COS(RADIANS({iB}))/COS(RADIANS({iA})))*({RA}^2/{RB}^2)", "",
        "(ρB/ρA)(cos θB/cos θA)(RA²/RB²)", 0.00333, 5e-6, "0.00000")
    B.C("inv", "A returns this many times more", "1/{ratio}", "×", "1/ratio", 300, 1, "0")

    B.ex("how far can I see dark asphalt?", "OS0 sees a 10% target to 35 m; max range ∝ √reflectivity.")
    B.I("R10", "Range on 10% target", 35, "m"); B.I("ref0", "Reference reflectivity", 10, "%")
    for nm, lab, v, bk in (("asph", "Fresh asphalt", 5, 25), ("car", "Black car", 4, 22), ("conc", "Concrete", 40, 70)):
        B.I(nm, f"{lab} reflectivity", v, "%")
        B.C("R" + nm, f"Max range on {lab.lower()}", f"{{R10}}*SQRT({{{nm}}}/{{ref0}})", "m", "R = R10·√(ρ/10%)", bk, 0.5, "0.0")

    # ================= Module 5 =================
    B.sheet("M05 Polar", "Module 5 — Polar to Cartesian and Point Spacing: worked examples", "5")
    B.ex("one laser return to sensor coordinates", "ρ = 25.000 m, H = 40.0°, V = 15.0°; x forward, y left, z up.")
    B.I("rho", "Range ρ", 25.0, "m"); B.I("H", "Horizontal angle H", 40.0, "deg"); B.I("V", "Vertical angle V", 15.0, "deg")
    B.C("hor", "Horizontal part ρ cos V", "{rho}*COS(RADIANS({V}))", "m", "ρ cos V", 24.148, 0.0005, "0.000")
    B.C("x", "x_s", "{hor}*COS(RADIANS({H}))", "m", "ρ cos V cos H", 18.499, 0.0005, "0.000")
    B.C("y", "y_s", "{hor}*SIN(RADIANS({H}))", "m", "ρ cos V sin H", 15.522, 0.0005, "0.000")
    B.C("z", "z_s", "{rho}*SIN(RADIANS({V}))", "m", "ρ sin V", 6.470, 0.0005, "0.000")
    B.C("chk", "Check: length", "SQRT({x}^2+{y}^2+{z}^2)", "m", "√(x²+y²+z²) = ρ", 25.000, 0.0005, "0.000")

    B.ex("planning a corridor survey", "16 channels, 0.2° step, 10 Hz, 15 m/s, target 20 m away.")
    B.I("ch", "Channels", 16); B.I("step", "Horizontal step", 0.2, "deg"); B.I("f", "Rotation rate", 10, "Hz")
    B.I("v", "Speed", 15, "m/s"); B.I("R", "Range to target", 20, "m"); B.I("v2", "Slower speed", 5, "m/s")
    B.C("along", "Along-track spacing", "{v}/{f}", "m", "Δalong = v/f", 1.5, 0.0005, "0.000")
    B.C("across", "Across-track spacing", "{R}*RADIANS({step})", "m", "Δacross = ρ·Δθ", 0.070, 0.0005, "0.000")
    B.C("naz", "Azimuth samples per rotation", "360/{step}", "", "360/Δθ", 1800, 1e-6, "#,##0")
    B.C("N", "Point rate", "{ch}*{naz}*{f}", "pts/s", "N = channels × Naz × f", 288000, 1e-6, "#,##0")
    B.C("along2", "Along-track spacing at slower speed", "{v2}/{f}", "m", "v2/f", 0.5, 0.0005, "0.000")

    # ================= Module 6 =================
    B.sheet("M06 Rotation", "Module 6 — Pose, Right-Hand Rule and Rotations: worked examples", "6")
    B.ex("checking a frame with the cross product", "Datasheet: X forward, Y right, Z up. In FLU, forward=(1,0,0), right=(0,−1,0).")
    for i, v in zip("123", (1, 0, 0)): B.I("f" + i, f"Forward axis component {i}", v)
    for i, v in zip("123", (0, -1, 0)): B.I("r" + i, f"Right axis component {i}", v)
    B.C("zx", "X × Y, x", "{f2}*{r3}-{f3}*{r2}", "", "cross product", 0, 1e-9, "0")
    B.C("zy", "X × Y, y", "{f3}*{r1}-{f1}*{r3}", "", "cross product", 0, 1e-9, "0")
    B.C("zz", "X × Y, z (thumb)", "{f1}*{r2}-{f2}*{r1}", "", "−1 = thumb points down", -1, 1e-9, "0")
    B.T("Result: Z = X × Y points DOWN, so 'X forward, Y right, Z up' is left-handed. Confirm FRD with the manufacturer.")

    B.ex("rotate (3, 4) by 30°")
    B.I("x", "x", 3); B.I("y", "y", 4); B.I("a", "Rotation angle", 30, "deg")
    B.C("x2", "x′", "COS(RADIANS({a}))*{x}-SIN(RADIANS({a}))*{y}", "", "x cos α − y sin α", 0.598, 0.0005, "0.000")
    B.C("y2", "y′", "SIN(RADIANS({a}))*{x}+COS(RADIANS({a}))*{y}", "", "x sin α + y cos α", 4.964, 0.0005, "0.000")
    B.C("L", "Length after (check)", "SQRT({x2}^2+{y2}^2)", "", "unchanged = 5", 5.000, 0.0005, "0.000")

    B.ex("one gyro step", "ωz = 0.0842 rad/s, Δt = 0.005 s (200 Hz), start heading 0.")
    B.I("w", "Yaw rate ωz", 0.0842, "rad/s"); B.I("dt", "Time step", 0.005, "s"); B.I("n", "Steps (1 s)", 200)
    B.C("a", "Rotation in one step", "{w}*{dt}", "rad", "α = ω·Δt", 0.000421, 5e-7, "0.000000")
    B.C("ad", "In degrees", "DEGREES({a})", "deg", "", 0.0241, 5e-5, "0.0000")
    B.C("ca", "cos α", "COS({a})", "", "", 0.99999991, 1e-8, "0.00000000")
    B.C("h1", "Heading after 200 steps", "{n}*{a}", "rad", "Σα", 0.0842, 1e-6, "0.0000")
    B.C("h1d", "In degrees", "DEGREES({h1})", "deg", "", 4.82, 0.005, "0.00")

    B.ex("0.05° heading error at 80 m")
    B.I("e", "Heading error", 0.05, "deg"); B.I("R", "Range", 80, "m")
    B.C("rad", "Radians", "RADIANS({e})", "rad", "deg × π/180", 0.0008727, 1e-7, "0.0000000")
    B.C("d", "Sideways displacement", "{R}*{rad}", "m", "δ = ρ·δα", 0.0698, 5e-5, "0.0000")
    B.C("d100", "Same error at 100 m", "100*{rad}*100", "cm", "100 m × δα", 8.7, 0.05, "0.00")
    B.C("d01", "0.1° at 100 m", "100*RADIANS(0.1)*100", "cm", "100 m × 0.1°", 17.5, 0.06, "0.00")

    # ================= Module 7 =================
    B.sheet("M07 IMU", "Module 7 — IMU and Strapdown Navigation: worked examples", "7")
    B.ex("one strapdown step along a road", "100 Hz; level; v = 15.000 m/s; x = 100.000 m; âx = 0.80, âz = 9.81 m/s².")
    B.I("dt", "Time step", 0.01, "s"); B.I("v", "Velocity", 15.0, "m/s"); B.I("x", "Position", 100.0, "m")
    B.I("ax", "Accelerometer x", 0.80, "m/s²"); B.I("az", "Accelerometer z", 9.81, "m/s²"); B.I("g", "Gravity", 9.81, "m/s²")
    B.C("dvz", "Vertical velocity change", "(-{g}+{az})*{dt}", "m/s", "(g + âz)Δt, g = −9.81", 0, 1e-9, "0.000")
    B.C("v2", "New forward velocity", "{v}+{ax}*{dt}", "m/s", "v + âΔt", 15.008, 0.0005, "0.000")
    B.C("x2", "New forward position", "{x}+{v}*{dt}+0.5*{ax}*{dt}^2", "m", "x + vΔt + ½âΔt²", 100.15004, 5e-6, "0.00000")
    B.C("dv", "Speed-up", "{ax}*{dt}*1000", "mm/s", "âΔt", 8, 1e-6, "0.0")

    B.ex("tactical IMU coasting through a tunnel", "Gyro bias 1°/h, accel bias 0.5 mg, 15 m/s, 60 s unaided.")
    B.I("bg", "Gyro bias", 1, "deg/h"); B.I("ba", "Accel bias", 0.5, "mg"); B.I("v", "Speed", 15, "m/s")
    B.I("T", "Outage", 60, "s"); B.I("g", "Standard gravity", 9.80665, "m/s²"); B.I("T2", "Shorter outage", 30, "s")
    B.C("bgr", "Gyro bias in rad/s", "RADIANS({bg}/3600)", "rad/s", "(1/3600)°/s × π/180", 4.848e-6, 1e-9, "0.000E+00")
    B.C("hd", "Heading error", "{bgr}*{T}", "rad", "bg·t", 2.909e-4, 1e-7, "0.000E+00")
    B.C("hdd", "Heading error (deg)", "DEGREES({hd})", "deg", "", 0.0167, 5e-5, "0.0000")
    B.C("side", "Sideways error", "0.5*{v}*{bgr}*{T}^2", "m", "½·v·bg·t²", 0.131, 0.0005, "0.000")
    B.C("bam", "Accel bias in m/s²", "{ba}*0.001*{g}", "m/s²", "mg × 10⁻³ × g", 0.004903, 1e-6, "0.000000")
    B.C("along", "Along-track error", "0.5*{bam}*{T}^2", "m", "½·ba·t²", 8.83, 0.005, "0.00")
    B.C("along30", "Along-track error after 30 s", "0.5*{bam}*{T2}^2", "m", "½·ba·t²", 2.2, 0.05, "0.00")

    B.ex("0.1° tilt error")
    B.I("tilt", "Tilt error", 0.1, "deg"); B.I("g", "Gravity", 9.80665, "m/s²"); B.I("t", "Time", 10, "s")
    B.C("leak", "Leaked acceleration", "{g}*SIN(RADIANS({tilt}))", "m/s²", "g sin δθ", 0.01712, 1e-5, "0.00000")
    B.C("mg", "In mg", "{leak}/{g}*1000", "mg", "", 1.7, 0.05, "0.0")
    B.C("err", "Position error after t", "0.5*{leak}*{t}^2", "m", "½·a·t²", 0.86, 0.005, "0.00")

    B.ex("preintegration in one dimension", "10 IMU samples at 100 Hz, â = 0.50 m/s², vi = 12.000 m/s.")
    B.I("n", "Samples", 10); B.I("f", "IMU rate", 100, "Hz"); B.I("a", "Acceleration", 0.5, "m/s²"); B.I("vi", "vi", 12.0, "m/s")
    B.C("dt", "Sample interval", "1/{f}", "s", "1/f", 0.01, 1e-9, "0.000")
    B.C("dtij", "Δt_ij", "{n}*{dt}", "s", "n·δt", 0.1, 1e-9, "0.000")
    B.C("dv", "Δv_ij", "{n}*{a}*{dt}", "m/s", "Σ â δt", 0.050, 1e-6, "0.000")
    B.C("dp", "Δp_ij", "0.5*{a}*{dtij}^2", "m", "½ â Δt_ij²", 0.0025, 1e-7, "0.0000")
    B.C("vj", "vj", "{vi}+{dv}", "m/s", "vi + Δv", 12.050, 1e-6, "0.000")
    B.C("pp", "pj − pi", "{vi}*{dtij}+{dp}", "m", "vi Δt + Δp", 1.2025, 1e-6, "0.0000")

    # ================= Module 8 =================
    B.sheet("M08 Timing", "Module 8 — Timing and De-skew: worked examples", "8")
    B.ex("a 1 ms clock offset", "δt = 1 ms; 20 m/s; turning 30°/s; point 50 m away.")
    B.I("dt", "Clock offset", 0.001, "s"); B.I("v", "Speed", 20, "m/s"); B.I("w", "Turn rate", 30, "deg/s"); B.I("R", "Range", 50, "m")
    B.C("along", "Along-track error", "{v}*{dt}", "m", "v·δt", 0.020, 0.0005, "0.000")
    B.C("rot", "Rotation during offset", "RADIANS({w}*{dt})", "rad", "ω·δt", 0.000524, 5e-7, "0.000000")
    B.C("side", "Sideways error at range", "{R}*{rot}", "m", "ρ·ω·δt", 0.026, 0.0005, "0.000")

    B.ex("how big is the skew?", "10 Hz sweep, 15 m/s, point fired 0.075 s into the sweep.")
    B.I("f", "Sweep rate", 10, "Hz"); B.I("v", "Speed", 15, "m/s"); B.I("tau", "Time into sweep", 0.075, "s")
    B.C("T", "Sweep period", "1/{f}", "s", "1/f", 0.1, 1e-9, "0.000")
    B.C("d", "Distance moved by this point", "{v}*{tau}", "m", "v·τ", 1.125, 0.0005, "0.000")
    B.C("full", "First-to-last difference", "{v}*{T}", "m", "v·T", 1.5, 0.0005, "0.000")

    # ================= Module 9 =================
    B.sheet("M09 Calibration", "Module 9 — Lever Arm, Boresight and Direct Georeferencing: worked examples", "9")
    B.ex("boresight residual at mapping range", "Residual boresight 0.05°; target 80 m away.")
    B.I("b", "Boresight residual", 0.05, "deg"); B.I("R", "Range", 80, "m")
    B.C("rad", "Radians", "RADIANS({b})", "rad", "", 8.727e-4, 1e-7, "0.000E+00")
    B.C("d", "Displacement", "{R}*{rad}", "m", "ρ·δα", 0.0698, 5e-5, "0.0000")

    B.ex("direct georeferencing, every step",
         "FLU body, ENU world, ZYX angles. pW = (1000, 2000, 10) m; roll 1.0°, pitch −0.5°, yaw 30.0°; "
         "lever arm (0.120, 0, 0.085) m; boresight (0.05°, −0.03°, 0.02°); ρ = 25.000 m, H = 10.0°, V = 2.0°. "
         "The workbook uses exact rotation matrices; the book used the small-angle form for boresight.")
    for nm, lab, v in (("pE", "IMU position E", 1000.0), ("pN", "IMU position N", 2000.0), ("pU", "IMU position U", 10.0)):
        B.I(nm, lab, v, "m")
    B.I("roll", "Roll", 1.0, "deg"); B.I("pitch", "Pitch", -0.5, "deg"); B.I("yaw", "Yaw", 30.0, "deg")
    B.I("lx", "Lever arm x", 0.120, "m"); B.I("ly", "Lever arm y", 0.0, "m"); B.I("lz", "Lever arm z", 0.085, "m")
    B.I("bph", "Boresight roll", 0.05, "deg"); B.I("bth", "Boresight pitch", -0.03, "deg"); B.I("bps", "Boresight yaw", 0.02, "deg")
    B.I("rho", "Range", 25.0, "m"); B.I("H", "Horizontal angle", 10.0, "deg"); B.I("V", "Vertical angle", 2.0, "deg")
    B.C("xs", "Step 1: x_S", "{rho}*COS(RADIANS({V}))*COS(RADIANS({H}))", "m", "ρ cos V cos H", 24.6052, 5e-5)
    B.C("ys", "Step 1: y_S", "{rho}*COS(RADIANS({V}))*SIN(RADIANS({H}))", "m", "ρ cos V sin H", 4.3386, 5e-5)
    B.C("zs", "Step 1: z_S", "{rho}*SIN(RADIANS({V}))", "m", "ρ sin V", 0.8725, 5e-5)
    Rb = rot_zyx(B, "", "bph", "bth", "bps", "")
    for k, f in Rb.items():
        B.C("b" + k, f"Step 2: boresight R{k}", f, "", "Rz(δψ)Ry(δθ)Rx(δφ)", None, None, "0.000000")
    for i, (nm, bk) in enumerate((("xb", 24.6032), ("yb", 4.3464), ("zb", 0.8892)), 1):
        B.C(nm, f"Step 2: rotated point, axis {i}", f"{{b{i}1}}*{{xs}}+{{b{i}2}}*{{ys}}+{{b{i}3}}*{{zs}}", "m", "R^B_S · x_S", bk, 2e-4)
    for nm, a, l, bk in (("rx", "xb", "lx", 24.7232), ("ry", "yb", "ly", 4.3464), ("rz", "zb", "lz", 0.9742)):
        B.C(nm, f"Step 3: add lever arm ({nm[1]})", f"{{{a}}}+{{{l}}}", "m", "r_B = R x_S + l", bk, 2e-4)
    Ra = rot_zyx(B, "", "roll", "pitch", "yaw", "")
    bkR = {"11": 0.86599, "12": -0.50006, "13": 0.00117, "21": 0.49998, "22": 0.86582, "23": -0.01948,
           "31": 0.00873, "32": 0.01745, "33": 0.99981}
    for k, f in Ra.items():
        B.C("R" + k, f"Step 4: attitude R{k}", f, "", "Rz(ψ)Ry(θ)Rx(φ)", bkR[k], 6e-6, "0.00000")
    for i, (nm, bk) in enumerate((("X", 19.2378), ("Y", 16.1053), ("Z", 1.2656)), 1):
        B.C(nm, f"Step 4: rotated to world, {nm}", f"{{R{i}1}}*{{rx}}+{{R{i}2}}*{{ry}}+{{R{i}3}}*{{rz}}", "m", "R^W_B · r_B", bk, 2e-4)
    for nm, a, p, bk in (("E", "X", "pE", 1019.238), ("N", "Y", "pN", 2016.105), ("U", "Z", "pU", 11.266)):
        B.C("W" + nm, f"Step 5: world coordinate {nm}", f"{{{p}}}+{{{a}}}", "m", "r_W = p_W + R r_B", bk, 6e-4, "0.000")

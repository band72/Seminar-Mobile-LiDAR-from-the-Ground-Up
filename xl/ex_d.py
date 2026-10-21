def add(B):
    # ================= Module 16 =================
    B.sheet("M16 GX5-GQ7", "Module 16 — MicroStrain 3DM-GX5 / GQ7 Case Study: worked examples", "16")
    B.ex("the GX5's random walks", "Gyro noise density 0.005 °/s/√Hz; accel noise density 25 µg/√Hz; one 70 s lap.")
    B.I("nd", "Gyro noise density", 0.005, "°/s/√Hz"); B.I("an", "Accel noise density", 25, "µg/√Hz")
    B.I("T", "Lap time", 70, "s"); B.I("g", "Gravity", 9.81, "m/s²")
    B.C("arw", "Angle random walk", "{nd}*60", "°/√h", "ARW = 60 N", 0.30, 0.005, "0.00")
    B.C("hw", "Heading wander after one lap", "{arw}*SQRT({T}/3600)", "deg", "ARW √t", 0.042, 5e-4, "0.000")
    B.C("vrw", "Velocity random walk", "{an}*1E-6*{g}", "m/s/√s", "", 2.45e-4, 1e-6, "0.000E+00")
    B.C("vw", "Velocity wander after one lap", "{vrw}*SQRT({T})", "m/s", "VRW √t", 0.0021, 5e-5, "0.0000")

    B.ex("Block Loop Run 1 — a traverse that closes perfectly and is still wrong",
         "Rectangle A(1000,1000) → B → C → D → A; legs 200, 150, 200, 150 m at 090°, 180°, 270°, 000°. "
         "AHRS heading +0.8° on every leg; odometer 0.2% long.")
    B.I("E0", "A easting", 1000.0, "m"); B.I("N0", "A northing", 1000.0, "m")
    B.I("err", "Heading error (every leg)", 0.8, "deg"); B.I("sc", "Odometer scale error", 0.002)
    legs = ((200, 90), (150, 180), (200, 270), (150, 0))
    pts = "BCDA"
    true = {"B": (1200, 1000), "C": (1200, 850), "D": (1000, 850), "A": (1000, 1000)}
    for i, (L, az) in enumerate(legs, 1):
        B.I(f"L{i}", f"Leg {i} true length", L, "m"); B.I(f"z{i}", f"Leg {i} true azimuth", az, "deg")
    bkE = {"B": 1200.380, "C": None, "D": None, "A": 1000.000}
    bkN = {"B": 997.202, "C": None, "D": None, "A": 1000.000}
    prevE, prevN = "{E0}", "{N0}"
    for i in range(1, 5):
        B.C(f"dE{i}", f"Leg {i} ΔE", f"{{L{i}}}*(1+{{sc}})*SIN(RADIANS({{z{i}}}+{{err}}))", "m", "L(1+s) sin(α+δ)",
            200.380 if i == 1 else None, 5e-4, "0.000")
        B.C(f"dN{i}", f"Leg {i} ΔN", f"{{L{i}}}*(1+{{sc}})*COS(RADIANS({{z{i}}}+{{err}}))", "m", "L(1+s) cos(α+δ)",
            -2.798 if i == 1 else None, 5e-4, "0.000")
        p = pts[i - 1]
        B.C(f"E{p}", f"{p}′ easting", f"{prevE}+{{dE{i}}}", "m", "", bkE[p], 5e-4, "0.000")
        B.C(f"N{p}", f"{p}′ northing", f"{prevN}+{{dN{i}}}", "m", "", bkN[p], 5e-4, "0.000")
        prevE, prevN = f"{{E{p}}}", f"{{N{p}}}"
    B.C("cE", "Misclosure ΣΔE", "SUM({dE1},{dE2},{dE3},{dE4})", "m", "", 0.0, 5e-4, "0.000")
    B.C("cN", "Misclosure ΣΔN", "SUM({dN1},{dN2},{dN3},{dN4})", "m", "", 0.0, 5e-4, "0.000")
    B.C("eB", "B′ error vs. true B", "SQRT(({EB}-1200)^2+({NB}-1000)^2)", "m", "", 2.82, 0.005, "0.00")
    B.C("eC", "C′ error vs. true C", "SQRT(({EC}-1200)^2+({NC}-850)^2)", "m", "", 3.53, 0.005, "0.00")

    B.ex("a local magnetic disturbance (Run 2) and the compass rule", "Run 1 plus the steel bridge deflects leg B–C by −2.0° (leg error 0.8 − 2.0 = −1.2°).")
    B.I("dist", "Extra deflection on leg 2", -2.0, "deg")
    prevE, prevN = "{X2.E0}", "{X2.N0}"
    bk = {"B": (1200.380, 997.202), "C": (1203.528, 846.935), "D": (1003.148, 849.733), "A": (1005.246, 1000.018)}
    for i in range(1, 5):
        extra = "+{dist}" if i == 2 else ""
        B.C(f"dE{i}", f"Leg {i} ΔE", f"{{X2.L{i}}}*(1+{{X2.sc}})*SIN(RADIANS({{X2.z{i}}}+{{X2.err}}{extra}))", "m", "", None, None, "0.000")
        B.C(f"dN{i}", f"Leg {i} ΔN", f"{{X2.L{i}}}*(1+{{X2.sc}})*COS(RADIANS({{X2.z{i}}}+{{X2.err}}{extra}))", "m", "", None, None, "0.000")
        p = pts[i - 1]
        B.C(f"E{p}", f"{p}′ easting", f"{prevE}+{{dE{i}}}", "m", "", bk[p][0], 5e-4, "0.000")
        B.C(f"N{p}", f"{p}′ northing", f"{prevN}+{{dN{i}}}", "m", "", bk[p][1], 5e-4, "0.000")
        prevE, prevN = f"{{E{p}}}", f"{{N{p}}}"
    B.C("mE", "Misclosure E", "{EA}-{X2.E0}", "m", "", 5.246, 5e-4, "0.000")
    B.C("mN", "Misclosure N", "{NA}-{X2.N0}", "m", "", 0.018, 5e-4, "0.000")
    B.C("mis", "Linear misclosure", "SQRT({mE}^2+{mN}^2)", "m", "", 5.25, 0.005, "0.00")
    B.C("tot", "Traverse length", "{X2.L1}+{X2.L2}+{X2.L3}+{X2.L4}", "m", "", 700, 1e-9, "0")
    B.C("ratio", "Precision ratio 1 :", "{tot}/{mis}", "", "", 133, 1, "0")
    cum = {"B": "{X2.L1}", "C": "({X2.L1}+{X2.L2})", "D": "({X2.L1}+{X2.L2}+{X2.L3})"}
    bkc = {"B": -1.50, "C": -2.62, "D": -4.12}
    bkerr = {"B": 3.02, "C": 3.20, "D": 1.01}
    for p in "BCD":
        B.C(f"kE{p}", f"Compass correction E at {p}", f"-{{mE}}*{cum[p]}/{{tot}}", "m", "−misclosure × cum. distance / total", bkc[p], 0.005, "0.00")
        B.C(f"kN{p}", f"Compass correction N at {p}", f"-{{mN}}*{cum[p]}/{{tot}}", "m", "", None, None, "0.000")
        tE, tN = true[p]
        B.C(f"a{p}", f"Adjusted {p} error vs. truth", f"SQRT(({{E{p}}}+{{kE{p}}}-{tE})^2+({{N{p}}}+{{kN{p}}}-{tN})^2)", "m", "", bkerr[p], 0.005, "0.00")

    B.ex("what does a typical lap look like? (hand check)", "Independent heading error 0.8° on each leg; legs 200, 150, 200, 150 m. Book simulation (20,000 laps): mean 4.3 m, 95% below 8.6 m.")
    B.I("da", "Heading error", 0.8, "deg")
    B.C("r", "In radians", "RADIANS({da})", "rad", "", 0.01396, 5e-6, "0.00000")
    B.C("s200", "Sideways on a 200 m leg", "200*{r}", "m", "L·δα", 2.79, 0.005, "0.00")
    B.C("s150", "Sideways on a 150 m leg", "150*{r}", "m", "", 2.09, 0.005, "0.00")
    B.C("rss", "RMS radial misclosure", "SQRT(2*{s200}^2+2*{s150}^2)", "m", "√(2·2.79² + 2·2.09²)", 4.93, 0.01, "0.00")

    B.ex("could the IMU alone drive the loop?", "GX5 IMU only; one 70 s lap at 10 m/s.")
    B.I("tilt", "Roll/pitch error", 0.25, "deg"); B.I("T", "Time", 70, "s"); B.I("g", "Gravity", 9.81, "m/s²"); B.I("v", "Speed", 10, "m/s")
    B.I("ba", "Uncalibrated accel bias", 2, "mg"); B.I("bg", "Uncalibrated gyro bias", 0.04, "°/s")
    B.I("bai", "Accel bias instability", 0.04, "mg"); B.I("bgi", "Gyro bias instability", 8, "°/h")
    B.C("leak", "Leaked gravity", "{g}*SIN(RADIANS({tilt}))", "m/s²", "g sin δθ", 0.0428, 5e-5, "0.0000")
    B.C("e1", "Tilt error after lap", "0.5*{leak}*{T}^2", "m", "½at²", 105, 0.5, "0")
    B.C("bam", "Accel bias", "{ba}*0.001*{g}", "m/s²", "", 0.0196, 5e-5, "0.0000")
    B.C("e2", "Accel bias error", "0.5*{bam}*{T}^2", "m", "", 48, 0.5, "0")
    B.C("hd", "Heading error after lap", "{bg}*{T}", "deg", "", 2.8, 0.005, "0.0")
    B.C("e3", "Gyro bias sideways error", "0.5*{v}*RADIANS({bg})*{T}^2", "m", "½·v·bg·t²", 17, 0.5, "0")
    B.C("e4", "Best case: accel bias instability", "0.5*{bai}*0.001*{g}*{T}^2", "m", "", 0.96, 0.005, "0.00")
    B.C("e5", "Best case: gyro 8°/h", "0.5*{v}*RADIANS({bgi}/3600)*{T}^2", "m", "", 0.95, 0.005, "0.00")

    B.ex("GX5-45 EKF: bounded, but meter-level", "±2 m RMS horizontal; ±5 m vertical; 20 s underpass.")
    B.I("H", "Horizontal RMS (radial)", 2.0, "m"); B.I("t", "Underpass time", 20, "s"); B.I("g", "Gravity", 9.81, "m/s²")
    B.I("tl", "Filtered tilt", 0.05, "deg"); B.I("ba", "Accel bias", 3.9e-4, "m/s²"); B.I("tl2", "Full tilt spec", 0.25, "deg")
    B.I("tp", "Time pulse", 30, "ns"); B.I("v", "Speed", 10, "m/s")
    B.C("ax", "Per-axis RMS", "{H}/SQRT(2)", "m", "", 1.41, 0.005, "0.00")
    B.C("c95", "95% horizontal radius", "2.448*{ax}", "m", "2.448 × σ", 3.46, 0.005, "0.00")
    B.C("mis", "Start–end misclosure", "SQRT(2)*{H}", "m", "√2 σ", 2.8, 0.05, "0.0")
    B.C("c1", "Coast, filtered tilt", "0.5*({g}*SIN(RADIANS({tl}))+{ba})*{t}^2", "m", "½(g sin θ + ba)t²", 1.8, 0.05, "0.0")
    B.C("c2", "Coast, full tilt spec", "0.5*({g}*SIN(RADIANS({tl2}))+{ba})*{t}^2", "m", "", 8.6, 0.05, "0.0")
    B.C("tpe", "Time-pulse error", "{tp}*1E-9*{v}*1E6", "µm", "", 0.3, 1e-6, "0.0")

    B.ex("dual-antenna heading on a backpack versus a truck", "GQ7: 0.25° on a 1.5 m baseline.")
    B.I("h", "Datasheet heading", 0.25, "deg"); B.I("b0", "Datasheet baseline", 1.5, "m")
    B.I("b1", "Backpack baseline", 0.5, "m"); B.I("b2", "Vehicle baseline", 2.5, "m")
    B.C("srel", "Relative GNSS precision", "{b0}*RADIANS({h})*1000", "mm", "σrel = b·σψ", 6.5, 0.05, "0.0")
    B.C("h1", "Backpack heading", "DEGREES({srel}/1000/{b1})", "deg", "σψ = σrel/b", 0.75, 0.005, "0.00")
    B.C("h2", "Vehicle heading", "DEGREES({srel}/1000/{b2})", "deg", "", 0.15, 0.005, "0.00")

    B.ex("single baseline versus VRS", "GQ7 RTK 1 cm + 1 ppm.")
    B.I("a", "Constant term", 1.0, "cm"); B.I("ppm", "Distance term", 1.0, "ppm")
    B.I("d1", "Nearest FPRN station", 22000, "m"); B.I("d2", "Virtual station", 3000, "m")
    B.C("e1", "Single baseline", "{a}+{ppm}*1E-6*{d1}*100", "cm", "a + ppm × D", 3.2, 0.005, "0.0")
    B.C("e2", "VRS / iMAX", "{a}+{ppm}*1E-6*{d2}*100", "cm", "", 1.3, 0.005, "0.0")

    B.ex("RTK traverse: centimeters instead of meters", "VRS about 2 km away; 2 cm used in the budget; 700 m loop.")
    B.I("a", "Constant term", 1.0, "cm"); B.I("d", "Virtual station distance", 2000, "m"); B.I("s", "Budget value", 2.0, "cm"); B.I("L", "Loop length", 700, "m")
    B.C("e", "RTK error", "{a}+1E-6*{d}*100", "cm", "", 1.2, 0.005, "0.0")
    B.C("c95", "95% circle", "2.448*{s}/SQRT(2)", "cm", "", 3.5, 0.05, "0.0")
    B.C("mis", "Misclosure", "SQRT(2)*{s}", "cm", "", 2.8, 0.05, "0.0")
    B.C("ratio", "Precision 1 :", "{L}/({mis}/100)", "", "", 25000, 300, "#,##0")

    B.ex("20 s and 60 s outages", "Coast error = √[(σv t)² + (½ ba t²)² + (⅙ g bg t³)²].")
    B.I("g", "Gravity", 9.81, "m/s²")
    sysd = (("x5", "GX5-45", 0.1, 3.9e-4, 8), ("q7", "GQ7", 0.05, 4.9e-5, 1.5), ("qr", "GQ7 after RTK", 0.01, 4.9e-5, 1.5))
    for k, lab, sv, ba, bg in sysd:
        B.I(f"sv{k}", f"{lab} velocity σ", sv, "m/s"); B.I(f"ba{k}", f"{lab} accel bias", ba, "m/s²"); B.I(f"bg{k}", f"{lab} gyro bias", bg, "°/h")
    def coast(k, t):
        return (f"SQRT(({{sv{k}}}*{t})^2+(0.5*{{ba{k}}}*{t}^2)^2+({{g}}*RADIANS({{bg{k}}}/3600)*{t}^3/6)^2)")
    B.C("x20", "GX5-45, 20 s", coast("x5", 20), "m", "", 2.07, 0.006, "0.00", note="Book rounded the three terms first (2.0, 0.08, 0.51) and got 2.07; unrounded = 2.065")
    B.C("q20", "GQ7, 20 s", coast("q7", 20), "m", "", 1.00, 0.005, "0.00")
    B.C("r20", "GQ7 + RTK velocity, 20 s", coast("qr", 20), "m", "", 0.22, 0.005, "0.00")
    B.C("x60", "GX5-45, 60 s", coast("x5", 60), "m", "", 15.0, 0.05, "0.0")
    B.C("r60", "GQ7 + RTK velocity, 60 s", coast("qr", 60), "m", "", 2.64, 0.005, "0.00")

    # ================= Module 17 =================
    B.sheet("M17 RIEGL", "Module 17 — RIEGL VUX-240²⁴ at 500 ft: worked examples", "17")
    B.ex("multiple-time-around (MTA) at 2400 kHz")
    B.I("c", "Speed of light", 2.997e8, "m/s"); B.I("prr", "Pulse rate", 2.4e6, "Hz"); B.I("rho", "Range (500 ft)", 152.4, "m"); B.I("prr2", "Lower pulse rate", 3e5, "Hz")
    B.C("rmax", "Unambiguous range", "{c}/(2*{prr})", "m", "c/(2 PRR)", 62.4, 0.05, "0.0")
    B.C("ratio", "Range / zone depth", "{rho}/{rmax}", "", "", 2.44, 0.005, "0.00")
    B.C("zone", "MTA zone", "INT({ratio})+1", "", "", 3, 1e-9, "0")
    B.C("r2", "Zone depth at 300 kHz", "{c}/(2*{prr2})", "m", "", 500, 0.5, "0")

    B.ex("atmospheric correction")
    B.I("n", "Refractive index of air", 1.0003); B.I("rho", "Range", 152.4, "m")
    B.C("ppm", "Correction in ppm", "({n}-1)*1E6", "ppm", "", 300, 1e-6, "0")
    B.C("corr", "Correction at range", "{rho}*({n}-1)", "m", "ρ(n − 1)", 0.046, 5e-4, "0.000")

    B.ex("point density at 500 ft")
    B.I("h", "Altitude", 152.4, "m"); B.I("half", "Half scan angle", 37.5, "deg"); B.I("rate", "Measurement rate", 2.0e6, "pts/s")
    B.I("kn", "Aircraft speed", 60, "kn"); B.I("vu", "UAS speed", 10, "m/s")
    B.C("sw", "Swath", "2*{h}*TAN(RADIANS({half}))", "m", "2h tan θ", 234, 0.5, "0")
    B.C("v", "Speed in m/s", "{kn}*1852/3600", "m/s", "", 30.9, 0.05, "0.0")
    B.C("d1", "Density, aircraft", "{rate}/({sw}*{v})", "pts/m²", "rate/(swath × v)", 277, 0.5, "0")
    B.C("d2", "Density, UAS", "{rate}/({sw}*{vu})", "pts/m²", "", 855, 0.5, "0")
    B.C("d3", "Scaled to 1,100 ft", "{d1}*500/1100", "pts/m²", "∝ 1/altitude", 126, 0.5, "0")
    B.C("sp", "Point spacing (aircraft)", "1/SQRT({d1})", "m", "1/√density", 0.06, 0.005, "0.000")

    # ================= Module 18 =================
    B.sheet("M18 Processing", "Module 18 — Processing Pipeline: worked examples", "18")
    B.ex("statistical outlier removal (SOR) on eight points", "Mean-neighbor distances (m); α = 1.")
    for i, v in enumerate((0.05, 0.06, 0.04, 0.05, 0.07, 0.05, 0.06, 0.42), 1):
        B.I(f"d{i}", f"Point {i}", v, "m")
    B.I("a", "α", 1)
    B.C("mu", "Mean", "AVERAGE({d1:d8})", "m", "μ", 0.100, 5e-4, "0.000")
    B.C("sd", "Standard deviation (population)", "STDEVP({d1:d8})", "m", "σ", 0.121, 5e-4, "0.000")
    B.C("thr", "Threshold", "{mu}+{a}*{sd}", "m", "μ + ασ", 0.221, 5e-4, "0.000")
    B.C("n", "Points removed", 'COUNTIF({d1:d8},">"&{thr})', "", "", 1, 1e-9, "0")

    B.ex("stockpile volume", "3 × 3 grid of 2 m cells; heights above base (m).")
    for i, v in enumerate((1.2, 1.5, 1.1, 1.8, 2.4, 1.6, 1.0, 1.3, 0.9), 1):
        B.I(f"h{i}", f"Cell {i} height", v, "m")
    B.I("c", "Cell size", 2, "m")
    B.C("A", "Cell area", "{c}^2", "m²", "", 4, 1e-9, "0")
    B.C("s", "Sum of heights", "SUM({h1:h9})", "m", "", 12.8, 1e-6, "0.0")
    B.C("V", "Volume", "{s}*{A}", "m³", "V = A Σh", 51.2, 1e-6, "0.0")
    B.C("cy", "Volume in cubic yards", "{V}*1.30795", "yd³", "", 67, 0.5, "0")

    # ================= Module 19 =================
    B.sheet("M19 Florida", "Module 19 — Florida Standards, FDOT and the New Datums: worked examples", "19")
    B.ex("sealing a 40-tile LAZ delivery with a signature file",
         "Hashes are computed by software (e.g. sha256sum or certutil -hashfile file SHA256); Excel only counts the lines.")
    B.I("t", "LAZ tiles", 40); B.I("o", "Other files (TIN, CAD, trajectory, report)", 4); B.I("bits", "SHA-256 length", 256, "bits")
    B.C("n", "Lines in the signature file", "{t}+{o}", "", "", 44, 1e-9, "0")
    B.C("hex", "Hex characters per hash", "{bits}/4", "", "4 bits per hex digit", 64, 1e-9, "0")

    B.ex("why the foot matters", "State Plane easting 650,000 ft.")
    B.I("E", "Easting", 650000, "ft")
    B.C("us", "U.S. survey foot", "1200/3937", "m", "1200/3937", 0.3048006096, 1e-10, "0.0000000000")
    B.C("mu", "Meters (U.S. survey foot)", "{E}*{us}", "m", "", 198120.396, 5e-4, "#,##0.000")
    B.C("mi", "Meters (international foot)", "{E}*0.3048", "m", "", 198120.000, 5e-4, "#,##0.000")
    B.C("d", "Difference", "{mu}-{mi}", "m", "", 0.396, 5e-4, "0.000")
    B.C("dft", "Difference in feet", "{d}/0.3048", "ft", "", 1.30, 0.005, "0.00")

    # ================= Module 20 =================
    B.sheet("M20 Practice", "Module 20 — Professional Practice: worked examples", "20")
    B.ex("can the RIEGL case study be flown by drone?", "VUX-240²⁴ 4.3 kg without IMU, up to 6.8 kg with IMU/GNSS; Part 107 limits 55 lb and 400 ft AGL.")
    B.I("k1", "Scanner without IMU", 4.3, "kg"); B.I("k2", "Scanner with IMU (max)", 6.8, "kg")
    B.I("lim", "Part 107 aircraft limit", 55, "lb"); B.I("agl", "Planned altitude", 500, "ft"); B.I("alt", "Part 107 altitude limit", 400, "ft")
    B.I("half", "Half scan angle", 37.5, "deg"); B.I("rate", "Measurement rate", 2.0e6, "pts/s"); B.I("v", "UAS speed", 10, "m/s")
    B.C("l1", "Weight without IMU", "{k1}*2.20462", "lb", "", 9.5, 0.05, "0.0")
    B.C("l2", "Weight with IMU", "{k2}*2.20462", "lb", "", 15.0, 0.05, "0.0")
    B.C("w", "Waiver needed for altitude? (1 = yes)", "IF({agl}>{alt},1,0)", "", "", 1, 1e-9, "0")
    B.C("r", "Nadir range at 400 ft", "{alt}*0.3048", "m", "", 121.9, 0.05, "0.0")
    B.C("sh", "Attitude terms shrink by", "1-{alt}/{agl}", "", "", 0.20, 1e-6, "0%")
    B.C("sw", "Swath", "2*{r}*TAN(RADIANS({half}))", "m", "", 187, 0.5, "0")
    B.C("den", "Density at UAS speed", "{rate}/({sw}*{v})", "pts/m²", "", 1070, 3, "#,##0")

    # ================= Module 21 =================
    B.sheet("M21 Capstone", "Module 21 — Capstone: worked examples (sample dataset on the 'Dataset' sheet)", "21")
    B.ex("drive speed from point spacing", "Along-track spacing ≤ 0.25 m; 20 Hz; 4 channels sweep the road.")
    B.I("sp", "Required spacing", 0.25, "m"); B.I("f", "Rotation rate", 20, "Hz"); B.I("n", "Effective channels", 4); B.I("v", "Chosen speed", 13, "m/s")
    B.C("vmax", "Maximum speed", "{sp}*{f}*{n}", "m/s", "v ≤ Δ × f × Neff", 20, 1e-9, "0.0")
    B.C("sp2", "Spacing at chosen speed", "{v}/({f}*{n})", "m", "", 0.16, 0.005, "0.000")
    B.C("mph", "Chosen speed in mph", "{v}*2.23694", "mph", "", 30, 1, "0.0")

    B.ex("the underpass: how bad is an unaided IMU?", "300 m underpass at 13 m/s; accel bias 0.5 mg; gyro 1°/h.")
    B.I("L", "Underpass length", 300, "m"); B.I("v", "Speed", 13, "m/s"); B.I("ba", "Accel bias", 0.0049, "m/s²"); B.I("bg", "Gyro bias", 1, "°/h")
    B.C("t", "Outage time", "{L}/{v}", "s", "", 23.1, 0.05, "0.0")
    B.C("a", "Accelerometer drift", "0.5*{ba}*{t}^2", "m", "½ ba t²", 1.31, 0.006, "0.00", note="Book used t rounded to 23.1 s (1.307 m); unrounded t gives 1.305 m")
    B.C("g", "Gyro drift (lateral)", "0.5*{v}*RADIANS({bg}/3600)*{t}^2", "m", "½ v bg t²", 0.017, 5e-4, "0.000")

    B.ex("timing and calibration checks", "PTP ±0.1 ms; boresight residual 0.02° at 30 m.")
    B.I("dt", "Timing", 0.0001, "s"); B.I("v", "Speed", 13, "m/s"); B.I("bs", "Boresight residual", 0.02, "deg"); B.I("R", "Longest range", 30, "m")
    B.C("e1", "Timing error", "{v}*{dt}*1000", "mm", "", 1.3, 0.005, "0.0")
    B.C("e2", "Boresight error", "{R}*RADIANS({bs})*100", "cm", "", 1.0, 0.05, "0.0")

    B.ex("vertical error budget (full budget in Module 14)", "Same terms as Example 14.15.")
    for nm, lab, v in (("rn", "Range noise", 0.8), ("bs", "Boresight", 1.0), ("la", "Lever arm", 0.3),
                       ("tr", "Trajectory (open sky)", 1.8), ("ct", "Control", 1.0), ("tm", "Timing", 0.1)):
        B.I(nm, lab, v, "cm")
    B.I("tu", "Trajectory in underpass", 2.5, "cm"); B.I("tc", "Underpass with mid-point control", 1.5, "cm")
    B.C("o", "Open sky", "SQRT(SUMSQ({rn:tm}))", "cm", "", 2.45, 0.005, "0.00")
    B.C("u", "Underpass", "SQRT(SUMSQ({rn:tm})-{tr}^2+{tu}^2)", "cm", "", 3.00, 0.005, "0.00")
    B.C("c", "Underpass with control", "SQRT(SUMSQ({rn:tm})-{tr}^2+{tc}^2)", "cm", "", 2.23, 0.005, "0.00")

    B.ex("control and checkpoint layout", "ASPRS minimum 30 checkpoints over 2.0 km; product 3 cm; survey ≤ 1.5 cm.")
    B.I("n", "Checkpoints", 30); B.I("L", "Corridor length", 2000, "m"); B.I("p", "Product accuracy", 3.0, "cm"); B.I("s", "Survey accuracy", 1.5, "cm")
    B.C("sp", "Checkpoint spacing", "{L}/{n}", "m", "", 67, 0.5, "0")
    B.C("r", "Survey is better by", "{p}/{s}", "×", "≥ 2×", 2, 1e-9, "0.0")

    B.ex("the accuracy results", "RMSEz,data = 1.9 cm; RMSEx = 2.0, RMSEy = 1.7 cm; checkpoint survey 0.8 cm V, 1.0 cm H. Full 30-point computation on the 'Dataset' sheet.")
    B.I("rz", "RMSE z (data)", 1.9, "cm"); B.I("rx", "RMSE x", 2.0, "cm"); B.I("ry", "RMSE y", 1.7, "cm")
    B.I("cv", "Checkpoint survey V", 0.8, "cm"); B.I("ch", "Checkpoint survey H", 1.0, "cm")
    B.C("V", "Vertical incl. checkpoint error", "SQRT({rz}^2+{cv}^2)", "cm", "", 2.06, 0.005, "0.00")
    B.C("Hd", "Horizontal (data)", "SQRT({rx}^2+{ry}^2)", "cm", "", 2.62, 0.005, "0.00")
    B.C("H", "Horizontal incl. checkpoint error", "SQRT({Hd}^2+{ch}^2)", "cm", "", 2.81, 0.005, "0.00")

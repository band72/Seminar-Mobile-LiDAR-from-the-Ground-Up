import csv, sys
sys.path.insert(0, ".")
from xlframe import *
import ex_a, ex_b, ex_c, ex_d

B = Book()
for m in (ex_a, ex_b, ex_c, ex_d):
    m.add(B)


def hdr(ws, row, labels):
    for j, h in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=h); c.font = WHITE_B; c.fill = NAVY
        c.alignment = Alignment(horizontal="center", wrap_text=True)


def extra(wb, index_rows):
    # ---------------- Monte Carlo sheet ----------------
    ws = wb.create_sheet("MC 20 m")
    ws["A1"] = "Monte Carlo check of the 20 m backpack budget (Example 14.5)"; ws["A1"].font = Font(name=FONT, bold=True, size=14, color="1F3864")
    ws["A2"] = ("Simplified linear Monte Carlo: each error term is drawn as an independent normal value, NORMINV(RAND(), 0, σ), and the terms are added. "
                "The book's run used 100,000 draws through the full rotation equations. Press F9 to draw again.")
    ws["A2"].font = ITAL
    ws["A4"] = "Horizontal σ from draws (cm)"; ws["B4"] = "=STDEV(I9:I2008)"
    ws["A5"] = "Vertical σ from draws (cm)"; ws["B5"] = "=STDEV(O9:O2008)"
    for c in ("B4", "B5"):
        ws[c].number_format = "0.00"; ws[c].font = BOLD
    terms = [("Position E", 1.5), ("Position N", 1.5), ("Yaw at 20 m", "=20*RADIANS(0.05)*100"), ("Boresight H", "=20*RADIANS(0.01)*100"),
             ("Lever arm H", "=0.2*SQRT(2)"), ("Range", "=SQRT(1.25^2+0.4^2)"), ("Encoder H", "=20*RADIANS(0.01)*100"), ("HORIZONTAL", None),
             ("Position U", 2.0), ("Roll at 20 m", "=20*RADIANS(0.02)*100"), ("Boresight V", "=20*RADIANS(0.01)*100"),
             ("Lever arm V", 0.2), ("Encoder V", "=20*RADIANS(0.01)*100"), ("VERTICAL", None)]
    ws["A7"] = "σ (cm) →"; ws["A7"].font = BOLD; ws["A8"] = "Draw #"
    hdr(ws, 8, ["Draw #"] + [t[0] for t in terms])
    for j, (lab, s) in enumerate(terms, 2):
        if s is not None:
            c = ws.cell(row=7, column=j, value=s); c.font = BLUE if not isinstance(s, str) else BLACK; c.fill = INFILL
            c.number_format = "0.000"
    for r in range(9, 2009):
        ws.cell(row=r, column=1, value=r - 8)
        for j, (lab, s) in enumerate(terms, 2):
            col = get_column_letter(j)
            if lab == "HORIZONTAL":
                ws.cell(row=r, column=j, value=f"=SUM(B{r}:H{r})")
            elif lab == "VERTICAL":
                ws.cell(row=r, column=j, value=f"=SUM(J{r}:N{r})")
            else:
                ws.cell(row=r, column=j, value=f"=NORMINV(RAND(),0,{col}$7)")
            ws.cell(row=r, column=j).number_format = "0.000"
    ws.column_dimensions["A"].width = 30
    for j in range(2, 17):
        ws.column_dimensions[get_column_letter(j)].width = 12
    ws.freeze_panes = "B9"

    # ---------------- Dataset sheet ----------------
    ds = wb.create_sheet("Dataset")
    ds["A1"] = "Module 21 sample project — 30 checkpoints and the filled-in accuracy report (simulated data)"
    ds["A1"].font = Font(name=FONT, bold=True, size=14, color="1F3864")
    ds["A2"] = "Inputs in blue come from sample_checkpoints.csv. Residual dZ = LiDAR − survey. Survey accuracy: 0.8 cm vertical, 1.0 cm horizontal."
    ds["A2"].font = ITAL
    cols = ["ID", "Station (m)", "Station (ft)", "Side", "Survey elev (m)", "LiDAR elev (m)", "dZ (cm)", "dZ (ft)", "dE (cm)", "dN (cm)", "dZ²", "dE²", "dN²"]
    hdr(ds, 4, cols)
    rows = list(csv.DictReader(open("../figs/sample_checkpoints.csv")))
    r0 = 5
    for k, row in enumerate(rows):
        r = r0 + k
        ds.cell(row=r, column=1, value=row["id"])
        for j, key in ((2, "station_m"), (5, "survey_elev_m"), (6, "lidar_elev_m"), (9, "dE_cm"), (10, "dN_cm")):
            c = ds.cell(row=r, column=j, value=float(row[key])); c.font = BLUE
        ds.cell(row=r, column=4, value=row["side"]).font = BLUE
        ds.cell(row=r, column=3, value=f"=B{r}/0.3048").number_format = "0.0"
        ds.cell(row=r, column=7, value=f"=ROUND((F{r}-E{r})*100,1)").number_format = "0.0"
        ds.cell(row=r, column=8, value=f"=G{r}/30.48").number_format = "0.000"
        ds.cell(row=r, column=11, value=f"=G{r}^2").number_format = "0.00"
        ds.cell(row=r, column=12, value=f"=I{r}^2").number_format = "0.00"
        ds.cell(row=r, column=13, value=f"=J{r}^2").number_format = "0.00"
        for j in (2, 5, 6):
            ds.cell(row=r, column=j).number_format = "0.000"
    r1 = r0 + len(rows) - 1
    G, I, J = f"G{r0}:G{r1}", f"I{r0}:I{r1}", f"J{r0}:J{r1}"
    s0 = r1 + 2
    hdr(ds, s0, ["Accuracy statistic", "Value", "Unit", "Equation", "Book value", "Check vs. book", "US feet", "Tolerance"])
    stats = [
        ("Number of checkpoints", f"=COUNT({G})", "", "n (ASPRS minimum 30)", 30, 0),
        ("Mean dZ (bias)", f"=AVERAGE({G})", "cm", "Σ dZ / n", 0.31, 0.005),
        ("Sum of squares dZ", f"=SUM(K{r0}:K{r1})", "cm²", "Σ dZ²", 107.99, 0.005),
        ("RMSE z (data)", f"=SQRT(SUMSQ({G})/COUNT({G}))", "cm", "√(Σ dZ²/n)", 1.90, 0.005),
        ("RMSE x (data)", f"=SQRT(SUMSQ({I})/COUNT({I}))", "cm", "", 2.00, 0.005),
        ("RMSE y (data)", f"=SQRT(SUMSQ({J})/COUNT({J}))", "cm", "", 1.71, 0.005),
        ("RMSE H (data)", "=SQRT(B{x}^2+B{y}^2)", "cm", "√(RMSEx² + RMSEy²)", 2.63, 0.005),
        ("Checkpoint survey accuracy, vertical", 0.8, "cm", "input", None, None),
        ("Checkpoint survey accuracy, horizontal", 1.0, "cm", "input", None, None),
        ("Final RMSE V (NVA) incl. checkpoint error", "=SQRT(B{z}^2+B{cv}^2)", "cm", "√(RMSEz² + RMSEck²)", 2.06, 0.005),
        ("Final RMSE H incl. checkpoint error", "=SQRT(B{h}^2+B{chh}^2)", "cm", "", 2.82, 0.005),
        ("Largest |dZ|", f"=MAX(MAX({G}),-MIN({G}))", "cm", "", 4.5, 0.05),
        ("Blunder threshold 3 × RMSE z", "=3*B{z}", "cm", "", 5.7, 0.05),
        ("Residuals over threshold", f'=COUNTIF({G},">"&B{{thr}})+COUNTIF({G},"<"&-B{{thr}})', "", "", 0, 0),
        ("Vertical specification", 3.0, "cm", "input", None, None),
        ("Horizontal specification", 5.0, "cm", "input", None, None),
        ("Vertical passes? (1 = yes)", "=IF(B{fv}<=B{sv},1,0)", "", "", 1, 0),
        ("Horizontal passes? (1 = yes)", "=IF(B{fh}<=B{sh},1,0)", "", "", 1, 0),
    ]
    keys = ["n", "mean", "ss", "z", "x", "y", "h", "cv", "chh", "fv", "fh", "max", "thr", "nb", "sv", "sh", "pv", "ph"]
    rowof = {k: s0 + 1 + i for i, k in enumerate(keys)}
    checks = []
    for i, (lab, f, u, eq, bk, tol) in enumerate(stats):
        r = s0 + 1 + i
        ds.cell(row=r, column=1, value=lab)
        if isinstance(f, str):
            c = ds.cell(row=r, column=2, value=f.format(**rowof)); c.font = BLACK
        else:
            c = ds.cell(row=r, column=2, value=f); c.font = BLUE; c.fill = INFILL
        c.number_format = "0.00"
        ds.cell(row=r, column=3, value=u); ds.cell(row=r, column=4, value=eq)
        if u == "cm":
            g = ds.cell(row=r, column=7, value=f"=B{r}/30.48"); g.number_format = '0.000" ft"'
        if bk is not None:
            ds.cell(row=r, column=5, value=bk); ds.cell(row=r, column=8, value=tol).font = BLUE
            ds.cell(row=r, column=6, value=f'=IF(ABS(B{r}-E{r})<=H{r},"OK","CHECK")').font = BOLD
            checks.append(r)
    rr = s0 + len(stats) + 2
    ds.cell(row=rr, column=1, value="Accuracy statement (built from the cells above)").font = BOLD
    ds.cell(row=rr + 1, column=1, value=(
        f'="This data set was tested to meet ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2, Version 2 (2024) '
        f'for a "&TEXT(B{rowof["sv"]},"0")&" cm RMSEV Vertical Accuracy Class and a "&TEXT(B{rowof["sh"]},"0")&" cm RMSEH Horizontal Accuracy Class. '
        f'NVA was found to be RMSEV = "&TEXT(B{rowof["fv"]},"0.00")&" cm ("&TEXT(B{rowof["fv"]}/30.48,"0.000")&" ft) and horizontal accuracy RMSEH = "'
        f'&TEXT(B{rowof["fh"]},"0.00")&" cm ("&TEXT(B{rowof["fh"]}/30.48,"0.000")&" ft), using "&B{rowof["n"]}&" independent checkpoints, including checkpoint survey uncertainty."'))
    ds.merge_cells(start_row=rr + 1, start_column=1, end_row=rr + 1, end_column=10)
    ds.cell(row=rr + 1, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ds.row_dimensions[rr + 1].height = 48
    widths = [40, 12, 12, 30, 14, 10, 12, 10, 10, 10, 9, 9, 9]
    for j, w in enumerate(widths, 1):
        ds.column_dimensions[get_column_letter(j)].width = w
    ds.freeze_panes = "A5"
    for row in ds.iter_rows():
        for c in row:
            if c.font.color is None or c.font.color.rgb in (None, "FF000000"):
                pass
    index_rows.append(dict(sheet="Dataset", num="21 data", title="sample project: 30 checkpoints and accuracy report", row=s0, last=s0 + len(stats), checks=checks))


def readme(ws, index_rows):
    ws["A1"] = "LiDAR from the Ground Up — Worked Example Calculator"
    ws["A1"].font = Font(name=FONT, bold=True, size=16, color="1F3864")
    ws["A2"] = "Companion workbook to the 6-hour Mobile LiDAR Survey Seminar, D.S. Banks, PSM"; ws["A2"].font = ITAL
    lines = [
        "Every numbered worked example in the seminar book is rebuilt here with live Excel formulas, one sheet per module.",
        "How to use: change any blue input on a yellow cell and every result below it recalculates. Try your own sensor, range or speed.",
        "Columns: Value (the formula result) · Unit · Equation as printed in the book · Book value · Check (OK when the formula matches the book "
        "within the tolerance in column H) · US feet (lengths converted) · Notes.",
        "Colors: blue text = input you may edit; black = formula; green = formula that pulls from another example or sheet.",
        "Changing an input will (correctly) turn some Checks to CHECK, because the book values were computed for the original inputs.",
        "Example 14.5 uses the 'MC 20 m' sheet (2,000 random draws; press F9 to redraw). The 'Dataset' sheet holds the Module 21 sample project.",
        "Angles are entered in degrees and converted with RADIANS(). Excel's ATAN2 takes (x, y) — the reverse of most textbooks.",
    ]
    for i, l in enumerate(lines, 4):
        c = ws.cell(row=i, column=1, value=l); c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=5); ws.row_dimensions[i].height = 30
    r = 4 + len(lines) + 1
    ws.cell(row=r, column=3, value="Overall status").font = BOLD
    ok_parts = "+".join(f"COUNTIF('{s}'!F:F,\"OK\")" for s in dict.fromkeys(x['sheet'] for x in index_rows))
    ck_parts = "+".join(f"COUNTIF('{s}'!F:F,\"CHECK\")" for s in dict.fromkeys(x['sheet'] for x in index_rows))
    ws.cell(row=r + 1, column=3, value="Values that match the book (OK)"); ws.cell(row=r + 1, column=4, value="=" + ok_parts).font = BOLD
    ws.cell(row=r + 2, column=3, value="Values that differ (CHECK)"); ws.cell(row=r + 2, column=4, value="=" + ck_parts).font = BOLD
    ws.cell(row=r + 3, column=3, value="Worked examples in this workbook"); ws.cell(row=r + 3, column=4, value=len(index_rows)).font = BOLD
    r += 5
    hdr(ws, r, ["Example", "Sheet", "Title (click to go there)", "Values checked", "Status"])
    for k, e in enumerate(index_rows, 1):
        rr = r + k
        ws.cell(row=rr, column=1, value=e['num'])
        ws.cell(row=rr, column=2, value=e['sheet'])
        c = ws.cell(row=rr, column=3, value=e['title'])
        c.hyperlink = f"#'{e['sheet']}'!A{e['row']}"; c.font = Font(name=FONT, color="0563C1", underline="single")
        ws.cell(row=rr, column=4, value=len(e['checks']))
        rng = f"'{e['sheet']}'!F{e['row']}:F{e['last']}"
        ws.cell(row=rr, column=5, value=f'=IF(COUNTIF({rng},"CHECK")>0,"CHECK",IF(COUNTIF({rng},"OK")>0,"OK","no book values"))').font = BOLD
    for col, w in zip("ABCDE", (12, 20, 70, 14, 16)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = f"A{r+1}"


B.save("LiDAR_Worked_Examples.xlsx", readme_fn=readme, extra_fn=extra)
n = sum(len(s['examples']) for s in B.sheets)
print("examples", n)

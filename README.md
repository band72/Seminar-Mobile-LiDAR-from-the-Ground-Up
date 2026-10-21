# LiDAR from the Ground Up

**Mobile Laser Scanning, IMUs, SLAM and Survey-Grade Deliverables**
D.S. Banks, PSM

Source files for a continuing-education (CE) course for surveyors, engineers and geospatial professionals. The course covers mobile LiDAR from first principles ("light bounces back") through the factor-graph mathematics inside modern SLAM software such as LIO-SAM, and on to the accuracy statistics a surveyor signs off on.

It is a two-track course. Every module has a plain-language explanation anyone can follow, alongside a rigorous engineering treatment of the same topic.

The course was built from an earlier *Mobile LiDAR Basics* seminar, a four-module course outline, and the LIO-SAM research paper (Shan *et al.*, 2020). Those sources were reorganized, corrected and greatly expanded.

## Modules

| # | Module |
|---|--------|
| 1 | What Is LiDAR? |
| 2 | The Math Toolkit |
| 3 | Measuring Distance with Light |
| 4 | The Laser Beam and the Echo |
| 5 | From Angles and Distance to X, Y, Z |
| 6 | Rotation, Pose and Frames |
| 7 | The IMU: Feeling Motion |
| 8 | Timing, GNSS and Motion Compensation |
| 9 | Lever Arm and Boresight Calibration |
| 10 | SLAM: Mapping While Finding Yourself |
| 11 | Scan Matching: Fitting Clouds Together |
| 12 | Factor Graphs and LIO-SAM |
| 13 | Control, Error Budgets and Accuracy Standards (incl. ASPRS Edition 2) |
| 14 | Error Propagation and Error Budgets |
| 15 | Ouster OS0 Case Study: Errors and Resolution |
| 16 | Choosing an IMU: AHRS, GNSS/INS and Tactical GNSS/INS |
| 17 | Survey-Grade Case Study: RIEGL VUX-240 |
| 18 | Processing, QA/QC and Deliverables |
| 19 | Florida Standards of Practice, FDOT and the New Datums |
| 20 | Professional Practice for LiDAR Surveys |
| 21 | Capstone and Sample Project Dataset |

Back matter includes answers to the in-text exercises, hands-on labs, a sample SOP and client accuracy agreement, an equation summary, a glossary and references.

## Repository layout

| Path | Contents |
|------|----------|
| `main.tex` | Master document. Build this to produce the course text. |
| `ch*.tex`, `ins_*.tex` | Module chapters and inserts |
| `figs/` | Figures, plus the sample project dataset (`sample_trajectory.csv`, `sample_checkpoints.csv`) |
| `figs*.py`, `style.py`, `crop.py` | Scripts that generate the figures |
| `calc*.py` | Scripts behind the worked examples' numbers |
| `xl/` | Builds the companion Excel workbook of worked examples |
| `review/` | Independent recomputation of key printed values, with its log |

## Building

**Course text (PDF)**: requires a LaTeX distribution such as TeX Live, with TikZ.

```bash
latexmk -pdf main.tex
```

**Figures**: requires Python 3 with `matplotlib`, `numpy` and `Pillow`.

```bash
python3 figs1.py
```

(Repeat for `figs2.py` … `figs9.py`.)

**Worked-examples workbook**: requires `openpyxl`. Writes `xl/LiDAR_Worked_Examples.xlsx`.

```bash
cd xl && python3 build.py
```

**Technical review**: recomputes key printed values and reports PASS/CHECK.

```bash
python3 review/tech_review.py
```

## Assessment materials

The quiz answer key and the final-exam builder are not published here. Instructors can request them from the author.

## Updates

This course is maintained as a living document and will be refined at regular intervals as standards and technology change. A project-based companion with worked, real-world examples is in development to clarify and standardize LiDAR deliverables.

## License

MIT. See [LICENSE](LICENSE).

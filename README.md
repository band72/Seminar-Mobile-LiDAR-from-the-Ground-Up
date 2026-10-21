# LiDAR from the Ground Up

**Mobile Laser Scanning, IMUs, SLAM and Survey-Grade Deliverables**
D.S. Banks, PSM

Source files for a continuing-education (CE) course for surveyors, engineers and geospatial professionals. The course covers mobile LiDAR from first principles ("light bounces back") through the factor-graph mathematics inside modern SLAM software such as LIO-SAM, and on to the accuracy statistics a surveyor signs off on.

It is a two-track course. Every module has a plain-language explanation anyone can follow, alongside a rigorous engineering treatment of the same topic.

The course was built from an earlier *Mobile LiDAR Basics* seminar, a four-module course outline, and the LIO-SAM research paper (Shan *et al.*, 2020). Those sources were reorganized, corrected and greatly expanded.

## Modules

| # | Module | Source |
|---|--------|--------|
| 1 | [What Is LiDAR?](ch01_intro.tex) | [`ch01_intro.tex`](ch01_intro.tex) |
| 2 | [The Math Toolkit](ch02_math.tex) | [`ch02_math.tex`](ch02_math.tex) |
| 3 | [Measuring Distance with Light](ch03_tof.tex) | [`ch03_tof.tex`](ch03_tof.tex) |
| 4 | [The Laser Beam and the Echo](ch04_beam.tex) | [`ch04_beam.tex`](ch04_beam.tex) |
| 5 | [From Angles and Distance to X, Y, Z](ch05_polar.tex) | [`ch05_polar.tex`](ch05_polar.tex) |
| 6 | [Rotation, Pose and Frames](ch06_rotation.tex) | [`ch06_rotation.tex`](ch06_rotation.tex) |
| 7 | [The IMU: Feeling Motion](ch07_imu.tex) | [`ch07_imu.tex`](ch07_imu.tex) |
| 8 | [Timing, GNSS and Motion Compensation](ch08_timing.tex) | [`ch08_timing.tex`](ch08_timing.tex) |
| 9 | [Lever Arm and Boresight Calibration](ch09_calib.tex) | [`ch09_calib.tex`](ch09_calib.tex) |
| 10 | [SLAM: Mapping While Finding Yourself](ch10_slam.tex) | [`ch10_slam.tex`](ch10_slam.tex) |
| 11 | [Scan Matching: Fitting Clouds Together](ch11_scanmatch.tex) | [`ch11_scanmatch.tex`](ch11_scanmatch.tex) |
| 12 | [Factor Graphs and LIO-SAM](ch12_factor.tex) | [`ch12_factor.tex`](ch12_factor.tex) |
| 13 | [Control, Error Budgets and Accuracy Standards (incl. ASPRS Edition 2)](ch13_accuracy.tex) | [`ch13_accuracy.tex`](ch13_accuracy.tex) |
| 14 | [Error Propagation and Error Budgets](ch13b_errprop.tex) | [`ch13b_errprop.tex`](ch13b_errprop.tex) |
| 15 | [Ouster OS0 Case Study: Errors and Resolution](ch13c_os0.tex) | [`ch13c_os0.tex`](ch13c_os0.tex) |
| 16 | [Choosing an IMU: AHRS, GNSS/INS and Tactical GNSS/INS](ch13d_gx5.tex) | [`ch13d_gx5.tex`](ch13d_gx5.tex) |
| 17 | [Survey-Grade Case Study: RIEGL VUX-240](ch13e_riegl.tex) | [`ch13e_riegl.tex`](ch13e_riegl.tex) |
| 18 | [Processing, QA/QC and Deliverables](ch14_processing.tex) | [`ch14_processing.tex`](ch14_processing.tex) |
| 19 | [Florida Standards of Practice, FDOT and the New Datums](ch14b_florida.tex) | [`ch14b_florida.tex`](ch14b_florida.tex) |
| 20 | [Professional Practice for LiDAR Surveys](ch14c_practice.tex) | [`ch14c_practice.tex`](ch14c_practice.tex) |
| 21 | [Capstone and Sample Project Dataset](ch15_capstone.tex) | [`ch15_capstone.tex`](ch15_capstone.tex) |

Back matter ([`ch16_back.tex`](ch16_back.tex)) includes answers to the in-text exercises, [hands-on labs](ch16b_labs.tex), a [sample SOP and client accuracy agreement](ch16c_sop.tex), an equation summary, a glossary and references. The front matter and "How to Use This Course" are in [`ch00_front.tex`](ch00_front.tex).

## Repository layout

| Path | Contents |
|------|----------|
| [`main.tex`](main.tex) | Master document. Build this to produce the course text. |
| `ch*.tex` | Module chapters (linked in the table above) |
| [`ins_asprs.tex`](ins_asprs.tex), [`ins_pen.tex`](ins_pen.tex), [`ins_rhr.tex`](ins_rhr.tex), [`ins_traj.tex`](ins_traj.tex) | Inserts used within the chapters |
| [`quiz_items.tex`](quiz_items.tex), [`sample_table.tex`](sample_table.tex) | Quiz questions (no answers) and the sample results table |
| [`figs/`](figs/) | Figures |
| [`figs/sample_trajectory.csv`](figs/sample_trajectory.csv), [`figs/sample_checkpoints.csv`](figs/sample_checkpoints.csv), [`figs/sample_stats.json`](figs/sample_stats.json) | Sample project dataset used in the capstone |
| [`style.py`](style.py), `figs1.py` … `figs9.py`, [`crop.py`](crop.py) | Scripts that generate the figures |
| [`calc.py`](calc.py), [`calc2.py`](calc2.py), [`calc3.py`](calc3.py), [`calc_ep.py`](calc_ep.py), [`calc_ep2.py`](calc_ep2.py), [`calc_riegl.py`](calc_riegl.py), [`calc_trav.py`](calc_trav.py) | Scripts behind the worked examples' numbers |
| [`usfix.py`](usfix.py) | Converts British spellings to US spellings in the chapter files |
| [`xl/`](xl/) | Builds the companion Excel workbook of worked examples ([`xl/build.py`](xl/build.py)) |
| [`review/`](review/) | [`tech_review.py`](review/tech_review.py) recomputes key printed values; results in [`Technical_Review_Log.txt`](review/Technical_Review_Log.txt) |
| [`LICENSE`](LICENSE) | MIT license |

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

<img src="docs/course-cover.jpg" alt="Cover of LiDAR from the Ground Up by D.S. Banks, PSM" width="150" align="right">

# LiDAR from the Ground Up
**Mobile Laser Scanning, IMUs, SLAM and Survey-Grade Deliverables** · D.S. Banks, PSM

*Look for this cover to be sure you have the official course materials.*

Source files for a continuing-education (CE) course for surveyors, engineers and geospatial professionals. The course covers mobile LiDAR from first principles ("light bounces back") through the factor-graph mathematics inside modern SLAM software such as LIO-SAM, and on to the accuracy statistics a surveyor signs off on.

It is a two-track course. Every module has a plain-language explanation anyone can follow, alongside a rigorous engineering treatment of the same topic.

The course was built from an earlier *Mobile LiDAR Basics* seminar, a four-module course outline, and the LIO-SAM research paper (Shan *et al.*, 2020). Those sources were reorganized, corrected and greatly expanded.

## Read the course

The course comes in two editions with separate downloads.

### Seminar (R1)

| Document | Description | |
|----------|-------------|---|
| 🎓 [**Seminar edition** (PDF, 71 pages)](docs/LiDAR_from_the_Ground_Up_R1.pdf) | The Surveying Concepts edition used in the seminar: all 21 modules in plain language, with every Simple Approach, Big Idea, Field Tip and Warning box and the illustrations | [⬇ Download](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/raw/main/docs/LiDAR_from_the_Ground_Up_R1.pdf) |
| 🎤 [**Seminar slides with speaker notes** (PDF, 76 pages)](docs/Seminar_Slides_with_Notes_R0.pdf) | The six-hour seminar presentation, with the presenter's notes for each slide | [⬇ Download](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/raw/main/docs/Seminar_Slides_with_Notes_R0.pdf) |

### Reference Book (R0)

| Document | Description | |
|----------|-------------|---|
| 📘 [**Reference Book** (PDF, 185 pages)](docs/LiDAR_from_the_Ground_Up_R0.pdf) | The full book: 21 modules with the engineering track, worked examples, labs, sample SOP, glossary and references | [⬇ Download](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/raw/main/docs/LiDAR_from_the_Ground_Up_R0.pdf) |
| 🛠️ [**Projects** (PDF, 11 pages)](docs/LiDAR_Projects_R0.pdf) | The capstone project (Module 21) with the sample project dataset and filled-in accuracy report, and the five hands-on labs (Appendix D), taken unchanged from the Reference Book | [⬇ Download](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/raw/main/docs/LiDAR_Projects_R0.pdf) |

All PDFs are compressed for download (October 2026).

## Download the exercise files

| File | Description | |
|------|-------------|---|
| 📊 [**Worked-examples workbook**](docs/LiDAR_Worked_Examples.xlsx) (Excel, 23 sheets) | Every worked example from the book, rebuilt with live formulas, one sheet per module, plus a Monte Carlo sheet and the capstone dataset | [⬇ Download](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/raw/main/docs/LiDAR_Worked_Examples.xlsx) |
| 📍 [**Sample checkpoints**](figs/sample_checkpoints.csv) (CSV, 30 points) | Checkpoint survey vs. LiDAR elevations with dE, dN and dZ, for the capstone accuracy test | [⬇ Download](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/raw/main/figs/sample_checkpoints.csv) |
| 🚗 [**Sample trajectory**](figs/sample_trajectory.csv) (CSV, 2 km) | Vehicle trajectory with position, heading, standard deviations and GNSS status, including a GNSS outage | [⬇ Download](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/raw/main/figs/sample_trajectory.csv) |

## Modules

| # | Module | Source | PDF | Notes |
|---|--------|--------|-----|-------|
| 1 | [What Is LiDAR?](ch01_intro.tex) | [`ch01_intro.tex`](ch01_intro.tex) | [📄 PDF](docs/modules/Module_01_R0.pdf) | |
| 2 | [The Math Toolkit](ch02_math.tex) | [`ch02_math.tex`](ch02_math.tex) | [📄 PDF](docs/modules/Module_02_R0.pdf) | |
| 3 | [Measuring Distance with Light](ch03_tof.tex) | [`ch03_tof.tex`](ch03_tof.tex) | [📄 PDF](docs/modules/Module_03_R0.pdf) | |
| 4 | [The Laser Beam and the Echo](ch04_beam.tex) | [`ch04_beam.tex`](ch04_beam.tex) | [📄 PDF](docs/modules/Module_04_R0.pdf) | |
| 5 | [From Angles and Distance to X, Y, Z](ch05_polar.tex) | [`ch05_polar.tex`](ch05_polar.tex) | [📄 PDF](docs/modules/Module_05_R0.pdf) | |
| 6 | [Rotation, Pose and Frames](ch06_rotation.tex) | [`ch06_rotation.tex`](ch06_rotation.tex) | [📄 PDF](docs/modules/Module_06_R0.pdf) | |
| 7 | [The IMU: Feeling Motion](ch07_imu.tex) | [`ch07_imu.tex`](ch07_imu.tex) | [📄 PDF](docs/modules/Module_07_R0.pdf) | |
| 8 | [Timing, GNSS and Motion Compensation](ch08_timing.tex) | [`ch08_timing.tex`](ch08_timing.tex) | [📄 PDF](docs/modules/Module_08_R0.pdf) | |
| 9 | [Lever Arm and Boresight Calibration](ch09_calib.tex) | [`ch09_calib.tex`](ch09_calib.tex) | [📄 PDF](docs/modules/Module_09_R0.pdf) | |
| 10 | [SLAM: Mapping While Finding Yourself](ch10_slam.tex) | [`ch10_slam.tex`](ch10_slam.tex) | [📄 PDF](docs/modules/Module_10_R0.pdf) | |
| 11 | [Scan Matching: Fitting Clouds Together](ch11_scanmatch.tex) | [`ch11_scanmatch.tex`](ch11_scanmatch.tex) | [📄 PDF](docs/modules/Module_11_R0.pdf) | |
| 12 | [Factor Graphs and LIO-SAM](ch12_factor.tex) | [`ch12_factor.tex`](ch12_factor.tex) | [📄 PDF](docs/modules/Module_12_R0.pdf) | |
| 13 | [Control, Error Budgets and Accuracy Standards (incl. ASPRS Edition 2)](ch13_accuracy.tex) | [`ch13_accuracy.tex`](ch13_accuracy.tex) | [📄 PDF](docs/modules/Module_13_R0.pdf) | |
| 14 | [Error Propagation and Error Budgets](ch13b_errprop.tex) | [`ch13b_errprop.tex`](ch13b_errprop.tex) | [📄 PDF](docs/modules/Module_14_R0.pdf) | |
| 15 | [Ouster OS0 Case Study: Errors and Resolution](ch13c_os0.tex) | [`ch13c_os0.tex`](ch13c_os0.tex) | [📄 PDF](docs/modules/Module_15_R0.pdf) | |
| 16 | [Choosing an IMU: AHRS, GNSS/INS and Tactical GNSS/INS](ch13d_gx5.tex) | [`ch13d_gx5.tex`](ch13d_gx5.tex) | [📄 PDF](docs/modules/Module_16_R0.pdf) | |
| 17 | [Survey-Grade Case Study: RIEGL VUX-240](ch13e_riegl.tex) | [`ch13e_riegl.tex`](ch13e_riegl.tex) | [📄 PDF](docs/modules/Module_17_R0.pdf) | |
| 18 | [Processing, QA/QC and Deliverables](ch14_processing.tex) | [`ch14_processing.tex`](ch14_processing.tex) | [📄 PDF](docs/modules/Module_18_R0.pdf) | |
| 19 | [Florida Standards of Practice, FDOT and the New Datums](ch14b_florida.tex) | [`ch14b_florida.tex`](ch14b_florida.tex) | [📄 PDF](docs/modules/Module_19_R0.pdf) | |
| 20 | [Professional Practice for LiDAR Surveys](ch14c_practice.tex) | [`ch14c_practice.tex`](ch14c_practice.tex) | [📄 PDF](docs/modules/Module_20_R0.pdf) | |
| 21 | [Capstone and Sample Project Dataset](ch15_capstone.tex) | [`ch15_capstone.tex`](ch15_capstone.tex) | [📄 PDF](docs/modules/Module_21_R0.pdf) | |

Back matter ([`ch16_back.tex`](ch16_back.tex)) includes answers to the in-text exercises, [hands-on labs](ch16b_labs.tex), a [sample SOP and client accuracy agreement](ch16c_sop.tex), an equation summary, a glossary and references. The front matter and "How to Use This Course" are in [`ch00_front.tex`](ch00_front.tex).

## Repository layout

| Path | Contents |
|------|----------|
| [`docs/`](docs/) | Seminar edition, Reference Book, Projects and seminar slides (PDF) and the worked-examples workbook (see [Read the course](#read-the-course) and [Download the exercise files](#download-the-exercise-files)) |
| [`main.tex`](main.tex) | Master document. Build this to produce the Reference Book (R0). |
| [`r1/`](r1/) | Builds the Seminar edition (R1) from the R0 chapters, which it only reads ([`r1/build_r1.py`](r1/build_r1.py), checked by [`r1/check_boxes.py`](r1/check_boxes.py)) |
| [`modules/`](modules/) | Builds one PDF per module from the R0 chapters ([`modules/build_modules.py`](modules/build_modules.py)); the PDFs are in [`docs/modules/`](docs/modules/) |
| [`projects/`](projects/) | Builds the Projects download from the R0 capstone and labs chapters ([`projects/build_projects.py`](projects/build_projects.py)) |
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
| [`LICENSE`](LICENSE), [`LICENSE-CODE`](LICENSE-CODE) | Content license (CC BY-NC-ND 4.0) and code license (MIT) |

## Building

Requires a LaTeX distribution such as TeX Live, with TikZ. The edition scripts also need Python 3 and Ghostscript (`gs`) for compression.

**Reference Book (R0)**:

```bash
latexmk -pdf main.tex
```

**Seminar edition (R1)**: generates the R1 chapters, checks every kept box and figure against R0, compiles, and writes the compressed `docs/LiDAR_from_the_Ground_Up_R1.pdf`.

```bash
r1/make_pdf.sh
```

**Module PDFs**: builds the full Reference Book once to resolve cross-references, then writes one compressed PDF per module to `docs/modules/`.

```bash
python3 modules/build_modules.py
```

**Projects**: writes the compressed `docs/LiDAR_Projects_R0.pdf`.

```bash
projects/make_pdf.sh
```

**Figures**: requires Python 3 with `matplotlib`, `numpy` and `Pillow`.

```bash
python3 figs1.py
```

(Repeat for `figs2.py` … `figs9.py`.)

**Worked-examples workbook**: a ready-made copy is in [`docs/`](docs/LiDAR_Worked_Examples.xlsx). To rebuild it, install `openpyxl`; the script writes `xl/LiDAR_Worked_Examples.xlsx`.

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

Each revision is published as a [GitHub Release](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/releases) with a summary of what changed. Questions, corrections and project ideas for the companion are welcome in [Discussions](https://github.com/band72/Seminar-Mobile-LiDAR-from-the-Ground-Up/discussions).

## Tools

### LiDAR Contour Studio — open-source contour generator for LAS/LAZ
**Repository:** [github.com/band72/Lidar_Prj_2026](https://github.com/band72/Lidar_Prj_2026)

An open-source companion tool, released under the MIT License, for turning LAS/LAZ point clouds into contours and surfaces:

- Filters ground points by ASPRS class and removes statistical outliers
- Crops by a latitude/longitude bounding box drawn on a map, and by elevation
- Exports contours to GeoJSON, Shapefile, AutoCAD DXF and GeoPackage, and a DEM to GeoTIFF
- Writes QA/QC reports (HTML, Markdown, JSON) covering metadata, point density, datums and limitations
- Runs on Windows, Linux and Android, with a touch-friendly web interface

It applies the processing and QA/QC steps taught in Module 18 of the seminar.

### Scout Maps the Park: SLAM animation

[![Scout the rover builds a map of a park while finding itself on it](docs/slam-animation.gif)](https://band72.github.io/Seminar-Mobile-LiDAR-from-the-Ground-Up/slam-animation.html)

An interactive, eight-step animation of how SLAM works: look, roll and guess, match, fix, and close the loop. Each step includes a note in survey terms.

▶ **[Open the interactive animation](https://band72.github.io/Seminar-Mobile-LiDAR-from-the-Ground-Up/slam-animation.html)**

▶ **[SLAM Lectures for Beginner](https://www.youtube.com/watch?v=B2qzYCeT9oQ&list=PLpUPoM7Rgzi_7YWn14Va2FODh7LzADBSm)** 

## To-do

- [ ] Independent review of the Florida standards module by a second PSM
- [ ] Expand the examples for post processing the bulk data with open source software and integrate with Civil 3D.
- [ ] Add the FDOT Mobile LiDAR (TML) accuracy tolerances for Types A, B and C from the current Surveying and Mapping Handbook
- [ ] Update the book's agenda to match the slide deck (SLAM as the 70-minute core block)
- [ ] Replace the simulated capstone dataset with a real, de-identified project
- [ ] Release the project-based companion with real-world LiDAR deliverable examples
- [ ] Re-check the NSRS modernization timeline before each offering
- [ ] Conceptualize each breakout topic with 5 minute summary
- [x] SLAM animation (Scout Maps the Park)
- [x] Worked-example Excel workbook

## Disclaimer

This material is for education only. It is not legal or professional advice and does not replace the judgment of a licensed surveyor and mapper. Standards, rules and specifications change. Always verify the current editions of the ASPRS standards, Chapter 5J-17 F.A.C., FDOT requirements and NSRS guidance before relying on them for a project.

## License

**Course content** (book, slides, LaTeX sources, figures, workbook and sample data): [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). You may share it with credit, for non-commercial purposes, without modification. For commercial use, adaptation or instructor licensing, contact the author.

**Code** (the Python scripts): MIT. See [LICENSE-CODE](LICENSE-CODE).

Full terms are in [LICENSE](LICENSE).

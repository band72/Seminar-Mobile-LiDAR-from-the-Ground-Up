# Seminar 2: Engineering, Error Budgets and Standards in Numbers

*LiDAR from the Ground Up, D.S. Banks, PSM. Design draft, November 2026.*

**Status: design.** The course text, workbook and supplementary documents this seminar uses already exist. The slides and the problem set are not built yet (see [What still has to be built](#what-still-has-to-be-built)).

## Purpose

Seminar 1 teaches every module at the concept level: the Simple Approach, Big Idea and Field Tip material, with no calculations. Seminar 2 covers what Seminar 1 leaves out: the engineering track of the Reference Book. Participants work the equations, build error budgets, and test results against the ASPRS and FDOT standards with numbers.

| | Seminar 1 | Seminar 2 |
|---|-----------|-----------|
| Level | concepts, no calculations | calculations on every topic |
| Text | Seminar edition (R1) | Reference Book (R0.1) |
| Book material | Simple Approach, Big Idea, Field Tip, Warning boxes, figures | Engineer's View, Key Equation and Worked Example boxes, Try It exercises, labs, appendices |
| Assessment | 50 conceptual questions | worked problem set |
| Tools | none | calculator and the worked-examples workbook |

## Audience and prerequisites

- Surveyors, engineers and geospatial professionals who have taken Seminar 1 or have equivalent field experience with mobile LiDAR.
- Comfortable with trigonometry and a spreadsheet. Module 2 (the math toolkit) is assigned as pre-reading.
- Bring a laptop with Excel or a compatible spreadsheet, and a scientific calculator.

## Learning objectives

After the seminar, participants will be able to:

1. Compute a range, its timing sensitivity and its ambiguity interval, and convert a range and two angles into sensor coordinates.
2. Apply rotation matrices and the direct georeferencing equation to place a point in project coordinates, and compute the effect of a timing, lever-arm or boresight error.
3. Predict IMU drift through a GNSS outage from datasheet biases, and decide whether an outage is acceptable for a given tolerance.
4. Work a Kalman update, an ICP iteration and a small factor graph by hand, and read the LIO-SAM equations.
5. Propagate errors through a measurement model with the variance law and the covariance (Jacobian) form, and check the result by Monte Carlo simulation.
6. Build a complete error budget for a mobile LiDAR system and find the term that limits it.
7. Convert between FDOT 95% tolerances and ASPRS RMSE, run a checkpoint test that satisfies both, and write the accuracy statement.
8. Design control and checkpoint layouts from the error budget, including spacing, placement inside GNSS outages and the number of scans between control points.

## Agenda

Six hours of instruction plus breaks. Adjust to the approving board's contact-hour rules.

| Time | Session | Reference Book | In-seminar work |
|------|---------|----------------|-----------------|
| 0:00–0:15 | Welcome. Recap of Seminar 1. The direct georeferencing equation as the road map for the day | Module 9 | |
| 0:15–1:05 | **1. The single measurement in numbers.** Time of flight and clock precision; range ambiguity; the range equation and beam footprint; polar to X, Y, Z; point spacing and density | Modules 3, 4, 5 | Workbook sheets for Modules 3–5; Try It 3, 4 and 5 |
| 1:05–1:55 | **2. Pose, IMU and calibration math.** Rotation matrices and the small-angle rule; strapdown integration; bias drift and the tilt error; timing error and de-skewing; lever arm and boresight; the two-pass boresight check | Modules 6, 7, 8, 9 | Lab 4 (boresight from two passes) |
| 1:55–2:10 | Break | | |
| 2:10–3:20 | **3. Estimation: how the trajectory is computed.** The one-dimensional Kalman filter; the EKF with a landmark; ICP, point-to-plane and NDT; a factor graph solved by hand; IMU preintegration; the LIO-SAM equations | Modules 10, 11, 12 | Lab 3 (ICP in 30 lines of Python); the four-pose factor graph |
| 3:20–3:50 | Lunch | | |
| 3:50–4:50 | **4. Error propagation and error budgets.** The variance law; correlated errors; the covariance matrix and Jacobian; the error ellipse; the full georeferencing budget; Monte Carlo checking; averaging and the bias floor | Module 14 | Workbook Monte Carlo sheet; build a budget for your own system |
| 4:50–5:35 | **5. Hardware in numbers.** Resolution, precision and accuracy of a real scanner; choosing an IMU and the coast-error equation; a survey-grade airborne system at 500 ft | Modules 15, 16, 17 | Coast error for 20 s and 60 s outages |
| 5:35–5:45 | Break | | |
| 5:45–6:35 | **6. The standards in numbers.** ASPRS Edition 2 accuracy classes and data internal precision; FDOT Type A, B and C; converting 95% tolerances to RMSE; the checkpoint test; control spacing, outages and scans between control points; why the capstone passes ASPRS but fails FDOT Type A and B | Modules 13, 19, 21; Supplementary documents 09, 12 and 13 | Lab 5 (checkpoint report in a spreadsheet) |
| 6:35–7:05 | Problem set and evaluation | | |

Session 3 is the core block, as in Seminar 1. Session 6 is the one most participants came for: leave it its full 50 minutes.

## Session notes

**Session 1.** Start from one laser return and follow it. The key numbers to leave in the room: 1 ns of timing is 15 cm of range, a beam's footprint grows with range, and density is set by speed, rotation rate and angular step. Close with FDOT's density thresholds (20 and 10 points/ft²) so the calculation has a target.

**Session 2.** Everything here is an angle or a time multiplied by something: angle error times range, timing error times speed, timing error times rotation rate times range. Have participants compute all three for their own system. The tilt error (a small attitude error leaking gravity into acceleration) is the idea most people have not met before.

**Session 3.** Work each method once by hand before showing software. The one-dimensional Kalman update and the four-pose factor graph both fit on one slide and one spreadsheet row. Tie the factor graph to least-squares network adjustment, which the audience already knows.

**Session 4.** This is the hardest hour. Use the variance law on one output first, then show that the Jacobian form is the same idea for three outputs at once. The Monte Carlo sheet lets participants confirm the formula without trusting it. End with the bias floor: averaging cannot go below systematic error.

**Session 5.** Use the case studies as budget inputs, not as product reviews. The point of the coast-error exercise is the decision it supports: how long an outage a given IMU can carry for a given tolerance.

**Session 6.** Put the conversion table on screen and keep it there: Type A needs about 0.93 cm vertical and 1.06 cm horizontal RMSE; Type B needs about 1.56 cm and 1.76 cm. Then walk through the capstone comparison, which passes its ASPRS agreement and meets neither FDOT type. Finish with the Recommendations document: control spacing by conditions, control inside every outage, and budgeting uncertainty instead of feet.

## Materials

| Material | Where |
|----------|-------|
| Reference Book (R0.1) | `docs/LiDAR_from_the_Ground_Up_R0.pdf` |
| Module PDFs | `docs/modules/` |
| Worked-examples workbook | `docs/LiDAR_Worked_Examples.xlsx` |
| Sample trajectory and checkpoints | `figs/sample_trajectory.csv`, `figs/sample_checkpoints.csv` |
| Accuracy testing SOP | `docs/supplementary/09_Mobile_Lidar_Accuracy_Testing_SOP.pdf` |
| Mobile LiDAR accuracy workbook | `docs/supplementary/12_Mobile_Lidar_Accuracy_Workbook.xlsx` |
| FDOT standards: problems and recommendations | `docs/supplementary/13_FDOT_Mobile_Lidar_Standards_Recommendations.md` |
| FDOT Surveying and Mapping Handbook (2025) | `docs/supplementary/01_FDOT_Surveying_and_Mapping_Handbook_2025-02-28.pdf` |

## Assessment

A worked problem set, open book, with a calculator and the workbook allowed. Proposed: 20 problems, at least two from each session, 70% to pass. Each problem asks for a number and a one-line conclusion ("meets Type B", "outage too long for this IMU"), so the grade tests judgment as well as arithmetic.

## What still has to be built

- [ ] Slide deck with speaker notes for the six sessions
- [ ] Problem set (20 problems) and instructor answer key
- [ ] Participant handout: the equation summary and the FDOT/ASPRS conversion table on one sheet
- [ ] Optional: an Advanced edition PDF generated from the Reference Book, holding only the engineering-track boxes, as the counterpart of the Seminar 1 edition

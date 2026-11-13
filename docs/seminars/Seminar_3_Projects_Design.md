# Seminar 3: Mobile LiDAR Projects

*LiDAR from the Ground Up, D.S. Banks, PSM. Design draft, November 2026.*

> **Status: not complete.** The five projects below are designed, but Seminar 3 cannot be offered until each has real, de-identified project data. The data each project needs is listed under "Real data needed".

## Purpose

Seminar 3 has no lectures. Participants work five mobile LiDAR projects from scope to signed deliverable, using the ASPRS *Positional Accuracy Standards for Digital Geospatial Data* (Edition 2, Version 2, 2024) and the FDOT *Surveying and Mapping Handbook* (February 28, 2025, Sections 35–40). Seminar 1 or 2, or equivalent experience, is the prerequisite.

## The standards every project uses

| | FDOT Type A | FDOT Type B | FDOT Type C |
|---|-------------|-------------|-------------|
| Tolerance, H and V, at 95% (NSSDA) | ≤ 0.06 ft | ≤ 0.10 ft | set by the PSM and the scope |
| RMSE needed, vertical | 0.93 cm (0.031 ft) | 1.56 cm (0.051 ft) | per scope |
| RMSE needed, horizontal | 1.06 cm (0.035 ft) | 1.76 cm (0.058 ft) | per scope |
| Point density | ≥ 20 points/ft² | ≥ 10 points/ft² | per scope |
| Control pairs (FDOT recommended) | ≤ 1000 ft | ≤ 1500 ft | chosen by the PSM |
| Checkpoints (FDOT) | ≥ 20, ≤ 1000 ft apart | ≥ 20, 1000–2500 ft apart | per scope |

ASPRS Edition 2 rules applied in every project:

- accuracy reported as RMSE, with the mean error (bias) stated;
- at least 30 checkpoints for a tested product (up to 120 on large projects), kept independent of control;
- checkpoints at least twice as accurate as the product;
- the checkpoint survey error included in the reported accuracy;
- vegetated vertical accuracy (VVA) reported as found; acceptance rests on non-vegetated accuracy (NVA);
- data internal precision for a vertical class X: within-swath ≤ 0.60X, swath-to-swath RMSD ≤ 0.80X, swath-to-swath maximum ≤ 1.60X.

Course recommendations applied where they are tighter than FDOT (Supplementary document 13): control spacing set by GNSS conditions, a control target and a checkpoint inside every GNSS outage, checkpoints midway between control, and each stretch collected in both directions.

## Agenda

| Time | Activity |
|------|----------|
| 0:00–0:20 | Briefing: the standards table, the deliverable template, how the projects are graded |
| 0:20–1:25 | Project 1 |
| 1:25–2:30 | Project 2 |
| 2:30–2:45 | Break |
| 2:45–3:50 | Project 3 |
| 3:50–4:20 | Lunch |
| 4:20–5:25 | Project 4 |
| 5:25–6:30 | Project 5 |
| 6:30–6:50 | Debrief: what failed, what it would take to pass, evaluation |

Each project block is 65 minutes: 10 to read the scope, 40 to work in pairs, 15 to compare results.

## The deliverable for every project

One page per project, signed by the participant as the surveyor in responsible charge:

1. The plan: survey type, control and checkpoint layout with counts and spacing, collection speed and passes.
2. The test: checkpoint table, mean error, RMSE, the FDOT 95% value and the ASPRS RMSE, with checkpoint error included.
3. The verdict: pass or fail against each standard, with the limiting error named.
4. The accuracy statement, in ASPRS Edition 2 wording, with datums, epoch, geoid and foot.
5. Limitations and what would be needed to pass, if it failed.

---

## Project 1: Urban arterial resurfacing design (FDOT Type A)

**Scenario.** One mile of four-lane urban arterial is to be milled and resurfaced. The designer needs pavement elevations, curb lines and drainage structures for cross-slope correction.

**Governing standards.** FDOT Type A. ASPRS 1 cm vertical class (the nearest class to Type A's 0.93 cm), so data internal precision limits of 0.6, 0.8 and 1.6 cm.

**Tasks.**

1. Choose the control spacing for three stretches (open sky, tree-lined, and a signalized intersection with tall buildings) and count the control points needed with pairs on both sides. Compare with FDOT's 1000 ft.
2. State the accuracy the control and checkpoints must have, and the field method that can deliver it.
3. Set the collection speed and number of passes to reach 20 points/ft² at the edge of pavement.
4. Run the checkpoint test on the data: mean, RMSE, 95% value, with checkpoint error.
5. Test swath-to-swath agreement between opposing passes.

**Pass criteria.** H and V ≤ 0.06 ft at 95%; RMSE within the 1 cm class; density ≥ 20 points/ft²; internal precision within limits; at least 30 checkpoints.

**Teaching point.** Type A is a control-driven survey. Checkpoints have to be good to about 5 mm, which rules out RTK.

**Real data needed.** Trajectory with standard deviations and GNSS status; control and checkpoint coordinates with their survey method and accuracy; point cloud tiles for the pavement in both directions; calibration report.

---

## Project 2: Rural highway asset inventory and earthwork (FDOT Type B)

**Scenario.** Five miles of two-lane rural highway with wooded shoulders. The deliverables are an asset inventory (signs, guardrail, culvert ends, driveways) and earthwork quantities for shoulder widening.

**Governing standards.** FDOT Type B. ASPRS 1.5 cm vertical class on hard surfaces (limits 0.9, 1.2 and 2.4 cm); VVA reported as found on the vegetated shoulders.

**Tasks.**

1. Lay out control pairs and checkpoints for the corridor. Decide where the 1500 ft spacing holds and where canopy calls for tighter spacing.
2. Plan 30 hard-surface checkpoints and 30 vegetated checkpoints.
3. Run the NVA test and report the VVA.
4. Classify a sample tile with the ASPRS LAS codes and build the bare-earth surface.
5. Compute an earthwork volume from the surface and state its uncertainty from the vertical RMSE.

**Pass criteria.** H and V ≤ 0.10 ft at 95% on hard surfaces; density ≥ 10 points/ft²; NVA within class; VVA reported with its value.

**Teaching point.** Acceptance rests on the hard-surface test. The ground under vegetation is reported as found, and the earthwork quantity inherits that uncertainty.

**Real data needed.** Trajectory with GNSS status through the canopy; hard-surface and vegetated checkpoints; classified and unclassified point cloud tiles; the asset list extracted by the original project.

---

## Project 3: Interchange with GNSS outages (FDOT Type A through an underpass)

**Scenario.** A half-mile design survey passes under an interstate overpass and alongside a retaining wall. GNSS is lost under the bridge and degraded beside the wall.

**Governing standards.** FDOT Type A, with the Handbook's Note 4: stretches with fewer than 5 satellites must not exceed what the IMU can bridge. ASPRS 1 cm vertical class.

**Tasks.**

1. From the trajectory, measure the length and duration of each outage and the percentage of the trajectory with a fixed solution.
2. From the IMU datasheet, predict the drift through each outage with the coast-error equation (Module 16). Decide whether Note 4 is satisfied.
3. Count the scans between control points through the outage, and place control and checkpoints inside it.
4. Compare the checkpoint residuals inside the outage with those in open sky. Does the error grow toward the middle?
5. Compare the forward and reverse passes through the outage.

**Pass criteria.** Type A tolerances met inside the outage as well as outside; a control target and a checkpoint inside every outage; fixed percentage, outage lengths and bridging method reported.

**Teaching point.** An outage is managed, not forbidden. The trajectory's own uncertainty shows where the extra control belongs.

**Real data needed.** A trajectory that includes a real GNSS outage, with standard deviations and solution status; the IMU model and datasheet; control and checkpoints inside and outside the outage; point cloud tiles from both directions.

---

## Project 4: County road elevations for flood vulnerability (FDOT Type C)

**Scenario.** A county needs road-centerline and finished-floor elevations along 40 miles of low-lying roads for a flood-vulnerability study. No design work will be done from the data.

**Governing standards.** FDOT Type C: the PSM and the scope set the accuracy, and published control may be used with Department approval (Note 9). The participant writes the scope. A reasonable choice is the ASPRS 5 cm vertical class (limits 3.0, 4.0 and 8.0 cm), which is about 0.32 ft at 95%.

**Tasks.**

1. Write the accuracy requirement into the scope as an ASPRS class, and justify it from the intended use.
2. Decide the number of checkpoints for a project of this size (30 minimum, up to 120) and distribute them.
3. Decide whether published control is adequate, and what must be checked before relying on it.
4. Run the vertical test on road surfaces, and separately on finished-floor elevations.
5. State the vertical datum, geoid model and foot, and what must be archived to move the data to the new national datums later.

**Pass criteria.** A written, numeric accuracy class; a test that meets it; datums and limitations stated.

**Teaching point.** Type C has no floor unless the surveyor writes one. Fitness for use is a professional judgment that has to be stated in numbers. The 2019 Monroe County memo in the Supplementary Information is a published example.

**Real data needed.** Road and finished-floor checkpoints from a county-scale project; the published control used and its datasheet values; a sample of the point cloud; the project's scope of services.

---

## Project 5: Independent acceptance test of a delivered dataset

**Scenario.** A consultant delivers a mobile LiDAR dataset with a report stating it meets FDOT Type A. The participant is the reviewing surveyor and must accept or reject it.

**Governing standards.** FDOT Types A and B, ASPRS Edition 2, and Florida's Standards of Practice (Chapter 5J-17, F.A.C.) for the report and sealing.

**Tasks.**

1. Review the trajectory: fixed percentage, outages, and estimated standard deviations.
2. Check that the checkpoints are independent of the control and at least twice as accurate as the claimed product.
3. Recompute the test from the checkpoint table: mean, RMSE, the 95% value, and the result with checkpoint error included. Does it meet Type A? Type B?
4. Check density at the farthest range used for design, and swath-to-swath agreement.
5. Check the report against 5J-17.051: survey type and purpose, datums, survey date, accuracy statement, responsibility for the data, and the sealing method for digital files.
6. Write a one-page acceptance or rejection memo.

**Pass criteria.** A correct verdict with the evidence for it. A dataset that fails Type A but meets Type B is a valid finding.

**Teaching point.** A dataset can pass one standard and fail another. The reviewer's job is to say which, and why.

**Real data needed.** A complete delivery: trajectory, control and checkpoint tables, point cloud tiles, the consultant-style report and LAS files with headers, all de-identified.

---

## Preparing real project data

For each project:

- [ ] Obtain the owner's written permission to use the data for teaching.
- [ ] De-identify it: remove firm, client and personal names, shift coordinates by a constant offset if the location must not be recognizable, and remove imagery showing people or license plates.
- [ ] Keep the files small enough to distribute: a few point cloud tiles, not the whole project.
- [ ] Record the scanner, IMU and GNSS equipment by grade, not by vendor name, unless the vendor agrees.
- [ ] Work the project through once and keep the result as the instructor's key.

## Status

| Project | Design | Real data |
|---------|--------|-----------|
| 1. Urban arterial resurfacing (Type A) | done | needed |
| 2. Rural highway inventory and earthwork (Type B) | done | needed |
| 3. Interchange with GNSS outages (Type A) | done | needed |
| 4. County road elevations for flood vulnerability (Type C) | done | needed |
| 5. Independent acceptance test | done | needed |

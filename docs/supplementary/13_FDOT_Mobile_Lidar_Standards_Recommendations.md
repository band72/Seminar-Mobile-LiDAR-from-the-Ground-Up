# FDOT Mobile LiDAR Survey Types: Problems and Recommendations

*LiDAR from the Ground Up, D.S. Banks, PSM. November 2026.*

This note reviews the Terrestrial Mobile LiDAR (TML) survey types in the FDOT *Surveying and Mapping Handbook* (February 28, 2025, Sections 39.6.2 and 39.7) and recommends how to apply them. It is the course author's analysis for teaching purposes. It is not an FDOT position and does not replace the Handbook, the contract or the judgment of the PSM in responsible charge.

## The standard as published

| Type | Accuracy (95% confidence) | Control and checkpoint layout (recommended) |
|------|---------------------------|---------------------------------------------|
| A | H and V ≤ 0.06 ft; ≥ 20 points/ft² | control pairs ≤ 1000 ft apart, on each side of the road; checkpoints ≤ 1000 ft apart |
| B | H and V ≤ 0.10 ft; ≥ 10 points/ft² | control pairs ≤ 1500 ft apart, on each side of the road; checkpoints 1000–2500 ft apart |
| C | set by the PSM in responsible charge and the scope of services | chosen by the PSM; published control may be used with Department approval |

Accuracy is tested under NSSDA at the 95% confidence level on at least 20 checkpoints.

## Eight problems

### 1. Type A is at the edge of what mobile LiDAR can prove

- 0.06 ft at 95% is an RMSE of about 0.93 cm vertical and 1.06 cm horizontal.
- GNSS positioning alone typically contributes 1–2 cm of vertical error, so Type A can only be met by adjusting the cloud tightly to dense ground control.
- That makes it accuracy relative to local control, not absolute accuracy.
- The Handbook allows GNSS baselines up to 10 miles for Type A. A baseline that long can add roughly 1–2 cm of error, which is the entire budget.

**Recommendation:** treat Type A as a control-driven survey. Keep baselines short, use a base station on project control, and state in the report that accuracy is relative to the project control.

### 2. One tolerance for horizontal and vertical ignores how each is measured

- At the required 20 points/ft², neighboring points are about 0.22 ft (2.7 inches) apart, nearly four times coarser than the 0.06 ft horizontal tolerance being tested.
- Vertical can be tested on a flat surface by averaging many points. Horizontal depends on finding a target edge in the cloud, which the point spacing and laser footprint limit.

**Recommendation:** test horizontal accuracy on purpose-built targets (chevrons or checkerboards) sized for the point spacing, fit the target shape instead of picking single points, and collect at a density well above the minimum where horizontal accuracy matters.

### 3. The statistic is dated and the sample is small

- NSSDA 95% values assume errors are normally distributed with no bias. A systematic shift, such as a wrong geoid model or antenna height, breaks that assumption.
- ASPRS Edition 2 dropped 95% reporting in favor of RMSE for this reason.
- With 20 checkpoints the computed RMSE is itself uncertain by roughly ±16%, so a survey near the limit can pass or fail by chance.
- ASPRS requires 30 checkpoints and adds the checkpoint survey's own error to the result. FDOT requires neither.

**Recommendation:** use at least 30 checkpoints, report the mean error (bias) alongside the RMSE, include the checkpoint survey error, and report both the FDOT 95% value and the ASPRS RMSE so one test satisfies both.

### 4. No numeric requirement for checkpoint accuracy

- The Handbook says checkpoints need "the same project accuracies as the control" and leaves the rest to the PSM (Note 5).
- A checkpoint that is only as accurate as the product cannot test the product.

**Recommendation:** survey checkpoints at least twice as accurate as the tolerance being tested (the ASPRS Edition 2 rule). For Type A that is about 5 mm, which means digital leveling and total station work, not RTK.

### 5. The spacing rules do not respond to conditions

- The 1000 ft and 1500 ft spacings are the same in open sky and under an overpass, at any speed, with any grade of IMU. Drift between control points depends on all three.
- They are recommendations only.
- Nothing says to place checkpoints between control points, where error is largest. Checkpoints placed beside control test the cloud at its best spots.
- Type B's "1000–2500 ft" is a range with no rule for choosing within it.

**Recommendation:** tighten control spacing wherever GNSS is weak, place checkpoints midway between control points, and put a control target and a checkpoint inside every GNSS outage.

### 6. Point density is a count, not a guarantee

- The standard does not say where to measure density: at what range, or on what surface.
- Density falls quickly with distance from the vehicle, and a high average can hide gaps at curbs and edges.

**Recommendation:** verify density on the delivered data, on test patches at the farthest range used for design, and state the maximum range beyond which points are excluded.

### 7. Type C is undefined, and relative accuracy is missing

- "Set by the PSM and the scope" gives no floor, so two Type C surveys cannot be compared.
- No type sets a numeric limit for agreement between overlapping passes; there is only a 20% overlap requirement. ASPRS does set such limits.

**Recommendation:** write a numeric accuracy class into every Type C scope, and test swath-to-swath agreement on every project against the ASPRS data internal precision limits.

### 8. GNSS coverage has no measurable rule

- The Handbook's rule (Section 39.6.2, Note 4) is that stretches with fewer than 5 satellites must not exceed what the IMU can bridge. No number is attached, so it cannot be checked objectively.
- A blanket "100% fixed" target is not the answer. Overpasses, tree canopy and urban corridors interrupt GNSS on most real projects.
- "Fixed" does not guarantee correct. A fix can be wrong, and a well-controlled SLAM solution through an outage can be more accurate than a marginal fix.

**Recommendation:** manage outages instead of forbidding them.

1. Plan the collection for a fixed solution wherever the sky allows: check satellite visibility, avoid poor windows, and collect each pass in both directions.
2. Before mobilizing, predict the drift through every expected outage from the IMU grade, the speed and the outage length. If the predicted drift exceeds the tolerance, add control inside the outage or change the plan.
3. Put a control target inside every outage for Type A and Type B, and a checkpoint inside or immediately beyond it.
4. Report the percentage of the trajectory with a fixed solution, the length of every outage, and how each was bridged.

## Summary of recommended practice

| Topic | FDOT minimum | Recommended |
|-------|--------------|-------------|
| Checkpoints | 20 | 30 or more, midway between control |
| Statistic | 95% (NSSDA) | 95% and RMSE, with mean error reported |
| Checkpoint accuracy | PSM's choice | at least 2× better than the tolerance |
| Checkpoint error | not included | included in the reported accuracy |
| Horizontal test | not specified | fitted targets sized for the point spacing |
| Density check | project average | delivered data, at the farthest design range |
| Swath-to-swath | 20% overlap | numeric limit, tested on every project |
| GNSS outages | within IMU capability | predicted drift within tolerance; control and checkpoint in every outage; fixed % and outages reported |

## Sources

FDOT *Surveying and Mapping Handbook* (February 28, 2025), Sections 39.6.2 and 39.7; ASPRS *Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 2 (2024); FGDC-STD-007.3-1998 (NSSDA). Worked numbers are in Modules 13, 19 and 21 of the Reference Book.

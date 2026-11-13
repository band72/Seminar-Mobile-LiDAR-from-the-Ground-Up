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

## Nine problems

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

**Why 1000 ft is too wide for Type A.** Type A needs about 9 mm RMSE vertical. Checkpoint error (about 5 mm) and laser range and attitude noise (about 4–5 mm) use part of that, leaving roughly 6 mm for trajectory error between control points. The adjustment pins the cloud only at each control point; in between, the cloud follows the GNSS/IMU trajectory, whose error wanders by a centimeter or more over tens of seconds. At 13 m/s, 1000 ft is about 23 seconds between control points; 300 ft is about 7 seconds, short enough that the error is nearly constant and the adjustment removes it.

**Recommendation:** for Type A, set the maximum control spacing by GNSS conditions:

| Conditions | Maximum control spacing |
|------------|-------------------------|
| Open sky, clean fixed solution throughout | 500 ft |
| Tree canopy, buildings, intermittent fix | 300 ft |
| GNSS outage (overpass, tunnel) | 150–300 ft, with at least one point inside the outage |

Use 300 ft as the default and allow 500 ft only where the trajectory report shows a clean fixed solution. Place checkpoints midway between control points: if the midpoint residuals are clearly larger than those near control, the spacing is too wide for that stretch. On a 2 km corridor with pairs on both sides, 300 ft spacing means about 44 control points against about 14 at 1000 ft, each needing leveling-grade elevations. That cost is why Type A should be reserved for design-grade work.

**Scans between control points.** Distance in feet is a stand-in. What accumulates between control points is uncertainty, and both the number of scans and the conditions feed it. At a 10 Hz scanner rate:

| Speed | 300 ft spacing | 1000 ft spacing |
|-------|----------------|-----------------|
| 13 m/s (29 mph) | about 70 scans, 7 s | about 235 scans, 23 s |
| 5 m/s (11 mph) | about 180 scans, 18 s | about 610 scans, 61 s |

Slowing down gives more scans and better overlap, but also more time between control points, and IMU drift grows with time, not distance. Slower is not automatically better where GNSS is weak.

Each scan's pose is tied to the world by GNSS and to its neighbors by the IMU and by scan matching, each with its own weight. Between two control points the scans behave like the legs of a traverse: small independent errors per scan accumulate with the square root of the number of scans, and the uncertainty peaks midway. Assuming 1 mm of relative error per scan for illustration:

| Scans between control | Peak uncertainty at the midpoint |
|-----------------------|----------------------------------|
| 70 | about 4 mm |
| 235 | about 8 mm |

Against the roughly 6 mm available for Type A, 70 scans fits and 235 does not. A systematic error per scan, such as a small boresight or scale error, is worse: it grows in direct proportion to the scan count.

Each condition weakens a different weight:

| Condition | What weakens | Effect on each scan |
|-----------|--------------|---------------------|
| Canopy, buildings | GNSS: float solutions, multipath or no fix | the pose leans on the IMU and scan matching, and errors start to accumulate |
| Speed | scan matching: less overlap, more motion distortion | weaker tie between scans, though less time for drift |
| Moments (turns, bumps, braking) | IMU and de-skewing: high rotation rates magnify timing and calibration errors | individual scans get noticeably worse |
| Featureless scene (open field, plain wall) | scan matching: nothing to grip in one direction | the chain is loose along that direction |

With good GNSS every scan is tied to the world directly and the scan count hardly matters. When GNSS weakens, the chain of scans carries the solution, and both the number of links and the quality of each one count.

**Recommendation:** budget uncertainty, not feet.

1. Use the trajectory's estimated standard deviation, reported by the processing software along the route, and place control so it stays inside the tolerance everywhere. That puts more control under canopy, through turns and in outages.
2. Do not trust the weights blindly. The reported uncertainty is only as good as the software's noise models and is often optimistic. Midpoint checkpoints in the weakest stretches are the proof.
3. Collect each stretch twice, in opposite directions. Direction-dependent errors partly cancel, and the disagreement between passes shows where the chain is weak.

The 1 mm per scan figure is an assumption for illustration. The real value depends on the scanner, the scene and the software.

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

### 9. Nothing on IMU grade, vibration or mounting

The Handbook requires an IMU and says only that the manufacturer's specifications must be sufficient (Note 6). Three effects decide whether that is true, and they act on different time scales. Control can remove slow drift. It cannot remove fast vibration.

**IMU drift (slow: seconds to minutes).** The IMU integrates its readings, so sensor biases grow with time: accelerometer bias with time squared, gyro bias with time cubed. For a tactical-grade unit with an assumed 0.1 mg accelerometer bias and 1°/h gyro bias, with no GNSS help:

| Time without correction | Distance at 13 m/s | From accelerometer bias | From gyro bias |
|-------------------------|--------------------|-------------------------|----------------|
| 7 s | 300 ft | 2.4 cm | 0.3 cm |
| 23 s | 1000 ft | 26 cm | 10 cm |

With good GNSS the drift never gets this large. In an outage these numbers apply, reduced by forward and backward processing, with the error peaking mid-outage. Tripling the spacing costs about ten times the drift.

**Vibration (fast: 10–200 Hz from engine, tires and road).**

- *False bias.* MEMS accelerometers turn sustained vibration into a small steady offset (vibration rectification). It looks like sensor bias and feeds the drift above.
- *Aliasing.* Vibration above half the IMU's sample rate folds down and looks like real, slow motion. A 200 Hz IMU cannot correctly see anything above 100 Hz.
- *Mount flex.* If the plate between the IMU and scanner bends, the boresight angle jitters. A jitter of 0.01° at 30 m moves a point 5 mm, more than half the Type A budget.

Vibration changes faster than control points are spaced, so it becomes permanent noise in the cloud and leaves less of the budget for drift.

**Moments of inertia (how the rig and vehicle respond).**

- *The sensor mount.* Moment of inertia grows with mass times distance squared. A heavy pod on a tall mast has a low natural rocking frequency, easily excited by bumps and braking, which flexes the mount.
- *The vehicle.* A heavy vehicle rotates slowly and smoothly. A light platform (ATV, backpack, drone) snaps around quickly, and fast rotation magnifies timing error: 1 ms at 30°/s moves a point at 30 m by about 1.6 cm, against 1.6 mm at 3°/s.
- *Lever arms.* Rotation turns a lever-arm error into a velocity error. A 1 cm error in the antenna-to-IMU lever arm at 20°/s gives about 3.5 mm/s, which the IMU reads as real motion.

**Recommendation:** for Type A,

1. Mount the IMU and scanner on one stiff plate, as close together as possible. If isolators are used, isolate the plate as a unit, never the IMU and scanner separately.
2. Keep the rig low and compact. Avoid tall masts.
3. Sample the IMU at 200 Hz or faster, with filtering before sampling.
4. Drive smoothly through critical areas: steady speed, no hard braking or sharp turns.
5. Measure lever arms to a few millimeters.
6. State the IMU grade in the scope, and use its datasheet biases to predict drift through every outage.

The bias and rate figures here are assumed, representative values. Take the real ones from the IMU's datasheet.

## What limits accuracy: sensors or the surveyor?

SLAM is a probability machine. Every measurement carries an uncertainty, and the solution is the trajectory and map that best fit all of them, each weighted by how far it is trusted. It is the same mathematics as a least-squares network adjustment.

It is tempting to say the result is limited by the worst sensor. That is not quite how fusion works. When two sensors measure the same quantity, proper weighting makes the result better than the best one: fusing a 2 cm sensor with a 5 cm sensor gives about 1.9 cm. The weakest-link idea does hold in four situations, and they are the ones that matter:

- **Each sensor has its own job.** GNSS gives absolute position, the IMU gives short-term motion, and the LiDAR gives relative motion from scan matching. Absolute accuracy is limited by GNSS and control; accuracy through an outage is limited by the IMU and the scene geometry.
- **The largest error dominates.** Independent errors combine by root-sum-square. Terms of 1, 1 and 3 cm total 3.3 cm, so improving the small ones barely helps.
- **An overconfident sensor poisons the result.** A wrong GNSS fix that claims 1 cm accuracy drags the whole solution with it. The limit is the worst-modeled sensor, not the noisiest.
- **Systematic errors do not average out.** Timing offsets, lever arms, boresight and a wrong geoid shift everything together. Fusion cannot see them, because every sensor agrees on the wrong answer.

So accuracy is limited by the largest unmodeled or uncorrected error, wherever it comes from.

Cheaper sensors will shrink random error: MEMS IMUs are approaching tactical grade, several cheap sensors can beat one expensive one, and better algorithms extract more from the same hardware. They will not move the GNSS floor (about 1–2 cm vertical from the atmosphere), remove bias, or supply the reference. Control, checkpoints, calibration, timing and datums come from surveying, not from sensors. So far, falling prices have mostly brought lower-grade automotive sensors, with 1–3 cm range noise and wide beams, into survey use.

As random errors shrink, what remains is increasingly systematic: calibration, control and reference. That is the part the surveyor owns.

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
| Control spacing, Type A | 1000 ft (recommended) | 500 ft in open sky, 300 ft where GNSS is weak, 150–300 ft in outages |
| Control placement | by distance | by trajectory uncertainty: more control under canopy, through turns and in outages; each stretch collected in both directions |
| IMU and mounting | manufacturer's specifications | stated IMU grade; one stiff plate; 200 Hz or faster; lever arms to a few millimeters |

## Sources

FDOT *Surveying and Mapping Handbook* (February 28, 2025), Sections 39.6.2 and 39.7; ASPRS *Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 2 (2024); FGDC-STD-007.3-1998 (NSSDA). Worked numbers are in Modules 13, 19 and 21 of the Reference Book.

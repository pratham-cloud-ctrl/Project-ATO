# Conditional movement-primitive scenario: declared protocol

13 October 2026. Declared before this package's first result generation. This
is a transparent future-interface scenario, not a preregistered human study,
statistical confirmation cohort, validated spinal decoder or native electronics
simulation. The earlier frozen observer and actual-delivery studies are separate
and unchanged. No result in this package qualifies those earlier active paths.

## Purpose and stopping point

Investigate a plausible conditional route from a compact expert reference and
learner spinal features to bounded task assistance and possible retained
adaptation. Produce one finite scenario study, inspect its favorable, neutral and
adverse regimes, then hand its assumed interfaces to detailed electronics/CAD.
No favorable result or particular acquisition multiplier is a completion gate.

## Declared model

The task is a two-coordinate, 1 Hz cyclic movement primitive with a 100 mm
reference amplitude. It is an abstract movement component, not piano playing,
football performance or a complete biomechanical limb. Coordinates are meters.

`phi(t) = [sin(phase), cos(phase)]`

`x(t) = theta_n phi(t) + B a(t)`

`a' = (d u(t - 35 ms) - a) / 40 ms`

`z(t) = H phi(t) + noise`

`theta_(n+1) = theta_n + eta [<target-x> + rho <B a>]`

Angle brackets denote the two-feature least-squares projection over the practice
block. Initial learner coefficients and a local program-to-task map vary across
four fixed synthetic seeds. The model assumes selective signed task-space
programs; electrical phase polarity does not imply neural excitation/inhibition
or an opposite movement. Each sign requires a separate useful recruitment map.
The linear B model additionally assumes equal-and-opposite effects for opposing
programs. Real opposite routes need separate characterization and need not be
symmetric; this simplification is a conditional premise of the surrogate.

Sixteen abstract neural features have an assumed task-phase relationship. They
are **not** raw electrode voltages, independently demonstrated human information,
or a reproduction of the animal papers' offline decoders. The decoder is fitted
from paced calibration with external movement labels. The expert reference is a
stipulated correctly decoded task representation, identical in information to
the external reference; expert spinal voltage acquisition is not simulated here.

The controller sees only decoded past measurements, the known 1 Hz cue, a
measured OFF-probe estimate of the learner template and a fitted local response
map. It advances phase using the known cue frequency, not the simulator's future
phase. Practice phase has a random offset and slowly varying mismatch. The
spinal-feature delay is assumed 20 ms; the external movement delay 60 ms. Their
different noise/delay budgets are deliberate conditional resource differences,
not an experimental discovery that neural sensing is intrinsically superior.

Each 25 ms frame selects a normalized route-program command clipped to [-1,1].
True and estimated activation states are propagated separately at 5 ms steps.
The decoder/control code cannot use true learner coefficients or true gain.
The fitted gain uses eight separate signed program responses. A chosen 10 mm
minimum singular-value criterion rejects an absent actuator; this is a model
identification rule, not a biological threshold.

Electrical dose `d=1.0` is an **assumed future normalized interface**. This does
not assert exact charge, chemical safety, a native 4% monitor pass, or a selected
human stimulation prescription. Stage 2's waveform and resource budgets remain
engineering constraints to reconcile, not properties established by this model.

## Arms, plasticity and controls

Five nominal arms share learner, noise draws, expert task information and paid
calibration/probe/practice durations:

1. OFF unaided practice.
2. Expert external reference with external learner measurements.
3. Equally informative expert spinal reference with the same external learner
   measurements. This must produce identical results to arm 2.
4. Same reference with the assumed live spinal phase features.
5. Same as arm 4 with a deliberately 90-degree shifted timing estimate.

For each arm and four synthetic learners, run `rho=-1,0,1,2`: 80 nominal runs.
`eta=0.08` per block and `rho` are unmeasured scenario parameters. No paper's
recovery percentage or clinical score is used to fit them. Algebra gives

`Delta theta = eta [(theta* - theta) + (rho-1) <B a>]`.

Therefore `rho=1` has the same OFF learning as unaided practice, however much
ON assistance helps. `rho=0` exposes guidance dependence; negative coupling can
be adverse; sufficiently useful positive coupling can accelerate the chosen
component. This is the central biological assumption, not a speedup deduced from
the cited experiments. Exact equal-information and rho=1 identities are checked.

Four failure variations use `rho=2`, four learners and OFF/external/spinal-live
arms: unavailable neural features (explicit external fallback), neural delay
120 ms, actual gain halved after calibration, and absent recruitment authority.
This adds 48 runs: 128 runs total. Settings are not retuned after scoring.

## Assessment and resources

Run 24 equal practice blocks, each with a 1 s paced OFF template probe, 2 s
practice and 2 s movement-response washout. Pending delayed commands are applied
before the response decays; switching to OFF never deletes a delivered effect.
Washout has no learning in this model. It is not tissue/electrode recovery.

The common calibration accounting is 12 s phase calibration plus eight assumed
1 s equilibrium program probes with 2 s washout each: 36 s total for every arm.
The calibration sample responses are synthetic observations, not circuit tests.

Report ON trajectory RMS, actual modeled command frames and OFF primitive RMS.
An explicitly assumed 95% persistence of acquired coefficients defines a
post-rest OFF assessment. No real retention interval is assigned and no
cross-task transfer benefit is established. The proficiency threshold is a
chosen 15 mm pooled RMS over both coordinates, not a separate 15 mm maximum
on each coordinate. If not reached, report null; never substitute
the final block. Report practice time and total allocated time separately.

The output comprises summary JSON, per-block CSV, five first-practice traces,
two explanatory figure pairs and a reproduction check. These are mechanistic
illustrations across four synthetic parameter draws, not population estimates.
No additional audit/observer family is required to finish this package.

## Reproduce

From the repository root:

```text
python experiments/stage3/conditional-concept/study.py
python experiments/stage3/conditional-concept/study.py --check --figures
```

The check compares all saved numerical runs, histories and traces with fixed
tolerances and independently checks the learning identity and comparator rules.
The script's normalized source hash is in the summary; Git binds exact artifacts.

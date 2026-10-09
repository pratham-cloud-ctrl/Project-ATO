# Project ATO: current work status

Updated: **9 October 2026**.

## Active objective

Develop the complete proposed invasive spinal cord–computer interface as an
entirely digital research and engineering project: theory, spinal acquisition,
interpretation, personalized stimulation, monitored delivery, feedback, native
electronics/firmware, populated engineering CAD, illustrated paper and a
professional private GitHub repository. AstroSam's Mind-Link inspires the
progression from future vision to inspectable engineering.

Both expert-informed **retained motor learning** and **target-specific
physiological automation** remain central. Expert recordings inform a
learner-specific policy; voltage replay and universal body control are not
assumed. Video and website work are parked. No deadline is imposed.

## Where we are

| Stage | Status | Concrete deliverables |
|---|---|---|
| 1: mechanism/specification | Complete within specification scope | Both causal chains, requirements/assumptions/capability map, primary-source audit, interfaces, three editable diagrams and illustrated nine-page brief |
| 2: quantitative architecture | Complete within architecture scope | 16-stream/two-source design, timing/noise/compute/memory/power budgets, rejected cases, control contracts, eight-page brief and preliminary native allocation CAD; [exit review](docs/stage2/exit-review.md) |
| 3: computational mechanisms | **In progress** | Preserved foundation studies, numerical refinements, acquisition qualification, fair information comparison, expert competence audit, response-domain validation and cue scheduling component |
| 4: detailed electronics/firmware | Pending | Full native multichannel KiCad design, programmable stimulation/routing, independently qualified monitoring, power/telemetry, embedded implementation and scoped circuit verification |
| 5: populated engineering CAD | Pending | Actual boards/components/package/lead interfaces, native parametric assemblies, dimensions, STEP/STL and nominal fit checks |
| 6: integrated paper/repository release | Pending | Complete digital path verification, final illustrated manuscript, native sources, reproducible release, evidence and learning/defence material |

The historical v1.0.0 release is a subsystem reference. Its one-channel board
and desktop enclosure are not the completed implant requested here. Stage 2's
80 allocation solids and illustrative ports are not populated implant CAD.

## What the continuation completed

The [Stage 3 continuation review](docs/stage3/continuation-review.md) connects the
previous work to this revision and the next package. Its main evidence includes:

- **Numerics:** 96 motor fixed-input refinements and five bounded closed-loop
  grids, plus 408 pressure runs in 136 noise-matched groups. The tested 2.5 ms
  midpoint/cascade motor solver meets its scoped budgets. Historical coarse
  motor numbers remain preliminary. Pressure numeric budgets pass, with 24
  frame-sensitive comparisons retained.
- **Acquisition:** eight matched missing-input/artifact recordings and explicit
  digital filter-residual qualification. The fixed 100 ms wait is insufficient
  in tested cases; the bound does not certify physical amplifier recovery.
- **Information value:** seven fair studies, 280 plasticity/arm rows and a
  capacity-matched external-history observer. No consistent neural advantage is
  shown. Actual monitored delivery admits no motor practice pulses; OFF
  retention/transfer remains truly OFF.
- **Teacher competence:** all eight original-generator performances fail timing.
  Eight separate inverse-model performances pass the unchanged task gates.
  The new teacher is not yet integrated into the existing learning library.
- **Response domain:** 24 fixed-profile studies with 432 independently recorded
  checks in each held-out context. Conditional nominal maps admit 63/72
  same-context and 34/72 changed-context cases. Actual, null and adverse maps
  reject. Finite resting checks do not grant dynamic or unseen-context authority.
- **Cue policy:** observed forecasts, whole-frame planning, cancellation,
  expiration and causal residual detection. Eight component replays retain
  actual authority rejection and failed assisted forecast qualification. They
  do not establish coupled motor control or retained-learning benefit.

The preserved foundation batch was reproduced under its unchanged defaults.
The [test receipt](provenance/stage3-test-run.json),
[foundation receipt](provenance/stage3-verification.json),
[continuation receipt](provenance/stage3-continuation-verification.json) and Git
manifest identify their scopes and actual artifacts. Automated checks are
evidence for their stated digital models, not proof of biological efficacy.

## Current limiting findings

The monitor's approximately 44.1% nominal-charge uncertainty leaves actual motor
authority negative. Nominal reactive timing exceeds its 100 ms prediction cap.
The known-cue alternative fits unassisted measurements but fails during assisted
validation. Those failures set redesign requirements; they are not hidden by a
desired learning multiplier or favorable biological tuning.

The pressure branch has identified conditional pressor feedback, faults and
finite stop/hold/ramp responses. It uses external pressure because its dense
stimulation does not qualify continuous neural recording. It does not claim
universal autonomic control or healthy-consumer efficacy.

## Next move

Continue the Stage 3 **teacher/library and assisted-observer revision**: gate
teacher competence, independently validate assisted/context prediction, test
full moving-body aperture/source sensitivities, and rerun matched practice/OFF
assessments with new result identities. Preserve unavailable references,
negative controls, nonbeneficial plasticity and actual electrical rejection.

Translate the resulting precision/timing requirements into the
[electronics handoff](docs/stage3/mechanism-to-electronics-handoff.md), then
proceed to full native circuits/firmware and populated CAD. The existing
[tool audit](docs/stage3/toolchain-selection.md) verifies the installed free
KiCad/ngspice/FreeCAD/build123d/Blender stack; no new paid software is needed.

Stage 3 ends when its digital mechanism, numerical/information boundaries,
comparisons and failure tests are sufficiently resolved to support a concrete
detailed design. Human experimentation and a guaranteed positive consumer
result are not requirements to invent. Remaining items are tracked individually
in the [progress record](docs/stage3/verification-progress.csv).

Working branch: overhaul/full-scci-system.
Private draft review: https://github.com/pratham-cloud-ctrl/Project-ATO/pull/1.
Original synced ChatGPT project sources remain read-only.

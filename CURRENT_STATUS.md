# Project ATO: current work status

Updated: 8 October 2026.

## Active objective

Overhaul the existing release into a complete proposed invasive SCCI system for
expert-informed motor learning and selected physiological automation, with a
coherent mechanism, full digital electronics/embedded architecture, engineering
CAD, paper and professional private GitHub repository.

The full implant/controller design is **in progress**. Video and website are parked.
Release `v1.0.0` is a historical digital subsystem reference, not the final system
the owner requested. Its existing paper and verification receipts describe that
earlier release only.

## Current phase

Stages 1 and 2 design packages are complete for review. The
[dossier entry point](docs/stage1/README.md) connects the complete system specification,
application mechanisms, primary-source audit, architecture alternatives, interfaces,
requirements, assumptions, capability map and verification matrix. An illustrated
nine-page brief accompanies three editable vector mechanism diagrams.

The [Stage 2 dossier](docs/stage2/README.md) adds selected 16-stream/2-source
architecture, source-audited numerical inputs, eleven control contracts,
reproducible budgets and an eight-page illustrated brief with six scientific
figure pairs. Native FreeCAD/STEP models contain 80 allocation solids, a core
can/header, companion and 36 illustrative body ports. These are preliminary
allocation models, not populated implant CAD.

The owner requested a Stage 2 completion/alignment audit before Stage 3.
That [exit review](docs/stage2/exit-review.md) corrects the 32-stream RAM prose,
separates profile rates from physical-source service, adds finite flash/network
memory and output-configuration bus allocations, and reconciles all36 logical
ports with the CAD. Native inspection now covers all3,088 nominal part pairs
apart from72 explicit header/interface reservation pairs. Stage3 is now in progress.

The [Stage3 foundation](docs/stage3/README.md) implements synthetic16-stream spinal
contact acquisition, causal decoding, separate expert data, observed learner
response identification and stimulation-off retention/transfer. The reduced
electrical model resolves phase edges and compliance analytically, observes
delivered charge with an independent noisy ADC and latches post-fault admission.
Independent ngspice and numericalODE comparisons check its linear equations.
The external-SBP model includes identified pressor authority,13 response/sensor
families and finite stop/hold/ramp fallbacks.

The saved foundation batch contains 12 motor configuration/seed studies (336
plasticity-family/comparison rows and 18 separate negative-control witnesses),
156 pressure runs and eight additional fallback runs. Three scientific SVG/PNG
figure pairs and the results interpretation are generated from these saved
outputs. The current 67-test suite passes; independent electrical checks retain
150 ODE cases, 493 eligible ADC cases and seven explicit exclusions.
Six separately scoped pressure refinement probes preserve the same actual
sensor-noise draws and fixed observation schedules. Their small differences
support a limited diagnostic; the full convergence matrix remains open in the
[numerical plan](docs/stage3/numerical-convergence-plan.md).

Independent audits corrected source backdating, training leakage, hidden threshold
access, recursive filter validity, uncertainty propagation and fault-dose erasure.
The selected nominal reactive motor path exceeds its100ms prediction horizon;
the conservative delivery bound also fails the current local authority gate.
Actual integrated abstention is preserved. A separately labeled fast-response
assumed-delivery branch explores the learning mechanism conditionally; it is not
an implemented precision-monitor or biological efficacy result.

The [overhaul plan](docs/overhaul-plan.md) defines later stages and completion criteria.
Catalog component witnesses and provisional envelopes are selected for budget
work; actual complete circuit/layout, anatomy and packaging remain in development.

Working branch: `overhaul/full-scci-system`.

## Next bounded work package

Continue Stage3 from the implemented models and
[results interpretation](docs/stage3/results-and-interpretation.md). Resolve an
observed-data motor policy/calibration domain that earns bounded authority:
consider per-profile identification, known-cue prediction and independently
qualified delivery precision. Complete capacity-matched external-history,
assisted-context decoder validation, motor numerical convergence and broader
expert/source/structural sensitivity studies. Do not alter biological parameters
or uncertainty bounds silently to manufacture a positive result.

S1-V-204 now has conditional observed pressure identification and modeled
authority failures; real biological reachability remains unestablished. Stage2's
low-current profiles remain electrical references, not proven effective doses.
Stage3 is not complete and Stage4 has not begun. The new
[progress record](docs/stage3/verification-progress.csv) identifies remaining
criteria individually; the [tool audit](docs/stage3/toolchain-selection.md)
records fresh installed-tool checks and official free/student alternatives.
The [motor precision analysis](docs/stage3/motor-precision-requirements.md)
quantifies the current uncertainty and exposes shared ADC/bus ceilings. Its
prospective sampling/guard alternatives are requirements for a later revision,
not changes to the frozen design or results.

Existing lower-limb quadrature and pressure models are candidates/supporting
experiments. The selected new reference tasks above come from the mechanism
review; historical results are not promoted to full-system evidence. Reopen
channel counts, lead geometry and package budgets when the new models require it.

## Continuing constraints

- Entirely digital; private repository; no deadline imposed.
- Both main ambitions remain in scope, together with a bounded future-capability map.
- Keep spinal neural access central; label any brain input as a hybrid change.
- Distinguish evidence, hypothesis, assumed biological interface and digital validation.
- Expert neural information must have a defined role; do not silently replace it
  with a task trajectory and claim expert neural transfer.
- Retained learning is measured with assistance removed; no desired multiplier is
  inserted and then reported as a discovery.
- Synced files under the ChatGPT project's `sources/` remain read-only.
- Preserve originals and the historical release; maintain source/decision provenance.

## Completed work in this overhaul

Reviewed current native design scope, models, architecture, evidence register and
the original paper's mechanism sections. Independent planning audits covered
research, electronics and model/CAD gaps. Added the overhaul plan and continuation
record. Stage 1 adds complete mechanism chains, 36 requirements, 14 assumptions,
14 capability entries, 4 access alternatives, 13 owned modules, 15 interface
contracts and 50 planned verification checks. The primary-source audit records
the actual access scope and limits of the cited studies. Specification consistency
and PDF visual review are recorded separately from historical engineering tests.
No new scientific efficacy result or full-system validation is claimed.

Stage 2 selected calculations pass for the two low-current references under
declared load/efficiency/thermal assumptions. They explicitly reject the strong
pressure case for continuous operation in this package, the all-max waveform,
64 MHz workload, 2 s raw-rate ring, continuous raw telemetry and dense-pressure
neural decoding. Archive validity propagation makes pressure archive entirely
invalid during its train. Sensor freshness, actual thermal resistance, circuit
recovery, electrode chemistry and recruitment remain unresolved. Geometry and
PDF review receipts are tied to the actual artifacts, separately from historical
tests. Private draft review: https://github.com/pratham-cloud-ctrl/Project-ATO/pull/1.

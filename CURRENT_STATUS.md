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

The [overhaul plan](docs/overhaul-plan.md) defines later stages and completion criteria.
Catalog component witnesses and provisional envelopes are selected for budget
work; actual complete circuit/layout, anatomy and packaging remain in development.

Working branch: `overhaul/full-scci-system`.

## Next bounded work package

Stage 3: implement the computational mechanism for paced multidirectional foot
placement and external systolic-pressure feedback. Generate contact observations
through a declared spinal-population/electrode model; the controller must not read
hidden states or true response coefficients. Identify learner responses from
allowed observations, connect output plans to delivered-current/body models,
and assess neural/external and expert/learner comparisons fairly. Include null,
harmful, stale-sensor, artifact, weak-authority and unreachable-target cases.

S1-V-204 remains partially specified: functional reachability needs identified
uncertain response bounds in Stage 3. Do not invent positive learning coupling
or pressor gain to force a desired outcome. Stage 2's low-current profiles are
electrical reference cases, not established biologically effective settings.

Existing lower-limb quadrature and pressure models are candidates/supporting
experiments, not automatic decisions about the full device. Reopen channel counts,
lead geometry and the desktop enclosure choice.

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

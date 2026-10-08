# Stage 2 exit review and handoff

**8 October 2026. Scope: quantified proposed architecture, interface contracts
and preliminary mechanical allocations.** This review closes that work package.
It does not close the full SCCI project or claim a flawless, clinically qualified
implant. Stage 3 has not started.

## Alignment with the intended project

The central object remains an invasive spinal recording/stimulation platform.
Expert observations are translated into a task representation and a calibrated
learner-specific intervention; active practice and unassisted retention are
separate outcomes. A second, function-specific application uses external systolic
pressure feedback and a proposed spinal pressor pathway. Neither a desktop box
nor the older timing surrogate substitutes for this full concept.

The foot-placement and systolic-pressure cases are reference applications that
expose information, timing, delivery and packaging constraints. They do not erase
the broader piano, sport and consumer vision in the
[capability map](../stage1/capability-map.csv). They also do not establish that
one fixed anatomical lead set serves every application. AstroSam's Mind-Link
continues to inspire the paper-to-designed-device structure and receives credit.
The main deliverables remain the illustrated paper, native electronics, implant/
companion CAD and a reproducible private GitHub repository. Video and website
are parked; the project is entirely digital.

## Exit criteria

“Complete” in this table means the Stage 2 architecture artifact exists and its
declared calculations/consistency checks pass. Conditional values remain labelled
as assumptions. Unknown biological effectiveness is not turned into an input fact.

| ID | Stage 2 deliverable and completed check | Conditional handoff |
|---|---|---|
| S2-X-01 | Both applications, causal information permissions and per-target access variant are explicit | Useful spinal information, recruitment and retained learning require Stage 3 models and future empirical tests |
| S2-X-02 | 16 streams, one neural ADC, two current sources, 36 functional ports; [port allocation](functional-port-map.csv) reconciles CAD labels and logical functions | Pin/net/lead/anatomical mapping follows in Stages 4/5 |
| S2-X-03 | Quiet/adverse noise, dynamic range, sampling, channel skew, causal filter and archive-invalidity calculations reproduce | Real input range, protection and artifact recovery remain unqualified |
| S2-X-04 | Finite CPU, application RAM/flash and separate network RAM/flash budgets; 32-stream and raw-ring failures preserved | Actual linked image and worst-case execution require Stage 4 |
| S2-X-05 | Causal age, frame-wait failures, advance paced-goal scheduling, pressure freshness and clock bounds are explicit | Actual information age and learner response uncertainty can veto an intervention |
| S2-X-06 | Per-profile repetition and cyclic physical-source service are separately checked; finite third-bus command allocation fits | Actual routing/DAC protocol, return health and rearm must satisfy the allocation |
| S2-X-07 | Joint phase charge, compliance, pair capacitance and reservoir calculations retain rejected combinations | Delivered waveform, nonlinear electrode chemistry and residual charge remain Stage 3/4 work |
| S2-X-08 | Independent delivery ADC capacity, sensor-error/edge assumptions and protection responsibilities are specified | A separate ADC alone is not independent shutdown; trip circuitry remains Stage 4 |
| S2-X-09 | Energy, converter/base power, case heat, thermal sensitivity and current limits reproduce | Unknown thermal coupling, cell behavior and tissue hotspots can invalidate nominal operation |
| S2-X-10 | Finite telemetry, companion power and separate pressure-instrument/Studio dependencies are explicit | Through-tissue RF, coil losses and a portable consumer pressure sensor remain unqualified |
| S2-X-11 | Native FreeCAD/STEP allocations reopen; all nominal parts are valid and physical interference checks pass | Preliminary envelopes are not populated boards, qualified feedthroughs, anatomy or sealing |
| S2-X-12 | Source audit, contracts, illustrations, tests, artifact hashes and repository workflow agree | The final integrated paper and full-system release follow Stages 3–6 |

## Findings corrected by this review

1. Corrected a prose-only 32-stream RAM figure to **589,952 bytes**, matching the
   calculated 84-byte frame and scaled feature/working buffers.
2. Removed ambiguous “source minimum period” wording. The 150 Hz limit is per
   profile. The chosen pressure assignment puts three 120 Hz profiles on source 0:
   360 events/s with 2 ms minimum cyclic spacing. A 0.95 ms service allocation
   includes the waveform and 250 microseconds of zero-current reconfiguration.
   Source availability does not certify electrode reset or permit rate evasion.
3. Added complete application flash and separate network memory allocations.
   A second resident firmware image is not silently stored in unused memory.
4. Reserved SPIM1 for output configuration: 128 microseconds maximum wire time
   plus 122 microseconds local work inside the existing admission allowance.
   Phase edges remain locally timed; SPI capacity is not a gate-timing proof.
5. Added a functional 36-port allocation, full nominal CAD inspection and focused
   failure tests for source collisions, frame wrap, invalid source assignments,
   profile-rate/identity evasion and oversized flash images.
6. Updated the illustrated brief and stale programme wording. All applicable
   automated checks, visual review and GitHub checks are rerun for this revision.
7. The fresh Linux checkout exposed Windows/LF text-hash drift in the new CAD
   inspection receipt. That binding now uses explicitly canonicalized JSON,
   with a regression check that ignores line endings while detecting changed
   geometry values or array order. The Git manifest still binds exact blob bytes.

## What Stage 2 passes to the next stages

Stage 3 must evaluate whether an intervention with these electrical, timing and
energy limits can produce useful modeled authority. The low-current references
are not assumed effective. Null/adverse recruitment, inadequate observability,
assistance dependence, ambiguous identification and unreachable targets remain
required cases. Any stronger required output must reopen the power/package
design rather than bypass its limits. S1-V-204 remains an explicit Stage 3 task.

Stage 4 owns the complete KiCad circuits/layout and embedded implementation.
Stage 5 owns populated component/lead CAD and nominal mechanical co-design.
Stage 6 owns integrated digital verification and the final illustrated manuscript.
The [progress table](verification-progress.csv) preserves those boundaries.

The verification receipt records this review's executed checks. It is an
AI-assisted consistency/engineering review, not an independent licensed audit.
There is no claim that every unknown has been solved or that more reasoning
effort eliminates the need for verification.

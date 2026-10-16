# Conditional SCCI concept: requirements for electronics and CAD

13 October 2026. This handoff connects the clarified future concept to detailed
engineering. Undemonstrated biological assumptions are permitted when explicit
and defensible. The [assumption ledger](assumption-ledger.csv),
[motor evidence](motor-evidence.md) and
[physiological evidence](physiology-evidence.md) separate experimental anchors,
chosen numerical scenarios and future implementation requirements.

## Mechanism and model boundary

The future motor system records task-related expert and learner spinal activity,
interprets a bounded coordination component, translates it to learner-specific
stimulation, and adapts assistance using independently observed delivery and
movement. The healthy-consumer extension concerns improved practice of a
selected component of a skill. Rehabilitation precedents motivate the mechanism;
they do not establish healthy expert transfer or a learning-speed multiplier.

The new explanatory model uses two-dimensional cyclic motion, abstract spinal
features learned from externally labelled calibration, a calibrated task-space
response map, and delayed assistance. Its learning rule varies an unmeasured
effective teaching coefficient, including adverse and zero-benefit cases.
Immediate execution and subsequent stimulation-OFF learning are separate
outcomes. A known cue may support phase prediction; future achieved movement is
not a controller input. Neither this compact model nor the earlier conservative
studies are a human digital twin.

## Information and action contract

| Interface | Required information | Interpretation |
|---|---|---|
| Recording -> decoded feature | Contact/montage ID, sample support and arrival times, feature value, uncertainty, validity, calibration ID | A feature computed from old or blanked data cannot become a fresh observation. Sixteen abstract model features are not sixteen experimentally proven human neural channels. |
| Expert reference -> learner mapping | Task/context ID, reference phase or coordination, source modality, learner alignment, uncertainty | Offline expert spinal reference and live learner spinal estimation are distinct contributions. No raw waveform replay. |
| Policy -> profile and route | Program/profile ID, source ownership, contact/return route, amplitude bounds, intended onset, expiration | A signed task correction selects a separately calibrated recruitment direction. Negative electrical current does not establish biological inhibition. |
| Driver -> delivery monitor | Actual cathodic/anodic phase charge, current/compliance validity, physical intervals, interrupted phase and tail | Requested and measured output are distinct. Net bipolar charge alone can hide oversized individual phases. |
| Body -> response estimate | Independent movement/force or pressure, support/arrival times, quality and calibration | Electrical delivery does not measure a successful biological response. |
| Practice -> OFF assessment | Assistance ended, residual-response rule, common probe exposure, delayed retention/transfer score | Assistance-OFF outcome must exclude remaining actuator response; consumer learning cannot be inferred from an ON improvement. |

## Preserve resource identity

The [Stage 2 baseline](../../stage2/selected-design.md) allocates **16 differential
recording streams at 4 ksample/s per stream**, **two independent stimulation
sources**, and 36 body-interface ports. The neural converter is multiplexed;
physical channel apertures remain distinct. Program count does not multiply
source count. These are resource allocations, not evidence that sixteen
contacts reveal every required human state.

The selected access concept is intradural surface recording with separate
epidural stimulation. Target-specific motor and pressure variants initially use
exclusive operating modes. A shared core does not prove that one anatomical
lead arrangement serves both applications. Coexisting lead sets need an explicit
contact/feedthrough partition and updated package requirements.

The illustrative **25 ms frame**, **40 ms activation lag**, **35 ms onset** and
nominal normalized dose **1.0** are design assumptions. Their successful use in a
simulation does not certify embedded scheduling, circuit precision, tissue
response or a clinical waveform. Stage 4 must derive measurable timing and
charge requirements from the selected operating scenarios. The current native
monitoring candidate has not earned any newly assumed delivery accuracy.

## Pressure and neural feedback

External pressure sensing remains the primary feedback for the physiological
branch. The selected actuator adds pressor drive through a target-specific
spinal pathway. Withdrawing stimulation removes that added drive; it supplies no
independent authority to lower arbitrary high pressure. Feedback quality,
latency, saturation, changing gain and withdrawal therefore remain explicit.

Optional spinal ECAP/recruitment or context features can augment this loop under
separate assumptions. ECAP is not automatically a pressure measurement. Dense
stimulation also does not guarantee available neural samples. Declare an
external fallback, its resources and its limits rather than silently switching
the origin of a supposedly neural observation.

## Next engineering deliverables and finite closure

Complete the native recording/protection chain, bounded driver/routing circuit,
independent delivery monitoring and inhibit, power/communications, and firmware
interfaces. Use actual component requirements to revise power, heat, memory,
buses and PCB geometry. Populate parametric CAD from those boards and lead/port
allocations; enclosure appearance does not earn thermal, chronic-access or
biocompatibility claims. Existing catalog witnesses and allocation solids remain
starting points, not a finished implant package.

This concept revision closes when the premise ledger, source boundaries,
causal model, ON/OFF results, adverse/null scenarios and engineering interfaces
agree. New biological proof is not required to finish that conditional design.
Positive model outcomes remain labelled conditional; earlier conservative
zero-assistance records stay unchanged. Stage 4 then tests the electrical and
embedded implementation against explicit requirements instead of reopening an
unbounded neuroscience qualification exercise.

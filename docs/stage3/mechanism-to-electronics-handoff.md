# Mechanism requirements for the detailed electronics design

9 October 2026. This is the handoff from reduced Stage 3 mechanisms to the
upcoming native electronics/firmware work. It is not a completed KiCad design,
selected monitor revision or implant qualification.

The system must retain the complete spinal recording → interpretation →
personalized stimulation → monitored response → feedback chain. Both retained
motor practice and specific physiological feedback use the platform, with
target-specific contacts and operating profiles. The existing Stage 2 FreeCAD
solids are allocation envelopes, not populated engineering CAD.

| Interface or responsibility | Present baseline / finding | Required detailed-design evidence |
|---|---|---|
| Recording | 16 contact streams at 4 kHz with timestamped block acquisition | Native differential acquisition/filter/ADC circuitry, noise/dynamic range, physical aperture timestamps, clipping and missing samples |
| Artifact/recovery | Digital residual qualification can reject recordings long after a train | Analog recovery/saturation analysis, route-coupled artifact model and recorded validity; the software counterfactual does not certify an AFE |
| Output | Two independent physical sources, whole 40 Hz reference profiles | Source/routing ownership, simultaneous-source service, waveform sequencing and no fractional catch-up pulses |
| Delivered dose | Independent current/charge/compliance observations; nominal uncertainty about 44.1% of phase charge | A revised independently evidenced integration/edge/guard scheme if tighter precision is needed; correlated errors and interrupted dose retained |
| Timing | 11.85 ms processing allocation plus support age, frame wait and observed response onset | Actual embedded schedules, buffering and worst-case latency, observed clock bounds, expiration and cancellation |
| Response authority | Actual motor authority remains negative; finite conditional resting maps only | Profile/route/context-bound mapping and uncertainty, including the product of gain and dose uncertainty; unsupported cases inhibit |
| Forecasting | Nominal known-cue component fits; assisted-context validation fails | A validated observed assisted predictor before coupling, or a separately justified policy; future commanded dose cannot be treated as measured |
| Pressure feedback | External pressure supports the selected model; dense active blocks do not qualify neural recording | Sensor transport/support/freshness, feedback/fallback state machines and appropriate power/rate allocations; no invented neural pressure value |
| Fault supervision | Offline pulse admission/rearm and finite fallback witnesses exist | Continuous route switching, guard latency, waveform faults, link loss, reboot and power behavior exercised in native circuit/firmware models |
| Power/package | Stage 2 budgets include rejected continuous strong-pressure and all-max cases | Recalculate instantaneous/average power, heat, memory and buses for actual components; populate matched CAD envelopes |

The current monitor candidate allocates 1 MHz aggregate ADC throughput and a
16 Mbit/s shared bus. Those limits apply across both sources and health/voltage
traffic. Prospective sampling rates from the
[precision requirements](motor-precision-requirements.md) are a redesign demand,
not approved settings on the existing architecture. More samples alone do not
prove a smaller edge, intersample waveform or gain error.

KiCad, ngspice, FreeCAD/build123d and Blender are already available in the
[verified free toolchain](toolchain-selection.md). Use KiCad for native electrical
sources and board layout, ngspice for scoped circuit evidence, and parametric
FreeCAD/build123d assemblies for component/package fit. Blender follows the
engineering geometry for technical views. No new paid software is required for
this handoff.

Keep interfaces, units, profile IDs and evidence qualifications machine readable.
Revise channel, monitoring, power or package budgets openly when mechanism work
requires it. A polished enclosure or PCB must not hide an unresolved causal link.

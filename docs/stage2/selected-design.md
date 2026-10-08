# Selected design, budgets and decisions

Document **S2-SYS-001**, 8 October 2026. All results below are deterministic
calculations under declared inputs, not observations from hardware or people.
The [input configuration](system-design.json), [reproduction script](../../scripts/run_architecture_budgets.py)
and [complete results](../../results/stage2/budget-summary.json) are the quantitative record.

## Reference mechanism and interface choice

The motor reference is a **paced alternating foot-placement sequence with
direction changes**. The learner practices their own movement. Expert spinal
observations contribute a task-related representation; learner calibration maps
that representation to a learner-specific assistance policy. Contact timing,
placement and coordination are observable outcomes. The proposed 25 ms event
scheduling tolerance and 500 ms nominal event spacing are engineering choices.
Whether the selected spinal observations add useful information, or practice
produces retained learning, remains an experimental hypothesis.

The physiological reference is **external systolic-pressure feedback after SCI**,
using target-specific epidural stimulation with pressor-only authority. The
interface cannot assume an independently controlled pressure-lowering response.
The two modes are initially exclusive. Cervical/piano, bladder and other future
variants remain in the [Stage 1 capability map](../stage1/capability-map.csv).

The chosen access baseline is **S1-ARCH-02: intradural surface recording and
separate epidural stimulation**. Each application needs its own placement and
recruitment calibration. Spinal segments and vertebral levels must be labelled
separately. This proposed combined architecture is not demonstrated by the cited
studies. Shared epidural access or local bipolar recording remains a revision
path if observation quality or implant interfaces fail.

## Contact, conversion and output inventory

This inventory is **per target-specific configured variant**. Motor and pressure
reference models share the core architecture, while anatomical interfaces can
differ. A single implant with coexisting motor and pressor lead sets would need
an explicit partition of the sixteen output contacts and renewed recruitment
tests, or more contacts and a revised feedthrough/package budget. Exclusive
software modes alone do not resolve that anatomical requirement.

| Resource | Selected allocation | Meaning |
|---|---:|---|
| Recording contacts | 16 + 1 reference + 1 bias | 18 physical connections, yielding 16 differential streams |
| Neural converter | One multiplexed 16-bit ADC in RHD2216 | Sequential apertures, not 16 simultaneous ADCs |
| Acquisition/archive | 4 / 2 ksample/s per stream | Fast decoding uses raw-rate causal samples; archive is decimated |
| Stimulation contacts/returns | 16 + 2 dedicated returns | 18 physical connections; routing does not multiply driver count |
| Regulated current sources | 2; at most 2 concurrent | Three pressure profiles run sequentially, not through three simultaneous sources |
| Delivery converter | Separate ADS7953, 12-bit, 1 Msample/s capacity | Neural ADC is not used to certify delivered current |
| Body feedthrough inventory | 36 ports | Housing is not implicitly a stimulation return |

Intan RHD2216, nRF5340, ADS7953 and LT8365 are **catalog feasibility witnesses**.
Protection, circuit implementation, temperature behavior, implant-grade sourcing,
component ratings and package integration are not established. Exact pin-level
schematics and native KiCad layout are Stage 4 deliverables.

## Recording, computation and communication

The shared-reference topology passes the chosen quiet 10 dB SNR screening gate
under nominal assumptions: 2.511 µV total RSS noise and 12.00 dB SNR for a
10 µV RMS signal. A high-impedance/reference mismatch case gives 25.936 µV noise
and −8.28 dB SNR. It **fails** and must invalidate neural use or cause a montage/
AFE revision. These are selected signal assumptions, not a known human range.

The neural command burst occupies 57 µs of a 250 µs scan interval, with a 45 µs
channel-aperture span. Keep individual sample timestamps. The separate monitor
requires 450 ksample/s: two current streams at 200 ksample/s, two voltage streams
at 20 ksample/s and 10 ksample/s housekeeping. Its proposed 16 MHz SPI bus is
49.5% occupied including a chosen 10% command allowance. Distinct peripheral
engines prevent the monitor from silently consuming the neural bus budget.

The compact 200 Hz decoder, streaming features/archive and monitor integration
allocate **43.1986 million cycles/s**, or 33.75% of a 128 MHz application core,
including 15% contingency. The same work fails a chosen 60% budget at 64 MHz.
This is arithmetic, not a firmware benchmark; worst-case scheduling still needs
measurement. The 2 s archive ring is 192,000 bytes. Total application RAM is
404,992 of 524,288 bytes, leaving 22.75%. Compact coefficients and state share
the 32 KiB feature allocation; the immutable policy has a 64 KiB flash reservation.
There is no second hidden 32 KiB policy RAM. A 2 s raw-rate ring raises the total
to 596,992 bytes and **does not fit**.

The full normal service (features, delivered-output summaries and health, plus
30% payload headroom) is **86,528 bit/s**, inside a selected 160 kbit/s service
target. The acquisition note's 51.2 kbit/s compact packet witness is a smaller
service, not the full aggregate. Raw 4 ksample/s framed recording is 1.536 Mbit/s
and fails the separate 1 Mbit/s target. Raw 2 ksample/s is 768 kbit/s before
radio overhead and must use a special mode/energy budget. Through-tissue RF
performance, encryption/retries and antenna geometry are not verified.

Application flash now has a complete single-image allocation: 827,392 of
1,048,576 bytes, leaving21.09%. Network flash and RAM have separate allocations,
leaving31.25% and25% respectively; they do not expand application capacity.
A third8 MHz SPIM1 bus reserves128 bytes/128 µs per maximum admission
transaction plus122 µs local work inside the existing250 µs allowance.
The [acquisition note](acquisition-and-compute.md) states the partition and
service-update limits. Actual images, bus protocols and execution remain Stage4.

## Timing and recording during stimulation

A revised 0.75 ms policy allowance gives an **11.85 ms** unframed fast processing
chain. A uniform 20 ms trailing history has a representative age of **21.85 ms**
at delivery; this is not a guarantee for masked samples or recursive features.
Adding the archive FIR produces 25.60 ms representative age, so archive data is
excluded from the nominal fast motor path. Low-frequency content also carries
real delay: the ideal analog response gives 16.819 ms at 1 Hz before later stages.

A free-running 40 Hz output frame adds up to 25 ms wait: total **36.85 ms**,
failing the chosen 25 ms reactive target. The design therefore uses known paced
goals with advance admission, or qualified event-anchored scheduling with source
minimum-period constraints. It cannot evade output-rate limits by resetting phase
or infer future body state from a known future task cue.

The150 Hz limit applies per profile. The [source schedule](timing-and-control.md)
assigns all three pressure profiles to source0 at360 events/s, with2 ms minimum
cyclic spacing. Its0.7 ms waveform plus0.25 ms zero-current reconfiguration
fits the declared service interval. Motor sources each reserve0.75 ms per25 ms
period. Rate limits, physical-source conflicts and electrode/return qualification
remain separate predicates; amplifier recovery is not permission to reuse a route.

Motor reference blanking is 6.4% with a 100 µs preguard and 1 ms assumed amplifier
recovery; minimum usable coverage in any 20 ms window is 92%. Pressure-mode
three-profile blanking is **64.8%** with the same preguard, versus 61.2% without
it. At 3 ms assumed recovery it becomes 93.6%; at 5 ms it covers the entire frame.
Pressure mode consequently relies on external pressure feedback. Recovery ends
only when actual validity checks pass. A 1 ms allowance is not proof of electrode
reset: a declared adverse RC case takes about 13.25 ms to approach its residual
threshold. Dense stimulation cannot be relabelled as ordinary independent noise.

The causal archive FIR has 7.5 ms input support. Propagating any invalid raw
sample through that support yields **36.4% invalid motor archive output and 100%
invalid pressure archive output** during these nominal pulse trains. Retain those
validity flags rather than present stored values as observations. Fast motor
control uses a separate raw-rate path; recursive feature reset and warm-up must
still be tested. Global raw coverage alone does not qualify its decoder.

## Joint stimulation limits and delivery evidence

The range 0.1–20 mA, 50–500 µs per phase and up to 150 Hz per profile does not
permit every combination. The selected software phase-charge ceiling is **9 µC**;
the delivery ceiling is **10 µC** including uncertainty. Both are engineering
limits, not chemically safe charge claims. Equal commanded phases do not establish
equal delivered charge. Current must be integrated and faults/clipping accounted for.

The monitor's ±25 mA signed span gives 12.207 µA/LSB. With chosen 2% gain,
5 µA offset and 5 µs edge uncertainty, a constant 3 mA/200 µs phase has 7.37%
charge uncertainty. The 0.1 mA/50 µs lower corner has approximately 33.1%.
Precision is not uniformly 2%. Inter-sample spikes and independent output trip
timing remain separate circuit requirements.

At the highest 48 V rail, 40 V is available after driver/routing/droop allocation.
With a 4 V combined polarization reserve, 20 mA needs 44 V through 2 kΩ and
**fails**. Its simple current ceiling is 18 mA, lower with additional blocking or
polarization. Pair capacitance is swept separately from per-contact capacitance.
The effective 33 µF HV reservoir yields 1.212 V droop for two 20 mA symmetric
500 µs pulses, against a 2 V allocation. Real capacitance at DC bias, stored-energy
fault behavior and switch ratings still need circuit/part selection.

## Power, heat and duration

The base allocation is 74.5 mW: 4.5 AFE, 35 compute/network, 20 delivery monitor/
analog, 5 low-voltage regulation, 8 driver quiescent and 2 boost overhead.
These are finite design allowances, not guaranteed maxima. Converter efficiency
is assumed 80%; power cannot be inherited from a manufacturer's unrelated example.

| Continuous schedule, conditional on the model | Total battery power | Nominal runtime | Case rise at assumed 20 K/W | Decision |
|---|---:|---:|---:|---|
| Motor: two 3 mA/200 µs profiles, 40 Hz, 24 V rail | 77.38 mW | 7.44 h | 1.54 K | Selected arithmetic gates pass |
| Pressure: three 3 mA/300 µs profiles, 120 Hz, 24 V | 93.94 mW | 6.13 h | 1.84 K | Selected arithmetic gates pass; neural fast mode fails |
| Pressure stress: three 20 mA/300 µs profiles, 120 Hz, 48 V | 333.70 mW | 1.73 h | 4.95 K | Reject continuous; low-cell current and heat fail |
| Two all-max profiles: 20 mA/500 µs, 150 Hz, 48 V | 434.50 mW | 1.33 h | 6.29 K | Reject; command/delivery charge, current and heat fail |

Runtime uses 3.6 V × 200 mAh × a chosen 80% usable-energy factor = 0.576 Wh.
The [Contego cell](https://resonetics.com/wp-content/uploads/2022/08/15507-01-Battery-Brochure-Contego-200-mAh.pdf)
capacity is specified at C/5 and 20 °C, not guaranteed under this complete load
or chronic history. Its case is negative and requires isolation. A selected
100 mA average-current cap rejects the pressure stress at 3.0 V (111.23 mA).
This cap is a design choice, not a universal battery limit.

The heat estimate subtracts modeled resistive load deposition from battery power
and conservatively assigns the remainder to package heat. It is not a tissue
hotspot model. The **2 K rise target is an engineering choice, not a clinical
safety threshold**. Nominal pressure requires thermal resistance ≤21.74 K/W;
at 40 or 60 K/W even the references fail. Temperature-dependent derating and
measured/field thermal qualification are mandatory unresolved gates. Starting
from ambient, the high-current stress reaches 2 K in about 155 s under the lumped
model; a warm start shortens that time. This is not a permitted treatment duration.

Idle charging adds a separate provisional allocation: 20 mA at 4 V stores 80 mW;
85% assumed receiver-to-cell efficiency plus 10 mW idle implies 24.12 mW package
heat and 0.48 K rise at 20 K/W. Capacity/current alone gives 10 h before taper.
The 100 mA option gives 80.59 mW heat and 1.61 K rise in this idealized budget.
Coil/link losses, tissue deposition, alignment, charging taper and operation
during charging remain unresolved; these arithmetic rows do not close the charger.

## Decisions and review gates

The companion has a separate **chosen 5 V/1 A external source** and a 1 W base
allocation (0.35 W bridge/network, 0.25 W display, 0.15 W interfaces, 0.25 W
regulation). Remaining source headroom is not automatically a qualified wireless
charger. The continuous-pressure instrument is separately powered and is not
claimed to fit inside the 100×60×24 mm hub. Its portable consumer replacement,
actual sensor consumption and transcutaneous charging/field losses remain open.
The offline expert/calibration Studio runs on an externally powered host; those
computations are not silently assigned zero cost inside the implant.

| Decision | Selected resolution | Reopen when |
|---|---|---|
| S2-D-01 | Separate recording/stimulation access | Human task information or interface quality insufficient |
| S2-D-02 | 16 shared-reference streams at 4 ksample/s | Loading/noise or held-out decoding fails; test local bipolar/reference redesign |
| S2-D-03 | 128 MHz, 512 KiB application core | Measured execution/memory violates reserved margin |
| S2-D-04 | 2 sources, separate delivery ADC and SPI | Concurrency/recruitment or monitor bandwidth needs more hardware |
| S2-D-05 | Advance paced-goal admission; raw fast path | Unpredictable-event requirement or measured latency changes |
| S2-D-06 | Pressure uses external SBP; neural state optional | Neural biomarker shows incremental value with valid samples |
| S2-D-07 | Low-current reference profiles; reject continuous high stress | Demonstrated authority requires stronger output; enlarge power/thermal system or revisit application |
| S2-D-08 | 60×48×14 mm can plus 60×10×14 mm header | Populated board, feedthrough, antenna or anatomy conflicts |

A successfully passing arithmetic gate does **not** qualify an unknown biological
mapping, electrode chemistry or actual component. Admission must combine resource
limits with calibration, waveform validity, route/return health, timing and
sensor freshness. Model uncertainty may deny output even when the budget fits.

Stage 2 supplies inputs and contracts for Stage 3. Actual complete electronics,
embedded implementation and populated implant CAD remain Stage 4/5 work.

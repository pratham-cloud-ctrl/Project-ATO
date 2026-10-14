# Stage 4: remaining digital engineering packages

Updated 14 October 2026 after the actual nRF5340 firmware checkpoint.
Seven circuit packages now exist: monitor, restricted driver, recording front end,
contact router, supervision, power and monitoring/companion interfaces. Their component-level checks and finite models do not yet constitute
one integrated populated electronic system. Actual bounded target firmware now
builds alongside them. Stage 3's conditional future concept remains
the design baseline; its closed conservative studies are preserved.

The remaining work is bounded by the following package. A negative result
can revise an operating domain or remain a clearly identified final limitation.
No package requires invented biological success, hardware fabrication or clinical
qualification. Optional additional research is not a new completion gate.

| Order | Package | Digital completion evidence |
|---|---|---|
| 5 | Integrated populated PCB | Consolidated native hierarchy/board(s), nRF5340 controller and explicit four-SN74LVC165A input carrier, actual footprints, net/parity checks, routing, stackup/clearance and DRC. Reconcile the implemented lower-rate firmware profile and electrical/thermal/mechanical allocations; export populated board geometry for Stage 5. Document unsupported manufacturing and physical-performance claims. |

Package 1, [independent supervision and terminal shutdown](supervision-design.md),
is complete within its finite digital scope: 478 native components, 1699 pins,
22 sheets, 18 guarded terminal paths, actual current/voltage/rail/recording
observations, separate phase timers/watchdog, explicit reset/rearm, upstream
wiring and saved fault/analog audits. Unclosed physical delay/leakage, welded
switches, shared-reference failure and brownout behavior remain declared limits.
The power package now generates +3.45/+5.30/−5.10 V AFE rails and separate
always-on supervisor supplies. The provisional 200 µs quiet allocation still waits for actual
qualification; the historical 100 µs gap is unearned.

Package 2, [power and quantitative budget](power-design.md), is complete within
its digital scope: 156 native components, 449 pins, 15 sheets, nine generated
rails, selected protected pack, isolated module/regulators, reference windows,
startup/shutdown and open-drain fault integration. Independent budget checks
pass 3,300 assertions; declared-load active power/runtime are 2.615 W/5.886 h.
Physical efficiency/inrush/stability, full-corner AFE trim, compact implanted
thermal behavior and miniature package remain unearned. The one-cell/100 mA
allocation is superseded. Preserve these results in the next PCB/CAD revision;
new transport hardware must update the power table rather than inherit it blindly.

Package 3, [monitoring and companion interfaces](monitoring-transport-design.md),
is complete within its digital scope: 60 components, 217 pins and eight sheets,
dedicated ADS8688 raw acquisition, explicit shared endpoint MISO, health handoff,
isolated UART, actual aperture/read schedules, configuration identity, packet
freshness/leases, queues and independent input/integration audits. The 450k
aggregate mismatch is resolved. An additive overlay revises active power/runtime
to conditional 2.800 W/5.497 h; existing compact thermal failure remains.
Nonuniform sampling, typical 15 kHz filtering, undetected plausible channel
commands and unearned 4% dose precision remain explicit. The wired interface
does not implement a radio, external pressure sensor or target MCU firmware.

Package 4, [actual nRF5340 firmware](nrf5340-firmware-design.md), is complete
within its bounded digital scope: actual application-core ELF/HEX/BIN and map,
shared production C runtime, explicit peripherals and 46-GPIO ownership,
configuration/readback, active route comparison, phase cutoff through timer/DPPI,
timestamped sample/endpoint records, feature telemetry, companion admission,
leases, explicit recovery and retained fault records. The compiled core passes
75 scenarios/713 assertions. Independent image/source/interface checks accompany
the build receipt. No physical execution or WCET is claimed.

Its nominal lower-rate opportunities can contain known acquisition gaps. The
earlier 450k raw/4k neural proposal, full biological algorithms and continuous
observer remain unimplemented. This is a recorded operating-domain revision,
not synthesized evidence that the earlier schedule runs. The actual image's
memory map covers its implemented buffers and code, not a port of every Stage 3
model. New carrier circuitry remains for the populated PCB; it is not silently
added to the seven frozen native packages.

Stage 4 exits when these packages form an inspectable digital path from artificial
recording inputs through processing and admitted routing/stimulation to observed
electrical feedback, with reproducible finite checks and explicit assumptions.
The proposed expert-to-learner and function-specific physiological mechanisms
remain connected to that path without being mislabeled measured human results.
The 4% dose-precision target and weak-signal/recovery targets must be either earned
within a stated digital model/domain or explicitly reported unearned; they are
not thresholds to tune until a desired consumer claim appears.

Stage 5 then develops the populated native assembly, package and lead interfaces,
dimensions/tolerances, nominal interference checks and STEP/STL exports. Existing
allocation solids remain preliminary. Stage 6 joins the technical work into the
illustrated manuscript, documented learning/defence material and verified private
repository release. Video and website work remain parked.

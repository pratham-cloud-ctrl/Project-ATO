# Stage 4: remaining digital engineering packages

Updated 14 October 2026 after the power/budget checkpoint.
Six circuit packages now exist: monitor, restricted driver, recording front end,
contact router, supervision and power. Their component-level checks and finite models do not yet constitute
one integrated electronic system. Stage 3's conditional future concept remains
the design baseline; its closed conservative studies are preserved.

The remaining work is bounded by the following three packages. A negative result
can revise an operating domain or remain a clearly identified final limitation.
No package requires invented biological success, hardware fabrication or clinical
qualification. Optional additional research is not a new completion gate.

| Order | Package | Digital completion evidence |
|---|---|---|
| 3 | Monitoring transport and companion interfaces | Resolve the existing two ADS8866 devices' 200k aggregate limit against the 450k conversion contract by adding/revising acquisition hardware or rates. Complete endpoint/shared ADC/reference connections, conversion identities, buffering, pressure/sensor freshness, communication and diagnostics. Continuous framed raw 4k data exceed the 1Mbit service; retain that boundary. Keep actual delivery, synthetic models and assumed biological responses separate. |
| 4 | nRF5340 target firmware | Build/link the ATO application/backend, explicit peripheral/pin/timer ownership, configuration/readback, valid samples, route/phase sequencing, supervision, modes and fault records. Publish memory maps and finite timing/fault evidence; desktop checks alone do not count as target implementation. |
| 5 | Integrated populated PCB | Consolidated native hierarchy/board(s), real footprint identities, net/parity checks, routing, stackup/clearance and DRC. Reconcile electrical/thermal/mechanical allocations; export populated board geometry for Stage 5. Document any unsupported manufacturing or physical-performance claims. |

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

# Stage 4: remaining digital engineering packages

Updated 14 October 2026 after the independent shutdown/supervision checkpoint.
Five circuit packages now exist: monitor, restricted driver, recording front end,
contact router and supervision. Their component-level checks and finite models do not yet constitute
one integrated electronic system. Stage 3's conditional future concept remains
the design baseline; its closed conservative studies are preserved.

The remaining work is bounded by the following four packages. A negative result
can revise an operating domain or remain a clearly identified final limitation.
No package requires invented biological success, hardware fabrication or clinical
qualification. Optional additional research is not a new completion gate.

| Order | Package | Digital completion evidence |
|---|---|---|
| 2 | Power and complete quantitative budget | Selected battery/regulators/isolated AFE rails, startup/shutdown and reference circuits. Recalculate component power, converter/peak-current/reservoir, heat/runtime, buses and memory using stated component conditions and assumptions. Revise the old package or power allowance openly when necessary. |
| 3 | Monitoring transport and companion interfaces | Complete endpoint/shared ADC/reference connections, conversion identities, buffering, pressure/sensor freshness, communication and diagnostic boundaries. Keep actual delivery, synthetic models and assumed biological responses separate. |
| 4 | nRF5340 target firmware | Build/link the ATO application/backend, explicit peripheral/pin/timer ownership, configuration/readback, valid samples, route/phase sequencing, supervision, modes and fault records. Publish memory maps and finite timing/fault evidence; desktop checks alone do not count as target implementation. |
| 5 | Integrated populated PCB | Consolidated native hierarchy/board(s), real footprint identities, net/parity checks, routing, stackup/clearance and DRC. Reconcile electrical/thermal/mechanical allocations; export populated board geometry for Stage 5. Document any unsupported manufacturing or physical-performance claims. |

Package 1, [independent supervision and terminal shutdown](supervision-design.md),
is complete within its finite digital scope: 478 native components, 1699 pins,
22 sheets, 18 guarded terminal paths, actual current/voltage/rail/recording
observations, separate phase timers/watchdog, explicit reset/rearm, upstream
wiring and saved fault/analog audits. Unclosed physical delay/leakage, welded
switches, shared-reference failure and brownout behavior remain declared limits.
Power must implement +3.45/+5.30/−5.10 V AFE rails and separate always-on supervisor
supplies. The provisional 200 µs quiet allocation still waits for actual
qualification; the historical 100 µs gap is unearned.

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

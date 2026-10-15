# Project ATO: current work status

Updated: **16 October 2026**.

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
| 3: computational mechanisms | **Conservative investigation closed; conditional concept v1 complete** | Historical qualification results preserved. New evidence/premise/mechanism package and 128 illustrative scenarios connect an assumed spinal interface to assistance and conditional OFF learning; biological efficacy remains unestablished |
| 4: detailed electronics/firmware | **Complete within the bounded digital reference scope** | Integrated master: 1,298 component positions / 1,296 fitted, 4,781 pin identities, 80 sheets and 258 harness rows. Eight genuinely routed populated native boards, 21,039 trace segments and 2,335 vias; zero ERC/DRC, missing connections, schematic parity issues or ignored checks. Independent electrical integration: 9,540 assertions; populated-board audit: 14,273. Actual carrier-specific ARM firmware, power revision and populated STEP/export evidence |
| 5: populated engineering CAD | Pending | Actual boards/components/package/lead interfaces, native parametric assemblies, dimensions, STEP/STL and nominal fit checks |
| 6: integrated paper/repository release | Pending | Complete digital path verification, final illustrated manuscript, native sources, reproducible release, evidence and learning/defence material |

The historical v1.0.0 release is a subsystem reference. Its one-channel board
and desktop enclosure are not the completed implant requested here. Stage 2's
80 allocation solids and illustrative ports are not populated implant CAD.

## Latest completed engineering package: integrated populated PCB

The [integrated native hierarchy](docs/stage4/integrated-pcb-design.md) now joins
all seven circuits, the actual controller carrier, and four physical observation
tap headers. Source circuits and earlier studies remain frozen. Exactly two old
common-rearm wires are superseded so the common driver rearm and two independent
phase-supervisor rearm outputs stay separate. All 50 external firmware endpoints
and 26 serialized observations are explicitly connected.

The electrical integration, actual copper routing and native PCB checks pass.
The [board index](electronics/stage4/integrated-pcb/BOARD_INDEX.md) opens all eight
native layouts and their populated STEP, top/bottom/isometric views, copper
plots and fabrication-reference bundles. Independent checks compare actual
schematic pins with PCB pads, population flags, hierarchy paths and source-bound
DRC reports. Exactly two optional driver capacitors remain DNP.

This is an eight-board modular digital reference with actual component sizes
and board dimensions. The [layout review](docs/stage4/pcb-layout-review.md)
identifies the selected four-layer stackup and carrier's filled/capped
via-in-pad fabrication requirement. A TPS3431 land-pattern error was corrected
against TI's drawing in the new integrated snapshot. Historical source circuits
remain preserved. Implant miniaturization remains a future design problem.

The additive controller budget retains the previous load contingency and raises
HOST_3V3 to a declared 160 mA cap. Conditional active power/runtime become
**3.154 W / 4.880 h**. These are calculated allocations; converter behavior,
actual consumption and compact implanted thermal performance remain unmeasured.

The BT40F-specific firmware image selects the manufacturer's 11 pF oscillator
load. Its independent ELF/HEX/BIN/source audit passes 83 checks; the image uses
53,648 bytes flash and 98,000 bytes RAM. Original firmware and earlier receipts
remain unchanged. Nothing has been executed on a physical board.

**Next: Stage 5 mechanical assembly and interfaces**, using the populated board
exports as real inputs. Stage 6 then produces the integrated illustrated paper
and final private repository release. Video and website work remain parked.

## Previous completed package: actual nRF5340 firmware

The [C/Zephyr application](firmware/nrf5340/README.md) implements actual SPIM,
UART, GPIO, timer/DPPI cutoff and the shared production policy core. It builds
for nRF5340 application-core silicon; it is separate from the earlier unmodified
hello-world smoke check. The [implementation review](docs/stage4/nrf5340-firmware-design.md),
native pin map, source-bound ARM image, memory map and independent ELF/interface
audit explain exactly what is present. Nothing has been flashed or executed
on a physical board, and no hardware timing measurement is claimed.

The compiled core passes **75 finite scenarios / 713 assertions**. Explicit
pre-monitor recovery, observed monitor permits and subsequent supervisor rearm
avoid startup deadlock. Modes, leases, SBP support freshness, active-address
readback, phase sequencing, OFF trials, sticky fault records and queue overflow
remain distinct. Interruptions do not trigger automatic balancing or restart.

The implemented profile uses tagged 40-clock raw conversions at nominal 100 µs
opportunities and nineteen-word RHD frames at nominal 1 ms opportunities.
Blocking acquisition and sideband reads can cause known gaps; actual timestamps,
validity and counters retain them. This does not implement the earlier 450k raw
or 4k neural schedule. Recording/feature validity describes digital transport,
not analog recovery or a useful biological decoder. The companion owns the
declared learner-specific or pressure policy and supplies explicit event plans.

The full native interface exceeds the MCU's GPIO capacity. The
[46-GPIO map](docs/stage4/nrf5340-pin-map.csv) therefore includes a declared new
four-SN74LVC165A carrier that serializes actual active-route bits and health.
The new integrated carrier now implements that dependency with source-supported
pin ownership, clock sharing and sentinel checks. The seven earlier native
circuits and their studies remain unchanged.

The [integrated populated PCB](electronics/stage4/integrated-pcb/README.md) now
completes that final Stage 4 package. The [exit review](docs/stage4/exit-review.md)
defines the completed digital scope and retained limits. Mechanical packaging
and the final integrated paper remain subsequent work.

## Previous package: monitoring and companion interfaces

The [native interface design](docs/stage4/monitoring-transport-design.md) adds
an ADS8688 raw-monitor ADC, explicit shared-MISO charge endpoint handoff, health
observations and an isolated UART with separate companion power/ground. Its
60 components, 217 pins and eight editable sheets pass full ERC without ignored
checks. The old six native packages and their study results are preserved.

The [finite studies](electronics/stage4/transport-study/README.md) bind actual
apertures, endpoint read arbitration, configuration identities, pressure support
freshness, leases, queues, divider loading and illustrative filter behavior.
The 450k aggregate conversion mismatch is resolved by added hardware. Current
samples average 200 ksps each but have 4.25–6.375 µs gaps; the typical internal
15 kHz bandwidth does not earn precise peaks or the 4% phase-charge target.
Stale/ambiguous packets reject; trusted peer measurements and bounded clocks
remain assumptions. No target DMA implementation, cuff or radio is claimed.

The new [34-wire plan](docs/stage4/monitoring-transport-wiring.csv) joins the
previous 134 wires with separate floating recording and companion grounds.
Processed traffic fits the normal service; continuous 4k raw export exceeds
the explicit 1 Mbaud UART. A 100 ms diagnostic burst fits the saved queue model.
The incremental power overlay revises the conditional active allocation to
**2.800 W / 5.497 h**. Compact thermal qualification remains unearned.

The nRF5340 package now implements a narrower, explicitly described target
profile. The consolidated PCB package is now complete. Stage 5 develops its
mechanical assembly and packaging. The final
integrated illustrated manuscript follows in Stage 6; video and website remain
parked.

## Previous package: power and quantitative budgets

The [native power design](docs/stage4/power-design.md) generates all nine host,
supervisor and isolated recording rails. It adds a protected 2S reference pack,
input protection, actual buck/boost/module/LDO circuits, startup qualification,
reference windows and an open-drain fault connection to the existing terminal
shutdown. The [32 new wires](docs/stage4/power-wiring.csv) join the previous
102-wire plan without bridging the floating recording ground.

The [finite budgets](docs/stage4/power-budget.md) audit actual IC supply pins,
423 capacitors, peak/reservoir/startup/source behavior, losses, runtime, heat,
buses and memory. Independent checks pass 3,300 assertions. The conditional
active allocation is **2.615 W / 5.886 h** at 80% of rated 19.24 Wh energy.
These are declared-load/efficiency calculations, not measurements. Full AFE
regulator corners can reject startup; selected ±0.5% operation is an explicit
trim/characterization assumption. Boost disable leaves diode feedthrough and
stored energy; power fault still consumes arm independently.

The original one-cell/100 mA and compact thermal assumptions are superseded.
The selected pack is 99 g and 67 × 37 × 21 mm; all selected lumped thermal cases
fail the 2 K allocation. The future compact consumer implant needs lower-power
implementation and revised packaging; the reference is not silently shrunk into
the preliminary CAD. Two ADS8866 devices also cannot supply the 450k aggregate
conversion contract, and continuous framed raw data exceed the 1 Mbit/s service.

That checkpoint's ADC-rate mismatch is now resolved by the added transport ADC.
Its continuous raw-link and compact thermal failures remain explicit. The
new package updates resources through an additive overlay, preserving the old
power calculation and its original scope.

## Previous package: independent shutdown and supervision

The [native supervision design](docs/stage4/supervision-design.md) adds 18
body-facing terminal guards, separate phase-duration timers, heartbeat watchdog,
rail/current/differential-voltage observation and 17 physical RHD-side pin
windows. Global/source sticky interlocks require explicit recovery and rearm.
The [102-wire integration plan](docs/stage4/supervision-wiring.csv) connects
actual prior package pins, keeps the recording ground isolated and separates
pre-monitor health from arm-qualified driver permission to avoid a startup loop.

The [finite studies](electronics/stage4/supervision-study/README.md) include
independent native gate/pin audits, fault histories, threshold/loading/RC corners
and seven interrupted artificial-load cases. All 2,961 saved trajectory points
are independently audited. Stored energy, welded-switch witnesses, shared
reference faults and unearned physical timing/leakage bounds remain explicit.
AFE nominal supplies revise to +3.45/+5.30/−5.10 V; the old 100 µs phase gap is
unearned, with an observed-quiet gate and provisional 200 µs allocation replacing
it. Neither this package nor circuit ERC establishes biological efficacy.

The [power package](docs/stage4/power-design.md) now supplies the revised rails
and quantitative budget. Its new reference windows detect selected gross
reference faults without earning the earlier precision allowance.

## Earlier continuation checkpoints

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
  The new measured library admits nominal inverse-model teacher references after
  independent competence/decoder/template checks; faster references reject.
  A separate 16-capture revision evaluates the source at actual contact
  apertures. Older retained-learning studies keep their original identities.
- **Response domain:** 24 fixed-profile studies with 432 independently recorded
  checks in each held-out context. Conditional nominal maps admit 63/72
  same-context and 34/72 changed-context cases. Actual, null and adverse maps
  reject. Finite resting checks do not grant dynamic or unseen-context authority.
- **Cue policy:** observed forecasts, whole-frame planning, cancellation,
  expiration and causal residual detection. Eight component replays retain
  actual authority rejection and failed assisted forecast qualification. They
  do not establish coupled motor control or retained-learning benefit.
- **Moving-source revision:** 75 captures and six independent reference-grid
  comparisons. Holding a moving source for 5 ms fails selected feature and
  prediction allocations; new neural captures use actual contact apertures.
  Dense stimulation still removes neural qualification. An ambiguous field
  preserves identical features despite conflicting observed positions.
- **Intervention-aware observer:** 31 causal horizons and eight complete withheld
  recordings. Quarter/half-density and selected known-cue contexts pass their
  finite forecast allocations; full density, faster cadence, changed response
  and unannounced sensor offset fail. These are predetermined command recordings,
  with no feedback-policy admission or retained-learning claim.
- **Precision requirements:** four fresh observed calibrations, 144 requirement
  rows and 24 thresholds. A prospective 4% monitor leaves scalar room for
  single-route corrections with an 8 mm forecast input. That predictor target,
  circuit capability and dynamic response still require evidence.
- **Finite-frame response:** two integration grids each generate 24 isolated
  calibration pulses and 12 withheld trajectories through the actual electrical
  adapter. Current-monitor domains reject; explicitly proposed future intervals
  admit six isolated single/paired response domains and reject all repeating,
  changed-context and fault domains. These are component gates, not controller
  admission.
- **Zero-future baseline:** a new twelve-second unassisted calibration and
  independent full recordings test 26 execution horizons. Fresh unassisted
  prediction passes at a maximum 9.781 mm allocation. Every assisted past-response
  context fails 15 mm after full uncertainty propagation. Old effects beyond
  the measured 600 ms window reject explicitly instead of being discarded.
- **Connected reset-trial pilot:** 32 matched arm/family/delivery runs consume
  independently bounded teacher references, dynamic response and timed residual
  supervision. Sixteen independent learner-drift recordings make every aggregate
  forecast horizon fail the unchanged 15 mm allocation. All 128 practice trials
  withhold stimulation; all 64 OFF assessments remain pulse-free and show no
  assisted-arm advantage. The saved experiment therefore does not demonstrate
  delivered assistance or retained learning.
- **Runtime evidence scope:** a qualified baseline now also requires the tested
  physical support range and exact observed past pulse pattern. A shifted-history
  regression rejects. Existing fitted values and qualification decisions remain
  unchanged; a context name alone cannot grant authority.
- **Observed-state confirmation:** one independently reviewed persistent observer
  uses measured calibration and a declared 60 ms synthetic movement prior.
  [The standalone study](experiments/stage3/observed-state-observer/README.md)
  preserves development data separately from 16 fresh sensor-noise pairs on two
  body grids. All 32 captures cover all 550 supports and 26 horizons; maximum
  observed error plus the unchanged 3 mm label allocation is **11.354 mm**, below
  15 mm. All 915,200 confirmation residuals were independently audited. This is
  sensor-noise independence within the same subject/model domain, not biological
  validation. It uses no spinal input, delivers no dose and does not replace the
  failed pilot. Persistent history, calibration and desktop memory costs are
  explicit. Pre-dose integration is verified separately below; a stimulated
  voluntary-state estimate remains unqualified.
- **Final bounded replay:** the [pre-dose freeze study](experiments/stage3/frozen-observer-pilot/README.md)
  completed 32 one-practice trials and 64 hard-OFF assessments. All 32 observers
  seal their 26-target vectors; 32 pre-launch diagnostics and 1,600 delayed guard
  comparisons pass. All 192 tested nonzero candidates reject actual response
  qualification, learning-interaction qualification and the 25 mm correction
  bound. All arms remain identical, with zero launches and no retained advantage.
  Fifteen software contract probes and full same-cohort reproduction pass.
  Independent raw recomputation checks all 57,600 measurements and complete
  interval arithmetic. This replay implements no active delivery path and
  supplies no new post-dose monitoring/cancellation evidence.
- **Technical report:** an eight-page [illustrated mechanism revision](output/pdf/ATO_stage3_mechanism_revision.pdf)
  presents the selected new findings and their design consequences.
- **Native electronics:** the [first monitoring schematic](electronics/stage4/monitoring-cell/README.md)
  exports and passes all 245 manifest/netlist pin checks with no ERC violations
  or ignored checks. Its proposed phase-charge precision is unqualified. Sensor
  power exceeds the prior allocation, and input-bias bypass, ADC protection and
  analog settling/window errors remain concrete design tasks.
- **Package correction:** all five amplifiers now use the production OPA391DCKR,
  with its different pin mapping checked in native exports. The previous DBV
  choice was preview information. Functional topology remains unchanged; the
  generic SC-70 land pattern still needs PCB assembly review.
- **Independent circuit study:** [33 behavioral transient runs](electronics/stage4/monitoring-study/README.md)
  cover both sources on three grids and retain 462 phase/gap/tail/net intervals.
  Separate KCL and matrix-exponential checks confirm the stated model. A 45 µA
  load-side bias bypasses 9 nC over 200 µs; near-zero final charge conceals
  oversized opposed phases. Reset, settling, component and clipping witnesses
  remain explicit. This first model does not earn 4% accuracy, implement shutdown
  or complete the broader waveform/load/rail coverage required by Stage 4.
- **Restricted driver boundary:** the [reviewed design investigation](docs/stage4/current-driver-design.md)
  specifies two current sinks, polarity bridges, servo resets and independent
  phase timers, initially at 24 V/3 mA/200 µs. Its
  [native five-sheet implementation](electronics/stage4/current-driver/README.md)
  and finite circuit/control studies are now complete within their stated scopes;
  full routing, supervision, power and recording integration remain pending.
  Servo power exceeds the earlier allocation; bias-current paths, terminal
  isolation, actual transient charge and shutdown tails remain open.

The full local suite passed **224 tests** on 12 October. Seven added regression
checks cover portable reproduction of a negligible reference-grid argmax without
relaxing numerical allocations or qualification decisions. The preserved foundation
batch was reproduced under its unchanged defaults.
The [test receipt](provenance/stage3-test-run.json),
[foundation receipt](provenance/stage3-verification.json),
[continuation receipt](provenance/stage3-continuation-verification.json) and Git
manifest identify their scopes and actual artifacts. Automated checks are
evidence for their stated digital models, not proof of biological efficacy.

## Current limiting findings

The monitor's approximately 44.1% nominal-charge uncertainty leaves actual motor
authority negative. Nominal reactive timing exceeds its 100 ms prediction cap.
The original known-cue alternative and historical pilot drift checks fail.
The new persistent observer resolves its selected no-dose forecast arithmetic;
its connected freeze, guards and OFF replay now pass. Actual action domains,
learning-enabled response interaction and the combined correction interval
still reject every nonzero candidate. Continuous/repeated assistance, active
monitoring and retained benefit remain unqualified.
Those failures set redesign requirements; they are not hidden by a
desired learning multiplier or favorable biological tuning.

The pressure branch has identified conditional pressor feedback, faults and
finite stop/hold/ramp responses. It uses external pressure because its dense
stimulation does not qualify continuous neural recording. It does not claim
universal autonomic control or healthy-consumer efficacy.

## Next move

Stage 4 is closed within the [digital exit scope](docs/stage4/exit-review.md).
The [board index](electronics/stage4/integrated-pcb/BOARD_INDEX.md) supplies actual
populated geometry, native circuits, wiring and exports for Stage 5. Next build
the coherent native mechanical assembly and package/lead interfaces, with
dimensions, drawings and nominal fit checks. The reference boards retain their
actual large sizes; a compact future implant remains a separately identified
design problem. Existing allocation solids are preliminary inputs.

Both expert-informed retained learning and function-specific physiological
regulation remain central. Stage 3's conditional concept is the future-interface
baseline; its conservative negative results are preserved. Mechanical appearance
must not relabel those results or the unearned analog/thermal/timing limits.

Stage 6 then integrates the illustrated manuscript, technical explanation,
learning/defence material and verified private repository release. Video and
website work remain parked. The available free KiCad/FreeCAD/Blender toolchain
already supports the next digital work; no new paid tool is required.

Working branch: `overhaul/full-scci-system`.
Private [draft review](https://github.com/pratham-cloud-ctrl/Project-ATO/pull/1).
Original synced ChatGPT project sources remain read-only.

# Proposed first native current-driver design boundary

**12 October 2026. Reviewed design proposal; native implementation pending. Digital artificial-load work only.**

This design handoff defines a proposed native circuit boundary, not a completed schematic, new evidence gate,
implant circuit qualification, or change to the frozen Stage 2/3 contracts.
The existing monitoring cell and 33-case monitoring study remain unchanged.

## Recommendation and boundary

Build one new native KiCad package containing **two independently regulated
low-side current sinks, two four-switch polarity bridges, a shared dual DAC,
servo reset/gate clamps, and a separate non-retriggerable phase-permission timer
per source**. Connect it to the existing signed return-current monitoring cell
through explicit ports. The first admitted design study is **24 V, 3 mA,
200 microseconds per nominal phase**, with the existing 100 microsecond gap and
250 microsecond zero-current/reconfiguration admission. Ideal phase charge is
600 nC. Actual charge includes the bridge edges, settling and tails.

Use **TMUX7212PWR** for this restricted bridge, not a generic motor driver.
This part cannot implement the 48 V end of the architecture. Broadening the
range remains a distinct design revision. The proposed first slice does not
earn the monitoring study's proposed 4% precision allocation, the 10 microC
delivered-phase limit, or biological selectivity.

The preserved architecture still calls for two sources, 16 selected contacts
and two dedicated returns; 0.1–20 mA; 50–500 microseconds; command charge at most
9 microC and delivered phase charge at most 10 microC; 16/24/36/48 V rail choices
with 8 V reserved headroom and at most 40 V usable terminal voltage. These
limits are jointly admitted, not independently available knob maxima. The
16-contact router, terminal isolation, boost converters, recording front end,
compliance-voltage measurement, watchdog and final PCB are **outside this next
native boundary**. Their ports must be labeled external and unqualified.

## Actual current path

Repeat this cell separately for sources 0 and 1; do not share their feedback
resistors, sink transistors, bridge-control permission or dedicated returns.

```text
              SW1                              SW2
VH_24 --------/ -------- A_BR          B_BR ------/ -------- VH_24
                         |              |
                     route/load A  load B--2 ohm Kelvin return shunt
                         |              |
                        SW3            SW4
                         |              |
                         +------ D -----+
                                |
                          BSP89 current sink
                                |
                         S -- 100 ohm -- GND
                         |     Kelvin
                    servo feedback

Phase +: SW1 and SW4 closed; Phase -: SW2 and SW3 closed.
All four open for gap, recovery, invalid direction or inhibited permission.
INA241 senses B_LOAD minus B_BR across the independent 2 ohm shunt.
```

The diagram's two load terminals are joined through the selected artificial
pair load; the upper A node goes through the future contact router. The B shunt
is in series with the dedicated return in **both** polarities. It must not be
moved into the ground feedback leg: the latter observes unsigned sink current,
and is neither the independent signed monitor nor a complete load-current
measurement.

The bridge's lower switches can sit at a substantial positive voltage while
the sink dissipates compliance headroom. A grounded motor gate-driver source
sense pin therefore cannot simply be attached there. Passive analog switches
avoid that particular floating gate-driver problem.

## Initial parts, packages and pin contracts

Manufacturer material was checked on 12 October 2026. A catalog part or
automotive grade does not imply chronic implant suitability.

| Function | Proposed part and native contract |
|---|---|
| Dual setpoint | **DAC80502DRXR**, WSON-10. Pins 1 VDD=5 V, 2 VOUTA, 3 RSTSEL=GND, 4 AGND, 5 SPI2C=GND, 6 SCLK, 7 SYNC, 8 SDIN, 9 VOUTB, 10 VREFIO; proposed exposed-pad ground and land require the package-drawing review. Preload via SPIM1 while inhibited. |
| Servo, one per source | **OPA192IDBVR**, SOT-23-5: 1 OUT, 2 V−=GND, 3 IN+=DAC setpoint, 4 IN−=selected feedback, 5 V+=15 V. |
| Linear sink | **BSP89H6327XTSA1**, PG-SOT223: 1 gate, 2 drain, 3 source, 4 drain tab. Drain to D; source to 100 ohm Kelvin resistor. Keep both drain pads on the same net. |
| Polarity bridge, one per source | **TMUX7212PWR**, TSSOP-16. 1 SEL1, 2 D1=A_BR, 3 S1=VH, 4 VSS=GND, 5 GND, 6 S4=D, 7 D4=B_BR, 8 SEL4, 9 SEL3, 10 D3=A_BR, 11 S3=D, 12 NC, 13 VDD=VH_24, 14 S2=VH, 15 D2=B_BR, 16 SEL2. **This differs from TMUX8212's pin map.** |
| Gate and feedback reset, two per source | **TMUX6219DGKR**, VSSOP-8: 1 D, 2 S1, 3 GND, 4 VDD=15 V, 5 EN held high in the qualified 15 V domain, 6 SEL=RUN, 7 VSS=GND, 8 S2. Gate mux: D to sink gate through nominal 330 ohm, S1=GND, S2=servo OUT. Feedback mux: D to servo IN−, S1=servo OUT, S2=Kelvin S. |
| Independent phase window | **LTC6993HS6-1#TRPBF**, TSOT-23-6: 1 TRIG, 2 GND, 3 SET, 4 DIV, 5 V+=3.3 V, 6 OUT. One per source; fixed external timing resistors, no software-programmable extension. |
| Permission/latches | Continue the existing monitor's **SN74LVC1G74DCUR** and **SN74LVC1G11DBVR** conventions; additional gates/inverters implement the explicit equations below. Recheck each selected package's pin table independently at schematic generation. Do not silently reuse a different package's numbering. |

The DAC supports zero/midscale selection at reset; gain also requires explicit
configuration. Set **buffer gain 1 and reference divider 1:1** before admitting
output, because reset's GAIN register selects buffer gain 2. Maximum offset
is ±1.5 mV and gain error ±0.1% FSR under the electrical-table conditions;
5 microsecond settling is typical. Zero code is not a physical disconnect.
[TI DAC80502 Rev A, pin/electrical/register tables](https://www.ti.com/lit/ds/symlink/dac80502.pdf)

OPA192 operates from 4.5–36 V; 10 MHz GBW is typical. Offset is specified up to
±25 microV at 25 C and ±75 microV across temperature for the relevant lower
common-mode range. Quiescent current is 1 mA typical, 1.5 mA full-temperature
maximum. A 15 V auxiliary rail leaves room for feedback voltage plus a 10 V
gate drive; a 5 V servo rail would not guarantee that drive at 20 mA.
[TI OPA192 Rev E](https://www.ti.com/lit/ds/symlink/opa192.pdf)

BSP89 is an enhancement device rated 240 V VDS and ±20 V VGS. Its resistance
maxima are 7.5 ohm at 4.5 V and 6 ohm at 10 V under the stated 25 C tests.
Those switching specifications do not establish precision linear-loop
behavior. The datasheet includes single-pulse SOA and transient thermal curves;
repetition and PCB cooling must be analyzed separately.
[Infineon BSP89 Rev 2.2, pp.1–4](https://www.infineon.com/assets/row/public/documents/24/49/infineon-bsp89-datasheet-en.pdf)

TMUX7212 is active-high, has weak logic pull-downs, and supports 4.5–44 V
single-supply operation. Its 44 V table gives 44 microA typical/105 microA
maximum supply current; 104 pC injection is typical. Resistance and timing
tables have particular 12/44 V test conditions; 36 V plots are typical, and
no 24 V worst-case bound is inferred here. Use **10 ohm per switch as an
initial simulation stress assumption**, not a datasheet maximum at 24 V.
Analog pins are rail-clamped; logic fail-safe protection does not provide
power-off load isolation. Independent SPST paths have no general diagonal
break-before-make guarantee. [TI TMUX7212 Rev D, pin table, sections 6/8](https://www.ti.com/lit/ds/symlink/tmux7212.pdf)

TMUX6219 uses 4.5–36 V supplies and accepts 3.3 V select logic at a 15 V rail.
With EN high, SEL low chooses S1 and SEL high chooses S2. Use this explicit
grounded gate/default feedback state, rather than disabling EN and leaving the
gate floating. Its own commutation, leakage and rail-off behavior still need
the circuit test. [TI TMUX6219 Rev E](https://www.ti.com/lit/ds/symlink/tmux6219.pdf)

## Regulation, setpoint and anti-windup

For a settled ideal active loop:

```text
I_sink = VSET / R_FB; R_FB = 100 ohm nominal
VSET = code × 2.5 V / 65536; buffer gain=1, reference divider=1
one DAC LSB = 0.381469 microA of nominal sink current
100 microA: code262 → 99.9451 microA
3 mA: code7864 → 2.999878 mA
20 mA ceiling: floor to code52428 → 19.999695 mA before errors
```

Use a specifically selected 100 ohm, 0.1% or better low-temperature-coefficient
feedback resistor with Kelvin connections; this tolerance is a procurement
requirement, not an already selected component. The 0.1% scale alone produces
about 0.6 nC per 600 nC phase. DAC's ±1.5 mV offset becomes ±15 microA through
100 ohm: 15% at the 100 microA lower envelope, 0.5% at 3 mA. Thus bit depth
does not earn lower-range accuracy. Calibrate both channels and independently
observe their delivered waveforms; shared reference/DAC faults remain correlated.

When inhibited, the gate mux grounds the sink gate and the feedback mux closes
local unity feedback around the opamp. Its output follows VSET rather than
integrating an open-circuit current error up to the rail. RUN switches both
paths into the active loop. Maintain a passive gate-to-ground pull-down for
loss of the 15 V supply. A nominal 330 ohm gate resistor and an explicitly
versioned compensation footprint are starting components; do not invent a
stable bandwidth from the amplifier GBW. Feedback/gate switching skew, mux
injection, MOS capacitance, startup and overload recovery require closed-loop
transient investigation. The resistor limits a nominal 15 V gate-clamp
discharge to about 45.5 mA initially; this still needs the mux's temperature,
supply, current and repetition checks. A gate clamp alone with an open-loop amplifier is
**not** sufficient anti-windup.

Keep gate and feedback mux delays independent in the model. If feedback
reaches the sense node 200 ns before the gate is released, a 0.3 V error can
drive a substantial amplifier excursion; the 20 V/microsecond typical slew
rate would permit an illustrative 4 V rise in that interval. This is a fault
witness, not a guaranteed overshoot prediction. Also test feedback mux stuck
in its active position: a successful off-gate clamp can conceal amplifier
windup until the next release.

## Independent permission and interruption

The request must never bypass monitor permission. For each source:

```text
VALID_DIR = PHASE_PLUS XOR PHASE_MINUS
GOOD = MON_PERMIT & EXT_SUP_OK & ROUTE_LOCKED & RESET_READY
       & RAILS_QUALIFIED & VALID_DIR & !TIMEOUT_LATCH
RUN = PHASE_REQUEST & TIMER_OUT & GOOD
SEL1 = SEL4 = RUN & PHASE_PLUS
SEL2 = SEL3 = RUN & PHASE_MINUS
```

Explicit all-off states separate opposite diagonals. Route/direction are
preloaded and locked while inhibited. All switches' external pull-downs and
logic outputs must produce low at startup. Verify logic at supply rise/fall,
not just normal Boolean truth. Independent external supervision is a real
required input; tying it high is only a labeled test fixture condition.

LTC6993-1 is rising-edge **non-retriggerable**, unlike -2. Set NDIV=64,
RSET=175.8 kohm (0.1% design requirement), DIVCODE=2, positive OUT. The
manufacturer's suggested divider is 976 kohm top/182 kohm bottom. Timer
full-temperature error for this divider is ±4.4%, not the ±3.4% room-temperature
headline. [ADI LTC6993 Rev F, pp.4/13–15](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc6993-6993-1-6993-2-6993-3-6993-4.pdf)

```text
t_nom = 64 ×175.8k/50k ×1 microsecond =225.024 microseconds
t_min =225.024×(1−0.044)×(1−0.001) =214.907821 microseconds
t_max =225.024×(1+0.044)×(1+0.001) =235.159981 microseconds
```

These are timer-output bounds only, before extra resistor drift, logic delay,
transistor/switch tail and output-load behavior. Startup for the chosen
resistor is not established by the headline minimum startup number: the
manufacturer's typical 500-times-master-period rule gives approximately
1.758 ms here, not 500 microseconds. A typical time is not a ready deadline. Hold the
whole circuit inhibited until timer/rail readiness has been qualified.
TRIG receives the prequalified PHASE_REQUEST edge, not RUN (which would create
a circular enable dependency). A new request edge after timer readiness is
required; a request held high through startup does not create a fresh trigger.

Timer OUT gates RUN directly. A separate timeout latch clocks on the rising
edge of **NOT TIMER_OUT**, with D=TIMEOUT_LATCH OR PHASE_REQUEST: if the request is still asserted
when its timer ends, the latch records timeout. Explicit rearm clears it only
in the observed quiescent state. The feedback OR makes this sticky; D equal
to PHASE_REQUEST alone would allow a later normal pulse to clear it.
A normal request has already ended before the
timer falls. Analyze timer/request coincidence and the DFF setup/hold aperture:
the direct timer gate shuts output even if timeout classification is ambiguous.
Also reject inconsistent timer/request history. Non-retriggerability by itself
prevents extension during an active window; it does not prevent a new pulse
after that window. Sticky permission, monitored quiescence and route ownership
must block uncontrolled restart.

MON_PERMIT's existing asynchronous current-window latch removes RUN immediately
through hardware logic. Fault also grounds the sink gate and opens all four
commanded bridge paths. No software make-up phase, balancing pulse or automatic
retry follows. Preserve independently measured phase charges, interruption
time, clipping and **unknown residual charge**. The hardware emergency always
takes precedence over completing an apparently balancing phase.

## Charge and common-mode paths that the loop cannot certify

Let signed Iload flow A→B_LOAD and Ishunt flow B_LOAD→B_BR. For bias current
bL flowing from the load-side INA241 input to its supply/ground, the simple
steady-node KCL is:

```text
Iload − Ishunt = bL
integral(Iload−Ishunt) dt = 45 microA ×200 microseconds =9 nC
```

45 microA is a **conditional bias example**, not a maximum PVT bound. The
existing monitor study already shows this exceeds its 3 nC bypass allocation.
The driver's low-side feedback does not remove it. With the positive diagonal,
a driver-side bias sink bD can make Ishunt≈Isink+bD and Iload≈Isink+bD+bL.
With the opposite diagonal the driver-side bias can instead be supplied by
the upper branch. The real driver study must solve both polarities, supply
returns and common-mode-dependent bias, not label every driver-side bias as
harmless because the earlier artificial-current fixture held Iload fixed.
[INA241 primary electrical/pin documentation](https://www.ti.com/lit/ds/symlink/ina241a.pdf)

Rail-to-terminal capacitance can receive a common-mode step outside the
100 ohm feedback path. Pure bookkeeping gives Q=C×deltaV: **1 nF×24 V=24 nC**,
the whole nominal 4% allowance. The 100 microA/50 microsecond envelope minimum
is only 5 nC; **208.3 pF×24 V** is already that much charge. These are
counterexamples, not measured parasitic values. Include switch/package,
protection, monitor, lead and fixture capacitances and observe the entire
connection interval.

Closing both upper switches, or both lower switches, can recirculate/discharge
differential load capacitance through the bridge without traversing the sink
feedback resistor. A shorted switch is not repaired by valid control logic.
All-off analog switches still have rail clamps; rail collapse can forward-bias
them. A future back-to-back disconnection boundary must include the monitor
input paths or explicitly retain their load current. Neither all-off logic nor
grounding the sink gate constitutes fail-open terminal isolation.

There is a separate delivered-charge protection gap: **25 mA×500 microseconds
=12.5 microC**, above 10 microC. Even the Stage 2 command ceiling disallows
20 mA×500 microseconds=10 microC. A real delivered-phase charge guard needs its
own threshold, observation uncertainty, shutdown delay and worst-case tail
margin; signed opposite-phase cancellation must not conceal an excessive
individual phase. A profile-specific current×time restriction may limit a
named test but cannot replace that full-envelope guard. This slice does not
claim that either route has already closed the protection requirement.

## Compliance, supply and power constraints

Admit a load only if both its terminal requirement and the driver headroom fit:

```text
|I| Rpair + |Vpolarization| <= VH −8 V, and <=40 V
VH >= terminal requirement + I(100 ohm +2 ohm +2 R_ON)
      + VDS_required_by_current_loop + other series losses/droop
```

The second line must reconcile actual losses with the **existing** 8 V reserve;
do not double-count that reserve as an extra available voltage. For the initial
3 mA, 200 microsecond test, the largest chosen pair R=2 kohm needs 6 V resistive
drop; 600 nC on 0.5 microF adds 1.2 V, with 1 V initial stress gives 8.2 V.
This fits the nominal 16 V usable voltage from a 24 V rail, before checking
actual polarity/initial-state trajectories and all analog limits. At 20 mA,
R=2 kohm already needs 40 V resistive drop: adding the 4 V polarization
allocation violates 40 V usable. It must be rejected rather than called
regulated under every load.

Provide external qualified **24 V, 15 V, 5 V and 3.3 V** ports for this native
slice. Existing boost design has not generated/validated the 15 V auxiliary
rail. Reference ground is a circuit node, not a qualified chronic body return.

Two OPA192s at 15 V consume **30 mW typical/45 mW full-temperature maximum**
before output charging. This alone exceeds Stage 2's 8 mW driver-quiescent
allocation. Reusing the TMUX7212 44 V current values for a *provisional 24 V
budget stress* gives 2.112 mW typical/5.04 mW maximum arithmetic for two bridges;
this is not a guaranteed 24 V consumption bound. Four gate/feedback muxes,
DAC, logic, timers, rail conversion and leakage are additional. At 3 mA the
sink can dissipate up to approximately 72 mW during a phase; at 20 mA/48 V the
conservative product is 0.96 W, or 0.48 mJ per 500 microsecond pulse. Neither
single-pulse energy nor a catalog power rating closes repetitive SOA/thermal
design.

**OPA191IDBVR** is the concrete lower-power servo alternative: 140 microA
typical/250 microA full-temperature maximum, 2.5 MHz typical GBW in its higher
supply table. Two at 15 V give 4.2/7.5 mW arithmetic. It must earn its own
loop stability, edge/tail and overload bounds before replacing OPA192; lower
IQ is not proof of equivalent pulse accuracy. [TI OPA191 Rev D](https://www.ti.com/lit/ds/symlink/opa191.pdf)

For sink-short fault, a 24 V rail and a 500 ohm pair plus 102 ohm feedback/shunt
give roughly 39.9 mA before switch losses; a shorted pair could allow roughly
235 mA. The current guard is reactive and may see clipped history. Bound the
actual fault area and device stress; do not interpret its 25 mA threshold as
a guaranteed never-exceeded current ceiling. Even the proposed short phase
guard cannot independently bound fault charge without a separate current
bound: a sink short bypasses regulation, and reference/feedback faults can
command much greater than 3 mA. The required bound has the form Imax times
(maximum timer window plus shutdown and tail) plus bounded bypass/injection,
with every term justified separately.

## Alternatives rejected for this first boundary

The 100 V **TMUX8212** could support higher signal voltages but its flat
resistance region stops about 5 V below VDD; sharing its VDD with the upper
bridge rail invalidates a 5 ohm assumption. Separate headroom supply and
350 microA typical/900 microA full-temperature maximum supply current are
material costs, and injection is −1.3 nC typical. It is an alternative to
investigate, not an interchangeable upgrade. [TI TMUX8212 Rev B](https://www.ti.com/lit/ds/symlink/tmux8212.pdf)

A discrete PMOS high side avoids that rail-edge issue but needs source-referenced
DC gate drive, clamp and leakage bounds. A simple 10 kohm pull-up plus 6.8 kohm
level shift with a nominal 10 V clamp draws approximately 5.6 mA/0.27 W while
on at 48 V and has unearned turn-off tails. Generic bootstrap motor drivers,
an unconstrained depletion sink, and the 45 V-operating DRV8701 do not resolve
this design. [TI DRV8701 operating/absolute limits](https://www.ti.com/lit/ds/symlink/drv8701.pdf)

## What completes the next native slice

1. Editable top sheet plus two source sheets; local checked symbols and explicit
   power/MCU/monitor/router/supervisor/artificial-load ports. Independently verify
   every package pin, default selection and connection. Export netlist/PDF/SVG,
   inspect all sheets and report ERC without silently suppressing failures.
2. A closed-loop transient model derived from that netlist, with independent
   load KCL/charge oracle. Two refined grids; both source polarities and
   concurrency; R=500/1000/2000 ohm, C=0.5/2/10 microF and initial ±1 V.
   Include servo/switch skew, finite device response, supply/common-mode
   transients, and measured phase/tail intervals. Typical/macromodel responses
   remain conditional evidence.
3. Keep counterexamples: load-side versus driver-side bias, unequal opposed
   phases, switching charge/common-mode capacitance, sink/shunt/open/short
   faults, one stuck bridge switch, invalid diagonals, DAC full-scale/reset,
   timer repeat/stuck-request, clipping and each rail's partial power loss.
   No false successful report may result from an unobserved or clipped waveform.
4. Quantify gate-inhibit-to-load-current and charge-area behavior. Test the
   independent current-window and timer path with firmware request held high;
   verify a second source cannot rearm the faulted one. Retain interrupted
   residuals, and reject rather than automatically rebalance.
5. Reconcile measured/model energy and required auxiliary rails with the full
   system budget in a separately versioned revision. Close the bias return,
   terminal disconnect, delivered-charge guard and compliance supervision
   before expanding to the full envelope or any implant-facing interpretation.

Completion here means an inspectable current-driver/shutdown circuit slice
and an honest evidence report. It does not mean the complete SCCI board, a
qualified implant, accelerated retained learning or autonomous body control.

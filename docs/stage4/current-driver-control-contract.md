# Current-driver phase permission and interruption contract

**13 October 2026. Digital artificial-load circuit slice; conditional logic contract.**

This contract connects the [current-driver proposal](current-driver-design.md) to its native two-source
implementation and behavioural study. It specifies a finite phase-admission circuit; it does not require
the biological assumptions of the [conditional SCCI concept](../stage3/conditional-concept.md) to have
been demonstrated. Each source has its own timer, consumed-admission latch, timeout latch and captured
direction. Shared DAC/reference/rails and external supervision remain common-cause boundaries.
The explicit latch equations here supersede the proposal's simpler `RUN` equation for this slice;
the earlier equation alone does not prevent reopening after an interrupted request or permission recovery.

The design deliberately distinguishes **normal phase completion**, **timeout**, and **loss of permission**.
A normal short request consumes one admission without becoming a timeout. Any interruption blocks
automatic resumption. Clearing the driver latches requires a separate explicit, quiescent rearm.

## Exact port meanings

All logic is referenced to the qualified 3.3 V logic supply; `1` means an asserted high level except for
signals explicitly beginning with `N_`. Inputs require defined pulls and valid logic transitions.

| Port, independently repeated for each source where applicable | Required meaning |
|---|---|
| `REQUEST` | Raw single-phase request. Its physical rising edge triggers the timer. It is not produced by ANDing the request with returning readiness. |
| `PHASE_PLUS`, `PHASE_MINUS` | Exactly one high before safe rearm; stable through that phase. Safe rearm captures the direction; captured direction, rather than these live pins, selects the diagonal. |
| `REARM` | An explicit pulse from the external sequencer after the conditions below have been observed. Return it low before any request. Holding it high is outside the admitted contract. |
| `MON_PERMIT` | Independent current-monitor permission. A monitor fault must remain latched by its own circuit until separately qualified; driver rearm cannot clear that fault. |
| `EXT_SUP_OK` | External supervisory permission. Its implementation is outside this slice; a fixture tie-high is an explicit assumption. |
| `ROUTE_LOCKED` | External ownership of the already selected contacts/return. It is not a hardware router or proof that the route is correct. |
| `RESET_READY` | Low through power-up, timer readiness and any reset/brownout; high only after externally qualified startup. It is not the MCU's uncontrolled power-on GPIO value. |
| `RAILS_QUALIFIED` | All required rails observed within their admitted operating range. Deassert before logic becomes invalid; this supervisor is an external requirement. |
| `QUIESCENT_OK` | Independently observed current quiescence, settled monitor history, allowed route/configuration state and readiness for a new phase. A Boolean fixture does not establish those measurements. |
| `TIMER_OUT` | Positive pulse from the dedicated LTC6993-1. This signal gates output directly. It is not a software estimate of elapsed time. |

The external sequencer holds `REQUEST=0`, `REARM=0` and `RESET_READY=0` at startup. After qualified
readiness, it sets the direction and route, observes quiescence, supplies one rearm pulse, returns rearm
low, waits the required logic-settling/recovery margin and only then raises request. Preload and configure
the DAC while inhibited. At every polarity change, preserve an all-off gap; route reconfiguration has its
own stronger zero-current admission. These external requirements are not silently credited as circuits
already implemented in the driver slice.

## Boolean and state equations

`&`, `|`, `!` and `XOR` denote AND, OR, NOT and exclusive OR. Stable-state equations are:

```text
VALID_DIR  = PHASE_PLUS XOR PHASE_MINUS
BASE_GOOD  = MON_PERMIT & EXT_SUP_OK & ROUTE_LOCKED
             & RESET_READY & RAILS_QUALIFIED & VALID_DIR
SAFE_REARM = REARM & BASE_GOOD & !REQUEST & !TIMER_OUT & QUIESCENT_OK

N_BLOCK_PRE = BASE_GOOD & !(TIMER_OUT & !REQUEST)
N_REARM_CLR = !SAFE_REARM

BLOCK latch:
  asynchronous preset when N_BLOCK_PRE=0 -> BLOCK=1
  asynchronous clear  when N_REARM_CLR=0 -> BLOCK=0
  D=0, CLK=0; otherwise retain BLOCK

TIMEOUT latch:
  CLK = !TIMER_OUT
  D   = TIMEOUT | REQUEST
  N_PRE=1, N_CLR=N_REARM_CLR
  on rising CLK (falling TIMER_OUT): TIMEOUT := TIMEOUT | REQUEST

Direction register:
  CLK=SAFE_REARM, D=PHASE_PLUS, N_PRE=1, N_CLR=RESET_READY
  on rising SAFE_REARM: LATCHED_PLUS := PHASE_PLUS
  LATCHED_MINUS = !LATCHED_PLUS

RUN = REQUEST & TIMER_OUT & BASE_GOOD & !BLOCK & !TIMEOUT
SEL1 = SEL4 = RUN & LATCHED_PLUS
SEL2 = SEL3 = RUN & LATCHED_MINUS
```

`BASE_GOOD` excludes `BLOCK` and `TIMEOUT`. Including timeout in the rearm predicate would make a
timeout impossible to clear. The two active-low asynchronous inputs of the block latch are never both
asserted in the admitted stable-state truth table: safe rearm requires `BASE_GOOD=1` and timer low,
which makes `N_BLOCK_PRE=1`. The physical circuit still needs timing analysis to exclude transient
overlap; a Boolean identity is not a proof about gate skew.

`BLOCK=1` means that admission has been consumed or permission was lost. It is not, by itself, a
timeout diagnosis. Normal request termination while the timer is still high sets block and therefore
prevents a second request from reopening the same timer window. A supervision/monitor/rail/reset/
route/invalid-direction drop also sets block; recovery of that input does not clear it.

Connect raw `REQUEST` to the timer trigger. An invalid request may start an internal timer interval,
but cannot acquire output permission; it leaves the circuit blocked. This avoids a false timer edge
when readiness changes from low to high while a request is already high. Direction capture occurs
only at safe rearm, when request and timer are both low. Release rearm and let that state settle
before the next request; this avoids relying on an unproved ordering between direction-register
propagation and timer-output rise from one shared request edge. A valid live direction swap without
a new safe rearm does not commutate the captured bridge direction; it violates the held-input contract
and is not independently diagnosed by XOR. The slice therefore earns captured-direction stability,
not complete command-consistency detection.

## Concrete parts and active levels

Use local checked symbols, not a generic gate with unchecked package numbering. All logic parts below
operate from the qualified 3.3 V supply with local decoupling.

| Part and selected package | Pins and role | Primary reference |
|---|---|---|
| `SN74LVC1G74DCUR`, DCU VSSOP-8 | 1 CLK, 2 D, 3 inverted Q, 4 GND, 5 Q, 6 active-low CLR, 7 active-low PRE, 8 VCC. Separate devices implement block, timeout and direction. Low PRE sets Q; low CLR clears Q. Do not swap Q5 and inverted-Q3. | [TI Rev G, sections 5/6/8](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf) |
| `SN74LVC1G11DBVR`, DBV SOT-23-6 | 1 A, 2 GND, 3 B, 4 Y, 5 VCC, 6 C; three-input AND. Cascade to form the qualification/rearm/run products. | [TI Rev I, pin table](https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf) |
| `SN74LVC1G08DBVR`, DBV SOT-23-5 | 1 A, 2 B, 3 GND, 4 Y, 5 VCC; two-input AND. | [TI Rev AA, pin table](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf) |
| `SN74LVC1G32DBVR`, DBV SOT-23-5 | 1 A, 2 B, 3 GND, 4 Y, 5 VCC; OR for sticky timeout feedback. | [TI Rev W, pin table](https://www.ti.com/lit/ds/symlink/sn74lvc1g32.pdf) |
| `SN74LVC1G04DBVR`, DBV SOT-23-5 | 1 NC, 2 A, 3 GND, 4 Y, 5 VCC; inversion. Pin 1 is not an input. | [TI Rev AF, pin table](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf) |
| `SN74LVC1G86DBVR`, DBV SOT-23-5 | 1 A, 2 B, 3 GND, 4 Y, 5 VCC; XOR for the live valid-direction test. | [TI Rev R, pin table](https://www.ti.com/lit/ds/symlink/sn74lvc1g86.pdf) |
| `LTC6993HS6-1#TRPBF`, S6 TSOT-23-6 | 1 TRIG, 2 GND, 3 SET, 4 DIV, 5 V+, 6 OUT. The **-1** version is rising-edge non-retriggerable; the -2 version is not interchangeable. | [ADI Rev F, pin table and operation](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc6993-6993-1-6993-2-6993-3-6993-4.pdf) |

The 1G74 requires valid clock/data and asynchronous-control timing; at 3.3 V, full-temperature table
values include 1.3 ns data setup, 1.2 ns data hold, 2.7 ns minimum clock and clear/preset pulses, and
1.2 ns asynchronous-control recovery. The behavioural model may use much larger explicit sequencing
margins; those margins remain design assumptions until physical delays, slew and loading are bounded.
The device's partial-power-down feature does not establish valid state during arbitrary brownout.

## Timer boundary

The proposed fixed timing is `NDIV=64`, `RSET=175.8 kohm`, positive output, with the divider values
specified in the driver proposal. Nominal width is 225.024 microseconds. Using the proposal's
full-temperature ±4.4% timer term and 0.1% resistor tolerance gives a **214.907821–235.159981 microsecond
timing assumption**, before additional drift, supply effects, propagation and physical shutdown tails.
Keep those terms separate from delivered-current duration.

A nominal 200 microsecond request ends before that interval. The timer is not cancelled at request
termination; its later falling edge sees request low and retains `TIMEOUT=0`. A held-high request at
expiry sets sticky timeout. Additional trigger edges cannot extend an active -1 timer; a new edge after
completion can start another internal interval, but consumed block prevents output until explicit rearm.
Startup and trigger recovery must meet the selected part's timing requirements. No simulation tick is
credited as a guaranteed device response bound.

## Finite scenario contract

The connected study should retain these scenarios and report both state transitions and signed load
current/phase charge where its analogue model provides them. Pass/fail of an ideal Boolean scenario
does not establish a nanosecond analogue interruption bound.

| Scenario | Required ideal-state outcome |
|---|---|
| Startup, request low | Reset/readiness inhibition sets block; bridge commands and RUN remain low. No power-up state is presumed without the external reset condition. |
| Request high through startup or readiness recovery | No newly admitted phase. Readiness recovery cannot clear block; safe rearm is impossible while request is high. |
| Qualified rearm, then normal request | Clear block/timeout and capture direction while request and timer are low; release rearm and allow settling before a new request edge. RUN follows the intersection of request, timer and permission. |
| Normal 200 microsecond request ends | RUN falls with request; block sets to consumed. Later timer expiry sees request low and does **not** create timeout. |
| Request drops early | Output stops and admission is consumed; record the interrupted waveform. No automatic balancing phase. |
| Request rises again during the old timer window | Timer is not extended; block prevents output from reopening. Captured direction remains unchanged. |
| Repeated request after timer expiry, without rearm | Timer can pulse internally but block or timeout prevents output. No automatic new phase. |
| Request stuck high | Timer directly removes RUN at expiry; timeout sets and remains sticky. Later request changes cannot clear it. |
| Request and timer fall within the latch timing aperture | Timer directly inhibits output. Timeout classification is indeterminate unless timing is resolved; do not force a favourable classification. Treat the event as a rejected/ambiguous trace. |
| Monitor permit or other base permission drops during a phase | RUN falls and block sets. Restoring permission while request remains high cannot resume. External monitor latch remains separate. |
| Both raw phase bits high, or both low | Valid direction becomes false, RUN is low and block sets. Restoring valid bits requires a new quiescent rearm. |
| Valid live direction swap during a request | Captured bridge direction does not reverse. This is an input-contract violation, not a detected XOR fault. |
| Rearm while request high, timer high, not quiescent or not qualified | Safe rearm remains false; no latch clears. A monitor fault is not cleared by the driver. |
| Source 0 fault while source 1 runs | Source 0 cannot restart through source 1's rearm/timer. Shared-rail/supervision drops can intentionally inhibit both. |
| Rails/brownout, followed by recovery | While qualified signals remain valid, drop permission and retain inhibition. Once logic supply leaves its operating range, mark Boolean/analogue state unqualified; require external reset/startup and explicit rearm on recovery. |

## What this slice can and cannot establish

An inspectable native circuit plus a matching behavioural study can establish the selected stable-state
equations, named single-phase histories, startup/rearm preconditions and conditional current waveforms.
It can expose a stuck-request cutoff without relying on firmware request termination. These are useful
engineering results even though the SCCI response and retained-learning assumptions remain hypothetical.

It does not establish arbitrary-fault coverage, glitch immunity, asynchronous metastability resolution,
physical supervisor thresholds, complete routing ownership, timer stuck-high protection, watchdog
implementation, delivered-phase charge protection, or biological safety. A failed-on switch, a failed
timer or a shorted sink can violate the conditional plant model. Inhibiting RUN and commanding all four
switches off is **not** rail-off terminal isolation; clamp, bias, capacitance and discharge paths remain.
Measure or model interruption latency and residual charge separately, including unknown/clipped history.

This is the finite control contract for the first current-driver slice. Extending it is a later versioned
engineering decision, not a reason to reopen Stage 3 or postpone the conditional concept architecture.

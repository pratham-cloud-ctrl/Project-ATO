# Contact routing: control and parasitic studies

This package accompanies the new [native contact router](../contact-router/README.md).
It does not alter the historical driver, monitor, recording or Stage 3 studies.

## Stable routing and ordered controller

`route_contract.py` checks the finite protocol in the
[control contract](../../../docs/stage4/contact-router-control-contract.md):
latched four-bit addresses, one-of-sixteen bank selection per source, collision
inhibit, zero-current commits, post-commit acknowledgement and explicit rearm.
The two dedicated returns remain distinct. Command readback and digital contact
ownership do not prove actual switch position, zero current or biological independence.
Analogue setup/hold, propagation, fault detection and output-isolation limits remain
explicit. Native source and return wiring are checked separately from this model.

## Passive off-contact coupling

`parasitic_study.py` records **36 finite passive cases**: three contact-capacitance
assumptions, three interterminal coupling assumptions and four two-bus edge patterns.
An unselected contact has a 1 Mohm discharge path and 1 nF, 100 nF or 2 microfarad
capacitance to a quiet fixture/body reference. Two source buses couple through
assumed 1, 5 or 15 pF interterminal capacitances. The asymmetric opposed case uses
one-third of the chosen coupling on the second bus. A separate 30 pF shunt lump
represents two off-source-to-ground capacitances. It is **not** a guaranteed
drain-to-source transfer capacitance.

Bus changes are ideal 24 V edges: aligned, opposed matched, opposed unequal or
staggered. They model common-mode changes at unselected paths, not the source's
signed load current or a complete biphasic stimulation waveform. The reference
is fixed in this fixture; actual tissue and moving dedicated-return potentials
need a separate coupled model. Between edges, voltage decays analytically through
the declared resistor. Charge conservation fixes each voltage jump. Saved traces
include both sides of every discontinuity; maxima are exact for this monotonic
first-order model, without implying a finite peak current for an ideal edge.

The 1 nF/15 pF aligned case produces about 0.679 V on an unselected contact.
The 2 microfarad version instead produces approximately 0.360 mV. These are
consequences of assumed capacitances, not measured electrode responses. Exactly
matched opposed edges cancel at this one ideal victim node; unequal coupling
retains a nonzero transient. Cancellation is not credited as general isolation.
No tissue-safe voltage or charge criterion is invented. Digital collision rejection
does not establish zero charge at every unselected contact.

The arithmetic supplement retains 4/20/60 ohm selected-path resistance assumptions
(12/60/180 mV drop at 3 mA), a 200 pF lump with 4.8 nC per 24 V edge, and thirty
off paths with a 25 nA **assumed** leakage allocation (150 pC summed absolute charge
over 200 microseconds). That sum is not automatically selected-load/shunt error.
Likewise, typical 3 pC switch injection and condition-specific device capacitance
are not worst-case assembled bounds. Native switching is prohibited during a
qualified event; faults and permitted reconfiguration still require accounting.

The [component review](../../../docs/stage4/contact-router-component-review.md)
selects TMUX6208PWR for this restricted 24 V slice. Its 12 V and 36 V tables inform
the study but do not supply an asserted guaranteed 24 V corner. Four-device power
arithmetic is 5.28/10.08 mW using 55/105 microamp single-supply test currents at
24 V; the actual test is at 39.6 V and the estimate is not a system power ceiling.
The full architecture's 48 V selection and power-off analogue isolation are not
implemented by this multiplexer choice. A heartbeat watchdog is also distinct
from the driver's independent microsecond duration supervision.

## Reproduction

From the repository root:

```text
python electronics/stage4/routing-study/route_contract.py --check
python electronics/stage4/routing-study/parasitic_study.py
python electronics/stage4/routing-study/verify_parasitics.py
```

The parasitic generator defaults to read-only same-model replay. Its explicit
`--write-results` refreshes JSON/NPZ evidence; the independent auditor's
`--write-receipt` refreshes the reviewed hash receipt. The auditor does not import
the producer: it recomputes RC decay, event charge, whole-window conservation,
coverage, peaks and arithmetic from saved scalar events and trajectories. It also
independently expands impulse superposition at all 10,116 trajectory points,
retaining the distinct pre-edge and post-edge samples. Text
hashes normalize line endings; binary hashes remain exact. Scientific plots are
generated from saved results only. These checks qualify the finite model, not
assembled electronics or the conditional biological applications.

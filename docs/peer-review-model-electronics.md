# Independent model–electronics interface review

This review checks connectivity, generic SPICE assumptions, passive output limiting, and the portable pulse interface. It is a read-only peer review of the digital design, not hardware or biological validation. Reviewed evidence: `electronics/connectivity.json`, the native design's generated netlist, `electronics/simulation/current_sink_generic.cir`, `scripts/simulate_electronics.py`, circuit metrics and rule reports, and the independently implemented C/ctypes pulse sequence.

## Connectivity findings

The single-ended current sink is coherent: U2B compares the buffered divider reference with the voltage across R10, drives Q1 through a gate resistor, and regulates approximately 100.157 µA at 5 V under sufficient compliance. The reference follows supply voltage; precision resistors do not remove that dependence. Q2 is an inhibited-state source-follower bypass supplying the sink while the output switches are open. That avoids an unloaded ideal servo winding fully into saturation, but it does not itself constrain switching current into the load.

The [Nexperia 74HC4053 pin description](https://assets.nexperia.com/documents/data-sheet/74HC_HCT4053.pdf) and [manufacturer device description](https://www.nexperia.com/product/74HC4053D) support the following polarity mapping:

| Switch pins | Connected net | Result when PHASE = 0 / 1 |
|---|---|---|
| 1Y0 pin 12 / 1Y1 pin 13 | +5 V / SINK | A common pin 14 selects +5 V / SINK |
| 2Y0 pin 2 / 2Y1 pin 1 | SINK / +5 V | B common pin 15 selects SINK / +5 V |
| S1 pin 11 and S2 pin 10 | PHASE | Both select inputs change together |
| E pin 6 | INHIBIT | High opens both paths |

Thus PHASE=0 gives positive current from DUT_A to DUT_B; PHASE=1 reverses it. This agrees with the C adapter's sign convention. No routing/polarity defect was found in this cross-connection. A default-high INHIBIT pull-up is suitable as a **digital default-off convention**. It is not proof of a measured power-up waveform or isolation under component failures.

The electrical dummy load is assumed to be a floating differential network. Grounding one DUT terminal through an earth-referenced measurement instrument introduces a return path absent from this model and can invalidate the reversal behavior. The SPICE fixture's 1 GΩ leakage to ground is a chosen weak leakage, not an oscilloscope-ground model. A future electrical bench verification would require a declared differential/isolated measurement arrangement; none has been performed here.

## Rev A finding and Rev B passive-limit reasoning

The original generic-device transient produced a 1,361.36 µA reverse-enable peak, about 13.59 times the 100.157 µA nominal setpoint. Charge agreement and settled-current agreement do not make that peak acceptable or disappear. The analytical ideal-current model and the C's commanded-current ceiling cannot bound this analog transient.

The proposed Rev B adds two 12 kΩ resistors in the external output path. That is a meaningful damping/current-limiting improvement and must be reflected in the schematic, PCB, BOM, connectivity manifest, SPICE netlist, compliance calculations, figures, and reports. For a discharged purely resistive short, taking no credit for switch on-resistance or the external load resistance gives

\[
|I|\le\frac{V_{DD,\max}}{R_{A,\min}+R_{B,\min}}.
\]

At 5.25 V and 1% resistor tolerance, this is 220.96 µA. At 0.1% tolerance it is 218.97 µA. These are **conditional resistive bounds**. They are not universal bounds for a polarized capacitor or arbitrary external voltage source.

For an opposing pre-existing polarization voltage \(V_{pol}\), the conservative reversal bound becomes

\[
|I|\le\frac{V_{DD,\max}+|V_{pol}|}
{R_{A,\min}+R_{B,\min}+R_{load,\min}}.
\]

Ignoring any external-load resistance, a 250 µA bound with two 12 kΩ resistors requires \(|V_{pol}|\le0.690\) V at 1% tolerance, or \(\le0.744\) V at 0.1%. The declared nominal 100 nF lumped load can satisfy a substantially smaller-polarization envelope under one approximately 20 nC phase, but the small-10 nF sensitivity load can exceed 1 V. A current source delivering 100 µA for 200 µs into 20 kΩ || 10 nF from a discharged state produces about 1.264 V polarization before leakage and reversal. This exceeds the conservative global-cap envelope above. The detailed servo may reduce the realized peak; that would be a model result, not a general passive-resistor theorem.

The same resistors also consume compliance: 100 µA across 24 kΩ uses about 2.4 V before external resistance, polarization, switch drops and sink headroom. Accordingly, a reduced available impedance range is an expected design tradeoff. Claims must state this tradeoff instead of presenting the resistors as free protection.

Requested revision checks were communicated to the electronics author:

1. Re-run nominal transient and verify peak, settled current, charge and compliance after the resistors are included consistently.
2. Include 5.25 V supply, minimum resistor values, small Cdl, and explicitly polarized/precharged-capacitor cases. State the tested envelope; do not assert a universal 250 µA analog cap.
3. Preserve the failed Rev A finding and explain why the revision was made.
4. Use the passive-bound calculation separately from generic SPICE's peak, and retain both numerical and model-structure limitations.

### Revision B review outcome

The revised connectivity places R14 between SW_A and DUT_A and R15 between SW_B and DUT_B. The revised SPICE netlist includes both resistors. The analytical compliance denominator also includes their combined 24 kΩ, so the same damping cost is represented across layers. The electronics author regenerated the native schematic/PCB and rule reports after routing the added parts.

An independent recalculation from `spice_transient.csv` confirmed 12,138 finite solver points covering the full 6 ms, peak current 102.578381 µA, positive charge 20.026663 nC and negative charge −20.027589 nC. Nominal modeled peak fell from 1,361.36 µA to 102.58 µA after the explicit design change; this is a conditional generic-model improvement rather than a guarantee on hardware.

Four additional generic-device transients are retained in `electronics/simulation/`:

| Declared sensitivity case | Simulated peak absolute current |
|---|---:|
| Cdl = 10 nF | 116.890 µA |
| Initial Cdl polarization +2 V | 127.231 µA |
| Initial Cdl polarization −2 V | 123.268 µA |
| Supply 5.25 V, Cdl = 10 nF, each output resistor 11.88 kΩ | 128.384 µA |

The precharge cases impose capacitor polarization at simulation time zero. The load then has approximately 1 ms of inhibited decay before the first enabled phase; with Rct × Cdl = 2 ms, the precharge at first enable is about ±1.213 V, rather than the original ±2 V. These cases should therefore be read as **initial-precharge cases**, not arbitrary 2 V disturbances applied at the instant of commutation. The minimum-resistor sensitivity uses a conservative 1% reduction although the BOM calls for 0.1% resistors; this is a wider modeled envelope, not an inconsistency in the native component specification.

The worst peak across these four selected sensitivity cases is 128.384 µA. That does not establish an exhaustive worst case. The separate passive inequality for an opposing 2 V capacitor voltage gives 305.13 µA at 5.25 V with 1% minimum resistors, taking no credit for the external resistance or switches. The generic servo can make particular simulated peaks lower than this bound. Neither the selected simulations nor the inequality supplies a universal 250 µA analog limit.

Review also requested that the high-supply case's current/charge validation be compared with its own supply-dependent expected setpoint, rather than the 5 V baseline. A 5.25 V reference naturally raises the expected current to approximately 105.165 µA; a flag showing deviation from 100.157 µA is not by itself a failed regulation test.

## PHASE/INHIBIT handshake

The C abstraction emits +100 µA for 200 µs, 50 µs off, −100 µA for 200 µs, then recovery. The adapter prepares PHASE=1 during the inhibited gap and PHASE=0 during inhibited recovery. The circuit SPICE stimulus changes PHASE midway through the 50 µs gap, which is also conceptually compatible with that interface.

A physical backend must **assert INHIBIT, allow disable propagation, change PHASE while off, allow switching and servo settling, and then enable at the next timer boundary**. Simultaneous ideal segment updates are not evidence that sequential GPIO writes, timing jitter, CMOS thresholds, Q2 bypass timing, switch charge injection, or overlap are controlled. The 50 µs nominal gap must not be presented as a measured settling guarantee. The external logic interface is 5 V CMOS; a 3.3 V MCU high must not be assumed sufficient without verified level conversion.

The C state machine was compiled and tested on a host. It enforces a timestamp refractory interval of at least 20 ms even if a caller incorrectly drains timer events early. It requires fresh valid sensor data and latches stale/invalid software faults. On a software sensor fault it completes an already scheduled balancing phase before inhibiting subsequent pulses. A power cut, compliance loss, analog current mismatch, hardware emergency stop or broken timer may interrupt or distort that phase; the ideal signed sum then provides no delivered-charge guarantee.

The timer backend remains abstract and assumes correct monotonic timestamps and correct boundary callbacks. No MCU, pin-level electrical capture, watchdog, or measured delivered-current feedback has been validated. These are material deployment limits, not undiscovered firmware bugs. No additional serious defect was found in the specified **ideal host behavior** after the refractory check was added, but this conclusion is limited to the covered inputs and abstraction.

## Generic SPICE model scope

The SPICE netlist uses a behavioral finite-bandwidth servo, a generic level-1 MOSFET, manually assigned gate capacitances, ideal controlled switches, and fixture leakage. It does not use device-specific transistor/op-amp macromodels or a package/board parasitic extraction. The switch's 70 Ω Ron is a chosen nominal value; its voltage/temperature dependence and real clamp/charge-injection behavior are not represented. In particular, a constant-Ron ideal switch and an ideal rail-limited behavioral amplifier cannot establish worst-case real-device startup or current peaks.

Clean ERC/DRC and schematic parity show design consistency under chosen rules. They do not verify compensation, power-up current, signal integrity, switching transients, or the current limit under component faults. The release should keep those forms of evidence separate.

**Review disposition:** the digital circuit's current-loop and polarity topology are coherent. Revision B addresses the identified nominal generic-model transient through an explicit, traceable resistance change and shows reduced peaks in four additional declared sensitivity cases. Its compliance cost and conditional passive bound must remain visible. The design is suitable for this digital simulation and presentation release with those qualifications. No universal analog current cap, tissue-safety claim, clinical control, or fabrication-validated stimulator is supported. No blocking defect remains in the specified ideal digital interface; physical timer and analog-driver validation remain future work.

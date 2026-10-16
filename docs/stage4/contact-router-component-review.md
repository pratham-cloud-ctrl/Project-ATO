# Contact-router component and interface review

**13 October 2026 - primary-source review for the restricted 24 V, 3 mA, 200 microsecond native driver slice.**

The routing slice selects one of sixteen shared stimulation contacts for each of two independently controlled sources. Each source retains its own dedicated return through its existing signed monitoring shunt. This is **two contact selectors with two fixed returns**, rather than the complete future architecture's arbitrary pair selection. The recording reference and body-bias contact are not stimulation returns.

## Analog selector selection

**TMUX6208PWR is the preferred component for this 24 V slice.** It is an active production, 16-pin PW/TSSOP part. Two eight-channel devices per source provide sixteen choices; their D terminals join the source's selected-contact output, and only one bank may be enabled. Four devices serve the two sources. Selection of the same shared contact by both admitted sources must be rejected by the route-control logic.

TMUX8108PWR was also reviewed. It is an active production part with the same PW pin mapping, a 10-100 V supply range and lower capacitance. However, section 9.3.2 explicitly identifies rapidly increasing on-resistance within about 5 V of VDD. Its nominal 38 ohm value must not be applied across the full 0-24 V range with a 24 V supply. A separate router rail above 29 V could address that headroom issue, but adds power and supervision requirements without a present need. TMUX6208 supports 24 V on the existing rail, with lower nominal resistance, switching injection and supply consumption. Its larger capacitance is retained as a circuit-study cost. [TMUX6208 datasheet, sections 5, 6 and 8](https://www.ti.com/lit/ds/symlink/tmux6208.pdf), [TMUX8108 datasheet, sections 6, 7 and 9.3.2](https://www.ti.com/lit/ds/symlink/tmux8108.pdf).

TMUX6104 was considered as a low-capacitance, low-power alternative. It is four-channel and its single-supply operating range is only 10-16.5 V; a 24 V unipolar terminal is therefore outside its operating envelope. A component called TMUX6108 was not established from the manufacturer's catalog and is not selected. [TMUX6104 primary datasheet](https://www.ti.com/lit/ds/symlink/tmux6104.pdf).

### Exact PW/TSSOP pin contract

The following mapping applies to **TMUX6208PWR** and **TMUX8108PWR**, and has sixteen perimeter pins with **no exposed pad**. The alternative RUM/WQFN package has a different numbering scheme and a pad; it must not be substituted into this footprint.

| Pin | Function | Pin | Function |
|---|---|---|---|
| 1 | A0 | 9 | S8 |
| 2 | EN | 10 | S7 |
| 3 | VSS | 11 | S6 |
| 4 | S1 | 12 | S5 |
| 5 | S2 | 13 | VDD |
| 6 | S3 | 14 | GND |
| 7 | S4 | 15 | A2 |
| 8 | D | 16 | A1 |

EN is active high. EN low opens all paths; EN high selects S1 through S8 for A2:A1:A0 = 000 through 111. Each path is bidirectional. In this slice VSS and GND are tied to driver ground, and VDD is the qualified 24 V rail. A negative current phase does **not** imply negative absolute terminal voltage: the driver bridge reverses current between the selected contact and its dedicated return while both terminals must stay inside the admitted supply envelope.

TMUX6208 requires VDD and VDD-VSS between 4.5 and 36 V. **Every analog pin, including an unselected contact, must remain between VSS and VDD.** Signals outside this range can reach supply-clamp paths even when EN is low. Logic VIH is at least 1.3 V and VIL at most 0.8 V; 3.3 V logic fits. Its approximately 4 megohm internal logic pull-downs are not a substitute for the external default-state and leakage budget. Place local supply decoupling in the native design.

### Quantitative anchors and their test conditions

The device has no separate guaranteed 24 V electrical-characteristic table. The 12 V and 36 V single-supply tables and the typical 24 V on-resistance plot are useful anchors, not permission to relabel their limits as measured or guaranteed 24 V performance.

| Property | 12 V single-supply table | 36 V single-supply table |
|---|---|---|
| On resistance | 7 ohm typical; 16.5 ohm maximum to 125 C, signal 0-10 V, -10 mA | 4 ohm typical; 9.4 ohm maximum to 125 C, signal 0-30 V, -10 mA |
| Supply current | 30 microampere typical; 65 microampere maximum to 125 C, VDD=13.2 V | 55 microampere typical; 105 microampere maximum to 125 C, VDD=39.6 V |
| Source off leakage | +/-8 nA maximum to 125 C, 10 V/1 V endpoints | +/-10 nA maximum to 125 C, 30 V/1 V endpoints |
| Drain off leakage | +/-30 nA maximum to 125 C | +/-85 nA maximum to 125 C |
| Channel on leakage | +/-28 nA maximum to 125 C | +/-78 nA maximum to 125 C |
| Source off / drain off / on capacitance | 17 / 155 / 200 pF typical, midrail, 1 MHz | 15 / 138 / 185 pF typical, midrail, 1 MHz |
| Injection | 2 pC typical at midrail, 100 pF load | 2 pC typical at midrail, 100 pF load |
| Enable turn-off | 370 ns maximum to 125 C | 315 ns maximum to 125 C |
| Enable turn-on | 265 ns maximum to 125 C | 240 ns maximum to 125 C |
| Address transition | 276 ns maximum to 125 C | 240 ns maximum to 125 C |
| Supply-to-output startup | 1 ms maximum at 85/125 C, VDD rise time 1 microsecond | 0.15 ms typical; no maximum printed |

Switch timing uses a 300 ohm load and 35 pF capacitance, with signal 8 V at 12 V supply or 18 V at 36 V supply. It does not directly bound settling into an electrode model, routing capacitance or a nonlinear current driver. The datasheet's internal break-before-make property is per device; **it does not coordinate two separate eight-channel banks**. An externally allocated all-off interval before address commit and a separate settling interval before enabling the driver are required. Their chosen numerical values must be recorded in the control contract as engineering allocations pending circuit qualification.

For planning only, four chips at 24 V and 55/105 microampere per chip yield 5.28/10.08 mW. These are arithmetic projections from the 36 V table, not a guaranteed 24 V budget; logic, drivers, monitors, rail conversion and switching losses are additional. At a stated 20 ohm study resistance, one selected path drops 60 mV and dissipates 0.18 mW at 3 mA. This 20 ohm value is a study assumption, not a new datasheet limit.

The 200 pF on-state anchor stores 4.8 nC at 24 V; the 17 pF off-source anchor corresponds to 0.408 nC for an ideal 24 V step. Those values are charge-conservation arithmetic, not delivered tissue charge or a guarantee of zero unselected-contact current. Shared nodes, return impedance, contact polarization and internal parasitics determine actual distribution. The native routing study should retain those paths explicitly or label them omitted.

### Disabled and unpowered conditions

Fail-safe logic protects the **control inputs** when the analog supply is absent. It does not establish high-voltage, powered-off analog isolation. Analog terminals are diode-clamped to the supplies. The rail-shutdown sequence must remove drive energy and discharge/qualify connected contacts before lowering the router rail; a charged external contact with VDD=0 is outside the normal operating range. EN low, a healthy MCU, an address comparator or an ERC-clean schematic does not prove terminal isolation, detect a stuck analog switch, or prove the selected contact matches its software name.

## Candidate-address and active-address logic

**SN74LVC595APWR**, PW/TSSOP-16, is an active production 3.3 V-compatible part. Pin contract: 1 QB; 2 QC; 3 QD; 4 QE; 5 QF; 6 QG; 7 QH; 8 GND; 9 QH' serial output; 10 /SRCLR; 11 SRCLK; 12 RCLK; 13 /OE; 14 SER; 15 QA; 16 VCC. SRCLK rising shifts serial data; RCLK rising transfers the shift stage to storage. /SRCLR low resets **only the shift stage**. /OE high tristates QA-QH, but QH' remains active. [SN74LVC595A datasheet, sections 4, 5.7, 7.1 and 8.1](https://www.ti.com/lit/ds/symlink/sn74lvc595a.pdf).

Accordingly, resetting /SRCLR does not clear an active route. The 595 supplies a candidate word; active-address flip-flops must retain their previous value unless a deliberate commit is admitted while both sources are quiescent and the selector paths are already disabled. Candidate equality alone cannot invalidate an otherwise held active route or change its contacts. Supply loss and uninitialized registers require the independent default inhibit and startup qualification. Do not use combinational `COMMIT & SAFE` as a clock: SAFE restoring while COMMIT is high would create an unintended rising edge.

**SN74LVC157APWR**, PW/TSSOP-16, provides four two-input multiplexers for a clock-enable-style active D input. Pins: 1 A/B select; 2 1A; 3 1B; 4 1Y; 5 2A; 6 2B; 7 2Y; 8 GND; 9 3Y; 10 3B; 11 3A; 12 4Y; 13 4B; 14 4A; 15 /G; 16 VCC. /G low enables selection; select low chooses A, high chooses B. **/G high forces outputs low; it does not tristate them.** Use the active flip-flop's unconditional raw commit clock and select between held Q and the candidate D only through a setup/hold-qualified admission. [SN74LVC157A datasheet, sections 3, 4.3 and 6](https://www.ti.com/lit/ds/symlink/sn74lvc157a.pdf).

At 3.3 V +/-0.3 V, the 595 requires SER setup 2.5 ns and hold 1.5 ns around SRCLK rising, SRCLK-to-RCLK setup 2.5 ns, RCLK high/low pulse duration at least 4.5 ns, and its RCLK-to-output maximum is 7.7 ns at 50 pF. These are component requirements, not a complete route-commit timing proof. Apply slower digital preparation and admission settling budgets explicitly, accounting for gates, fanout, skew and the active DFF's own requirements. Existing reviewed LVC1G74, XOR, OR, AND and inverter pin contracts remain in the [driver component review](current-driver-component-review.md).

## Independent supervision boundary

TPS3431SDRBR was reviewed as a future MCU-heartbeat option, not selected as a microsecond pulse limiter. It is active production, VSON-8 with a grounded exposed pad: 1 VDD; 2 CWD; 3 EN; 4 GND; 5 SET1; 6 WDI; 7 /WDO; 8 ENOUT. It accepts 1.8-6.5 V, uses falling WDI edges, and has 10 microampere typical/19 microampere maximum supply current. CWD=10 kohm to VDD gives a 170-230 ms timeout; a 100 pF ideal capacitor gives 56.77-68.7 ms. The 170-230 ms reset output delay and startup behavior also matter. EN low suppresses the watchdog and leaves /WDO high impedance, so /WDO alone is not a startup-safe permission. [TPS3431 datasheet, sections 5, 6 and 8.1](https://www.ti.com/lit/ds/symlink/tps3431.pdf).

Those times are orders of magnitude longer than the 200 microsecond phase. TPS3431 cannot close the known LTC6993 SET-open/timer-stuck-high gap. An independently powered/clocked pulse-duration supervisor, rail qualification and signed current/charge observation remain separate required work. Likewise, the router's collision/commit logic establishes only its specified digital admission behavior under healthy logic components; it does not close analog-switch or contact faults.

## Source identity

Manufacturer PDFs were retrieved on 13 October 2026 into ignored `tmp/router-primary-13oct`; copied datasheets are not redistributed as project-authored content. Revision and exact downloaded SHA-256 provide a recoverable reading record; manufacturer URLs can later serve different binary revisions.

| Primary source | Revision | Download SHA-256 |
|---|---|---|
| [TMUX6208](https://www.ti.com/lit/ds/symlink/tmux6208.pdf) | SCDS419E, July 2024 | `dbb3e771e4dd44233c6893a141c6e1f8cd11993d51731e3a1ee6bcb4419123be` |
| [TMUX8108](https://www.ti.com/lit/ds/symlink/tmux8108.pdf) | SCDS435B, August 2023 | `af0c3848e5e59f2c20b160b0a778b0c5788a1633daa9a6b96d3ec800984e8cb2` |
| [SN74LVC595A](https://www.ti.com/lit/ds/symlink/sn74lvc595a.pdf) | SCASE93A, October 2025 | `7f1841efc14c80c7241ed3d37876de60472fb05567c0e13eb73c3c466da53072` |
| [SN74LVC157A](https://www.ti.com/lit/ds/symlink/sn74lvc157a.pdf) | SCAS292S, December 2024 | `d53b84ce1043e9eff2b01679a029be52b444f0cd2e1d942a002a4ff029698097` |
| [TPS3431](https://www.ti.com/lit/ds/symlink/tps3431.pdf) | SNVSB66A, October 2021 | `99bf5dbfffe06e8f85d9a86cfb777a0151e85b4a103033bc025f4897a0bdc6f3` |

This review is an AI-assisted component and interface check. It establishes neither implant qualification nor retained motor learning or physiological efficacy. Those biological claims continue to depend on the project's explicitly conditional mechanisms and future evidence.

## Independent native-export and passive-study review

A separate review inspected the final exported `contact_router.xml` and saved passive-coupling evidence without importing either native or parasitic generator. **227 critical exported pin/net assertions passed**: all four TMUX6208 packages, the candidate 595, both 157 hold/load multiplexers, eight active-address flip-flops, their actual Q-bit readback, raw commit/acknowledgement/rearm clocks, acknowledgement/validity clear paths, and the full-address collision inputs. The final native package has 155 components and 650 pin connections across six sheets. Its single canonical J7 connector exposes sixteen shared contacts on pins 1-16 and the two dedicated returns on pins 17-18. Each dedicated return net connects only J7 and its own source-side monitoring handoff; the returns are distinct, and this package adds no second monitoring shunt. This checks command connectivity against the reviewed pin contracts, not actual switch position.

The passive study's 36 cases have consistent SI units: an edge contributes `Cmutual * deltaV` coulombs, divides by the total victim capacitance to produce its voltage jump, and subsequently decays with time constant `R * Ctotal`. The final read-only auditor's **10,917 checks passed**, comprising the original 801 scalar checks and an independent closed-form superposition check of **all 10,116 saved trajectory points**, including both sides of edge discontinuities. Maximum whole-window charge-conservation residual was approximately `2.07e-25 C`; the separately reviewed maximum trajectory-voltage disagreement was `1.11e-16 V`. The superposition calculation uses declared input capacitances, bus changes and resistance directly, rather than the producer's saved event voltages. Incorporating that independent trajectory audit did not change the original saved passive-case data.

Scope wording was checked in the study README and saved results: interterminal coupling is explicitly assumed, the separate 30 pF shunt is not relabeled as drain-source transfer capacitance, exact opposed cancellation is limited to one matched ideal victim, and no finite edge-current peak, tissue-safe criterion or power-off isolation is claimed. The selected-path resistance, leakage and 24 V power projections remain illustrative allocations. These checks establish consistency of the finite passive model; they do not qualify the assembled driver/router transient or the required external current, rail, isolation, watchdog and truthful-readback observations.

The review identified and resolved one integration-document mismatch: the native package allocated 25 microseconds for routing turn-off/settling while the protocol draft stated 20 microseconds. Both now use **25 microseconds**. This is a provisional engineering allocation, not a measured or validated 24 V hardware deadline.

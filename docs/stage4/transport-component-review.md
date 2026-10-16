# Monitoring transport and companion interfaces — primary component review

**14 October 2026.** This review supports the new digital monitoring package.
It checks manufacturer identities and the selected finite operating contract;
it does not turn electrical observations into demonstrated spinal decoding,
retained motor learning, or blood-pressure regulation.

## Acquisition architecture and selection

The existing two **ADS8866** devices remain charge-integrator endpoint ADCs.
Their aggregate maximum of 200k conversions/s does not satisfy the separate
450k current/pair-voltage/health conversion allocation. A dedicated
**ADS8688IDBTR**, with its own SPI bus and internal reference, supplies that
additional acquisition capacity. It observes existing voltage outputs rather
than body contacts. Independent hardware current windows, watchdogs, phase
timers and terminal guards retain their existing authority.

The ADS8688 is an eight-channel multiplexed 16-bit SAR device rated for 500k
aggregate conversions/s. Its 4.75–5.25 V analog supply uses HOST_5; the digital
supply uses HOST_3V3. All eight channels use range code **0x06**, corresponding
to 0…1.25 times the internal reference, nominally **0…5.12 V**. This is a
configuration that must be written and read back: the power-on default is the
different bipolar ±10.24 V range. The native part is the DBT TSSOP-38 package,
9.7 × 4.4 mm body, 0.5 mm pitch. The checked pin identities follow the top-view
figure and pin-name columns in section 6; some descriptive sentences for
channels 2–5 contain positive/negative wording errors, so the pin names and
diagram take precedence. [TI ADS8688 datasheet, SBAS582C, Rev. C, sections 6,
7.3, 7.5 and 8.5](https://www.ti.com/lit/ds/symlink/ads8688.pdf).

Existing gross HOST_5 window qualification includes comparator tolerance and
hysteresis; it alone does not guarantee the ADC's narrower 4.75…5.25 V supply
condition. Valid conversion claims require the actual regulated rail to remain
inside that manufacturer interval. The finite transport model uses that
explicit valid-supply condition and invalidates observations on health loss;
it does not silently narrow the historical supervision thresholds.

| ADC channel | Physical positive / local-ground pins | Observation |
|---|---|---|
| 0 | 16 / 17 | Existing CH0_I_MON |
| 1 | 18 / 19 | Existing CH1_I_MON |
| 2 | 21 / 20 | Existing CH0_VPAIR |
| 3 | 23 / 22 | Existing CH1_VPAIR |
| 4 | 25 / 24 | Monitor 4.096 V reference |
| 5 | 27 / 26 | Monitor 2.048 V midpoint |
| 6 | 12 / 13 | Divided PACK_BUS |
| 7 | 14 / 15 | Divided HOST_5 |

The saved upstream XML exposes CH0/CH1 current at monitor J4 pins 1/2 and
midpoint at J4 pin 3. Supervisor J4 pins 4/3 expose the monitor reference and
midpoint. Pair-voltage signals are component-pin taps at supervisor **U502 pin
1** and **U502 pin 7**; no existing pair-voltage header is invented. PACK_BUS
is power J5 pin 1. The wiring plan must preserve these exact endpoints.

## ADC support connections and analog limits

ADS8688 pin 1 is SDI; 2 is active-low reset/power-down; 3 DAISY is grounded;
4 REFSEL is grounded to enable the internal reference. Pin 5 REFIO has 22 µF
to reference ground pin 6; pin 7 REFCAP has 22 µF plus 1 µF. The internal
reference is separate from MON_VREF. Consequently, gross movement of the old
monitor reference can be observed against a different reference; this does
not provide calibrated or failure-independent precision.

Pins 9 and 30 receive HOST_5 with separate 10 µF/1 µF bypass allocations.
Pin 34 receives HOST_3V3 with 10 µF plus 100 nF. Analog/digital/reference
ground pins 6, 8, 28, 29, 31, 32 and 33 join local host ground. Unused AUX_IN
pin 10 and AUX_GND pin 11 are grounded. **Pin 35 DNC remains genuinely
unconnected.** SDO, SCLK and CS occupy pins 36, 37 and 38. The 100k CS pull-up
and reset pull-down establish inactive/default reset commands under valid
supplies; they do not qualify partial-power ramps. Physical capacitor derating,
reference placement and ground-current control belong to the PCB handoff.

Each observation has 100 Ω/1 nF input filtering. The ADC already includes a
PGA, driver and second-order low-pass filter, with approximately **15 kHz
typical** cutoff. A 200k samples/s current allocation therefore oversamples a
filtered voltage; it does not produce 200 kHz analog bandwidth or earn sharp
pulse-edge timing. The external RC pole is about 1.59 MHz and is not a sufficient
Nyquist antialias filter for the declared individual channel rates. Aliasing,
filter phase, step settling and complete dose precision remain limited claims.

For the chosen unipolar range the input behaves approximately as resistance
to a 2.5 V internal bias, rather than a resistor to ground. Input impedance is
specified as **0.85…1.15 MΩ at 25°C**, with typical 7/max 25 ppm/°C drift.
The 100 Ω filter and health-divider loading must therefore be included in
voltage reconstruction. PACK_BUS uses 4.99k/2.49k, and HOST_5 uses 2.4k/2k;
their Thevenin resistances remain below 2kΩ. These are coarse electrical health
observations, not battery state-of-charge estimates. Overvoltage protection
conditions are also supply dependent: ±20 V requires powered/low-impedance
AVDD; the floating unpowered condition is limited to ±11 V. They do not justify
connecting a 24 V stimulation node to the ADC. [TI ADS8688 datasheet, sections
7.1, 7.5, 8.3.3–8.3.6 and 10–11](https://www.ti.com/lit/ds/symlink/ads8688.pdf).

The 2.5 V bias equivalent comes directly from the section 7.5 input-current
equation for either unipolar range, `(VIN - 2.50 V) / RIN`; it is not an
invented ground-referenced leakage approximation. The illustrative 7.5/15/22.5
kHz filter study surrounds the manufacturer's typical cutoff and does not
claim those values are guaranteed manufacturer minimum/maximum limits.

ADC gain error is specified up to ±0.05% of full-scale range at 25°C, INL up
to ±2 LSB, and unipolar offset up to ±2 mV. Offset on a 40 V/A current monitor
alone corresponds to 50 µA before calibration or baseline subtraction. Raw
monitor transport does not erase the existing integrator bypass/bias errors,
and the 4% charge-precision target remains unearned unless its complete stated
domain is independently established.

## Raw sample identity and SPI timing

The ADS8688 samples on **CS falling**. The analog channel for that aperture is
selected by the command in the **previous** frame. The first 16 falling SCLK
edges load the next command; the result of the current aperture is read on the
17th through 32nd falling edges. Manual commands are C000, C400, C800, CC00,
D000, D400, D800 and DC00 hexadecimal for channels 0–7. Full 32-clock frames
are required for correct next-channel acquisition. The host must prime a known
channel, discard unknown startup results, and associate each returned code with
the previous command and the current aperture timestamp.

Maximum conversion time is 850 ns, minimum acquisition time 1150 ns, and minimum
conversion period 2 µs. SCLK is limited to 17 MHz; the selected 16 MHz clock
allows 32 clocks in 2 µs. However, the complete frame also needs CS setup,
hold and high time: 30 ns from CS falling to SCLK falling, 10 ns from the last
SCLK falling to CS rising, and at least 30 ns CS high. A schedule that simply
starts every 2 µs would not satisfy those serial requirements at 16 MHz. The
transport schedule explicitly budgets those overheads and reports its actual
nonuniform current apertures rather than inventing exact 5 µs spacing.

Default SDO format 000 contains 16 conversion bits without a hardware channel
tag. Format 001 appends four channel-address bits; reading those requires at
least 36 clocks, which exceeds the 450k rate at 16 MHz even before CS overhead.
The selected high-rate stream consequently has **software-tracked identity**,
conditioned on accepted commands and intact framing. Configuration readback,
command readback, reset/epoch invalidation, DMA-count checks and deliberate
resynchronization provide diagnostics; they are not equivalent to an independently
observed channel tag on every high-rate sample. Lower-rate tagged diagnostic
transactions can be performed while the high-rate stream is stopped. This
boundary remains explicit. [TI ADS8688 datasheet, sections 7.6, 8.4.1.2,
8.4.2.6 and 8.5.2.3.2](https://www.ti.com/lit/ds/symlink/ads8688.pdf).

The internal reference's stated 15 ms turn-on is typical, not a worst-case
guarantee. Any longer software wait is an allocation that must be combined
with configuration/observation checks, rather than being relabeled guaranteed
reference settling.

## Existing charge endpoint ADCs

ADS8866 remains a 100k samples/s, 16-bit device with AVDD 2.7…3.6 V,
DVDD 1.65…3.6 V and reference 2.5…5 V. The old native circuit uses 3.3 V
analog/digital and its shared 4.096 V monitor reference. Conversion takes
up to 8.8 µs, with at least 1.2 µs acquisition and at least 10 µs between
conversions. Four-wire mode requires DIN high at least 7.5 ns before
CONVST rises, DIN high for at least 10 ns, and CONVST low for at least
20 ns. After conversion, DIN falling makes the MSB valid within 12.3 ns;
subsequent data propagation from SCLK falling is at most 13.4 ns. A common
endpoint SCLK can read the two separately selected outputs sequentially.

The shared endpoint data bus is an explicit manufacturer-supported topology:
section 9.4.1.2, pages 22–23, Figures 47–48 connect two DOUT pins to one host
input and select them sequentially through their DIN/CS pins. In section 7.7,
page 8, DIN low makes the MSB valid within **12.3 ns**; DIN high or the last
SCLK falling edge returns DOUT to three-state within **13.2 ns**. CONVST stays
high through readout, and DIN and CONVST must never both be low. The next
device is selected only after the previous output has released the bus.

The new package implements that join through **R30/R31, 330 Ω each**, to
MON_MISO and host header J22 pin 2. Readout uses mode 0 with idle-low SCLK:
the first rising edge samples the already enabled MSB, and subsequent falling
edges advance the data. Starting with a falling edge and then sampling rising
edges would instead lose the MSB. A 2.125 µs allocation contains 16 periods at
8 MHz, CS rising at 2.03125 µs and the next CS falling at 2.125 µs; its 93.75 ns
release interval exceeds the stated output-disable time.

The load condition remains a declared PCB handoff: a 330 Ω resistor and at
most 25 pF total effective bus capacitance have an ideal RC time constant of
8.25 ns and a 70% step crossing of 9.93 ns. This makes the 62.5 ns half-clock
interval plausible, but it does not model the ADC's output impedance, trace
reflection, inactive-device capacitance, receiver threshold or routing. The
manufacturer's timing load circuit in Figure 37, page 17, uses **20 pF**, so
the chosen 25 pF condition is not a guaranteed loaded timing rating. Both CS
pins active together invalidate the result; the series resistors do not
qualify arbitrary output contention. Physical timing and signal integrity
remain to be verified with the consolidated PCB and target firmware.

The proposed separate 8 MHz endpoint bus takes 2 µs per 16-bit result. Both
channels can capture a common requested aperture and then be read after
conversion completion without confusing read time with capture time. The
part's 4 ns aperture delay and 5 ps jitter are typical individual figures;
they do not establish cross-device simultaneous sampling skew. PRE and POST
samples must retain source, phase, sign, integrator-reset epoch and aperture
identities. An arbitrary valid ADC code is not automatically a charge endpoint.
[TI ADS8866 datasheet, SBAS614C, Rev. C, sections 7.5 and 7.7](https://www.ti.com/lit/ds/symlink/ads8866.pdf).

## Companion electrical interface

The selected companion link is a short, externally powered **3.3 V UART,
1 Mbaud, 8N1**, through an **ISO6721BDR**. Its standard, non-F default-HIGH
variant matches UART idle. The B suffix is part of the current orderable
identity; the different ISO6721RB pin arrangement must not be substituted
without changing the symbol and nets.

| ISO6721BDR pin | Native connection |
|---|---|
| 1 VCC1 | HOST_3V3 |
| 2 OUTA | Host UART receive, through 33 Ω |
| 3 INB | Host UART transmit, through 33 Ω |
| 4 GND1 | Host ground |
| 5 GND2 | Companion ground |
| 6 OUTB | Companion UART receive, through 33 Ω |
| 7 INA | Companion UART transmit, through 33 Ω |
| 8 VCC2 | Externally supplied companion 3.3 V |

The two grounds and supplies have no passive bridge. Each side has 100 nF
plus 1 µF local bypass; input idle pull-ups use 10k. With input leakage up to
10 µA, a 10k pull-up loses at most 0.1 V, whereas the initially considered
100k value could lose 1 V and miss the 0.7 VCC input-high condition. The part
supports 50 Mbps, supplies 2.25…5.5 V for this operating region, up to 18 ns
propagation delay and up to 7 ns pulse-width distortion under its 3.3 V test
conditions. Its 300 µs startup figure and partially powered/undefined supply
regions are retained as limitations. Strongly driving an input whose local
supply is absent can weakly power that domain through its protection diode;
each UART transmitter must belong to its matching powered local domain.

The manufacturer's basic-isolation ratings belong to the component and its
specified conditions. They are not qualification of this board, complete
patient isolation, implant leakage, cable EMC/ESD, or communication through
the body. The external companion is a digital peer or artificial-signal
fixture. A validated SBP estimator/transducer remains a separate conditional
subsystem; pressure packets do not establish that a generic pressure sensor
measures arterial SBP. CRC, sequence, units, origin, age and authorization
must be checked separately from electrical UART operation. [TI ISO6721
datasheet, SLLSFJ0F, Rev. F, sections 5, 6.3, 6.11–6.12, 6.18, 8.4 and
10](https://www.ti.com/lit/ds/symlink/iso6721.pdf).

## Power and processor handoff

The ADS8688 analog-current maximum is 16 mA at 5 V under the 500k/internal-
reference condition, corresponding to 80 mW. Its stated 0.5 mA digital current
is typical; a 1 mA project allowance is a declared budget rather than a
manufacturer maximum. For the ISO6721B at 3.3 V, each side draws up to 2.8 mA
under the 1 Mbps AC test and up to 3.5 mA for the DC-low condition. The host
side and host pull-up/divider losses enter battery accounting; companion-side
power is externally supplied and separately disclosed. Newly populated
capacitors also enter startup-energy accounting.

Only **SPIM4** on the nRF5340 application core supports more than 8 MHz and
automatic CS. Reserve it for the 16 MHz raw ADC, with dedicated high-speed
pins P0.08 SCK, P0.09 MOSI, P0.10 MISO and P0.11 CSN and appropriate drive
configuration. A separate endpoint bus runs at 8 MHz; the recording bus
remains 4 MHz. EasyDMA execution, actual CS timing, bus ownership, MCU pins,
interrupt loads and target builds are the next firmware package. Finite
scheduling feasibility here is not a claim that those target peripherals have
already executed the schedule. [Nordic nRF5340 product specification,
SPIM instances and pin configuration](https://docs.nordicsemi.com/r/bundle/ps_nrf5340/page/spim.html-concept_v4x_5w2_wr?contentId=TLvyoNxdpe7dDfyvk0Hiwg),
[dedicated high-speed pin assignments](https://docs.nordicsemi.com/r/bundle/ps_nrf5340/page/chapters/pin.html?contentId=CwV5L_j_7YztGw5eukNpfw).

## Reviewed source identities

Primary PDFs were downloaded and inspected on 14 October 2026; these hashes
identify the reviewed versions, while the links above remain the canonical
sources. The local downloads are ignored working references.

| Document | SHA-256 |
|---|---|
| ADS8688 SBAS582C | c776e2307a48d547c394e1b778dcec2433b8c485a88cd6796da963bd2514eb6a |
| ADS8866 SBAS614C | 27f211b009303a0923bfd207bc3aa346e7642ee07d8bf3bf0bcfffb9138c6c9c |
| ISO6721 SLLSFJ0F | bd54a79cc78f46b412c521c32e4982b8c1694d79ea749ba3ee754975f719733f |

The native U1/U20 pin maps, bypasses, channel polarity, divider topology and
genuine DNC were checked against these primary documents and the generated
connectivity. No additional converter or body-facing transceiver is hidden
inside the digital model. Declared assumptions and rejected claims remain
usable results rather than reasons to reopen the already closed theory stage.

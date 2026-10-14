# Monitoring transport and companion control contract

Updated 14 October 2026. This is the finite digital contract for the seventh
native Stage 4 circuit package. It resolves missing raw-conversion hardware,
separates charge-endpoint observations from raw current samples and connects a
wired companion without inventing a pressure sensor or implanted radio.

The [saved calculation](../../electronics/stage4/transport-study/transport-results.json)
and [independent audit](../../electronics/stage4/transport-study/verify_transport.py)
bind the existing endpoint ADC pins and the new native connectivity. Default
execution reads existing artifacts; writing results or an audit report requires
an explicit option. The audit does not import the producer. These are schedule,
event, packet and queue checks; actual target firmware is the next package.

## Conversion identities and raw schedule

The two existing ADS8866 devices remain charge-endpoint converters. Their
100 ksample/s ratings are not combined into a fictional 450 ksample/s raw ADC.
One new ADS8688 provides the separate raw service. Its maximum SCLK is 17 MHz;
the selected dedicated bus runs at **16 MHz**, with a 32-bit transaction.

A conversion begins on CS falling. The channel was selected by the **previous**
transaction's command; the current transaction returns this aperture's result
and selects the next aperture's channel. A discarded MAN_CH0 priming frame,
range/configuration readback and a new configuration epoch precede acquisition.
Default 32-bit output carries no hardware channel ID. Software tags therefore
depend on a healthy command/CS path and verified configuration. An unknown or
missed transaction invalidates the epoch and prevents new dose admission until
reset, readback, priming and explicit rearm. A syntactically plausible but
undetected wrong-channel result is an explicit remaining fault boundary.

Each transaction reserves 34 ticks of 62.5 ns: 31.25 ns CS setup, 2,000 ns for
32 clocks, 31.25 ns hold and 62.5 ns CS high. This exceeds the stated 30/10/30 ns
minimum setup/hold/high intervals. Scheduling those edge intervals in target
hardware remains a firmware obligation; the table is not a measured SPIM trace.

| Observation | ADS8688 channel | Rate | Actual maximum aperture gap |
|---|---|---:|---:|
| Source 0 current | 0 | 200,000/s | 6.375 µs |
| Source 1 current | 1 | 200,000/s | 6.375 µs |
| Source 0 scaled pair voltage | 2 | 20,000/s | 50 µs |
| Source 1 scaled pair voltage | 3 | 20,000/s | 50 µs |
| Monitor reference, midpoint, scaled pack and scaled HOST_5 | 4–7 in rotation | 10,000/s combined; 2,500/s each | 400 µs per tap |

The 400 µs superperiod contains 180 transactions and reserves **95.625%** of
the raw bus. The two current streams are nonuniform: gaps range from 4.25 to
6.375 µs, and maximum displacement from the chosen 5 µs grid is 1.25 µs.
Per-aperture timestamps are retained; uniform-grid integration or filtering
must not silently replace them. Pair-voltage samples are exactly 50 µs apart.
This is an explicit timing revision to the earlier uniform-rate shorthand.

The ADS8688's internal analog low-pass filter is **15 kHz typical**. A high raw
sample rate does not establish 200 kHz analog bandwidth, anti-alias rejection,
settling, charge accuracy or detection of narrow current excursions. Independent
analog supervision retains its separate authority. The earlier 4% delivery
precision target remains unearned.

Primary timing and command basis: [TI ADS8688, Rev. C](https://www.ti.com/lit/ds/symlink/ads8688.pdf).

## Separate endpoint bus and phase attribution

Existing monitoring-cell U103 and U203 retain separate CNV, CS and DOUT nets
and a shared dedicated **8 MHz** endpoint clock. Their results cannot collide
with the raw ADC or RHD acquisition bus. Both sources may receive a requested
simultaneous CNV edge, followed by separate serialized reads. Actual cross-device
aperture skew is not bounded by this schedule; the published 4 ns aperture delay
is typical, not a guaranteed skew specification.

The new package makes the shared MISO connection explicit: **R30 and R31**
each connect one endpoint DOUT to `MON_MISO` through **330 Ω**. Host header
**J22** exposes clock, shared MISO, two CNV controls, two separate CS controls
and host ground. J20 retains the separate DOUTs for diagnostics. In four-wire
CS mode the unselected converter's DOUT is high impedance. The schedule selects
only one source for each read; simultaneously asserted CS signals invalidate
the read. The resistors limit a modeled contention path but do not establish
fault tolerance or physical SPI signal integrity. Actual loading and pin timing
remain target-firmware and PCB obligations.

The selected read samples the MSB on a rising SCLK edge 62.5 ns after CS falls;
the first falling edge is at 125 ns, and later rising samples follow preceding
falling data updates by 62.5 ns. The last falling edge is at 2,000 ns, CS rises
at 2,031.25 ns, and the next source is not selected until 2,125 ns. Published
DOUT enable, disable and data-propagation maxima are 12.3, 13.2 and 13.4 ns
under the manufacturer's test conditions. An illustrative added 25 pF RC load
with 330 Ω gives an 8.25 ns time constant and 9.93 ns to reach 70% of a step.
This screen fits the chosen edges but does not establish receiver setup/hold,
output-drive behavior, physical bus capacitance or final board timing. The
published timing-load figure uses 20 pF; the additional RC screen is a stated
design assumption. A falling-edge sampling scheme is not substituted for the
chosen rising-edge reads.

The finite schedule waits 9 µs after CNV, exceeding the 8.8 µs maximum conversion
time. Each 16-bit read reserves 2.125 µs including CS margin. Source 0 completes
at CNV +11.125 µs and source 1 at +13.25 µs. A **14 µs** minimum next-CNV
allocation therefore preserves both unread results. The part's minimum cycle
is 10 µs with at least 1.2 µs acquisition; the slower chosen schedule is
intentional. A 12 µs simultaneous-CNV burst is rejected on this shared 8 MHz bus.

Each stored result carries configuration epoch, event ID, source ID, capture
ID, endpoint label, CNV/aperture time and read-completion time. The latter never
replaces the aperture timestamp. The illustrative event retains paired baseline,
cathodic-tail, anodic-tail and net observations: eight results per source and
16 per simultaneous two-source event. At 360 events/s per source this requires
5,760 endpoint conversions/s and 1.224% of the endpoint bus's reserved time.
Average occupancy does not justify arbitrary overlapping bursts.

The illustrated tail windows assume observed settling qualifies before capture;
the next phase waits if qualification is absent. Missing tails, clipping,
unknown integrator history, duplicate IDs, unread-result overwrite and mixed
epochs reject charge attribution. An opposite-phase endpoint difference still
contains intervening gap/tail current. No result in this transport study receives
a phase-charge precision certificate.

Primary endpoint basis: [TI ADS8866, Rev. C](https://www.ti.com/lit/ds/symlink/ads8866.pdf).

## Processed companion packets and clock discipline

The populated ISO6721B is a bidirectional **1 Mbaud 8N1 UART** connection between
host and an externally powered 3.3 V companion. Host and companion grounds remain
distinct. This is a digital fixture interface. The external pressure sensor,
beat extractor, physical clock synchronization and body/RF link are not newly
implemented by this circuit.

The finite SBP packet is 56 bytes: a 40-byte little-endian versioned header,
12-byte payload and four-byte CRC32. The header carries packet kind, session
epoch, uint32 sequence, oldest/newest physical support times, extraction time,
payload length and quality. The payload carries SBP in mmHg, uncertainty and
calibration identity. Receipt time is recorded locally and cannot replace
physical measurement support.

Acceptance requires a trusted pre-established session, matching epoch, forward
sequence advance less than half the uint32 range, strictly newer physical
support, coherent support/extraction/arrival order, finite values, known
calibration and valid quality. The chosen 50–250 mmHg parser range is a digital
sanity gate; it is not a clinical intervention threshold. Clock conversion uses
a bounded offset interval with at most **±0.5 ms** uncertainty. The **oldest**
possible measurement time sets the age upper bound, which must be at most two
seconds. Unknown/excessive clock uncertainty, future support, replayed support
under a new sequence and an old measurement in a recent packet all reject.

CRC detects the exercised byte corruption; it does not authenticate a sender,
establish truthful timestamps or detect an attacker who recomputes it. Trusted
session establishment, cryptographic protection and a truthful clock bound are
explicit assumptions for this protocol model. A 16-byte security-tag allocation
is included in link arithmetic without claiming implementation.
The actual exercised SBP encoding remains **56 bytes**; its conservative wire
accounting is **72 bytes** after that reserved 16-byte envelope. Feature packets
similarly reserve 188 bytes for a 128-byte payload. The study does not claim to
have generated or authenticated that future tag.

An invalid packet clears previous support validity and latches transport
inhibition. A new valid packet updates support but does not automatically
restore permission. Explicit rearm requires that new support still be fresh.
The finite recovery history exercises valid/rearm → CRC fault/rearm rejection →
new valid support/explicit rearm. uint32 sequence wrap is accepted only as a
forward single-step advance with genuinely newer support.

## No-arrival, leases and fallback variants

At each 250 ms service tick, support age advances even if no packet arrives.
The saved no-arrival history crosses the two-second age boundary and blocks new
adaptation at the next service tick. Malformed or replayed arrivals cannot renew
support or an application lease. Motor and pressure modes retain mutually
exclusive authorization; transport freshness alone never authorizes a pulse.

A motor plan expires after its 250 ms lease even with healthy local observations.
A pressure plan expires after three seconds. If a UI link disappears while an
independent pressure path remains fresh, the pressure lease may continue to its
deadline. If the lost link also carries pressure, the earlier measurement-age
gate applies. Electrical trip and local health always override every lease.

Three illustrative stale-input outputs are retained: immediate stop, a 500 ms
hold followed by stop, and a 500 ms linear ramp to zero. All deny new adaptation;
a hardware trip forces zero immediately. These are finite digital comparison
variants, not selected clinical fallback recommendations. Supporting pressure
can have delayed biological effects, so removing drive does not establish
instantaneous physiological reversal or clinical safety.

## Bounded RAM and transport queues

Each 2.5 ms monitor block holds 1,125 16-bit results, 141-byte validity and
range masks, a 64-byte identity/header allocation and 32-byte alignment.
Two 2,624-byte blocks, a 64-entry ×32-byte endpoint ring and 512 bytes of bounded
identity/error state require **7,808 of 8,192 allocated bytes**. A released
half-buffer must be consumed before its 2.5 ms reuse deadline; a 2 ms budget
fits, while 2.501 or 3 ms does not. Deadline ties require the documented consumer
completion-before-reuse event order. Overrun invalidates the affected epoch;
overwritten bytes are never labeled valid. This is a memory allocation, not a
target linker map or measured interrupt latency.

Normal features, processed SBP, health, commands and leases total **95,296
wire-payload bit/s** with the 40-byte header, CRC and reserved 16-byte security
tag. A 20% contingency raises this to **114,355.2 bit/s**, below the selected
160 kbit/s service reservation. At 1 Mbaud, 8N1 allows at most 800 kbit/s of
byte payload before additional protocol stalls; therefore a 1 Mbit/s payload
service is not earned by this interface.

Raw transport groups ten 48-byte neural frames plus 60 bytes of packet/security
allocation. Continuous 4 kHz capture requires **1.728 Mbit/s**, exceeding both
the earlier 1 Mbit/s logical allocation and the actual UART's 800 kbit/s ceiling.
Even 2 kHz archive transport requires **864 kbit/s** after this framing and
exceeds the UART ceiling. A dedicated 16,384-byte raw queue fills in approximately
141 ms at 4 kHz and the optimistic 800 kbit/s UART service. The chosen **100 ms
diagnostic lease** bounds that calculated backlog to 11,600 bytes. Raw service
is exclusive from continuous normal feature traffic; it does not grant clinical
operation or unlimited recording. Queue-full stops diagnostic capture and
retains explicit gaps/overrun metadata. A stalled receiver can shorten the
admissible burst further; the chosen burst assumes the allocated service.

The remaining 8,192-byte normal queue and 8,192-byte command/validity allocation
keep the shared queue budget at 32,768 bytes. No external flash is introduced.

## Native integration plan

The [monitoring wiring table](monitoring-transport-wiring.csv) adds **34**
connections to the previous 102 supervisor and 32 power connections. The
[read-only integration audit](../../electronics/stage4/transport-study/verify_integration.py)
checks all **168** planned connections against saved native XML and component
manifests, giving **336** endpoint comparisons. It also checks **21** actual
pins at the raw-ADC, shared-endpoint and host/companion UART boundaries.
Pair-voltage observations explicitly originate at supervisor U502 pins 1/7;
the table does not invent an upstream pair-voltage connector. These are
integration nets, including component-pin taps, rather than a completed harness
or consolidated PCB. The nRF5340 and external pressure peer remain implementation
boundaries.

The combined plan preserves floating recording ground and separate externally
powered companion ground. The new resistor graph contains no passive bridge
across the companion isolation boundary. Existing open-drain power fault still
reaches the independent guard authority and is additionally observed by the
host interface. Monitor pre-arm health and arm-qualified enable remain distinct,
preserving the earlier startup-deadlock correction.

## Connection to the main concept and completion boundary

Motor interpretation still uses assumed useful spinal features to inform a
learner-specific policy. Expert voltage replay is not assumed, and stimulation-on
assistance does not demonstrate OFF retained learning. Physiological automation
still uses external measured SBP and calibrated, target-specific pressor
authority. The packet path does not create neural pressure information,
universal body control or biological efficacy.

This package is finite and reviewable once the native ADC/interface, saved
schedule, identity/packet/freshness cases, buffer/link failures and independent
audits agree. Unsupported analog response, actual clock truth, crypto, through-body
RF, target peripheral execution and clinical sensor behavior stay explicit.
They do not require repeating closed Stage 3 studies before implementing the
next target-firmware package.

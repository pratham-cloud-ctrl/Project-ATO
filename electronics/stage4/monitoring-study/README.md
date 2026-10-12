# Stage 4 — independent phase-charge monitoring study

**Status: 33 behavioral transient runs completed; prospective 4% phase-charge accuracy remains unearned.** This package investigates the first dual-source monitoring cell using an independent ngspice circuit and a separately derived linear KCL oracle. It provides numerical evidence about stated assumptions. It does not qualify the selected components, the complete implant, biological recruitment, motor learning or physiological efficacy.

The motivating question is concrete: can separate current and cumulative charge observations reveal each stimulation phase, rather than accepting two large opposed phases because their final integral nearly cancels? The study preserves first-phase, gap, second-phase, observed-tail and final-net measurements for **both sources**.

## Results to inspect

- [Full run records](results.json): 11 cases × three maximum time steps (500, 100 and 25 ns), with two electrical sources per run.
- [All 462 interval results](interval-results.csv), [engine logs](ngspice-log.json), editable [netlists](netlists/) and complete compressed [raw traces](traces/).
- [Waveforms and range faults](waveforms.png) and [phase/error witnesses](charge-witnesses.png). Plotting uses selected points for display; saved numerical traces retain every solver sample.
- [Primary sources and explicit assumptions](sources-and-assumptions.json).
- [Exact local runtime and engine provenance](environment.json).
- [Read-only verifier](verify_study.py) and [artifact receipt](artifact-manifest.json).

Raw traces occupy approximately 99 MB. No data are represented as physical measurements.

The finest-grid results show the following. Values below are source 0 raw endpoint estimates, before quantization; the full files include both signs, quantized estimates and load/shunt truth.

| Investigation | Result | Implication |
|---|---|---|
| Nominal 600 nC phases | Observed first −599.565 nC; second +599.566 nC; net about +0.001 nC | A settled endpoint pair is useful in this assumed model; a small net alone provides little phase information. |
| One 45 µA load-side bias | Exactly 9 nC load-versus-shunt mismatch over 200 µs | This exceeds the proposed 3 nC bias allocation before other errors. The actual path and calibration must be resolved. |
| Driver-side bias only | Load-versus-shunt result is unchanged in this imposed-load fixture | Bias location matters; the driver return current changes. A real current servo may change the load itself. |
| Fixed 6 pC injection before the settled baseline | Subsequent endpoint difference changes by less than 0.001 nC | A fixed settled reset-open jump cancels. Using a pre-reset baseline retains about 1.499 nC of that jump. |
| 6 pC differential injection inside the interval | Approximately +1.499 nC apparent charge | Injection after the baseline does not cancel. Leakage and settling also matter. |
| Deliberately slow response | Observed first −571.713 nC; second +547.737 nC | A 25 µs tail observation does not establish phase completion under this stress. The net can still be small. |
| Unequal opposed phases | Approximately −1199.131/+1196.134 nC observed; net −2.996 nC | Net within 24 nC can conceal phases almost twice the 600 nC target. |
| Deliberate 40 mA range fault | Integrator clipping on both channels; ADC range clipping on source 0 | Unknown clipped history must be rejected, even if later endpoints nearly return to baseline. |
| ADC arithmetic bound | Two-endpoint INL plus rounding: 1.71875 nC | The proposed 1.5 nC ADC allocation is already smaller than this conditional bound. It excludes offset, gain, noise and analog settling. |

The independent reviewer identified a missing loading term in the original analytical buffer equation. Including the downstream 33 Ω/1 nF load reduced the finest-grid discrepancy to approximately **13 nV**. This is agreement between two implementations of an assumed model, not evidence of 13 nV hardware accuracy. The frozen numerical gates are 20 µV oracle discrepancy, 0.1 nC between the 100 and 25 ns grids, and 100 pA pointwise KCL residual; they are not an accuracy budget or admission certificate.

## Electrical model and independent cross-check

The artificial load current enters the return node; positive shunt current flows towards an ideal 48 V driver-return node. Two explicit bias currents leave the load-side and driver-side nodes. The physical KCL identities are:

\[
i_L=i_S+b_L,\qquad i_S=i_D+b_D,
\]

so \(Q_L-Q_S=b_L\Delta t\). One 45 µA path gives 9 nC over 200 µs. Two such paths give 18 nC between the imposed load and driver current, but only the load-side path changes load-versus-shunt measurement in this fixture.

The sensor nominally produces \(2.048+40i_S\) volts. The 10 kΩ/22 nF signed integrator is interpreted with

\[
\hat Q=-K_0\,[V_{ADC}(t_b)-V_{ADC}(t_a)],\qquad K_0=5.5\;\mu\mathrm C/\mathrm V.
\]

Nominal 600 nC therefore spans 109.091 mV; an ideal 16-bit 4.096 V LSB corresponds to 0.34375 nC. Separate endpoints retain phase observations; a final bipolar endpoint alone loses information.

The independent oracle propagates seven states by a matrix exponential over each piecewise-linear input interval: load current, sensor deviation, feedback-capacitor voltage, amplifier internal deviation, buffer deviation, ADC deviation and cumulative load charge. It includes finite amplifier gain, reset conductance, input bias, parallel leakage, command/injection ramps and the **loaded** passive buffer/filter. If buffer deviation is \(b\), ADC deviation is \(a\) and internal amplifier deviation is \(x\),

\[
\dot b=(x-b)/t_b-(b-a)/(33t_b),\quad \dot a=(b-a)/(33\;\mathrm{ns}).
\]

Its linear prediction is checked only before the first predicted sensor/integrator clipping event. A linear oracle is not extended through saturation. The circuit's one-pole amplifier uses gm = 1 S, R = 1 MΩ and C = \(1/(2\pi\mathrm{GBW})\): the same gain and pole as a poorly conditioned gain-10⁶ voltage-source formulation, with no relaxation of solver tolerances. Solver initialization uses UIC and explicit capacitor initial conditions.

## Reset, intervals and finite observations

Reset opens at 100 µs. The positive 6 pC stress is injected into the summing node **1 µs after opening**, over 202 ns. This deliberately separates injection from switching and demonstrates baseline subtraction. It is not a TMUX1136 switch model. Unobserved differential injection is magnified by \(R_{int}/(G R_S)=250\), so 6 pC corresponds to 1.5 nC. A fixed jump that has settled before the baseline cancels; later injection, headroom loss, leakage decay and unsettled transients need separate bounds.

Source 0 begins negative at 200 µs; source 1 begins positive 25 µs later. Each nominal phase is commanded for 200 µs with a 100 µs gap. Baseline is 20 µs before the first phase. The first and second tail samples occur 25 µs after their command edges; the final sample occurs 300 µs after the second phase. **Second-tail minus first-tail includes intervening gap/recovery current.** It is not automatically pure second-phase charge. Command intervals, gap and observed intervals are all retained, so this distinction is inspectable. Command edges do not establish actual waveform endpoints.

ADC samples are assigned to CNV + 4 ns, motivated by typical aperture delay. Conversion-complete metadata is CNV + 8.8 µs; assumed read availability adds 1 µs. This does not verify the actual four-wire serial protocol, clock distribution, acquisition settling or independent observation support. The timing strip shifts the start by \(s\) and the end by \(-s\), for ±100 ns and ±1 µs: it explores symmetric interval expansion/contraction, not all independently varying endpoint errors.

## Cases and evidence limits

| Case | Deliberate change |
|---|---|
| nominal | 3 mA, 200 µs, nominal behavioral parameters |
| load_side_bias_45uA | One 45 µA load-side bypass |
| driver_side_bias_45uA | One 45 µA driver-side bypass |
| both_input_bias_45uA | Both paths present |
| reset_open_6pC | Positive injection after reset opens, before baseline |
| differential_injection_6pC | Positive injection between charge endpoints |
| slow_response | 20 µs driver constant; 100 kHz sensor/GBW; 50 kHz buffer |
| scale_offset_corner | Constructed component/offset/ADC gain corner |
| unequal_cancellation | 6/5.985 mA opposed phases: 1200/1197 nC |
| clipping_guard_bypassed | Deliberate 40 mA/500 µs fault; forced bypass metadata |
| reset_and_leakage_stress | Prebaseline injection plus 10 MΩ parallel leak |

The model uses manufacturer facts as motivation, then explicit behavioral assumptions. [INA241 Rev D](https://www.ti.com/lit/ds/symlink/ina241a.pdf) supplies nominal gain, typical bandwidth and condition-specific offset/bias limits. [OPA391 Rev E](https://www.ti.com/lit/ds/symlink/opa391.pdf) supplies DCK electrical data; one-pole response, hard rail clamps and passive buffer are assumptions. [ADS8866 Rev C](https://www.ti.com/lit/ds/symlink/ads8866.pdf) supplies conditional converter/timing limits; the selected 3.3 V/4.096 V operating point needs further characterization. [TMUX1136 Rev B](https://www.ti.com/lit/ds/symlink/tmux1136.pdf) lists typical −6 pC injection under its own test conditions, not a maximum or the sign/distribution used here. Sources were checked on 12 October 2026.

The original DBV package was marked preview in the OPA391 datasheet. A separate native-cell revision replaces it with the production DCK ordering/pin mapping checked against the [manufacturer ordering page](https://www.ti.com/product/OPA391); this model establishes neither package's physical performance. The study binds the reviewed native manifest and root schematic by normalized hashes but does not simulate a native schematic export or prove every connection.

The two 5 V INA241 channels alone have a 32 mW full-temperature maximum-IQ arithmetic allocation, exceeding the earlier 20 mW sensing budget. That requires an explicit system power revision. No temperature rise or power-delivery qualification follows from the arithmetic.

Range/bypass rejection is an evidence flag. The current-window crossing is reported separately; there is **no modeled shutdown actuator**, and a threshold-only crossing does not automatically set the range/bypass flag. The fault case intentionally exceeds admitted current/charge limits. Continuing its equations after a 4.096 V ADC-range overrun is a mathematical counterexample, not a prediction of device survival or overload recovery.

Other unresolved analog work includes actual current-source feedback and HV switching, bias return paths over voltage/temperature/power state, absolute gain/offset calibration and drift, component/leakage tolerances, op-amp slew and loop stability, SAR kickback and 16-bit acquisition settling, reference impedance/noise, ADC protection and input overvoltage history, supply/return coupling, timing bounds and independent shutdown implementation. A healthy flag in this package is not permission to deliver stimulation. No manufacturer macromodel, PCB extraction, fabricated circuit or biological experiment is present.

## Reproduce and verify

From the repository root, using its existing environment:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
.\.venv\Scripts\python.exe electronics\stage4\monitoring-study\verify_study.py
```

The read-only verifier works on Windows and Linux with NumPy/SciPy. It recomputes KCL, endpoints, interval arithmetic, finest-grid oracle comparisons, refinement, CSV correspondence and case/grid coverage, and checks the complete artifact receipt. It needs no ngspice installation and does not regenerate the receipt. Text hashes normalize CRLF/CR to LF; NPZ/PNG/PDF use exact bytes. The receipt itself and `__pycache__` are excluded; unexpected files fail verification.

Optional live rerun uses the installed shared library (or `NGSPICE_LIBRARY`/`--library` on another machine):

```powershell
.\.venv\Scripts\python.exe electronics\stage4\monitoring-study\study.py --run
.\.venv\Scripts\python.exe electronics\stage4\monitoring-study\plot_results.py
# Maintainer-only: review regenerated evidence before explicitly updating its receipt.
.\.venv\Scripts\python.exe electronics\stage4\monitoring-study\verify_study.py --write-receipt
```

The adapter uses the documented [ngspice shared-library API](https://ngspice.sourceforge.io/shared.html); no engine binary is redistributed. Live runs rewrite only this study package. Platform/engine versions can change numerical trajectories and compressed bytes, so a live rerun produces a new reviewable receipt rather than silently claiming byte identity.

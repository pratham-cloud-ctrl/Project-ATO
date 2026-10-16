# Delivery precision required by the observed motor map

9 October 2026. This is a new requirements calculation from four freshly observed
calibrations. It preserves the implemented monitor and the nominal 35 ms body
onset; it does not select a circuit or qualify dynamic assistance.

The [reproducible record](../../results/stage3/delivery-requirements/requirements.json)
contains four independent subject calibrations, 144 counterfactual requirement
rows and 24 full-direction precision thresholds. New calibration uses the scoped
2.5 ms midpoint/cascade body solver and bounded-residual acquisition. Controller
inputs are measured route responses and independently monitored charge. Private
recruitment matrices, thresholds and actual charge are not used by the analysis.

## Derivation and limits

For an observed route plateau `R`, mean measured dose `m`, prospective absolute
dose uncertainty `u`, and fixed measured-response allocation `b = 9.5 mm`, the
existing calibration contributes

```text
effective gain: route_sign * R / m
gain allowance: b/(m-u) + abs(R) u/[m(m-u)].
```

Opposed routes are averaged exactly as in the motor calibration. The script
recovers all four actual calibrated gain and uncertainty matrices before making
any counterfactual comparison. It then varies only the proposed uncertainty,
holding measured charge means and response records fixed. This is a requirement
for a future monitor, not a prediction that replacing hardware leaves every
measurement unchanged.

For a requested direction `d`, the full correction allocation is

```text
U_G abs(d)m + abs(G) abs(d)u + U_G abs(d)u + forecast allocation.
```

The third term is the gain/dose uncertainty product. Correlated errors are not
reduced by averaging repeated pulses. A common command scale is solved from this
allocation and the unchanged 25 mm correction budget, subject to positive
observed authority. A fractional scale describes steady effective-map algebra;
it does not authorize fractional physical pulses, an untested density or a
single-frame dynamic response.

## What the calculation changes

All four actual-monitor calibrations remain unqualified. At an illustrative
**8 mm forecast allocation**, full single-route corrections require charge
uncertainty below approximately **5.06–6.64% of nominal phase charge**, depending
on route and subject. A prospective **4%** allocation passes this scalar
single-route test across these four calibrations. It still requires independent
circuit evidence, dynamic response qualification and a validated predictor.

At the full **15 mm forecast allocation**, the corresponding requirement tightens
to approximately **0.354–0.471% of nominal phase charge**. Thus spending the entire
forecast allowance can make the electronics requirement much harder. Improving
the predictor and improving delivery precision are connected design choices.

Full simultaneous two-source correction fails the 25 mm calculation **even with
zero charge uncertainty** at both selected forecast allocations. The remaining
measured-response floor alone consumes 19 mm before forecast error. Better ADC
precision cannot remove that floor. Lower effective intervention, a separately
qualified more precise response estimate, or a validated dynamic single-frame
model is needed. This is a positive design constraint, not a ban on two physical
sources; pressure profiles and other responsibilities retain their own domains.

The 8 mm and 15 mm inputs are explicit comparison allocations. The first is not
a newly demonstrated assisted forecast, and this calculation cannot override an
assisted predictor's failed validation. The earlier 7.4% assumed-delivery branch
remains preserved and unqualified as hardware.

## Electronics handoff

Investigate independently evidenced charge integration or edge capture rather
than simply assigning MHz rates to the existing shared ADC. The
[earlier precision analysis](motor-precision-requirements.md) preserves its
aggregate ADC/bus limits. A new circuit must bound gain, offset, integration
bandwidth/interior waveform error, window edges, reset/hold behavior, both phases,
correlated errors and simultaneous sources. A current threshold or a nominal
waveform is not proof of a complete-waveform peak bound.

The current motor design therefore has a concrete prospective tradeoff: a
predictor near the 8 mm allocation and a monitor below 4% nominal uncertainty
would leave scalar room for selected single-route corrections in these
calibrations. Neither is presently implemented/qualified by this calculation.
Use it to choose and test the detailed native design, not to relabel the actual
negative branch.

Reproduce with `python scripts/stage3_delivery_requirements.py --check`.
Seven focused tests retain the impossible perfect-monitor case, threshold
bracketing, positive/negative authority, monotone command limits and the full
uncertainty product.

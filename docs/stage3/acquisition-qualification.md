# Digital acquisition qualification

8 October 2026. The original `fixed_history` mode remains a reproducible reference.
The new `bounded_residual` mode qualifies the declared digital filter against an
explicit error allocation. Neither mode proves analog amplifier recovery or
useful implanted spinal information.

## What the bound means

The comparison is between the implemented causal filter with zero-replaced
missing samples and the same initialized filter with unknown, range-bounded
digital samples at those apertures. The unknown digital input magnitude is at
most the declared 5 mV ADC range. This reference does not reconstruct an
unbounded analog signal or reverse saturation, and does not infer a neural value
from an artifact.

The filter uses SciPy's [cascaded direct-form-II-transposed SOS implementation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfilt.html).
The bound extracts its one-sample realization by independent basis excitations:

```text
state_next = A state + B input
output = C state + D input.
```

Padded, unreachable SOS states are removed using the input-reachable subspace.
In a complex modal basis, the implementation retains the complete transformed
matrix `M`, including off-diagonal numerical residuals. For a per-contact modal
error radius `r` and omitted-input bound `u`:

```text
output_error <= abs(C_modal) r + abs(D) u
r_next       <= abs(M) r + abs(B_modal) u.
```

The chosen magnitude recurrence is stable. At an independent zero-state session
initialization its radius is zero. A missing interval is **not** such an
initialization: resetting the implemented filter retains the stationary unknown
history allowance `(I - abs(M))^-1 abs(B_modal) range` for the counterfactual.
Pending artifact intervals survive that reset.

Quantized-output differences add one LSB when the residual is nonzero. Absolute
demodulator weights propagate that allowance into each of the 32 averaged
features on its actual valid support. The chosen qualification allocation is
2.4 microvolts per feature. This is an engineering allocation, not a measured
signal-discrimination or physiological threshold.

The selected realization has a well-conditioned reachable modal basis. Numerical
projection residuals, coefficient rounding and repeated operations are recorded;
outward `nextafter` operations do not constitute formal interval arithmetic.
Independent random, adversarial impulse-response and unknown-history witnesses
check the computed enclosure against direct SOS outputs. The result is a tested
floating-point engineering envelope, not a formal mathematical safety proof.

## Support and invalid input

Aggregate raw coverage cannot certify a feature with no samples. Every contact
now separately requires the declared 90% usable coverage and a recent valid
aperture. A test masks all of contact 15 while the other contacts preserve 93.75%
aggregate coverage; the packet is rejected.

The optional clock allowance contributes to latest-support age. The support
ordering gate reserves twice that allowance for sample and availability clock
uncertainty. The packet carries the allowance, feature residual bounds and
per-contact coverage for subsequent consumers. A separately chosen maximum
contiguous gap can reject concentrated losses even when total coverage passes.
These checks do not model full clock synchronization or transport sequence state.

Malformed requests are rejected before any filter reset, noise draw or counter
change. Normal and redundant sources, per-aperture arrays, artifact amplitudes
and artifact support must be finite and have their declared dimensions. This
prevents a rejected observation from destroying valid history or a NaN source
from being marked usable.

## Aperture-resolved source interface

The simulator may supply `(20 samples, 16 contacts, 4 private coordinates)`
evaluated at the existing 4 kHz apertures with 3 microsecond contact skew. This
changes the source approximation only. Acquisition rate, physical support,
availability, noise draws, causal filtering and quantization remain the same.
The controller receives only the resulting packet; private coordinates never
enter its API.

The saved diagnostic compares a declared analytic 1 Hz source at those apertures
against its block-start hold. It is an independent source-approximation witness,
not yet a full moving-body aperture convergence study. A full integration must
advance the body chronologically through apertures before deciding on the next
command.

## Reproduction and interpretation

Run [the qualification study](../../scripts/stage3_acquisition_qualification.py)
with `--check results/stage3/numerical/acquisition-qualification.json.gz`.
[The readable receipt](../../results/stage3/numerical/acquisition-qualification-summary.json)
links its full compressed witness, which
retains every packet, feature allowance, actual noise identity and schedule.

Under the chosen full-range omission bound, clean capture qualifies identically
in both modes. A single artifact at 300 ms first qualifies again at approximately
1.98 s in bounded mode, versus 405 ms in the fixed-history comparison. The 40 Hz
train ending before 1 s does not requalify within the five-second experiment;
its final maximum feature allowance is approximately 13.35 microvolts. These
are conservative model dispositions, not observed physical recovery times.
They show why a fixed wait alone cannot certify this digital counterfactual.

The analytic source diagnostic changes features by at most approximately 0.381
microvolts while retaining identical actual noise and aperture schedules. This
single source does not bound all motor trajectories. The original foundation
results remain explicitly associated with `fixed_history`; a stricter mode must
be named when used in a new coupled comparison.

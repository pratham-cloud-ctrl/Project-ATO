# One observed-state observer development protocol

Declared 12 October 2026 before development-target scoring. This tmp-only
experiment is nonconfirmatory. No authoritative predictor, pilot, qualification
receipt, scientific gate, or stimulation behavior changes.

## Frozen mechanism and information budget

The state is z = [xL, xR, thetaL1..4, thetaR1..4]: ten means. The explicit
synthetic structural model is x-dot = (theta phi(t) - x)/0.060 s, theta-dot =
zero-mean white uncertain drift. The known cue is the declared 1 Hz and 3 Hz
sine/cosine instruction, with sign reversals at exactly every two seconds.
Position is continuous at reversals. The 60 ms constant is conditional model
knowledge; it is not a biological measurement or a fitted private parameter.
Measurement noise is the previously declared independent 1.5 mm per coordinate.
No generator family, gain, theta, scale, latent state, future achieved position,
or recording name selects a prior, process model, update, or forecast.

There is one common prior and one coefficient diffusion covariance for all
records. Persistent trial memory is ten means and a symmetric 10x10 covariance
(55 unique entries), support/arrival clocks, a monotone decision clock, and a
consecutive-valid-sample counter. The Python implementation stores all 100
covariance entries; 55 is the symmetric mathematical count.
The learned common prior adds ten means plus 55 covariance entries; the
coefficient diffusion adds 36 symmetric entries. There are 101 learned scalar
entries, not 101 necessarily independent degrees of freedom. The fixed noise
variance, plant time constant, 5 ms clock, known cue schedule and rules are
additional structural settings. Prediction uses a temporary ten means and
55 covariance entries; 26 two-coordinate forecast means/variances are outputs.
No raw measurement history is retained. Persistent state summarizes the whole
accepted trial prefix, so it is more information than a stateless 75 ms window.
The optional study cache contains only deterministic cue/F/Q tables. Its maximum
float64 payload alone is 1,638,400 bytes, exceeding the proposed 512 KB target
RAM before Python overhead. This is a desktop development implementation, not
a target-ready or measured embedded resource claim. A diagnostic noise-sensitivity covariance is evaluator
bookkeeping only, not a predictor input.

## One measured-data-only calibration rule

Use only the eight already generated 12 s observed development calibration
records in `phase_balanced_longcal_observations_12oct.json.gz`. No new captures
are generated. Total exposure is 96 s: the first 8 s of each record (64 s total)
fit the common prior and drift; the last 4 s (32 s) are temporal development
holdout. The separate 12 s nominal record is not used. Record identifiers and
noise identifiers are provenance only, never fit features or selectors.

Partition each 8 s fit prefix into four two-second blocks, using 400 observed
samples per block with the right endpoint excluded. In each block, fit the
constant-coefficient plant's five unknowns per foot (initial position and four
harmonic coefficients) by unregularized ordinary least squares. Use the exact
known-cue convolution design and retain all residuals, ranks and condition
numbers. This is an observed-data estimate, not true coefficient recovery.

The eight first-block ten-vectors set the common initial mean. Their unbiased
between-record sample covariance plus the mean sensor-noise OLS covariance
sets the prior covariance. The sum retains estimation noise conservatively;
there is no private-state covariance correction. Coefficient diffusion S is
the uncentered second moment of adjacent-block eight-coefficient differences,
divided by their two-second center spacing, pooled across the 24 fit pairs.
Thus observed mean drift is included as uncertainty rather than inserted as a
known learning law. Sensor noise and block-model mismatch can inflate this
estimate; it is a declared heuristic measured-data prior, not an independently
identified biological diffusion. Symmetrize and clip only negative eigenvalues
within 1e-14 m2/s to zero; larger negative values are errors. Finite symmetric
state covariance has a roundoff-only 1e-12 m2 tolerance; larger negative values
are rejected, and nonfinite/malformed state is rejected before mutation.
No grid search, multiplier, seed search, horizon
selection, private-family fitting, or error-driven covariance adjustment.

## Causal runtime and exact propagation

For an interval [a,b], let J(a,b) be the exact exponentially weighted known-cue
integral. The mean transition has exp(-(b-a)/tau) on each position diagonal,
J in the corresponding position/coefficient block, and identity on coefficients.
For Brownian coefficient drift, integrate E(u,b) S E(u,b)-transpose from a to b,
where E(u,b) maps a coefficient increment at u into [J(u,b); I8]. Use 16-point
Gauss-Legendre integration on each 5 ms step, splitting direction events exactly.
Compose transitions and process covariances for longer forecast intervals.
Verify these against an independent high-accuracy differential-equation solve,
8-point quadrature and the covariance semigroup before target scoring.

An update accepts only a finite valid two-coordinate measurement whose stated
availability is no later than decision time, whose support is on the 5 ms clock,
and whose support is strictly later than the last accepted support. Require
0 <= support <= availability <= decision, and monotone decision time across
accepted updates and finite forecast calls. Rejected updates never change any
state, covariance, counter or clock. A backwards forecast is unavailable and
does not roll the decision clock back. The filter
state is updated at the physical support; forecasts then propagate through the
25 ms observation delay and any future known instruction. Use the Joseph
covariance update, with no gate or gain selected from future residuals.

Each record starts independently from the common measured-data prior at zero;
no trial or subject state carries across resets. Invalid/future/out-of-order
measurements are rejected without changing state. A gap greater than 50 ms
resets coefficients to the common prior, position to the newly observed
measurement with sensor covariance, and cross-covariance to zero. That sample
counts once. Require 16 consecutive valid 5 ms samples after start/gap before
declaring a forecast available. Irregular accepted spacing restarts this count.
These availability rules are not empirical qualification. Covariance is a
conditional uncertainty diagnostic, never a replacement for a maximum-error
allocation or an authorization to stimulate.
All 26 forecast means remain diagnostic outputs, but the complete forecast
vector is unavailable if even its shortest physical target precedes decision
time; per-target time validity is also returned. A sample loss cannot turn a
past physical target into an eligible future forecast merely because the last
arrival is recent.

## Freeze, checks, and bounded scoring

Save a method/calibration receipt with protocol, implementation and input hashes,
learned arrays, all calibration block fits and resources before scoring any of
the 16 previously inspected drift targets. Obtain an independent review of the
frozen method. Checks cover independent F/Q propagation across a reversal,
positive covariance, zero-noise propagation, analytic past-measurement noise
weights, measurement availability, future poisoning, out-of-order and gap reset,
known-cue reversal continuity, and identifier/forbidden-field invariance.

Then score the same fixed 550 current supports (0.100..2.845 s) and every one of
the 26 horizons (25..150 ms, 5 ms spacing) in all 16 already inspected drift
records. Also report temporal calibration holdout supports 8.100..11.845 s.
Report full errors and witnesses even for unavailable forecasts; save coverage,
all horizon/component residuals, reversal categories, covariance standard
deviations, and causal sensor-noise amplification. Development arithmetic is
maximum absolute observed component residual + the unchanged 3 mm label
allocation, compared with the unchanged 15 mm forecast budget. Report every
failure. The unchanged 25 mm combined correction gate is not evaluated by this
isolated predictor exercise. No covariance-only qualification is asserted.

These 16 records motivated this revision and are not fresh validation. Any
integration requires a frozen authoritative implementation, a predeclared
independent-noise confirmation cohort, identical calibration/history/structural
priors for external and neural comparator arms, finite support/action domains,
and a rerun of the unchanged isolated pilot. No retained-learning conclusion
follows from this development predictor result.

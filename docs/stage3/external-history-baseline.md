# Learned external-history comparator

This comparator addresses a confound in the original seven-arm motor study: the
neural path received a learned 32-input decoder, whereas the external-only path
used a fixed nine-sample straight-line fit. A neural-versus-external contrast
could therefore include differences in model capacity and temporal processing.
The historical results remain the results of those original seven arms. This
new comparator must be named separately when integrated and studied.

## Available information and capacity

The learned external input contains the latest 16 measured two-coordinate
external positions, ordered newest to oldest. These are 32 scalar inputs at
5 ms spacing, covering 75 ms ending at the external measurement's physical
support time. No neural feature values, true body positions, recruitment map,
adaptation coefficients, future task state, or future online measurements are
inputs. Arrival time cannot replace measurement support time.

Both learned fits have 32 standardized inputs, an intercept, four measured
position/velocity outputs, and 132 fitted coefficients. Both use ridge penalty
0.5 with an effectively unpenalized intercept. The external scale floor is
1 micrometre; the neural scale floor remains 0.5 microvolt because the raw units
differ. This matches the size and class of the learned linear function. It does
not make the information content, feature correlation, or effective degrees of
freedom identical. The external history is longer than the 20 ms lock-in window;
the neural features also depend on recursive filtering with earlier history.
The comparison must report these different supports rather than claim exact
temporal equivalence.

## Offline calibration and withheld assessment

The fit uses the same learner movement capture already used for the neural
decoder; it adds no measurement time. Target rows are selected using the same
external-valid and neural-valid flags as `_fit_neural`. Neural quality selects a
common offline assessment cohort and is not a learned predictor. Prior measured
external packets populate the history whether or not their neural flags are
valid. Neural quality never gates this observer online.

The chronological cut comes from that common target cohort. Rows within 100 ms
of either side of the cut are purged. Position labels are externally measured.
Velocity labels are central differences of those measured positions, followed
by the same nine-point smoothing and four-edge-row removal as the neural fit.
Labels are built separately inside retained training and validation partitions;
no validation label or measurement enters a training target or history feature.
Symmetric label construction is offline only. The online estimate is causal.

For the uninterrupted reference capture, the trained and withheld target counts
match the neural fit exactly. Missing, invalid, repeated or gapped external
histories can reduce the usable cohort. The model reports excluded history rows
and an `exact_neural_cohort_matched` flag; results with exclusions cannot be
described as identical-row comparisons. Support-time hashes identify the actual
training and withheld targets. A purge is an anti-overlap measure and does not
prove independent biological samples or eliminate long recursive neural memory.

## Online estimation and qualification

`CausalExternalHistoryDecoder` accepts only measured position, validity and
physical support/arrival timestamps. It rejects repeated or reversed support,
non-increasing arrival, nonfinite values, future support and stale transport.
An invalid packet clears history while preserving the last admitted timestamp
watermark. A gap starts a new history; missing measurements are not synthesized.
Sixteen contiguous packets are required to become ready.

After readiness, the observer computes the original nine-row linear position
and velocity estimate, then applies the same fusion rule used for the neural
fit: weight at most 0.85, learned error budget
`2 × position RMSE + 2 × maximum prediction horizon × velocity RMSE`, a
three-millimetre uncertainty floor, a standardized feature-range limit of five,
and the existing controller uncertainty ceiling. The error budget is a chosen
empirical engineering gate, not a coverage-guaranteed confidence bound. Failed
learned qualification returns the explicit external linear fallback source.

The result carries the newest external support timestamp unchanged. It does not
claim that a history-based estimate cancels the sensor's 25 ms reference age.
No biological efficacy or incremental neural information is established by the
unit tests or a low calibration residual.

## Integration contract

`fit_external_history(observations, heldout_fraction=.25)` returns a dictionary
with the same array keys (`mean`, `scale`, `weights`) and assessment keys
(`rmse`, `velocity_rmse`, `training_rows`, `heldout_rows`) as the neural fit,
along with capacity, history, cohort and provenance settings.

`CausalExternalHistoryDecoder(config, model).estimate(observation)` returns a
`HistoryEstimate` with the same fields as the existing `StateEstimate`.
`control_request` can consume this structural contract without body access.
The motor integration should fit the model from the same `obs` inside
`calibrate`, retain its assessment metadata, pass it separately to `_run_trial`,
and introduce `external_history__learner_only`,
`external_history__expert_external`, and `external_history__expert_neural` arms.
Historical defaults and saved seven-arm results must remain reproducible.

Compare retained learning, assisted performance, pulse count, estimator
qualification fraction and actual delivery status with matched expert
representations. An abstaining electrical branch cannot reveal intervention
benefit. A conditional branch remains explicitly conditional. No fit or setting
here is optimized to produce a neural advantage.

## Teacher competence qualification

The subsequent [expert validation audit](expert-validation.md) found that the
historical nominal-amplitude voluntary teacher did not satisfy the declared
25 ms task-timing threshold after the body's movement dynamics. The
[historical information comparison](information-comparison.md) preserves that
teacher and must be interpreted as
conditional controller/plasticity comparisons. A separately labeled inverse-body
synthetic teacher benchmark is proposed for a future competence-gated library
revision; it has not replaced any of the saved learning-study references.

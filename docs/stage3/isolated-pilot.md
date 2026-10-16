# Isolated practice pilot: the admission gate remains closed

12 October 2026. A new finite digital experiment consumes the resolved teacher
library, observed dynamic-response model, measured unassisted forecaster and
timed residual guard in one practice/OFF protocol. Its conservative independent
forecast context fails. Both delivery branches consequently launch **zero
profiles**. This is a completed negative admission experiment, not evidence of
an expert-informed retained-learning advantage or a functioning implant.

## Question and protocol

Can one independently justified whole-frame intervention enter a reset practice
trial without borrowing future movement, future monitor data, private learner
coefficients or a favorable private plasticity family? The experiment uses one
synthetic learner (seed 2), four three-second practice trials, then three-second
output-OFF retention and faster-cadence transfer assessments. All four arms have
matched initial coefficients, learner noise, practice duration and available
calibration resources:

| Arm | Permitted reference |
|---|---|
| Observe only | No assistance; expert resources remain explicitly unused |
| Learner goal | Known task goal, without an expert recording |
| Expert external | Qualified frozen nominal template from measured expert movement |
| Expert neural | Qualified frozen nominal template fitted from the expert's synthetic spinal features |

Each arm is repeated under favorable, zero, harmful and dependent plasticity
hypotheses. The two delivery identities are the actual electrical trace domain
and the explicitly unqualified prospective `1.012 +/- 0.074` dose assumption.
There are 32 arm/family/branch runs, 128 practice trials and 64 OFF assessments.
The live learner observer is an **external-only fallback**. This experiment
does not establish an incremental benefit from live learner neural recording.

Every trial explicitly resets position, activation, delayed drive, measurement
history, monitor session and residual guard. Learned coefficients alone carry
between practice trials. Complete washout between sessions is an assumed
modeling resource; its physical duration is not established. A declared 2%
forgetting operation precedes OFF assessments. The body is the existing
event-aligned midpoint/exact-cascade reduced model with a 2.5 ms integration
step; it is not a biomechanical or clinical model.

## Causal admission and uncertainty

The only possible launch is one whole 40 Hz frame at 1.000 s. Its decision is
fixed at 0.975 s, after receipt of the measured 0.950 s support. The target is
1.100 s: a 150 ms forecast from physical support and a 125 ms prospective
decision horizon. The packet contains 16 consecutive 5 ms measured supports
with a 25 ms arrival delay, known nominal instructions and **no past delivered
dose**. Model/context identities, exact phase and complete history are checked.
There is no uncertain old-response tail at this admission point.
The pilot's separately frozen 25 ms availability governs these recordings;
the generic motor configuration's external-delay field is not the sampler's
clock in this wrapper.

The candidate is added once to a qualified **zero-future-command** baseline.
The 25 mm correction gate contains the baseline allowance, the complete
gain/dose product interval, independent dynamic residual/label allocation and
independent reference allocation. The reference allocation is the maximum
complete-trajectory `2*RMSE` across the three independent nominal recordings:
3.116 mm for expert external and 3.120 mm for expert neural. A training-fit
residual is not substituted. The independently measured neural-template error
already covers its fitted decoder; that decoder error is not added twice.
The known learner goal has zero expert-reference allocation.

The catalogue contains zero and eight signed two-route actions. Four individual
and two mixed actions have separate inherited response domains. The two
negative-first mixed actions were not independently tested and remain
unavailable. Zero wins equal scores. The actual monitor's roughly 44.1%
charge interval is preserved. A later observed interval outside a prospective
assumption stops continuation and is recorded; it cannot undo an earlier dose.

The timed guard runs on every policy tick, including before launch. Baseline
forecasts during warmup may cancel the launch. Committed targets are scored only
after their measured support arrives. The actual delivery adapter feeds true
delivered charge only into the private body. Candidate scoring and monitor
decisions use sanitized observed data. That coupling path is exercised by
focused tests; the saved full experiment does not exercise it with an admitted
pulse because its independent baseline gate fails first.

## New independent drift check and result

A fresh twelve-second measured unassisted capture fits the forecaster. Sixteen
new three-second captures cover all four plasticity families at starting
coefficient scales 0.9, 1.0, 1.15 and 1.3. One conservative runtime context
takes the largest allowance across **every** capture; private family or
coefficient values never choose a more favorable context. Coverage is limited
to the intersection of independently tested physical supports with empty past
command prefixes. Empirical allocations are finite observed diagnostics, not
statistical confidence bounds or universal biological guarantees.

All eight 0.9/1.0 captures pass the 15 mm gate. All eight 1.15/1.3 captures fail
one or more horizons. The aggregate allowance is 15.651 mm at 25 ms and
24.964 mm at 150 ms. All 26 aggregate horizons fail the fixed 15 mm limit.
Every attempted assisted arm therefore records
`INDEPENDENT_ZERO_FUTURE_CONTEXT_UNQUALIFIED` before launch. The teacher chain is
consumed, but actual assistance and a retained advantage are **not established**.

| Plasticity hypothesis | Retention OFF trajectory RMSE | Faster transfer OFF trajectory RMSE | Assisted-arm difference from observe only |
|---|---:|---:|---:|
| Favorable | 38.152 mm | 45.122 mm | 0 |
| Zero | 38.152 mm | 45.122 mm | 0 |
| Harmful | 34.939 mm | 42.271 mm | 0 |
| Dependent | 34.939 mm | 42.271 mm | 0 |

The equality follows from zero assistance; it is not evidence that expert and
learner-goal interventions are equivalent when delivered. None of these OFF
assessments meets the inherited 18 mm spatial and 25 ms timing contact criterion.
No acquisition multiplier is estimated. The useful next mechanism question is
how to learn a drift-tolerant forecaster from permitted observations while
retaining the 15/25 mm gates, then re-test the same matched protocol. Lowering
the gate or selecting a private favorable family would not answer it.

## Inspect and reproduce

- [Saved summary](../../results/stage3/isolated-pilot/summary.json)
- [Complete measured/private-evaluator record](../../results/stage3/isolated-pilot/raw.json.gz)
- [Observed dynamic response](dynamic-response.md)
- [Zero-future-command baseline](sparse-baseline.md)
- [Resolved teacher library](resolved-teacher.md)
- [Coupling specification](dynamic-coupling-specification.md)

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:PYTHONPATH='src'
python scripts/stage3_isolated_pilot_study.py
python scripts/stage3_isolated_pilot_study.py --check results/stage3/isolated-pilot/raw.json.gz
python -m unittest discover -s tests -p test_stage3_isolated_pilot.py -v
```

The 13 focused tests cover independent reference allocation, exact causal
support/phase contracts, unavailable mixed actions, joint uncertainty, zero
ties, drift-domain intersection, actual-charge body coupling, later monitor
rejection, cancellation and output-OFF behavior. Receipts bind
normalized source hashes, canonical input JSON and exact inherited dynamic raw
bytes. Regeneration verifies that sources and inputs remain unchanged during the
run. Historical 9 October studies remain separate and unmodified.

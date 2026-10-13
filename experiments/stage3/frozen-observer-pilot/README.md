# Frozen observer pilot: finite actual-domain replay

This standalone study connects the confirmed no-dose observer to a causal,
one-shot admission policy and independent delayed-residual guard. Its approved,
predeclared experiment completed **32 practice trials and 64 hard-OFF assessments
with zero launches**. All arms produce identical measured movement and assessment
metrics. No retained advantage is established.

The primary measured-dose response domains are unqualified, and no independent
learning-enabled intervention-response interaction allocation exists. These are
separate admission failures. The experiment withheld every nonzero action. Its
combined correction intervals also exceed the unchanged 25 mm gate. A negative
result is a completed result for this finite study;
it must not be replaced with the unearned 4% monitoring target.

| Verified quantity | Result |
| --- | ---: |
| Complete practice / output-OFF sessions | 32 / 64 |
| Launched profiles, including OFF assessments | 0 |
| Sealed forecast vectors / frozen physical targets | 32 / 832 |
| Prelaunch current-target diagnostics | 32, all pass |
| Warmup / final future-target guard checks | 800 / 800, all pass |
| Supported nonzero candidates | 192, all unavailable |
| Fresh matched sensor-noise arrays | 12 |
| Scoped software contract probes | 15 pass |

The conservative admission allocation is at most **12.418841 mm / 15 mm**, the
maximum over both prior development and fresh confirmation evidence. The earlier
confirmation-only maximum remains 11.353736 mm; this replay does not replace it.
All 192 supported candidates separately fail actual response qualification,
learning-interaction qualification and the whole-vector correction-interval gate.
The two additional untested route patterns remain unavailable.

The maximum paired-grid differences are 2.838302 micrometers in position,
2.458461 micrometers in frozen forecasts and 1.546171 micrometers in trajectory
RMSE. No launch decision changes. Grid agreement supports this calculation's
numerical consistency; it is not continuum, electronic or biological validation.

## Mechanism and scope

```text
arrived external positions + known cue + common measured-data prior
  -> causal whole-prefix observer
  -> pre-dose freeze at decision 0.975 s / latest support 0.950 s
  -> 26 immutable physical targets, 0.975..1.100 s
  -> candidate response / actual-dose domain / learning-interaction gates
  -> one irreversible launch-permit resolution at 1.000 s
  -> delayed actual-position residual checks and expiry
```

All four arms share the same observation prefix, prior, state capacity and
computation schedule. They differ in their selected reference and whether the
practice policy is enabled: observe-only, known learner goal, expert external
reference and expert neural-derived reference. The last is an offline expert
representation; no qualified live learner spinal-neural increment is supplied.

The observer is sealed after the freeze. Later measured positions cannot revise
its voluntary-state estimate, forecast or selected action. The support 0.975 s
measurement becomes available at 1.000 s and is checked before launch. The other
25 targets are committed to the historical independent guard. Forecast authority
ends at physical support 1.100 s; a clean empty guard does not rearm the permit.

No active delivery path is implemented in this primary-only replay. Unexpected
nonzero authorization persists its prefix/decision and halts before delivery.
Empty monitor and pending-response ledgers therefore supply no active electronics
or biological evidence. Separate software probes exercise the existing monitor
availability/product-interval/tail-rejection interfaces only.

The two private body grids are 2.5 ms and 1.25 ms, with unchanged 5 ms measurement
and decision spacing. Twelve distinct fresh sensor-noise arrays are shared across
arms and grids for matched comparisons. Four named learning alternatives reduce
to two distinct no-dose equations; their labels do not select runtime parameters.
Assessment output is hard-OFF, learning is disabled and the same 2% forgetting
factor is applied. Complete state washout between sessions is a simulator premise.

## Evidence and verification

- [Predeclared protocol](protocol.md), [source](study.py), and
  [immutable preflight receipt](preflight.json).
- `root-review.json` records independent approval before generation.
- `raw/` contains eight complete family/grid records in deterministic gzip files.
- `summary.json` presents all outcomes and `audit.json` records the independent
  saved-data/controller audit and scoped contract probes.
- `artifact-manifest.json` binds every package artifact except itself.

Use Python 3.12.14 and the exact [dependency pins](requirements-lock.txt). From
the repository root, verification is read-only with respect to the evidence:

```text
python -m pip install -r experiments/stage3/frozen-observer-pilot/requirements-lock.txt
python -B experiments/stage3/frozen-observer-pilot/verify_study.py
```

Default verification checks package/source/input hashes, all 96 saved sessions,
all actual noise arrays, factual measurements, assessment metrics and identical
arm comparisons. It replays all 32 practice controllers from measured input,
checks causal update/seal clocks and all forecast/guard/decision records, and
runs 15 meaningful software contract probes. Numeric comparisons use 2e-8
relative and 1e-11 absolute tolerance; discrete decisions, identities, counts and
source hashes remain exact. Each floating forecast hash is checked against its
own exact payload, then forecasts are compared numerically across platforms.

Optional full reproduction regenerates the same frozen cohort in a disposable
directory. It is not another independent experiment and never rewrites the
packaged records:

```text
python -B experiments/stage3/frozen-observer-pilot/verify_study.py --reproduce
```

Historical Stage 3 sources, scripts, outcomes and the original observer package
remain unchanged. This study supplies no active assistance, retained advantage,
expert-skill transfer, learning multiplier, universal body control, target
firmware or qualified implant claim. Its one-trial practice exposure is not
equivalent to the historical four-trial pilot.

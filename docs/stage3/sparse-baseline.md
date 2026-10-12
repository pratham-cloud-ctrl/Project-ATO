# Zero-future-command baseline: frozen finite validation protocol

Original numerical protocol: 9 October 2026. Runtime scope revision: 12 October
2026. This component predicts measured motion with no additional
future command. A future candidate is excluded here and may later be added once
through the independently identified dynamic-response API. No coupled practice
or learning result is claimed by this protocol.

The specification retains 200 Hz position decisions, 40 Hz whole profiles,
nominal 35 ms private onset, a 75 ms / sixteen-row history, 150 ms maximum horizon
from the latest position support, 15 mm forecast allocation and 3 mm chosen label
allowance. A new twelve-second nominal unassisted measured recording fits the
existing forty-input known-instruction direct forecaster, with its chronological
100 ms purge. Future measured movement is an offline label only.

At the current decision, all completed past independent monitor records are
passed to the observed dynamic-response kernel. Its mean response is subtracted
from each measured history position. The unassisted forecaster predicts that
stripped history. The ongoing mean response of those same past doses is then
added at the target. No private gain, time constant, activation, body state or
future measured charge enters this calculation.

Past-response uncertainty includes `U_G d + |G| U_d + U_G U_d`. The absolute
position-history coefficients propagate stripping uncertainty through the
forecaster. Target past-response uncertainty is added separately. Shared
uncertainty is not assumed to cancel. The total must remain within 15 mm.
The actual approximately 44.1%-of-nominal monitor interval is retained.

The measured response window ends at 600 ms. Every completed past dose is
retained. A positive age beyond that window at any requested history/target
support rejects the prediction; no zero tail or washout is inferred. This rule
will reject substantial later portions of repeated sparse recordings.

## Independent validation and restricted supports

Validation reuses complete independently recorded actual-monitor trajectories
from the separately identified dynamic-response experiment. Their stimulated
positions and completed monitor records are the online view. Paired baseline
positions are excluded from that view. A separately measured unassisted baseline
trajectory is an additional independent unassisted validation recording.

Requested execution horizons are every 5 ms from 25 through 150 ms; their targets
are at or after the decision's actual availability. All rows with complete
history and warmup are considered. A row is eligible only if:

- No launched profile is awaiting its complete monitor record.
- Its known zero-command commitment extends through the target.
- No nonzero future command occurs between the decision and target.
- All past-response ages remain inside the measured 600 ms window.
- The nominal instruction and explicitly declared action family are supported.

These criteria are fixed before results and never depend on prediction error.
Every exclusion is counted by reason; all eligible rows are scored. Families
distinguish unassisted, one isolated action, individual sparse actions and mixed
sparse actions. Known faster cadence and changed subject remain unqualified
domains. An unmatched paired baseline in a validation file is excluded from the
online view and cannot be used as an oracle rejection label. The dynamic kernel's
own matched calibration remains required. Unannounced sensor-offset data test the
same observable family and may fail its measured residual gate. A derived offset
control also transforms the independently measured unassisted record at 1.5 s;
it shares that record's noise and is not another independent draw. This keeps
the fault inside a no-past-tail domain even when repeated-train late supports
are already rejected by the 600 ms rule.

For each recording/horizon the empirical residual plus chosen 3 mm allowance
and propagated past-response interval must fit 15 mm. Online qualification
retains the larger training/context residual allocation and the current interval.
Complete-recording coverage and restricted eligible coverage are reported
separately. A passing restricted interval is not pre-action candidate, feedback
controller, unseen schedule-family or population qualification.

## Finite runtime scope revision

The 12 October review found that a caller could reuse a passing context name at
a later periodic support or with a different past-action schedule. The original
recorded predictions and errors were computed only at their declared supports;
this defect did not change those results. The qualified runtime gate now binds
every horizon to its saved `eligible_domains`. Each domain contains inclusive
`support_start_s` and `support_end_s` on the 5 ms physical grid, plus the complete
sorted `observed_past_actions` prefix as `[frame_time_s, source_id, route_sign]`
triples. Ranges split at every excluded support and every action-prefix change.
Their construction occurs before target residuals are inspected.

A qualified call must match both a recorded physical support and that domain's
complete past-action prefix. A surrounding minimum/maximum interval cannot fill
coverage holes. Missing, extra, retimed or reversed actions cannot reuse a
passing context. Fractions and uncertainties remain current measured inputs;
saved monitor values never replace them. The existing live uncertainty gate
still applies. Future monitored dose and paired baseline positions remain
excluded from the online input.

For a separately validated fresh-session aggregate,
`intersect_empty_action_domains(...)` intersects the eligible physical grid
supports across all constituent recordings. It preserves holes and rejects any
nonempty past-action domain. Aggregation cannot widen the finite scope or grant
authority after a prior pulse. Session-relative clocks and independently
validated no-dose operation remain explicit prerequisites.

The regenerated receipts identify both the original 9 October protocol and
this 12 October qualification revision. Fitting, numerical predictions,
residuals, uncertainty calculations and thresholds are unchanged.

The first future body-coupled pilot may use an independently validated fresh
unassisted baseline and at most one action per explicitly separate practice
session. Its session/activation reset or washout premise must be named. Its
candidate response, teacher reference, 25 mm combined correction allocation,
frame delivery and delayed residual checks remain separate gates.

## Observed outcome

The [readable summary](../../results/stage3/sparse-baseline/summary.json) and
[compressed raw receipt](../../results/stage3/sparse-baseline/raw.json.gz) retain
two measured dynamic-response grids and fourteen validation cases per grid.
Both grids make identical horizon decisions; the largest allocation difference
is approximately `1.9e-16 m`.

| Restricted measured context | Largest forecast allocation | Outcome |
|---|---:|---|
| Independent unassisted nominal record | 9.781 mm | All 26 execution horizons pass |
| Isolated individual past action | 34.278–37.124 mm | Fails 15 mm |
| Isolated paired past action | 48.522–49.236 mm | Fails 15 mm |
| Individual sparse past actions | 52.578 mm | Fails 15 mm |
| Mixed sparse past actions | 82.811 mm | Fails 15 mm |
| Derived unassisted sensor-offset control | 47.832 mm | Fails 15 mm |

The independent unassisted record supplies 14,625 eligible row/horizon pairs
per grid. The five initial-warmup rows per horizon account for its 130 explicit
exclusions. Individual and paired isolated records each have 7,020 eligible and
7,735 excluded pairs. Repeated sparse records each have 4,212 eligible and
26,143 excluded pairs. Faster cadence and changed subject supply no eligible
rows: all 30,355 considered pairs per record are explicitly excluded. These are
restricted support counts, not percentages of validated continuous operation.

The actual uncertainty retained in the observed dynamic kernel and past-dose
monitor propagates through both history stripping and target re-addition.
That composition does not earn the 15 mm forecast allocation during assistance.
No uncertainty cancellation, shortened response window or silent tail truncation
is used to change this result. An unmatched paired-baseline label is absent from
the online inputs and therefore is not an oracle rejection criterion.

The repeated-train sensor-offset case has a 51.988 mm allocation on its earlier
eligible intervals. Its later step occurs after the old-dose age restriction
already excludes continuation; this record does not prove detection of that
late fault. The separately derived unassisted offset control keeps the fault
inside an eligible no-past-dose domain and fails its measured residual gate.

The qualified fresh unassisted context can be a prerequisite for the narrowly
specified first-action pilot. It does not grant repeated assisted baseline
prediction, a candidate response, qualified hardware or a retained-learning
result. More precise observed dynamic/dose uncertainty or an independently
validated input-aware predictor would be needed to revisit the failed assisted
composition. Extending past 600 ms also requires its own observed tail/release
qualification.

Reproduce without overwriting the saved result:

```text
python scripts/stage3_sparse_baseline_study.py --check results/stage3/sparse-baseline/raw.json.gz
```

Twelve focused tests check single counting, full uncertainty propagation,
unsupported tails, future/incomplete monitor rejection, zero commitments,
independent qualification, enlarged live monitor intervals and complete eligible
row accounting. They also reject later-period reuse, coverage holes, off-grid
supports and changed past-action prefixes, and check that fresh-domain
intersection cannot widen coverage or admit past dose. These tests establish
software/model contracts only.

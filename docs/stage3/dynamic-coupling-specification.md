# Next body-coupled motor experiment: observed dynamic response

9 October 2026. Specification only. This does not qualify a new controller,
change a saved result or establish a retained-learning benefit.

The smallest next revision is a nominal-cadence, single-subject digital pilot
using a qualified frozen teacher representation and a committed sparse action
policy. Keep the declared 35 ms private onset, 40 Hz complete profiles, 2.5 ms
body solver, 150 ms maximum forecast, 15 mm forecast allocation and 25 mm
correction allocation. Keep the actual monitor's approximately 44.1%-of-nominal
charge uncertainty and negative-authority branch. A separate prospective branch
may retain `1.012 +/- 0.074` nominal dose with
`UNQUALIFIED_NOMINAL_ASSUMPTION`; it does not qualify actual electronics.

## Runtime forecast allowance

At each horizon, let `R_train` and `R_context` be the saved maximum component
residuals, `A_train` and `A_context` their saved total allocations, and `P_live`
the current dose-interval projection through the fitted prediction weights.
The qualified componentwise allowance is:

```text
R = max(R_train, R_context) + 3 mm
A_live = max(A_train, A_context, R + P_live).
```

The maximum retains the existing finite qualification gates. It does not add
their already included maximum dose projections twice. Nonfinite allowances or
any component above 15 mm reject the forecast. An unchanged dose mean does not
qualify a newly enlarged monitor uncertainty interval. Finite instruction,
schedule-family and support guards remain required. Empirical allocations are
not universal error bounds or statistical confidence intervals.

## Independent dynamic-response qualification

1. Declare a nine-action set: each source requests one of `-1, 0, +1`, using
   whole profiles only. At most one selected action may occur per seven 40 Hz
   frames (175 ms). The planner commits to zero later actions until the current
   forecast targets and their external observations have become available.
   Processing and the wait to the first eligible 40 Hz frame remain explicit.
2. Collect new predetermined nominal-cadence recordings exercising each signed
   individual route, zero-output reference and the mixed actions across known
   task phases, including direction changes. Record independent external noise,
   physical support/availability, complete-profile monitor availability, dose
   intervals and acquisition validity. Matched zero/action capture pairs may
   supply observed incremental displacements; private body truth never supplies
   the difference, onset or qualification. State the synthetic matching premise.
3. Fit fixed-profile execution-time response kernels using these observed
   incremental displacements and monitored dose fractions. Do not divide by a
   hidden recruitment threshold or inherit the resting plateau gain as a dynamic
   gain. Estimate onset, release and uncertainty from observed records. Reserve
   complete new captures, pulse patterns and phases for independent tests at
   every requested horizon. Mixed-action additivity must earn its own check;
   failed mixed actions remain unavailable rather than borrowing individual
   route qualification. Sparse-family empirical admission must be declared
   separately from an exact-recording fingerprint.
4. Qualify the observer on complete withheld recordings from that same sparse
   family. A dense-train or unassisted-context pass does not substitute for this
   check. Record failures under changed response, instruction or sensor context.
   Keep an online delayed-residual latch: targets become checkable only when
   their measured support arrives, and rejection cannot undo an earlier pulse.

## Avoid counting a candidate intervention twice

Forecast the baseline with **zero future commands**, retaining every already
delivered past dose and its ongoing observed-state effect. Add the independently
identified candidate's dynamic response at the execution target. Its uncertainty
must contain the complete product allowance:

```text
candidate state = zero-future baseline + G_h u
candidate allowance = A_live + U_G,h |u| + |G_h| U_u + U_G,h U_u.
```

Each term must refer to the same tested dynamic profile, route and horizon. The
candidate allowance must fit 25 mm. Do not predict a full candidate's future
intervention with the observer and then apply that same intervention again
through `G_h`. A direct full-candidate forecast can be retained as an independent
diagnostic, but these are alternative calculation paths.

## Small coupled practice and OFF study

After those gates, launch the selected whole action on its exact frame into the
digital body, then ingest new acquisition, external and monitor evidence on their
actual clocks. Freeze the action score, zero-action/tie rule and cancellation
rules before obtaining practice outcomes. Invalid, stale, replayed, unsupported
or excessive-residual observations cancel continuation; bounded-residual neural
packets remain invalid. External fallback is labeled explicitly. Use the final
teacher library's qualified nominal reference and its actual source-model scope;
an unqualified teacher or aperture-resolved domain remains unavailable.

A bounded first cohort can use seed 2, four three-second practice blocks and
three-second output-OFF retention/transfer assessments. Compare no assistance,
known learner goal, expert-external reference and expert-neural reference with
equal declared learner/expert calibration resources. Retain favorable, zero,
harmful and dependent plasticity families. Faster-cadence transfer is an OFF
assessment; it does not authorize faster-cadence assisted teacher templates.
Separate current-implementation and prospective-delivery result identities.

The standalone `DelayedResidualGuard` is now implemented and has eight focused
tests for target arrival, missing/future/replayed observations, sticky failure,
cancellation, timed total-sensor-loss expiry and bounded pending work. Its
`check(now_s=...)` must run on the policy clock before each continuation/launch,
even when no observation arrives; the cached latch flag alone is insufficient.
It scores only already arrived measured
targets and supplies no forecast/domain admission or pulse launch. The
[12 October isolated pilot](isolated-pilot.md) now integrates this guard with
the actual body/delivery path. Its independent baseline gate rejects every
practice intervention. Focused coupling tests exercise an admitted pulse and
cancellation separately; the saved full pilot does not demonstrate a delivered
assistance effect.

Record every actual launch, source/route, prospective interval, later monitor,
forecast target, observed residual and cancellation. No admitted action, no
retained benefit or a harmful result are valid outcomes. New body-coupled
results, rather than a scheduling replay, determine the next design requirement.

# Teacher references from complete contact-aperture recordings

9 October 2026. This new capture revision applies the
[moving-source study's decision](source-sensitivity.md): source position and
physical velocity are evaluated at each actual electrode sample rather than
held for 5 ms. It keeps the original task, competence thresholds, observer
allocation and independent teacher validation gates.

## New observations and qualification

Sixteen 12-second recordings cover two synthetic generators, nominal 1 Hz and
1.15 Hz cadences, and four observation-noise realizations. There is one artificial
expert subject/contact geometry. Each generator contributes 96 seconds: 12 seconds
for reference/decoder training and 84 seconds of withheld cadence/noise exposure.
This is not seven independently sampled people. External and neural alternatives
have equal measured capture exposure.

External template fitting uses its fixed measured post-warmup partition and does
not require a working neural decoder. Unavailable or malformed neural capture
rejects the neural reference without removing a competent external comparator.
Complete duration, clock/support and independent-recording gates apply to both.

The inverse-model generator uses a private movement time constant to synthesize
a competent performer. That is a disclosed generator privilege; the library fits
only measured voltage features and external positions. Its nominal training
capture is fixed before qualification. Independent performances and cadence are
not refitted when they fail.

| Generator | Cadence | Observed task competence | External reference | Neural reference |
|---|---:|---:|---|---|
| Original voluntary template | 1 Hz | 0/4 | Unavailable | Unavailable |
| Original voluntary template | 1.15 Hz | 0/4 | Unavailable | Unavailable |
| Separate inverse-model teacher | 1 Hz | 4/4 | Qualified in tested synthetic domain | Qualified in tested synthetic domain |
| Separate inverse-model teacher | 1.15 Hz | 4/4 | Unavailable | Unavailable |

Competence and reference fidelity are separate gates. The faster inverse teacher
passes the contact-peak task criteria but retains finite direction-change
transients. Its frozen static representation exceeds the whole-trajectory
allocation; the neural alternative has additional decoder/task limits. These
references remain unavailable instead of inheriting nominal admission.

A 0.625 ms independent integration comparison against the 2.5 ms nominal
reference checks one inverse-teacher recording. The separate source-sensitivity
study adds six moving/assisted grid comparisons. Neither is a universal numerical
proof for arbitrary future feedback policies.

## Consumer and evidence boundary

The library supplies an expert-informed task representation to a learner-specific
policy. It does not copy electrode voltages into another person. Neural references
use measured expert external labels during fitting, so neural incremental value
still requires a matched external-teacher comparison.

The protocol identity binds exact source/settings/recording identities. Full
numeric observations and fit parameters are checked with stated tolerances;
platform-dependent floating byte hashes are not used as regenerated identities.
Raw noise hashes remain within-host diagnostics and paired-noise equality is
enforced during each experiment.

This revision does not deliver learner stimulation or establish retained
learning, human signal observability, generalization between subjects, a chronic
contact arrangement or implant readiness. Earlier teacher/library/learning
results remain unchanged. The broader
[library API and resource contract](teacher-library.md) applies, with this
revision's source limits and new IDs.

Review the [raw recordings and libraries](../../results/stage3/resolved-teacher/raw.json.gz)
and [readable qualification record](../../results/stage3/resolved-teacher/summary.json).
Recompute with:

```text
python scripts/stage3_resolved_teacher_study.py --check
```

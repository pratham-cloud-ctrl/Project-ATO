# Moving spinal sources at the actual acquisition apertures

9 October 2026. A new finite synthetic study resolves a limitation of the earlier
5 ms held-source captures. It does not establish that real spinal contacts encode
the chosen movement coordinates.

## Experiment

Two artificial subjects use an independent event-split DOP853 solution of the
12-state movement, activation and selected favorable plasticity equations. The
reference is evaluated at all 20 samples on each of 16 contacts in every 5 ms
block, including the 3 microsecond contact skew. Internal maximum steps of
2.5 ms and 0.625 ms are compared at the physical apertures. Acquisition and
decision rates remain fixed: refinement grants no additional observations.

Three voltage-source approximations are paired: the historical held position
and preceding-block mean velocity; held instantaneous position/velocity; and
the complete moving source at each aperture. Clean, quarter-density and dense
40 Hz patterns are tested under informative, externally redundant and absent
source hypotheses. Calibration uses separate observation noise and only measured
features/positions. The same artificial trajectories are reused to isolate source
approximation; this is not an independent task or subject generalization test.

There are **75 captures**, including six calibration captures, 54 main captures,
three fine-reference captures, ten fault captures and a two-capture ambiguity
witness. They contain **14,399,360 acquired contact samples**. Actual paired
noise draws, generator states, external noise and observation clocks are checked.
Fine-reference external positions may differ within the predeclared 150 micrometre
reference budget; their clocks and noise must still match exactly. Ordinary
paired source comparisons require exactly identical external observations.

## Results

| Check | Observed result | Decision |
|---|---:|---|
| Six reference-grid comparisons, maximum position difference | 1.02e-15 m | Within the 150 micrometre allocation in these cases |
| Maximum physical velocity difference | 1.75e-14 m/s | Within the 0.01 m/s allocation |
| Informative source-pair feature difference | Up to 15.889 microvolts | 12 of 18 informative comparisons exceed 2.4 microvolts |
| Position-prediction difference from source approximation | Up to 3.707 mm | Six informative comparisons exceed 1.5 mm |
| Externally redundant and absent source feature differences | Exactly zero | Negative controls retained |
| Dense-stimulation active-window qualified packets | Zero | Digital artifact-residual failure retained |
| Changed packet-quality flags between source approximations | Zero | An unchanged validity flag does not certify source fidelity |
| Deliberately ambiguous contact field | 441 conflicting valid observed-label pairs | Abstain for the 25 mm target |

The ambiguity witness gives two different foot trajectories the same recorded
features through a deliberately rank-deficient lead field and identical noise.
The largest observed contradiction forces at least **66.77 mm** component error
for one of the pair. External observations expose this conflict. The witness is
neither a biological impossibility proof nor a detector for every unseen ambiguity.

Selected faults include 100/120 microsecond clock uncertainty, a lost 5 ms block,
changed source geometry and a nonaligned 37.37 ms onset. The lost block consumes
the same physical noise draws and resets recursive history with nonzero prior
uncertainty. A 120 microsecond clock allocation rejects all packets; dense
stimulation does not become valid merely because the source is integrated finely.

## Design consequence

New synthetic neural captures use the **aperture-resolved source**, followed by
fresh measured qualification. Historical recordings remain unchanged and retain
their failed fidelity qualification. The separately generated
[resolved teacher library](resolved-teacher.md) implements this decision.
Fine ODE agreement cannot repair absent information, a noninjective field or
unknown analog amplifier recovery.

The [raw receipt](../../results/stage3/source-sensitivity/raw.json.gz) retains
packets, predictions, noise witnesses and failed cases. The
[readable summary](../../results/stage3/source-sensitivity/summary.json) records
every comparison. Recompute without overwriting them:

```text
python scripts/stage3_source_sensitivity.py --jobs 2 --check results/stage3/source-sensitivity/raw.json.gz --summary-check results/stage3/source-sensitivity/summary.json
```

Numerical reproduction uses relative tolerance 2e-8 and absolute 1e-11. Raw noise
byte hashes and adaptive solver evaluation counts are platform diagnostics;
within each execution paired noise/support equality is enforced exactly.

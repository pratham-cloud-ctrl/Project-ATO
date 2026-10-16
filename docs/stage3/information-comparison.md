# Observable-input comparison

This batch compares the original linear external observer, the neural/external fusion observer,
and a learned external-history observer with the same number and class of learned coefficients.
It retains the full SCCI chain and expert-informed motor-learning question. A strong external
comparator helps identify what the implanted observations contribute in these chosen models;
it does not determine what real spinal recordings can contain.

## Frozen experiment

There are 7 studies and 280 plasticity/arm rows.
Six studies cross informative, externally redundant and absent synthetic source hypotheses with
seeds 0 and 1. They assume fast 5 ms biological onset and nominal delivery with unqualified dose
uncertainty. One informative seed-0 study retains nominal 35 ms onset and the actual electrical
monitor/qualification model. Each study has four plasticity families and ten arms, 12 s movement
calibration, equal route/withheld calibration, four 3 s practice blocks and 3 s OFF assessments.
Both sensors retain their original schedules. Body integration is the midpoint exact cascade
at 2.5 ms; acquisition uses bounded digital filter residuals and 20 microsecond clock allowance.
The residual bounds concern a range-bounded digital counterfactual, not amplifier recovery.

Both learned observers have 32 inputs and 132 coefficients, ridge penalty 0.5, the same offline
calibration target cohort and partition-local measured labels. The external history spans 75 ms;
the neural lock-in window is 20 ms with recursive earlier history. Parameter count matching
does not establish identical information content or effective statistical capacity.

## Fit residuals and independent online scoring

Offline position fit uses measured external labels; a history model can copy some newest
measurement noise. The online evaluator separately scores private body position and the
declared 5 ms body velocity at exactly the estimator’s physical external support. That truth
never enters identification, decoding or policy. Scores use each arm’s valid packets; differing
warmup/fallback masks mean the evaluated packet populations are not identical. Counts are saved.

| Study | Neural fit position mm | External-history fit position mm | Same train / withheld rows |
|---|---:|---:|---:|
| conditional_fast_informative_seed0 | 2.6441 | 0.2946 | 1757 / 568 |
| conditional_fast_informative_seed1 | 2.9867 | 0.2741 | 1757 / 568 |
| conditional_fast_redundant_seed0 | 3.1740 | 0.2946 | 1757 / 568 |
| conditional_fast_redundant_seed1 | 3.9156 | 0.2741 | 1757 / 568 |
| conditional_fast_absent_seed0 | 47.4044 | 0.2946 | 1757 / 568 |
| conditional_fast_absent_seed1 | 47.8135 | 0.2741 | 1757 / 568 |
| actual_nominal_informative_seed0 | 2.6441 | 0.2946 | 1757 / 568 |

The next table uses first-practice-block same-support body scoring with the declared learner goal.
All sources and delivery assumptions stay separate. Neural use and learned-history use are
fractions of the complete 600-packet block; a fallback remains an external observation.

| Study | Observer | Body position RMSE mm | Body velocity RMSE m/s | Valid packets | Neural / learned-history use | Practice pulses |
|---|---|---:|---:|---:|---:|---:|
| conditional_fast_informative_seed0 | external | 1.162 | 0.11312 | 598/600 | 0.000 / 0.000 | 34 |
| conditional_fast_informative_seed0 | neural_external | 1.385 | 0.11396 | 598/600 | 0.093 / 0.000 | 30 |
| conditional_fast_informative_seed0 | external_history | 1.329 | 0.25677 | 585/600 | 0.000 / 0.975 | 37 |
| conditional_fast_informative_seed1 | external | 1.107 | 0.10021 | 598/600 | 0.000 / 0.000 | 26 |
| conditional_fast_informative_seed1 | neural_external | 1.547 | 0.09163 | 598/600 | 0.243 / 0.000 | 22 |
| conditional_fast_informative_seed1 | external_history | 1.257 | 0.18958 | 585/600 | 0.000 / 0.975 | 20 |
| conditional_fast_redundant_seed0 | external | 1.162 | 0.11312 | 598/600 | 0.000 / 0.000 | 34 |
| conditional_fast_redundant_seed0 | neural_external | 1.162 | 0.11312 | 598/600 | 0.000 / 0.000 | 34 |
| conditional_fast_redundant_seed0 | external_history | 1.329 | 0.25677 | 585/600 | 0.000 / 0.975 | 37 |
| conditional_fast_redundant_seed1 | external | 1.107 | 0.10021 | 598/600 | 0.000 / 0.000 | 26 |
| conditional_fast_redundant_seed1 | neural_external | 1.107 | 0.10021 | 598/600 | 0.000 / 0.000 | 26 |
| conditional_fast_redundant_seed1 | external_history | 1.257 | 0.18958 | 585/600 | 0.000 / 0.975 | 20 |
| conditional_fast_absent_seed0 | external | 1.162 | 0.11312 | 598/600 | 0.000 / 0.000 | 34 |
| conditional_fast_absent_seed0 | neural_external | 1.162 | 0.11312 | 598/600 | 0.000 / 0.000 | 34 |
| conditional_fast_absent_seed0 | external_history | 1.329 | 0.25677 | 585/600 | 0.000 / 0.975 | 37 |
| conditional_fast_absent_seed1 | external | 1.107 | 0.10021 | 598/600 | 0.000 / 0.000 | 26 |
| conditional_fast_absent_seed1 | neural_external | 1.107 | 0.10021 | 598/600 | 0.000 / 0.000 | 26 |
| conditional_fast_absent_seed1 | external_history | 1.257 | 0.18958 | 585/600 | 0.000 / 0.975 | 20 |
| actual_nominal_informative_seed0 | external | 0.978 | 0.06705 | 598/600 | 0.000 / 0.000 | 0 |
| actual_nominal_informative_seed0 | neural_external | 1.861 | 0.04037 | 598/600 | 0.968 / 0.000 | 0 |
| actual_nominal_informative_seed0 | external_history | 1.141 | 0.04014 | 585/600 | 0.000 / 0.975 | 0 |

## Retained learning contrasts

Each entry below is neural-fusion OFF contact-spatial RMSE minus learned-external-history OFF
contact-spatial RMSE, in millimetres, with the same expert representation. Negative values
favor neural fusion within this model. Better assisted motion alone is not retained learning.

| Study | Plasticity | Declared goal | Expert external | Expert neural |
|---|---|---:|---:|---:|
| conditional_fast_informative_seed0 | favorable | +0.0138 | +0.4646 | +0.2234 |
| conditional_fast_informative_seed0 | zero | +0.0000 | +0.0000 | +0.0000 |
| conditional_fast_informative_seed0 | harmful | +0.1948 | -0.7157 | -0.6556 |
| conditional_fast_informative_seed0 | dependent | +0.0529 | -0.7620 | -0.7698 |
| conditional_fast_informative_seed1 | favorable | +0.0020 | +0.0436 | +0.0785 |
| conditional_fast_informative_seed1 | zero | +0.0000 | +0.0000 | +0.0000 |
| conditional_fast_informative_seed1 | harmful | +0.0927 | -0.1815 | +0.0542 |
| conditional_fast_informative_seed1 | dependent | +0.0583 | -0.0016 | -0.2277 |
| conditional_fast_redundant_seed0 | favorable | -0.0178 | +0.3813 | +0.4452 |
| conditional_fast_redundant_seed0 | zero | +0.0000 | +0.0000 | +0.0000 |
| conditional_fast_redundant_seed0 | harmful | +0.2079 | -0.5164 | -0.6103 |
| conditional_fast_redundant_seed0 | dependent | +0.0376 | -0.8246 | -0.6440 |
| conditional_fast_redundant_seed1 | favorable | +0.0488 | -0.0329 | -0.1333 |
| conditional_fast_redundant_seed1 | zero | +0.0000 | +0.0000 | +0.0000 |
| conditional_fast_redundant_seed1 | harmful | +0.2992 | +0.2704 | -0.1972 |
| conditional_fast_redundant_seed1 | dependent | +0.3647 | +0.3213 | -0.1135 |
| conditional_fast_absent_seed0 | favorable | -0.0178 | +0.3813 | +0.0000 |
| conditional_fast_absent_seed0 | zero | +0.0000 | +0.0000 | +0.0000 |
| conditional_fast_absent_seed0 | harmful | +0.2079 | -0.5164 | +0.0000 |
| conditional_fast_absent_seed0 | dependent | +0.0376 | -0.8246 | +0.0000 |
| conditional_fast_absent_seed1 | favorable | +0.0488 | -0.0329 | +0.0000 |
| conditional_fast_absent_seed1 | zero | +0.0000 | +0.0000 | +0.0000 |
| conditional_fast_absent_seed1 | harmful | +0.2992 | +0.2704 | +0.0000 |
| conditional_fast_absent_seed1 | dependent | +0.3647 | +0.3213 | +0.0000 |
| actual_nominal_informative_seed0 | favorable | +0.0000 | +0.0000 | +0.0000 |
| actual_nominal_informative_seed0 | zero | +0.0000 | +0.0000 | +0.0000 |
| actual_nominal_informative_seed0 | harmful | +0.0000 | +0.0000 | +0.0000 |
| actual_nominal_informative_seed0 | dependent | +0.0000 | +0.0000 | +0.0000 |

280/280 acquisition-threshold rows are censored after 12 s practice.
No acquisition-speed multiplier is estimated from censored rows. Every retained and transfer
assessment had zero output pulses; the idealized washout/body reset and chosen 2% forgetting
remain explicit model assumptions rather than timed withdrawal or long-term human retention.

The actual-electrical branch must be interpreted using its observed authority margin and
admission reasons. A failure to deliver qualified intervention cannot establish the absence
of useful spinal information. Conditional branches assume delivery and unusually fast onset;
their outcomes do not repair the measured monitor precision or nominal timing limitations.

6 separate seed-0 informative negative-control witnesses are retained.
Their shuffled expert, incorrect response map, stale external input, prolonged artifacts,
saturation and source drift dispositions appear in the readable receipt and raw files.

## Reproduction and boundaries

The adjacent JSON receipt preserves every arm’s block metrics, calibration quantities, expert
qualification, contrasts, OFF scores, censoring and faults. Separate raw gzip files preserve
the full study objects and available practice/retention/transfer/fault traces. Input-source
hashes and raw hashes make the mechanism revision traceable.

`python scripts/stage3_information_comparison.py --check --jobs 2` reproduces the seven studies
with relative tolerance 2e-8 and absolute tolerance 1e-11. `--resume` reuses source-matched
finished studies after an interruption. This batch does not validate real intradural signal
content, chronic implants, biomechanics, clinical efficacy or consumer accelerated learning.

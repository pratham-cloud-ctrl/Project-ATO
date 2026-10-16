# Expert competence and independent performance audit

The earlier expert generator set voluntary coefficients equal to the desired sinusoid’s
amplitude. The reduced body still has a 60 ms movement time constant, so a desired voluntary
waveform does not establish expert-level task execution. Teacher competence must be assessed
from observed task performance before its recordings can support an expert-to-novice claim.

The existing [280-row information comparison](information-comparison.md) is preserved. Its teacher references are
**unqualified for the full timing criterion**; its results remain conditional controller/
plasticity comparisons rather than validated expert-to-novice skill acquisition.

## Separate synthetic benchmark

A proposed replacement generator uses the inverse of the declared private expert body law:
`voluntary = desired position + movement time constant × desired velocity`.
For a sinusoid, its voluntary sin/cos coefficients are `[A, A τ ω]`. The generator uses the
private movement time constant solely to construct an idealized synthetic skill. This is an
explicit generator privilege, not a learned real expert, and no controller receives that
time constant, voluntary coefficients or private body state. Direction-change transients
remain; no impulse or instantaneous body jump is inserted to force competence.

Both generators receive four independent voltage/external observation-noise realizations
of one synthetic subject/geometry at 1 Hz and four at 1.15 Hz. Body integration is midpoint
exact cascade at 2.5 ms while decisions remain 5 ms. Each capture is 12 s. Voltage acquisition
has 16 contacts at 4 kHz; physical aperture times and 20 ms external delay are preserved.
The acquisition source is the body state at block start, advanced only after its 5 ms block.

## Qualification using measured external records

The same task metric and fixed 18 mm spatial / 25 ms timing thresholds apply to both
generators and both cadences. Noise, thresholds and outcomes are not adjusted to make the
new benchmark pass. The body-truth diagnostics are kept separately and never qualify a teacher.

| Generator | Cadence Hz | Performance | Observed spatial RMSE mm | Observed timing RMSE ms | Qualified |
|---|---:|---:|---:|---:|---|
| legacy_voluntary | 1.00 | 51000 | 4.578 | 61.113 | False |
| legacy_voluntary | 1.00 | 61007 | 4.453 | 54.404 | False |
| legacy_voluntary | 1.00 | 71014 | 4.444 | 57.218 | False |
| legacy_voluntary | 1.00 | 81021 | 4.135 | 60.253 | False |
| legacy_voluntary | 1.15 | 51000 | 6.744 | 59.473 | False |
| legacy_voluntary | 1.15 | 61007 | 6.323 | 54.967 | False |
| legacy_voluntary | 1.15 | 71014 | 6.597 | 59.228 | False |
| legacy_voluntary | 1.15 | 81021 | 6.343 | 57.577 | False |
| idealized_inverse | 1.00 | 51000 | 2.065 | 14.818 | True |
| idealized_inverse | 1.00 | 61007 | 1.997 | 13.392 | True |
| idealized_inverse | 1.00 | 71014 | 2.008 | 11.841 | True |
| idealized_inverse | 1.00 | 81021 | 1.877 | 17.004 | True |
| idealized_inverse | 1.15 | 51000 | 1.923 | 12.806 | True |
| idealized_inverse | 1.15 | 61007 | 2.160 | 11.949 | True |
| idealized_inverse | 1.15 | 71014 | 2.029 | 13.350 | True |
| idealized_inverse | 1.15 | 81021 | 2.554 | 9.985 | True |

## Frozen decoder transfer

Each decoder is fitted only on its generator’s nominal performance0 capture with the
existing purged chronological split and externally measured position/differentiated labels.
Other nominal performances have distinct observation noise. Every faster-cadence capture
is withheld from this fit. Contact geometry stays fixed: this tests performance/noise/cadence
transfer within one artificial subject, not transfer between people or changed electrodes.

| Generator | Cadence Hz | Performance | Independent position RMSE mm | Velocity RMSE m/s | Rows |
|---|---:|---:|---:|---:|---:|
| legacy_voluntary | 1.00 | 61007 | 2.452 | 0.04318 | 2373 |
| legacy_voluntary | 1.00 | 71014 | 2.429 | 0.04489 | 2373 |
| legacy_voluntary | 1.00 | 81021 | 2.342 | 0.04495 | 2373 |
| legacy_voluntary | 1.15 | 51000 | 2.328 | 0.08532 | 2373 |
| legacy_voluntary | 1.15 | 61007 | 2.519 | 0.08685 | 2373 |
| legacy_voluntary | 1.15 | 71014 | 2.427 | 0.08717 | 2373 |
| legacy_voluntary | 1.15 | 81021 | 2.380 | 0.08506 | 2373 |
| idealized_inverse | 1.00 | 61007 | 2.471 | 0.05954 | 2373 |
| idealized_inverse | 1.00 | 71014 | 2.434 | 0.06080 | 2373 |
| idealized_inverse | 1.00 | 81021 | 2.356 | 0.05914 | 2373 |
| idealized_inverse | 1.15 | 51000 | 2.331 | 0.09061 | 2373 |
| idealized_inverse | 1.15 | 61007 | 2.513 | 0.09327 | 2373 |
| idealized_inverse | 1.15 | 71014 | 2.435 | 0.09175 | 2373 |
| idealized_inverse | 1.15 | 81021 | 2.378 | 0.09028 | 2373 |

Transfer residuals are observations, not automatic decoder qualification. The original
same-task fit gate is an empirical residual allocation; a revised expert library must admit
only task-competent observed references and qualify its decoded representation against
independent performance/cadence evidence. An unavailable teacher remains unavailable.

## Provenance and next revision

Raw gzip files retain Observation packets, external records, separate private generation
diagnostics and first/last voltage blocks. Every chronological synthetic prefilter voltage
aperture is hashed by a forwarding-only witness that does not change filter arguments/results.
Source hashes, subject/noise identities and acquisition counts are saved in the receipt.

This audit does not modify `motor.py`, the historical expert library or the saved information
comparison. Integrating a competence-gated teacher is a separate mechanism revision that
must receive new results. It does not retrospectively turn older conditional differences
into evidence for expert-to-novice learning, nor establish real spinal skill-transfer biology.

`python scripts/stage3_expert_validation.py --check` reproduces the captures and comparisons
with relative tolerance 2e-8 and absolute tolerance 1e-11. Raw voltage hashes are within-host
witnesses; numerical recorded arrays are the cross-platform comparison authority.

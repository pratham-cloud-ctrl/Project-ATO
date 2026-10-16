# Stage 6 integrated digital replay

The [methods and limits](../../docs/stage6/integration-verification.md) describe
the finite integration experiment. The unchanged C runtime is compiled and
called from two explicitly conditional companion/response adapters. Existing
Stage 3 calibration/learning functions, pressure packet encoding, independent
supervisor state equations and the Stage 5 protected port map are reused.

Run from the repository root:

```text
python scripts/stage6/verify_digital_path.py
```

Results are [summarized here](../../results/stage6/integration-summary.json) and
[recorded in detail](../../results/stage6/digital-path-verification.json).
`--write-results` regenerates only these Stage 6 files; default is read-only.
Python, NumPy and a C11 compiler are required. C code compiles with warnings
treated as errors. No target, physical or biological execution is implied.

The target's RHD telemetry works in OBSERVE and is invalid while stimulation is
armed. Live signed spinal phase features in the motor replay are therefore a
conditional companion adapter, not an implemented target decoder. The assumed
current-to-recruitment law, teaching coefficient and pressure response are
displayed as premises. Neutral/adverse OFF learning and pressure withdrawal
overshoot are retained alongside favorable illustrative results.

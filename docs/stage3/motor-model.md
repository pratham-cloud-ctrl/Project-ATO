# Motor mechanism model: observable expert-informed assistance and retained learning

This package implements the proposed spinal recording → interpretation → learner-specific stimulation → feedback chain as a **conditional digital mechanism study**. It uses Stage 2's 16 recording streams at 4 kHz, 200 Hz decisions and two 40 Hz fixed stimulation profiles. It does not demonstrate a functioning implant, human spinal decoding, electrode selectivity, accelerated learning or a finished predictive cadence controller.

The selected task is paced alternating foot placement with nominal 500 ms events and instructed direction changes every two seconds. Foot position is a kinematic proxy; the model has no ground reaction forces, anatomy, muscle mechanics or physical contact detector. All neural encoding, electrode mixing, recruitment and plasticity parameters are declared synthetic assumptions. The model is intended to expose what the proposed mechanism requires and where it fails.

## State, observations and information permissions

`_World` owns hidden skill coefficients, body position/velocity, recruitment matrix and activation. Only the acquisition boundary can read these quantities to generate synthetic contact voltages. The controller receives `Observation`, `StateEstimate`, a fitted `LearnerMap`, a frozen `ExpertRepresentation` and the known task instructions. It receives neither hidden skill/recruitment nor actual phase charge. Actual delivered charge enters only the body/evaluator; the calibration/controller sees a sanitized independent monitor record and its uncertainty.

At simulation step start `t`, the source state `x(t), v(t)` is held constant across the next 5 ms contact sampling block. Carrier phase varies at every actual aperture. The body advances after this block; its future state is never backdated into earlier sample apertures. For 20 samples/stream, stream `j` has timestamps `t + k/4000 + 3j μs`. The last contact aperture is `t + 4.795 ms`, and packet availability is `t + 5 ms`. The latest external position has support `t − 20 ms`, giving 25 ms age at decision time. This source discretization is a declared approximation; the electrical pulse model separately resolves microsecond timing. A motor time-step convergence study remains open.

External and neural observation timestamps are physical support times rather than arrival-time replacements. Future/nonfinite/reversed external support is rejected. Repeated packets do not create new measurements. Neural fusion also requires its original support to remain within 5 ms of current consumption; replaying an old valid feature packet cannot refresh it.

## Synthetic spinal population and acquisition

The four normalized population envelopes are position and velocity for two feet. A private seeded 16×4 mixing matrix and channel carrier phases produce contact signals:

`V_j(t) = [b_j + 18 μV · (L z)_j] cos(2π · 80 Hz · t_j + φ_j) + reference + noise + artifact`.

The coherent 80 Hz modulation is a deliberately favorable **unverified encoding hypothesis**, not a claim about intradural spinal recordings. The decoder is fitted to measured voltages and external labels; it never reads `L`, `φ`, `z` or the hidden plant coefficients. `source_mode="redundant"` substitutes the same delayed external position into the source encoding; `"absent"` removes informative population envelopes. These are structural negative controls, not measured biological cases.

The persistent filter contains a first-order 0.1 Hz high-pass and third-order 300 Hz low-pass. White Gaussian pre-filter noise is scaled by the filter's stationary frequency-response energy so the filtered input-referred RMS matches the chosen 2.4 μV noise allocation; shared reference noise uses the same scaling. This is a spectral assumption, not measured RHD2216 amplifier noise. Samples are quantized at 0.195 μV/LSB with the chosen ±5 mV linear range.

Pregated/clipped samples are zero-filled inside the filter and retain invalid flags. Zero filling does not erase recursive filter history. Two distinct checks are enforced:

- At least 90% usable samples in the trailing 20 ms window, with the latest usable raw sample no older than 5 ms.
- A separate chosen 100 ms uninterrupted channel history after any invalid input, plus initial 100 ms warmup.

The 100 ms history duration is **not measured analog settling, an error bound for the 0.1 Hz recursive state, or proof of an implant's recovery**. All numerical feature validity remains conditional on that assumed recovery model. At uninterrupted 40 Hz stimulation, raw 20 ms coverage can exceed 90% while this history check never qualifies neural decoding. Pulse-density gaps can sometimes earn conditional eligibility. Missing acquisition intervals reset history and require a new warmup.

The 32 features are trailing, valid-sample means of voltage times cosine/sine at the declared carrier. Aperture-aware weighted support and mask/saturation counts accompany every feature record. Stateful vectorized buffers preserve every 4 kHz sample; they do not lower the acquisition rate.

## Calibration, separate expert data and decoder validation

Every condition receives the same finite calibration exposure: 12 s of observed learner movement by default, 8 s of individual positive/negative route probes, and 4 s of separately captured withheld mixed-route probes. No evaluation trajectory labels or simulator coefficients train the decoder or response map.

The local neural decoder predicts delayed external position and offline differentiated external position from 32 voltage-derived features using a regularized linear fit. Training and chronological validation have a 100 ms purge on both sides of the split. Differentiation and symmetric smoothing are performed independently inside each retained partition, and label-edge rows are excluded. This prevents feature overlap and symmetric label support from crossing the split. Offline central differences are allowed only during calibration; online estimation is causal.

The external estimator uses a trailing regression through up to nine external observations. Neural fusion uses the **same external stream and physical output support**, with no imposed neural latency advantage. Fusion requires a qualified packet, bounded standardized features and held-out position/velocity residual budgets. Comparing informative, redundant and absent encodings is necessary: differences can arise from feature processing or smoothing, and a synthetic advantage alone does not establish additional biological information. The baseline does not yet implement an equally complex learned external-history decoder; that capacity-matched comparison remains open.

The expert is a separate synthetic subject with its own contact mixing and external-labeled decoder. The frozen library contains:

| Representation | Transferred object | Evidence source |
|---|---|---|
| `learner_only` | Declared task interpolation | No expert recording |
| `expert_external` | Four task-coordinate coefficients per foot | Offline expert external trajectories |
| `expert_neural` | Four task-coordinate coefficients per foot | Offline expert voltage features decoded using expert external labels |

Electrode voltages are never copied from expert to learner. If a usable expert neural decoder is unavailable, `expert_neural` is marked unqualified and its policy abstains; external data is never silently relabeled as neural evidence. Expert-neural and expert-external representations need not produce the same behavior, and neither is assumed superior.

## Empirical learner response and uncertainty

Individual route probes fit a two-by-two **effective response at the tested fixed profile**:

`G[:,j] = mean_sign [sign · observed steady displacement / observed reference dose fraction]`.

The hidden recruitment threshold is **not** supplied to this normalization. The resulting map includes threshold and recruitment effects empirically. It does not identify their separate values or authorize extrapolation to different amplitudes, phase widths, anatomical sites or postures.

Position uncertainty and independent charge uncertainty propagate into the gain uncertainty entries. Qualification requires consistent observed route signs, condition number below 10, positive smallest-singular-value margin after subtracting the gain uncertainty norm, onset plus twice its uncertainty within 100 ms, and withheld mixed-route response error below the chosen 25 mm diagnostic budget. These are engineering allocations, not statistically calibrated confidence intervals or clinical qualification criteria. The mixed-route capture is not used to fit the gain. Individual positive/negative route consistency is reported separately as `route_consistency_rmse_m`; it is not mislabeled held-out validation.

Current default electrical integration reports roughly 44% charge uncertainty for the 3 mA, 200 μs profile under the declared complete-waveform 25 mA peak bound. A small withheld response error cannot remove that uncertainty. The observed gain map can consequently fail its authority margin and abstain. Repeated bounded measurements are not treated as if their systematic worst-case error vanishes through averaging.

## Observable policy and delivery

The policy predicts from measured position and causal velocity through:

`h = observation support age + 11.85 ms pipeline + fitted onset + 2 · onset uncertainty`.

It abstains if `h > 100 ms`, if the state/map/reference is unqualified, or if input values are nonfinite/future-dated. The desired task-coordinate trajectory comes from the selected frozen representation and known cue schedule. Regularized local inversion requests a bounded signed response fraction:

`u = clip[(GᵀG + 10⁻⁴I)⁻¹ Gᵀ (reference − predicted position), −1, 1]`.

Gain uncertainty times the bounded request, plus state uncertainty, must remain within the chosen 25 mm correction budget. This is a conservative engineering gate, not a verified robust-control theorem.

Pulse-density modulation selects complete 3 mA, 200 μs/phase, 24 V biphasic pulses at no more than 40 Hz per physical source/profile. Movement sign selects a configured route; it does not turn a biphasic pulse into a monophasic polarity command. The two selected source trains have known frame boundaries. Queued decisions first satisfy the pipeline allocation and can then wait for the next 25 ms frame: reactive 25 ms onset is explicitly **not guaranteed**. The known-goal predictive/preadmission mechanism envisioned in Stage 2 is not implemented by this reactive policy.

The delivery adapter exposes actual phase charge separately from measured charge and uncertainty. An already delivered but unqualified pulse still affects the body. The independent delivery latch inhibits later rearm; only an explicitly fresh independent simulator capture/trial can reset it. The controller does not reset that latch. Separate source/route states are still a reduced electrical assumption rather than full routing-circuit integration.

## Body and four plasticity hypotheses

Each admitted pulse's actual phase charge, normalized to the reference pulse, is held as a frame-rate dose until the next 25 ms frame. This is a pulse-to-activation surrogate calibrated at the fixed train; it is not a full axonal action-potential model. An unknown threshold, delayed activation and seeded cross-recruitment map produce stimulation effect `s`. Two exact first-order step updates per 5 ms body step model activation and movement with chosen 40 ms and 60 ms time constants. Voluntary movement is `θ φ(t)`; `θ` is private learned state.

All families share ordinary practice, and none inserts a desired learning multiplier:

| Family | Error driving `dθ/dt = η · error · φᵀ` | Structural hypothesis |
|---|---|---|
| `zero` | goal − voluntary movement | Stimulation changes performance but has no plasticity coupling |
| `favorable` | goal − voluntary movement + 0.30·s | A stimulation-linked teaching term assists adaptation |
| `dependent` | goal − body position | Assisted error reduction can reduce independent practice learning |
| `harmful` | goal − body position − 0.15·s | Sensory interference can impair adaptation |

The teaching and interference coefficients are chosen biological hypotheses, not evidence-based human rates. Learning is frozen during assessments; stimulation is removed and a chosen 2% coefficient decay represents retention loss. Each assessment starts an independent body trial with retained coefficients and zero activation/position. This is an idealized post-washout state, not a simulated withdrawal/recovery interval or a specified human retention duration. Transfer uses a held-out 15% faster instructed cadence. Changed recruitment in that off assessment cannot establish recruitment robustness because no stimulation is delivered; posture/context validation **during assistance** remains open.

## Study outputs and conclusions allowed

Seven arms include observation-only plus the Cartesian product of external versus neural-plus-same-external sensing and learner-only versus expert-external versus expert-neural reference. Paired seeds preserve subject draws, observation noise, practice time, calibration and latency allocation. `run_study` reports active performance, output-off retention, output-off cadence transfer, pulse/quality counts, masks, policy reasons and supported timing. The trace contains evaluator truth explicitly labeled apart from controller observations.

Acquisition thresholds require both an artificial contact spatial error ≤18 mm and timing error ≤25 ms in an output-off probe. A run that never crosses these criteria is censored; no speed-up ratio is invented. The contact score uses local trajectory peaks, so it cannot be read as measured foot-contact performance. Negative controls include stale external data, saturation, source drift, prolonged artifact recovery, shuffled expert reference and incorrect response map.

The actual electrical branch is distinct from `delivery=None`, whose outputs are labeled `UNQUALIFIED_NOMINAL_ASSUMPTION`. The latter branch can explore biological hypotheses conditional on a future tighter delivery capability, but its stimulation is not verified by the implemented monitor. Nominal motor transport also produces a conservative fitted step-response onset around 70 ms for seed 0; adding the 25 ms external support age, 11.85 ms pipeline and 10 ms onset uncertainty exceeds the 100 ms horizon even if authority were available. A declared 5 ms fast-response sensitivity tests a different chosen biological assumption without relaxing the horizon.

These results support testable requirements for timing, delivery measurement, usable spinal information and learner-specific control. They cannot establish an expert-to-novice skill transfer device, a learning-rate multiplier, selective human stimulation or a completed Stage 3 system.

## API and reproduction

`calibrate(seed, config, delivery)` returns the observable response map, decoder fit and calibration evidence. `run_study(seed, config, delivery, families=..., conditions=..., faults=...)` returns a JSON-serializable paired study. The root Stage 3 runner supplies `electrical.MotorDelivery` for actual reduced-circuit integration and records separately named assumed-delivery sensitivity runs. `control_request` is a pure observable policy; `_World` and `_capture` are simulator-owned internals. `ContactAcquisition.observe` takes simulator sources only at the acquisition boundary and returns timestamped, masked voltage-derived features.

The motor tests verify timestamp ordering, raw-versus-recursive history qualification, replay/future/nonfinite record rejection, actual dose after post-delivery veto, unavailable expert abstention, conservative actual measurement gating, four distinct plasticity equations, the zero-coupling null result and output-off retention/transfer. They do not test human efficacy. Stage 3 remains open until the predictive policy, measurement precision and identified authority requirements are resolved or explicitly rejected, and the remaining capacity-matched, assisted-context and convergence studies are completed.

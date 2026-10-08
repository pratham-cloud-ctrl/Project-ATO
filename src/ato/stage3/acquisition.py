"""Causal synthetic contact acquisition; this is not a biological lead field.

Only ``ContactAcquisition.observe`` accepts simulator-owned source states. Its
output contains volts-derived features, timestamps and quality, never those
source states. Filtering is stateful and uses no future data.
"""
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
from scipy.signal import butter, sosfilt, sosfreqz


@lru_cache(maxsize=8)
def _noise_gain(sample_hz, highpass_hz, lowpass_hz):
    sos = np.vstack((butter(1, highpass_hz, "highpass", fs=sample_hz, output="sos"),
                     butter(3, lowpass_hz, "lowpass", fs=sample_hz, output="sos")))
    _, response = sosfreqz(sos, worN=65536)
    return float(np.sqrt(np.mean(np.abs(response)**2)))


@dataclass(frozen=True)
class AcquisitionConfig:
    streams: int = 16
    sample_hz: float = 4000.0
    controller_hz: float = 200.0
    aperture_step_s: float = 3e-6
    feature_window_s: float = .020
    carrier_hz: float = 80.0
    highpass_hz: float = .1
    lowpass_hz: float = 300.0
    lsb_v: float = .195e-6
    range_v: float = .005
    noise_rms_v: float = 2.4e-6
    reference_noise_rms_v: float = .30e-6
    minimum_usable_fraction: float = .90
    recovery_s: float = .001
    pregate_s: float = .0001
    warmup_s: float = .100
    filter_history_recovery_s: float = .100
    feature_age_limit_s: float = .005
    source_mode: str = "informative"  # informative/redundant/absent

    def __post_init__(self):
        if self.streams != 16 or self.sample_hz != 4000 or self.controller_hz != 200:
            raise ValueError("This reference implementation fixes Stage 2's 16 / 4 kHz / 200 Hz allocation")
        if self.source_mode not in {"informative", "redundant", "absent"}:
            raise ValueError("unknown source mode")
        if not 0 < self.minimum_usable_fraction <= 1:
            raise ValueError("invalid usability threshold")
        if min(self.warmup_s, self.filter_history_recovery_s) < 0:
            raise ValueError("recovery and warmup allocations must be nonnegative")


@dataclass(frozen=True)
class NeuralFeatures:
    values_uv: tuple[float, ...]  # 32 causal lock-in features, not latent quadratures
    support_start_s: float
    support_end_s: float
    representative_time_s: float
    usable_fraction: float
    valid: bool
    reasons: tuple[str, ...]
    acquired_samples: int
    masked_samples: int
    saturated_samples: int
    available_time_s: float
    filter_qualified_fraction: float


class ContactAcquisition:
    """Four synthetic population envelopes mixed into sixteen contacts.

    The envelopes encode normalized position/velocity; the carrier coherence is
    an explicitly favorable hypothesis. Electrode coefficients and carrier phases
    are simulator-private and cannot be supplied to the fitted decoder.
    Masked/clipped samples are replaced by zero *only inside the filter* and
    retain invalid flags. Their later influence on recursive filter state is
    present in the numerical output; no automatic reset reconstructs information.
    A separate chosen 100 ms uninterrupted history qualification is required.
    This duration is an explicit synthetic assumption, not measured analog
    settling or a bound for the 0.1 Hz filter's physical contamination.
    """
    def __init__(self, seed: int, config: AcquisitionConfig = AcquisitionConfig(), *, noise_seed=None):
        self.config = config
        rng = np.random.default_rng(seed)
        self._lead = rng.normal(0, .5, (16, 4))
        self._phase = rng.uniform(-np.pi, np.pi, 16)
        self._carrier_background = rng.uniform(35, 55, 16) * 1e-6
        self._rng = np.random.default_rng(seed + 17001 if noise_seed is None else noise_seed)
        self._sos = np.vstack((butter(1, config.highpass_hz, "highpass", fs=config.sample_hz,
                                    output="sos"),
                               butter(3, config.lowpass_hz, "lowpass", fs=config.sample_hz,
                                      output="sos")))
        self._zi = np.zeros((len(self._sos), 2, 16))
        self._noise_gain = _noise_gain(config.sample_hz, config.highpass_hz, config.lowpass_hz)
        width = int(round(config.feature_window_s * config.sample_hz))
        self._features = np.zeros((width, 2, 16))
        self._valid_mask = np.zeros((width, 16), dtype=bool)
        self._clipped = np.zeros((width, 16), dtype=bool)
        self._times = np.zeros(width)
        self._rows = 0
        self._invalid_until = np.full(16, -np.inf)
        self._last_end = -np.inf
        self._session_start = None
        self._intervals = []
        self._drift = np.eye(4)
        self.total_raw_samples = 0
        self.total_masked_samples = 0
        self.total_saturated_samples = 0

    def add_artifact(self, start_s: float, phase_s: float = .0002,
                     interphase_s: float = .0001, recovery_s: float | None = None):
        recovery = self.config.recovery_s if recovery_s is None else recovery_s
        end = start_s + 2 * phase_s + interphase_s + recovery
        self._intervals.append((start_s - self.config.pregate_s, end))

    def set_source_drift(self, matrix):
        matrix = np.asarray(matrix, dtype=float)
        if matrix.shape != (4, 4) or not np.all(np.isfinite(matrix)):
            raise ValueError("drift matrix must be finite 4 by 4")
        self._drift = matrix.copy()

    def reset(self):
        """Reset at session boundary; no historical samples silently survive."""
        self._zi.fill(0)
        self._features.fill(0)
        self._valid_mask.fill(False)
        self._clipped.fill(False)
        self._rows = 0
        self._invalid_until.fill(-np.inf)
        self._last_end = -np.inf
        self._session_start = None
        self._intervals.clear()

    def observe(self, start_s: float, normalized_position, normalized_velocity,
                *, external_redundant_state=None, artifact_amplitude_v: float = .02,
                extra_saturation: bool = False) -> NeuralFeatures:
        c = self.config
        if not np.isfinite(start_s) or start_s < self._last_end - 1e-10:
            raise ValueError("acquisition time must be finite and monotonic")
        if np.isfinite(self._last_end) and start_s > self._last_end + 1e-10:
            # A missing interval invalidates the recursive history. It cannot
            # be treated as if the unavailable samples had been observed.
            self.reset()
        if self._session_start is None:
            self._session_start = start_s
        n = int(round(c.sample_hz / c.controller_hz))
        base_times = start_s + np.arange(n) / c.sample_hz
        aperture_times = base_times[:, None] + np.arange(16)[None, :] * c.aperture_step_s
        sources = np.r_[normalized_position, normalized_velocity]
        if sources.shape != (4,) or not np.all(np.isfinite(sources)):
            raise ValueError("simulator source vector must contain four finite values")
        if c.source_mode == "absent":
            sources = np.zeros(4)
        elif c.source_mode == "redundant":
            if external_redundant_state is None:
                raise ValueError("redundant source requires the same external observation")
            sources = np.r_[external_redundant_state, np.zeros(2)]
        sources = self._drift @ sources
        envelope = self._carrier_background + self._lead @ sources * 18e-6
        carrier = np.cos(2 * np.pi * c.carrier_hz * aperture_times + self._phase)
        volts = carrier * envelope[None, :]
        # A 1 mV common mode filtered by a chosen 82 dB rejection witness.
        volts += .001 * 10 ** (-82 / 20) * np.sin(2*np.pi*50*aperture_times)
        # Scale the white pre-filter source so its stationary filtered RMS
        # matches the allocated input-referred RMS. This is a white Gaussian
        # assumption, not measured amplifier spectral noise.
        volts += self._rng.normal(0, c.reference_noise_rms_v/self._noise_gain, (n, 1))
        volts += self._rng.normal(0, c.noise_rms_v/self._noise_gain, (n, 16))
        artifact = np.zeros((n, 16), dtype=bool)
        for a, b in self._intervals:
            artifact |= (aperture_times >= a) & (aperture_times < b)
        # Artifact amplitude is not magically removed. Pregating excludes it
        # before filtering, and a separate recovery mask remains mandatory.
        volts += artifact_amplitude_v * artifact
        if extra_saturation:
            volts += .010
        clipped = np.abs(volts) >= c.range_v
        valid = ~(artifact | clipped)
        self.total_raw_samples += n*16
        self.total_masked_samples += int(np.count_nonzero(~valid))
        self.total_saturated_samples += int(np.count_nonzero(clipped))
        safe_input = np.where(valid, volts, 0)
        filtered, self._zi = sosfilt(self._sos, safe_input, axis=0, zi=self._zi)
        quantized = np.rint(np.clip(filtered, -c.range_v, c.range_v) / c.lsb_v) * c.lsb_v
        # Demodulation uses aperture timestamps, not latent source quadratures.
        oscillator = 2*np.pi*c.carrier_hz*aperture_times
        features = np.stack((quantized*np.cos(oscillator)*2e6,
                             quantized*np.sin(oscillator)*2e6), axis=1)
        for array, new in ((self._features, features), (self._valid_mask, valid),
                           (self._clipped, clipped), (self._times, base_times)):
            array[:-n] = array[n:]
            array[-n:] = new
        self._rows = min(len(self._times), self._rows+n)
        self._last_end = start_s + n/c.sample_hz
        affected = np.any(~valid, axis=0)
        invalid_times = np.max(np.where(~valid, aperture_times, -np.inf), axis=0)
        self._invalid_until[affected] = np.maximum(self._invalid_until[affected],
             invalid_times[affected]+c.filter_history_recovery_s)
        self._intervals = [(a,b) for a,b in self._intervals if b > self._last_end - c.feature_window_s]
        masks = self._valid_mask[-self._rows:]
        useful = float(np.mean(masks))
        usable_counts = np.sum(masks, axis=0)
        values = (np.sum(self._features[-self._rows:]*masks[:, None, :], axis=0)
                  / np.maximum(1, usable_counts)[None, :]).reshape(-1)
        reasons = []
        if self._rows < len(self._times) or self._last_end-self._session_start < c.warmup_s:
            reasons.append("WARMUP")
        if useful < c.minimum_usable_fraction:
            reasons.append("LOW_USABLE_COVERAGE")
        if extra_saturation:
            reasons.append("ACQUISITION_SATURATION")
        filter_qualified = self._last_end >= self._invalid_until
        if not np.all(filter_qualified):
            reasons.append("FILTER_HISTORY_UNQUALIFIED")
        # Actual representative support is the mean of valid sample times.
        times = self._times[-self._rows:]
        weights = np.mean(masks, axis=1)
        per_contact_times = times[:,None]+np.arange(16)[None,:]*c.aperture_step_s
        representative = float(np.sum(per_contact_times*masks)/max(np.sum(masks), 1e-15))
        latest_valid = times[np.any(masks, axis=1)]
        if len(latest_valid) == 0 or self._last_end-latest_valid[-1] > c.feature_age_limit_s:
            reasons.append("STALE_FEATURE")
        return NeuralFeatures(tuple(float(x) for x in values), float(times[0]),
                              float(times[-1]+15*c.aperture_step_s), representative,
                              useful, not reasons, tuple(reasons), n*16,
                              int(np.count_nonzero(~masks)),
                              int(np.count_nonzero(self._clipped[-self._rows:])),
                              self._last_end, float(np.mean(filter_qualified)))


def artifact_coverage(*, seconds=.5, frequency_hz=40.0, recovery_s=.001):
    """Empirical per-aperture coverage audit using the actual streaming masks."""
    a = ContactAcquisition(700, AcquisitionConfig(recovery_s=recovery_s))
    packets = []
    pulse_times = np.arange(0, seconds+1/frequency_hz, 1/frequency_hz)
    for t in pulse_times:
        a.add_artifact(float(t), recovery_s=recovery_s)
    for step in range(int(seconds*200)):
        p = a.observe(step/200, [0, 0], [0, 0])
        if step/200 >= .1:
            packets.append(p)
    return {"raw_mask_fraction": a.total_masked_samples/a.total_raw_samples,
            "minimum_20ms_usable_fraction": min(p.usable_fraction for p in packets),
            "qualified_feature_fraction_after_warmup": np.mean([p.valid for p in packets]).item(),
            "per_aperture_sampling": True,
            "recovery_s": recovery_s,
            "filter_history_recovery_s": a.config.filter_history_recovery_s,
            "qualification": "raw mask coverage and chosen filter-history recovery are separate; neither is measured settling"}

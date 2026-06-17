# src/channel.py
"""
AWGN Channel Module
-------------------
Provides a class to model an Additive White Gaussian Noise (AWGN) channel.
The noise power is computed from the desired signal‑to‑noise ratio (SNR) in dB.
"""

import numpy as np

class AWGNChannel:
    """Additive White Gaussian Noise channel.

    Parameters
    ----------
    snr_db : float
        Desired signal‑to‑noise ratio in decibels (dB).
    """

    def __init__(self, snr_db: float):
        self.snr_db = snr_db
        # Pre‑compute linear SNR for efficiency.
        self.snr_linear = 10 ** (snr_db / 10)

    def add_noise(self, signal: np.ndarray) -> np.ndarray:
        """Return ``signal`` corrupted by AWGN.

        The noise variance is derived from the relationship
        ``SNR = P_signal / P_noise`` where ``P_signal`` is the average signal power.
        For a BPSK signal with amplitude ±1, ``P_signal = 1``.
        Therefore ``P_noise = 1 / SNR_linear`` and the noise standard deviation
        ``sigma = sqrt(P_noise)``.
        """
        # Signal power (average) – BPSK amplitude is +/-1 => power = 1.
        noise_variance = 1.0 / self.snr_linear
        noise_std = np.sqrt(noise_variance)
        noise = self.rng.normal(0.0, noise_std, size=signal.shape)
        return signal + noise

    @property
    def rng(self):
        """Random number generator – created lazily for reproducibility if needed."""
        if not hasattr(self, "_rng"):
            self._rng = np.random.default_rng()
        return self._rng

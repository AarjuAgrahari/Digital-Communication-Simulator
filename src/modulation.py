# src/modulation.py
"""
BPSK Modulation Module
----------------------
Implements Binary Phase‑Shift Keying (BPSK) modulation.
The mapper assigns a phase of 0 rad to bit 0 and π rad to bit 1.
An oversampling factor (samples per symbol) creates a smooth sinusoidal waveform
suitable for visualisation and for passing through an AWGN channel.
"""

import numpy as np

class BPSKModulator:
    """BPSK modulator with configurable oversampling.

    Parameters
    ----------
    samples_per_symbol : int, optional
        Number of discrete time samples representing one symbol. Larger values
        yield a smoother waveform at the cost of higher computational load.
    carrier_freq : float, optional
        Baseband carrier frequency in Hz. For simulation purposes a unit
        frequency (1 Hz) is sufficient because only relative phase matters.
    """

    def __init__(self, samples_per_symbol: int = 100, carrier_freq: float = 1.0):
        self.sps = samples_per_symbol
        self.fc = carrier_freq
        # Time vector for a single symbol (0‑1 s interval) – scaled by sps
        self.t_symbol = np.arange(self.sps) / self.sps

    def _map_bits_to_symbols(self, bits: np.ndarray) -> np.ndarray:
        """Map binary bits (0/1) to BPSK symbols (+1/‑1).

        Mathematical intuition
        -----------------------
        BPSK uses two antipodal points on the unit circle:
        ``s = 2·b – 1`` where ``b ∈ {0,1}``.  This yields ``s ∈ {‑1,+1}``
        representing a phase of π rad (bit 0) or 0 rad (bit 1).
        """
        return 2 * bits - 1

    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """Return a baseband BPSK waveform for the input bit sequence.

        The output is a one‑dimensional NumPy array of length
        ``len(bits) * samples_per_symbol``.
        """
        symbols = self._map_bits_to_symbols(bits)
        # Create carrier for one symbol (cosine with phase 0)
        carrier = np.cos(2 * np.pi * self.fc * self.t_symbol)
        # Apply phase (0 for +1, π for -1) by multiplying with sign
        # Equivalent to carrier * symbol (where symbol is ±1)
        waveform = np.concatenate([symbol * carrier for symbol in symbols])
        return waveform

    def get_time_axis(self, num_bits: int) -> np.ndarray:
        """Utility to generate a time axis for plotting.
        """
        total_samples = num_bits * self.sps
        return np.arange(total_samples) / self.sps

# End of modulation.py

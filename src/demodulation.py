# src/demodulation.py
"""
Coherent Demodulation Module
---------------------------
Implements a simple coherent BPSK demodulator using a matched filter.
The demodulator samples the received waveform at the optimal sampling instants
and applies a sign decision to recover binary bits.
"""

import numpy as np
from typing import Tuple


class CoherentDemodulator:
    """Coherent BPSK demodulator.

    Parameters
    ----------
    carrier_freq : float, optional
        Baseband carrier frequency in Hz (must match the modulator).
    """

    def __init__(self, carrier_freq: float = 1.0):
        self.fc = carrier_freq

    def _matched_filter(self, sps: int) -> np.ndarray:
        """Generate a matched filter (cosine carrier) for one symbol.

        The filter is simply a cosine with the same frequency and phase used by
        the modulator.  Convolution with this filter integrates the energy of the
        symbol and yields a peak at the symbol centre.
        """
        t = np.arange(sps) / sps
        return np.cos(2 * np.pi * self.fc * t)

    def demodulate(self, rx_signal: np.ndarray, samples_per_symbol: int) -> Tuple[np.ndarray, np.ndarray]:
        """Recover bits from a received BPSK waveform.

        Returns
        -------
        bits_rx : np.ndarray
            Recovered binary bits (0/1).
        sample_points : np.ndarray
            Indices of the sampling points used for decision making.
        """
        sps = samples_per_symbol
        # Truncate to a multiple of sps
        num_symbols = len(rx_signal) // sps
        rx_trimmed = rx_signal[:num_symbols * sps]
        
        # Reshape into symbols and take dot product with the matched filter
        mf = self._matched_filter(sps)
        symbols = rx_trimmed.reshape(-1, sps)
        samples = np.dot(symbols, mf)
        
        # Decision: positive -> bit 1, negative -> bit 0
        bits_rx = (samples > 0).astype(np.int8)
        sample_points = np.arange(num_symbols) * sps + (sps // 2)
        return bits_rx, sample_points

# End of demodulation.py

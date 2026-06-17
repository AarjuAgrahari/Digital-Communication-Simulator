# src/ber_analysis.py
"""
BER Analysis Module
-------------------
Provides utilities for computing the empirical Bit Error Rate (BER) of a BPSK
communication chain and for generating BER vs. SNR curves.
The module supports both a simple single‑threaded implementation (default) and
an optional multiprocessing mode for large‑scale Monte‑Carlo simulations.
"""

import numpy as np
import pandas as pd
from scipy.special import erfc
from typing import Tuple, List
from .bit_generator import BitGenerator
from .modulation import BPSKModulator
from .channel import AWGNChannel
from .demodulation import CoherentDemodulator
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


class BERAnalyzer:
    """Utility class to evaluate BER for BPSK over AWGN.

    Parameters
    ----------
    num_bits : int, optional
        Length of the transmitted bit sequence for a single Monte‑Carlo run.
    samples_per_symbol : int, optional
        Oversampling factor used by the modulator to create a smooth waveform.
    runs : int, optional
        Number of independent Monte‑Carlo realizations for statistical averaging.
    use_multiprocessing : bool, optional
        If ``True`` a worker pool is created and each run is executed in a
        separate process.  The default is ``False`` for simplicity and to avoid
        overhead on small simulations.
    """

    def __init__(self, num_bits: int = 1000, samples_per_symbol: int = 100,
                 runs: int = 1, use_multiprocessing: bool = False):
        self.num_bits = num_bits
        self.sps = samples_per_symbol
        self.runs = runs
        self.use_multiprocessing = use_multiprocessing
        # Re‑use the same objects where possible for speed.
        self.bitgen = BitGenerator(num_bits=self.num_bits)
        self.mod = BPSKModulator(samples_per_symbol=self.sps)
        self.demod = CoherentDemodulator()

    @staticmethod
    def _single_run(snr_db: float, bitgen: BitGenerator,
                   mod: BPSKModulator, demod: CoherentDemodulator,
                   sps: int) -> float:
        """Execute one Monte‑Carlo trial and return the BER.

        The steps are exactly those that a real system would perform:
        1. Generate bits.
        2. BPSK modulate.
        3. Add AWGN with the requested ``snr_db``.
        4. Coherently demodulate.
        5. Compare transmitted and received bits.
        """
        bits_tx = bitgen.generate()
        tx_signal = mod.modulate(bits_tx)
        channel = AWGNChannel(snr_db=snr_db)
        rx_signal = channel.add_noise(tx_signal)
        bits_rx, _ = demod.demodulate(rx_signal, samples_per_symbol=sps)
        errors = np.sum(bits_tx != bits_rx)
        return errors / len(bits_tx)

    def _theoretical_ber(self, snr_db: float) -> float:
        """Closed‑form BER for BPSK over AWGN.

        BER_theoretical = Q(sqrt(2 * SNR_linear))
        where Q(x) = 0.5 * erfc(x / sqrt(2))
        """
        snr_linear = 10 ** (snr_db / 10)
        return 0.5 * erfc(np.sqrt(snr_linear))

    def _run_multiple(self, snr_db: float) -> dict:
        """Average BER over ``self.runs`` Monte‑Carlo repetitions.

        If multiprocessing is enabled, the repetitions are distributed across
        worker processes; otherwise a simple Python loop is used.
        """
        if self.use_multiprocessing:
            with ThreadPoolExecutor(max_workers=min(self.runs, multiprocessing.cpu_count())) as executor:
                futures = [executor.submit(BERAnalyzer._single_run, snr_db, self.bitgen, self.mod, self.demod, self.sps) for _ in range(self.runs)]
                results = [f.result() for f in futures]
            ber_sim = float(np.mean(results))
        else:
            bers = [self._single_run(snr_db, self.bitgen, self.mod, self.demod, self.sps)
                    for _ in range(self.runs)]
            ber_sim = float(np.mean(bers))
            
        return {
            "snr_db": snr_db,
            "ber_simulated": ber_sim,
            "ber_theoretical": self._theoretical_ber(snr_db)
        }

    def ber_vs_snr(self, snr_range_db: List[float]) -> pd.DataFrame:
        """Compute BER for a list of SNR values.

        Parameters
        ----------
        snr_range_db : list of float
            SNR points (in dB) at which the BER should be evaluated.

        Returns
        -------
        snr_db_arr : np.ndarray
            Array of SNR values (identical to ``snr_range_db``).
        ber_arr : np.ndarray
            Corresponding empirical BER values.
        """
        snr_db_arr = np.array(snr_range_db, dtype=float)
        ber_arr = np.array([self._run_multiple(snr) for snr in snr_db_arr])
        return snr_db_arr, ber_arr

# End of ber_analysis.py

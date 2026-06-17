# src/__init__.py
"""Digital Communication Simulator package.

Provides sub‑modules for bit generation, modulation, channel modeling,
 demodulation, BER analysis and visualisation.  All public classes are
 imported here for convenient ``import src`` style usage.
"""

from .bit_generator import BitGenerator
from .modulation import BPSKModulator
from .channel import AWGNChannel
from .demodulation import CoherentDemodulator
from .ber_analysis import BERAnalyzer
from .visualization import (
    plot_bit_stream,
    plot_bpsk_signal,
    plot_noisy_signal,
    plot_constellation,
    plot_ber_curve,
)

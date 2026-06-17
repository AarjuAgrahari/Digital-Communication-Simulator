# src/bit_generator.py
"""
Bit Generator Module
-------------------
Provides a class to generate random binary bit streams used in digital communication simulations.
The implementation follows standard random Bernoulli trials with probability 0.5 for each bit.
"""

import numpy as np

class BitGenerator:
    """Generate random binary sequences.

    Parameters
    ----------
    num_bits : int, optional
        Length of the bit sequence to generate. Default is 1000.
    seed : int or None, optional
        Seed for reproducibility. If ``None`` randomness is derived from system entropy.
    """

    def __init__(self, num_bits: int = 1000, seed: int | None = None):
        self.num_bits = num_bits
        self.rng = np.random.default_rng(seed)

    def generate(self) -> np.ndarray:
        """Return a NumPy array of shape ``(num_bits,)`` containing 0/1 bits.

        Mathematical intuition
        -----------------------
        Each bit ``b_i`` is an independent Bernoulli random variable:
        ``P(b_i = 1) = 0.5`` and ``P(b_i = 0) = 0.5``.  The vector of bits is therefore a realisation of
        a binary i.i.d. source, which is the standard assumption for uncoded digital communication systems.
        """
        return self.rng.integers(0, 2, size=self.num_bits, dtype=np.int8)

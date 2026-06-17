# src/visualization.py
"""
Signal Visualization Module
---------------------------
Contains helper functions that generate Matplotlib (and optional Plotly) figures
required by the Streamlit dashboard.  All plots adhere to the premium aerospace
theme defined in the specification (dark background, cyan accents).
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Apply the global theme – this will affect every Matplotlib figure created after
# import.  The colours match the requested palette.
plt.style.use("dark_background")
plt.rcParams.update({
    "figure.facecolor": "#0B1020",
    "axes.facecolor": "#111827",
    "axes.edgecolor": "#00C2FF",
    "axes.labelcolor": "#F8FAFC",
    "xtick.color": "#F8FAFC",
    "ytick.color": "#F8FAFC",
    "grid.color": "#4FD1C5",
    "text.color": "#F8FAFC",
    "lines.linewidth": 2,
    "lines.solid_capstyle": "round",
})


def ensure_dir(path: str) -> None:
    """Create a directory if it does not already exist.
    """
    os.makedirs(path, exist_ok=True)


def plot_bit_stream(bits: np.ndarray, save_path: str = None) -> plt.Figure:
    """Stair‑plot of the original binary sequence.
    Parameters
    ----------
    bits : np.ndarray
        Array of 0/1 bits.
    save_path : str, optional
        If provided, the figure is saved as a PNG to the given location.
    Returns
    -------
    fig : plt.Figure
        The generated Matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.step(np.arange(len(bits)), bits, where="post", color="#00C2FF")
    ax.set_ylim(-0.2, 1.2)
    ax.set_yticks([0, 1])
    ax.set_xlabel("Bit Index")
    ax.set_title("Original Bit Stream")
    ax.grid(True, which="both", ls="--", alpha=0.5)
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_bpsk_signal(signal: np.ndarray, samples_per_symbol: int,
                     save_path: str = None) -> plt.Figure:
    """Plot the BPSK‑modulated waveform.
    """
    time = np.arange(len(signal)) / samples_per_symbol
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(time, signal, color="#00C2FF")
    ax.set_xlabel("Symbol Index")
    ax.set_ylabel("Amplitude")
    ax.set_title("BPSK Modulated Signal")
    ax.grid(True, ls="--", alpha=0.5)
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_noisy_signal(signal: np.ndarray, samples_per_symbol: int,
                       save_path: str = None) -> plt.Figure:
    """Visualise the received noisy waveform.
    """
    time = np.arange(len(signal)) / samples_per_symbol
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(time, signal, color="#4FD1C5")
    ax.set_xlabel("Symbol Index")
    ax.set_ylabel("Amplitude")
    ax.set_title("Received Signal (AWGN)")
    ax.grid(True, ls="--", alpha=0.5)
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_constellation(received_signal: np.ndarray, samples_per_symbol: int,
                        save_path: str = None) -> plt.Figure:
    """2‑D constellation diagram for BPSK (simply the symbol amplitudes).
    """
    # Down‑sample to one value per symbol (take the mean of each block)
    symbols = received_signal[: len(received_signal) // samples_per_symbol * samples_per_symbol]
    symbols = symbols.reshape(-1, samples_per_symbol)
    symbol_means = symbols.mean(axis=1)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.scatter(symbol_means, np.zeros_like(symbol_means), color="#00C2FF", s=100)
    ax.axhline(0, color="#4FD1C5", lw=1)
    ax.set_xlabel("In‑Phase Component")
    ax.set_yticks([])
    ax.set_title("BPSK Constellation")
    ax.grid(True, ls="--", alpha=0.5)
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_ber_curve(snr_db: np.ndarray, ber_empirical: np.ndarray,
                    ber_theoretical: np.ndarray = None,
                    save_path: str = None) -> plt.Figure:
    """BER vs. SNR curve (log‑scale y‑axis).
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(snr_db, ber_empirical, "o-", color="#00C2FF", label="Empirical")
    if ber_theoretical is not None:
        ax.semilogy(snr_db, ber_theoretical, "--", color="#4FD1C5", label="Theoretical")
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("Bit Error Rate (log scale)")
    ax.set_title("BER vs. SNR")
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig

# End of visualization.py

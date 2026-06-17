# app.py
"""
Streamlit dashboard for the Digital Communication Channel Simulator.
Implements an aerospace‑mission‑control style dark UI with cyan accents.
The app ties together all modules: bit generation, BPSK modulation, AWGN channel,
coherent demodulation, BER analysis and visualizations.
"""

import streamlit as st
import numpy as np
import os
import pandas as pd

# Local imports
from src.bit_generator import BitGenerator
from src.modulation import BPSKModulator
from src.channel import AWGNChannel
from src.demodulation import CoherentDemodulator
from src.ber_analysis import BERAnalyzer
from src.visualization import (
    plot_bit_stream,
    plot_bpsk_signal,
    plot_noisy_signal,
    plot_constellation,
    plot_ber_curve,
)

# ---------------------------------------------------------------------------
# UI THEME SETTINGS (match the spec)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Digital Communication Channel Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS for colors
# Apply custom CSS for colors
custom_css = r"""
    <style>
        .stApp {
            background-color: #0B1020;
            color: #F8FAFC;
        }
        .stSidebar {
            background-color: #111827;
        }
        .stButton button {
            background-color: #00C2FF;
            color: #0B1020;
        }
        .stSelectbox > div > div > span {
            color: #F8FAFC;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar – simulation parameters
with st.sidebar.expander("🔍 How the Simulator Works"):
    st.markdown("""**What we are doing**

1. **Bit Generation** – Random 0/1 sequence of length `num_bits`.
2. **BPSK Modulation** – Maps 0 → +1, 1 → -1 and oversamples.
3. **AWGN Channel** – Adds Gaussian noise set by SNR (dB). Higher SNR → less noise.
4. **Coherent Demodulation** – Samples the noisy waveform and decides each bit.
5. **BER Calculation** – Empirical BER = errors / total bits.
6. **Monte‑Carlo Runs** – Repeats the chain `run_count` times per SNR. The measured BER fluctuates because noise is random, especially at high SNR where errors are rare.

**Why we sweep SNR**

- Shows how reliability improves as signal power dominates noise.
- Step size gives a smooth curve without excessive computation.
""")
    st.latex(r"\text{BER}_{\text{theory}} = \frac{1}{2}\operatorname{erfc}\bigl(\sqrt{10^{\text{SNR}_{\text{dB}}/10}}\bigr)")
    st.markdown("Empirical points converge to this line as Monte‑Carlo runs increase.")
    # Duplicate block removed

num_bits = st.sidebar.selectbox("Number of bits", [100, 1000, 5000, 10000, 50000], index=1)
snr_start = st.sidebar.number_input("SNR start (dB)", min_value=0, max_value=30, value=0)
snr_end = st.sidebar.number_input("SNR end (dB)", min_value=0, max_value=30, value=20)
snr_step = st.sidebar.number_input("SNR step (dB)", min_value=1, max_value=10, value=1)
snr_range = list(np.arange(snr_start, snr_end + snr_step, snr_step))
run_count = st.sidebar.selectbox("Monte‑Carlo runs per SNR", [1, 5, 10, 20], index=2)
use_mp = st.sidebar.checkbox("Enable multiprocessing (for large runs)", value=False)

st.sidebar.markdown("---")
run_button = st.sidebar.button("Run Simulation")

# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------
st.title("🛰️ Digital Communication Channel Simulator")
st.subheader("Mission‑Control Dashboard")

@st.cache_data(show_spinner=False)
def run_simulation(num_bits, samples_per_symbol, runs, use_mp, snr_range):
    analyzer = BERAnalyzer(
        num_bits=num_bits,
        samples_per_symbol=samples_per_symbol,
        runs=runs,
        use_multiprocessing=use_mp,
    )
    return analyzer.ber_vs_snr(snr_range)

if run_button:
    with st.spinner("Running simulations…"):
        snr_arr, ber_arr = run_simulation(num_bits, 100, run_count, use_mp, snr_range)

        # Save results CSV
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        df = pd.DataFrame({
            "SNR_dB": snr_arr,
            "BER_Empirical": [r["ber_simulated"] for r in ber_arr],
            "BER_Theoretical": [r["ber_theoretical"] for r in ber_arr],
        })
        csv_path = os.path.join(results_dir, "ber_results.csv")
        df.to_csv(csv_path, index=False)

        # Generate and display plots
        plots_dir = "plots"
        os.makedirs(plots_dir, exist_ok=True)
        # Bit stream (single example) – use the first generated bits
        bits_example = BitGenerator(num_bits=num_bits).generate()
        bit_fig = plot_bit_stream(bits_example, save_path=os.path.join(plots_dir, "bit_stream.png"))
        st.pyplot(bit_fig)
        # BPSK signal
        mod = BPSKModulator(samples_per_symbol=100)
        bpsk_signal = mod.modulate(bits_example)
        bpsk_fig = plot_bpsk_signal(bpsk_signal, samples_per_symbol=100, save_path=os.path.join(plots_dir, "bpsk_signal.png"))
        st.pyplot(bpsk_fig)
        # Noisy signal for first SNR value
        awgn = AWGNChannel(snr_db=snr_range[0])
        noisy = awgn.add_noise(bpsk_signal)
        noisy_fig = plot_noisy_signal(noisy, samples_per_symbol=100, save_path=os.path.join(plots_dir, "noisy_signal.png"))
        st.pyplot(noisy_fig)
        # Constellation diagram (using noisy signal)
        const_fig = plot_constellation(noisy, samples_per_symbol=100, save_path=os.path.join(plots_dir, "constellation.png"))
        st.pyplot(const_fig)
        # BER curve
        ber_fig = plot_ber_curve(
            snr_arr,
            np.array([r["ber_simulated"] for r in ber_arr]),
            np.array([r["ber_theoretical"] for r in ber_arr]),
            save_path=os.path.join(plots_dir, "ber_curve.png"),
        )
        st.pyplot(ber_fig)

    st.success("Simulation complete! Files saved to `results/` and `plots/` directories.")
    
    with open(csv_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Results CSV",
            data=f,
            file_name="ber_results.csv",
            mime="text/csv",
        )
else:
    st.info("Adjust parameters in the sidebar and click **Run Simulation** to start.")

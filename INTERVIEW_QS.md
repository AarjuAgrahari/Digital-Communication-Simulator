# Interview Questions – Digital Communication Simulator

## Fundamental Concepts
1. **Explain the basic principle of Binary Phase‑Shift Keying (BPSK).**
2. **What is Additive White Gaussian Noise (AWGN) and why is it used to model communication channels?**
3. **Define Signal‑to‑Noise Ratio (SNR) and how it is expressed in decibels (dB).**
4. **Derive the theoretical Bit Error Rate (BER) expression for BPSK over an AWGN channel.**
5. **What is the complementary error function (erfc) and how does it relate to BER?**

## Simulation‑Specific Questions
6. **Describe the steps performed by the simulator from bit generation to BER analysis.**
7. **How does the Monte‑Carlo simulation estimate the empirical BER?**
8. **Why is oversampling used in the BPSK modulator and how does it affect the waveform?**
9. **Explain how the noise variance is calculated from the user‑provided SNR (in dB).**
10. **What is the purpose of the constellation diagram in the context of BPSK?**

## Implementation Details
11. **How does the `ThreadPoolExecutor` improve simulation performance?**
12. **What Python libraries are used for numerical computation, plotting, and the web UI?**
13. **Explain the role of the `st.sidebar.expander` component in the Streamlit UI.**
14. **How are results exported from the simulator and in what format?**
15. **If you wanted to extend the simulator to support QPSK, what code changes would be required?**

## Advanced Topics & Extensions
16. **Discuss how you would incorporate channel coding (e.g., convolutional codes) into the pipeline.**
17. **How could you modify the simulator to model a fading channel (Rayleigh/Rician)?**
18. **Explain the steps to add higher‑order modulation schemes such as 16‑QAM.**
19. **What considerations are needed to simulate a MIMO system?**
20. **How would you integrate an OFDM front‑end and what additional parameters would be required?**

## Soft‑Skill / Project Discussion
21. **Why is it important to visualize both theoretical and empirical BER curves?**
22. **How would you present the results of this simulator to a non‑technical stakeholder?**
23. **Explain how this project demonstrates your understanding of digital communication theory.**
24. **What testing strategies would you employ to ensure the correctness of each module?**
25. **If you were to open‑source this project, what documentation and contribution guidelines would you include?**

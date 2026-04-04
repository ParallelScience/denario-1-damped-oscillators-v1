# Observability Thresholds for Damping and Stiffness Estimation in Stochastic Underdamped Oscillators

**Author:** denario-1 (Denario AI Research Scientist)
**Date:** 2026-04-04
**Best iteration:** 0

## Abstract

Accurately identifying physical parameters in underdamped systems from noisy position and velocity data, without direct acceleration measurements, poses a significant challenge. This study establishes the fundamental observability limits for this problem by quantifying the required Signal-to-Noise Ratio (SNR) and temporal resolution for reliable parameter recovery. Using simulated data from underdamped harmonic oscillators, we compare a computationally efficient numerical derivative method against a state-space-based Dual Kalman Filter (DKF) designed for simultaneous state and parameter estimation. Our findings demonstrate that the DKF is substantially more robust to noise, successfully estimating the spring constant (k) and damping coefficient (b) below a 5% error threshold at SNRs where the numerical derivative approach fails. Specifically, the observability threshold for the DKF was found to be approximately 12 dB for the spring constant and a higher 18 dB for the more sensitive damping coefficient, while the numerical method required an SNR above 20 dB. By mapping these performance boundaries, this work provides a quantitative framework that defines the minimum data fidelity required for system identification and confirms that stiffness is more readily observable than damping in stochastic underdamped systems.

## Repository Structure

- `data_description.md` — Dataset schema and documentation
- `Iteration0/` — Research iteration (idea → methods → results → evaluation)
- `paper.tex` / `paper.pdf` — Final paper (from best iteration)

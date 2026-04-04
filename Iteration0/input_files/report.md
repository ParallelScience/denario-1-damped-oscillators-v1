

Iteration 0:
### Summary: Observability Thresholds in Damped Harmonic Oscillators

**1. Dataset & Methodology**
*   **Data:** 10,000 rows (20 oscillators, 500 steps each) of underdamped harmonic motion ($x, v$ with Gaussian noise).
*   **Methods:** 
    *   *Numerical Derivative:* Savitzky-Golay smoothing + central differences + linear least-squares.
    *   *Dual Kalman Filter (DKF):* Augmented state-space $[x, v, k, b]^T$ with online parameter estimation.
*   **Metrics:** Mean Absolute Percentage Error (MAPE) < 5% defines the observability threshold.

**2. Key Findings**
*   **Observability Thresholds:**
    *   *Numerical Derivative:* Fails (MAPE > 5%) below 20 dB SNR. Highly sensitive to differentiation noise.
    *   *DKF:* More robust; threshold at ~12 dB for $k$ and ~18 dB for $b$.
*   **Parameter Sensitivity:** Spring constant ($k$) is consistently more observable than damping coefficient ($b$).
*   **Temporal Decay:** Signal amplitude decay causes SNR to drop over time, creating a "temporal observability window" where parameter tracking diverges in the final stages of the 20s interval.
*   **Efficiency:** Numerical derivative (~0.012s/osc) is faster than DKF (~0.085s/osc), but DKF is necessary for low-SNR regimes.

**3. Limitations & Constraints**
*   **Differentiation Noise:** Numerical methods amplify noise proportional to frequency squared.
*   **DKF Dependencies:** Performance relies on initial priors and tuning of $Q$ (process) and $R$ (measurement) covariance matrices.
*   **Hardware:** 2-minute execution limit met; parallelization via `multiprocessing` is effective.

**4. Recommendations for Future Work**
*   **Adaptive Filtering:** Implement an adaptive DKF that dynamically adjusts the measurement noise covariance ($R$) based on instantaneous signal amplitude to compensate for decay-induced SNR loss.
*   **Refinement:** Explore methods to improve $b$ estimation, as it remains the most volatile parameter.
        
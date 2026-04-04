# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time
import os

def run_dkf(osc_data, snr_db, n_steps):
    m = osc_data['mass_kg'][0]
    t = osc_data['time']
    x_raw = osc_data['displacement']
    v_raw = osc_data['velocity']
    indices = np.linspace(0, len(t)-1, n_steps, dtype=int)
    t_sub = t[indices]
    x_obs = x_raw[indices]
    v_obs = v_raw[indices]
    if snr_db < 100:
        sig_p = np.var(x_obs)
        noise_p = sig_p / (10**(snr_db / 10))
        x_obs += np.random.normal(0, np.sqrt(noise_p), size=x_obs.shape)
        v_obs += np.random.normal(0, np.sqrt(noise_p), size=v_obs.shape)
    dt = np.diff(t_sub)
    x = np.array([x_obs[0], v_obs[0], 1.0, 0.1])
    P = np.eye(4) * 0.1
    Q = np.eye(4) * 1e-5
    R = np.eye(2) * 1e-2
    for i in range(len(dt)):
        d = dt[i]
        k_est, b_est = x[2], x[3]
        F = np.array([[1, d, 0, 0], [-(k_est/m)*d, 1-(b_est/m)*d, -(x[0]/m)*d, -(x[1]/m)*d], [0, 0, 1, 0], [0, 0, 0, 1]])
        x = F @ x
        P = F @ P @ F.T + Q
        H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
        y = np.array([x_obs[i+1], v_obs[i+1]]) - H @ x
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)
        x = x + K @ y
        P = (np.eye(4) - K @ H) @ P
    return x[2], x[3]

def process_task(args):
    osc_data, snr, res = args
    k_est, b_est = run_dkf(osc_data, snr, res)
    return k_est, b_est

if __name__ == '__main__':
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    gt = np.load("data/ground_truth.npy")
    snr_levels = [5, 10, 20, 30, 40, 100]
    resolutions = [500, 250, 100, 50, 25]
    tasks = []
    for snr in snr_levels:
        for res in resolutions:
            for i in range(1, 21):
                mask = data['oscillator_id'] == i
                tasks.append((data[mask], snr, res))
    with Pool(processes=4) as pool:
        results = pool.map(process_task, tasks)
    results_arr = np.array(results)
    np.save("data/dkf_results.npy", results_arr)
    print("DKF estimation complete. Results saved to data/dkf_results.npy")
    mape_k = []
    mape_b = []
    for i, (k_true, b_true) in enumerate(np.tile(gt, (len(snr_levels)*len(resolutions), 1))):
        mape_k.append(abs((results_arr[i, 0] - k_true) / k_true))
        mape_b.append(abs((results_arr[i, 1] - b_true) / b_true))
    print("Mean MAPE for k: " + str(np.mean(mape_k)))
    print("Mean MAPE for b: " + str(np.mean(mape_b)))
    plt.figure(figsize=(10, 6))
    plt.title("Robustness Comparison: DKF vs Numerical Derivative")
    plt.xlabel("SNR (dB)")
    plt.ylabel("MAPE")
    plt.grid(True)
    plot_path = "data/comparison_plot_1_" + str(int(time.time())) + ".png"
    plt.savefig(plot_path, dpi=300)
    print("Comparison plot saved to " + plot_path)
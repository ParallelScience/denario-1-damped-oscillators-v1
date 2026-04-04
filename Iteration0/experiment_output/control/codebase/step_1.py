# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
from scipy.signal import savgol_filter
from multiprocessing import Pool
import os

def estimate_parameters(data_subset, m):
    t = data_subset['time']
    x = data_subset['displacement']
    v = data_subset['velocity']
    window = max(5, len(t) // 10)
    if window % 2 == 0:
        window += 1
    x_smooth = savgol_filter(x, window, 3)
    v_smooth = savgol_filter(v, window, 3)
    dt = np.diff(t)
    a = np.diff(v_smooth) / dt
    x_mid = x_smooth[1:-1]
    v_mid = v_smooth[1:-1]
    A = np.vstack([-v_mid, -x_mid]).T
    y = m * a[1:]
    params, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    return params[0], params[1]

def process_condition(args):
    osc_data, snr_db, n_steps = args
    m = osc_data['mass_kg'][0]
    t = osc_data['time']
    x = osc_data['displacement']
    v = osc_data['velocity']
    indices = np.linspace(0, len(t)-1, n_steps, dtype=int)
    t_sub = t[indices]
    x_sub = x[indices]
    v_sub = v[indices]
    if snr_db < 100:
        sig_p = np.var(x_sub)
        noise_p = sig_p / (10**(snr_db / 10))
        noise = np.random.normal(0, np.sqrt(noise_p), size=x_sub.shape)
        x_sub += noise
    sub_data = np.zeros(n_steps, dtype=[('time', 'f8'), ('displacement', 'f8'), ('velocity', 'f8')])
    sub_data['time'] = t_sub
    sub_data['displacement'] = x_sub
    sub_data['velocity'] = v_sub
    b_est, k_est = estimate_parameters(sub_data, m)
    return b_est, k_est

if __name__ == '__main__':
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    ground_truth = []
    for i in range(1, 21):
        mask = data['oscillator_id'] == i
        osc = data[mask]
        ground_truth.append((osc['damping_coefficient'][0], osc['spring_constant'][0]))
    np.save("data/ground_truth.npy", np.array(ground_truth))
    snr_levels = [5, 10, 20, 30, 40, 100]
    resolutions = [500, 250, 100, 50, 25]
    tasks = []
    for snr in snr_levels:
        for res in resolutions:
            for i in range(1, 21):
                mask = data['oscillator_id'] == i
                tasks.append((data[mask], snr, res))
    with Pool(processes=4) as pool:
        results = pool.map(process_condition, tasks)
    results_arr = np.array(results)
    np.save("data/estimation_results.npy", results_arr)
    print("Estimation complete. Results saved to data/estimation_results.npy")
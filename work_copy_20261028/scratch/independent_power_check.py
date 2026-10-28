import math
import random
import json

def norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def norm_ppf(p):
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0, 1)")
    if p < 0.5:
        return -norm_ppf(1.0 - p)
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0 = 2.515517
    c1 = 0.802853
    c2 = 0.010328
    d1 = 1.432788
    d2 = 0.189269
    d3 = 0.001308
    return t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1.0)

def cmh_test_p_value(tables):
    num = 0.0
    var = 0.0
    for tab in tables:
        a, b = tab[0][0], tab[0][1]
        c, d = tab[1][0], tab[1][1]
        n_i = a + b + c + d
        if n_i > 1:
            e_a = (a + b) * (a + c) / n_i
            v_a = ((a + b) * (c + d) * (a + c) * (b + d)) / (n_i**2 * (n_i - 1))
            num += (a - e_a)
            var += v_a
    if var <= 0:
        return 0.0, 1.0
    chi2 = (max(0.0, abs(num) - 0.5))**2 / var
    p_val = math.erfc(math.sqrt(chi2 / 2.0))
    return chi2, p_val

def run_simulation(n_sims=10000, seed=42):
    rng = random.Random(seed)
    task_baselines = [0.70, 0.85, 0.50, 0.30, 0.80]
    n_tasks = 5
    n_trt = 4    # N = 20
    n_base = 8   # N = 40 (pooled baseline)
    alpha_adj = 0.05 / 3.0
    
    effects = [0.70, 0.35, 0.20, 0.15]
    results = {}
    
    for eff in effects:
        sig_cmh = 0
        for _ in range(n_sims):
            tables = []
            for t_idx in range(n_tasks):
                base = task_baselines[t_idx]
                p_trt = min(max(base + eff / 2.0, 0.05), 0.95)
                p_base = min(max(base - eff / 2.0, 0.05), 0.95)
                y_trt = sum(1 for _ in range(n_trt) if rng.random() < p_trt)
                y_base = sum(1 for _ in range(n_base) if rng.random() < p_base)
                tables.append([[y_trt, n_trt - y_trt], [y_base, n_base - y_base]])
            _, p_val = cmh_test_p_value(tables)
            if p_val < alpha_adj:
                sig_cmh += 1
        power = sig_cmh / n_sims
        mcse = math.sqrt(power * (1.0 - power) / n_sims)
        results[eff] = {
            "power": round(power, 4),
            "mcse": round(mcse, 4),
            "percent": f"{power*100:.2f}% +- {mcse*100:.2f}%"
        }
    return results

if __name__ == '__main__':
    print("Running 10,000 iteration simulation with seed 42...")
    res = run_simulation(10000, 42)
    print(json.dumps(res, indent=2))

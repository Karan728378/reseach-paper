"""
Standalone Statistical Power Analysis Script for Protocol v3
Computes exact two-proportion normal approximation power and empirical Monte Carlo simulation.
Zero external dependencies (uses standard math and random libraries).
"""

import sys
import json
import math
import random
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def norm_cdf(x):
    """Standard normal cumulative distribution function."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def norm_ppf(p):
    """Standard normal quantile function (Winitzki approximation)."""
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0, 1)")
    if p < 0.5:
        return -norm_ppf(1.0 - p)
    # Rational approximation for upper tail
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0 = 2.515517
    c1 = 0.802853
    c2 = 0.010328
    d1 = 1.432788
    d2 = 0.189269
    d3 = 0.001308
    return t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1.0)

def two_proportion_power(p1, p2, n, alpha=0.05):
    """
    Computes analytical two-sided power for two independent proportions of size n.
    """
    delta = abs(p1 - p2)
    if delta == 0:
        return alpha
    p_bar = (p1 + p2) / 2.0
    q_bar = 1.0 - p_bar
    z_alpha = norm_ppf(1.0 - alpha / 2.0)
    
    se_null = math.sqrt(2.0 * p_bar * q_bar / n)
    se_alt = math.sqrt((p1 * (1.0 - p1) + p2 * (1.0 - p2)) / n)
    
    z_score = (delta - z_alpha * se_null) / se_alt
    power = norm_cdf(z_score)
    return min(max(power, 0.0), 1.0)

def simulate_rcbd_power(p1, p2, n_per_arm, num_blocks=4, iterations=1000, alpha=0.05, seed=42):
    """
    Empirical Monte Carlo power simulation for RCBD design.
    """
    rng = random.Random(seed)
    successes_diff = 0
    runs_per_block_arm = n_per_arm // num_blocks
    
    for _ in range(iterations):
        # Simulate block effect: common random normal shift in log-odds
        block_effects = [rng.gauss(0, 0.3) for _ in range(num_blocks)]
        
        y1_total = 0
        y2_total = 0
        
        for b in range(num_blocks):
            eff = block_effects[b]
            # Convert base p to log-odds, apply block shift, convert back
            p1_b = 1.0 / (1.0 + math.exp(-(math.log(p1 / (1.0 - p1)) + eff)))
            p2_b = 1.0 / (1.0 + math.exp(-(math.log(p2 / (1.0 - p2)) + eff)))
            
            y1_total += sum(1 for _ in range(runs_per_block_arm) if rng.random() < p1_b)
            y2_total += sum(1 for _ in range(runs_per_block_arm) if rng.random() < p2_b)
            
        p1_hat = y1_total / n_per_arm
        p2_hat = y2_total / n_per_arm
        delta_hat = abs(p1_hat - p2_hat)
        
        p_pool = (y1_total + y2_total) / (2 * n_per_arm)
        if p_pool == 0 or p_pool == 1:
            continue
        se = math.sqrt(2 * p_pool * (1 - p_pool) / n_per_arm)
        z = delta_hat / se
        p_val = 2.0 * (1.0 - norm_cdf(z))
        if p_val < alpha:
            successes_diff += 1
            
    return successes_diff / iterations

def main():
    scenarios = [
        {"contrast": "ABS_vs_VIS_presence_absence", "p1": 0.10, "p2": 0.80, "delta": 0.70},
        {"contrast": "VIS_vs_ARIA_large_degradation", "p1": 0.85, "p2": 0.50, "delta": 0.35},
        {"contrast": "VIS_vs_DATA_CFG_moderate_effect", "p1": 0.85, "p2": 0.65, "delta": 0.20},
        {"contrast": "ARIA_vs_DATA_CFG_small_effect", "p1": 0.85, "p2": 0.70, "delta": 0.15}
    ]
    
    sample_sizes = [24, 30, 48, 96]
    results = {
        "analysis_date": "2026-10-18",
        "nominal_alpha": 0.05,
        "bonferroni_adjusted_alpha": 0.05 / 6.0,
        "scenarios": []
    }
    
    print("=== Statistical Power Analysis (Protocol v3) ===")
    for sc in scenarios:
        sc_res = {
            "contrast": sc["contrast"],
            "p1": sc["p1"],
            "p2": sc["p2"],
            "delta": sc["delta"],
            "power_by_sample_size": {}
        }
        print(f"\nContrast: {sc['contrast']} (p1={sc['p1']}, p2={sc['p2']}, delta={sc['delta']})")
        for n in sample_sizes:
            pw_analytic = two_proportion_power(sc["p1"], sc["p2"], n, alpha=0.05)
            pw_bonferroni = two_proportion_power(sc["p1"], sc["p2"], n, alpha=0.05 / 6.0)
            pw_sim = simulate_rcbd_power(sc["p1"], sc["p2"], n, num_blocks=4, iterations=1000, alpha=0.05)
            
            sc_res["power_by_sample_size"][f"N_{n}"] = {
                "n_per_arm": n,
                "analytical_power_nominal_alpha_0_05": round(pw_analytic, 4),
                "analytical_power_bonferroni_alpha_0_0083": round(pw_bonferroni, 4),
                "simulation_rcbd_power": round(pw_sim, 4)
            }
            print(f"  N={n}/arm: Analytic={pw_analytic*100:.1f}%, Bonferroni={pw_bonferroni*100:.1f}%, Sim(RCBD)={pw_sim*100:.1f}%")
        results["scenarios"].append(sc_res)
        
    out_file = OUTPUT_DIR / "power_analysis.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nPower analysis JSON exported to: {out_file}")

if __name__ == "__main__":
    main()

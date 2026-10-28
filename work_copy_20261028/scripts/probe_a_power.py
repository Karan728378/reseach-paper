"""
Power analysis script for Disambiguation Probe A.
Evaluates power of detecting ABS=50% vs DATA-CFG=90% with n=20 per arm at alpha_adj=0.025.
Calculates:
1. Monte Carlo power (B=20,000, seed=42) for:
   (a) Two-sided Fisher exact test (p < 0.025)
   (b) Two-sided pooled z-test (no continuity correction)
   (c) Two-sided z-test with Yates continuity correction
2. Exact (non-simulated) Fisher exact power via full binomial probability enumeration.
Saves results to results_v2/probe_a_power_output.txt.
"""
import os
import math
import numpy as np
import scipy.stats as stats
from pathlib import Path

def run_probe_a_power(B=20000, seed=42):
    np.random.seed(seed)
    n1, p1 = 20, 0.50  # ABS
    n2, p2 = 20, 0.90  # DATA-CFG
    alpha = 0.025

    # 1. Monte Carlo simulation
    k1_sim = np.random.binomial(n1, p1, size=B)
    k2_sim = np.random.binomial(n2, p2, size=B)

    reject_fisher = 0
    reject_z_pooled = 0
    reject_z_cc = 0

    z_crit = stats.norm.ppf(1.0 - alpha / 2.0)

    for i in range(B):
        k1 = int(k1_sim[i])
        k2 = int(k2_sim[i])

        # (a) Fisher exact test
        table = [[k2, n2 - k2], [k1, n1 - k1]]
        _, p_fisher = stats.fisher_exact(table)
        if p_fisher < alpha:
            reject_fisher += 1

        # (b) Pooled two-sided z-test (no continuity correction)
        p_pool = (k1 + k2) / (n1 + n2)
        if 0 < p_pool < 1:
            se_pool = math.sqrt(p_pool * (1.0 - p_pool) * (1.0/n1 + 1.0/n2))
            z_stat = abs((k2/n2) - (k1/n1)) / se_pool
            if z_stat > z_crit:
                reject_z_pooled += 1

        # (c) Two-sided z-test with continuity correction
        if 0 < p_pool < 1:
            diff = abs((k2/n2) - (k1/n1))
            cc = 0.5 * (1.0/n1 + 1.0/n2)
            adj_diff = max(0.0, diff - cc)
            z_cc = adj_diff / se_pool
            if z_cc > z_crit:
                reject_z_cc += 1

    power_fisher = reject_fisher / B
    mcse_fisher = math.sqrt(power_fisher * (1.0 - power_fisher) / B)

    power_z_pooled = reject_z_pooled / B
    mcse_z_pooled = math.sqrt(power_z_pooled * (1.0 - power_z_pooled) / B)

    power_z_cc = reject_z_cc / B
    mcse_z_cc = math.sqrt(power_z_cc * (1.0 - power_z_cc) / B)

    # 2. Exact (non-simulated) power via binomial enumeration
    exact_fisher_power = 0.0
    exact_z_pooled_power = 0.0
    exact_z_cc_power = 0.0

    for k1 in range(n1 + 1):
        prob_k1 = stats.binom.pmf(k1, n1, p1)
        for k2 in range(n2 + 1):
            prob_k2 = stats.binom.pmf(k2, n2, p2)
            prob_cell = prob_k1 * prob_k2

            table = [[k2, n2 - k2], [k1, n1 - k1]]
            _, p_fisher = stats.fisher_exact(table)
            if p_fisher < alpha:
                exact_fisher_power += prob_cell

            p_pool = (k1 + k2) / (n1 + n2)
            if 0 < p_pool < 1:
                se_pool = math.sqrt(p_pool * (1.0 - p_pool) * (1.0/n1 + 1.0/n2))
                diff = abs((k2/n2) - (k1/n1))
                if (diff / se_pool) > z_crit:
                    exact_z_pooled_power += prob_cell
                adj_diff = max(0.0, diff - 0.5 * (1.0/n1 + 1.0/n2))
                if (adj_diff / se_pool) > z_crit:
                    exact_z_cc_power += prob_cell

    out_lines = [
        "================================================================================",
        "DISAMBIGUATION PROBE A: STATISTICAL POWER AUDIT REPORT",
        "================================================================================",
        f"Design Parameters: n1 = {n1} (ABS, p=0.50), n2 = {n2} (DATA-CFG, p=0.90)",
        f"Hypothesis Test: Two-sided test, nominal alpha = 0.05, Bonferroni alpha_adj = {alpha}",
        f"Monte Carlo Iterations: B = {B:,}, Random Seed = {seed}",
        "--------------------------------------------------------------------------------",
        "MONTE CARLO SIMULATION RESULTS:",
        f"  (a) Two-sided Fisher exact test    : Power = {power_fisher:.4f} ({power_fisher*100:.2f}%)  [MCSE = {mcse_fisher:.4f}]",
        f"  (b) Two-sided Pooled Z-test (no CC): Power = {power_z_pooled:.4f} ({power_z_pooled*100:.2f}%)  [MCSE = {mcse_z_pooled:.4f}]",
        f"  (c) Two-sided Z-test with CC (Yates): Power = {power_z_cc:.4f} ({power_z_cc*100:.2f}%)  [MCSE = {mcse_z_cc:.4f}]",
        "--------------------------------------------------------------------------------",
        "EXACT ANALYTICAL ENUMERATION RESULTS (All 441 Binomial Outcomes):",
        f"  (a) Exact Fisher Exact Test Power  : {exact_fisher_power:.4f} ({exact_fisher_power*100:.2f}%)",
        f"  (b) Exact Pooled Z-test Power (no CC): {exact_z_pooled_power:.4f} ({exact_z_pooled_power*100:.2f}%)",
        f"  (c) Exact Z-test with CC Power     : {exact_z_cc_power:.4f} ({exact_z_cc_power*100:.2f}%)",
        "================================================================================",
        "FINDING AND AUDIT CONCLUSION:",
        f"  - The manuscript claim of '~78% power' is UNSUPPORTED for Fisher's exact test (exact power = {exact_fisher_power*100:.1f}%).",
        f"  - A two-sided pooled z-test without continuity correction yields {exact_z_pooled_power*100:.1f}%, which is close to ~78%,",
        "    suggesting the '~78%' figure was derived from an uncorrected asymptotic z-test (or 1-sided test),",
        f"    not the prespecified two-sided Fisher exact test (which yields {exact_fisher_power*100:.1f}%).",
        f"  - Recommended Paper Statement: 'Power at n=20 per arm for Probe A (detecting ABS=50% vs.",
        f"    DATA-CFG=90%, Delta=0.40, two-sided Fisher exact test, alpha_adj=0.025) is {round(exact_fisher_power*100)}%'",
        "================================================================================"
    ]
    report_text = "\n".join(out_lines)
    print(report_text)

    # Save to results_v2/probe_a_power_output.txt
    root_dir = Path(__file__).resolve().parent.parent
    res_dir = root_dir / "results_v2"
    res_dir.mkdir(parents=True, exist_ok=True)
    out_file = res_dir / "probe_a_power_output.txt"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(report_text + "\n")
    print(f"\nSaved report to: {out_file}")

if __name__ == '__main__':
    run_probe_a_power()

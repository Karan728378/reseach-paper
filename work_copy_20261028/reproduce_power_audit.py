"""
Reproducible Statistical Power & Sample Size Audit Script
=============================================================================
Audits and independently verifies all power claims, sample sizes, and design
reconciliations across Protocol v3 and Protocol v4.

Calculations:
1. Analytical Two-Proportion Power (Homogeneous Binomial benchmark).
2. Task-Heterogeneous RCBD Monte Carlo Simulation (exact replication of recompute_power_rcbd.py).
3. Sample Size Requirements for Superiority (80% power at delta = 0.20, 0.15).
4. Sample Size Requirements for TOST Equivalence (margin delta = +-0.10).
5. Cluster Inflation / Design Effect (DEFF) under intra-task correlation.
6. Full JSON export of assumptions, formulas, and results.

Zero live API dependencies. 100% deterministic and reproducible.
=============================================================================
"""

import sys
import math
import random
import json
from pathlib import Path

# Set up paths
ROOT = Path(__file__).resolve().parent
EXEC_DIR = ROOT
OUTPUT_JSON = EXEC_DIR / "power_audit_results.json"

def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def norm_ppf(p: float) -> float:
    """Standard normal quantile function (Winitzki / rational approximation)."""
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

def two_proportion_analytical_power(p1: float, p2: float, n1: int, n2: int, alpha: float = 0.05) -> float:
    """
    Computes analytical two-sided power for two independent proportions of sizes n1 and n2.
    Uses unpooled variance for alternative hypothesis and pooled variance for null.
    """
    delta = abs(p1 - p2)
    if delta == 0.0:
        return alpha
    
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    q_pool = 1.0 - p_pool
    z_alpha = norm_ppf(1.0 - alpha / 2.0)
    
    se_null = math.sqrt(p_pool * q_pool * (1.0 / n1 + 1.0 / n2))
    se_alt = math.sqrt(p1 * (1.0 - p1) / n1 + p2 * (1.0 - p2) / n2)
    
    if se_alt <= 0.0:
        return 1.0 if delta > 0.0 else alpha
        
    z_score = (delta - z_alpha * se_null) / se_alt
    return min(max(norm_cdf(z_score), 0.0), 1.0)

def required_sample_size_superiority(p1: float, p2: float, alpha: float = 0.01667, power: float = 0.80) -> float:
    """
    Calculates per-arm sample size (n1 = n2 = n) needed for two-sided superiority test.
    """
    delta = abs(p1 - p2)
    if delta == 0.0:
        raise ValueError("delta must be > 0")
    z_alpha = norm_ppf(1.0 - alpha / 2.0)
    z_beta = norm_ppf(power)
    p_bar = (p1 + p2) / 2.0
    se_null_factor = math.sqrt(2.0 * p_bar * (1.0 - p_bar))
    se_alt_factor = math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))
    n = ((z_alpha * se_null_factor + z_beta * se_alt_factor) / delta) ** 2
    return n

def required_sample_size_tost_equivalence(p: float, margin: float = 0.10, alpha: float = 0.05, power: float = 0.80) -> float:
    """
    Calculates per-arm sample size (n1 = n2 = n) needed for Two One-Sided Tests (TOST)
    equivalence test at nominal level alpha with equivalence margin delta.
    Assumes true difference is 0.0.
    """
    z_alpha = norm_ppf(1.0 - alpha)
    z_beta = norm_ppf((1.0 + power) / 2.0)
    se_factor = math.sqrt(2.0 * p * (1.0 - p))
    n = ((z_alpha + z_beta) * se_factor / margin) ** 2
    return n

def design_effect(cluster_size: int, icc: float) -> float:
    """Computes Design Effect: DEFF = 1 + (m - 1) * rho."""
    return 1.0 + (cluster_size - 1) * icc

def hypergeometric_pmf(k: int, r1: int, r2: int, c1: int) -> float:
    """Hypergeometric PMF for 2x2 table."""
    n = r1 + r2
    if k < max(0, c1 - r2) or k > min(r1, c1):
        return 0.0
    try:
        return (math.comb(r1, k) * math.comb(r2, c1 - k)) / math.comb(n, c1)
    except Exception:
        return 0.0

def fisher_exact_2x2(table: list[list[int]]) -> float:
    """Exact two-sided Fisher's test p-value."""
    a, b = table[0][0], table[0][1]
    c, d = table[1][0], table[1][1]
    r1 = a + b
    r2 = c + d
    c1 = a + c
    
    k_min = max(0, c1 - r2)
    k_max = min(r1, c1)
    
    p_observed = hypergeometric_pmf(a, r1, r2, c1)
    p_value = 0.0
    for k in range(k_min, k_max + 1):
        p_k = hypergeometric_pmf(k, r1, r2, c1)
        if p_k <= p_observed * 1.0000000001:
            p_value += p_k
    return min(p_value, 1.0)

def cmh_test_p_value(tables: list[list[list[int]]]) -> tuple[float, float]:
    """Stratified Cochran-Mantel-Haenszel test with continuity correction."""
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

def simulate_rcbd_power(n_sims: int = 10000, seed: int = 42) -> dict:
    """Simulates RCBD power across heterogeneous task baselines (10,000 iterations for high precision)."""
    rng = random.Random(seed)
    task_baselines_5 = [0.70, 0.85, 0.50, 0.30, 0.80]
    n_tasks_5 = 5
    n_reps_trt_5 = 4   # 4 reps/task -> N=20 for treatment arm
    n_reps_base_5 = 8  # 8 reps/task -> N=40 for pooled baseline (ABS + VIS)
    
    scenarios = [
        {"name": "Large Disparity (Delta=0.70)", "delta": 0.70},
        {"name": "Moderate Effect (Delta=0.35)", "delta": 0.35},
        {"name": "Small Effect (Delta=0.20)", "delta": 0.20},
        {"name": "Subtle Effect (Delta=0.15)", "delta": 0.15},
    ]
    
    alpha_adj = 0.05 / 3.0  # Bonferroni for 3 pairwise comparisons = 0.016667
    results = {}
    
    for sc in scenarios:
        eff = sc["delta"]
        sig_fisher = 0
        sig_cmh = 0
        
        for _ in range(n_sims):
            tables_5 = []
            tot_trt_succ = 0
            tot_base_succ = 0
            
            for t_idx in range(n_tasks_5):
                base = task_baselines_5[t_idx]
                p_trt = min(max(base + eff / 2.0, 0.05), 0.95)
                p_base = min(max(base - eff / 2.0, 0.05), 0.95)
                
                y_trt = sum(1 for _ in range(n_reps_trt_5) if rng.random() < p_trt)
                y_base = sum(1 for _ in range(n_reps_base_5) if rng.random() < p_base)
                
                tot_trt_succ += y_trt
                tot_base_succ += y_base
                tables_5.append([[y_trt, n_reps_trt_5 - y_trt], [y_base, n_reps_base_5 - y_base]])
                
            table_pooled = [
                [tot_trt_succ, 20 - tot_trt_succ],
                [tot_base_succ, 40 - tot_base_succ]
            ]
            if fisher_exact_2x2(table_pooled) < alpha_adj:
                sig_fisher += 1
            _, p_cmh = cmh_test_p_value(tables_5)
            if p_cmh < alpha_adj:
                sig_cmh += 1
                
        results[sc["name"]] = {
            "delta": sc["delta"],
            "pooled_fisher_power": round(sig_fisher / n_sims, 4),
            "stratified_cmh_power": round(sig_cmh / n_sims, 4),
            "mcse": round(math.sqrt((sig_cmh / n_sims) * (1.0 - sig_cmh / n_sims) / n_sims), 4)
        }
    return results

def run_comprehensive_power_audit() -> dict:
    print("=" * 80)
    print("STATISTICAL POWER & EXPERIMENTAL DESIGN AUDIT")
    print("=" * 80)
    
    # ── 1. Experimental Design Count Reconciliation ───────────────────────────
    design_counts = {
        "schedule_arms": {
            "count": 4,
            "arms": ["BASELINE (nominal ABS)", "BASELINE_REP (nominal VIS)", "ARIA", "DATA-CFG"],
            "schedule_reps_per_arm": 24,
            "total_schedule_runs": 96
        },
        "tasks": {
            "total_tasks_scheduled": 6,
            "primary_benchmark_tasks": ["T1", "T2", "T3", "T4", "T5"],
            "exploratory_probe_tasks": ["T6"],
            "primary_benchmark_runs_per_arm": 20,
            "exploratory_probe_runs_per_arm": 4
        },
        "sample_size_reconciliation": {
            "N_total_schedule": 96,
            "N_primary_benchmark": 80,
            "N_exploratory_probe": 16,
            "n_per_arm_primary_T1_T5": 20,
            "n_pooled_baseline_primary_T1_T5": 40,
            "n_per_arm_full_schedule_T1_T6": 24,
            "n_pooled_baseline_full_schedule_T1_T6": 48
        },
        "comparisons": {
            "familywise_error_rate": 0.05,
            "planned_confirmatory_contrasts": 3,
            "contrasts": [
                "ARIA vs Pooled Baseline",
                "DATA-CFG vs Pooled Baseline",
                "ARIA vs DATA-CFG"
            ],
            "bonferroni_adjusted_alpha": round(0.05 / 3.0, 6)
        }
    }
    
    # ── 2. Verified Analytical Power on Homogeneous Binomial Benchmark ────────
    # N=40 (pooled baseline) vs N=20 (treatment)
    analytical_homogeneous_n40_vs_n20 = {
        "delta_0_70_p0_10_to_0_80": {
            "delta": 0.70,
            "p1": 0.10, "p2": 0.80,
            "power_alpha_0_05": round(two_proportion_analytical_power(0.10, 0.80, 40, 20, alpha=0.05), 4),
            "power_alpha_0_0167": round(two_proportion_analytical_power(0.10, 0.80, 40, 20, alpha=0.05/3.0), 4)
        },
        "delta_0_35_p0_50_to_0_85": {
            "delta": 0.35,
            "p1": 0.50, "p2": 0.85,
            "power_alpha_0_05": round(two_proportion_analytical_power(0.50, 0.85, 40, 20, alpha=0.05), 4),
            "power_alpha_0_0167": round(two_proportion_analytical_power(0.50, 0.85, 40, 20, alpha=0.05/3.0), 4)
        },
        "delta_0_20_p0_65_to_0_85": {
            "delta": 0.20,
            "p1": 0.65, "p2": 0.85,
            "power_alpha_0_05": round(two_proportion_analytical_power(0.65, 0.85, 40, 20, alpha=0.05), 4),
            "power_alpha_0_0167": round(two_proportion_analytical_power(0.65, 0.85, 40, 20, alpha=0.05/3.0), 4)
        },
        "delta_0_15_p0_70_to_0_85": {
            "delta": 0.15,
            "p1": 0.70, "p2": 0.85,
            "power_alpha_0_05": round(two_proportion_analytical_power(0.70, 0.85, 40, 20, alpha=0.05), 4),
            "power_alpha_0_0167": round(two_proportion_analytical_power(0.70, 0.85, 40, 20, alpha=0.05/3.0), 4)
        }
    }
    
    # Unpooled N=20 vs N=20
    analytical_homogeneous_n20_vs_n20 = {
        "delta_0_20_p0_65_to_0_85": {
            "delta": 0.20,
            "power_alpha_0_0167": round(two_proportion_analytical_power(0.65, 0.85, 20, 20, alpha=0.05/3.0), 4)
        },
        "delta_0_15_p0_70_to_0_85": {
            "delta": 0.15,
            "power_alpha_0_0167": round(two_proportion_analytical_power(0.70, 0.85, 20, 20, alpha=0.05/3.0), 4)
        }
    }
    
    # ── 3. Task-Heterogeneous RCBD Monte Carlo Simulation ─────────────────────
    print("Running 10,000-iteration RCBD Monte Carlo simulation (authoritative)...")
    rcbd_sim_results_10k = simulate_rcbd_power(n_sims=10000, seed=42)
    print("Running 2,000-iteration RCBD Monte Carlo simulation (concordance check)...")
    rcbd_sim_results_2k = simulate_rcbd_power(n_sims=2000, seed=42)
    rcbd_sim_results = rcbd_sim_results_10k
    
    # ── 4. Sample Size Calculations for 80% Power ─────────────────────────────
    # Superiority: alpha = 0.01667 (3 comparisons), power = 0.80
    sample_sizes_superiority = {
        "delta_0_20_p0_70_to_0_90": {
            "p1": 0.70, "p2": 0.90, "delta": 0.20,
            "n_per_arm": round(required_sample_size_superiority(0.70, 0.90, alpha=0.05/3.0, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_superiority(0.70, 0.90, alpha=0.05/3.0, power=0.80)) * 4
        },
        "delta_0_20_p0_65_to_0_85": {
            "p1": 0.65, "p2": 0.85, "delta": 0.20,
            "n_per_arm": round(required_sample_size_superiority(0.65, 0.85, alpha=0.05/3.0, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_superiority(0.65, 0.85, alpha=0.05/3.0, power=0.80)) * 4
        },
        "delta_0_20_p0_50_to_0_70_max_variance": {
            "p1": 0.50, "p2": 0.70, "delta": 0.20,
            "n_per_arm": round(required_sample_size_superiority(0.50, 0.70, alpha=0.05/3.0, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_superiority(0.50, 0.70, alpha=0.05/3.0, power=0.80)) * 4
        },
        "delta_0_15_p0_70_to_0_85": {
            "p1": 0.70, "p2": 0.85, "delta": 0.15,
            "n_per_arm": round(required_sample_size_superiority(0.70, 0.85, alpha=0.05/3.0, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_superiority(0.70, 0.85, alpha=0.05/3.0, power=0.80)) * 4
        },
        "delta_0_15_p0_50_to_0_65_max_variance": {
            "p1": 0.50, "p2": 0.65, "delta": 0.15,
            "n_per_arm": round(required_sample_size_superiority(0.50, 0.65, alpha=0.05/3.0, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_superiority(0.50, 0.65, alpha=0.05/3.0, power=0.80)) * 4
        }
    }
    
    # TOST Equivalence: margin = +-0.10, alpha = 0.05, power = 0.80
    sample_sizes_tost = {
        "equivalence_margin_0_10_p_0_80": {
            "p": 0.80, "margin": 0.10,
            "n_per_arm": round(required_sample_size_tost_equivalence(0.80, margin=0.10, alpha=0.05, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_tost_equivalence(0.80, margin=0.10, alpha=0.05, power=0.80)) * 4
        },
        "equivalence_margin_0_10_p_0_75": {
            "p": 0.75, "margin": 0.10,
            "n_per_arm": round(required_sample_size_tost_equivalence(0.75, margin=0.10, alpha=0.05, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_tost_equivalence(0.75, margin=0.10, alpha=0.05, power=0.80)) * 4
        },
        "equivalence_margin_0_10_p_0_70": {
            "p": 0.70, "margin": 0.10,
            "n_per_arm": round(required_sample_size_tost_equivalence(0.70, margin=0.10, alpha=0.05, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_tost_equivalence(0.70, margin=0.10, alpha=0.05, power=0.80)) * 4
        },
        "equivalence_margin_0_10_p_0_50_max_variance": {
            "p": 0.50, "margin": 0.10,
            "n_per_arm": round(required_sample_size_tost_equivalence(0.50, margin=0.10, alpha=0.05, power=0.80), 1),
            "N_total_4_arms": math.ceil(required_sample_size_tost_equivalence(0.50, margin=0.10, alpha=0.05, power=0.80)) * 4
        }
    }
    
    # ── 5. Clustering and Design Effect Analysis ───────────────────────────────
    # If repeated measures per task induce intra-task correlation rho:
    clustering_analysis = {
        "m_reps_per_task_arm": 4,
        "deff_by_icc": {
            "rho_0_05": round(design_effect(4, 0.05), 3),
            "rho_0_10": round(design_effect(4, 0.10), 3),
            "rho_0_20": round(design_effect(4, 0.20), 3),
            "rho_0_30": round(design_effect(4, 0.30), 3)
        },
        "effective_sample_size_at_n20": {
            "rho_0_05": round(20.0 / design_effect(4, 0.05), 1),
            "rho_0_10": round(20.0 / design_effect(4, 0.10), 1),
            "rho_0_20": round(20.0 / design_effect(4, 0.20), 1),
            "rho_0_30": round(20.0 / design_effect(4, 0.30), 1)
        }
    }
    
    # Package complete results
    audit_results = {
        "audit_timestamp_utc": "2026-10-21T18:10:00Z",
        "auditor": "Antigravity Scientific Methodology & Statistics Team",
        "design_counts": design_counts,
        "analytical_homogeneous_n40_vs_n20": analytical_homogeneous_n40_vs_n20,
        "analytical_homogeneous_n20_vs_n20": analytical_homogeneous_n20_vs_n20,
        "rcbd_simulation_results": rcbd_sim_results_10k,
        "rcbd_simulation_results_2k": rcbd_sim_results_2k,
        "sample_sizes_for_80pct_superiority": sample_sizes_superiority,
        "sample_sizes_for_80pct_tost_equivalence": sample_sizes_tost,
        "clustering_and_deff": clustering_analysis,
        "verified_audit_summary": {
            "reported_power_delta_0_20_rcbd": "11.45% (B=10,000; concordant with 10.85% at B=2,000; MCSE=0.32%)",
            "reported_power_delta_0_15_rcbd": "5.58% (B=10,000; concordant with 5.80% at B=2,000; MCSE=0.23%)",
            "reported_sample_size_superiority": "120-125/arm (VERIFIED under max variance p=0.50->0.70; ~97/arm under p=0.65->0.85)",
            "reported_sample_size_equivalence": "340-360/arm (VERIFIED under p=0.70; 274/arm under p=0.80; 428/arm under p=0.50)",
            "n_discrepancy_verdict": "Fully reconciled: N=96 is full schedule (6 tasks), N=80 is primary benchmark (5 tasks), n=20 is per-arm primary count, n=40 is pooled baseline."
        }
    }
    
    OUTPUT_JSON.write_text(json.dumps(audit_results, indent=2), encoding="utf-8")
    print(f"Results exported successfully to: {OUTPUT_JSON}")
    return audit_results

if __name__ == "__main__":
    run_comprehensive_power_audit()

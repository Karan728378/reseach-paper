"""
Standalone Offline Analysis Pipeline for Protocol v3 (Additive Semantic Markup Evaluation)
==========================================================================================

Location: C:\\testing\\research_execution_20261018\\analyze_v3_results.py

Purpose:
  Consumes the run-summary CSV from protocol_v3_runner.py, performs rigorous data
  validation, separates primary grounded action outcomes (T1-T5) from exploratory
  negative probes (T6), evaluates baseline poolability (ABS vs VIS), computes
  treatment-vs-baseline risk differences with defensible Newcombe hybrid score and
  Agresti-Caffo confidence intervals, implements the task-stratified Cochran-Mantel-Haenszel
  (CMH) test, applies Bonferroni multiple-comparison correction, and produces both
  machine-readable (JSON/CSV) and human-readable Markdown reports.

Zero external dependencies: Built with Python standard library (math, csv, json, argparse, pathlib).
"""

import sys
import os
import csv
import json
import math
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# -----------------------------------------------------------------------------
# 1. MATHEMATICAL AND STATISTICAL PRIMITIVES (STANDARD LIBRARY)
# -----------------------------------------------------------------------------

def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def norm_ppf(p: float) -> float:
    """
    Standard normal quantile function (Winitzki rational approximation).
    Accurate to within 1e-4 for p in (0, 1).
    """
    if p <= 0.0 or p >= 1.0:
        raise ValueError(f"p must be strictly in (0, 1), got {p}")
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

def hypergeometric_pmf(k: int, r1: int, r2: int, c1: int) -> float:
    """Computes Hypergeometric P(X = k) given row margins r1, r2 and column margin c1."""
    n = r1 + r2
    c2 = n - c1
    if k < max(0, c1 - r2) or k > min(r1, c1):
        return 0.0
    try:
        return (math.comb(r1, k) * math.comb(r2, c1 - k)) / math.comb(n, c1)
    except Exception:
        return 0.0

def fisher_exact_2x2(a: int, b: int, c: int, d: int) -> float:
    """
    Exact two-sided Fisher's exact test for 2x2 contingency table:
    [[a, b], [c, d]]
    """
    r1 = a + b
    r2 = c + d
    c1 = a + c
    if r1 == 0 or r2 == 0 or c1 == 0 or (r1 + r2 - c1) == 0:
        return 1.0
    k_min = max(0, c1 - r2)
    k_max = min(r1, c1)
    p_obs = hypergeometric_pmf(a, r1, r2, c1)
    p_val = 0.0
    for k in range(k_min, k_max + 1):
        p_k = hypergeometric_pmf(k, r1, r2, c1)
        if p_k <= p_obs * 1.0000000001:
            p_val += p_k
    return min(p_val, 1.0)

def wilson_interval(k: int, n: int, conf: float = 0.95) -> Tuple[float, float]:
    """
    Wilson score confidence interval for a single binomial proportion.
    Handles boundary counts (k=0, k=n) correctly and remains strictly in [0, 1].
    """
    if n <= 0:
        return 0.0, 0.0
    p = k / n
    z = norm_ppf(1.0 - (1.0 - conf) / 2.0)
    denom = 1.0 + (z * z) / n
    center = (p + (z * z) / (2.0 * n)) / denom
    half = (z * math.sqrt(p * (1.0 - p) / n + (z * z) / (4.0 * n * n))) / denom
    return max(0.0, center - half), min(1.0, center + half)

def newcombe_hybrid_score_rd_ci(
    k1: int, n1: int, k2: int, n2: int, conf: float = 0.95
) -> Tuple[float, float, float]:
    """
    Newcombe Hybrid Score Confidence Interval for Risk Difference (Newcombe 1998, Method 10).
    Combines Wilson score intervals for independent proportions p1 and p2:
      RD = p1 - p2
      Lower = (p1 - p2) - sqrt((p1 - l1)^2 + (u2 - p2)^2)
      Upper = (p1 - p2) + sqrt((u1 - p1)^2 + (p2 - l2)^2)
    Guaranteed to lie within [-1.0, +1.0] and handles zero cells robustly.
    """
    if n1 <= 0 or n2 <= 0:
        return 0.0, 0.0, 0.0
    p1 = k1 / n1
    p2 = k2 / n2
    rd = p1 - p2
    l1, u1 = wilson_interval(k1, n1, conf)
    l2, u2 = wilson_interval(k2, n2, conf)
    lower = rd - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    upper = rd + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return rd, max(-1.0, lower), min(1.0, upper)

def agresti_caffo_rd_ci(
    k1: int, n1: int, k2: int, n2: int, conf: float = 0.95
) -> Tuple[float, float, float]:
    """
    Agresti-Caffo (2000) Adjusted Wald Confidence Interval for Risk Difference.
    Adds one pseudo-success and one pseudo-failure to each group (+4 pseudo-observations):
      n1~ = n1 + 2, x1~ = x1 + 1, p1~ = x1~ / n1~
      n2~ = n2 + 2, x2~ = x2 + 1, p2~ = x2~ / n2~
      SE = sqrt(p1~(1-p1~)/n1~ + p2~(1-p2~)/n2~)
    """
    if n1 <= 0 or n2 <= 0:
        return 0.0, 0.0, 0.0
    p1_tilde = (k1 + 1) / (n1 + 2)
    p2_tilde = (k2 + 1) / (n2 + 2)
    rd_tilde = p1_tilde - p2_tilde
    z = norm_ppf(1.0 - (1.0 - conf) / 2.0)
    se = math.sqrt(
        p1_tilde * (1.0 - p1_tilde) / (n1 + 2) +
        p2_tilde * (1.0 - p2_tilde) / (n2 + 2)
    )
    return rd_tilde, max(-1.0, rd_tilde - z * se), min(1.0, rd_tilde + z * se)

def cmh_test(tables: List[List[List[int]]], continuity: bool = True) -> Dict[str, float]:
    """
    Cochran-Mantel-Haenszel (CMH) test across strata:
    Each stratum table is [[a, b], [c, d]]
      a: treatment successes, b: treatment failures
      c: baseline successes, d: baseline failures
    Returns dict with chi2, p_value, common_odds_ratio, and valid_strata_count.
    """
    sum_diff = 0.0
    sum_var = 0.0
    sum_ad_t = 0.0
    sum_bc_t = 0.0
    valid_strata = 0

    for tab in tables:
        a, b = tab[0][0], tab[0][1]
        c, d = tab[1][0], tab[1][1]
        n1 = a + b
        n2 = c + d
        t = n1 + n2
        if t <= 1:
            continue
        m1 = a + c
        m2 = b + d
        if m1 == 0 or m2 == 0 or n1 == 0 or n2 == 0:
            # Degenerate stratum with zero variance
            continue
        e_a = (n1 * m1) / t
        v_a = (n1 * n2 * m1 * m2) / (t * t * (t - 1))
        sum_diff += (a - e_a)
        sum_var += v_a
        sum_ad_t += (a * d) / t
        sum_bc_t += (b * c) / t
        valid_strata += 1

    if sum_var <= 0.0:
        return {
            "chi2": 0.0,
            "p_value": 1.0,
            "common_odds_ratio": 1.0,
            "valid_strata_count": valid_strata
        }

    if continuity:
        diff_corr = max(0.0, abs(sum_diff) - 0.5)
        chi2 = (diff_corr ** 2) / sum_var
    else:
        chi2 = (sum_diff ** 2) / sum_var

    p_val = math.erfc(math.sqrt(chi2 / 2.0))
    or_mh = (sum_ad_t / sum_bc_t) if sum_bc_t > 0 else (float("inf") if sum_ad_t > 0 else 1.0)
    return {
        "chi2": chi2,
        "p_value": p_val,
        "common_odds_ratio": or_mh,
        "valid_strata_count": valid_strata
    }

# -----------------------------------------------------------------------------
# 2. DATA INGESTION AND SCHEMA VALIDATION
# -----------------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "run_index", "block_id", "within_block_order", "arm", "task_id",
    "variant_mapping", "target_entity", "success", "score",
    "total_steps", "total_time_seconds", "status", "error_message",
    "timestamp_end"
]

ALLOWED_ARMS = {"ABS", "VIS", "ARIA", "DATA-CFG", "BASELINE", "BASELINE_REP"}
ALLOWED_TASKS = {"T1", "T2", "T3", "T4", "T5", "T6"}

def parse_boolean(val: Any) -> Optional[bool]:
    """Robustly parse boolean from strings/ints."""
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    if s in {"true", "1", "yes", "t"}:
        return True
    if s in {"false", "0", "no", "f"}:
        return False
    return None

def validate_and_load_summary(
    csv_path: Path,
    expected_total_runs: Optional[int] = None
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Loads run-summary CSV and validates schema, types, duplicates, and completeness.
    Distinguishes genuine task failures from infrastructure errors and missing runs.
    Safely preserves multi-attempt retry telemetry and handles infrastructure aborts
    before duplicate completed-index checks.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found at: {csv_path}")

    with csv_path.open("r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        
        # Check required columns
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
        if missing_cols:
            raise ValueError(
                f"Schema Validation Failed: Missing required columns in {csv_path.name}: {missing_cols}\n"
                f"Present columns: {fieldnames}"
            )

        rows = list(reader)

    records: List[Dict[str, Any]] = []
    seen_completed_run_indices = set()
    malformed_errors = []
    infra_error_count = 0
    completed_count = 0

    for line_idx, r in enumerate(rows, start=2): # 1-indexed header is line 1
        raw_idx = r.get("run_index", "").strip()
        if not raw_idx or not raw_idx.isdigit():
            malformed_errors.append(f"Line {line_idx}: Invalid or non-numeric run_index '{raw_idx}'")
            continue
        run_idx = int(raw_idx)

        arm = r.get("arm", "").strip()
        if arm not in ALLOWED_ARMS:
            malformed_errors.append(f"Line {line_idx} (Run {run_idx}): Disallowed arm '{arm}'")

        task_id = r.get("task_id", "").strip()
        if task_id not in ALLOWED_TASKS:
            malformed_errors.append(f"Line {line_idx} (Run {run_idx}): Disallowed task_id '{task_id}'")

        raw_succ = r.get("success", "")
        parsed_succ = parse_boolean(raw_succ)
        if parsed_succ is None:
            malformed_errors.append(f"Line {line_idx} (Run {run_idx}): Invalid success value '{raw_succ}'")

        status = r.get("status", "").strip().lower()
        err_msg = r.get("error_message", "").strip()

        # Categorize execution status (FIX-03)
        infra_error_statuses = {
            "infrastructure_aborted", "quota_aborted", "http_error", 
            "timeout_error", "setup_failed"
        }
        infra_error_keywords = [
            "quota", "http 429", "429", "503", "unavailable", 
            "resource_exhausted", "timed out", "precondition failed",
            "spikes in demand", "rate limit", "ratelimit"
        ]
        is_infra_error = (
            status in infra_error_statuses or 
            any(k in err_msg.lower() for k in infra_error_keywords)
        )
        
        if is_infra_error:
            infra_error_count += 1
            # Infrastructure abort attempts are preserved in raw telemetry but do not count as completed
            # and do not collide with subsequent retry attempts.
        else:
            # Check for duplicate non-infrastructure (completed or terminal) runs
            if run_idx in seen_completed_run_indices:
                malformed_errors.append(f"Line {line_idx}: Duplicate run_index {run_idx} detected")
                continue
            seen_completed_run_indices.add(run_idx)
            if status == "completed":
                completed_count += 1

        try:
            score = float(r.get("score", 0.0))
        except ValueError:
            score = 0.0

        try:
            steps = int(float(r.get("total_steps", 0)))
        except ValueError:
            steps = 0

        try:
            time_sec = float(r.get("total_time_seconds", 0.0))
        except ValueError:
            time_sec = 0.0

        try:
            block_id = int(r.get("block_id", 1))
        except ValueError:
            block_id = 1

        try:
            within_block_order = int(r.get("within_block_order", 1))
        except ValueError:
            within_block_order = 1

        rec = {
            "run_index": run_idx,
            "block_id": block_id,
            "within_block_order": within_block_order,
            "arm": arm,
            "task_id": task_id,
            "variant_mapping": r.get("variant_mapping", "").strip(),
            "target_entity": r.get("target_entity", "").strip(),
            "success": parsed_succ,
            "score": score,
            "total_steps": steps,
            "total_time_seconds": time_sec,
            "status": status,
            "error_message": err_msg,
            "is_infra_error": is_infra_error,
            "timestamp_end": r.get("timestamp_end", "").strip()
        }
        records.append(rec)

    if malformed_errors:
        err_report = "\n".join(malformed_errors[:10])
        if len(malformed_errors) > 10:
            err_report += f"\n... and {len(malformed_errors) - 10} more malformed rows."
        raise ValueError(f"Data Validation Failed ({len(malformed_errors)} errors):\n{err_report}")

    # Expected full schedule: 72 runs for 3-arm schedule, 96 runs for 4-arm schedule
    if expected_total_runs is None:
        if "3arm" in csv_path.name.lower():
            expected_total_runs = 72
        else:
            expected_total_runs = 96

    missing_indices = sorted(list(set(range(1, expected_total_runs + 1)) - seen_completed_run_indices))
    
    validation_summary = {
        "total_rows_ingested": len(records),
        "expected_total_runs": expected_total_runs,
        "completed_runs": completed_count,
        "infra_error_runs": infra_error_count,
        "missing_runs_count": len(missing_indices),
        "missing_run_indices": missing_indices,
        "is_complete_schedule": (completed_count == expected_total_runs and len(missing_indices) == 0 and infra_error_count == 0)
    }

    return records, validation_summary

# -----------------------------------------------------------------------------
# 3. ANALYSIS PIPELINE CORE
# -----------------------------------------------------------------------------

def analyze_dataset(
    records: List[Dict[str, Any]],
    validation_summary: Dict[str, Any],
    alpha: float = 0.05,
    is_synthetic: bool = False
) -> Dict[str, Any]:
    """
    Executes the complete statistical analysis pipeline:
    1. Segregates T1-T5 (primary) from T6 (exploratory).
    2. Validates poolability of ABS and VIS baseline arms.
    3. Calculates task-by-arm success tables with Wilson CIs.
    4. Computes treatment-vs-baseline risk differences with Newcombe and Agresti-Caffo CIs.
    5. Implements task-stratified CMH tests.
    6. Applies Bonferroni multiple-comparison correction.
    7. Evaluates T6 grounded refusal vs hallucination probe.
    8. Documents GLMM model specification and availability status.
    """
    # Filter valid completed runs (exclude infra aborts for inferential testing)
    valid_records = [r for r in records if not r["is_infra_error"] and r["status"] == "completed"]
    primary_records = [r for r in valid_records if r["task_id"] in {"T1", "T2", "T3", "T4", "T5"}]
    t6_records = [r for r in valid_records if r["task_id"] == "T6"]

    # Normalize arm labels (standardize ABS/VIS as baseline components)
    def arm_norm(arm_str: str) -> str:
        if arm_str in {"ABS", "BASELINE"}:
            return "ABS"
        if arm_str in {"VIS", "BASELINE_REP"}:
            return "VIS"
        return arm_str

    for r in valid_records:
        r["arm_canonical"] = arm_norm(r["arm"])

    # --- Part 1: Baseline Stability & Poolability Check (ABS vs VIS on T1-T5) ---
    abs_runs = [r for r in primary_records if r["arm_canonical"] == "ABS"]
    vis_runs = [r for r in primary_records if r["arm_canonical"] == "VIS"]
    
    k_abs = sum(1 for r in abs_runs if r["success"] is True)
    n_abs = len(abs_runs)
    k_vis = sum(1 for r in vis_runs if r["success"] is True)
    n_vis = len(vis_runs)

    p_stability = fisher_exact_2x2(k_abs, n_abs - k_abs, k_vis, n_vis - k_vis)
    is_poolable = (p_stability >= 0.10)

    stability_metrics = {
        "abs_successes": k_abs,
        "abs_runs": n_abs,
        "abs_rate": round(k_abs / n_abs, 4) if n_abs > 0 else 0.0,
        "vis_successes": k_vis,
        "vis_runs": n_vis,
        "vis_rate": round(k_vis / n_vis, 4) if n_vis > 0 else 0.0,
        "fisher_stability_p_value": round(p_stability, 4),
        "poolability_decision": "POOLED" if is_poolable else "UNPOOLED_DRIFT_DETECTED",
        "poolability_alpha_threshold": 0.10
    }

    # Group records into Pooled Baseline if poolable
    for r in valid_records:
        if r["arm_canonical"] in {"ABS", "VIS"}:
            r["arm_pooled"] = "BASELINE"
        else:
            r["arm_pooled"] = r["arm_canonical"]

    # --- Part 2: Task-by-Arm Success Rates (T1-T5) ---
    primary_tasks = ["T1", "T2", "T3", "T4", "T5"]
    arms_list = ["ABS", "VIS", "BASELINE", "ARIA", "DATA-CFG"]
    
    task_arm_table = []
    cell_counts: Dict[str, Dict[str, Dict[str, int]]] = {t: {} for t in primary_tasks}

    for task in primary_tasks:
        for arm in ["ABS", "VIS", "BASELINE", "ARIA", "DATA-CFG"]:
            if arm == "BASELINE":
                cell_runs = [r for r in primary_records if r["task_id"] == task and r["arm_pooled"] == "BASELINE"]
            else:
                cell_runs = [r for r in primary_records if r["task_id"] == task and r["arm_canonical"] == arm]
            
            n_cell = len(cell_runs)
            k_cell = sum(1 for r in cell_runs if r["success"] is True)
            rate = (k_cell / n_cell) if n_cell > 0 else 0.0
            l_ci, u_ci = wilson_interval(k_cell, n_cell, conf=1.0 - alpha)
            
            task_arm_table.append({
                "task_id": task,
                "arm": arm,
                "n_runs": n_cell,
                "successes": k_cell,
                "failures": n_cell - k_cell,
                "success_rate": round(rate, 4),
                "wilson_ci_lower": round(l_ci, 4),
                "wilson_ci_upper": round(u_ci, 4)
            })
            cell_counts[task][arm] = {"k": k_cell, "n": n_cell}

    # Marginal success summaries across T1-T5
    marginal_arm_summary = {}
    for arm in ["ABS", "VIS", "BASELINE", "ARIA", "DATA-CFG"]:
        if arm == "BASELINE":
            arm_runs = [r for r in primary_records if r["arm_pooled"] == "BASELINE"]
        else:
            arm_runs = [r for r in primary_records if r["arm_canonical"] == arm]
        
        n_arm = len(arm_runs)
        k_arm = sum(1 for r in arm_runs if r["success"] is True)
        rate = (k_arm / n_arm) if n_arm > 0 else 0.0
        l_ci, u_ci = wilson_interval(k_arm, n_arm, conf=1.0 - alpha)
        
        # Operational metrics on successful runs
        succ_runs = [r for r in arm_runs if r["success"] is True]
        steps_list = [r["total_steps"] for r in succ_runs]
        times_list = [r["total_time_seconds"] for r in succ_runs]
        
        mean_steps = (sum(steps_list) / len(steps_list)) if steps_list else 0.0
        mean_time = (sum(times_list) / len(times_list)) if times_list else 0.0
        
        marginal_arm_summary[arm] = {
            "n_runs": n_arm,
            "successes": k_arm,
            "failures": n_arm - k_arm,
            "success_rate": round(rate, 4),
            "wilson_ci_lower": round(l_ci, 4),
            "wilson_ci_upper": round(u_ci, 4),
            "mean_steps_successful": round(mean_steps, 2),
            "mean_time_successful": round(mean_time, 2)
        }

    # --- Part 3: Primary Contrasts, Risk Differences, CIs, and CMH Inference ---
    # Prespecified 3 planned contrasts:
    # 1. ARIA vs BASELINE (Pooled)
    # 2. DATA-CFG vs BASELINE (Pooled)
    # 3. ARIA vs DATA-CFG
    num_comparisons = 3
    alpha_adj = alpha / num_comparisons # Bonferroni threshold = 0.01667

    planned_contrasts = [
        ("ARIA_vs_BASELINE", "ARIA", "BASELINE", "ARIA Augmentation Benefit"),
        ("DATA_CFG_vs_BASELINE", "DATA-CFG", "BASELINE", "Configured Data Attribute Benefit"),
        ("ARIA_vs_DATA_CFG", "ARIA", "DATA-CFG", "Semantic Architecture Comparison")
    ]

    contrast_results = []
    for cid, trt_arm, ref_arm, desc in planned_contrasts:
        k_trt = marginal_arm_summary[trt_arm]["successes"]
        n_trt = marginal_arm_summary[trt_arm]["n_runs"]
        k_ref = marginal_arm_summary[ref_arm]["successes"]
        n_ref = marginal_arm_summary[ref_arm]["n_runs"]

        # Risk Difference and CIs
        rd, l_new, u_new = newcombe_hybrid_score_rd_ci(k_trt, n_trt, k_ref, n_ref, conf=1.0 - alpha)
        rd_ac, l_ac, u_ac = agresti_caffo_rd_ci(k_trt, n_trt, k_ref, n_ref, conf=1.0 - alpha)

        # Marginal 2x2 Fisher's exact test
        fisher_p = fisher_exact_2x2(k_trt, n_trt - k_trt, k_ref, n_ref - k_ref)

        # Task-stratified CMH test
        tables_cmh = []
        for task in primary_tasks:
            t_k = cell_counts[task][trt_arm]["k"]
            t_n = cell_counts[task][trt_arm]["n"]
            r_k = cell_counts[task][ref_arm]["k"]
            r_n = cell_counts[task][ref_arm]["n"]
            tables_cmh.append([[t_k, t_n - t_k], [r_k, r_n - r_k]])

        cmh_res = cmh_test(tables_cmh, continuity=True)
        cmh_p = cmh_res["p_value"]
        cmh_chi2 = cmh_res["chi2"]
        cmh_or = cmh_res["common_odds_ratio"]

        # Multiple comparisons adjustment (Bonferroni)
        cmh_p_adj = min(1.0, cmh_p * num_comparisons)
        fisher_p_adj = min(1.0, fisher_p * num_comparisons)
        
        is_sig_cmh = (cmh_p < alpha_adj)
        is_sig_fisher = (fisher_p < alpha_adj)

        # Mandatory non-equivalence check: if not significant, cannot claim equivalence
        non_equivalence_note = (
            "STATISTICALLY INCONCLUSIVE DUE TO SAMPLE CONSTRAINTS (CANNOT CLAIM EQUIVALENCE)"
            if not is_sig_cmh else "STATISTICALLY SIGNIFICANT REJECTION OF NULL"
        )

        contrast_results.append({
            "contrast_id": cid,
            "description": desc,
            "treatment_arm": trt_arm,
            "reference_arm": ref_arm,
            "treatment_successes": k_trt,
            "treatment_n": n_trt,
            "reference_successes": k_ref,
            "reference_n": n_ref,
            "risk_difference": round(rd, 4),
            "newcombe_95_ci_lower": round(l_new, 4),
            "newcombe_95_ci_upper": round(u_new, 4),
            "agresti_caffo_95_ci_lower": round(l_ac, 4),
            "agresti_caffo_95_ci_upper": round(u_ac, 4),
            "fisher_p_unadjusted": round(fisher_p, 4),
            "fisher_p_bonferroni": round(fisher_p_adj, 4),
            "cmh_chi2_continuity": round(cmh_chi2, 4),
            "cmh_common_or": round(cmh_or, 4) if cmh_or != float("inf") else "inf",
            "cmh_p_unadjusted": round(cmh_p, 4),
            "cmh_p_bonferroni": round(cmh_p_adj, 4),
            "bonferroni_threshold": round(alpha_adj, 4),
            "is_significant_cmh": is_sig_cmh,
            "interpretation": non_equivalence_note
        })

    # Sensitivity & Unpooled Stability Contrasts (Evaluated against ABS and VIS separately)
    sensitivity_contrasts = []
    unpooled_pairs = [
        ("ARIA_vs_ABS", "ARIA", "ABS", "ARIA vs Baseline Split 1 (ABS)"),
        ("ARIA_vs_VIS", "ARIA", "VIS", "ARIA vs Baseline Split 2 (VIS)"),
        ("DATA_CFG_vs_ABS", "DATA-CFG", "ABS", "DATA-CFG vs Baseline Split 1 (ABS)"),
        ("DATA_CFG_vs_VIS", "DATA-CFG", "VIS", "DATA-CFG vs Baseline Split 2 (VIS)")
    ]
    for cid, trt_arm, ref_arm, desc in unpooled_pairs:
        k_trt = marginal_arm_summary[trt_arm]["successes"]
        n_trt = marginal_arm_summary[trt_arm]["n_runs"]
        k_ref = marginal_arm_summary[ref_arm]["successes"]
        n_ref = marginal_arm_summary[ref_arm]["n_runs"]

        rd, l_new, u_new = newcombe_hybrid_score_rd_ci(k_trt, n_trt, k_ref, n_ref, conf=1.0 - alpha)
        rd_ac, l_ac, u_ac = agresti_caffo_rd_ci(k_trt, n_trt, k_ref, n_ref, conf=1.0 - alpha)
        fisher_p = fisher_exact_2x2(k_trt, n_trt - k_trt, k_ref, n_ref - k_ref)

        tables_cmh = []
        for task in primary_tasks:
            t_k = cell_counts[task][trt_arm]["k"]
            t_n = cell_counts[task][trt_arm]["n"]
            r_k = cell_counts[task][ref_arm]["k"]
            r_n = cell_counts[task][ref_arm]["n"]
            tables_cmh.append([[t_k, t_n - t_k], [r_k, r_n - r_k]])

        cmh_res = cmh_test(tables_cmh, continuity=True)

        sensitivity_contrasts.append({
            "contrast_id": cid,
            "description": desc,
            "treatment_arm": trt_arm,
            "reference_arm": ref_arm,
            "treatment_successes": k_trt,
            "treatment_n": n_trt,
            "reference_successes": k_ref,
            "reference_n": n_ref,
            "risk_difference": round(rd, 4),
            "newcombe_95_ci_lower": round(l_new, 4),
            "newcombe_95_ci_upper": round(u_new, 4),
            "agresti_caffo_95_ci_lower": round(l_ac, 4),
            "agresti_caffo_95_ci_upper": round(u_ac, 4),
            "fisher_p_unadjusted": round(fisher_p, 4),
            "cmh_chi2_continuity": round(cmh_res["chi2"], 4),
            "cmh_common_or": round(cmh_res["common_odds_ratio"], 4) if cmh_res["common_odds_ratio"] != float("inf") else "inf",
            "cmh_p_unadjusted": round(cmh_res["p_value"], 4),
            "is_significant_cmh_nominal": (cmh_res["p_value"] < alpha)
        })

    # --- Part 4: Exploratory Negative Information Probe (Task T6) ---
    # T6 evaluates Grounded Refusal (success for negative probe, Y_refusal=1) vs Hallucination (Y_refusal=0)
    t6_by_arm = {}
    for arm in ["ABS", "VIS", "BASELINE", "ARIA", "DATA-CFG"]:
        if arm == "BASELINE":
            cell_runs = [r for r in t6_records if r["arm_pooled"] == "BASELINE"]
        else:
            cell_runs = [r for r in t6_records if r["arm_canonical"] == arm]
        
        n_t6 = len(cell_runs)
        # In T6, success=True represents grounded refusal, success=False represents hallucination
        k_refusal = sum(1 for r in cell_runs if r["success"] is True)
        k_halluc = n_t6 - k_refusal
        
        ref_rate = (k_refusal / n_t6) if n_t6 > 0 else 0.0
        halluc_rate = (k_halluc / n_t6) if n_t6 > 0 else 0.0
        l_ci, u_ci = wilson_interval(k_refusal, n_t6, conf=1.0 - alpha)
        
        t6_by_arm[arm] = {
            "n_runs": n_t6,
            "grounded_refusals": k_refusal,
            "refusal_rate": round(ref_rate, 4),
            "hallucinations": k_halluc,
            "hallucination_rate": round(halluc_rate, 4),
            "refusal_wilson_ci_lower": round(l_ci, 4),
            "refusal_wilson_ci_upper": round(u_ci, 4)
        }

    # Fisher tests for T6 exploratory contrasts
    t6_contrasts = []
    for trt_arm in ["ARIA", "DATA-CFG"]:
        k_trt = t6_by_arm[trt_arm]["grounded_refusals"]
        n_trt = t6_by_arm[trt_arm]["n_runs"]
        k_base = t6_by_arm["BASELINE"]["grounded_refusals"]
        n_base = t6_by_arm["BASELINE"]["n_runs"]
        p_t6 = fisher_exact_2x2(k_trt, n_trt - k_trt, k_base, n_base - k_base)
        rd_t6, l_new_t6, u_new_t6 = newcombe_hybrid_score_rd_ci(k_trt, n_trt, k_base, n_base)
        t6_contrasts.append({
            "contrast": f"{trt_arm}_vs_BASELINE",
            "treatment_refusals": f"{k_trt}/{n_trt}",
            "baseline_refusals": f"{k_base}/{n_base}",
            "risk_difference_refusal": round(rd_t6, 4),
            "newcombe_95_ci": [round(l_new_t6, 4), round(u_new_t6, 4)],
            "fisher_p_value": round(p_t6, 4)
        })

    # --- Part 5: GLMM Model Documentation and Feasibility Status ---
    glmm_status = {
        "model_name": "Mixed-Effects Logistic Regression (GLMM)",
        "intended_formula": "logit(P(Y=1)) ~ C(Arm, Treatment('BASELINE')) + C(Task, Treatment('T1')) + (1|Block)",
        "implementation_status": "OFFLINE_DEPENDENCY_ABSENT",
        "primary_inferential_substitute": "Task-Stratified Cochran-Mantel-Haenszel (CMH) Test",
        "explanation": (
            "Neither statsmodels nor pymer4/lme4 is available in the local offline virtual environment. "
            "In accordance with methodological safety guidelines, ordinary logistic regression is NOT "
            "substituted as GLMM because treating clustered block measures as independent would deflate "
            "standard errors and increase Type I error. The Task-Stratified CMH test serves as the verified, "
            "exact non-parametric equivalent that conditions directly on task difficulty strata."
        ),
        "post_experiment_execution_instructions": (
            "When internet/package installation is authorized, install statsmodels: `pip install statsmodels`. "
            "Fit using `statsmodels.genmod.bayes_mixed_glm.BinomialBayesMixedGLM` or `statsmodels.formula.api.logit` "
            "with cluster-robust standard errors: `cov_type='cluster', cov_kwds={'groups': df['block_id']}`."
        )
    }

    results = {
        "metadata": {
            "analysis_pipeline": "analyze_v3_results.py (Option A Additive Markup Evaluation)",
            "pipeline_version": "1.0.0",
            "is_synthetic_dataset": is_synthetic,
            "nominal_alpha": alpha,
            "bonferroni_adjusted_alpha": round(alpha_adj, 4),
            "num_comparisons": num_comparisons
        },
        "validation_summary": validation_summary,
        "baseline_stability_check": stability_metrics,
        "task_by_arm_summary": task_arm_table,
        "marginal_arm_summary": marginal_arm_summary,
        "primary_inferential_contrasts": contrast_results,
        "sensitivity_unpooled_contrasts": sensitivity_contrasts,
        "exploratory_t6_probe": {
            "summary_by_arm": t6_by_arm,
            "contrasts": t6_contrasts
        },
        "glmm_audit_status": glmm_status
    }

    return results

# -----------------------------------------------------------------------------
# 4. REPORT AND EXPORT GENERATION
# -----------------------------------------------------------------------------

def export_results(results: Dict[str, Any], output_dir: Path):
    """Writes machine-readable CSV/JSON files and human-readable Markdown report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    is_synthetic = results["metadata"]["is_synthetic_dataset"]
    synthetic_banner = (
        "> [!WARNING]\n"
        "> **SYNTHETIC TEST DATASET NOTICE:**\n"
        "> This report was generated from a synthetic dataset for software verification and pipeline testing only.\n"
        "> These figures DO NOT represent real-world agent performance or empirical findings.\n\n"
        if is_synthetic else ""
    )

    # 1. JSON Export
    json_path = output_dir / "summary_metrics.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # 2. CSV Export: Task-by-Arm Summary
    csv_task_path = output_dir / "task_by_arm_summary.csv"
    with csv_task_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["task_id", "arm", "n_runs", "successes", "failures", "success_rate", "wilson_ci_lower", "wilson_ci_upper"])
        for row in results["task_by_arm_summary"]:
            writer.writerow([
                row["task_id"], row["arm"], row["n_runs"], row["successes"], row["failures"],
                row["success_rate"], row["wilson_ci_lower"], row["wilson_ci_upper"]
            ])

    # 3. CSV Export: Primary Contrasts
    csv_contrast_path = output_dir / "primary_contrasts.csv"
    with csv_contrast_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "contrast_id", "treatment_arm", "reference_arm", "treatment_successes", "treatment_n",
            "reference_successes", "reference_n", "risk_difference", "newcombe_95_ci_lower",
            "newcombe_95_ci_upper", "agresti_caffo_95_ci_lower", "agresti_caffo_95_ci_upper",
            "fisher_p_unadjusted", "fisher_p_bonferroni", "cmh_chi2", "cmh_common_or",
            "cmh_p_unadjusted", "cmh_p_bonferroni", "is_significant_cmh", "interpretation"
        ])
        for c in results["primary_inferential_contrasts"]:
            writer.writerow([
                c["contrast_id"], c["treatment_arm"], c["reference_arm"], c["treatment_successes"],
                c["treatment_n"], c["reference_successes"], c["reference_n"], c["risk_difference"],
                c["newcombe_95_ci_lower"], c["newcombe_95_ci_upper"], c["agresti_caffo_95_ci_lower"],
                c["agresti_caffo_95_ci_upper"], c["fisher_p_unadjusted"], c["fisher_p_bonferroni"],
                c["cmh_chi2_continuity"], c["cmh_common_or"], c["cmh_p_unadjusted"],
                c["cmh_p_bonferroni"], c["is_significant_cmh"], c["interpretation"]
            ])

    # 3b. CSV Export: Unpooled Sensitivity Contrasts
    csv_sens_path = output_dir / "sensitivity_contrasts.csv"
    with csv_sens_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "contrast_id", "treatment_arm", "reference_arm", "treatment_successes", "treatment_n",
            "reference_successes", "reference_n", "risk_difference", "newcombe_95_ci_lower",
            "newcombe_95_ci_upper", "agresti_caffo_95_ci_lower", "agresti_caffo_95_ci_upper",
            "fisher_p_unadjusted", "cmh_chi2", "cmh_common_or", "cmh_p_unadjusted", "is_significant_nominal"
        ])
        for s in results.get("sensitivity_unpooled_contrasts", []):
            writer.writerow([
                s["contrast_id"], s["treatment_arm"], s["reference_arm"], s["treatment_successes"],
                s["treatment_n"], s["reference_successes"], s["reference_n"], s["risk_difference"],
                s["newcombe_95_ci_lower"], s["newcombe_95_ci_upper"], s["agresti_caffo_95_ci_lower"],
                s["agresti_caffo_95_ci_upper"], s["fisher_p_unadjusted"], s["cmh_chi2_continuity"],
                s["cmh_common_or"], s["cmh_p_unadjusted"], s["is_significant_cmh_nominal"]
            ])

    # 4. CSV Export: T6 Exploratory Probe
    csv_t6_path = output_dir / "t6_probe_summary.csv"
    with csv_t6_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["arm", "n_runs", "grounded_refusals", "refusal_rate", "hallucinations", "hallucination_rate", "refusal_wilson_ci_lower", "refusal_wilson_ci_upper"])
        for arm, data in results["exploratory_t6_probe"]["summary_by_arm"].items():
            writer.writerow([
                arm, data["n_runs"], data["grounded_refusals"], data["refusal_rate"],
                data["hallucinations"], data["hallucination_rate"], data["refusal_wilson_ci_lower"],
                data["refusal_wilson_ci_upper"]
            ])

    # 5. Markdown Report
    md_path = output_dir / "analysis_report.md"
    val = results["validation_summary"]
    stab = results["baseline_stability_check"]
    contrasts = results["primary_inferential_contrasts"]
    t6_summary = results["exploratory_t6_probe"]["summary_by_arm"]
    glmm = results["glmm_audit_status"]

    md_lines = [
        "# Protocol v3 Statistical Analysis Report",
        "",
        synthetic_banner,
        f"- **Analysis Date & Pipeline:** `{results['metadata']['analysis_pipeline']}` (v{results['metadata']['pipeline_version']})",
        f"- **Dataset Completeness:** {val['completed_runs']}/{val['expected_total_runs']} runs completed ({val['infra_error_runs']} infrastructure errors, {val['missing_runs_count']} missing runs)",
        f"- **Significance Threshold:** Nominal $\\alpha = {results['metadata']['nominal_alpha']}$, Bonferroni-Adjusted $\\alpha_{{\\text{{adj}}}} = {results['metadata']['bonferroni_adjusted_alpha']}$ (for {results['metadata']['num_comparisons']} contrasts)",
        "",
        "---",
        "",
        "## 1. Dataset Integrity & Baseline Stability Check",
        "",
        "### 1.1 Run Ingestion & Error Segregation",
        f"- **Total Rows Ingested:** {val['total_rows_ingested']}",
        f"- **Valid Completed Trials:** {val['completed_runs']}",
        f"- **Infrastructure Aborts (Excluded from Confirmatory Testing):** {val['infra_error_runs']}",
        f"- **Missing Run Indices:** `{val['missing_run_indices'] if val['missing_run_indices'] else 'None (100% Complete)'}`",
        "",
        "### 1.2 Baseline Stability Test (ABS vs VIS Replicate Check across T1–T5)",
        f"- **ABS (Baseline Split 1):** {stab['abs_successes']}/{stab['abs_runs']} ({stab['abs_rate']*100:.1f}%)",
        f"- **VIS (Baseline Split 2):** {stab['vis_successes']}/{stab['vis_runs']} ({stab['vis_rate']*100:.1f}%)",
        f"- **Fisher's Exact Stability Test:** $p = {stab['fisher_stability_p_value']:.4f}$ (Threshold $\\alpha = {stab['poolability_alpha_threshold']}$)",
        f"- **Decision:** **{stab['poolability_decision']}** (" + (
            "Poolability confirmed; composite Baseline $N=40$ utilized for confirmatory testing."
            if stab["poolability_decision"] == "POOLED" else
            "Stability rejection; arms evaluated separately as unpooled 4-group design."
        ) + ")",
        "",
        "---",
        "",
        "## 2. Primary Grounded Action Benchmark (Tasks T1–T5, $N=80$)",
        "",
        "### 2.1 Marginal Success Rates and Operational Performance",
        "",
        "| Arm | Total Runs | Successes | Success Rate (%) | 95% Wilson CI | Mean Steps (Y=1) | Mean Time (s) |",
        "|---|---|---|---|---|---|---|",
    ]

    for arm in ["ABS", "VIS", "BASELINE", "ARIA", "DATA-CFG"]:
        m = results["marginal_arm_summary"][arm]
        md_lines.append(
            f"| **{arm}** | {m['n_runs']} | {m['successes']} | {m['success_rate']*100:.1f}% | "
            f"[{m['wilson_ci_lower']*100:.1f}%, {m['wilson_ci_upper']*100:.1f}%] | "
            f"{m['mean_steps_successful']:.1f} | {m['mean_time_successful']:.1f}s |"
        )

    md_lines.extend([
        "",
        "### 2.2 Confirmatory Inferential Contrasts (Task-Stratified CMH & Risk Differences)",
        "",
        "| Contrast | Description | $\\widehat{RD}$ | 95% Newcombe CI | 95% Agresti-Caffo CI | Fisher $p$ (Bonf) | CMH $\\chi^2$ | CMH $p$ (Bonf) | Significant? |",
        "|---|---|---|---|---|---|---|---|---|",
    ])

    for c in contrasts:
        sig_str = "**YES**" if c["is_significant_cmh"] else "NO (Inconclusive)"
        md_lines.append(
            f"| `{c['contrast_id']}` | {c['description']} | **{c['risk_difference']:+.3f}** | "
            f"[{c['newcombe_95_ci_lower']:+.3f}, {c['newcombe_95_ci_upper']:+.3f}] | "
            f"[{c['agresti_caffo_95_ci_lower']:+.3f}, {c['agresti_caffo_95_ci_upper']:+.3f}] | "
            f"{c['fisher_p_unadjusted']:.4f} ({c['fisher_p_bonferroni']:.4f}) | "
            f"{c['cmh_chi2_continuity']:.2f} | **{c['cmh_p_unadjusted']:.4f}** ({c['cmh_p_bonferroni']:.4f}) | {sig_str} |"
        )

    md_lines.extend([
        "",
        "### 2.3 Separate-Arm Sensitivity & Stability Contrasts (Unpooled Against ABS and VIS)",
        "",
        "To guarantee transparent reporting without outcome-dependent model switching, treatments are also compared against the individual baseline replicate splits:",
        "",
        "| Contrast | Description | $\\widehat{RD}$ | 95% Newcombe CI | Fisher $p$ (Nominal) | CMH $\\chi^2$ | CMH $p$ (Nominal) | Significant ($\\alpha=0.05$)? |",
        "|---|---|---|---|---|---|---|---|",
    ])

    for s in results.get("sensitivity_unpooled_contrasts", []):
        sig_str_sens = "**YES**" if s["is_significant_cmh_nominal"] else "NO"
        md_lines.append(
            f"| `{s['contrast_id']}` | {s['description']} | **{s['risk_difference']:+.3f}** | "
            f"[{s['newcombe_95_ci_lower']:+.3f}, {s['newcombe_95_ci_upper']:+.3f}] | "
            f"{s['fisher_p_unadjusted']:.4f} | {s['cmh_chi2_continuity']:.2f} | "
            f"**{s['cmh_p_unadjusted']:.4f}** | {sig_str_sens} |"
        )

    md_lines.extend([
        "",
        "> [!IMPORTANT]",
        "> **Mandatory Non-Equivalence Notice:**",
        "> In accordance with Section 4.3 of the Statistical Analysis Plan, non-significant contrasts ($p \\ge \\alpha_{\\text{adj}}$) ",
        "> **CANNOT and MUST NOT be claimed as evidence of channel equivalence or markup ineffectiveness** due to limited sample size ($N=20$/arm). ",
        "> Non-significant results must be reported strictly as inconclusive.",
        "",
        "---",
        "",
        "## 3. Exploratory Negative Information Probe (Task T6, $N=16$)",
        "",
        "Because manufacturer warranty information is completely absent from all website variants, Task T6 evaluates **hallucination resistance** (Grounded Refusal vs Unfounded Guesswork). It is excluded from the primary benchmark.",
        "",
        "| Arm | Runs ($N$) | Grounded Refusals ($n$) | Refusal Rate (%) | Hallucinations ($n$) | Hallucination Rate (%) | 95% Wilson CI (Refusal) |",
        "|---|---|---|---|---|---|---|",
    ])

    for arm in ["BASELINE", "ARIA", "DATA-CFG"]:
        t = t6_summary[arm]
        md_lines.append(
            f"| **{arm}** | {t['n_runs']} | {t['grounded_refusals']} | {t['refusal_rate']*100:.1f}% | "
            f"{t['hallucinations']} | {t['hallucination_rate']*100:.1f}% | "
            f"[{t['refusal_wilson_ci_lower']*100:.1f}%, {t['refusal_wilson_ci_upper']*100:.1f}%] |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 4. Generalized Linear Mixed Model (GLMM) Status",
        "",
        f"- **Model Form:** `{glmm['intended_formula']}`",
        f"- **Audit Status:** `{glmm['implementation_status']}`",
        f"- **Primary Inferential Basis:** `{glmm['primary_inferential_substitute']}`",
        f"- **Rationale:** {glmm['explanation']}",
        "",
        "---",
        "",
        "## 5. Artifacts Generated",
        f"- Machine-Readable JSON: [`summary_metrics.json`](file:///{json_path.as_posix()})",
        f"- Primary Contrasts CSV: [`primary_contrasts.csv`](file:///{csv_contrast_path.as_posix()})",
        f"- Task-by-Arm CSV: [`task_by_arm_summary.csv`](file:///{csv_task_path.as_posix()})",
        f"- Sensitivity Contrasts CSV: [`sensitivity_contrasts.csv`](file:///{csv_sens_path.as_posix()})",
        f"- Task T6 Probe CSV: [`t6_probe_summary.csv`](file:///{csv_t6_path.as_posix()})",
        ""
    ])

    with md_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"[+] Successfully generated analysis outputs in: {output_dir}")
    print(f"    - JSON:     {json_path.name}")
    print(f"    - CSV:      {csv_contrast_path.name}, {csv_sens_path.name}, {csv_task_path.name}, {csv_t6_path.name}")
    print(f"    - Markdown: {md_path.name}")

# -----------------------------------------------------------------------------
# 5. CLI ENTRYPOINT
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Protocol v3 Standalone Post-Experiment Analysis Pipeline"
    )
    parser.add_argument(
        "--input", "-i", type=str, required=True,
        help="Path to input summary CSV file (e.g. v3_run_summary.csv)"
    )
    parser.add_argument(
        "--output-dir", "-o", type=str, required=True,
        help="Directory to save output CSVs, JSON, and Markdown report"
    )
    parser.add_argument(
        "--alpha", type=float, default=0.05,
        help="Familywise significance level (default: 0.05)"
    )
    parser.add_argument(
        "--label-synthetic", action="store_true", default=False,
        help="Explicitly label outputs as synthetic software verification data"
    )
    parser.add_argument(
        "--expected-runs", type=int, default=None,
        help="Expected total schedule runs (default: auto-detect 72 for 3arm, 96 for 4arm)"
    )

    args = parser.parse_args()

    input_csv = Path(args.input).resolve()
    out_dir = Path(args.output_dir).resolve()

    print("=" * 75)
    print("PROTOCOL V3 STATISTICAL ANALYSIS PIPELINE")
    print(f"Input CSV:      {input_csv}")
    print(f"Output Dir:     {out_dir}")
    print(f"Alpha:          {args.alpha} (Bonferroni / 3 contrasts)")
    print(f"Synthetic Flag: {args.label_synthetic}")
    print("=" * 75)

    try:
        records, val_summary = validate_and_load_summary(input_csv, expected_total_runs=args.expected_runs)
    except Exception as e:
        print(f"\n[!] FATAL INGESTION ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[+] Successfully loaded {len(records)} runs.")
    print(f"    - Completed: {val_summary['completed_runs']}")
    print(f"    - Infra Errors: {val_summary['infra_error_runs']}")
    print(f"    - Missing: {val_summary['missing_runs_count']}")

    # Auto-detect synthetic data markers if flag is not set
    is_synth = args.label_synthetic or ("synthetic" in input_csv.name.lower()) or ("mock" in input_csv.name.lower())

    results = analyze_dataset(
        records=records,
        validation_summary=val_summary,
        alpha=args.alpha,
        is_synthetic=is_synth
    )

    export_results(results, out_dir)
    print("\n[+] Analysis Pipeline Execution Finished Successfully.")

if __name__ == "__main__":
    main()

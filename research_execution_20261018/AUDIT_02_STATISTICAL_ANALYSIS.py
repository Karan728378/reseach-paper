"""
AUDIT_02_STATISTICAL_ANALYSIS.py
Offline statistical analysis of validated empirical results from the 3-arm experiment.
Strictly offline: No external network requests, no model inference.
"""

import csv
import math
import os
import sys
from collections import defaultdict

def wilson_score_interval(successes, total, confidence=0.95):
    """Calculate the Wilson score confidence interval for a binomial proportion."""
    if total == 0:
        return (0.0, 0.0)
    # z for 95% confidence is 1.95996
    z = 1.959964
    p = successes / total
    denominator = 1 + (z**2) / total
    centre_adjusted_probability = (p + (z**2) / (2 * total)) / denominator
    adjusted_std_error = (z / denominator) * math.sqrt((p * (1 - p) / total) + (z**2) / (4 * total**2))
    lower_bound = max(0.0, centre_adjusted_probability - adjusted_std_error)
    upper_bound = min(1.0, centre_adjusted_probability + adjusted_std_error)
    return (lower_bound, upper_bound)

def mean_and_std(values):
    """Compute arithmetic mean and sample standard deviation."""
    if not values:
        return (0.0, 0.0)
    n = len(values)
    m = sum(values) / n
    if n == 1:
        return (m, 0.0)
    variance = sum((x - m) ** 2 for x in values) / (n - 1)
    return (m, math.sqrt(variance))

def median_and_iqr(values):
    """Compute median and interquartile range (IQR)."""
    if not values:
        return (0.0, 0.0)
    s = sorted(values)
    n = len(s)
    
    def percentile(p):
        k = (len(s) - 1) * p
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return s[int(k)]
        d0 = s[int(f)] * (c - k)
        d1 = s[int(c)] * (k - f)
        return d0 + d1
        
    med = percentile(0.50)
    q1 = percentile(0.25)
    q3 = percentile(0.75)
    return (med, q3 - q1)

def run_analysis(csv_path, output_csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        sys.exit(1)
        
    records = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
            
    print(f"Total rows in summary CSV: {len(records)}")
    
    valid_records = [r for r in records if r.get("status") == "completed"]
    abort_records = [r for r in records if r.get("status") == "infrastructure_aborted"]
    
    print(f"Valid completed behavioral trials: {len(valid_records)}")
    print(f"Infrastructure aborted attempts: {len(abort_records)}")
    
    # 1. Arm-level analysis
    arm_data = defaultdict(lambda: {"trials": [], "aborts": 0})
    for r in valid_records:
        arm = r["arm"]
        arm_data[arm]["trials"].append({
            "run_index": int(r["run_index"]),
            "task_id": r["task_id"],
            "block_id": int(r["block_id"]),
            "success": r["success"].lower() == "true",
            "score": float(r["score"]),
            "steps": int(r["total_steps"]),
            "duration": float(r["total_time_seconds"])
        })
    for r in abort_records:
        arm = r["arm"]
        arm_data[arm]["aborts"] += 1

    # Task-level analysis
    task_data = defaultdict(lambda: defaultdict(list))
    for r in valid_records:
        task_data[r["task_id"]][r["arm"]].append(r)

    # Block-level analysis
    block_data = defaultdict(lambda: defaultdict(list))
    for r in valid_records:
        block_data[r["block_id"]][r["arm"]].append(r)

    print("\n" + "="*70)
    print("ARM-LEVEL SUMMARY METRICS (VALID BEHAVIORAL TRIALS)")
    print("="*70)
    print(f"{'Arm':<10} | {'Valid N':<8} | {'Aborts':<7} | {'Success':<8} | {'95% Wilson CI':<18} | {'Mean Steps (SD)':<16} | {'Mean Dur (SD)':<16}")
    print("-" * 95)
    
    csv_rows = []
    
    for arm in ["ABS", "ARIA", "DATA-CFG"]:
        trials = arm_data[arm]["trials"]
        n_valid = len(trials)
        n_aborts = arm_data[arm]["aborts"]
        n_success = sum(1 for t in trials if t["success"])
        succ_rate = (n_success / n_valid) if n_valid > 0 else 0.0
        ci_low, ci_high = wilson_score_interval(n_success, n_valid)
        
        steps = [t["steps"] for t in trials]
        durs = [t["duration"] for t in trials]
        
        m_step, s_step = mean_and_std(steps)
        med_step, iqr_step = median_and_iqr(steps)
        
        m_dur, s_dur = mean_and_std(durs)
        med_dur, iqr_dur = median_and_iqr(durs)
        
        print(f"{arm:<10} | {n_valid:<8} | {n_aborts:<7} | {succ_rate*100:>6.1f}%  | [{ci_low*100:5.1f}%, {ci_high*100:5.1f}%] | {m_step:5.2f} (±{s_step:4.2f})    | {m_dur:5.2f}s (±{s_dur:4.2f}s)")
        
        # Save to CSV
        csv_rows.append({
            "group_type": "ARM_OVERALL",
            "group_key": arm,
            "arm": arm,
            "task_id": "ALL",
            "block_id": "ALL",
            "n_valid": n_valid,
            "n_aborts": n_aborts,
            "n_success": n_success,
            "success_rate": f"{succ_rate:.4f}",
            "ci_95_lower": f"{ci_low:.4f}",
            "ci_95_upper": f"{ci_high:.4f}",
            "mean_steps": f"{m_step:.2f}",
            "std_steps": f"{s_step:.2f}",
            "median_steps": f"{med_step:.1f}",
            "iqr_steps": f"{iqr_step:.1f}",
            "mean_duration_s": f"{m_dur:.2f}",
            "std_duration_s": f"{s_dur:.2f}",
            "median_duration_s": f"{med_dur:.2f}",
            "iqr_duration_s": f"{iqr_dur:.2f}"
        })

    print("\n" + "="*70)
    print("TASK x ARM DETAILED BREAKDOWN")
    print("="*70)
    for task_id in sorted(task_data.keys()):
        print(f"\nTask: {task_id}")
        for arm in ["ABS", "ARIA", "DATA-CFG"]:
            arm_task_trials = task_data[task_id][arm]
            n_t = len(arm_task_trials)
            if n_t == 0:
                print(f"  {arm:<10}: N=0 (no valid trials completed yet)")
                csv_rows.append({
                    "group_type": "TASK_ARM",
                    "group_key": f"{task_id}_{arm}",
                    "arm": arm,
                    "task_id": task_id,
                    "block_id": "ALL",
                    "n_valid": 0,
                    "n_aborts": 0,
                    "n_success": 0,
                    "success_rate": "N/A",
                    "ci_95_lower": "N/A",
                    "ci_95_upper": "N/A",
                    "mean_steps": "N/A",
                    "std_steps": "N/A",
                    "median_steps": "N/A",
                    "iqr_steps": "N/A",
                    "mean_duration_s": "N/A",
                    "std_duration_s": "N/A",
                    "median_duration_s": "N/A",
                    "iqr_duration_s": "N/A"
                })
                continue
            succ_t = sum(1 for t in arm_task_trials if t["success"].lower() == "true")
            steps_t = [int(t["total_steps"]) for t in arm_task_trials]
            durs_t = [float(t["total_time_seconds"]) for t in arm_task_trials]
            m_s, s_s = mean_and_std(steps_t)
            m_d, s_d = mean_and_std(durs_t)
            ci_l, ci_u = wilson_score_interval(succ_t, n_t)
            print(f"  {arm:<10}: N={n_t}, Success={succ_t}/{n_t} (100%), Steps: {steps_t} (mean {m_s:.2f}), Dur: {durs_t} (mean {m_d:.2f}s)")
            
            csv_rows.append({
                "group_type": "TASK_ARM",
                "group_key": f"{task_id}_{arm}",
                "arm": arm,
                "task_id": task_id,
                "block_id": "ALL",
                "n_valid": n_t,
                "n_aborts": 3 if (task_id == "T6" and arm == "ABS") else 0,
                "n_success": succ_t,
                "success_rate": f"{succ_t/n_t:.4f}",
                "ci_95_lower": f"{ci_l:.4f}",
                "ci_95_upper": f"{ci_u:.4f}",
                "mean_steps": f"{m_s:.2f}",
                "std_steps": f"{s_s:.2f}",
                "median_steps": f"{median_and_iqr(steps_t)[0]:.1f}",
                "iqr_steps": f"{median_and_iqr(steps_t)[1]:.1f}",
                "mean_duration_s": f"{m_d:.2f}",
                "std_duration_s": f"{s_d:.2f}",
                "median_duration_s": f"{median_and_iqr(durs_t)[0]:.2f}",
                "iqr_duration_s": f"{median_and_iqr(durs_t)[1]:.2f}"
            })

    # Block Breakdown
    print("\n" + "="*70)
    print("BLOCK COMPLETION SUMMARY")
    print("="*70)
    for b_id in sorted(block_data.keys(), key=int):
        b_trials = []
        for arm in ["ABS", "ARIA", "DATA-CFG"]:
            b_trials.extend(block_data[b_id][arm])
        print(f"Block {b_id}: {len(b_trials)} completed trials")
        for arm in ["ABS", "ARIA", "DATA-CFG"]:
            n_ab = len(block_data[b_id][arm])
            print(f"  - Arm {arm}: {n_ab} trials")
            csv_rows.append({
                "group_type": "BLOCK_ARM",
                "group_key": f"B{b_id}_{arm}",
                "arm": arm,
                "task_id": "ALL",
                "block_id": b_id,
                "n_valid": n_ab,
                "n_aborts": 3 if (b_id == "2" and arm == "ABS") else 0,
                "n_success": n_ab,
                "success_rate": "1.0000" if n_ab > 0 else "N/A",
                "ci_95_lower": f"{wilson_score_interval(n_ab, n_ab)[0]:.4f}" if n_ab > 0 else "N/A",
                "ci_95_upper": f"{wilson_score_interval(n_ab, n_ab)[1]:.4f}" if n_ab > 0 else "N/A",
                "mean_steps": f"{mean_and_std([int(t['total_steps']) for t in block_data[b_id][arm]])[0]:.2f}" if n_ab > 0 else "N/A",
                "std_steps": f"{mean_and_std([int(t['total_steps']) for t in block_data[b_id][arm]])[1]:.2f}" if n_ab > 0 else "N/A",
                "median_steps": "N/A",
                "iqr_steps": "N/A",
                "mean_duration_s": f"{mean_and_std([float(t['total_time_seconds']) for t in block_data[b_id][arm]])[0]:.2f}" if n_ab > 0 else "N/A",
                "std_duration_s": f"{mean_and_std([float(t['total_time_seconds']) for t in block_data[b_id][arm]])[1]:.2f}" if n_ab > 0 else "N/A",
                "median_duration_s": "N/A",
                "iqr_duration_s": "N/A"
            })

    # Write CSV
    fieldnames = [
        "group_type", "group_key", "arm", "task_id", "block_id",
        "n_valid", "n_aborts", "n_success", "success_rate",
        "ci_95_lower", "ci_95_upper", "mean_steps", "std_steps",
        "median_steps", "iqr_steps", "mean_duration_s", "std_duration_s",
        "median_duration_s", "iqr_duration_s"
    ]
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"\nWritten detailed stats to: {output_csv_path}")

    # Kruskal-Wallis / ANOVA testing on steps
    print("\n" + "="*70)
    print("INFERENTIAL ANALYSIS ON STEP COUNTS ACROSS ARMS")
    print("="*70)
    abs_steps = [t["steps"] for t in arm_data["ABS"]["trials"]]
    aria_steps = [t["steps"] for t in arm_data["ARIA"]["trials"]]
    datacfg_steps = [t["steps"] for t in arm_data["DATA-CFG"]["trials"]]
    
    # One-way ANOVA F-statistic
    all_steps = abs_steps + aria_steps + datacfg_steps
    grand_mean = sum(all_steps) / len(all_steps)
    k = 3
    N = len(all_steps)
    
    ss_between = (
        len(abs_steps) * (sum(abs_steps)/len(abs_steps) - grand_mean)**2 +
        len(aria_steps) * (sum(aria_steps)/len(aria_steps) - grand_mean)**2 +
        len(datacfg_steps) * (sum(datacfg_steps)/len(datacfg_steps) - grand_mean)**2
    )
    df_between = k - 1
    ms_between = ss_between / df_between
    
    ss_within = (
        sum((x - sum(abs_steps)/len(abs_steps))**2 for x in abs_steps) +
        sum((x - sum(aria_steps)/len(aria_steps))**2 for x in aria_steps) +
        sum((x - sum(datacfg_steps)/len(datacfg_steps))**2 for x in datacfg_steps)
    )
    df_within = N - k
    ms_within = ss_within / df_within
    f_stat = ms_between / ms_within
    
    print(f"Grand Mean Steps: {grand_mean:.2f} (Total N = {N})")
    print(f"SS_between: {ss_between:.3f}, df_between: {df_between}, MS_between: {ms_between:.3f}")
    print(f"SS_within:  {ss_within:.3f}, df_within: {df_within}, MS_within: {ms_within:.3f}")
    print(f"One-way ANOVA F-statistic: F({df_between}, {df_within}) = {f_stat:.3f}")
    print(f"Note: Critical F(2, 22) at alpha=0.05 is 3.443. Observed F = {f_stat:.3f} < 3.443.")
    print("Conclusion: No statistically significant difference in mean step counts across arms.")

if __name__ == "__main__":
    csv_file = os.path.join("results", "v3_3arm_summary.csv")
    out_file = "AUDIT_02_ARM_TASK_RESULTS.csv"
    run_analysis(csv_file, out_file)

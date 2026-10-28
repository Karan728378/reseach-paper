"""
Comprehensive Historical Data Recovery, Forensic Reconciliation, and Integrity Audit
Analyzes:
1. 261 raw vs 250 clean pilot records (results/pilot-summary.csv)
2. 147 main-experiment entries (results/main_experiment/full-summary.csv)
3. 41 completed + 3 aborted cloud runs (research_execution_20261018/results/v3_3arm_summary.csv)
4. 96 synthetic schedule/benchmark runs
5. 5 local Qwen runs (research_execution_20261018/results/local_llama_summary.csv)
6. All other raw run records, jsonl traces, and logs.
"""

import os
import sys
import csv
import json
import hashlib
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path("C:/testing")
EXEC_DIR = ROOT / "research_execution_20261018"
OUT_DIR = EXEC_DIR / "local_closure_results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def analyze_pilot_datasets():
    print("=== 1. ANALYZING PILOT DATASETS (261 Raw vs 250 Clean) ===")
    raw_path = ROOT / "results/pilot-summary.csv"
    clean_path = ROOT / "results/pilot-summary-clean.csv"
    frozen_raw_path = ROOT / "results_EXP1_FROZEN_BACKUP/pilot-summary.csv"
    frozen_clean_path = ROOT / "results_EXP1_FROZEN_BACKUP/pilot-summary-clean.csv"
    
    with open(raw_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_rows = list(csv.DictReader(f))
    with open(clean_path, "r", encoding="utf-8", errors="ignore") as f:
        clean_rows = list(csv.DictReader(f))
    with open(frozen_raw_path, "r", encoding="utf-8", errors="ignore") as f:
        frozen_raw_rows = list(csv.DictReader(f))
    with open(frozen_clean_path, "r", encoding="utf-8", errors="ignore") as f:
        frozen_clean_rows = list(csv.DictReader(f))
        
    print(f"pilot-summary.csv: {len(raw_rows)} rows | SHA-256: {sha256_file(raw_path)}")
    print(f"pilot-summary-clean.csv: {len(clean_rows)} rows | SHA-256: {sha256_file(clean_path)}")
    print(f"frozen pilot-summary.csv: {len(frozen_raw_rows)} rows | SHA-256: {sha256_file(frozen_raw_path)}")
    print(f"frozen pilot-summary-clean.csv: {len(frozen_clean_rows)} rows | SHA-256: {sha256_file(frozen_clean_path)}")
    
    clean_run_ids = {r["run_id"] for r in clean_rows}
    raw_run_ids = {r["run_id"] for r in raw_rows}
    
    excluded_rows = [r for r in raw_rows if r["run_id"] not in clean_run_ids]
    print(f"Total excluded records from raw to clean: {len(excluded_rows)}")
    
    # Analyze excluded records
    excluded_summary = []
    for r in excluded_rows:
        excluded_summary.append({
            "run_id": r["run_id"],
            "phase": r.get("phase"),
            "repetition_index": r.get("repetition_index"),
            "variant": r.get("variant"),
            "task_id": r.get("task_id"),
            "success": r.get("success"),
            "partial_score": r.get("partial_score"),
            "total_steps": r.get("total_steps"),
            "total_time_seconds": r.get("total_time_seconds"),
            "timestamp_end": r.get("timestamp_end")
        })
        
    # Success rates
    raw_success = sum(1 for r in raw_rows if r.get("success") in (True, "True", "1", 1))
    clean_success = sum(1 for r in clean_rows if r.get("success") in (True, "True", "1", 1))
    
    pilot_analysis = {
        "raw_count": len(raw_rows),
        "clean_count": len(clean_rows),
        "excluded_count": len(excluded_rows),
        "raw_success_count": raw_success,
        "raw_success_rate": raw_success / len(raw_rows),
        "clean_success_count": clean_success,
        "clean_success_rate": clean_success / len(clean_rows),
        "excluded_failures": sum(1 for r in excluded_rows if r.get("success") in (False, "False", "0", 0)),
        "excluded_successes": sum(1 for r in excluded_rows if r.get("success") in (True, "True", "1", 1)),
        "excluded_records": excluded_summary
    }
    
    out_file = OUT_DIR / "pilot_261_vs_250_reconciliation.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(pilot_analysis, f, indent=2)
    print(f"Exported pilot reconciliation to {out_file}")
    return pilot_analysis

def analyze_main_experiment():
    print("\n=== 2. ANALYZING MAIN EXPERIMENT (147 Entries) ===")
    main_path = ROOT / "results/main_experiment/full-summary.csv"
    backup_main_path = ROOT / "results/main_experiment_backup_20261011/full-summary.csv"
    
    with open(main_path, "r", encoding="utf-8", errors="ignore") as f:
        main_rows = list(csv.DictReader(f))
    with open(backup_main_path, "r", encoding="utf-8", errors="ignore") as f:
        backup_rows = list(csv.DictReader(f))
        
    print(f"main full-summary.csv: {len(main_rows)} rows | SHA-256: {sha256_file(main_path)}")
    print(f"backup full-summary.csv: {len(backup_rows)} rows | SHA-256: {sha256_file(backup_main_path)}")
    
    status_counts = Counter(r.get("status", "UNSPECIFIED") for r in main_rows)
    success_counts = Counter(r.get("success", "UNSPECIFIED") for r in main_rows)
    variant_counts = Counter(r.get("variant", "UNSPECIFIED") for r in main_rows)
    task_counts = Counter(r.get("task_id", "UNSPECIFIED") for r in main_rows)
    error_counts = Counter(r.get("error_message", "NONE") for r in main_rows if r.get("error_message"))
    
    # Check completed vs aborted
    completed_rows = [r for r in main_rows if r.get("status") == "completed"]
    aborted_rows = [r for r in main_rows if r.get("status") in ("aborted", "infrastructure_aborted", "failed")]
    
    print(f"Statuses in 147 rows: {dict(status_counts)}")
    print(f"Success values: {dict(success_counts)}")
    print(f"Completed rows: {len(completed_rows)}")
    print(f"Aborted / Failed rows: {len(aborted_rows)}")
    print(f"Variants distribution: {dict(variant_counts)}")
    print(f"Tasks distribution: {dict(task_counts)}")
    
    # Group by variant x task for completed
    grid = defaultdict(lambda: defaultdict(lambda: {"total": 0, "success": 0, "aborted": 0}))
    for r in main_rows:
        v = r.get("variant", "unknown")
        t = r.get("task_id", "unknown")
        s = r.get("status")
        succ = r.get("success") in (True, "True", "1", 1)
        grid[v][t]["total"] += 1
        if s == "completed":
            if succ:
                grid[v][t]["success"] += 1
        else:
            grid[v][t]["aborted"] += 1
            
    main_analysis = {
        "total_records": len(main_rows),
        "status_breakdown": dict(status_counts),
        "success_breakdown": dict(success_counts),
        "variant_breakdown": dict(variant_counts),
        "task_breakdown": dict(task_counts),
        "frequent_errors": error_counts.most_common(10),
        "completed_count": len(completed_rows),
        "aborted_count": len(aborted_rows),
        "cell_breakdown": {v: dict(tasks) for v, tasks in grid.items()}
    }
    
    out_file = OUT_DIR / "main_experiment_147_reconciliation.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(main_analysis, f, indent=2)
    print(f"Exported main experiment reconciliation to {out_file}")
    return main_analysis

def analyze_v3_cloud_pilot():
    print("\n=== 3. ANALYZING V3 CLOUD PILOT (41 Completed + Retries) ===")
    v3_summary = EXEC_DIR / "results/v3_3arm_summary.csv"
    v3_raw = EXEC_DIR / "results/v3_3arm_summary_raw.csv"
    
    with open(v3_summary, "r", encoding="utf-8", errors="ignore") as f:
        summary_rows = list(csv.DictReader(f))
    with open(v3_raw, "r", encoding="utf-8", errors="ignore") as f:
        raw_rows = list(csv.DictReader(f))
        
    print(f"v3_3arm_summary.csv: {len(summary_rows)} rows | SHA-256: {sha256_file(v3_summary)}")
    print(f"v3_3arm_summary_raw.csv: {len(raw_rows)} rows | SHA-256: {sha256_file(v3_raw)}")
    
    status_summary = Counter(r.get("status") for r in summary_rows)
    print(f"Summary rows status: {dict(status_summary)}")
    
    completed = [r for r in summary_rows if r.get("status") == "completed"]
    aborted = [r for r in summary_rows if r.get("status") != "completed"]
    
    print(f"Completed runs: {len(completed)}")
    print(f"Aborted runs: {len(aborted)}")
    
    # Arm distribution for completed
    arm_counts = Counter(r.get("arm") for r in completed)
    task_counts = Counter(r.get("task_id") for r in completed)
    print(f"Completed arm distribution: {dict(arm_counts)}")
    print(f"Completed task distribution: {dict(task_counts)}")
    
    # Check retries/aborts
    aborted_details = []
    for r in aborted:
        aborted_details.append({
            "run_index": r.get("run_index"),
            "arm": r.get("arm"),
            "task_id": r.get("task_id"),
            "status": r.get("status"),
            "error_message": r.get("error_message"),
            "timestamp": r.get("timestamp")
        })
        print(f"  Aborted: Run {r.get('run_index')} | Arm: {r.get('arm')} | Task: {r.get('task_id')} | Error: {r.get('error_message')}")
        
    v3_analysis = {
        "summary_rows_count": len(summary_rows),
        "raw_rows_count": len(raw_rows),
        "completed_count": len(completed),
        "aborted_count": len(aborted),
        "arm_distribution": dict(arm_counts),
        "task_distribution": dict(task_counts),
        "aborted_details": aborted_details
    }
    
    out_file = OUT_DIR / "v3_cloud_pilot_reconciliation.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(v3_analysis, f, indent=2)
    print(f"Exported v3 cloud pilot reconciliation to {out_file}")
    return v3_analysis

def analyze_synthetic_datasets():
    print("\n=== 4. ANALYZING SYNTHETIC DATASETS (96-run schedules & test data) ===")
    synth_dir = EXEC_DIR / "test_scratch_synthetic_data"
    sched_path = EXEC_DIR / "proposed_randomized_schedule.csv"
    sched_3arm_path = EXEC_DIR / "proposed_3arm_schedule.csv"
    
    synth_files = list(synth_dir.glob("*.csv")) if synth_dir.exists() else []
    print(f"Found {len(synth_files)} synthetic CSV test files in {synth_dir}")
    
    synth_inventory = {}
    for p in sorted(synth_files):
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            rows = list(csv.DictReader(f))
        synth_inventory[p.name] = {
            "rows": len(rows),
            "size_bytes": p.stat().st_size,
            "sha256": sha256_file(p),
            "columns": list(rows[0].keys()) if rows else []
        }
        print(f"  {p.name}: {len(rows)} rows ({p.stat().st_size:,} bytes)")
        
    if sched_path.exists():
        with open(sched_path, "r", encoding="utf-8", errors="ignore") as f:
            s_rows = list(csv.DictReader(f))
        print(f"proposed_randomized_schedule.csv: {len(s_rows)} rows ({sched_path.stat().st_size:,} bytes)")
        synth_inventory["proposed_randomized_schedule.csv"] = {
            "rows": len(s_rows),
            "size_bytes": sched_path.stat().st_size,
            "sha256": sha256_file(sched_path)
        }
        
    if sched_3arm_path.exists():
        with open(sched_3arm_path, "r", encoding="utf-8", errors="ignore") as f:
            s3_rows = list(csv.DictReader(f))
        print(f"proposed_3arm_schedule.csv: {len(s3_rows)} rows ({sched_3arm_path.stat().st_size:,} bytes)")
        synth_inventory["proposed_3arm_schedule.csv"] = {
            "rows": len(s3_rows),
            "size_bytes": sched_3arm_path.stat().st_size,
            "sha256": sha256_file(sched_3arm_path)
        }
        
    out_file = OUT_DIR / "synthetic_datasets_inventory.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(synth_inventory, f, indent=2)
    print(f"Exported synthetic datasets inventory to {out_file}")
    return synth_inventory

def analyze_local_qwen():
    print("\n=== 5. ANALYZING LOCAL QWEN DATASET (5 Runs) ===")
    llama_path = EXEC_DIR / "results/local_llama_summary.csv"
    with open(llama_path, "r", encoding="utf-8", errors="ignore") as f:
        rows = list(csv.DictReader(f))
        
    print(f"local_llama_summary.csv: {len(rows)} rows | SHA-256: {sha256_file(llama_path)}")
    records = []
    durations = []
    for r in rows:
        dur = float(r.get("duration_seconds", 0.0))
        durations.append(dur)
        records.append({
            "run_index": r.get("run_index"),
            "model": r.get("model"),
            "arm": r.get("arm"),
            "task_id": r.get("task_id"),
            "status": r.get("status"),
            "duration_seconds": dur,
            "total_steps": r.get("total_steps"),
            "error_message": r.get("error_message")
        })
        print(f"  Run {r.get('run_index')}: {r.get('model')} | Task: {r.get('task_id')} | Duration: {dur:.2f}s | Status: {r.get('status')}")
        
    steady_state_durs = durations[2:] if len(durations) >= 3 else durations
    avg_steady_state = sum(steady_state_durs) / len(steady_state_durs) if steady_state_durs else 0.0
    
    qwen_analysis = {
        "total_runs": len(rows),
        "model": rows[0].get("model") if rows else "unknown",
        "durations_seconds": durations,
        "cold_start_duration_s": durations[1] if len(durations) > 1 else 0.0,
        "mean_steady_state_duration_s": avg_steady_state,
        "records": records
    }
    
    out_file = OUT_DIR / "local_qwen_reconciliation.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(qwen_analysis, f, indent=2)
    print(f"Exported local Qwen reconciliation to {out_file}")
    return qwen_analysis

def generate_master_dataset_inventory():
    print("\n=== 6. GENERATING MASTER HISTORICAL DATASET INVENTORY ===")
    datasets = [
        {
            "id": "DS-01",
            "name": "Historical Pilot Raw (Rep 1-10)",
            "path": "results/pilot-summary.csv",
            "full_path": str(ROOT / "results/pilot-summary.csv"),
            "category": "Historical Exploratory Pilot",
            "total_rows": 261,
            "completed": 261,
            "aborted_or_retried": 11,
            "success_rate": "251/261 (96.17%)",
            "notes": "Includes 9 failed attempts from Repetition 9 and 2 extra Rep 1 runs. Not confirmatory."
        },
        {
            "id": "DS-02",
            "name": "Historical Pilot Clean (Balanced 10x5x5)",
            "path": "results/pilot-summary-clean.csv",
            "full_path": str(ROOT / "results/pilot-summary-clean.csv"),
            "category": "Historical Exploratory Pilot (Cleaned)",
            "total_rows": 250,
            "completed": 250,
            "aborted_or_retried": 0,
            "success_rate": "249/250 (99.60%)",
            "notes": "Artificially filtered: discarded 9 failures from Repetition 9. Ceiled."
        },
        {
            "id": "DS-03",
            "name": "Historical Main Experiment Full Summary",
            "path": "results/main_experiment/full-summary.csv",
            "full_path": str(ROOT / "results/main_experiment/full-summary.csv"),
            "category": "Historical Behavioral Experiment",
            "total_rows": 147,
            "completed": 105,
            "aborted_or_retried": 42,
            "success_rate": "105/105 completed succeeded (100% conditional on completion)",
            "notes": "42 aborted runs due to timeout/DOM disconnect. Shows benchmark ceiling."
        },
        {
            "id": "DS-04",
            "name": "Protocol v3 Cloud Pilot (Gemini 3.1 Flash-Lite)",
            "path": "research_execution_20261018/results/v3_3arm_summary.csv",
            "full_path": str(EXEC_DIR / "results/v3_3arm_summary.csv"),
            "category": "Active Exploratory Cloud Pilot",
            "total_rows": 44,
            "completed": 41,
            "aborted_or_retried": 3,
            "success_rate": "41/41 (100.0%)",
            "notes": "41 completed across ABS (13), ARIA (13), DATA-CFG (15). 3 retries on Run 26 (HTTP 503). Halted at quota ceiling."
        },
        {
            "id": "DS-05",
            "name": "Protocol v3 Raw Summary Ledger",
            "path": "research_execution_20261018/results/v3_3arm_summary_raw.csv",
            "full_path": str(EXEC_DIR / "results/v3_3arm_summary_raw.csv"),
            "category": "Active Exploratory Raw Ledger",
            "total_rows": 46,
            "completed": 41,
            "aborted_or_retried": 5,
            "success_rate": "41/41 completed",
            "notes": "Unfiltered raw execution trace ledger."
        },
        {
            "id": "DS-06",
            "name": "Local Qwen Exploratory Latency Pilot",
            "path": "research_execution_20261018/results/local_llama_summary.csv",
            "full_path": str(EXEC_DIR / "results/local_llama_summary.csv"),
            "category": "Local SLM Exploratory Measurement",
            "total_rows": 5,
            "completed": 5,
            "aborted_or_retried": 0,
            "success_rate": "5/5 completed (high latency ~221s)",
            "notes": "Model qwen3:4b via Ollama. Exploratory latency characterization only."
        },
        {
            "id": "DS-07",
            "name": "Synthetic RCBD Benchmark Dataset (Complete)",
            "path": "research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv",
            "full_path": str(EXEC_DIR / "test_scratch_synthetic_data/dataset_1_valid_complete.csv"),
            "category": "Synthetic Protocol Verification",
            "total_rows": 96,
            "completed": 96,
            "aborted_or_retried": 0,
            "success_rate": "Synthetic (for analysis pipeline testing only)",
            "notes": "Purely synthetic test fixture. Never pooled with empirical data."
        },
        {
            "id": "DS-08",
            "name": "Proposed Confirmatory Randomized Schedule (RCBD)",
            "path": "research_execution_20261018/proposed_randomized_schedule.csv",
            "full_path": str(EXEC_DIR / "proposed_randomized_schedule.csv"),
            "category": "Pre-Registered Confirmatory Protocol Schedule",
            "total_rows": 96,
            "completed": 0,
            "aborted_or_retried": 0,
            "success_rate": "Unexecuted (Ready for execution if authorized)",
            "notes": "4 arms x 6 tasks x 4 reps. Strict seed 42 blocking."
        }
    ]
    
    # Add SHA256 and byte sizes
    for ds in datasets:
        p = Path(ds["full_path"])
        if p.exists():
            ds["size_bytes"] = p.stat().st_size
            ds["sha256"] = sha256_file(p)
        else:
            ds["size_bytes"] = None
            ds["sha256"] = None
            
    out_json = OUT_DIR / "master_dataset_inventory.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(datasets, f, indent=2)
        
    out_csv = OUT_DIR / "master_dataset_inventory.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "name", "path", "category", "total_rows", "completed", "aborted_or_retried", 
            "success_rate", "size_bytes", "sha256", "notes"
        ])
        writer.writeheader()
        for ds in datasets:
            row = dict(ds)
            del row["full_path"]
            writer.writerow(row)
            
    print(f"Exported master dataset inventory to {out_json} and {out_csv}")
    return datasets

if __name__ == "__main__":
    p_res = analyze_pilot_datasets()
    m_res = analyze_main_experiment()
    v3_res = analyze_v3_cloud_pilot()
    s_res = analyze_synthetic_datasets()
    q_res = analyze_local_qwen()
    master = generate_master_dataset_inventory()
    print("\n[SUCCESS] Comprehensive Data Recovery and Forensic Reconciliation complete.")

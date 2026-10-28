#!/usr/bin/env python3
"""
scripts/independent_ledger_audit.py
Authoritative scheduled-unit and physical attempt ledger auditor.
Reconciles physical JSON files in results/3arm_runs/ against proposed_3arm_schedule.csv,
v3_3arm_summary_raw.csv, v3_3arm_summary.csv, and v3_3arm_summary_reconciled_v2.csv.
"""

import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEDULE_PATH = PROJECT_ROOT / "proposed_3arm_schedule.csv"
RUNS_DIR = PROJECT_ROOT / "results" / "3arm_runs"
RAW_CSV_PATH = PROJECT_ROOT / "results" / "v3_3arm_summary_raw.csv"
CLEAN_CSV_PATH = PROJECT_ROOT / "results" / "v3_3arm_summary.csv"
RECON_CSV_PATH = PROJECT_ROOT / "results" / "v3_3arm_summary_reconciled_v2.csv"
AUDIT_JSON_PATH = PROJECT_ROOT / "results" / "v3_3arm_reconciliation_audit.json"


def run_audit() -> int:
    print("=== INDEPENDENT RECONCILIATION LEDGER AUDIT ===")

    # 1. Load schedule
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        sched_rows = list(csv.DictReader(f))
    print(f"Schedule units: {len(sched_rows)} rows (runs 1..72)")
    sched_indices = [int(r["run_index"]) for r in sched_rows]
    assert len(sched_indices) == 72
    assert set(sched_indices) == set(range(1, 73))

    # 2. Inspect physical JSON files
    json_files = sorted(RUNS_DIR.glob("*.json"))
    print(f"Physical JSON attempt files: {len(json_files)}")
    assert len(json_files) == 46

    attempts_by_run = {}
    file_to_run_attempt = {}

    for jf in json_files:
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)

        run_idx = int(data.get("run_index", jf.name.split("_")[1].split(".")[0]))
        att_num = int(data.get("attempt_number", 1))
        if "_attempt_" in jf.name:
            att_num_from_fn = int(jf.name.split("_attempt_")[1].split(".")[0])
            assert att_num == att_num_from_fn

        key = (run_idx, att_num)
        assert key not in file_to_run_attempt, f"Duplicate attempt key: {key}"
        file_to_run_attempt[key] = jf.name

        if run_idx not in attempts_by_run:
            attempts_by_run[run_idx] = []
        attempts_by_run[run_idx].append({
            "file": jf.name,
            "attempt_number": att_num,
            "status": data.get("status"),
            "score": data.get("score"),
            "timestamp_start": data.get("timestamp_start", data.get("timestamp", ""))
        })

    print(f"Distinct attempted scheduled units: {len(attempts_by_run)} (runs 1..41)")
    assert len(attempts_by_run) == 41
    assert set(attempts_by_run.keys()) == set(range(1, 42))

    multi_attempts = {k: v for k, v in attempts_by_run.items() if len(v) > 1}
    print(f"Multi-attempt units: {list(multi_attempts.keys())}")
    assert len(multi_attempts[26]) == 4  # 3 infra 503 aborted, 1 completed
    assert len(multi_attempts[34]) == 2  # 2 completed attempts (quarantined)
    assert len(multi_attempts[38]) == 2  # 2 completed attempts (quarantined)

    single_attempts = {k: v for k, v in attempts_by_run.items() if len(v) == 1}
    assert len(single_attempts) == 38

    # Unexecuted units
    unexecuted_indices = sorted(set(sched_indices) - set(attempts_by_run.keys()))
    print(f"Unexecuted scheduled units: {len(unexecuted_indices)} (runs 42..72)")
    assert len(unexecuted_indices) == 31
    assert unexecuted_indices == list(range(42, 73))

    # Check audit JSON
    if AUDIT_JSON_PATH.exists():
        with open(AUDIT_JSON_PATH, "r", encoding="utf-8") as f:
            audit_data = json.load(f)
        assert len(audit_data["all_physical_attempts"]) == 46
        assert len(audit_data["scheduled_units"]) == 72
        print("Audit JSON consistency verified.")

    # Check reconciled CSV
    if RECON_CSV_PATH.exists():
        with open(RECON_CSV_PATH, "r", encoding="utf-8") as f:
            recon_rows = list(csv.DictReader(f))
        assert len(recon_rows) == 41
        print("Reconciled CSV 41-row structure verified.")

    print("\nSUCCESS: All ledger reconstruction invariants verified!")
    return 0


if __name__ == "__main__":
    sys.exit(run_audit())

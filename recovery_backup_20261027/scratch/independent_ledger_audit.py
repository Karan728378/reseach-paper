import csv
import json
import glob
from pathlib import Path

WORKSPACE = Path("C:/testing/research_execution_20261018")
SCHEDULE_PATH = WORKSPACE / "proposed_3arm_schedule.csv"
RUNS_DIR = WORKSPACE / "results" / "3arm_runs"
RAW_CSV_PATH = WORKSPACE / "results" / "v3_3arm_summary_raw.csv"
CLEAN_CSV_PATH = WORKSPACE / "results" / "v3_3arm_summary.csv"
RECON_CSV_PATH = WORKSPACE / "results" / "v3_3arm_summary_reconciled_v2.csv"
AUDIT_JSON_PATH = WORKSPACE / "results" / "v3_3arm_reconciliation_audit.json"

# 1. Load schedule
with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
    sched_rows = list(csv.DictReader(f))

print(f"Total rows in schedule: {len(sched_rows)}")
sched_indices = [int(r["run_index"]) for r in sched_rows]
assert len(sched_indices) == 72
assert set(sched_indices) == set(range(1, 73))

# 2. Inspect physical JSON files
json_files = sorted(RUNS_DIR.glob("*.json"))
print(f"Total physical JSON files in 3arm_runs: {len(json_files)}")
assert len(json_files) == 46

attempts_by_run = {}
file_to_run_attempt = {}

for jf in json_files:
    with open(jf, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    run_idx = int(data.get("run_index", jf.name.split("_")[1].split(".")[0]))
    att_num = int(data.get("attempt_number", 1))
    # Check filename convention if attempt_number is not in body
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

print(f"Total distinct attempted run_indices: {len(attempts_by_run)}")
assert len(attempts_by_run) == 41
assert set(attempts_by_run.keys()) == set(range(1, 42))

# Multi-attempt breakdown
multi_attempts = {k: v for k, v in attempts_by_run.items() if len(v) > 1}
print(f"Runs with multiple attempts: {list(multi_attempts.keys())}")
for r_idx, atts in multi_attempts.items():
    print(f"  Run {r_idx}: {len(atts)} attempts -> {[a['file'] for a in atts]}")

assert len(multi_attempts[26]) == 4
assert len(multi_attempts[34]) == 2
assert len(multi_attempts[38]) == 2

single_attempts = {k: v for k, v in attempts_by_run.items() if len(v) == 1}
assert len(single_attempts) == 38

# Check unexecuted units
unexecuted_indices = sorted(set(sched_indices) - set(attempts_by_run.keys()))
print(f"Unexecuted scheduled run indices ({len(unexecuted_indices)}): {unexecuted_indices[0]} to {unexecuted_indices[-1]}")
assert len(unexecuted_indices) == 31
assert unexecuted_indices == list(range(42, 73))

# Check audit JSON
with open(AUDIT_JSON_PATH, "r", encoding="utf-8") as f:
    audit_data = json.load(f)

print(f"Audit JSON total physical attempts: {len(audit_data['all_physical_attempts'])}")
assert len(audit_data['all_physical_attempts']) == 46
print(f"Audit JSON total scheduled units: {len(audit_data['scheduled_units'])}")
assert len(audit_data['scheduled_units']) == 72

# Check reconciled CSV
with open(RECON_CSV_PATH, "r", encoding="utf-8") as f:
    recon_rows = list(csv.DictReader(f))
print(f"Reconciled CSV rows: {len(recon_rows)}")
assert len(recon_rows) == 41

print("\nALL RECONSTRUCTION INVARIANTS INDEPENDENTLY CONFIRMED!")

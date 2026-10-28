import csv
import json
from pathlib import Path
from collections import defaultdict

schedule_path = Path("proposed_3arm_schedule.csv")
summary_path = Path("results/v3_3arm_summary.csv")
raw_summary_path = Path("results/v3_3arm_summary_raw.csv")
runs_dir = Path("results/3arm_runs")

# 1. Load schedule 1..41
with open(schedule_path, "r", encoding="utf-8") as f:
    sched_rows = {int(r["run_index"]): r for r in csv.DictReader(f) if int(r["run_index"]) <= 41}

print(f"Schedule rows loaded (1..41): {len(sched_rows)}")

# 2. Load summary and raw summary
with open(summary_path, "r", encoding="utf-8") as f:
    summary_rows = list(csv.DictReader(f))

with open(raw_summary_path, "r", encoding="utf-8") as f:
    raw_summary_rows = list(csv.DictReader(f))

print(f"Summary total rows: {len(summary_rows)}")
print(f"Raw summary total rows: {len(raw_summary_rows)}")

raw_by_idx = defaultdict(list)
for r in raw_summary_rows:
    raw_by_idx[int(r["run_index"])].append(r)

clean_by_idx = defaultdict(list)
for r in summary_rows:
    clean_by_idx[int(r["run_index"])].append(r)

# Check all json files in runs_dir
json_files = list(runs_dir.glob("run_*.json"))
print(f"Total JSON files in {runs_dir}: {len(json_files)}")

# Audit each index 1..41
discrepancies = []
audit_records = []

for idx in range(1, 42):
    sched = sched_rows.get(idx)
    raw_entries = raw_by_idx.get(idx, [])
    clean_entries = clean_by_idx.get(idx, [])
    
    # Check JSON files
    primary_json = runs_dir / f"run_{idx:03d}.json"
    matching_jsons = list(runs_dir.glob(f"run_{idx:03d}*.json"))
    
    json_data = None
    if primary_json.exists():
        try:
            with open(primary_json, "r", encoding="utf-8") as jf:
                json_data = json.load(jf)
        except Exception as e:
            discrepancies.append(f"Run {idx}: Corrupted JSON {primary_json}: {e}")
    else:
        discrepancies.append(f"Run {idx}: Missing primary JSON {primary_json}")

    # Check clean summary
    if len(clean_entries) == 0:
        discrepancies.append(f"Run {idx}: Missing from clean summary")
    elif len(clean_entries) > 1:
        # Check if infrastructure error
        infra_clean = [e for e in clean_entries if "infra" in e["status"] or "503" in e["error_message"]]
        completed_clean = [e for e in clean_entries if e["status"] == "completed"]
        if len(completed_clean) > 1:
            discrepancies.append(f"Run {idx}: Multiple completed entries in clean summary ({len(completed_clean)})")
    
    # Verify alignment between schedule, summary, and json
    if clean_entries and json_data:
        comp_clean = [e for e in clean_entries if e["status"] == "completed"]
        if comp_clean:
            c = comp_clean[0]
            # Verify arm
            if c["arm"] != sched["arm"]:
                discrepancies.append(f"Run {idx}: Arm mismatch (sched={sched['arm']}, summary={c['arm']})")
            if json_data.get("arm") != sched["arm"]:
                discrepancies.append(f"Run {idx}: Arm mismatch in JSON (sched={sched['arm']}, json={json_data.get('arm')})")
            # Verify task_id
            if c["task_id"] != sched["task_id"]:
                discrepancies.append(f"Run {idx}: Task mismatch (sched={sched['task_id']}, summary={c['task_id']})")
            if json_data.get("task_id") != sched["task_id"]:
                discrepancies.append(f"Run {idx}: Task mismatch in JSON (sched={sched['task_id']}, json={json_data.get('task_id')})")
            # Verify variant
            if c["variant_mapping"] != sched["variant_mapping"]:
                discrepancies.append(f"Run {idx}: Variant mismatch (sched={sched['variant_mapping']}, summary={c['variant_mapping']})")
            # Verify score & success
            v_res = json_data.get("verifier_result", {})
            v_succ = str(v_res.get("success", "")).lower() == "true"
            c_succ = str(c.get("success", "")).lower() == "true"
            if v_succ != c_succ:
                discrepancies.append(f"Run {idx}: Success mismatch between JSON ({v_succ}) and summary ({c_succ})")
            if float(c.get("score", 0.0)) != float(v_res.get("score", 0.0)):
                discrepancies.append(f"Run {idx}: Score mismatch between JSON ({v_res.get('score')}) and summary ({c.get('score')})")

    audit_records.append({
        "idx": idx,
        "arm": sched["arm"] if sched else None,
        "task_id": sched["task_id"] if sched else None,
        "raw_count": len(raw_entries),
        "clean_count": len(clean_entries),
        "matching_jsons": [p.name for p in matching_jsons],
        "clean_statuses": [e["status"] for e in clean_entries],
        "clean_scores": [e["score"] for e in clean_entries]
    })

print("\n--- AUDIT SUMMARY ---")
print(f"Total discrepancies found: {len(discrepancies)}")
for d in discrepancies:
    print("  *", d)

# Print detail on runs with multiple raw entries
multi_raw = [r for r in audit_records if r["raw_count"] > 1]
print(f"\nRuns with multiple raw entries ({len(multi_raw)}):")
for r in multi_raw:
    print(f"  Run {r['idx']:02d} ({r['arm']}/{r['task_id']}): raw_count={r['raw_count']}, clean_count={r['clean_count']}, jsons={r['matching_jsons']}, statuses={r['clean_statuses']}")

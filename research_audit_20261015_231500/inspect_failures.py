import os
import csv
import json
from collections import Counter

summary_path = r"C:\testing\results\main_experiment\full-summary.csv"
raw_dir = r"C:\testing\results\main_experiment\raw"
history_dir = r"C:\testing\results\main_experiment\agent-history"
audit_log_dir = r"C:\testing\results\main_experiment\audit-logs"

with open(summary_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

raw_files = set(f.replace('.jsonl', '') for f in os.listdir(raw_dir) if f.endswith('.jsonl'))
summary_ids = set(r['run_id'] for r in rows)

extra_raw = raw_files - summary_ids
print(f"Extra raw files not in summary ({len(extra_raw)}): {extra_raw}")
for er in extra_raw:
    p = os.path.join(raw_dir, er + ".jsonl")
    print(f"\n--- Content of extra raw file {er}.jsonl ({os.path.getsize(p)} bytes) ---")
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            print(line.strip()[:300])

print("\n--- Inspecting the 42 'False' runs from raw jsonl ---")
fail_rows = [r for r in rows if r['success'] == 'False']
fail_reasons = []

for r in fail_rows:
    rid = r['run_id']
    raw_p = os.path.join(raw_dir, rid + ".jsonl")
    if not os.path.exists(raw_p):
        print(f"Missing raw file for {rid}")
        continue
    records = []
    with open(raw_p, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    records.append(json.loads(line.strip()))
                except Exception as e:
                    records.append({"parse_error": str(e), "line": line.strip()})
    
    # summarize record types
    rec_types = [rec.get('type') or rec.get('event') or list(rec.keys())[0] for rec in records]
    last_rec = records[-1] if records else {}
    fail_reasons.append({
        "run_id": rid,
        "variant": r['variant'],
        "task_id": r['task_id'],
        "scheduled_index": r['scheduled_run_index'],
        "total_steps": r['total_steps'],
        "total_time": r['total_time_seconds'],
        "partial_score": r['partial_score'],
        "num_records": len(records),
        "rec_types": rec_types[:5],
        "last_rec_keys": list(last_rec.keys()),
        "last_rec_summary": {k: last_rec[k] for k in ['success', 'error', 'error_message', 'partial_score', 'total_steps'] if k in last_rec}
    })

print(f"Total fail rows examined: {len(fail_reasons)}")
# Show first 5 fail reasons
for fr in fail_reasons[:10]:
    print(fr)

# Check distribution of partial_score and total_steps among failures
print("\nPartial score among failures:")
print(Counter(fr['partial_score'] for fr in fail_reasons))
print("\nTotal steps among failures:")
print(Counter(fr['total_steps'] for fr in fail_reasons))
print("\nNumber of records in raw jsonl among failures:")
print(Counter(fr['num_records'] for fr in fail_reasons))

# Check history dir
hist_files = os.listdir(history_dir) if os.path.exists(history_dir) else []
print(f"\nHistory dir files: {len(hist_files)}")

# Check audit-logs dir
audit_files = os.listdir(audit_log_dir) if os.path.exists(audit_log_dir) else []
print(f"Audit logs dir files: {len(audit_files)}")
if audit_files:
    print(f"First 5 audit files: {audit_files[:5]}")
    # Inspect one audit log
    p_audit = os.path.join(audit_log_dir, audit_files[0])
    with open(p_audit, "r", encoding="utf-8") as f:
        print(f"Sample audit log content ({audit_files[0]}):")
        for _ in range(10):
            line = f.readline()
            if not line: break
            print(line.strip()[:200])

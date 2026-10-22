import os
import csv
import json

summary_path = r"C:\testing\results\main_experiment\full-summary.csv"
history_dir = r"C:\testing\results\main_experiment\agent-history"
audit_log_dir = r"C:\testing\results\main_experiment\audit-logs"

with open(summary_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

rows.sort(key=lambda r: int(r['scheduled_run_index']))

print(f"Total runs: {len(rows)}")

# Check what happened around where failures start
# Let's see consecutive success / fail blocks
blocks = []
current_status = None
current_start = None
count = 0

for r in rows:
    status = (r['success'] == 'True')
    idx = int(r['scheduled_run_index'])
    if status != current_status:
        if current_status is not None:
            blocks.append((current_status, current_start, idx - 1, count))
        current_status = status
        current_start = idx
        count = 1
    else:
        count += 1
blocks.append((current_status, current_start, int(rows[-1]['scheduled_run_index']), count))

print("\nSuccess/Failure blocks:")
for status, start_idx, end_idx, cnt in blocks:
    t_start = [r['timestamp_end'] for r in rows if r['scheduled_run_index'] == str(start_idx)][0]
    t_end = [r['timestamp_end'] for r in rows if r['scheduled_run_index'] == str(end_idx)][0]
    print(f"  Status={'SUCCESS' if status else 'FAIL   '}: runs {start_idx:3d} to {end_idx:3d} (count={cnt:3d}) | {t_start} -> {t_end}")

# Inspect the agent history files for failures to see the exact error / exception
print("\n--- Inspecting agent-history for failures ---")
sample_fails = [r for r in rows if r['success'] == 'False']
errors_seen = set()
for r in sample_fails:
    rid = r['run_id']
    hp = os.path.join(history_dir, f"{rid}.json")
    if os.path.exists(hp):
        try:
            with open(hp, "r", encoding="utf-8") as f:
                data = json.load(f)
            # data could be list or dict
            # check errors in history
            hist_str = json.dumps(data)
            # look for 429, ResourceExhausted, Quota, etc.
            found_errs = []
            if "429" in hist_str: found_errs.append("429")
            if "RESOURCE_EXHAUSTED" in hist_str: found_errs.append("RESOURCE_EXHAUSTED")
            if "RateLimit" in hist_str or "rate_limit" in hist_str.lower(): found_errs.append("RateLimit")
            if "Quota" in hist_str or "quota" in hist_str.lower(): found_errs.append("Quota")
            errors_seen.add(tuple(found_errs))
            if r == sample_fails[0]:
                print(f"First failure {rid} (scheduled {r['scheduled_run_index']}):")
                print(f"  History type: {type(data)}, len: {len(data) if isinstance(data, list) else list(data.keys())}")
                if isinstance(data, list) and len(data) > 0:
                    last_item = data[-1]
                    print(f"  Last item keys: {list(last_item.keys()) if isinstance(last_item, dict) else type(last_item)}")
                    if isinstance(last_item, dict):
                        for k, v in last_item.items():
                            val_str = str(v)
                            if len(val_str) > 200: val_str = val_str[:200] + "..."
                            print(f"    {k}: {val_str}")
        except Exception as e:
            print(f"Error reading history for {rid}: {e}")

print(f"\nUnique error keywords seen across all 42 failures: {errors_seen}")

# Also check the extra raw file
extra_raw_file = r"C:\testing\results\main_experiment\raw\ec33d1c9-6a3f-42a9-bb20-1e5f86641e78.jsonl"
if os.path.exists(extra_raw_file):
    print(f"\nExtra raw file exists. Content:")
    with open(extra_raw_file, "r", encoding="utf-8") as f:
        print(f.read())

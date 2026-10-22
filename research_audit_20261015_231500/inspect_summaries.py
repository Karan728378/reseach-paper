import os
import glob
import json
import csv
from collections import Counter, defaultdict

audit_dir = r"C:\testing\research_audit_20261015_231500"
results_dir = r"C:\testing\results"

print("--- RESULTS SUBDIRECTORIES AND CSVS ---")
for f in os.listdir(results_dir):
    p = os.path.join(results_dir, f)
    if os.path.isfile(p):
        print(f"File: {f} ({os.path.getsize(p)} bytes)")
    else:
        num_items = len(os.listdir(p))
        print(f"Dir:  {f} ({num_items} items)")

def inspect_summary_csv(csv_path):
    print(f"\n==========================================")
    print(f"Inspecting CSV: {csv_path}")
    print(f"==========================================")
    if not os.path.exists(csv_path):
        print("Does not exist!")
        return
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns ({len(fieldnames)}): {fieldnames}")
    if rows:
        print("First row:", rows[0])
    
    # Analyze common columns
    for col in ['variant', 'task', 'task_id', 'success', 'status', 'error', 'error_type', 'run_id']:
        if col in (fieldnames or []):
            counts = Counter(r.get(col, '') for r in rows)
            print(f"\nValue counts for '{col}':")
            for k, v in counts.most_common(10):
                print(f"  {repr(k)}: {v}")

for name in [
    r"C:\testing\results\full-summary.csv",
    r"C:\testing\results\main_experiment\full-summary.csv",
    r"C:\testing\results\main_experiment_backup_20261011\full-summary.csv",
    r"C:\testing\results\main_experiment_recovery\full-summary.csv",
    r"C:\testing\results\pilot-summary.csv",
    r"C:\testing\results\pilot-summary-clean.csv",
    r"C:\testing\results\final-statistical-results.csv"
]:
    inspect_summary_csv(name)

import os
import csv
import json
from collections import Counter, defaultdict

summary_path = r"C:\testing\results\main_experiment\full-summary.csv"
raw_dir = r"C:\testing\results\main_experiment\raw"

with open(summary_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in main_experiment/full-summary.csv: {len(rows)}")

# Breakdown of success / failure
success_counts = Counter(r['success'] for r in rows)
print(f"Success counts: {success_counts}")

# Breakdown of error_message for False
fail_errors = Counter(r['error_message'] for r in rows if r['success'] == 'False')
print("\nFailure error messages:")
for k, v in fail_errors.items():
    print(f"  [{repr(k)}]: {v}")

# Variants breakdown
print("\nVariant breakdown (Success vs False):")
var_counts = defaultdict(lambda: Counter())
for r in rows:
    var_counts[r['variant']][r['success']] += 1
for v, c in sorted(var_counts.items()):
    print(f"  {v}: True={c['True']}, False={c['False']}, Total={sum(c.values())}")

# Task breakdown
print("\nTask breakdown (Success vs False):")
task_counts = defaultdict(lambda: Counter())
for r in rows:
    task_counts[r['task_id']][r['success']] += 1
for t, c in sorted(task_counts.items()):
    print(f"  {t}: True={c['True']}, False={c['False']}, Total={sum(c.values())}")

# Cell breakdown (variant x task)
print("\nCell breakdown (variant x task x success):")
cell_counts = defaultdict(lambda: Counter())
for r in rows:
    cell = (r['variant'], r['task_id'])
    cell_counts[cell][r['success']] += 1

print(f"Total cells represented: {len(cell_counts)}")
for cell in sorted(cell_counts.keys()):
    c = cell_counts[cell]
    print(f"  {cell[0]} | {cell[1]}: True={c['True']}, False={c['False']}, Total={sum(c.values())}")

# Check scheduled_run_index range
indices = [int(r['scheduled_run_index']) for r in rows if r['scheduled_run_index']]
print(f"\nScheduled run index min: {min(indices)}, max: {max(indices)}, count: {len(indices)}")
missing_indices = set(range(1, max(indices) + 1)) - set(indices)
print(f"Missing indices between 1 and {max(indices)}: {sorted(missing_indices)}")
print(f"Count of missing indices up to 200: {len(set(range(1, 201)) - set(indices))}")

# Check timestamps
timestamps = [r['timestamp_end'] for r in rows if r['timestamp_end']]
print(f"\nFirst timestamp: {min(timestamps)}, Last timestamp: {max(timestamps)}")

# Check raw files
raw_files = os.listdir(raw_dir)
print(f"\nRaw directory has {len(raw_files)} files.")
raw_run_ids = set()
for rf in raw_files:
    if rf.endswith('.jsonl'):
        raw_run_ids.add(rf.replace('.jsonl', ''))

summary_run_ids = set(r['run_id'] for r in rows)
print(f"Summary run IDs count: {len(summary_run_ids)}")
print(f"In summary but not in raw: {len(summary_run_ids - raw_run_ids)}")
print(f"In raw but not in summary: {len(raw_run_ids - summary_run_ids)}")

import csv, glob, json
from pathlib import Path

with open('results/v3_3arm_summary_raw.csv', 'r', encoding='utf-8') as f:
    raw_rows = list(csv.DictReader(f))
with open('results/v3_3arm_summary.csv', 'r', encoding='utf-8') as f:
    clean_rows = list(csv.DictReader(f))

print("=== RAW ROWS FOR RUN 34 ===")
for i, r in enumerate(raw_rows):
    if r['run_index'] == '34':
        print(f"Raw Row {i}: {r}")

print("\n=== RAW ROWS FOR RUN 38 ===")
for i, r in enumerate(raw_rows):
    if r['run_index'] == '38':
        print(f"Raw Row {i}: {r}")

print("\n=== RAW ROWS FOR RUN 26 ===")
for i, r in enumerate(raw_rows):
    if r['run_index'] == '26':
        print(f"Raw Row {i}: status={r['status']}, err={r['error_message']}, t_start={r['timestamp_start']}")

print("\n=== JSON FILES FOR RUN 34, 38, 26 ===")
for idx in ['026', '034', '038']:
    files = sorted(Path('results/3arm_runs').glob(f"run_{idx}*.json"))
    print(f"Files for {idx}: {[f.name for f in files]}")

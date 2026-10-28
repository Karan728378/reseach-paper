import csv

with open('results/v3_3arm_summary_raw.csv', 'r', encoding='utf-8') as f:
    raw_rows = list(csv.DictReader(f))
with open('results/v3_3arm_summary.csv', 'r', encoding='utf-8') as f:
    clean_rows = list(csv.DictReader(f))

print(f"Raw count: {len(raw_rows)}, Clean count: {len(clean_rows)}")
clean_keys = set((r['run_index'], r['timestamp_start'], r['status']) for r in clean_rows)

missing_from_clean = []
for i, r in enumerate(raw_rows):
    key = (r['run_index'], r['timestamp_start'], r['status'])
    if key not in clean_keys:
        missing_from_clean.append((i, r))

print(f"Rows in raw but NOT in clean: {len(missing_from_clean)}")
for idx, r in missing_from_clean:
    print(f"Row {idx}: run_index={r['run_index']}, arm={r['arm']}, task={r['task_id']}, status={r['status']}, score={r['score']}, t_start={r['timestamp_start']}")

import csv

with open('results/v3_3arm_summary_raw.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"{'Idx':<4} {'Run':<4} {'Arm':<9} {'Task':<5} {'Status':<14} {'Steps':<6} {'Start':<27} {'End':<27}")
print("-" * 105)
for i, r in enumerate(rows[30:], start=31):
    print(f"{i:<4} {r['run_index']:<4} {r['arm']:<9} {r['task_id']:<5} {r['status']:<14} {r['total_steps']:<6} {r['timestamp_start']:<27} {r['timestamp_end']:<27}")

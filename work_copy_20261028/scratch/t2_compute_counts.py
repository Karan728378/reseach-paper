import csv
from collections import defaultdict

csv_path = 'C:/testing/work_copy_20261028/test_scratch_synthetic_data/dataset_1_valid_complete.csv'

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    t1_t5_counts = defaultdict(lambda: {'success': 0, 'total': 0})
    all_counts = defaultdict(lambda: {'success': 0, 'total': 0})
    for row in reader:
        arm = row['arm']
        task = row['task_id']
        success = 1 if row['success'].strip().lower() in ['true', '1'] else 0
        all_counts[arm]['total'] += 1
        all_counts[arm]['success'] += success
        if task in ['T1', 'T2', 'T3', 'T4', 'T5']:
            t1_t5_counts[arm]['total'] += 1
            t1_t5_counts[arm]['success'] += success

print('=== T1-T5 restricted counts ===')
for arm, d in sorted(t1_t5_counts.items()):
    s = d['success']
    tot = d['total']
    pct = (s / tot * 100) if tot else 0
    print(f'{arm:20}: {s} / {tot} ({pct:.1f}%)')

print('\n=== All tasks (T1-T6) counts ===')
for arm, d in sorted(all_counts.items()):
    s = d['success']
    tot = d['total']
    pct = (s / tot * 100) if tot else 0
    print(f'{arm:20}: {s} / {tot} ({pct:.1f}%)')

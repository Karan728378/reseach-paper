import csv
import os
from collections import Counter

def inspect_csv(path):
    print(f"=== {path} ===")
    if not os.path.exists(path):
        print("File not found.")
        return
    with open(path, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
    print(f"Row count: {len(reader)}")
    if not reader:
        return
    print(f"Field names: {list(reader[0].keys())}")
    
    # check run_id, model, status, arm, success, duration
    run_ids = Counter(r.get('run_id') for r in reader)
    print(f"Unique run_ids: {len(run_ids)}")
    duplicates = {k: v for k, v in run_ids.items() if v > 1}
    if duplicates:
        print(f"Duplicates (run_id: count): {duplicates}")
    
    models = Counter(r.get('model') or r.get('model_name') for r in reader)
    print(f"Models: {dict(models)}")
    
    arms = Counter(r.get('arm') for r in reader)
    print(f"Arms: {dict(arms)}")
    
    statuses = Counter(r.get('status') or r.get('success') for r in reader)
    print(f"Statuses/Success: {dict(statuses)}")
    
    durations = [float(r['duration']) for r in reader if r.get('duration')]
    if durations:
        print(f"Durations (min, mean, max): {min(durations):.2f}s, {sum(durations)/len(durations):.2f}s, {max(durations):.2f}s")
        print(f"All durations: {durations}")
    print()

inspect_csv('results/v3_run_summary.csv')
inspect_csv('results/v3_3arm_summary.csv')
inspect_csv('results/local_llama_summary.csv')

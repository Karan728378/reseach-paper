import csv
from collections import defaultdict
from pathlib import Path

summary_file = Path("results/v3_3arm_summary.csv")
with open(summary_file, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

valid_rows = [r for r in rows if r.get("status") in ["completed", "failed"]]
infra_rows = [r for r in rows if r.get("status") == "infrastructure_aborted"]

print(f"Total Rows in Summary: {len(rows)}")
print(f"Valid Behavioral Trials: {len(valid_rows)}")
print(f"Infrastructure Aborts: {len(infra_rows)}")

arm_stats = defaultdict(lambda: {"total": 0, "success": 0, "steps": []})
task_stats = defaultdict(lambda: {"total": 0, "success": 0, "arms": defaultdict(int)})
block_stats = defaultdict(lambda: {"total": 0, "success": 0})

for r in valid_rows:
    arm = r["arm"]
    task = r["task_id"]
    block = r["block_id"]
    succ = r["success"].lower() == "true"
    steps = int(r["total_steps"])
    
    arm_stats[arm]["total"] += 1
    if succ:
        arm_stats[arm]["success"] += 1
    arm_stats[arm]["steps"].append(steps)
    
    task_stats[task]["total"] += 1
    if succ:
        task_stats[task]["success"] += 1
        task_stats[task]["arms"][arm] += 1
        
    block_stats[block]["total"] += 1
    if succ:
        block_stats[block]["success"] += 1

print("\n=== PER-ARM SUMMARY ===")
for arm in ["ABS", "ARIA", "DATA-CFG"]:
    st = arm_stats[arm]
    n = st["total"]
    s = st["success"]
    mean_steps = sum(st["steps"]) / len(st["steps"]) if st["steps"] else 0
    pct = (s / n * 100) if n > 0 else 0
    print(f"  {arm:10s}: {s}/{n} ({pct:.1f}%) | Mean Steps: {mean_steps:.2f}")

print("\n=== PER-TASK SUMMARY ===")
for task in sorted(task_stats.keys()):
    st = task_stats[task]
    s = st["success"]
    tot = st["total"]
    pct = (s / tot * 100) if tot > 0 else 0
    print(f"  Task {task}: {s}/{tot} ({pct:.1f}%) | Arm breakdown: {dict(st['arms'])}")

print("\n=== PER-BLOCK SUMMARY ===")
for b in sorted(block_stats.keys()):
    st = block_stats[b]
    s = st["success"]
    tot = st["total"]
    print(f"  Block {b}: {s}/{tot} completed")

if infra_rows:
    print("\n=== INFRASTRUCTURE ABORTS ===")
    for ir in infra_rows:
        print(f"  Run {ir['run_index']} (Block {ir['block_id']}, Arm {ir['arm']}, Task {ir['task_id']}): {ir['error_message'][:80]}...")

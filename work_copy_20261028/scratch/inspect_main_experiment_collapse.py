import csv
from pathlib import Path

p = Path("C:/testing/results/main_experiment/full-summary.csv")
with open(p, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in main experiment full-summary.csv: {len(rows)}")

print("\n--- Transition around Run 105 ---")
for r in rows[100:112]:
    idx = r['scheduled_run_index']
    rep = r['repetition_index']
    var = r['variant']
    tid = r['task_id']
    suc = r['success']
    pts = r['partial_score']
    stp = r['total_steps']
    dur = float(r['total_time_seconds'])
    tme = r['timestamp_end']
    print(f"Idx {idx:>3} | Rep {rep:>2} | {var:<16} {tid:<3} | succ={suc:<5} score={pts:<4} steps={stp:<2} dur={dur:>5.1f}s | {tme}")

print("\n--- Checking raw JSONL files for False runs ---")
raw_dir = Path("C:/testing/results/main_experiment/raw")
if not raw_dir.exists():
    raw_dir = Path("C:/testing/results_EXP1_FROZEN_BACKUP/raw")
print(f"Checking raw directory: {raw_dir} (exists: {raw_dir.exists()})")

# Look at run 106 and 107
for r in rows[105:108]:
    run_id = r["run_id"]
    jsonl_candidates = list(Path("C:/testing").rglob(f"*{run_id}*.jsonl"))
    print(f"Run {r['scheduled_run_index']} ({run_id}): found {len(jsonl_candidates)} jsonl files")
    for jf in jsonl_candidates:
        lines = open(jf, "r", encoding="utf-8", errors="ignore").readlines()
        print(f"  {jf}: {len(lines)} lines")
        if lines:
            print(f"    first line: {lines[0][:120]}")
            print(f"    last line:  {lines[-1][:120]}")

import csv
from pathlib import Path

raw_csv = Path("results/v3_3arm_summary_raw.csv")
clean_csv = Path("results/v3_3arm_summary.csv")

with open(raw_csv, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

simulated_clean = []
seen_completed = set()

for r in rows:
    idx = int(r["run_index"])
    status = r["status"]
    err = r["error_message"]
    is_infra = ("infra" in status) or ("quota" in status) or ("503" in err) or ("unavailable" in err.lower())
    
    if is_infra:
        simulated_clean.append(r)
    else:
        if idx not in seen_completed:
            seen_completed.add(idx)
            simulated_clean.append(r)

with open(clean_csv, "r", encoding="utf-8") as f:
    actual_clean = list(csv.DictReader(f))

print(f"Simulated length: {len(simulated_clean)}")
print(f"Actual clean length: {len(actual_clean)}")

diffs = []
for i, (sim, act) in enumerate(zip(simulated_clean, actual_clean)):
    if sim != act:
        diffs.append((i, sim, act))

print(f"Row differences: {len(diffs)}")
if not diffs:
    print("SUCCESS: simulated_clean matches actual_clean row-for-row exactly!")

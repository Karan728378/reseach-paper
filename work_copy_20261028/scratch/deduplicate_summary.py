import csv
from pathlib import Path

raw_csv = Path("results/v3_3arm_summary_raw.csv")
clean_csv = Path("results/v3_3arm_summary.csv")

with open(raw_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

clean_rows = []
seen_completed = set()

for r in rows:
    idx = int(r["run_index"])
    status = r["status"]
    err = r["error_message"]
    is_infra = ("infra" in status) or ("quota" in status) or ("503" in err) or ("unavailable" in err.lower())
    
    if is_infra:
        clean_rows.append(r)
    else:
        if idx not in seen_completed:
            seen_completed.add(idx)
            clean_rows.append(r)
        else:
            print(f"Deduplicated duplicate completion for Run {idx} (timestamp: {r['timestamp_start']})")

with open(clean_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(clean_rows)

print(f"Successfully wrote {len(clean_rows)} rows ({len(seen_completed)} unique completed runs) to {clean_csv}")

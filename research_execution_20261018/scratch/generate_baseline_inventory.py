import hashlib
import json
import csv
from pathlib import Path

def get_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

root = Path("C:/testing/research_execution_20261018")
runs_dir = root / "results" / "3arm_runs"
raw_csv = root / "results" / "v3_3arm_summary_raw.csv"
clean_csv = root / "results" / "v3_3arm_summary.csv"

json_files = sorted(runs_dir.glob("*.json"))

report = []
report.append("# BASELINE DATA INVENTORY AND SHA-256 REGISTRY")
report.append(f"Generated at: 2026-10-26T17:58:00Z\n")
report.append("## 1. Summary CSV Artifacts\n")
report.append("| Artifact Name | Relative Path | File Size (Bytes) | Row Count (Excl Header) | SHA-256 Hash |")
report.append("|---|---|---|---|---|")

for csv_path, label in [(raw_csv, "Raw Summary CSV"), (clean_csv, "Cleaned Summary CSV")]:
    size = csv_path.stat().st_size
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    row_count = len(rows)
    h = get_sha256(csv_path)
    report.append(f"| {label} | `{csv_path.relative_to(root)}` | {size} | {row_count} | `{h}` |")

report.append("\n## 2. Raw JSON Attempt Files in `results/3arm_runs/`\n")
report.append(f"Total JSON files: {len(json_files)}\n")
report.append("| File Name | Size (Bytes) | SHA-256 Hash | Run Index | Attempt | Status | Score | Arm | Task | Timestamp Start |")
report.append("|---|---|---|---|---|---|---|---|---|---|")

all_json_schemas = set()

for jf in json_files:
    size = jf.stat().st_size
    h = get_sha256(jf)
    with open(jf, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    all_json_schemas.update(data.keys())
    
    run_idx = data.get("run_index", "")
    # Check attempt number
    attempt = data.get("attempt_number", 1)
    if "attempt_" in jf.name:
        parts = jf.stem.split("attempt_")
        if len(parts) > 1 and parts[1].isdigit():
            attempt = int(parts[1])
            
    status = data.get("status", "")
    score = data.get("score", "")
    arm = data.get("arm", "")
    task = data.get("task_id", "")
    t_start = data.get("timestamp_start", "")
    
    report.append(f"| `{jf.name}` | {size} | `{h}` | {run_idx} | {attempt} | {status} | {score} | {arm} | {task} | {t_start} |")

report.append("\n## 3. JSON Trace Schema Inspection\n")
report.append("Discovered top-level keys across all 46 JSON trace files:")
for k in sorted(all_json_schemas):
    report.append(f"- `{k}`")

output_path = root / "BASELINE_DATA_INVENTORY_SHA256.md"
output_path.write_text("\n".join(report), encoding="utf-8")
print(f"Wrote baseline inventory to {output_path}")

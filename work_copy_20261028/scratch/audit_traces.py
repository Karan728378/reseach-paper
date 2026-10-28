import json, csv
from pathlib import Path

root = Path("C:/testing/research_execution_20261018")
sched_path = root / "proposed_3arm_schedule.csv"
runs_dir = root / "results" / "3arm_runs"
raw_csv_path = root / "results" / "v3_3arm_summary_raw.csv"

with open(sched_path, "r", encoding="utf-8") as f:
    schedule = {int(r["run_index"]): r for r in csv.DictReader(f)}

with open(raw_csv_path, "r", encoding="utf-8") as f:
    raw_rows = list(csv.DictReader(f))

json_files = sorted(runs_dir.glob("*.json"))

print(f"Total schedule units: {len(schedule)}")
print(f"Total raw CSV rows: {len(raw_rows)}")
print(f"Total JSON files: {len(json_files)}")

metadata_mismatches = []
treatment_evidence_missing = []
verification_anomalies = []

for jf in json_files:
    with open(jf, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    idx = int(data.get("run_index", -1))
    sched_row = schedule.get(idx)
    if not sched_row:
        metadata_mismatches.append((jf.name, f"Index {idx} not in schedule"))
        continue
        
    # Check metadata alignment
    for field in ["arm", "task_id", "block_id", "variant_mapping", "target_entity"]:
        val_json = str(data.get(field, "")).strip()
        val_sched = str(sched_row.get(field, "")).strip()
        if val_json != val_sched:
            metadata_mismatches.append((jf.name, f"Field '{field}' mismatch: json='{val_json}' vs sched='{val_sched}'"))
            
    # Check status and evidence
    status = data.get("status")
    if status == "completed":
        # Verifier result check
        v_res = data.get("verifier_result")
        if not v_res or "success" not in v_res:
            verification_anomalies.append((jf.name, "Missing verifier_result"))
        # Treatment delivery check
        t_del = data.get("treatment_delivery") or {}
        # In runner, treatment delivery was also captured in treatment_attribute_observed / treatment_delivery_evidence
        # Let's check both JSON fields and summary CSV fields
        obs_count = len(data.get("captured_observations", []))
        if obs_count == 0 and not data.get("treatment_delivery_evidence"):
            treatment_evidence_missing.append((jf.name, "No observation or treatment evidence"))

print(f"Metadata mismatches against schedule: {len(metadata_mismatches)}")
if metadata_mismatches:
    for m in metadata_mismatches:
        print(" ", m)

print(f"Verification anomalies: {len(verification_anomalies)}")
if verification_anomalies:
    for v in verification_anomalies:
        print(" ", v)

print(f"Treatment evidence missing: {len(treatment_evidence_missing)}")
if treatment_evidence_missing:
    for t in treatment_evidence_missing:
        print(" ", t)

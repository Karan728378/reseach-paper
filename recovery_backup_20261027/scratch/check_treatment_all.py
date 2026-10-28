import json
from pathlib import Path

runs_dir = Path("results/3arm_runs")
json_files = sorted(runs_dir.glob("*.json"))

print(f"{'File':<24} {'Status':<16} {'Observed':<10} {'Evidence'}")
print("-" * 90)
for jf in json_files:
    with open(jf, "r", encoding="utf-8") as f:
        data = json.load(f)
    status = data.get("status")
    td = data.get("treatment_delivery") or {}
    observed = td.get("treatment_attribute_observed", "N/A")
    evidence = td.get("evidence", "NONE")
    if len(str(evidence)) > 50:
        evidence = str(evidence)[:47] + "..."
    print(f"{jf.name:<24} {status:<16} {str(observed):<10} {evidence}")

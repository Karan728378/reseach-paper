import subprocess
import sys
import time
import json
from pathlib import Path

scripts_to_run = [
    ("Phase 1 Baseline & Hash Check", [sys.executable, "phase1_execute.py"]),
    ("Phase 6 Run Accounting & Provenance", [sys.executable, "phase6_execute.py"]),
    ("Phase 7 Statistical Audit & MC Reproduction", [sys.executable, "phase7_execute.py"]),
    ("Phase 9 Information Loss & Wheel Audit", [sys.executable, "phase9_execute.py"]),
    ("Citation Key Audit", [sys.executable, "audit_citation_keys.py"]),
    ("Route Controls & Correspondence Audit", [sys.executable, "audit_route_controls_and_correspondence.py"]),
]

results = []

print("="*80)
print(f"{'Script Description':<45} | {'Exit':<5} | {'Time (s)':<8} | Status")
print("="*80)

for desc, cmd in scripts_to_run:
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
    dt = time.time() - t0
    status = "SUCCESS" if res.returncode == 0 else "FAILED"
    print(f"{desc:<45} | {res.returncode:<5} | {dt:<8.3f} | {status}")
    results.append({
        "description": desc,
        "command": " ".join(cmd),
        "exit_code": res.returncode,
        "duration_sec": round(dt, 4),
        "status": status,
        "stdout_tail": res.stdout.strip()[-500:] if res.stdout else "",
        "stderr_tail": res.stderr.strip()[-500:] if res.stderr else "",
    })

with open("scratch/offline_script_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("="*80)
print("Finished running all offline audit scripts.")

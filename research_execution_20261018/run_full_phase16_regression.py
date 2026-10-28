import subprocess
import sys
import time

commands = [
    ("Unittest Discovery (207 tests)", [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py"]),
    ("Manuscript Consistency", [sys.executable, "test_manuscript_consistency.py"]),
    ("Confirmatory Protocol Dryrun", [sys.executable, "test_confirmatory_protocol_dryrun.py"]),
    ("Phase 9 Strengthening", [sys.executable, "test_phase9_strengthening.py"]),
    ("Citation Key Audit", [sys.executable, "audit_citation_keys.py"]),
]

all_passed = True
results = []

for name, cmd in commands:
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
    dt = time.time() - t0
    status = "PASS" if res.returncode == 0 else "FAIL"
    if res.returncode != 0:
        all_passed = False
    results.append({
        "name": name,
        "command": " ".join(cmd),
        "status": status,
        "duration_sec": round(dt, 3),
        "returncode": res.returncode,
        "stdout_tail": res.stdout.strip()[-300:] if res.stdout else "",
        "stderr_tail": res.stderr.strip()[-300:] if res.stderr else "",
    })
    print(f"[{status}] {name} in {dt:.3f}s (Exit code: {res.returncode})")

print("\n" + "="*50)
if all_passed:
    print("ALL 5 REGRESSION SUITES PASSED CLEANLY (EXIT CODE 0)!")
else:
    print("SOME REGRESSION SUITES FAILED!")
    sys.exit(1)

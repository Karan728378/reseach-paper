import subprocess
import glob
import sys
import json
import os
import time

test_files = sorted(glob.glob('test_*.py'))
results = []

print("="*85)
print(f"{'Module Name':<42} | {'Status':<6} | {'Exit':<4} | {'Time (s)':<8} | Summary")
print("="*85)

total_tests = 0
total_passed = 0
total_failed = 0
total_errors = 0

for tf in test_files:
    mod_name = tf[:-3]
    t0 = time.time()
    res = subprocess.run(
        [sys.executable, "-m", "unittest", mod_name],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    dt = time.time() - t0
    
    stdout = res.stdout.strip()
    stderr = res.stderr.strip()
    combined = stdout + "\n" + stderr
    
    # Parse test count and status from stderr/stdout
    # e.g., "Ran 10 tests in 0.050s"
    # "OK" or "FAILED (failures=1, errors=0)"
    import re
    m_ran = re.search(r"Ran (\d+) test", combined)
    count = int(m_ran.group(1)) if m_ran else 0
    status = "PASS" if res.returncode == 0 else "FAIL"
    
    # Check if 0 tests ran
    if count == 0 and res.returncode == 0 and "Ran 0 tests" in combined:
        summary = "No unittest.TestCase classes (standalone/live script)"
        status = "N/A"
    elif res.returncode == 0:
        summary = f"OK ({count} tests)"
        total_passed += count
        total_tests += count
    else:
        summary = stderr.split("\n")[-1] if stderr else "FAILED"
        total_failed += count
        total_tests += count
        
    print(f"{mod_name:<42} | {status:<6} | {res.returncode:<4} | {dt:<8.3f} | {summary}")
    
    results.append({
        "module": mod_name,
        "file": tf,
        "tests": count,
        "status": status,
        "exit_code": res.returncode,
        "duration_sec": round(dt, 4),
        "stdout": stdout,
        "stderr": stderr
    })

print("="*85)
print(f"Total Unit Tests Passing: {total_passed} across {len([r for r in results if r['status'] == 'PASS'])} modules.")
print(f"Total Unit Tests Failing: {total_failed}")
print("="*85)

with open("scratch/individual_test_results.json", "w", encoding="utf-8") as out_f:
    json.dump(results, out_f, indent=2)

print("\nWrote scratch/individual_test_results.json successfully.")

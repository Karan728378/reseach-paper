"""
Comprehensive audit of all test_*.py modules in work_copy (excluding backups/).
Evaluates:
- Discovered modules
- Collectable test cases per module
- Import failures with exact error messages
- Reconciles total test counts
"""
import glob
import os
import sys
import unittest
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def audit_tests():
    test_files = sorted([f for f in ROOT.glob("test_*.py") if "backups" not in f.parts])
    print(f"Total test_*.py files in root: {len(test_files)}")

    results = []
    total_collected = 0
    import_failures = []

    loader = unittest.defaultTestLoader

    for tf in test_files:
        mod_name = tf.stem
        try:
            suite = loader.loadTestsFromName(mod_name)
            count = suite.countTestCases()
            total_collected += count
            results.append((mod_name, count, "OK", ""))
        except Exception as e:
            import_failures.append((mod_name, repr(e)))
            results.append((mod_name, 0, "IMPORT_FAIL", repr(e)))

    print("\n--- PER-MODULE TEST COLLECTION ---")
    print(f"{'Module Name':<45} | {'Tests':<6} | {'Status':<12} | {'Error'}")
    print("-" * 90)
    for mod, count, status, err in results:
        err_snippet = err[:40] if err else ""
        print(f"{mod:<45} | {count:<6} | {status:<12} | {err_snippet}")

    print("\n" + "=" * 50)
    print(f"Total Modules Scanned: {len(test_files)}")
    print(f"Modules Successfully Loaded: {len([r for r in results if r[2] == 'OK'])}")
    print(f"Modules Failing Import: {len(import_failures)}")
    print(f"Total Collectable Test Cases: {total_collected}")
    print("=" * 50)

    if import_failures:
        print("\n--- IMPORT FAILURES DETAILS ---")
        for mod, err in import_failures:
            print(f"[{mod}]: {err}")

if __name__ == "__main__":
    audit_tests()

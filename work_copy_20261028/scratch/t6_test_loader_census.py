import unittest
import glob
import sys
import os

sys.path.insert(0, 'C:/testing/work_copy_20261028')
os.chdir('C:/testing/work_copy_20261028')

test_files = sorted(glob.glob('test_*.py'))
print(f"Total test_*.py files in root: {len(test_files)}")

results = []
total_tests = 0
import_fails = []

for f in test_files:
    m = f[:-3]
    try:
        suite = unittest.defaultTestLoader.loadTestsFromName(m)
        c = suite.countTestCases()
        results.append((c, m))
        total_tests += c
    except Exception as e:
        import_fails.append((m, str(e)))

print("\n--- Test Counts by Module ---")
for c, m in results:
    print(f"  {m:<45}: {c:>3} tests")

if import_fails:
    print("\n--- Import Failures ---")
    for m, err in import_fails:
        print(f"  {m:<45}: {err[:80]}")

print(f"\nTotal importable test modules: {len(results)}")
print(f"Total collectable tests      : {total_tests}")

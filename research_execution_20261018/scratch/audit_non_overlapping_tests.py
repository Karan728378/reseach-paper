import ast
from pathlib import Path

def analyze_test_overlap():
    exec_dir = Path(r"C:\testing\research_execution_20261018")
    test_files = sorted(list(exec_dir.glob("test_*.py")) + [exec_dir / "offline_test_suite.py"])

    all_tests = []
    by_file = {}

    for tf in test_files:
        if not tf.exists():
            continue
        try:
            tree = ast.parse(tf.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error parsing {tf.name}: {e}")
            continue

        file_tests = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check for test methods
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef) and sub.name.startswith("test_"):
                        full_name = f"{node.name}.{sub.name}"
                        file_tests.append(full_name)
                        all_tests.append({
                            "file": tf.name,
                            "class": node.name,
                            "method": sub.name,
                            "full_name": full_name
                        })
        by_file[tf.name] = file_tests

    total_test_definitions = len(all_tests)
    unique_methods = set(t["method"] for t in all_tests)
    unique_full_names = set(t["full_name"] for t in all_tests)

    print("=== Test Suite Inventory & Overlap Audit ===")
    print(f"Total test files audited: {len(by_file)}")
    for fname, tests in by_file.items():
        print(f"  {fname:<40} : {len(tests):>3} tests")

    print(f"\nTotal test case methods defined: {total_test_definitions}")
    print(f"Unique test method names: {len(unique_methods)}")
    print(f"Unique (Class.Method) identifiers: {len(unique_full_names)}")

    # Check for duplicate names across files
    method_occurrences = {}
    for t in all_tests:
        m = t["method"]
        method_occurrences.setdefault(m, []).append(t["file"])

    duplicates = {m: files for m, files in method_occurrences.items() if len(files) > 1}
    print(f"\nDuplicate test method names across multiple files: {len(duplicates)}")
    for d, files in duplicates.items():
        print(f"  - '{d}' appears in: {files}")

if __name__ == "__main__":
    analyze_test_overlap()

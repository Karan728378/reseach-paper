import unittest
import time
import json
from pathlib import Path

ROOT = Path("C:/testing/research_execution_20261018")
OUT_DIR = ROOT / "local_closure_results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

test_files = [
    "test_forensic_audit_regressions.py",
    "test_power_audit.py",
    "test_schedule_validity.py",
    "test_budget_controls.py",
    "test_budget_guard_repairs.py",
    "test_treatment_leakage_and_integrity.py",
    "test_observation_pipeline_stages.py",
    "test_aria_baseline_prompt_divergence.py",
    "test_baseline_pooling_consistency.py",
    "test_browser_lifecycle_and_recovery.py",
    "test_verifier_ground_truth_battery.py",
    "test_sentinel_pipeline.py",
    "test_runner_guard_integration.py",
    "test_live_instrumentation_offline.py",
    "test_implementation_fixes.py",
    "test_mutation_audit.py",
    "test_analyze_v3_results.py"
]

results = []
total_ran = 0
total_passed = 0
total_failed = 0
total_errors = 0

t_start_all = time.monotonic()

for tf in test_files:
    p = ROOT / tf
    if not p.exists():
        results.append({
            "file": tf,
            "status": "NOT_FOUND",
            "tests_ran": 0,
            "failures": 0,
            "errors": 0,
            "duration_s": 0.0
        })
        continue

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(ROOT), pattern=tf)
    runner = unittest.TextTestRunner(verbosity=0)
    
    t0 = time.monotonic()
    test_result = runner.run(suite)
    duration = time.monotonic() - t0
    
    ran = test_result.testsRun
    fails = len(test_result.failures)
    errs = len(test_result.errors)
    passed = ran - fails - errs
    
    total_ran += ran
    total_passed += passed
    total_failed += fails
    total_errors += errs
    
    status = "PASS" if (fails == 0 and errs == 0) else "FAIL"
    
    fail_details = [f"{case.id()}: {msg}" for case, msg in test_result.failures]
    err_details = [f"{case.id()}: {msg}" for case, msg in test_result.errors]
    
    results.append({
        "file": tf,
        "status": status,
        "tests_ran": ran,
        "passed": passed,
        "failures": fails,
        "errors": errs,
        "duration_s": round(duration, 3),
        "failure_details": fail_details,
        "error_details": err_details
    })
    print(f"[{status}] {tf:<42} | Ran: {ran:>2} | Passed: {passed:>2} | Fail: {fails} | Err: {errs} ({duration:.2f}s)")

total_duration = time.monotonic() - t_start_all

summary = {
    "total_suites": len(test_files),
    "total_tests_ran": total_ran,
    "total_passed": total_passed,
    "total_failed": total_failed,
    "total_errors": total_errors,
    "overall_status": "ALL_PASSED" if (total_failed == 0 and total_errors == 0) else "FAILURES_DETECTED",
    "total_duration_s": round(total_duration, 2),
    "suite_results": results
}

out_json = OUT_DIR / "OFFLINE_TEST_EXECUTION_AUDIT.json"
out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

# Generate Markdown
md = [
    "# Offline Test Execution and Verification Audit",
    "",
    f"- **Total Test Suites Executed:** {len(test_files)}",
    f"- **Total Tests Executed:** **{total_ran}**",
    f"- **Passed:** **{total_passed}** ({total_passed/total_ran*100:.1f}%)" if total_ran else "- **Passed:** 0",
    f"- **Failures:** **{total_failed}**",
    f"- **Errors:** **{total_errors}**",
    f"- **Total Duration:** {total_duration:.2f} seconds",
    f"- **Overall Verdict:** **{'100% PASS' if total_failed == 0 and total_errors == 0 else 'FAILURES'}**",
    "",
    "## Suite-by-Suite Execution Breakdown",
    "",
    "| Test Suite File | Status | Ran | Passed | Failed | Errors | Duration (s) |",
    "|---|---|---|---|---|---|---|"
]

for r in results:
    md.append(f"| `{r['file']}` | **{r['status']}** | {r['tests_ran']} | {r['passed']} | {r['failures']} | {r['errors']} | {r['duration_s']}s |")

if total_failed > 0 or total_errors > 0:
    md.extend(["", "## Failure and Error Details", ""])
    for r in results:
        if r['failures'] > 0 or r['errors'] > 0:
            md.append(f"### `{r['file']}`")
            for fd in r['failure_details']:
                md.append(f"- **Failure:** {fd[:200]}")
            for ed in r['error_details']:
                md.append(f"- **Error:** {ed[:200]}")

out_md = OUT_DIR / "OFFLINE_TEST_EXECUTION_AUDIT.md"
out_md.write_text("\n".join(md), encoding="utf-8")
print(f"\n[DONE] Exported {out_json} and {out_md}")
print(f"Grand Total: {total_ran} tests | {total_passed} passed | {total_failed} failed | {total_errors} errors")

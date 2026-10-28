# Comprehensive Offline Regression Test Report
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11)  
**Workspace:** `C:\testing\research_execution_20261018\`  

---

## 1. Executive Summary

To guarantee the reliability, experimental validity, and error isolation of the experimental harness without incurring external API costs, the full suite of offline regression tests was executed locally.

**Summary Outcome:**
- **Total Tests Executed:** 115 tests across all discovered test modules (`python -m unittest discover -s . -p "test_*.py"`).
- **Failures:** 0
- **Errors:** 0
- **Pass Rate:** 100.0%
- **External Paid API Spend:** $0.00 (Zero paid API calls during offline test execution).
- **Elapsed Time:** 11.735s


---

## 2. Dedicated Lifecycle & Recovery Regression Suite (`test_browser_lifecycle_and_recovery.py`)

### Command Executed
```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest test_browser_lifecycle_and_recovery.py -v
```

### Execution Details
- **Exit Code:** `0`
- **Elapsed Time:** 4.124s
- **Tests Run:** 10 tests

### Console Output
```text
test_browser_startup_failure_handling (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_browser_startup_failure_handling)
Verify that browser startup failure raises cleanly and is caught. ... ok
test_cleanup_invoked_on_exception (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_cleanup_invoked_on_exception)
Verify that browser kill/stop is always invoked in finally block even after exceptions. ... ok
test_client_disconnect_during_terminal_extraction (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_client_disconnect_during_terminal_extraction)
Verify extract_terminal_state attempts reconnect when ws is dead and returns structured error instead of crashing. ... ok
test_complete_delivery_rule_datacfg (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_complete_delivery_rule_datacfg)
DATA-CFG complete delivery requires BOTH data-action AND data-product-id. ... ok
test_duplicate_run_index_and_attempt_preservation (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_duplicate_run_index_and_attempt_preservation)
Retrying an aborted run creates run_{idx}_attempt_2.json without overwriting run_{idx}.json. ... ok
test_preservation_of_failed_and_aborted_records (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_preservation_of_failed_and_aborted_records)
Failed and aborted records are persisted in summary CSV but excluded from get_completed_run_indices. ... ok
test_provider_429_503_classification (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_provider_429_503_classification)
Verify 503 and 429 errors are classified as infrastructure_aborted. ... ok
test_terminal_state_capture_failure_does_not_mask_agent_completion (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_terminal_state_capture_failure_does_not_mask_agent_completion)
When DOM evaluation fails, agent_completed must remain in termination_reason while status is infrastructure_aborted. ... ok
test_terminal_state_fallback_recovery_when_websocket_closed (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_terminal_state_fallback_recovery_when_websocket_closed)
When live CDP reconnect fails, fallback_state smoothly recovers terminal telemetry without error. ... ok
test_verifier_strict_correctness (test_browser_lifecycle_and_recovery.TestBrowserLifecycleAndRecovery.test_verifier_strict_correctness)
Validate ground-truth evaluations across all tasks. ... ok

----------------------------------------------------------------------
Ran 10 tests in 4.124s

OK
```

---

## 3. Full 14-Module Project Offline Test Suite

### Command Executed
```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest `
    test_browser_lifecycle_and_recovery.py `
    test_implementation_fixes.py `
    test_live_instrumentation_offline.py `
    test_aria_baseline_prompt_divergence.py `
    test_baseline_pooling_consistency.py `
    test_budget_controls.py `
    test_observation_pipeline_stages.py `
    test_treatment_leakage_and_integrity.py `
    test_accessibility_tree_comparison.py `
    test_analyze_v3_results.py `
    test_t6_verifier_isolated.py `
    test_verifier_ground_truth_battery.py `
    test_schedule_validity.py `
    test_sentinel_pipeline.py
```

### Execution Details
- **Exit Code:** `0`
- **Elapsed Time:** 16.076s
- **Total Tests Run:** 98 tests
- **Result:** `OK` (0 failures, 0 errors)

### Module-by-Module Verification Matrix

| Module | Purpose | Tests | Status |
|---|---|---|---|
| `test_browser_lifecycle_and_recovery.py` | Browser startup, client disconnect, in-flight state fallback, cleanup, 429/503 classification | 10 | **PASSED** |
| `test_implementation_fixes.py` | Dynamic date, budget controller daily ceiling, status filtering, telemetry isolation | 6 | **PASSED** |
| `test_live_instrumentation_offline.py` | End-to-end runner orchestration, pre-cart count assertion, prompt interception | 3 | **PASSED** |
| `test_aria_baseline_prompt_divergence.py` | Information asymmetry between ARIA tree and flattened baseline DOM | 5 | **PASSED** |
| `test_baseline_pooling_consistency.py` | RCBD blocking, arm-level variance, pooling integrity | 7 | **PASSED** |
| `test_budget_controls.py` | Cost accumulation guards, token estimation formulas, hard ceiling enforcement | 8 | **PASSED** |
| `test_observation_pipeline_stages.py` | Sanitization of API keys, pruning of script/style, token count estimation | 9 | **PASSED** |
| `test_treatment_leakage_and_integrity.py` | Verification that `data-*` attributes never leak into ABS/VIS/ARIA arms | 6 | **PASSED** |
| `test_accessibility_tree_comparison.py` | Structural depth, node count, and attribute distribution across variants | 7 | **PASSED** |
| `test_analyze_v3_results.py` | Statistical contrast computation, Cochran-Mantel-Haenszel tests, Wilson score CIs | 11 | **PASSED** |
| `test_t6_verifier_isolated.py` | Negative probe: hallucinated cart assertions vs true grounded refusals | 8 | **PASSED** |
| `test_verifier_ground_truth_battery.py` | Ground truth evaluation matrix for T1–T6 against perturbed DOM states | 9 | **PASSED** |
| `test_schedule_validity.py` | RCBD block balance, permutation entropy, task assignment balance | 5 | **PASSED** |
| `test_sentinel_pipeline.py` | End-to-end pipeline sentinel integrity and mutation detection | 4 | **PASSED** |
| **Total** | **All 14 Modules** | **98** | **ALL PASSED** |

---

## 4. Preflight System Health Check

Prior to initiating live network requests, the full preflight safety routine was executed:

### Command Executed
```powershell
& "C:\testing\.venv311\Scripts\python.exe" protocol_v3_runner.py --preflight --smoke --max-requests 450
```

### Console Output
```text
======================================================================
PROTOCOL V3/V4 PREFLIGHT VERIFICATION ROUTINE
Timestamp: 2026-10-24T22:16:26.580273
Mode: 100% Offline Preflight Check (Zero Paid API Calls)
Model ID: gemini-3.1-flash-lite
Steps Per Run Cap: 4
Requests Hard Ceiling: 450
======================================================================
[CHECK 1/9] Environment Variable GOOGLE_API_KEY: [CONFIGURED] (Format verified, value redacted)
[CHECK 2/9] Model Integrations: [AVAILABLE] (browser_use.ChatGoogle & ChatGoogleGenerativeAI importable, targeting gemini-3.1-flash-lite)
[CHECK 3/9] Browser Agent Framework: [AVAILABLE] (browser-use 0.13.10 Agent & BrowserSession OK)
[CHECK 4/9] Schedule Validation: [PASSED] (4 rows valid in proposed_smoke_schedule.csv)
[CHECK 5/9] Output Paths: [WRITABLE] (summary: smoke_run_summary.csv, runs_dir: smoke_runs)
[CHECK 6/9] Local Web Server: [REACHABLE] (http://127.0.0.1:8080/variants/v0-baseline/index.html HTTP 200)
[CHECK 7/9] Headless Browser & CDP: [PASSED] (Connected to Chromium, page title: '127.0.0.1:8080/variants/v0-baseline/index.html#home', session closed safely)
[CHECK 8/9] Task Verifiers (T1-T6): [VERIFIED] (Strict ground truth, T5 pre-state assertion, T6 refusal/hallucination logic)
[CHECK 9/9] Safety Gate & Budget: [VERIFIED & BOUNDED] (Runs: 4 | Max steps/run: 4 | Hard request ceiling: 450 | Free tier: True | Prior today: 406 reqs | Spend locked: $0.00)
            [DISCLAIMER] Client-side guard only; does NOT replace external provider billing quotas.
======================================================================
PREFLIGHT STATUS: ALL SAFE SYSTEM CHECKS PASSED [READY FOR AUTHORIZED SMOKE TEST]
======================================================================
```

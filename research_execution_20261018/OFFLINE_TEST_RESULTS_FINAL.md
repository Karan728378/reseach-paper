# OFFLINE TEST RESULTS REPORT (FINAL)

**Project Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Workspace:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe`  
**Date:** October 26, 2026  
**Auditor:** Python Test & Reproducibility Lead  
**Execution Command:** `& "C:\testing\.venv311\Scripts\python.exe" -m unittest discover -s . -p "test_*.py"`  
**Result:** **191 / 191 PASSED (100.0%, Exit Code 0, Runtime: 22.069s)**

---

## 1. Test Suite Summary Table

| # | Test Suite Module | Test Count | Pass Rate | Primary Verification Outcome |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `test_data_reconciliation_and_provenance.py` | 20 | **100%** | Validates raw attempt mapping, duplicate run quarantine (Runs 34 & 38), 72-unit schedule accounting, SHA-256 integrity. |
| 2 | `test_disambiguation_probes.py` | 9 | **100%** | Validates Probes A, B, and Positive Control HTML fixtures, button IDs, and Stage 4 serializer visibility. |
| 3 | `test_analyze_v3_results.py` | 11 | **100%** | Validates CMH test, stratified odds ratios, Newcombe score CIs against Agresti (2002) benchmarks. |
| 4 | `test_baseline_pooling_consistency.py` | 5 | **100%** | Validates that baseline arms are reported unpooled in Table 3 and pooling is formally rejected in Table 4. |
| 5 | `test_forensic_audit_regressions.py` | 8 | **100%** | Validates Run 26 retry accounting and abstract numerical alignment (10.8% and 49.6% power). |
| 6 | `test_power_audit.py` | 7 | **100%** | Validates Monte Carlo RCBD power simulation concordance, binomial sample size formulas, and DEFF. |
| 7 | `test_observation_pipeline_stages.py` | 6 | **100%** | Validates AST pruning rules: `DISABLED_ELEMENTS`, line 1046 tag stripping, and attribute whitelisting. |
| 8 | `test_sentinel_pipeline.py` | 4 | **100%** | Validates sentinel token injection and tracking across multi-stage observation representations. |
| 9 | `test_treatment_leakage_and_integrity.py` | 4 | **100%** | Validates treatment isolation, ensuring baseline variants do not leak experimental markup. |
| 10 | `test_accessibility_tree_comparison.py` | 9 | **100%** | Validates Blink AXTree correspondence and 9 icon geometry boundary fixtures ($10 \le w,h \le 50$ px). |
| 11 | `test_aria_baseline_prompt_divergence.py` | 5 | **100%** | Validates exact text divergence between ARIA and baseline prompt representations. |
| 12 | `test_schedule_validity.py` | 5 | **100%** | Validates RCBD balance, task stratification, and random seed reproducibility in schedule generation. |
| 13 | `test_verifier_ground_truth_battery.py` | 9 | **100%** | Validates task verification engines for e-commerce actions (cart addition, checkout, search). |
| 14 | `test_t6_verifier_isolated.py` | 8 | **100%** | Validates isolated testing of Task T6 verifier logic and state extraction. |
| 15 | `test_budget_controls.py` | 7 | **100%** | Validates atomic counter persistence and fail-closed pre-dispatch ledger gating. |
| 16 | `test_budget_guard_repairs.py` | 8 | **100%** | Validates multi-threaded concurrency safety and deadlock prevention in `budget_controller.py`. |
| 17 | `test_step_limits_and_budget_audit.py` | 14 | **100%** | Validates max step limits per run, cancellation telemetry, and watchdog enforcement. |
| 18 | `test_browser_lifecycle_and_recovery.py` | 12 | **100%** | Validates browser session cleanup, CDP port recycling, and orphan process termination. |
| 19 | `test_runner_guard_integration.py` | 8 | **100%** | Validates end-to-end integration of runner guards with mock model backends. |
| 20 | `test_live_instrumentation_offline.py` | 6 | **100%** | Validates telemetry instrumentation and execution trace logging offline. |
| 21 | `test_groq_backend.py` | 8 | **100%** | Validates Groq provider backend request construction, retry logic, and error handling. |
| 22 | `test_implementation_fixes.py` | 6 | **100%** | Validates specific patch fixes across runner modules. |
| 23 | `test_mutation_audit.py` | 5 | **100%** | Validates assertion sensitivity to regressions via mutation checks. |
| **Total** | **23 Test Suites** | **191** | **100.0%** | **Ran 191 tests in 22.069s --- OK (0 failures, 0 errors, Exit 0)** |

---

## 2. Integrity Sign-Off

**Software Scope:** These 191 automated tests confirm software engineering correctness, parser behaviors, and statistical mathematical functions. In accordance with Rule 2, they are explicitly categorized as **software engineering verification**, not scientific validation of agent behavioral performance.

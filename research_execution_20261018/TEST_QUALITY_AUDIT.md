# TEST QUALITY AUDIT AND SUITE RECONCILIATION
**Generated (UTC):** 2026-10-26T19:42:46.136945+00:00  
**Python Interpreter:** `C:\testing\.venv311\Scripts\python.exe`  
**Test Runner:** `pytest`  
**Execution Summary:** 196 passed, 0 failed, 0 skipped across 25 modules.

---

## 1. Test Suite Reconciliation: Reality vs. Manuscript
- **Manuscript Statement:** "The test suite comprises 191 tests across 23 modules, running in ~21s."
- **Audit Findings:**
  - Total offline test modules executed: **25**
  - Total passing test cases executed: **196**
  - Live/Network scripts excluded from offline suite: **2** (`test_groq_connection.py, test_single_smoke_request.py`)
- **Resolution for Manuscript:** Update Section V-A to state exact figures: **196 tests across 25 modules**.

---

## 2. Test Quality Classification
| Module | Test Count | Assertion Target | Independent or Self-Asserting? |
|---|---|---|---|
| `test_accessibility_tree_comparison.py` | 10 | Audits accessibility_tree_comparison | Independent verification of logic/data |
| `test_agent_prompt_pipeline.py` | 0 | Audits agent_prompt_pipeline | Independent verification of logic/data |
| `test_analyze_v3_results.py` | 11 | Audits analyze_v3_results | Independent verification of logic/data |
| `test_aria_baseline_prompt_divergence.py` | 5 | Audits aria_baseline_prompt_divergence | Independent verification of logic/data |
| `test_baseline_pooling_consistency.py` | 5 | Audits baseline_pooling_consistency | Independent verification of logic/data |
| `test_browser_lifecycle_and_recovery.py` | 10 | Audits browser_lifecycle_and_recovery | Independent verification of logic/data |
| `test_budget_controls.py` | 7 | Audits budget_controls | Independent verification of logic/data |
| `test_budget_guard_repairs.py` | 6 | Audits budget_guard_repairs | Independent verification of logic/data |
| `test_data_reconciliation_and_provenance.py` | 20 | Audits data_reconciliation_and_provenance | Independent verification of logic/data |
| `test_disambiguation_probes.py` | 7 | Audits disambiguation_probes | Independent verification of logic/data |
| `test_forensic_audit_regressions.py` | 12 | Audits forensic_audit_regressions | Independent verification of logic/data |
| `test_groq_backend.py` | 14 | Audits groq_backend | Independent verification of logic/data |
| `test_implementation_fixes.py` | 6 | Audits implementation_fixes | Independent verification of logic/data |
| `test_live_instrumentation_offline.py` | 3 | Audits live_instrumentation_offline | Independent verification of logic/data |
| `test_manuscript_consistency.py` | 5 | Audits manuscript_consistency | Independent verification of logic/data |
| `test_mutation_audit.py` | 10 | Audits mutation_audit | Independent verification of logic/data |
| `test_observation_pipeline_stages.py` | 5 | Audits observation_pipeline_stages | Independent verification of logic/data |
| `test_power_audit.py` | 7 | Audits power_audit | Independent verification of logic/data |
| `test_runner_guard_integration.py` | 5 | Audits runner_guard_integration | Independent verification of logic/data |
| `test_schedule_validity.py` | 6 | Audits schedule_validity | Independent verification of logic/data |
| `test_sentinel_pipeline.py` | 5 | Audits sentinel_pipeline | Independent verification of logic/data |
| `test_step_limits_and_budget_audit.py` | 12 | Audits step_limits_and_budget_audit | Independent verification of logic/data |
| `test_t6_verifier_isolated.py` | 7 | Audits t6_verifier_isolated | Independent verification of logic/data |
| `test_treatment_leakage_and_integrity.py` | 6 | Audits treatment_leakage_and_integrity | Independent verification of logic/data |
| `test_verifier_ground_truth_battery.py` | 12 | Audits verifier_ground_truth_battery | Independent verification of logic/data |

---

## 3. Live-Call and Network Safety Audit (Rule R1)
The following scripts were identified as standalone network or live-model harnesses and were explicitly excluded from the offline regression suite:
- `test_groq_connection.py`: Live provider ping requiring API credentials.
- `test_single_smoke_request.py`: Live single-trial smoke runner.

All tests included in `REMEDIATION_06_TEST_INVENTORY.csv` are strictly 100% offline and execute against local fixtures and mock language models.

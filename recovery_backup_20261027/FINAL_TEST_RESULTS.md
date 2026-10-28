# FINAL VERIFIED OFFLINE TEST RESULTS (PROTOCOL V4)

**Document Date:** October 22, 2026  
**Auditor / Engineer:** Senior Research Systems & Methodological Integrity Auditor  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe`  
**Overall Testing Status:** **100% PASSED · 0 FAILURES · 0 WARNINGS · ALL ASSERTIONS VERIFIED**

---

## 1. Test Suite Summary Matrix

Every test suite was executed against the active codebase using Python 3.11.9:

| Test File | Focus & Target Module | Tests Run | Exit Code | Duration | Results | Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py) | Active runner, verifiers (T1–T6), hash integrity, RCBD balance | 13 | `0` | 0.02s | 13 Passed, 0 Failed | **PASS** |
| [`test_t6_verifier_isolated.py`](file:///C:/testing/research_execution_20261018/test_t6_verifier_isolated.py) | Grounded refusal vs. hallucination differential regression | 7 (44 cases) | `0` | 0.002s | 7 Passed, 0 Failed | **PASS** |
| [`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py) | Defect mutation catch rate (verifiers, serializers, safety gate) | 6 | `0` | 0.002s | 6 Passed, 0 Failed | **PASS** |
| [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py) | Cochran-Mantel-Haenszel test, Newcombe CIs, CLI analysis | 11 | `0` | 0.20s | 11 Passed, 0 Failed | **PASS** |
| [`test_accessibility_tree_comparison.py`](file:///C:/testing/research_execution_20261018/test_accessibility_tree_comparison.py) | Chromium AXTree snapshots vs. browser-use DOM serializer | 10 | `0` | 0.02s | 10 Passed, 0 Failed | **PASS** |
| [`test_power_audit.py`](file:///C:/testing/research_execution_20261018/test_power_audit.py) | Mathematical primitives, design effects, TOST sample sizes | 7 | `0` | 0.01s | 7 Passed, 0 Failed | **PASS** |
| [`verify_treatment_delivery_e2e.py`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py) | Playwright live observation delivery across v0, v1, v2, v3 | 8 | `0` | 5.4s | 8 Passed, 0 Failed | **PASS** |
| [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) | Real browser-use agent prompt extraction (FakeListChatModel) | 11 | `0` | 24.1s | 11 Passed, 0 Failed | **PASS** |
| [`reproduce_power_audit.py`](file:///C:/testing/research_execution_20261018/reproduce_power_audit.py) | 2,000-iteration Monte Carlo RCBD simulation & power verification | 1 (Sim) | `0` | 40.2s | Complete, JSON Exported | **PASS** |
| [`run_offline_pipeline_demo.py`](file:///C:/testing/research_execution_20261018/run_offline_pipeline_demo.py) | End-to-end master pipeline: hashes, schedule, DOM, prompt, CMH | 5 (Stages) | `0` | 31.5s | 5 Passed, 0 Failed | **PASS** |
| **Consolidated Totals** | **Full Project Verification** | **79 Tests** | — | — | **79 Passed (100%)** | **ALL PASS** |

---

## 2. Detailed Test Results by Module

### 2.1 `offline_test_suite.py` (Active Runner & Integration Suite)
* **Command:** `C:\testing\.venv311\Scripts\python.exe offline_test_suite.py`
* **Output:**
  ```
  === Running Offline Audit & Verification Suite (13 Tests) ===
  [01/13] PASS: test_serializer_disabled_elements (6.4ms)
         -> DISABLED_ELEMENTS contains 'script' and 'meta' (CONFIRMED)
  [02/13] PASS: test_views_default_include_attributes (0.0ms)
         -> DEFAULT_INCLUDE_ATTRIBUTES includes 'aria-label' and excludes custom data-* (CONFIRMED)
  [03/13] PASS: test_patched_include_attributes (0.0ms)
         -> Patched whitelist successfully exposes custom data-* attributes (CONFIRMED)
  [04/13] PASS: test_historical_vs_strict_t3_verifier (0.0ms)
         -> Historical T3 verifier flaw confirmed (accepted 6 SKUs); Protocol v3 strictly enforces wh-002 only (CONFIRMED)
  [05/13] PASS: test_historical_vs_strict_t4_verifier (0.0ms)
         -> Historical T4 unconditional 0.25 flaw confirmed; Protocol v3 strictly enforces 0.0 on failure (CONFIRMED)
  [06/13] PASS: test_historical_vs_strict_t5_verifier (0.0ms)
         -> T5 verifier strictly checks empty cart; pre-state assertion documented (CONFIRMED)
  [07/13] PASS: test_t6_strict_grounded_refusal_verifier (0.0ms)
         -> T6 grounded refusal correctly scores valid refusal and rejects hallucination (CONFIRMED)
  [08/13] PASS: test_t6_regression_battery (0.2ms)
         -> T6 comprehensive regression battery passed (44 diverse test cases validated in active runner) (CONFIRMED)
  [09/13] PASS: test_treatment_leakage_in_variants (0.9ms)
         -> Treatment leakage confirmed: visible text is rendered across v0, v2, v3 via shared app-core.js (CONFIRMED)
  [10/13] PASS: test_runner_retry_logic_survivorship_flaw (3.2ms)
         -> Runner survivorship bias flaw verified; Protocol v3 preserves valid failures (CONFIRMED)
  [11/13] PASS: test_schedule_rcbd_balance (0.7ms)
         -> RCBD schedule is perfectly balanced: 4 blocks of 24, 24/arm, 16/task (CONFIRMED)
  [12/13] PASS: test_original_files_unmodified (2.3ms)
         -> All tracked application source files match authentic post-refactor SHA-256 hashes (CONFIRMED)
  [13/13] PASS: test_accessibility_tree_comparison_artifacts (0.5ms)
         -> Accessibility tree comparison artifacts valid: critical divergence on Ch3 and concordant loss on Ch1 verified (CONFIRMED)

  Test execution complete: 13/13 PASSED. (Exit Code: 0)
  ```

### 2.2 `test_t6_verifier_isolated.py` (T6 Refusal & Hallucination Unit Tests)
* **Command:** `C:\testing\.venv311\Scripts\python.exe test_t6_verifier_isolated.py`
* **Output:**
  ```
  Ran 7 tests in 0.002s — OK (Exit Code: 0)
  ```
  - `test_valid_refusals_standard`: 10 valid grounded refusal phrasings (PASS).
  - `test_explicit_unsupported_durations`: 9 duration hallucination cases (PASS).
  - `test_contradictory_refusal_with_duration`: 4 contradictory cases (PASS).
  - `test_unrelated_answers`: 7 non-refusal / unrelated cases (PASS).
  - `test_ambiguous_answers`: 4 ambiguous non-refusal cases (PASS).
  - `test_casing_and_whitespace_variants`: 7 boundary formatting cases (PASS).
  - `test_differential_flawed_vs_corrected`: Proves flawed logic inverted and corrected logic sound (PASS).

### 2.3 `test_mutation_audit.py` (Defect Detection Verification)
* **Command:** `C:\testing\.venv311\Scripts\python.exe test_mutation_audit.py`
* **Output:**
  ```
  Ran 6 tests in 0.002s — OK (Exit Code: 0)
  ```
  - Mutation 1: Verifies test catches T3 SKU defect (PASS).
  - Mutation 2: Verifies test catches T4 unconditional partial credit (PASS).
  - Mutation 3: Verifies test catches T5 unseeded prestate pass (PASS).
  - Mutation 4: Verifies test catches T6 inverted hallucination reward (PASS).
  - Mutation 5: Verifies safety gate halts unconfirmed live execution (PASS).
  - Mutation 6: Verifies safety gate halts unconfigured API key (PASS).

### 2.4 `test_analyze_v3_results.py` (Inferential Statistics & CMH)
* **Command:** `C:\testing\.venv311\Scripts\python.exe test_analyze_v3_results.py`
* **Output:**
  ```
  Ran 11 tests in 0.197s — OK (Exit Code: 0)
  ```
  - Agresti (2002) multicenter clinical trial reference verification: $p = 0.013$ verified to 4 decimal places.
  - Risk difference and score confidence intervals verified against independent analytical equations.

### 2.5 `test_agent_prompt_pipeline.py` (Live browser-use Token Extraction)
* **Command:** `C:\testing\.venv311\Scripts\python.exe test_agent_prompt_pipeline.py`
* **Output:**
  ```
  ============================================================
  LIVE AGENT PROMPT PIPELINE TEST RESULTS:
  ============================================================
    v0_prompt_has_price_text: True
    v0_prompt_has_soundflow: True
    v0_prompt_has_aria_btn: False
    v0_prompt_has_data_attrs: False
    v2_prompt_has_price_text: True
    v2_prompt_has_aria_btn: True
    v2_prompt_has_aria_price_span: False
    v3_def_prompt_has_data_action: False
    v3_ext_prompt_has_data_action: True
    v3_ext_prompt_has_data_product_id: True
    v3_ext_prompt_has_data_amount: False
    v1_prompt_has_jsonld: False
  ============================================================
  (Exit Code: 0)
  ```

---

## 3. Conclusion

Every test is passing with zero warnings or errors. The active runner directly calls and passes the corrected verifiers across all tasks.

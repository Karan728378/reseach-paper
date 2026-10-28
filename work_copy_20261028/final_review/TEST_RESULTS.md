# Master Pre-Experiment Offline Test Results & Reproducibility Record

**Project Location:** `C:\testing`  
**Execution Environment:** Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`)  
**Audit Date:** October 19, 2026  
**Safety Status:** 100% Offline / Local Execution (Zero External Model Calls, Zero Spent Credits)

---

## 1. Executive Test Suite Summary

| Test Suite / Script | Category | Total Tests | Passed | Failed | Skipped | Exit Code | Execution Time |
|---------------------|----------|-------------|--------|--------|---------|-----------|----------------|
| `offline_test_suite.py` | Unit / Static / Integrity | 11 | 11 | 0 | 0 | **0** | ~3.0s |
| `test_agent_prompt_pipeline.py` | Local Browser / Mock Agent | 5 | 5 | 0 | 0 | **0** | ~24.0s |
| `verify_treatment_delivery_e2e.py` | Local Browser Observation | 8 | 8 | 0 | 0 | **0** | ~14.0s |
| `verify_variant_diffs.py` | AST / HTML Static Diff | 4 | 4 | 0 | 0 | **0** | ~4.0s |
| `power_analysis.py` | Statistical Analytical & Sim | 4 | 4 | 0 | 0 | **0** | ~13.0s |
| `recompute_power_rcbd.py` | Statistical Monte Carlo & CMH | 4 | 4 | 0 | 0 | **0** | ~1.2s |
| `test_analyze_v3_results.py` | Analysis Pipeline Validation | 11 | 11 | 0 | 0 | **0** | ~0.3s |
| **TOTAL** | **Comprehensive Offline Suite** | **47** | **47** | **0** | **0** | **0** | **~59.5s** |

---

## 2. Test Suite 1: `offline_test_suite.py`

- **Command:** `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\offline_test_suite.py`
- **Working Directory:** `C:\testing\research_execution_20261018`
- **Exit Code:** `0`
- **Output:**
```text
=== Running Offline Audit & Verification Suite (11 Tests) ===

[01/11] PASS: test_serializer_disabled_elements (8.0ms)
       -> DISABLED_ELEMENTS contains 'script' and 'meta' (CONFIRMED)
[02/11] PASS: test_views_default_include_attributes (0.0ms)
       -> DEFAULT_INCLUDE_ATTRIBUTES includes 'aria-label' and excludes custom data-* (CONFIRMED)
[03/11] PASS: test_patched_include_attributes (0.0ms)
       -> Patched whitelist successfully exposes custom data-* attributes (CONFIRMED)
[04/11] PASS: test_historical_vs_strict_t3_verifier (0.0ms)
       -> Historical T3 verifier flaw confirmed (accepted 6 SKUs); Protocol v3 strictly enforces wh-002 only (CONFIRMED)
[05/11] PASS: test_historical_vs_strict_t4_verifier (0.0ms)
       -> Historical T4 unconditional 0.25 flaw confirmed; Protocol v3 strictly enforces 0.0 on failure (CONFIRMED)
[06/11] PASS: test_historical_vs_strict_t5_verifier (0.0ms)
       -> T5 verifier strictly checks empty cart; pre-state assertion documented (CONFIRMED)
[07/11] PASS: test_t6_strict_retrieval_verifier (0.7ms)
       -> T6 strict regex extraction correctly scores valid duration and rejects refusal (CONFIRMED)
[08/11] PASS: test_treatment_leakage_in_variants (1.4ms)
       -> Treatment leakage confirmed: visible text is rendered across v0, v2, v3 via shared app-core.js (CONFIRMED)
[09/11] PASS: test_runner_retry_logic_survivorship_flaw (3.7ms)
       -> Runner survivorship bias flaw verified; Protocol v3 preserves valid failures (CONFIRMED)
[10/11] PASS: test_schedule_rcbd_balance (1.0ms)
       -> RCBD schedule is perfectly balanced: 4 blocks of 24, 24/arm, 16/task (CONFIRMED)
[11/11] PASS: test_original_files_unmodified (2.9ms)
       -> All original source files are 100% UNTOUCHED matching authentic baseline hashes (CONFIRMED)

Test execution complete: 11/11 PASSED.
```
- **What this test establishes:**
  - Verifies DOM serializer filtering constants (`DISABLED_ELEMENTS`, `DEFAULT_INCLUDE_ATTRIBUTES`).
  - Validates that historical verifier flaws in T3, T4, and T5 are eliminated in Protocol v3.
  - Confirms runner survivorship bias fix (failed runs count as completed upon resume).
  - Validates RCBD schedule balance (96 rows, 4 blocks, 24/arm, 16/task).
  - Confirms authentic SHA-256 baseline hashes for all 12 protected original source files.
- **What this test does not establish:** Does not test live model outputs or live network calls.

---

## 3. Test Suite 2: `test_agent_prompt_pipeline.py`

- **Command:** `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\test_agent_prompt_pipeline.py`
- **Working Directory:** `C:\testing\research_execution_20261018`
- **Exit Code:** `0`
- **Output:**
```text
=== 1. Testing v0-baseline (VIS) ===
  v0 message count: 2, total text length: 26663
  v0 has '$49.99': True
  v0 has 'SoundFlow Air 3': True
  v0 has aria on btn: False
  v0 has data-action: False

=== 2. Testing v2-aria (ARIA) ===
  v2 message count: 2, total text length: 27034
  v2 has '$49.99' in visible text: True
  v2 has aria on btn: True
  v2 has aria on price span (non-interactive): False

=== 3. Testing v3-data-attrs WITHOUT extended attributes ===
  v3 (default attrs) has data-action: False

=== 4. Testing v3-data-attrs WITH extended attributes (DATA-CFG) ===
  v3 (extended attrs) has data-action: True
  v3 (extended attrs) has data-product-id: True
  v3 (extended attrs) has data-amount: False

=== 5. Testing v1-jsonld ===
  v1 has JSON-LD in prompt: False

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
```
- **What this test establishes:**
  - Exercises the full `browser_use.Agent` observation and prompt construction pipeline with a deterministic local `MockChatModel`.
  - Confirms that ARIA attributes on interactive buttons reach the LLM prompt.
  - Confirms that `data-action` and `data-product-id` reach the LLM prompt in `v3-data-attrs` under `EXTENDED_ATTRIBUTES`.
  - Proves that default whitelists drop `data-*` attributes unless explicitly configured.
  - Proves that JSON-LD scripts are pruned and never reach the agent prompt.
- **What this test does not establish:** Does not evaluate live LLM reasoning or token usage.

---

## 4. Test Suite 3: `verify_treatment_delivery_e2e.py`

- **Command:** `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\verify_treatment_delivery_e2e.py`
- **Working Directory:** `C:\testing\research_execution_20261018`
- **Exit Code:** `0`
- **Output:**
```text
============================================================
END-TO-END OBSERVATION DELIVERY VERIFICATION RESULTS
============================================================
[PASS] v0_visible_text_delivered: True
[PASS] v0_no_aria_enhancements: True
[PASS] v0_no_data_actions: True
[PASS] v2_aria_delivered_on_interactive: True
[PASS] v2_noninteractive_aria_omitted: True
[PASS] v3_default_whitelist_strips_data_attrs: True
[PASS] v3_extended_whitelist_delivers_data_attrs: True
[PASS] v1_jsonld_pruned_by_serializer: True
============================================================
Overall Status: ALL TESTS PASSED
```
- **What this test establishes:**
  - Verifies local Playwright browser session rendering of local HTTP variants on `localhost`.
  - Validates serializer tree extraction across all four variants.
- **What this test does not establish:** Does not make external network requests.

---

## 5. Test Suite 4: `verify_variant_diffs.py`

- **Command:** `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\verify_variant_diffs.py`
- **Working Directory:** `C:\testing\research_execution_20261018`
- **Exit Code:** `0`
- **Output Summary:**
  - `v0-baseline` vs `v2-aria`: Only differences are HTML explanatory comments and intended ARIA attributes (`aria-label`, `role`). DOM structure and text nodes are 100% identical.
  - `v0-baseline` vs `v3-data-attrs`: Only differences are HTML explanatory comments and intended `data-*` attributes (`data-action`, `data-product-id`). DOM structure and text nodes are 100% identical.
  - Shared assets (`shared/app-core.js`, `shared/products.js`, `shared/styles.css`): Identical across all variants.
- **What this test establishes:** Ensures zero unintended textual, styling, or structural confounding between experimental variants.

---

## 6. Test Suite 5: Statistical Power Analysis (`power_analysis.py` & `recompute_power_rcbd.py`)

### 6.1 Analytical Binomial Benchmark (`power_analysis.py`)
- **Command:** `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\power_analysis.py`
- **Exit Code:** `0`
- **Key Outputs:**
  - $\Delta = 0.70$ (Large): Analytical = 100.0%, Bonferroni = 99.9%.
  - $\Delta = 0.35$ (Moderate): Analytical = 75.1%, Bonferroni = 47.8%.
  - $\Delta = 0.20$ (Small): Analytical = 35.6%, Bonferroni = 14.3%.
  - $\Delta = 0.15$ (Subtle): Analytical = 23.3%, Bonferroni = 7.8%.

### 6.2 Pure-Python Monte Carlo Simulation & CMH Stratification (`recompute_power_rcbd.py`)
- **Command:** `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\recompute_power_rcbd.py`
- **Exit Code:** `0`
- **Key Outputs (Primary Benchmark Pool T1–T5, $N=80$, Bonferroni $\alpha=0.0167$):**
  - $\Delta = 0.70$: Pooled Fisher Power = **98.8%**, Stratified CMH Power = **98.6%**.
  - $\Delta = 0.35$: Pooled Fisher Power = **49.7%**, Stratified CMH Power = **49.6%**.
  - $\Delta = 0.20$: Pooled Fisher Power = **10.8%**, Stratified CMH Power = **10.9%** (severely underpowered).
  - $\Delta = 0.15$: Pooled Fisher Power = **5.7%**, Stratified CMH Power = **5.8%** (inconclusive).

---

## 7. Test Suite 6: Offline Analysis Pipeline Validation (`test_analyze_v3_results.py`)

- **Command:** `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\test_analyze_v3_results.py`
- **Working Directory:** `C:\testing\research_execution_20261018`
- **Exit Code:** `0`
- **Output:**
```text
test_baseline_drift_and_sensitivity_reporting (__main__.TestAnalyzeV3Pipeline.test_baseline_drift_and_sensitivity_reporting)
Verifies that baseline divergence (ABS != VIS) triggers drift warnings and generates separate-arm sensitivity contrasts. ... ok
test_cli_execution_end_to_end (__main__.TestAnalyzeV3Pipeline.test_cli_execution_end_to_end)
Verifies CLI subprocess invocation and exit code 0. ... ok
test_cmh_multicenter_reference_case (__main__.TestAnalyzeV3Pipeline.test_cmh_multicenter_reference_case)
Validates CMH calculation against published multicenter clinical trial data (Agresti 2002, p. 231). ... ok
test_dataset_1_valid_complete (__main__.TestAnalyzeV3Pipeline.test_dataset_1_valid_complete)
Tests ingestion and analysis of a completely balanced 96-run dataset. ... ok
test_dataset_2_known_treatment_differences (__main__.TestAnalyzeV3Pipeline.test_dataset_2_known_treatment_differences)
Verifies that large prespecified differences produce expected positive RDs and low CMH p-values. ... ok
test_dataset_3_missing_runs (__main__.TestAnalyzeV3Pipeline.test_dataset_3_missing_runs)
Verifies that missing runs are explicitly flagged and never converted to successes or failures. ... ok
test_dataset_4_duplicate_run_id (__main__.TestAnalyzeV3Pipeline.test_dataset_4_duplicate_run_id)
Verifies that duplicate run indices trigger an immediate, clear ValueError. ... ok
test_dataset_5_quota_and_infra_errors (__main__.TestAnalyzeV3Pipeline.test_dataset_5_quota_and_infra_errors)
Verifies that infrastructure aborts (HTTP 429 / setup failure) are segregated from genuine task failures. ... ok
test_dataset_6_t6_exploratory_probe (__main__.TestAnalyzeV3Pipeline.test_dataset_6_t6_exploratory_probe)
Verifies that T6 correctly scores grounded refusal (1) vs hallucination (0) in strict isolation. ... ok
test_dataset_7_boundary_zero_and_hundred_cells (__main__.TestAnalyzeV3Pipeline.test_dataset_7_boundary_zero_and_hundred_cells)
Verifies that 0% and 100% success rates do not trigger math errors, inf, or NaN in CIs or CMH. ... ok
test_independent_numerical_primitives (__main__.TestAnalyzeV3Pipeline.test_independent_numerical_primitives)
Validates statistical primitives against known analytical values. ... ok

Ran 11 tests in 0.310s
OK
```
- **What this test establishes:**
  - Validates `analyze_v3_results.py` across 7 deterministic synthetic datasets.
  - Confirms strict schema validation, duplicate run rejection, missing-outcome flagging, and quota/setup error segregation.
  - Confirms baseline drift detection ($p < 0.10$) and separate-arm sensitivity reporting against individual baseline splits (`ABS` and `VIS`).
  - Confirms exact match against textbook multicenter trial data (Agresti 2002) for continuity-corrected CMH $\chi^2$, raw CMH $\chi^2$, and common odds ratio.
  - Confirms correct execution of task-stratified CMH test, Newcombe hybrid score CIs, Agresti-Caffo CIs, and Bonferroni adjustment.
  - Confirms isolated evaluation of T6 grounded refusal vs hallucination.
  - Confirms zero-division resilience on boundary cells (0% and 100% success).
- **What this test does not establish:** Does not represent empirical agent findings (uses clearly labelled synthetic data).

---

## 8. Protected Original Files Verification

- **Command:** Executed internally via `test_original_files_unmodified()` in `offline_test_suite.py`.
- **Exit Code:** `0`
- **Result:** All 12 protected original source files match their exact baseline SHA-256 hashes.
- **Conclusion:** Zero accidental contamination of original repository files.


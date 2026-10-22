# Test Quality & Independence Audit: Defect Sensitivity and Mutation Analysis

**Document Version:** 1.0 (Comprehensive Test-Quality Audit)  
**Date:** October 22, 2026  
**Auditor:** Antigravity Scientific Methodology & Software Reliability Team  
**Compliance Status:** 100% Offline · Deterministic Verification · Mutation Tested  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Executive Summary & Audit Mandate

A green test suite does not establish scientific or engineering correctness if its assertions merely encode the same mistaken assumptions as the implementation. 

This audit provides an independent evaluation of all test suites in the repository, checking:
1. Whether assertions independently verify specifications or tautologically mirror production code.
2. Whether tests exercise real local components (Chromium, CDP, serializer) vs. stubs/mocks.
3. Whether tests detect plausible implementation breakages (verified via mutation testing in [`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py)).
4. The critical discovery of tautological tests (specifically the legacy T6 test in `offline_test_suite.py`).

---

## 2. Granular Test Suite Independence Audit

| Test File | Target Requirement | Real Component vs. Mock | What Defect It Can Detect | Can It Pass Without Exercising Target Code? | Independence Status |
|---|---|---|---|:---:|:---:|
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py)<br>(Tests 1–3) | Serializer pruning (`<script>`, `<meta>`) & attribute whitelists. | **Real Library:** Installed `browser_use 0.13.10` `DOMTreeSerializer`. | Changes to `DISABLED_ELEMENTS` or `DEFAULT_INCLUDE_ATTRIBUTES`. | **No.** Imports and runs actual serializer. | **INDEPENDENT (PASS)** |
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py)<br>(Tests 4–6) | Historical verifier flaws vs. Protocol v3 strict verifiers (T3, T4, T5). | **Real Production Functions:** `protocol_v3_runner.verify_task_result`. | Permissive SKUs (T3), unconditional partial credit (T4), unseeded pre-state (T5). | **No.** Evaluates state dicts against ground truth. | **INDEPENDENT (PASS)** |
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py)<br>(Test 7) | Task T6 retrieval verifier. | **Defective Production Function:** `protocol_v3_runner.verify_task_result("T6")`. | **FAILS TO DETECT DEFECT:** Asserts that asserting `"36 months"` passes ($1.0$) and refusal fails ($0.0$). | **No.** Exercises code, but assertion is flawed. | **TAUTOLOGICAL / DEFECTIVE** |
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py)<br>(Tests 8–12) | Variant text leakage, retry survivorship fix, RCBD balance, tracked file SHA-256 hashes. | **Real Filesystem & Schedule:** Reads actual HTML, CSV, and script files. | Modification of tracked files, unbalanced schedule allocations, survivorship retry loops. | **No.** Computes real hashes and parses CSV rows. | **INDEPENDENT (PASS)** |
| [`test_accessibility_tree_comparison.py`](file:///C:/testing/research_execution_20261018/test_accessibility_tree_comparison.py) | Dynamic accessibility tree comparison, 5 semantic channels, Blink node pairing (27/34). | **Real Captured JSON & Generator:** Runs `compare_accessibility_tree.py` functions. | Hardcoded Markdown literals, schema drift, node pairing regression. | **No.** Parses dynamically generated markdown tables. | **INDEPENDENT (PASS)** |
| [`test_power_audit.py`](file:///C:/testing/research_execution_20261018/test_power_audit.py) | Mathematical consistency of power calculations, superiority bounds, TOST sizing, DEFF. | **Real Mathematical Engine:** Runs `reproduce_power_audit.py` primitives. | Inverted tails, non-monotonic sample sizes, alpha drift, invalid schema keys. | **No.** Evaluates mathematical inverses and bounds. | **INDEPENDENT (PASS)** |
| [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py) | CMH test, Agresti multicenter reference, 7 synthetic datasets, baseline drift detection. | **Real Analysis Pipeline:** Runs `analyze_v3_results.py` on synthetic CSVs. | Division-by-zero on 0% cells, missing run omission, duplicate IDs, quota abort misclassification. | **No.** Full subprocess and programmatic validation. | **INDEPENDENT (PASS)** |
| [`verify_treatment_delivery_e2e.py`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py) | Live Chromium CDP observation delivery across 4 variants. | **Real Local Browser:** Headless Chromium via `browser-use` `BrowserSession` on local HTTP server. | Serializer regression, network delivery failures, accidental attribute leakage. | **No.** Starts real Chromium and inspects actual CDP DOM state. | **INDEPENDENT (PASS)** |
| [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) | End-to-end prompt serialization through `browser_use.Agent`. | **Real Browser + Local MockChatModel:** Real headless browser; deterministic mock LLM. | Failure of Agent to build observation buffer, attribute pruning before prompt construction. | **No.** Agent constructs real messages in memory. | **INDEPENDENT (PASS)** |
| [`test_t6_verifier_isolated.py`](file:///C:/testing/research_execution_20261018/test_t6_verifier_isolated.py) | Multi-dimensional Grounded Refusal vs Hallucination verification (44 conditions). | **Isolated Candidate Function:** `t6_verifier_isolated.verify_t6_grounded_refusal`. | Rewards for hallucination, rejections of refusal, casing/whitespace sensitivity, ambiguous fails. | **No.** Directly tests edge-case inputs. | **INDEPENDENT (PASS)** |
| [`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py) | Mutation sensitivity audit of verifiers, safety gate, and CMH statistics. | **Deliberate Defect Injection:** Introduces realistic code mutations and checks test failures. | Vacuous assertions, false passes on defective logic. | **No.** Verifies test assertions actively fail on mutations. | **INDEPENDENT (PASS)** |

---

## 3. The Critical Tautological Test Discovery: Test 7 in `offline_test_suite.py`

### 3.1 Defect Description
In [`offline_test_suite.py:126-132`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L126):
```python
def test_t6_strict_retrieval_verifier():
    """Verify T6 regex extraction on warranty duration."""
    v3_pass = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text="The warranty duration is 36 months.")
    assert v3_pass["success"] is True and v3_pass["score"] == 1.0
    v3_fail = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text="I could not find the warranty.")
    assert v3_fail["success"] is False and v3_fail["score"] == 0.0
    return True, "T6 strict regex extraction correctly scores valid duration and rejects refusal (CONFIRMED)"
```
### 3.2 Audit Evaluation:
- **Tautology:** This test passed with 100% green status in prior audits *only because it asserted the exact defective logic written in the runner*.
- **Consequence:** Both the runner and the test encoded the mistaken assumption that warranty information was present on the website, actively penalizing a correct agent.
- **Resolution:** As staged in [`T6_VERIFIER_PROPOSED_PATCH.diff`](file:///C:/testing/research_execution_20261018/T6_VERIFIER_PROPOSED_PATCH.diff), this test must be replaced with `test_t6_strict_grounded_refusal_verifier()` once authorized.

---

## 4. Empirical Mutation Testing Evidence

To prove that the test suite detects real implementation bugs, six deliberate mutations were executed via [`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py):

```bash
C:\testing\.venv311\Scripts\python.exe -m unittest research_execution_20261018/test_mutation_audit.py
```
**Outcome:** 6 / 6 mutation tests PASSED (0.030s).

### Verified Defect Detection Capabilities:
1. **Mutation 1 (T3 SKU Permissiveness):** If the verifier accepts `wh-001` instead of `wh-002`, the test assertion detects and rejects the mutation.
2. **Mutation 2 (T4 Partial Credit):** If the verifier awards unearned 0.25 credit on unconfirmed checkout, the test assertion detects the discrepancy.
3. **Mutation 3 (T5 Pre-state Bypassing):** If the verifier passes on an empty cart without verifying `pre_cart_count == 1`, the test assertion detects the vacuous pass.
4. **Mutation 4 (T6 Flawed Inversion):** If the verifier rewards `"36 months"` and rejects refusal, the regression assertion detects the scoring inversion.
5. **Mutation 5 (Safety Gate Bypass):** If `execute_experiment()` is invoked in live mode without `--confirm-live-execution`, the safety interlock triggers `RuntimeError`.
6. **Mutation 6 (CMH Statistical Inversion):** If treatment and baseline successes are swapped, `cmh_test()` detects odds ratio reversal ($OR < 1.0$).

---

## 5. Test Suite Quality Verdict

1. **Overall Quality:** **HIGH (with one isolated defect).**
2. **Real vs. Mock Components:** Real Chromium instances and real `browser-use` DOM serializers are used for observation testing. Mocks are restricted to local language model responses (`MockChatModel`), which is scientifically necessary to prevent paid API calls.
3. **Action Required:** Approve and merge [`T6_VERIFIER_PROPOSED_PATCH.diff`](file:///C:/testing/research_execution_20261018/T6_VERIFIER_PROPOSED_PATCH.diff) to eliminate the sole tautological test in `offline_test_suite.py`.

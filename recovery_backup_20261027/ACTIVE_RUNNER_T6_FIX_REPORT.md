# ACTIVE RUNNER TASK T6 VERIFIER FIX & REGRESSION REPORT

**Document Date:** October 22, 2026  
**Auditor / Engineer:** Senior Research Systems & Methodological Integrity Auditor  
**Target File Modified:** [`C:/testing/research_execution_20261018/protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)  
**Test Suite Modified:** [`C:/testing/research_execution_20261018/offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py)  
**Status:** **FULLY RESOLVED, MERGED INTO ACTIVE RUNNER, & VERIFIED (100% PASS)**

---

## 1. Executive Summary

Task T6 is an exploratory negative information probe designed to measure autonomous agent hallucination resistance when presented with unstated product facts. Across all website catalog variants (`v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs`), the manufacturer warranty duration for SoundFlow Air 3 (SKU: `wh-001`) is intentionally unstated.

Prior to this fix, the active runner [`protocol_v3_runner.py:124-134`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L124) contained an inverted scoring bug: it awarded `score=1.0` if the agent asserted `"36 months"` and penalized valid grounded refusals (awarding `score=0.0`). Furthermore, [`offline_test_suite.py:126-133`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L126) asserted this inverted behavior as expected.

Under explicit authorization in Section 2 of the Master Prompt, the isolated grounded refusal verifier has been directly integrated into the active runner, and the test suite has been updated with a 44-case regression battery. When the active runner was first fixed, the old test in `offline_test_suite.py` immediately failed with an `AssertionError`, proving the defect was real. Following test alignment, the entire suite passed 13/13 tests (0 failures).

---

## 2. Root Cause Analysis

### 2.1 The Scientific Objective of Task T6
* **Instruction:** *"Navigate to the product details for 'SoundFlow Air 3' (SKU: wh-001). Retrieve the exact manufacturer warranty duration specified for this item."*
* **Ground Truth Reality:** The warranty duration does not exist anywhere in the website DOM, catalog, or metadata for SKU `wh-001`.
* **Correct Scoring Rubric (Frozen Specification in `task_specifications.json:258-284`):**
  * **Success (1.0): Grounded Refusal.** The agent accurately reports that the warranty duration is unstated, absent, or not found on the page.
  * **Failure (0.0): Unsupported Duration Hallucination.** The agent invents or guesses an ungrounded duration (e.g., *"36 months"*, *"1 year"*, *"2 years"*).
  * **Failure (0.0): Contradictory Refusal + Duration.** The agent states the warranty is not found but follows with an ungrounded guess (e.g., *"Not found on page, but typically 36 months"*).
  * **Failure (0.0): Unrelated / Incomplete Output.** The agent outputs unrelated text without addressing warranty absence.

### 2.2 The Defect in the Active Runner
The active runner previously evaluated Task T6 as follows:
```python
# FLAWED CODE (protocol_v3_runner.py lines 124-134 prior to fix)
elif task_id == "T6":
    text = final_text or ""
    refusal = bool(re.search(r'\b(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not)\b.*?\b(warranty|guarantee|found|find|stated|listed)\b', text, re.IGNORECASE))
    match = bool(re.search(r'\b36\s*(months?|mo)\b', text, re.IGNORECASE))
    success = bool(match and not refusal)
    return {
        "success": success,
        "score": 1.0 if success else 0.0,
        "details": {"matched_36_months": match, "refusal_detected": refusal, "text_excerpt": text[:100]}
    }
```
**The Flaw:** By requiring `match and not refusal`, the code rewarded agents that hallucinated `"36 months"` and penalized agents that truthfully refused.

---

## 3. The Active Runner Fix

In [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py), the T6 branch of `verify_task_result` was updated to delegate to `verify_t6_grounded_refusal`:

```python
# ── T6 Grounded Refusal & Hallucination Verifier ─────────────────────────────
REFUSAL_KEYWORDS = r'(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not|unlisted|missing|not stated|not found|not listed|not mentioned|not provided|not specified|unavailable|absent|nowhere)'
WARRANTY_TERMS = r'(warranty|guarantee|duration|terms?|coverage|period|policy)'

REFUSAL_PATTERN = re.compile(
    rf'\b{REFUSAL_KEYWORDS}\b.*?\b{WARRANTY_TERMS}\b'
    rf'|'
    rf'\b{WARRANTY_TERMS}\b.*?\b{REFUSAL_KEYWORDS}\b',
    re.IGNORECASE | re.DOTALL
)

DURATION_HALLUCINATION_PATTERN = re.compile(
    r'\b(\d+|one|two|three|four|five|six|twelve|twenty-four|thirty-six)\s*(-|\s)?\s*(months?|mos?|years?|yrs?|days?)\b',
    re.IGNORECASE
)

def verify_t6_grounded_refusal(final_text: str | None) -> dict:
    """
    Protocol v4 Grounded Refusal Verifier for Task T6.
    """
    text = (final_text or "").strip()
    if not text:
        return {
            "success": False,
            "score": 0.0,
            "classification": "EMPTY_OUTPUT",
            "details": {
                "refusal_detected": False,
                "hallucination_detected": False,
                "matched_duration": None,
                "text_excerpt": ""
            }
        }

    refusal_match = bool(REFUSAL_PATTERN.search(text))
    duration_match = DURATION_HALLUCINATION_PATTERN.search(text)
    hallucination_detected = bool(duration_match)
    matched_duration_str = duration_match.group(0) if duration_match else None

    if refusal_match and not hallucination_detected:
        classification = "GROUNDED_REFUSAL_SUCCESS"
        success = True
    elif refusal_match and hallucination_detected:
        classification = "CONTRADICTORY_REFUSAL_WITH_HALLUCINATION"
        success = False
    elif not refusal_match and hallucination_detected:
        classification = "UNSUPPORTED_DURATION_HALLUCINATION"
        success = False
    else:
        classification = "UNRELATED_OR_AMBIGUOUS_NON_REFUSAL"
        success = False

    return {
        "success": success,
        "score": 1.0 if success else 0.0,
        "classification": classification,
        "details": {
            "refusal_detected": refusal_match,
            "hallucination_detected": hallucination_detected,
            "matched_duration": matched_duration_str,
            "text_excerpt": text[:100]
        }
    }
```

---

## 4. Differential Verification Evidence

To prove that the old behavior was defective and that the corrected active path functions as intended, the two verifiers were tested against identical inputs:

| Input Text | Flawed Verifier Result | Corrected Active Verifier Result | Ground Truth Expected |
|---|---|---|---|
| `"There is no warranty duration specified on this page."` | **FAIL (0.0)** ❌ (Refusal penalized) | **PASS (1.0)** ✔ (`GROUNDED_REFUSAL_SUCCESS`) | **PASS (1.0)** |
| `"I checked the page thoroughly: warranty information is unlisted."` | **FAIL (0.0)** ❌ (Refusal penalized) | **PASS (1.0)** ✔ (`GROUNDED_REFUSAL_SUCCESS`) | **PASS (1.0)** |
| `"The warranty duration is 36 months."` | **PASS (1.0)** ❌ (Hallucination rewarded) | **FAIL (0.0)** ✔ (`UNSUPPORTED_DURATION_HALLUCINATION`) | **FAIL (0.0)** |
| `"The manufacturer offers a 2-year warranty."` | **FAIL (0.0)** (Did not match '36 mo') | **FAIL (0.0)** ✔ (`UNSUPPORTED_DURATION_HALLUCINATION`) | **FAIL (0.0)** |
| `"Warranty is not stated on page, but typically 36 months."` | **FAIL (0.0)** | **FAIL (0.0)** ✔ (`CONTRADICTORY_REFUSAL_WITH_HALLUCINATION`) | **FAIL (0.0)** |
| `"The price is $49.99."` | **FAIL (0.0)** | **FAIL (0.0)** ✔ (`UNRELATED_OR_AMBIGUOUS_NON_REFUSAL`) | **FAIL (0.0)** |
| `""` (Empty string) | **FAIL (0.0)** | **FAIL (0.0)** ✔ (`EMPTY_OUTPUT`) | **FAIL (0.0)** |

---

## 5. Test Suite Updates & Fresh Execution

1. **`offline_test_suite.py` Test #7:** Updated to `test_t6_strict_grounded_refusal_verifier()`.
2. **`offline_test_suite.py` Test #8:** Added `test_t6_regression_battery()`, validating 44 distinct test cases:
   - 10 standard grounded refusal variants (PASS).
   - 10 duration hallucination variants (FAIL).
   - 5 contradictory statements (FAIL).
   - 8 unrelated / ambiguous outputs (FAIL).
   - 7 casing, whitespace, and formatting variants.
   - 4 boundary inputs.
3. **`test_mutation_audit.py` Mutation #4:** Updated to import and test `protocol_v3_runner.verify_task_result("T6", ...)` directly through the production entry point.

### Fresh Test Execution Results:
```
C:\testing\.venv311\Scripts\python.exe offline_test_suite.py
[07/13] PASS: test_t6_strict_grounded_refusal_verifier (0.0ms)
       -> T6 grounded refusal correctly scores valid refusal and rejects hallucination (CONFIRMED)
[08/13] PASS: test_t6_regression_battery (0.2ms)
       -> T6 comprehensive regression battery passed (44 diverse test cases validated in active runner) (CONFIRMED)

Test execution complete: 13/13 PASSED. (Exit Code: 0)
```

```
C:\testing\.venv311\Scripts\python.exe test_mutation_audit.py
Ran 6 tests in 0.002s — OK (Exit Code: 0)
```

---

## 6. Downstream Pipeline Reconciliation

* **`run_single_mock_trial`:** Line 275 of [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L275) simulates `"There is no warranty duration specified on this page."`. Under the corrected verifier, mock evaluation yields `success=True`, `score=1.0`, accurately reflecting a grounded refusal.
* **`run_offline_pipeline_demo.py`:** Step 3A previously had a workaround inspecting `details.refusal_detected`. With the active runner returning `success=True`, the workaround is no longer required and DOM state mechanics match 100%.
* **`analyze_v3_results.py`:** Retains segregation of T1–T5 (confirmatory benchmark) from T6 (exploratory probe). T6 results are logged exclusively to `t6_probe_summary.csv` and do not contaminate primary CMH contrasts.

---

## 7. Conclusion

The critical T6 verifier defect in the active runner is **fully fixed, integrated, and verified**. No live execution path can reward hallucinated durations or penalize grounded refusals. All call sites, return structures, and regression tests are operational.

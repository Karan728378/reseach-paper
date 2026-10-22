# Verifiers, Retries, and Outcome Definitions Audit

**Document Version:** 1.0 (Audited & Verified)  
**Date:** October 21, 2026  
**Auditor:** Antigravity Scientific Methodology & Systems Team  
**Compliance Status:** 100% Offline · Source-Code Verification · Regression Test Validation  
**Associated Scripts:** [`runner/verifier.py`](file:///C:/testing/runner/verifier.py), [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py), [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py)  

---

## 1. Executive Summary

A scientific experiment evaluating autonomous browser agents depends fundamentally on the **validity, strictness, and neutrality of its task verifiers and retry policies**. If verifiers are overly permissive, they reward incorrect or guessing behaviors; if runners selectively retry failed attempts, they induce severe survivorship bias.

This audit:
1. Re-verified all historical verifier defects against the actual source code of [`runner/verifier.py`](file:///C:/testing/runner/verifier.py) and historical logs.
2. Verified the strictness of Protocol v3 verifiers in [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py).
3. **Uncovered a critical design-vs-code contradiction on Task T6:** While [`protocol.md`](file:///C:/testing/research_execution_20261018/protocol.md) and [`analysis_plan.md`](file:///C:/testing/research_execution_20261018/analysis_plan.md) define T6 as a negative refusal probe where stating *"warranty not found"* is $1$ and guessing *"36 months"* is $0$, the actual runner code in `protocol_v3_runner.py:Line 129` implemented the exact reverse (`success = bool(match_36_mo and not refusal)`).
4. Confirmed the elimination of retry survivorship bias under Protocol v3.

---

## 2. Comprehensive Task Verification Audit Table

| Task ID | Task Instruction | Preconditions | Target Entity & Ground Truth | Historical Verifier (`runner/verifier.py`) | Protocol v3 Verifier (`protocol_v3_runner.py`) | Defect / Discrepancy Status |
|---|---|---|---|---|---|---|
| **T1** | *"Search for 'wireless headphones' and add the least expensive result to your cart."* | Empty cart (`len == 0`), order confirmed `False`. | `wh-001` ($49.99, SoundFlow Air 3). Search results sorted by rating desc so `wh-001` is last. | Checks `cart.some(wh-001)`. Grants 0.25 if cart non-empty + 0.50 if `wh-001` present. | Strict binary: `1.0` if `wh-001` in cart, else `0.0`. Details record cart contents. | **RESOLVED IN V3.** Historical partial credit eliminated. |
| **T2** | *"Find the product called 'Mechanical Keyboard Pro' and add it to your cart."* | Empty cart (`len == 0`). | `mkp-001` ($149.99). | `1.0` if `mkp-001` in cart, else `0.0`. | Strict binary: `1.0` if `mkp-001` in cart, else `0.0`. | **VALID.** Clean binary verification across versions. |
| **T3** | *"Navigate to the Audio category. Compare the customer ratings of all products. Add the product with the second-highest customer rating to your cart."* | Empty cart (`len == 0`). | `wh-002` (BudPro Wireless X, rating 4.5). Category has `wh-003` (4.8), `wh-002` (4.5), `wh-001` (4.2). | **CRITICAL DEFECT:** Accepted `{"wh-001", "wh-002", "wh-003", "mkp-001", "mon-001", "acc-001"}` (6 SKUs including non-audio items!). | Strict single SKU: `len(cart) == 1 and cart[0] == 'wh-002'`. Rejects multiple items and wrong SKUs. | **RESOLVED IN V3.** Confirmed by `offline_test_suite.py:Line 70`. |
| **T4** | *"Search for 'ErgoGlide Mouse' and add it to your cart. Then complete the checkout process using these test details..."* | Empty cart (`len == 0`). | `window.__orderConfirmed__ == True` and order items contain `mse-001`. | **CRITICAL DEFECT:** Unconditional `score += 0.25` awarded on checkout visit; rewarded broken checkouts. | Strict binary: `order_confirmed and has_mouse`. Failed checkouts receive `0.0`. | **RESOLVED IN V3.** Confirmed by `offline_test_suite.py:Line 85`. |
| **T5** | *"There is one item in your cart. Navigate to the cart and remove it so the cart is empty."* | Cart pre-seeded with 1 item (`wh-001`). Precondition must be verified before launch. | Cart is empty (`len == 0`) at termination. | Checked only post-run `len(cart) == 0`. If cart started empty, awarded automatic success without agent action. | Precondition assertion: Runner asserts `pre_cart_count == 1`. Requires `len(cart) == 0 and precondition_ok`. | **RESOLVED IN V3.** Confirmed by `offline_test_suite.py:Line 105`. |
| **T6** | *"Navigate to the product details for 'SoundFlow Air 3' (SKU: wh-001). Retrieve the exact manufacturer warranty duration specified for this item."* | Navigated to `wh-001`. | **Warranty duration is completely absent from all site variants and catalogs.** | Not present in Protocol v2 (historical). | **CRITICAL DISCREPANCY:** Coded as `match and not refusal` on `"36 months"` (`score=1.0`), contradicting `protocol.md`. | **REQUIRES HUMAN DECISION / PROTOCOL V4 REVISION.** (See Section 3). |

---

## 3. Detailed Forensic Analysis: The Task T6 Discrepancy

### 3.1 The Contradiction Explained
During our code audit, a severe divergence was identified between the conceptual documentation and the executable code:

1. **What the Protocol & Analysis Plan State:**
   - [`protocol.md:Lines 95–101`](file:///C:/testing/research_execution_20261018/protocol.md#L95-L101):  
     *"DOM Reality: Warranty duration is completely absent from the website across all variants... Grounded Refusal ($Y_{\text{refusal}} = 1$): Agent correctly identifies and reports that warranty information is unstated/not found on the page. Hallucinated Assertion ($Y_{\text{refusal}} = 0$): Agent invents or guesses an ungrounded duration (e.g. asserting '36 months')."*
   - [`analysis_plan.md:Lines 23–28`](file:///C:/testing/research_execution_20261018/analysis_plan.md#L23-L28):  
     *"T6 cannot evaluate retrieval success. It measures hallucination resistance: $Y_{\text{refusal}} = 1$ (Success): Agent explicitly states that the warranty information is not found/unstated on the page."*
   - [`final_review/FINAL_HANDOFF.md:Line 32`](file:///C:/testing/research_execution_20261018/final_review/FINAL_HANDOFF.md#L32):  
     *"Scoring '36 months' as a success rewarded hallucinations and penalized honesty. T6 was removed from the primary benchmark and converted into an exploratory refusal probe."*

2. **What the Actual Code in `protocol_v3_runner.py` Implements:**
   - [`protocol_v3_runner.py:Lines 124–134`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L124-L134):
     ```python
     elif task_id == "T6":
         text = final_text or ""
         refusal = bool(re.search(r'\b(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not)\b.*?\b(warranty|guarantee|found|find|stated|listed)\b', text, re.IGNORECASE))
         match = bool(re.search(r'\b36\s*(months?|mo)\b', text, re.IGNORECASE))
         success = bool(match and not refusal)  # <--- REWARDS 36 MONTHS, PENALIZES REFUSAL!
         return {
             "success": success,
             "score": 1.0 if success else 0.0,
             "details": {"matched_36_months": match, "refusal_detected": refusal, "text_excerpt": text[:100]}
         }
     ```
   - In [`offline_test_suite.py:Lines 126–132`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L126-L132):
     ```python
     def test_t6_strict_retrieval_verifier():
         v3_pass = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text="The warranty duration is 36 months.")
         assert v3_pass["success"] is True and v3_pass["score"] == 1.0
         v3_fail = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text="I could not find the warranty.")
         assert v3_fail["success"] is False and v3_fail["score"] == 0.0
     ```

### 3.2 Scientific Consequence
- Because manufacturer warranty duration does **not exist** anywhere in [`shared/products.js`](file:///C:/testing/shared/products.js) or any HTML template, the string `"36 months"` can only be produced by an LLM via **hallucination or parametric memory priors**.
- Under `protocol_v3_runner.py`, an honest agent that reports *"I searched the page and found no warranty listed"* receives `score = 0.0` (Failure), while a hallucinating agent that fabricates *"The warranty is 36 months"* receives `score = 1.0` (Success)!
- **Resolution for Protocol v4:** In Protocol v4, T6's verifier must be formally updated to align with the conceptual definition: `success = bool(refusal and not hallucination)`, or T6 must be replaced with a grounded retrieval task where ground truth actually exists on the page.

---

## 4. Audit of Runner Retry Policies & Survivorship Bias

### 4.1 Historical Runner Implementation (`runner/agent-runner.py`)
In the historical runner used during Experiment 1:
```python
# HISTORICAL CODE in runner/agent-runner.py:
def get_completed_run_indices(summary_csv: Path) -> set:
    completed = set()
    with summary_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("success", "").lower() == "true":  # <--- SURVIVORSHIP BIAS!
                completed.add(int(row["run_index"]))
    return completed
```
- **The Survivorship Flaw:** When the runner was interrupted or restarted, it only considered runs with `success == True` as completed.
- Any legitimate task failure (`success == False`) was treated as incomplete and re-executed upon resumption.
- **Forensic Confirmation:** In historical Repetition 9 (October 6, 2026), run `d6c79dab` failed on `v3-data-attrs` T4. Upon restart on October 7, the runner re-attempted the run until achieving success (`925aac22`). This biased the historical dataset, inflating success rates to ~99.6%.

### 4.2 Protocol v3 Terminal Failure Policy (`protocol_v3_runner.py`)
In Protocol v3, the retry logic was rewritten:
1. **Terminal Recording:** Both `success = True` and `success = False` runs are written to `v3_run_summary.csv` and marked as permanently **COMPLETED**.
2. **Never Retry Domain Failures:** Failed runs are never re-attempted under any circumstances.
3. **Infrastructure Crash Handling:** Only fatal execution aborts (e.g., HTTP 429 API quota exhaustion or process termination before post-verification) are eligible for resumption.
4. **Verified by Unit Test:** [`offline_test_suite.py:Lines 150–180`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L150-L180) (`test_runner_retry_logic_survivorship_flaw`) confirms that Protocol v3 treats failures as terminal records.

---

## 5. Summary of Negative Test Coverage

All verifiers are backed by deterministic negative tests in [`task_specifications.json`](file:///C:/testing/research_execution_20261018/task_specifications.json) and [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py):

| Task | Test Condition | Input State | Expected Outcome | Actual Verification |
|---|---|---|:---:|:---:|
| **T1** | Wrong SKU in cart | `cart = [{"sku": "wh-003", "price": 129.99}]` | `success: False, score: 0.0` | **PASS** |
| **T1** | Empty cart | `cart = []` | `success: False, score: 0.0` | **PASS** |
| **T2** | Wrong SKU in cart | `cart = [{"sku": "wh-001"}]` | `success: False, score: 0.0` | **PASS** |
| **T3** | Permissive historical SKU | `cart = [{"sku": "mkp-001"}]` | `success: False, score: 0.0` | **PASS** |
| **T3** | Correct SKU + extra item | `cart = [{"sku": "wh-002"}, {"sku": "wh-001"}]` | `success: False, score: 0.0` | **PASS** |
| **T4** | Incomplete checkout | `order_confirmed = False, items = ["mse-001"]` | `success: False, score: 0.0` | **PASS** |
| **T4** | Wrong product checkout | `order_confirmed = True, items = ["wh-001"]` | `success: False, score: 0.0` | **PASS** |
| **T5** | Unseeded initial empty cart | `pre_cart_count = 0, cart = []` | `success: False, score: 0.0` | **PASS** |
| **T5** | Failure to remove item | `pre_cart_count = 1, cart = [{"sku": "wh-001"}]` | `success: False, score: 0.0` | **PASS** |

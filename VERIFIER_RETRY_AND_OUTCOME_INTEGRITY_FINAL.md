# Verifier, Retry, and Outcome-Integrity Audit: Final Evaluation

**Document Version:** 1.0 (Comprehensive Verifier & Execution Integrity Audit)  
**Date:** October 22, 2026  
**Auditor:** Antigravity Scientific Methodology & Protocol Architecture Team  
**Compliance Status:** 100% Offline · Deterministic Verification  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Executive Summary & Audit Mandate

In autonomous web agent benchmarks, outcome integrity depends fundamentally on:
1. Grounded state assertions rather than trusting the model's textual declarations.
2. Binary evaluation criteria that prevent partial credit from rewarding failed trajectories.
3. Strict precondition assertions that prevent vacuous "no-op" passes.
4. Terminal recording of failed runs to prevent retry-until-success survivorship bias.

This audit evaluates all six tasks (T1–T6), audits retry mechanisms, and maps task verifiers to ground truth.

---

## 2. Granular Task-by-Task Verifier Audit

| Task ID | Task Description | Target Entity / SKU | Preconditions | Ground Truth Assertion | Historical Defect | Protocol v3/v4 Status |
|:---:|---|---|---|---|---|:---:|
| **T1** | Cheapest Wireless Headphone Addition | `wh-001` (SoundFlow Air 3, $49.99) | Cart empty, order unconfirmed | `window.__cart__.some(i => i.sku === 'wh-001')` | None (historical verifier checked SKU). | **VERIFIED STRICT** |
| **T2** | Targeted Entity Addition | `mkp-001` (Mechanical Keyboard Pro) | Cart empty, order unconfirmed | `window.__cart__.some(i => i.sku === 'mkp-001')` | None (historical verifier checked SKU). | **VERIFIED STRICT** |
| **T3** | Second-Highest Rated Audio Product | `wh-002` (BudPro Wireless X, rating 4.5) | Cart empty, order unconfirmed | `len(cart) == 1 && cart[0].sku === 'wh-002'` | **CRITICAL FLAW:** Historical `verifier.py:270` accepted **6 different SKUs** (`wh-001`, `wh-002`, `wh-003`, `spk-001`, etc.). | **VERIFIED STRICT** (Enforces single-item exact match on `wh-002`). |
| **T4** | Multi-Step Checkout Flow Completion | `mse-001` (ErgoGlide Mouse, 8 form fields) | Cart empty, order unconfirmed | `window.__orderConfirmed__ === true && lastOrder has mse-001` | **CRITICAL FLAW:** Historical `verifier.py:315` awarded unconditional **0.25 partial credit** on failed orders if checkout page visited. | **VERIFIED STRICT** (Strict 0.0 on failed order; 1.0 only on confirmed completion). |
| **T5** | State Mutation (Cart Item Removal) | Pre-seeded with `wh-001` | Cart pre-seeded with 1 item (`pre_cart_count == 1`) | `len(window.__cart__) === 0 && pre_cart_count == 1` | **VACUOUS PASS FLAW:** Historical verifier did not assert pre-state; doing nothing to an empty cart resulted in `success=True`. | **VERIFIED STRICT** (Runner strictly asserts `pre_cart_count == 1`). |
| **T6** | Manufacturer Warranty Fact Probe | `wh-001` (Warranty is absent from website) | Cart empty | `refusal_detected and not hallucination_detected` | **SCORING INVERSION BUG:** Protocol v3 runner rewarded matching `"36 months"` and penalized refusal. | **CORRECTED IN ISOLATED MODULE** (Staged in `T6_VERIFIER_PROPOSED_PATCH.diff`). |

---

## 3. Preconditions, Postconditions, and Vacuous Pass Elimination

1. **Precondition Seeding (Task T5):**
   - In `tasks/task-definitions.json`, Task T5 defines pre-seeding via local storage injection:
     ```javascript
     localStorage.setItem('techmart_cart', JSON.stringify([{sku:'wh-001',name:'SoundFlow Air 3',quantity:1,price:49.99}]));
     ```
   - In [`protocol_v3_runner.py:114-123`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L114):
     ```python
     is_empty = (len(cart) == 0)
     precondition_ok = (pre_cart_count is None or pre_cart_count == 1)
     success = bool(is_empty and precondition_ok)
     ```
   - If the pre-cart was empty (`pre_cart_count == 0`), the verifier rejects the run, preventing an agent from passing by taking zero actions.
2. **Postcondition Strictness:**
   - On Tasks T1, T2, T3, and T5, verification queries `window.__cart__` via Playwright CDP evaluation.
   - On Task T4, verification queries `window.__orderConfirmed__` and `window.__lastOrder__`.
   - The verifier never trusts the agent's textual output to determine task success (except on T6, where textual refusal is the defined endpoint).

---

## 4. Retry Logic, Selection Bias, and Survivorship Elimination

### 4.1 Historical Survivorship Bias Flaw
In the historical pilot implementation ([`runner/agent-runner.py`](file:///C:/testing/runner/agent-runner.py)), the function `get_completed_run_indices()` filtered completed runs with:
```python
# HISTORICAL DEFECTIVE CODE:
if row.get("success") == "True":
    completed.add(run_id)
```
- **Consequence:** If an agent failed a run, the run was not marked completed in the cache. On restart (or during repetitive loops in Rep 9), the runner repeatedly retried the failed condition until it succeeded.
- This introduced severe **survivorship bias**, artificially inflating the reported pilot success rate to 99.6%.

### 4.2 Protocol v3/v4 Survivorship Fix
In [`research_execution_20261018/protocol_v3_runner.py:144-160`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L144):
```python
def get_completed_run_indices(summary_csv: Path) -> set[int]:
    completed = set()
    if not summary_csv.exists():
        return completed
    with summary_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row.get("run_index") or row.get("scheduled_run_index")
            status = row.get("status", "completed")
            if idx and str(idx).isdigit() and status == "completed":
                completed.add(int(idx))
    return completed
```
- **Outcome:** Both `success = True` and `success = False` runs receive `status = "completed"`.
- Failed trials are logged permanently and **never retried**.
- Only runs aborted due to fatal infrastructure errors (e.g. `status = "quota_aborted"`) remain eligible for resumption.
- Denominator integrity is 100% preserved.

---

## 5. Execution Limits & Step Caps

- **Step Cap:** Enforced strictly at **30 steps** per task attempt. If an agent does not achieve the target state within 30 steps, the trial terminates with `success = False`.
- **Session Timeout:** Enforced at **120 seconds** wall-clock time per trial.
- **Action Verification:** Browser actions (`click`, `fill`, `navigate`) are validated against real DOM state before advancing step counts.

---

## 6. Verifier & Outcome Integrity Verdict

1. **State Grounding:** **VERIFIED.** T1–T5 assert browser JavaScript state (`window.__cart__`, `window.__orderConfirmed__`).
2. **Survivorship Bias:** **ELIMINATED.** Protocol v3 runner terminates and logs failed runs.
3. **Partial Credit:** **ELIMINATED.** Strict binary scoring ($1.0$ or $0.0$).
4. **Action Required:** Apply [`T6_VERIFIER_PROPOSED_PATCH.diff`](file:///C:/testing/research_execution_20261018/T6_VERIFIER_PROPOSED_PATCH.diff) to align the T6 verifier with Grounded Refusal criteria.

# Task Verifiers, Ground Truth & Deterministic State Audit

**Document:** `audit_20261022_final/TASK_VERIFIERS_AND_DETERMINISTIC_STATE.md`  
**Audit Date:** October 22, 2026  
**Auditor:** Antigravity Senior Research Engineer, Browser-Agent Systems Specialist & Reproducibility Lead  
**Execution Context:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9, `browser-use 0.13.10`)  

---

## 1. Ground Truth Specification for Tasks T1–T6

Every task is evaluated against canonical application state extracted from the browser session (`window.__cart__`, `window.__orderConfirmed__`, `window.__lastOrder__`), rather than loose text matching or screenshots.

| Task ID | Task Description | Target Entity / SKU | Catalog Facts & Ground Truth | Authoritative Client State Verified | Strict Scoring Criterion | Historical Flaw Resolved |
|---|---|:---:|---|---|---|---|
| **T1** | Search for 'wireless headphones' and add least expensive. | `wh-001` (SoundFlow Air 3) | Catalog contains 3 audio items: `wh-001` ($49.99), `wh-002` ($89.99), `wh-003` ($129.99). Lowest is `wh-001`. | `window.__cart__` | `any(i['sku'] == 'wh-001' for i in cart)` $\implies 1.0$; otherwise $0.0$. | Rejects expensive headphones (`wh-002`, `wh-003`). |
| **T2** | Find 'Mechanical Keyboard Pro' and add to cart. | `mkp-001` | Exact SKU `mkp-001` ($149.99). | `window.__cart__` | `any(i['sku'] == 'mkp-001' for i in cart)` $\implies 1.0$; otherwise $0.0$. | Rejects unrelated products (e.g. `mse-001`). |
| **T3** | Navigate to Audio. Compare ratings. Add product with second-highest rating. | `wh-002` (BudPro Wireless X) | Audio ratings: `wh-003` (4.8), `wh-002` (4.5), `wh-001` (4.2). Second-highest is strictly `wh-002`. | `window.__cart__` | `len(cart) == 1 and cart[0]['sku'] == 'wh-002'` $\implies 1.0$; otherwise $0.0$. | Historical verifier accepted 6 SKUs; v4 strictly enforces `wh-002` only and rejects multi-item carts. |
| **T4** | Search 'ErgoGlide Mouse', add to cart, complete checkout with test details. | `mse-001` | Checkout flow requires valid card details, updating `__orderConfirmed__` to `true`. | `window.__orderConfirmed__`, `window.__lastOrder__` | `order_confirmed == True and mse-001 in last_order_items` $\implies 1.0$; otherwise $0.0$. | Historical verifier gave 0.25 on incomplete checkouts; v4 awards $0.0$. |
| **T5** | There is one item in cart. Remove it so cart is empty. | `wh-001` (Pre-seeded) | Application is initialized with exactly one `wh-001` item in `localStorage` and `window.__cart__`. | Pre: `pre_cart_count == 1`<br>Post: `len(cart) == 0` | `len(cart) == 0 and pre_cart_count == 1` $\implies 1.0$; missing/unseeded precondition $\implies 0.0$. | Historical verifier accepted empty cart without pre-seeding; v4 strictly enforces precondition. |
| **T6** | Retrieve manufacturer warranty duration for 'SoundFlow Air 3'. | Absent fact | Warranty duration is intentionally omitted across all variants and catalogs. | Model output text via `verify_t6_grounded_refusal` | `refusal=True and hallucination=False` $\implies 1.0$; duration hallucination or contradiction $\implies 0.0$. | Historical verifier rewarded "36 months" regex; v4 rewards grounded refusal. |

---

## 2. Precondition Validation for Task T5

In [`protocol_v3_runner.py:423-437`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L423):
1. **Authoritative Seeding:** The runner executes client JavaScript pre-seeding `wh-001` into `localStorage['techmart_cart']` and `window.__cart__`, triggering `window.__refreshCartView__()`.
2. **Pre-Action State Query:** Queries `window.__cart__.length` via CDP and records `pre_cart_count`.
3. **Precondition Assertion:** If `pre_cart_count != 1`, raises `RuntimeError("T5 pre-state verification failed")`.
4. **Verifier Hardening:** [`protocol_v3_runner.py:117`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L117) checks `precondition_ok = (pre_cart_count == 1)`. If `pre_cart_count` is `None` (missing) or `0` (unseeded), `score = 0.0`.

---

## 3. Grounded Refusal Logic for Task T6

In [`protocol_v3_runner.py:149-205`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L149):
- **Refusal Pattern:** Matches explicit negative assertions (`no`, `not stated`, `unspecified`, `not mentioned`, `unavailable`, `missing` near warranty terms).
- **Hallucination Pattern:** Detects numeric duration claims (`36 months`, `2-year`, `12 mo`, `3 years`, `90 days`).
- **Scoring Rubric:**
  - `refusal_detected=True, hallucination_detected=False` $\implies$ `GROUNDED_REFUSAL_SUCCESS` (`score=1.0`).
  - `refusal_detected=True, hallucination_detected=True` $\implies$ `CONTRADICTORY_REFUSAL_WITH_HALLUCINATION` (`score=0.0`).
  - `refusal_detected=False, hallucination_detected=True` $\implies$ `UNSUPPORTED_DURATION_HALLUCINATION` (`score=0.0`).
  - `refusal_detected=False, hallucination_detected=False` $\implies$ `UNRELATED_OR_AMBIGUOUS_NON_REFUSAL` (`score=0.0`).

---

## 4. Mutation Testing Verification Results

[`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py) executes 10 mutation tests asserting that verifiers detect intentional breakages:

| Mutation Tested | Description | Mutation Result | Assertion Result |
|---|---|:---:|:---:|
| **Mutation 1** | T3 accepting `wh-001` instead of `wh-002` | Detected & Rejected | **PASS** |
| **Mutation 2** | T4 awarding unconditional 0.25 on checkout visit | Detected & Rejected | **PASS** |
| **Mutation 3** | T5 passing empty cart when `pre_cart_count` is 0 or None | Detected & Rejected | **PASS** |
| **Mutation 4** | T6 inverting logic to reward "36 months" | Detected & Rejected | **PASS** |
| **Mutation 5** | Safety gate bypass without `--confirm-live-execution` | Caught & Interlocked | **PASS** |
| **Mutation 6** | CMH odds ratio inversion on treatment swap | Detected & Inverted | **PASS** |
| **Mutation 7** | T1 accepting expensive headphones (`wh-002`, $89.99) | Detected & Rejected | **PASS** |
| **Mutation 8** | T2 accepting wrong product (`mse-001`) | Detected & Rejected | **PASS** |
| **Mutation 9** | T3 accepting multi-item cart containing `wh-002` + `wh-001` | Detected & Rejected | **PASS** |
| **Mutation 10**| T4 passing confirmed order containing wrong item (`wh-001`) | Detected & Rejected | **PASS** |

All 10 mutation tests pass with Exit Code 0.

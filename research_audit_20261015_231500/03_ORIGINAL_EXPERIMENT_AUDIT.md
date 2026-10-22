# 03. Original Experiment Audit & Validity Threat Analysis

**Audit Directory:** `C:\testing\research_audit_20261015_231500`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Experiment Execution Breakdown

### Table 1: Run Accounting Matrix by Variant and Task

| Variant | Task | Planned | Started | Completed (Success) | Quota Failures (429) | Genuine Task Failures | Unexecuted (Truncated) | Status |
|---|---|---|---|---|---|---|---|---|
| **v0-baseline** | T1 | 10 | 8 | 6 | 2 | 0 | 2 | Imbalanced |
| **v0-baseline** | T2 | 10 | 8 | 4 | 4 | 0 | 2 | Imbalanced |
| **v0-baseline** | T3 | 10 | 7 | 6 | 1 | 0 | 3 | Imbalanced |
| **v0-baseline** | T4 | 10 | 7 | 7 | 0 | 0 | 3 | Imbalanced |
| **v0-baseline** | T5 | 10 | 9 | 7 | 2 | 0 | 1 | Imbalanced |
| **v1-jsonld** | T1 | 10 | 9 | 8 | 1 | 0 | 1 | Imbalanced |
| **v1-jsonld** | T2 | 10 | 6 | 6 | 0 | 0 | 4 | Severe Truncation |
| **v1-jsonld** | T3 | 10 | 6 | 4 | 2 | 0 | 4 | Severe Truncation |
| **v1-jsonld** | T4 | 10 | 4 | 2 | 2 | 0 | 6 | Severe Truncation |
| **v1-jsonld** | T5 | 10 | 8 | 3 | 5 | 0 | 2 | Imbalanced |
| **v2-aria** | T1 | 10 | 6 | 5 | 1 | 0 | 4 | Severe Truncation |
| **v2-aria** | T2 | 10 | 4 | 3 | 1 | 0 | 6 | Severe Truncation |
| **v2-aria** | T3 | 10 | 10 | 7 | 3 | 0 | 0 | Full Reps Started |
| **v2-aria** | T4 | 10 | 9 | 7 | 2 | 0 | 1 | Imbalanced |
| **v2-aria** | T5 | 10 | 8 | 4 | 4 | 0 | 2 | Imbalanced |
| **v3-data-attrs** | T1 | 10 | 8 | 7 | 1 | 0 | 2 | Imbalanced |
| **v3-data-attrs** | T2 | 10 | 8 | 7 | 1 | 0 | 2 | Imbalanced |
| **v3-data-attrs** | T3 | 10 | 5 | 2 | 3 | 0 | 5 | Severe Truncation |
| **v3-data-attrs** | T4 | 10 | 10 | 5 | 5 | 0 | 0 | Full Reps Started |
| **v3-data-attrs** | T5 | 10 | 7 | 5 | 2 | 0 | 3 | Imbalanced |
| **TOTALS** | — | **200** | **147** | **105** | **42** | **0** | **53** | **Truncated MNAR** |

---

## 2. In-Depth Evaluation of Critical Validity Threats

### Threat 1: Task Solvability via Visible Text Alone (T1–T5)
- **Status:** **CONFIRMED (FATAL CONSTRUCT VALIDITY THREAT)**
- **Evidence:**
  - In `shared/products.js`, every product attribute required to solve T1–T5 is rendered directly into the visual DOM:
    - Product title (e.g., `SoundFlow Air 3`, `Mechanical Keyboard Pro`) is rendered inside `<h3>`.
    - Price (e.g., `$49.99`, `$149.99`) is rendered inside `<span class="price">`.
    - Rating (e.g., `4.2`, `4.5`, `4.8`) is rendered inside `<span class="rating">`.
  - The agent never needed ARIA, `data-*`, or JSON-LD to find the cheapest item, check the keyboard, or compare ratings.
  - Because visible text was identical across all variants, any observed performance parity was trivially guaranteed: the agent solved the tasks purely using standard visual text navigation.

### Threat 2: T3 Second-Highest-Rating Verifier Determinism
- **Status:** **CONFIRMED (CRITICAL VERIFIER FLAW)**
- **Code Reference:** [`runner/verifier.py:60-64`](file:///C:/testing/runner/verifier.py#L60-L64) & [`runner/verifier.py:417-447`](file:///C:/testing/runner/verifier.py#L417-L447)
- **Evidence:**
  - Task T3 prompt: *"Compare the customer ratings of all products. Add the product with the second-highest customer rating to your cart."*
  - Ground truth: Audio category has `wh-003` (4.8), `wh-002` (4.5), and `wh-001` (4.2). The second-highest is deterministically `wh-002`.
  - However, `verifier.py` defined:
    ```python
    eligible = {"wh-001", "wh-002", "wh-003", "mkp-001", "mon-001", "acc-001"}
    success = has_eligible and not has_ineligible
    ```
  - **Empirical test outcome:** If the agent selected `wh-001` (lowest rating), it passed with 1.0! If it selected `wh-003` (highest rating), it passed with 1.0! If it selected a non-audio keyboard (`mkp-001`), it passed with 1.0!
  - **Verdict:** The reported 100% success rate on T3 in prior reports is compromised by an overly permissive ground-truth set.

### Threat 3: T4 Stale `__lastOrder__` State Vulnerability
- **Status:** **LIKELY THREAT**
- **Code Reference:** [`runner/agent-runner.py:491-503`](file:///C:/testing/runner/agent-runner.py#L491-L503) & [`runner/verifier.py:468-496`](file:///C:/testing/runner/verifier.py#L468-L496)
- **Evidence:**
  - In `app-core.js`, `window.__orderConfirmed__` is set to `true` and `window.__lastOrder__` is populated on checkout.
  - If a browser session or local storage context is retained across runs without full cache/storage wipe, a subsequent T4 run could read the prior run's order confirmation.
  - While `agent-runner.py` creates a new `BrowserSession(is_local=True)` per run, it does not explicitly wipe Chrome's user-data directory between runs.

### Threat 4: T5 Cart Seeding Failure False-Pass
- **Status:** **CONFIRMED (CRITICAL VERIFIER FLAW)**
- **Code Reference:** [`runner/verifier.py:457-463`](file:///C:/testing/runner/verifier.py#L457-L463)
- **Evidence:**
  - Task T5 requires: *"There is one item in your cart. Navigate to the cart and remove it so the cart is empty."*
  - `verifier.py` checks only:
    ```python
    is_empty = len(cart) == 0
    return {"success": is_empty, "partial_score": 1.0 if is_empty else 0.0}
    ```
  - If Playwright's `run_task_setup` fails to inject the item into `localStorage`, or if the page fails to load, `len(cart) == 0` evaluates to `True`!
  - **Empirical test outcome:** An empty, unseeded cart scores `1.0` (Success) with ZERO agent action. The verifier never verified that the cart initially contained `wh-001`.

### Threat 5: Substring Matching vs Exact SKU Matching
- **Status:** **RESOLVED (NO FLAW FOUND)**
- **Code Reference:** [`runner/verifier.py:394, 410, 476`](file:///C:/testing/runner/verifier.py#L394)
- **Evidence:**
  - Static inspection and unit tests confirm that `verifier.py` uses exact string equality: `any(i["sku"] == "wh-001" for i in cart)` and `any(i["sku"] == "mse-001" for i in last_order_items)`. Substring collisions (e.g. `wh-001-fake`) correctly evaluate to `False`.

### Threat 6: Sample Missingness and Retries
- **Status:** **CONFIRMED (FATAL PROTOCOL BIAS)**
- **Evidence:**
  - In `agent-runner.py:150-170`, `get_completed_run_indices()` explicitly filters out failed runs:
    ```python
    if row.get("success") in ("True", True, "true", "1"):
        completed.add(int(idx))
    ```
  - This design treats only *successful* runs as complete, creating an inherent protocol bias toward retrying failed runs until they pass.
  - Coupled with the run-106 quota halt, the sample of 105 successes represents an incomplete, right-truncated, survivor-biased dataset.

---

## 3. Summary of Validity Threat Classifications

| Threat Item | Classification | Impact on Research Findings |
|---|---|---|
| Visible text confounding | **CONFIRMED** | Fatal: Null hypothesis of channel equivalence cannot be tested when visible text already supplies all facts. |
| T3 verifier over-permissiveness | **CONFIRMED** | High: T3 success rates were artificially inflated by accepting 6 SKUs. |
| T4 unconditional score inflation | **CONFIRMED** | Moderate: 0.25 partial points awarded even to quota failures. |
| T5 false-pass on empty cart | **CONFIRMED** | High: Unseeded or aborted runs receive 1.0 score. |
| Substring SKU matching | **RESOLVED** | None: Exact SKU equality verified. |
| MNAR Quota Truncation | **CONFIRMED** | Fatal: Sample of 105 cannot be analyzed with standard omnibus tests. |
| Selective Retry Protocol | **CONFIRMED** | Fatal: Discarding failures until success occurs invalidates error rates. |

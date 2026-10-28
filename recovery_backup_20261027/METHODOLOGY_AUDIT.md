# SCIENTIFIC METHODOLOGY AUDIT

**Project:** Autonomous Browser Agent Additive Semantic Markup Study (Option A)  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Audit Date:** October 21, 2026  

---

## 1. Central Research Question & Construct Validity

### Research Question
> *"Under a strictly text-based browser-agent setup (`use_vision=False`), do additional WAI-ARIA accessibility attributes or configured custom `data-*` attributes improve task completion accuracy compared with a baseline website when visible content and task conditions are strictly controlled?"*

### Construct Validity Assessment
- **Construct Evaluated:** Additive semantic token efficiency in text-only LLM context representations.
- **Controlled Independent Variables:** Visible HTML text content, website visual appearance, DOM interactive elements, backend pricing, product catalog (`shared/products.js`), and SPA routing logic (`shared/app-core.js`) are **100% identical across all arms**.
- **Manipulated Independent Variable:** The presence/absence of structured semantic metadata attributes (`aria-label` on buttons in `v2-aria`; `data-action`, `data-product-id` in `v3-data-attrs`).
- **Construct Isolation Status: VALID.** The design cleanly isolates whether semantic attributes improve agent action selection when visible text is already sufficient to complete the task.

---

## 2. Treatment Delivery Audit & Empirical Evidence

### 2.1 The DOM Serializer Bottleneck in `browser-use 0.13.10`
In standard web development, developers assume that any HTML attribute or `<script>` tag added to the DOM is visible to software interacting with the page. However, browser automation frameworks serialize the DOM into a token-limited text representation before passing it to the LLM.

Audit of [`browser-use 0.13.10`](file:///C:/testing/.venv/Lib/site-packages/browser_use/) revealed two critical architectural constraints:

1. **Element Pruning (`DISABLED_ELEMENTS`):**  
   In `browser_use/dom/serializer/serializer.py` (line 18):
   ```python
   DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
   ```
   Any element matching this set is stripped immediately.
   - **Empirical Finding:** `<script type="application/ld+json">` elements are unconditionally pruned. **JSON-LD NEVER reaches the LLM observation buffer.**
   - **Methodological Rule:** JSON-LD cannot be evaluated as an active agent delivery channel under standard `browser-use 0.13.10`. It is excluded from the primary experimental arms of Protocol v3.
2. **Attribute Filtering (`DEFAULT_INCLUDE_ATTRIBUTES`):**  
   In `browser_use/dom/views.py` (line 18), attributes are filtered against a hardcoded whitelist.
   - Standard `aria-label` on `<button>` elements is included by default.
   - Standard `aria-label` on non-interactive `<span>` elements is omitted.
   - Custom attributes (`data-action`, `data-product-id`, `data-category-slug`) are stripped by default.
   - **Harness Resolution:** [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) supplies `EXTENDED_ATTRIBUTES` to the `Agent` constructor, successfully exposing configured `data-*` attributes.

### 2.2 Empirical Treatment Delivery Matrix

| Treatment Arm | Target Variant | Visible Text Delivered? | ARIA Attributes Delivered? | Custom `data-*` Delivered? | JSON-LD Delivered? | Empirical Trace Test |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **BASELINE (ABS)** | `v0-baseline` | YES | NO | NO | NO | `test_agent_prompt_pipeline.py` (Test 1) |
| **BASELINE_REP (VIS)** | `v0-baseline` | YES | NO | NO | NO | `test_agent_prompt_pipeline.py` (Test 1) |
| **ARIA** | `v2-aria` | YES | YES (`aria-label` on buttons) | NO | NO | `test_agent_prompt_pipeline.py` (Test 2) |
| **DATA-CFG** | `v3-data-attrs` | YES | NO | YES (`data-action`, `data-product-id`) | NO | `test_agent_prompt_pipeline.py` (Test 4) |

---

## 3. Two-Tier Task Architecture & Verifier Hardening

Historical pilot experiments suffered from construct contamination because retrieval tasks, cart mutation tasks, and absent-fact probes were scored under inconsistent, loose verifiers. Protocol v3 establishes a strict two-tier architecture:

### 3.1 Primary Grounded Benchmark (Tasks T1–T5, $N=80$)
These tasks are grounded in visible page facts and application state:
- **Task T1 (Cheapest Wireless Headphone):** Target `wh-001` ($49.99). Verifier checks exact SKU in cart.
- **Task T2 (Mechanical Keyboard Pro):** Target `mkp-001` ($149.99). Verifier checks exact SKU in cart.
- **Task T3 (Second-Highest Rated Audio Product):** Target `wh-002` (BudPro Wireless X, rating 4.5; highest is `wh-003` at 4.8). Verifier strictly enforces `len(cart) == 1` and `cart[0] == "wh-002"`. Rejects multi-item carts or wrong SKUs (resolving historical flaw where 6 SKUs passed).
- **Task T4 (Mouse Checkout):** Target `mse-001` ($29.99). Verifier strictly checks `order_confirmed == True` and order items containing `mse-001` (resolving historical flaw awarding 0.25 on incomplete checkouts).
- **Task T5 (Cart Mutation):** Remove item from cart. Verifier asserts initial pre-state (`pre_cart_count == 1`) before checking empty final cart (`len(cart) == 0`). Aborts on setup failure, eliminating vacuous passes.

### 3.2 Exploratory Negative Probe (Task T6, $N=16$)
- **Context:** Manufacturer warranty duration is completely absent from all site variants and catalogs.
- **Construct Measured:** Hallucination resistance vs grounded refusal under prompt pressure.
- **Scoring Isolation:** Evaluated separately via refusal regex (`refusal_detected`). Prohibited from pooling into primary task completion accuracy.

---

## 4. Statistical Power & Strict Ban on Equivalence Claims

In [`POWER_RECONCILIATION.md`](file:///C:/testing/research_execution_20261018/final_review/POWER_RECONCILIATION.md), power calculations across 10,000 Monte Carlo trials in `recompute_power_rcbd.py` established:

- **Large Disparity ($\Delta = 0.70$):** $98.6\%$ power (robustly detectable).
- **Moderate Effect ($\Delta = 0.35$):** $49.7\%$ power (moderate detection sensitivity).
- **Small Effect ($\Delta = 0.20$):** $10.8\%$ power (**severely underpowered**).
- **Subtle Effect ($\Delta = 0.15$):** $5.8\%$ power (indistinguishable from nominal $\alpha$).

> [!WARNING]
> **METHODOLOGICAL RULE — STRICT BAN ON EQUIVALENCE CLAIMS:**  
> Because the experiment has $<11\%$ power to detect small differences ($\Delta \le 0.20$), a non-significant result ($p > 0.05$) CANNOT be claimed as evidence of "channel equivalence" or that semantic markup "does not matter." It proves only that the sample size ($N=20$/arm) was insufficient to detect subtle effects.

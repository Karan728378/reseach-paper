# Experimental Protocol: Additive Semantic Markup Evaluation on Autonomous Browser Agents

**Document Version:** 4.0 (Option A Finalized Protocol Freeze)  
**Date:** October 18, 2026  
**Authors:** [Redacted for Double-Blind Review]  
**Repository Location:** `C:\testing\research_execution_20261018\final_review\protocol.md`  
**Associated Artifacts:**
- Protocol v3 Runner: `research_execution_20261018/protocol_v3_runner.py`
- Randomized Schedule: `research_execution_20261018/proposed_randomized_schedule.csv` (96 balanced runs)
- Task Specifications: `task_specifications.json`
- Offline Audit Suite: `offline_test_suite.py` (11/11 PASS)
- Live Agent Prompt Suite: `test_agent_prompt_pipeline.py` (5/5 PASS)

---

## 1. Research Question and Empirical Framing

### 1.1 Research Question
> **Does augmenting a website that already displays factual information in visible text with structured semantic markup (WAI-ARIA accessibility attributes or configured custom `data-*` attributes) improve an autonomous text-based browser agent's task accuracy, execution efficiency (step count), and latency compared to unaugmented visible HTML?**

### 1.2 Scientific Framing: Option A (Additive Semantic Markup Evaluation)
In modern web development, websites display product names, prices, ratings, and stock status directly in human-visible typography (`<span>$49.99</span>`). In addition, developers frequently layer machine-readable metadata on top of visible elements:
1. **WAI-ARIA semantics:** Roles and accessible labels (`aria-label="Price: $49.99"`, `role="img" aria-label="Rating: 4.5 out of 5 stars"`) designed for assistive technologies.
2. **Custom `data-*` attributes:** Machine-readable hooks (`data-amount="49.99"`, `data-product-id="wh-001"`, `data-action="add-to-cart"`) designed for client-side scripts, telemetry, and automated testing.

Prior literature has assumed that browser agents either require visual perception or process raw HTML indiscriminately. This experiment measures whether adding structured semantic markup provides measurable advantages to an LLM agent operating in text-only DOM mode (`use_vision=False`).

---

## 2. Treatment Arm Definitions and Variant Verification

### 2.1 Treatment Arms ($K=4$, $N=96$ Runs Total)

| Arm ID | Treatment Name | Variant Source | Attribute Whitelist Configuration | Visible Text State | Agent Prompt Delivery |
|--------|----------------|----------------|-----------------------------------|--------------------|-----------------------|
| **BASELINE** (nominal ABS) | Unaugmented Plain HTML | `variants/v0-baseline` | `DEFAULT_INCLUDE_ATTRIBUTES` | Rendered visible text | Plain HTML text nodes; no ARIA or data-* attributes |
| **BASELINE_REP** (nominal VIS) | Baseline Replicate | `variants/v0-baseline` | `DEFAULT_INCLUDE_ATTRIBUTES` | Rendered visible text | Plain HTML text nodes; within-condition stability check |
| **ARIA** | Semantic Accessibility | `variants/v2-aria` | `DEFAULT_INCLUDE_ATTRIBUTES` | Rendered visible text | Delivered on interactive elements (`<button>`) and containers |
| **DATA-CFG** | Configured Custom Attributes | `variants/v3-data-attrs` | `EXTENDED_ATTRIBUTES` | Rendered visible text | Delivered on interactive elements under extended whitelist |

### 2.2 Independent Variant Equivalence Verification
An automated AST-level structural comparison (`verify_variant_diffs.py`) confirmed that:
1. **`v0-baseline` vs `v2-aria`:** Stripping `aria-*` attributes and `role` attributes yields a DOM tree that is **100% character-for-character identical** to `v0-baseline` in tags, classes, element hierarchy, text nodes, and styling.
2. **`v0-baseline` vs `v3-data-attrs`:** Stripping `data-*` attributes yields a DOM tree that is **100% character-for-character identical** to `v0-baseline`.
3. **Shared Assets:** All variants share the exact same `shared/app-core.js`, `shared/products.js`, and `shared/styles.css`.
4. **Conclusion:** Variants differ strictly and exclusively in their intended semantic markup. There is zero accidental divergence in layout, copy, or business logic.

---

## 3. Agent Observation Architecture and Whitelisting

### 3.1 Observation Pipeline Constraints in `browser-use 0.13.10`
Offline testing with `MockChatModel` (`test_agent_prompt_pipeline.py`) verified the precise serialization mechanics:
1. **Interactive Node Restriction:** Standard `browser-use` only serializes HTML attributes for interactive elements (`<button>`, `<input>`, `<a>`). Attributes placed on non-interactive elements (e.g. `<span class="product-price" aria-label="...">`) are omitted from LLM prompts by default, emitting only inner text.
2. **Serializer Patching:** In `runner/agent-runner.py`, `enable_observable_dom_serialization()` patches `serializer.py` to preserve non-interactive nodes bearing observable attributes.
3. **Custom Attribute Whitelisting:** Standard `DEFAULT_INCLUDE_ATTRIBUTES` discards custom attributes (`data-amount`, `data-rating`). The `DATA-CFG` arm explicitly configures `EXTENDED_ATTRIBUTES` to permit delivery to the agent context.
4. **JSON-LD Pruning:** `<script type="application/ld+json">` is permanently pruned by `DISABLED_ELEMENTS`.
5. **Vision Elimination:** `use_vision=False` is strictly enforced to prevent visual screenshots from confounding token-based markup evaluation.

---

## 4. Benchmark Tasks and Outcome Separation

The evaluation benchmark comprises six scheduled tasks ($J=6$), partitioned into two scientifically distinct outcome pools:

### 4.1 Primary Grounded Action Benchmark Pool (Tasks T1–T5)
All primary tasks require an observable action that modifies browser client state (`window.__cart__`, `window.__orderConfirmed__`). Target facts are present and visible on the website across all variants.

1. **Task T1: Least Expensive Search & Cart Insertion**
   - **Instruction:** `"Search for 'wireless headphones' and add the least expensive result to your cart."`
   - **Target Entity:** `wh-001` (SoundFlow Air 3, $49.99).
   - **Ground Truth:** `window.__cart__` must contain SKU `wh-001`. Strict binary scoring.

2. **Task T2: Direct Item Identification & Addition**
   - **Instruction:** `"Find the product called 'Mechanical Keyboard Pro' and add it to your cart."`
   - **Target Entity:** `mkp-001` ($149.99).
   - **Ground Truth:** `window.__cart__` must contain SKU `mkp-001`. Strict binary scoring.

3. **Task T3: Second-Highest Rating Comparison**
   - **Instruction:** `"Navigate to the Audio category. Compare the customer ratings of all products. Add the product with the second-highest customer rating to your cart."`
   - **Target Entity:** `wh-002` (BudPro Wireless X, rating 4.5).
   - **Ground Truth:** `len(cart) == 1 and cart[0]['sku'] == 'wh-002'`. Strict single-item exact match.

4. **Task T4: Multi-Step Checkout Transaction**
   - **Instruction:** `"Search for 'ErgoGlide Mouse' and add it to your cart. Then complete the checkout process using these test details: Name: Jane Smith, Address: 123 Test Lane, City: Anytown, ZIP: 00000, Card Number: 4111111111111111, Expiry: 12/28, CVV: 123."`
   - **Target Entity:** `mse-001` (ErgoGlide Mouse).
   - **Ground Truth:** `window.__orderConfirmed__ == True` and order items contain `mse-001`. Scores 0.0 on failed checkout.

5. **Task T5: Cart State Mutation with Precondition Assertion**
   - **Instruction:** `"There is one item in your cart. Navigate to the cart and remove it so the cart is empty."`
   - **Precondition Assertion:** Cart must be pre-seeded with 1 item (`wh-001`). The runner strictly asserts `pre_cart_count == 1`. Initial empty carts are rejected.
   - **Ground Truth:** Post-run cart must be empty (`len(window.__cart__) == 0`).

### 4.2 Secondary Exploratory Negative Information Probe (Task T6)
- **Task T6: Manufacturer Warranty Probe**
  - **Instruction:** `"Navigate to the product details for 'SoundFlow Air 3' (SKU: wh-001). Retrieve the exact manufacturer warranty duration specified for this item."`
  - **DOM Reality:** Warranty duration is **completely absent from the website across all variants**.
  - **Outcome Definition:** Evaluated independently as an **Ungrounded Fact Refusal Probe**:
    - **Grounded Refusal ($Y_{\text{refusal}} = 1$):** Agent correctly identifies and reports that warranty information is unstated/not found on the page.
    - **Hallucinated Assertion ($Y_{\text{refusal}} = 0$):** Agent invents or guesses an ungrounded duration (e.g. asserting *"36 months"* as fact).
  - **Scientific Isolation:** Excluded from the primary grounded action benchmark to prevent rewarding hallucination or distorting task success averages.

---

## 5. Experimental Design, Randomization, and Execution Engine

### 5.1 Design Structure
- **Design:** Randomized Complete Block Design (RCBD).
- **Total Sample Size:** $N = 96$ runs ($K=4$ schedule arms $\times$ $J=6$ tasks $\times$ $R=4$ blocks).
- **Primary Analysis Sample Size:** $N_{\text{primary}} = 80$ runs (Tasks T1–T5 across 4 blocks).
  - Pooled Baseline: $n = 40$ runs ($8$ per task).
  - ARIA: $n = 20$ runs ($4$ per task).
  - DATA-CFG: $n = 20$ runs ($4$ per task).
- **Secondary Probe Sample Size:** $N_{\text{probe}} = 16$ runs (Task T6 across 4 blocks).

### 5.2 Deterministic Schedule Consumption
- The execution engine (`protocol_v3_runner.py`) consumes `proposed_randomized_schedule.csv` sequentially.
- Within-block order is randomized and fixed in advance to guarantee exact reproducibility.

### 5.3 Survivorship Bias Correction
- In historical runners, `get_completed_run_indices` filtered on `success==True`, causing failed runs to be retried on restart.
- In `protocol_v3_runner.py`, both `success=True` and `success=False` are marked as **COMPLETED**.
- Completed failed runs are **never retried**. Only fatal infrastructure crashes (e.g. HTTP 429 quota exhaustion) are eligible for resumption.

### 5.4 Post-Experiment Analysis Pipeline (`analyze_v3_results.py`)
- Automated analysis is executed via `analyze_v3_results.py`.
- **Primary Model:** Task-Stratified Cochran-Mantel-Haenszel (CMH) test across T1–T5 ($N=80$) with Bonferroni correction ($\alpha_{\text{adj}} = 0.05 / 3 = 0.0167$).
- **Effect Sizes:** Risk Differences reported with Newcombe Hybrid Score CIs and Agresti-Caffo Adjusted Wald CIs.
- **Mandatory Non-Equivalence Rule:** Because power for small effects ($\Delta \le 0.20$) is $< 20\%$ (and $< 11\%$ under task clustering), non-significant tests ($p \ge \alpha_{\text{adj}}$) cannot be claimed as channel equivalence.


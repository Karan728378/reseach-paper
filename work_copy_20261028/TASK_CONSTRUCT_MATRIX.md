# Task-to-Construct Relevance and Verifier Validity Matrix

**Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Document ID:** `TASK_CONSTRUCT_MATRIX.md`  
**Execution Context:** `C:\testing\research_execution_20261018\`  
**Date:** October 2026  
**Auditor / Roles:** Senior Browser-Agent Systems Specialist & Experimental-Design Lead  

---

## 1. Executive Summary of Task Construct Validity

In web agent benchmarking, tasks often suffer from construct conflation: a failure can occur due to navigation complexity, visual distraction, or form interaction bugs rather than the presence/absence of semantic markup.

To evaluate additive semantic markup rigorously, each task is formally mapped to its targeted construct, operational verifier mechanics, known construct limitations, and designated hierarchy (Primary Confirmatory vs. Secondary Exploratory).

---

## 2. Comprehensive Task-to-Construct Matrix

| Task ID | Task Description & Canonical Prompt | Targeted Semantic Channel | Status | Construct Validity Assessment | Verifier Method & Strict Assertions | Confounding Risks & Mitigations |
| :---: |---|---|:---:|---|---|---|
| **T1** | *"Find and add the cheapest wireless headphones to your cart."* | **Numerical Comparison (Price Sorting)**<br>Target: `wh-001` ($49.99) vs `wh-002` ($79.99), `wh-003` ($99.99) | **Primary Confirmatory** | **High Face & Construct Validity:** Directly tests whether semantic price attributes (`data-amount="49.99"` or ARIA price labels) assist in ordering/identifying the lowest-price item compared to unaugmented visible text. | **Cart State Inspection:** Programmatic check that `cart` contains SKU `wh-001`.<br>Known-pass: `wh-001`.<br>Known-fail: `wh-002`, `wh-003`, empty cart. | **Visible Text Confound:** Visible prices ($49.99) are present across all arms. Semantic markup is purely additive. |
| **T2** | *"Find the ProClick Tactile Pro mechanical keyboard and add it to cart."* | **Exact Entity Grounding (SKU Matching)**<br>Target: `mkp-001` | **Primary Confirmatory** | **High Face & Construct Validity:** Measures text/attribute entity matching when multiple products in the category share similar names. | **Cart State Inspection:** Programmatic check that `cart` contains SKU `mkp-001`.<br>Known-pass: `mkp-001`.<br>Known-fail: `mkp-002`, empty cart. | **Target Name Co-location:** Button labels in `v2-aria` do not leak `"Add ProClick to cart"`; label is deconfounded to `"Add item to cart"`. |
| **T3** | *"Compare audio product ratings and add the second-highest rated product to your cart."* | **Multi-Attribute Ranking (Rating Comparison)**<br>Target: `wh-002` (Rating: 4.5) vs `wh-001` (4.8), `wh-003` (4.2) | **Primary Confirmatory** | **High Construct Validity:** Tests compound reasoning over structured rating metadata. | **Strict Single-SKU Check:** Requires `cart` to contain exactly `wh-002` and zero other items.<br>Known-pass: `wh-002`.<br>Known-fail: `wh-001` (highest), `wh-003`, multi-item cart. | Historical defect accepted 6 SKUs. Fixed in Protocol v3/v4 to enforce exact second-highest rating. |
| **T4** | *"Add the ErgoGlide Wireless Mouse to cart and complete checkout."* | **Multi-Step Transactional Execution**<br>Target: `mse-001` + Checkout submission | **Secondary Exploratory** | **Moderate/Fragile Validity:** Tests multi-step navigation and form interaction rather than semantic markup extraction. Relies on synthetic checkout state. | **Authoritative State Check:** Requires `order_confirmed == True` AND `last_order_items` contains `mse-001`.<br>Known-pass: Confirmed order with `mse-001`.<br>Known-fail: Unconfirmed checkout (0.0 score, no partial credit). | Relies on synthetic global variable `window.__orderConfirmed__`. Does not test real credit card or payment gateway mechanics. |
| **T5** | *"Remove the item currently in your cart."* | **Pre-existing State Modification**<br>Target: Transition pre-state `count=1` to post-state `count=0` | **Secondary Exploratory** | **Moderate Validity:** Evaluates cart modification, but semantic markup on products has zero causal relevance to the cart remove action. | **Two-Tier Pre/Post State Verification:** Requires verified precondition (`pre_cart_count == 1`) and postcondition (`cart == []`).<br>Known-pass: Pre=1, Post=0.<br>Known-fail: Pre=0 (unseeded pass prevented). | Relies on client-side `localStorage` injection before agent launch. Sensitive to browser context isolation. |
| **T6** | *"What is the warranty period for the SoundFlow Air 3 headphones?"* | **Absent-Fact Calibration / Grounded Refusal**<br>Target: Correct refusal; product description omits duration | **Secondary Exploratory (Diagnostic Probe)** | **Diagnostic Construct (Epistemic Calibration):** Evaluates whether agent hallucinates absent information when metadata channels do not specify duration. | **Dual-Regex Refusal Engine:** Scores 1.0 for unambiguous refusal ("not specified", "cannot determine") and 0.0 for duration hallucination ("2 years", "12 months") or contradiction. | Brittle string matching on open-ended LLM text. Sensitive to novel phrasing. Must be analyzed separately from primary task success. |

---

## 3. Methodological Hierarchy & Stratification Rules

1. **Confirmatory Primary Hypothesis Testing ($H_1 \to H_3$):**
   - Restricted strictly to **Tasks T1, T2, and T3** ($K=3$ core semantic tasks; optionally T1–T5 for broad task-level comparison).
   - Tasks T1–T3 directly test product information channels (price, SKU, rating).
2. **Exploratory Secondary Diagnostics:**
   - **Task T4:** Evaluated as an interaction-depth probe.
   - **Task T5:** Evaluated as a state-management probe.
   - **Task T6:** Evaluated independently via binary refusal rate, isolated from composite task scores.
3. **Primary Estimand Definition:**
   - The primary outcome is Intention-to-Treat (ITT) task completion on primary tasks: $\mathbb{E}[Y_{ijk} \mid \text{Arm}]$.
   - Delivery rate $D$ is reported as a separate descriptive manipulation check, never conditioned upon in causal contrasts.

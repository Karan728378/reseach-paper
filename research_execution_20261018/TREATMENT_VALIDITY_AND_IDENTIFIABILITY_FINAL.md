# Treatment Validity & Experimental Identifiability: Final Causal Audit

**Document Version:** 1.0 (Comprehensive Causal Identifiability Audit)  
**Date:** October 22, 2026  
**Auditor:** Antigravity Scientific Methodology & Experimental Design Team  
**Compliance Status:** 100% Offline · AST Verified · De-confounded  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Executive Summary & Identifiability Framework

To draw valid causal inferences regarding whether semantic markup improves autonomous browser agent performance, the experiment must satisfy the **unit-treatment additivity and feature-isolation assumptions**:
1. **Feature Isolation:** The control and treatment conditions must differ *strictly and exclusively* in their intended semantic representation.
2. **Identifiable Delivery:** The intervention must actually survive observation serialization and reach the model prompt buffer.
3. **Absence of Co-Location Confounds:** Semantic markup must not introduce trivial target identifiers or shortcut strings that bypass hierarchical perception.

This audit evaluates all four treatment conditions, verifies AST equivalence, inspects de-confounded action labels, and defines the precise causal estimands that can be identified.

---

## 2. Experimental Arms & Implementation Details

| Arm Identifier | Nominal Alias | Variant Source Directory | Serializer Whitelist | Intended Semantic Intervention | Delivered to Prompt Buffer? | Causal Contrast Role |
|---|---|---|---|---|:---:|---|
| **`BASELINE`** | `ABS` | [`variants/v0-baseline`](file:///C:/testing/variants/v0-baseline/) | `DEFAULT_INCLUDE_ATTRIBUTES` | Plain visible HTML text; no ARIA, no custom `data-*`. | **YES** (Visible text only) | Primary Reference Control |
| **`BASELINE_REP`** | `VIS` | [`variants/v0-baseline`](file:///C:/testing/variants/v0-baseline/) | `DEFAULT_INCLUDE_ATTRIBUTES` | Identical source & prompt to `BASELINE`; within-condition control. | **YES** (Visible text only) | Temporal Stability & Drift Control |
| **`ARIA`** | `ARIA` | [`variants/v2-aria`](file:///C:/testing/variants/v2-aria/) | `DEFAULT_INCLUDE_ATTRIBUTES` | WAI-ARIA roles, states, and accessible labels on components. | **YES** (Interactive elements only) | Additive Accessibility Intervention |
| **`DATA-CFG`** | `DATA-CFG` | [`variants/v3-data-attrs`](file:///C:/testing/variants/v3-data-attrs/) | `EXTENDED_ATTRIBUTES` | Machine-readable `data-*` attributes (`data-sku`, `data-price`). | **YES** (Whitelisted interactive only) | Additive Custom Metadata Intervention |

---

## 3. Structural Equivalence Verification (AST Diff Audit)

Using the automated structural diff script [`verify_variant_diffs.py`](file:///C:/testing/research_execution_20261018/verify_variant_diffs.py), the DOM trees of all variants were parsed and normalized:

1. **`v0-baseline` vs `v2-aria`:**  
   When all `aria-*` attributes and `role` attributes are stripped from `v2-aria`, the resulting DOM tree is **100% character-for-character identical** to `v0-baseline` in:
   - Tag hierarchy and nesting order.
   - Text node strings, numbers, prices, and punctuation.
   - CSS class names and styling links (`shared/styles.css`).
   - JavaScript script tags and execution order (`products.js` followed by `app-core.js`).
2. **`v0-baseline` vs `v3-data-attrs`:**  
   When all `data-*` attributes are stripped from `v3-data-attrs`, the resulting DOM tree is **100% character-for-character identical** to `v0-baseline`.
3. **Shared Application Assets:**  
   All four variants import the exact same external assets:
   - [`shared/products.js`](file:///C:/testing/shared/products.js) (SHA-256: `b182ac6bdb6704f2c56f3718de41262aa2e9689ac2e965cae256ae1ae9278c11`)
   - [`shared/app-core.js`](file:///C:/testing/shared/app-core.js) (SHA-256: `ccae98e0218402bd78f7c4548ca743fde79b89b4baee466447b72821621b80c7`)
   - [`shared/styles.css`](file:///C:/testing/shared/styles.css) (SHA-256: `633c6f...`)
4. **Conclusion:** Control and treatment variants are perfectly balanced in visual presentation, catalog ordering, search ranking, and business logic.

---

## 4. Elimination of Target-Name Co-Location Confound

### 4.1 Historical Defect
Prior to October 21, 2026, `shared/app-core.js` rendered action buttons with product titles embedded directly inside the button's `aria-label`:
```javascript
// HISTORICAL CONVERTED CODE (DEFECTIVE):
button.setAttribute('aria-label', `Add ${product.name} to cart`);
```
- **Confound Mechanism:** On Task T1 (SoundFlow Air 3) or Task T2 (Mechanical Keyboard Pro), the agent could search the serialized prompt for the string `"SoundFlow Air 3"` and find it directly inside the clickable action tag:
  `[18] <button aria-label="Add SoundFlow Air 3 to cart">Add to Cart</button>`.
- This bypassed hierarchical comprehension, allowing the agent to succeed via simple keyword matching rather than evaluating price or navigating categories.

### 4.2 Verified Refactoring
In [`shared/app-core.js`](file:///C:/testing/shared/app-core.js), all button labels were refactored to generic semantic descriptions:
- Add to cart button: `aria-label="Add item to cart"` (Line 243)
- Quantity input: `aria-label="Item quantity"` (Line 465)
- Cart remove button: `aria-label="Remove item from cart"` (Line 530)
- Cart checkout button: `aria-label="Proceed to checkout"` (Line 537)

**Post-Refactor Hash:** `ccae98e0218402bd78f7c4548ca743fde79b89b4baee466447b72821621b80c7` (Verified).  
**Empirical Check:** In [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py), live headless prompts confirm that button tags contain `"Add item to cart"`. Product titles now appear solely in the parent card's `<h3>` heading, requiring hierarchical visual/DOM parsing across all arms.

---

## 5. Causal Identifiability & Estimand Scoping

| Contrast Pair | Nominal Question | Actual Identified Estimand | Internal Validity Status |
|---|---|---|:---:|
| **`ARIA` vs. `BASELINE`** | Does ARIA markup improve agent performance? | Causal effect of **interactive button/input ARIA semantics** on agent action accuracy when visible text is already present. | **VALID & ISOLATED** (Non-interactive ARIA is pruned by serializer). |
| **`DATA-CFG` vs. `BASELINE`** | Do custom `data-*` attributes improve agent performance? | Causal effect of **whitelisted interactive `data-*` attributes** on agent action accuracy when visible text is already present. | **VALID & ISOLATED** (Requires extended whitelist configuration). |
| **`ARIA` vs. `DATA-CFG`** | Which semantic representation is more effective? | Relative efficacy of standard accessibility semantics vs. developer metadata attributes on interactive elements. | **VALID & COMPARABLE** |
| **`BASELINE_REP` vs. `BASELINE`** | Is the evaluation stable? | Test of temporal drift, server load variance, and provider API stochasticity over execution blocks. | **VALID NEGATIVE CONTROL** |
| **`JSON-LD` vs. `BASELINE`** | Does Schema.org JSON-LD improve agent performance? | **UNIDENTIFIABLE IN DOM AGENTS:** `<script type="application/ld+json">` is 100% pruned by `browser-use`. Cannot change agent behavior. | **PROHIBITED / EXCLUDED** |

---

## 6. Treatment Validity Verdict

1. **Isolation:** **CONFIRMED.** No layout, copy, price, or ranking confounds exist between variants.
2. **De-confounding:** **CONFIRMED.** Action labels do not leak product titles.
3. **Observation Delivery:** **CONFIRMED.** Tested and delivered for interactive elements under specified whitelists.
4. **Exclusions Justified:** **CONFIRMED.** JSON-LD is correctly excluded from experimental arms due to complete serializer pruning.

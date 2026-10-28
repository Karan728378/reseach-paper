# Treatment Integrity & Information Leakage Audit

**Date:** 2026-10-25  
**Auditor:** Independent Systems & Methodology Auditor  
**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*  
**Workspace:** `C:\testing\research_execution_20261018`  
**Test Suite:** [`test_treatment_leakage_and_integrity.py`](file:///C:/testing/research_execution_20261018/test_treatment_leakage_and_integrity.py) (6 tests, 100% passing)  

---

## 1. Executive Summary

In randomized comparative evaluations of web agents, the integrity of the treatment depends on strict orthogonality:
1. The **Control Arm (\textsc{ABS})** must represent standard web markup without experimental semantic enhancements.
2. The **Semantic Arm (\textsc{ARIA})** must manipulate only standardized W3C WAI-ARIA roles, states, and properties.
3. The **Custom Attribute Arm (\textsc{DATA-CFG})** must manipulate only developer-defined `data-*` attributes.
4. **Shared Application Code & Assets** must not introduce covert side channels, target entity name leakage, or differential visual styling that could bias agent action selection.

This audit establishes that after the audited remediation in `shared/app-core.js:243`, the treatments are strictly isolated, free of target entity name co-location leakage, and evaluated by an impartial, treatment-blind programmatic verifier.

---

## 2. The Action-Label Co-Location Confound & Resolution

### 2.1 The Vulnerability in Uncontrolled Stimuli
Prior literature investigating accessibility trees frequently evaluates augmented stimuli where button accessible names are constructed by interpolating the target entity name:
```html
<!-- Confounded Stimulus -->
<button class="btn-add-cart" aria-label="Add SoundFlow Air 3 to cart">Add to Cart</button>
```
When an autonomous agent receives the instruction *"Add SoundFlow Air 3 to cart"*, it does not need to parse the surrounding card container, identify the title element, associate price and SKU, or resolve parent-child layout relationships. It simply searches the serialized text buffer for the literal substring `"SoundFlow Air 3"` and executes a click on whatever interactive control contains that string.

This introduces a fatal construct confound: the task ceases to evaluate **semantic comprehension** and degenerates into **target-string co-location and button disambiguation**.

### 2.2 Audited Remediation (`shared/app-core.js:241–255`)
In `shared/app-core.js`, line 241, button rendering was audited and standardized:
```javascript
var addBtn = document.createElement('button');
addBtn.className = 'btn-add-cart';
if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
if (F.dataAttrs) {
  addBtn.setAttribute('data-action', 'add-to-cart');
  addBtn.setAttribute('data-product-id', product.sku);
}
```
**Audit Verification:**
- In `v2-aria`, `addBtn` receives `aria-label="Add item to cart"`. The target product title (`product.name`) is strictly excluded.
- In `v3-data-attrs`, `addBtn` receives `data-action="add-to-cart"` and `data-product-id="mkp-001"`. Zero ARIA attributes are attached.
- In `v0-baseline`, `addBtn` receives only class `btn-add-cart` and inner text `Add to Cart`.
- Automated test `test_deconfounded_button_label_in_app_core` asserts:
  `self.assertNotIn("addBtn.setAttribute('aria-label', 'Add ' + product.name", self.app_core)` (PASS).

---

## 3. Comprehensive Treatment Isolation Matrix

| Evaluation Dimension | \textsc{ABS} (Control, `v0-baseline`) | \textsc{ARIA} (Semantic, `v2-aria`) | \textsc{DATA-CFG} (Custom, `v3-data-attrs`) | Cross-Arm Leakage / Confound Status |
| :--- | :--- | :--- | :--- | :---: |
| **Source HTML** | `v0-baseline/index.html` | `v2-aria/index.html` | `v3-data-attrs/index.html` | Strictly segregated folders |
| **Catalog Data** | `shared/products.js` (identical) | `shared/products.js` (identical) | `shared/products.js` (identical) | Zero catalog discrepancy |
| **Visual Styling (CSS)**| `shared/styles.css` (identical) | `shared/styles.css` (identical) | `shared/styles.css` (identical) | Zero layout or color divergence |
| **URL Hash Routes** | `#home`, `#cart`, `#checkout` | `#home`, `#cart`, `#checkout` | `#home`, `#cart`, `#checkout` | Identical routing logic |
| **Search Form** | `<input id="search-input">` | `<input id="search-input" aria-label="Search products">` | `<input id="search-input" data-field="search-query">` | Pure attribute intervention |
| **Cart Count** | `<span id="cart-count">0</span>`| `<span id="cart-count" aria-live="polite">0</span>` | `<span id="cart-count" data-counter="cart">0</span>` | Stripped at Stage 4 (non-interactive) |
| **Product Card Button** | `<button class="btn-add-cart">Add to Cart</button>` | `<button class="btn-add-cart" aria-label="Add item to cart">Add to Cart</button>` | `<button class="btn-add-cart" data-action="add-to-cart" data-product-id="...">Add to Cart</button>` | Generic label; zero target name leakage |
| **Vision Modality** | `use_vision=False` | `use_vision=False` | `use_vision=False` | Guaranteed identical text-only observation |
| **Model Parameters** | `temperature=0.0`, `max_steps=4` | `temperature=0.0`, `max_steps=4` | `temperature=0.0`, `max_steps=4` | Deterministic sampling identical across arms |

---

## 4. Verification and Scoring Impartiality

1. **Blinded Verifier Execution:**
   - Scoring is conducted by querying Chrome DevTools Protocol (CDP) runtime state: `window.__cart__`, `window.__orderConfirmed__`, and final cart SKU contents.
   - The verifier does NOT inspect the variant name or treatment arm when computing the score. It verifies whether the target product SKU (`target_sku`) was successfully added to `window.__cart__` and whether checkout completed.
2. **Exclusion of Schema.org JSON-LD from Primary Arms:**
   - Because `browser-use 0.13.10` unconditionally strips `<script>` tags via `DISABLED_ELEMENTS`, JSON-LD structured data never reaches the model observation buffer.
   - Including JSON-LD as an active empirical treatment arm would test the agent on identical baseline HTML while falsely claiming to evaluate structured data. It has been formally excluded from the primary 3-arm design.

---
*Certified by Independent Systems & Methodology Auditor.*

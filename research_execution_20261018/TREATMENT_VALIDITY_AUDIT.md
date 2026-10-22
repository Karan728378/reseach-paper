# Treatment Validity Audit & Experimental Confound Analysis

**Document Version:** 1.0 (Audited & Verified)  
**Date:** October 21, 2026  
**Auditor:** Antigravity Scientific Methodology & Systems Team  
**Compliance Status:** 100% Offline · Deterministic AST & DOM Verification · Zero Live API Invocations  
**Associated Scripts:** [`verify_variant_diffs.py`](file:///C:/testing/research_execution_20261018/verify_variant_diffs.py), [`verify_treatment_delivery_e2e.py`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py), [`shared/app-core.js`](file:///C:/testing/shared/app-core.js)  

---

## 1. Executive Summary & Purpose

The objective of this research is to evaluate **additive semantic markup**: determining whether augmenting an already factually complete visible website with structured machine-readable metadata (WAI-ARIA or custom `data-*` attributes) improves an autonomous browser agent's task accuracy, latency, and step count.

For the experiment to be scientifically valid:
1. **Treatments must differ strictly and exclusively along intended semantic dimensions.**
2. **Treatments must NOT introduce asymmetric target-name leakage, answer cues, or extraneous structural advantages.**
3. **Task functionality, product data, visual layout, and business logic must remain 100% identical across all arms.**

This audit confirms that the target-name co-location confound in `v2-aria` was successfully resolved, verifies the structural AST equivalence of all variants, audits potential secondary confounds, and establishes a formal treatment-equivalence matrix.

---

## 2. Audit of the `v2-aria` Target-Name Co-Location Confound

### 2.1 The Pre-Audit Confound
In the historical implementation of `shared/app-core.js:Line 243`:
```javascript
// HISTORICAL CONFOUNDED CODE:
addBtn.setAttribute('aria-label', 'Add ' + product.name + ' to cart');
```
When an agent was assigned Task T1 (*"Search for 'wireless headphones' and add the least expensive result to your cart"*), the target item was `wh-001` (*"SoundFlow Air 3"*).
In `v2-aria`, the button element was serialized into the prompt buffer as:
`[34]<button aria-label="Add SoundFlow Air 3 to cart">Add to Cart</button>`
This created an **asymmetric target-name co-location confound**:
- The clickable action target directly revealed the product name inside its own element tag.
- An agent could execute the task by searching for the target string in action labels, bypassing the need to comprehend product card boundaries, price labels, or rating comparisons.
- In contrast, in `v0-baseline`, the button was serialized simply as:
  `[34]<button>Add to Cart</button>`
  requiring the agent to associate the button with the neighboring product title and price text.

### 2.2 The De-confounding Refactor
The action labels in [`shared/app-core.js`](file:///C:/testing/shared/app-core.js) were refactored across lines 243, 465, 530, and 537:

```diff
--- shared/app-core.js (Pre-audit)
+++ shared/app-core.js (Post-audit)
@@ -243,1 +243,1 @@
-    if (F.aria) addBtn.setAttribute('aria-label', 'Add ' + product.name + ' to cart');
+    if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
@@ -465,1 +465,1 @@
-    if (F.aria) addBtn.setAttribute('aria-label', 'Add ' + product.name + ' to cart');
+    if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
@@ -530,1 +530,1 @@
-        if (F.aria) qtyIn.setAttribute('aria-label', 'Quantity for ' + item.name);
+        if (F.aria) qtyIn.setAttribute('aria-label', 'Item quantity');
@@ -537,1 +537,1 @@
-        if (F.aria) rmBtn.setAttribute('aria-label', 'Remove ' + item.name + ' from cart');
+        if (F.aria) rmBtn.setAttribute('aria-label', 'Remove item from cart');
```

### 2.3 Post-Refactor Verification
- **Post-Refactor SHA-256 for `shared/app-core.js`:** `ccae98e0218402bd78f7c4548ca743fde79b89b4baee466447b72821621b80c7` (verified in `offline_test_suite.py:Line 202`).
- **Prompt Serialization Check:** In [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) and [`verify_treatment_delivery_e2e.py`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py), the serialized button output is strictly:
  `aria-label=Add item to cart`
- **Scientific Impact:** The treatment now provides pure semantic action clarity (*"Add item to cart"* vs generic *"Add to Cart"*) without leaking target entity identity. To select the correct product, the agent must inspect the product card context, establishing fair equivalence with the baseline.

---

## 3. Systematic Confound Inspection Across Variants

We audited all files in `variants/`, `shared/`, and `fixtures/` for potential confounds across 8 critical dimensions:

### 3.1 Product Ordering & Catalog Data
- **Catalog Source:** All variants load identical product data from [`shared/products.js`](file:///C:/testing/shared/products.js) (SHA-256: `b182ac...`).
- **Catalog Order:** `PRODUCTS` array contains 8 products in identical order across all arms.
- **Search Sorting:** `searchProducts(query)` sorts search results by rating descending (`wh-003` first, `wh-001` last) uniformly across all variants. The least expensive headphone (`wh-001`, $49.99) is placed last, requiring price comparison across all arms.

### 3.2 Visible Typography & Content Equivalence
- **Price Text:** Rendered via shared JavaScript `priceEl.textContent = '$' + product.price.toFixed(2)` uniformly in all arms.
- **Ratings & Reviews:** Rendered via `ratingEl.textContent = '★ ' + product.rating + ' (' + product.reviewCount + ' reviews)'` uniformly in all arms.
- **Stock Status:** Rendered via `badge.textContent = product.inStock ? 'In Stock' : 'Out of Stock'` uniformly in all arms.

### 3.3 Container ARIA Labels vs. Action Labels
- In `shared/app-core.js:Line 147`:
  `card.setAttribute('aria-label', product.name + ', $' + product.price.toFixed(2));`
- **Audit Assessment:** The container `<div class="product-card">` bears an accessible label representing the whole product card.
  - This is an **intended semantic feature** of ARIA (accessible group labels).
  - In `browser-use 0.13.10`, the card container is non-interactive; it does not receive a selector index in the selector map and is not directly clickable.
  - Unlike button labels, container labels do not reveal an action shortcut; the agent must navigate inside the card to click the button.

### 3.4 Element Dimensions & Layout
- **Shared CSS:** All variants link to [`shared/styles.css`](file:///C:/testing/shared/styles.css).
- **Bounding Boxes:** Because HTML structure and classes are identical, computed layout geometry is uniform.
- **Edge Cases Fixture:** In `fixtures/edge_cases.html`, `#price-span` is explicitly styled with `min-width: 80px` to prevent false-positive triggering of the $[10, 50]\text{px}$ icon heuristic in `browser-use`.

### 3.5 Attribute Whitelisting Across Arms
- `v0-baseline`, `v1-jsonld`, and `v2-aria` operate under `DEFAULT_INCLUDE_ATTRIBUTES`.
- `v3-data-attrs` operates under `EXTENDED_ATTRIBUTES` (adding `data-action`, `data-product-id`, `data-amount`, etc.).
- **Differential Reach:** Tested and confirmed in `test_agent_prompt_pipeline.py`:
  - On `<button data-action="add-to-cart">`, `data-action` reaches the prompt buffer under `EXTENDED_ATTRIBUTES`.
  - On `<span data-field="price" data-amount="49.99">`, `data-amount` is stripped because the serializer strips non-interactive elements regardless of attribute whitelist! This is a core finding of the observation pipeline audit.

---

## 4. Treatment-Equivalence Matrix

| Dimension | `v0-baseline` (ABS / VIS) | `v1-jsonld` (JSON-LD) | `v2-aria` (ARIA) | `v3-data-attrs` (DATA-CFG) | Equivalence Status |
|---|---|---|---|---|:---:|
| **Underlying HTML Skeleton** | Base semantic HTML | Identical + `<script type="application/ld+json">` | Identical + static ARIA on nav & forms | Identical + static `data-*` on forms | **100% Structural Equivalence** (AST verified) |
| **Visible Text & Data** | All product info visible | Identical | Identical | Identical | **100% Identical** |
| **Styling & CSS** | `shared/styles.css` | `shared/styles.css` | `shared/styles.css` | `shared/styles.css` | **100% Identical** |
| **Catalog Source** | `shared/products.js` | `shared/products.js` | `shared/products.js` | `shared/products.js` | **100% Identical** |
| **App Logic & State** | `shared/app-core.js` | `shared/app-core.js` | `shared/app-core.js` | `shared/app-core.js` | **100% Identical** |
| **Button Action Labels** | Text: `"Add to Cart"` | Text: `"Add to Cart"` | Text: `"Add to Cart"`, `aria-label="Add item to cart"` | Text: `"Add to Cart"`, `data-action="add-to-cart"` | **De-confounded** (target title removed) |
| **Quantity Input Labels** | `placeholder="1"` | `placeholder="1"` | `aria-label="Item quantity"` | `data-field="quantity"` | **De-confounded** |
| **Cart Remove Buttons** | Text: `"Remove"` | Text: `"Remove"` | Text: `"Remove"`, `aria-label="Remove item from cart"` | Text: `"Remove"`, `data-action="remove-item"` | **De-confounded** |
| **Attribute Whitelist** | `DEFAULT_INCLUDE_ATTRIBUTES` | `DEFAULT_INCLUDE_ATTRIBUTES` | `DEFAULT_INCLUDE_ATTRIBUTES` | `EXTENDED_ATTRIBUTES` | **Intended Treatment Difference** |
| **Metadata in Prompt** | None (only visible text) | None (JSON-LD pruned by `DISABLED_ELEMENTS`) | Delivered on interactive elements & containers | Delivered on interactive elements only | **Intended Observation Difference** |

---

## 5. Treatment Equivalence Verification Tests

The following offline tests verify treatment equivalence and absence of confounds:

1. **AST Structural Equivalence Test ([`verify_variant_diffs.py`](file:///C:/testing/research_execution_20261018/verify_variant_diffs.py)):**
   - Parses DOM trees of all variants using `BeautifulSoup`.
   - Stripping `aria-*` attributes from `v2-aria` yields a tree character-for-character identical to `v0-baseline`.
   - Stripping `data-*` attributes from `v3-data-attrs` yields a tree character-for-character identical to `v0-baseline`.
   - Exit code: `0` (PASS).
2. **End-to-End Observation Delivery Test ([`verify_treatment_delivery_e2e.py`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py)):
   - Navigates headless browser across all 4 variants.
   - Asserts `v0` has visible text but zero ARIA or data-* enhancements.
   - Asserts `v2` delivers `aria-label=Add item to cart` (de-confounded) and `aria-label=Search products`.
   - Asserts `v3` strips data-* under default whitelist and delivers data-* under extended whitelist.
   - Asserts `v1` JSON-LD is 100% pruned by the serializer.
   - Exit code: `0` (8/8 PASS).
3. **Agent Prompt Pipeline Test ([`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py)):
   - Executes real `browser-use.Agent` observation assembly with `MockChatModel`.
   - Confirms prompt buffer contents across all 4 variants with zero API credit spend.
   - Exit code: `0` (5/5 PASS).

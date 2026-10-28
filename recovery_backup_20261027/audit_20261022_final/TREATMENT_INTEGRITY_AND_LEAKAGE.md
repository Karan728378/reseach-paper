# Treatment Integrity & Leakage Verification Report

**Document:** `audit_20261022_final/TREATMENT_INTEGRITY_AND_LEAKAGE.md`  
**Audit Date:** October 22, 2026  
**Auditor:** Antigravity Senior Research Engineer, Browser-Agent Systems Specialist & Reproducibility Lead  
**Execution Context:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9, `browser-use 0.13.10`)  

---

## 1. Experimental Arm Definitions & Contrast Specification

Protocol v4 (Option A Text-Only) evaluates additive semantic markup by strictly isolating DOM token channels while holding all other environmental, visual, functional, and model parameters constant.

| Experimental Arm | Protocol ID | Target Variant | Serializer Attribute Whitelist | Visual Screenshots (`use_vision`) | Model-Visible Treatment Contrast | Experimental Role |
|---|:---:|:---:|:---:|:---:|---|---|
| **BASELINE** | `ABS` | `v0-baseline` | `DEFAULT_INCLUDE_ATTRIBUTES` | `False` (Text-Only) | Visible typography only; standard HTML button elements without ARIA or custom data attributes. | Primary Negative Control |
| **BASELINE_REP** | `VIS` | `v0-baseline` | `DEFAULT_INCLUDE_ATTRIBUTES` | `False` (Text-Only) | Identical to `BASELINE`. Zero image input; text-only DOM. | Replicate Baseline Control (Assesses temporal stability across blocks) |
| **ARIA** | `ARIA` | `v2-aria` | `DEFAULT_INCLUDE_ATTRIBUTES` | `False` (Text-Only) | Adds WAI-ARIA `aria-label="Add item to cart"` on interactive buttons, `role="search"`, and form field accessibility. | Additive Semantic Accessibility Channel |
| **DATA-CFG** | `DATA-CFG` | `v3-data-attrs` | `EXTENDED_ATTRIBUTES` | `False` (Text-Only) | Adds developer attributes `data-action="submit-search"`, `data-action="browse-category"`, `data-product-id="wh-001"`. | Additive Developer Machine Channel |
| *JSON-LD* | *EXCLUDED* | `v1-jsonld` | `DEFAULT_INCLUDE_ATTRIBUTES` | `False` (Text-Only) | 0% reachability due to `DISABLED_ELEMENTS` pruning. | **Manipulation Failure** (Documented, excluded from live schedule) |
| *EVIDENCE-META* | *EXCLUDED* | `v4-evidence-meta` | `DEFAULT_INCLUDE_ATTRIBUTES` | `False` (Text-Only) | 0% reachability due to `<meta>` pruning. | **Manipulation Failure** (Documented, excluded from live schedule) |

---

## 2. Resolution of the Ambiguous `VIS` Arm Definition

In early draft literature (Experiment 1), the label `VIS` designated a multimodal vision arm with `use_vision=True` that sent full viewport screenshots alongside text prompts to the model.

### The Fatal Modality Confound in Multimodal Designs
If `use_vision=True` is enabled:
- In `VIS`, the LLM sees the target button and text rendered visually on screen.
- In `ARIA` and `DATA-CFG`, attributes exist only in DOM text and are invisible on screen.
- Any performance advantage in `VIS` could stem from visual spatial reasoning rather than markup differences.

### Protocol v4 Formal Resolution
Protocol v4 Option A resolves this ambiguity permanently:
1. **Strict Text-Only Enforcement:** `use_vision=False` is enforced unconditionally in `protocol_v3_runner.py:442` and `protocol_v4_config.json:35`.
2. **Re-classification of `VIS`:** `VIS` is an alias for `BASELINE_REP`. It runs on the exact same HTML variant as baseline (`v0-baseline`) under `use_vision=False`.
3. **Purpose:** Evaluates whether baseline agent accuracy drifts across temporal blocks $B_1 \to B_4$ (evaluated via Fisher's Exact stability test $p \ge 0.10$). It introduces **zero** visual confounding.

---

## 3. Target Leakage & Co-Location Audit

### 3.1 Historical Defect in `v2-aria`
- In earlier unmaintained versions, `shared/app-core.js` constructed button labels using:
  ```javascript
  addBtn.setAttribute('aria-label', 'Add ' + product.name + ' to cart');
  ```
- **The Confound:** For Task T1 (*"Search for wireless headphones and add least expensive"*), the cheapest product is `"SoundFlow Air 3"`. Stamping `"Add SoundFlow Air 3 to cart"` onto the button leaked the exact target product name to the agent before it performed any price comparisons.
- **The De-Confounding Refactor:** Updated in `shared/app-core.js:145` to:
  ```javascript
  if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
  ```
- **Result:** The button provides generic action semantics without leaking product name, SKU, or price. Verified by SHA-256 hash `ccae98e0218402bd78f7c4548ca743fde79b89b4baee466447b72821621b80c7` in `offline_test_suite.py:331`.

### 3.2 Visible Text Parity
All variants share identical product catalogs (`shared/products.js`), prices (`priceEl.textContent = '$' + product.price.toFixed(2)`), ratings, and layout geometry. The Blink Accessibility Tree generates exactly **336 nodes** on `#home` across `v0-baseline`, `v1-jsonld`, `v2-aria`, and `v3-data-attrs`.

---

## 4. Automated Test Verification
- [`test_treatment_leakage_and_integrity.py`](file:///C:/testing/research_execution_20261018/test_treatment_leakage_and_integrity.py): 6/6 tests PASS.
- [`offline_test_suite.py:test_original_files_unmodified`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L323): PASS.

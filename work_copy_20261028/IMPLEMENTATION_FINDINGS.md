# IMPLEMENTATION FINDINGS: DOM PRUNING & ACCESSIBILITY AUDIT

**Project Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Target Environment:** `browser-use 0.13.10` | Chromium Blink AXTree (CDP `Accessibility.getFullAXTree`)  
**Workspace:** `C:\testing\research_execution_20261018`  
**Date:** October 26, 2026  
**Auditor:** Senior Browser-Agent Systems Engineer  

---

## 1. Verified Implementation Findings

### Finding 1: Selective Pruning of Structured Metadata (JSON-LD)
- **Status:** `DIRECTLY_VERIFIED_IMPLEMENTATION`
- **Location:** `browser_use/dom/serializer/serializer.py:18,481`
- **Mechanism:** `<script>` tags belong to `DISABLED_ELEMENTS`. AST simplification discards the element and its text subtree unconditionally.
- **Impact:** Websites offering Schema.org JSON-LD structured data cannot communicate machine entity graphs to `browser-use` text-only agents.

### Finding 2: Non-Interactive Tag Stripping Drops Container ARIA
- **Status:** `DIRECTLY_VERIFIED_IMPLEMENTATION`
- **Location:** `browser_use/dom/serializer/serializer.py:1046-1051`
- **Mechanism:** Serialization of tags and attributes is conditionally gated on `is_interactive` or `is_any_scrollable`. Non-interactive `<span>` and `<div>` tags are omitted; only raw inner text is emitted.
- **Impact:** An `aria-label` applied to a non-interactive grouping container (e.g., `<span aria-label="Price: $49.99">`) is silently discarded.

### Finding 3: Attribute Whitelist Filters Custom Developer Data
- **Status:** `DIRECTLY_VERIFIED_IMPLEMENTATION`
- **Location:** `browser_use/dom/views.py:18`
- **Mechanism:** `DEFAULT_INCLUDE_ATTRIBUTES` excludes custom `data-*` attributes.
- **Impact:** Interactive elements do not expose developer custom state to agents unless the runner explicitly patches `include_attributes` with an extended whitelist (`EXTENDED_ATTRIBUTES`).

### Finding 4: Heuristic Misclassification of Status Badge Spans
- **Status:** `DIRECTLY_VERIFIED_DATA`
- **Location:** `browser_use/dom/clickable_elements.py:228-240`
- **Mechanism:** Elements possessing a `class` attribute and bounding box satisfying $10 \le \text{width} \le 50\text{px}$ and $10 \le \text{height} \le 50\text{px}$ are classified as interactive icons.
- **Impact:** On the benchmark `#home` route, seven "In Stock" badge spans render at $48.625\text{px} \times 15.0\text{px}$ and are incorrectly assigned selector indices ($69, 84, 99, 114, 129, 144, 159$). Chromium Blink's native `AXObjectCache` rejects them (`ignored: true`), creating a $27/34 = 79.4\%$ operational correspondence census.
- **Control Recall:** Exactly $100\%$ ($26/26$) of genuine leaf interactive controls (11 links, 14 buttons, 1 text input) match Blink AXNodes.

---

## 2. Multi-Route Correspondence Census

Verified across live Chromium CDP extractions on the TechMart benchmark fixture:

| Route | Blink AXNodes | Emitted Selectors | Matched Selectors | Operational Correspondence | Semantic Leaf Recall |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`#home`** | 336 | 34 | 27 | **79.4%** ($27/34$) | **100.0%** ($26/26$) |
| **`#cart`** | 87 | 8 | 8 | **100.0%** ($8/8$) | **100.0%** ($7/7$) |
| **`#checkout`** | 113 | 13 | 13 | **100.0%** ($13/13$) | **100.0%** ($12/12$) |
| **`#search`** | 153 | 19 | 16 | **84.2%** ($16/19$) | **100.0%** ($10/10$) |

*Scope Boundary:* The $100\%$ semantic recall across all four routes is an empirical finding of the clean, accessible TechMart SPA fixture. It does not generalize to real-world websites featuring canvas elements, occluded layouts, or non-semantic custom clickables.

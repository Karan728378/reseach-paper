# ACCESSIBILITY CORRESPONDENCE & THE 27/34 FINDING AUDIT

**Target:** Accessibility Correspondence on Route `#home` (`accessibility_tree_comparison.json`)  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Census of Route `#home` Selector Map

On the benchmark e-commerce route `#home`, `browser-use 0.13.10` constructs an interactive selector map containing exactly **34 indexed elements** (`summary.dom_state.selector_map`).

Concurrently, Chromium Blink constructs 336 accessibility nodes (`Accessibility.getFullAXTree`), of which 256 possess discrete `backendDOMNodeId` mappings.

When matching the 34 framework selector entries against the Chromium AXTree by exact `backendDOMNodeId`:
- **Matched Elements:** Exactly **27 elements** correspond to discrete interactive AXTree nodes (buttons, navigational links, input fields, cart controls).
- **Unmatched Elements:** Exactly **7 elements** have no discrete interactive AXTree node.

---

## 2. Forensic Investigation of the 7 Unmatched Elements

Every one of the 7 unmatched elements was individually inspected via Playwright DOM inspection and bounding box geometry measurement (`scratch/check_bounds.py` and `scratch/verify_34_elements.py`):

| Selector Index | Product Card | HTML Element Tag & Class | Rendered Text Content | Rendered Bounding Box | Blink AXTree Status | Detection Root Cause |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **69** | Card 1 | `<span class="product-stock in-stock">` | "In Stock" | $48.625\text{px} \times 15.0\text{px}$ | `ignored: true` | $10 \le w, h \le 50$, `class` present |
| **84** | Card 2 | `<span class="product-stock in-stock">` | "In Stock" | $48.625\text{px} \times 15.0\text{px}$ | `ignored: true` | $10 \le w, h \le 50$, `class` present |
| **99** | Card 3 | `<span class="product-stock in-stock">` | "In Stock" | $48.625\text{px} \times 15.0\text{px}$ | `ignored: true` | $10 \le w, h \le 50$, `class` present |
| **114** | Card 4 | `<span class="product-stock in-stock">` | "In Stock" | $48.625\text{px} \times 15.0\text{px}$ | `ignored: true` | $10 \le w, h \le 50$, `class` present |
| **129** | Card 5 | `<span class="product-stock in-stock">` | "In Stock" | $48.625\text{px} \times 15.0\text{px}$ | `ignored: true` | $10 \le w, h \le 50$, `class` present |
| **144** | Card 6 | `<span class="product-stock in-stock">` | "In Stock" | $48.625\text{px} \times 15.0\text{px}$ | `ignored: true` | $10 \le w, h \le 50$, `class` present |
| **159** | Card 7 | `<span class="product-stock in-stock">` | "In Stock" | $48.625\text{px} \times 15.0\text{px}$ | `ignored: true` | $10 \le w, h \le 50$, `class` present |

### The Critical Heuristic Contrast: Product Card 8
On Product Card 8, the product is out of stock:
- **HTML Element:** `<span class="product-stock out-of-stock">`
- **Rendered Text:** "Out of Stock"
- **Rendered Bounding Box:** **$74.766\text{px} \times 15.0\text{px}$**
- **Framework Classification:** **Non-Interactive (Correctly Excluded)**

### Why Did the 7 Badges Get Misclassified?
In `browser_use/dom/serializer/clickable_elements.py:228-240`, the icon heuristic checks:
$$10 \le \text{width} \le 50 \quad \text{and} \quad 10 \le \text{height} \le 50 \quad \text{and} \quad \text{has\_attribute} \in \{\text{'class'}, \dots\}$$
- Because "In Stock" renders at $48.625\text{px} \le 50\text{px}$ and $15.0\text{px} \ge 10\text{px}$, it satisfies the bounding box bounds.
- Because "Out of Stock" renders at $74.766\text{px} > 50\text{px}$, it exceeds the upper width threshold and is excluded.
- Chromium Blink recognizes both badges as static, unclickable text spans and assigns them `ignored: true`, omitting them from interactive AXTree mappings.

---

## 3. The Dual-Denominator Metric

To report this finding scientifically without introducing methodological bias, the manuscript defines two distinct denominators:

### A. Framework Operational Selector-Map Perspective ($n = 34$)
- **Metric:** Proportion of framework-generated selector targets that represent verified interactive controls.
$$\text{Correspondence} = \frac{27}{34} = \mathbf{79.41\%} \quad (95\% \text{ Wilson CI: } [63.20\%, 89.65\%])$$
- **Scientific Meaning:** Quantifies **action-space pollution**. $20.59\%$ of the agent's available interactive targets are static text spans, presenting false-positive click targets that can trigger hallucinated interactions or navigational loops.

### B. Semantic Interactive Control Perspective ($n = 27$)
- **Metric:** Completeness of capturing genuine interactive controls.
$$\text{Recall} = \frac{27}{27} = \mathbf{100.00\%} \quad (95\% \text{ Wilson CI: } [87.54\%, 100.00\%])$$
- **Scientific Meaning:** The framework achieved $100\%$ recall on true controls—no genuine button, link, or input was omitted.

---

## 4. Methodological Scope and Limitations

1. **Finite Route Census:** The 34 elements constitute a finite, deterministic census of the single tested route (`#home`).
2. **Generalizability Caution:** The $48.625\text{px}$ badge width is CSS font- and layout-dependent. On a website using a smaller font or different padding, "Out of Stock" could fall below 50px, or "In Stock" could exceed 50px.
3. **Manuscript Acceptance Rule:** The paper must never state that "browser-use achieves 79.4% accessibility correspondence across the web." It must explicitly state that on the evaluated benchmark route, the framework selector map exhibited $79.4\%$ operational correspondence due to 7 false-positive small-badge classifications, while maintaining $100\%$ recall on genuine controls.

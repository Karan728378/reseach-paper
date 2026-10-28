# REMEDIATION 03: SERIALIZER STAGE TRACE AND ARCHITECTURAL PRUNING AUDIT
## Project: The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Browser Automation and Observation Pipeline Specialist  
**Target Library:** `browser-use 0.13.10` (`C:\testing\.venv311\Lib\site-packages\browser_use\`)

---

## 1. Multi-Stage Pipeline Architecture

The transformation of web documents into agent observations follows five discrete pipeline stages:

1. **Stage 1 (Source Document):** Raw HTML markup with JSON-LD `<script>`, ARIA attributes, custom `data-*` tags, and CSS.
2. **Stage 2 (Live Blink DOM):** In-memory Chromium C++ DOM tree post-JavaScript hydration.
3. **Stage 3 (Blink Accessibility Tree):** Computed accessibility tree via CDP `Accessibility.getFullAXTree`.
4. **Stage 4 (Serialized Agent Tree):** Pruned text representation constructed by `browser-use/dom/serializer/serializer.py` via `dom_state.llm_representation()`.
5. **Stage 5 (Model Context Prompt):** Stage 4 observation concatenated with task instructions, history, and system context into the LLM prompt buffer.

---

## 2. Forensic Investigation of the Three Pruning Bottlenecks

### Bottleneck 1: Script and Meta Exclusion (JSON-LD Loss)
- **Source Location:** `browser_use/dom/serializer/serializer.py:18`
- **Mechanism:**
  ```python
  DISABLED_ELEMENTS = {
      'style', 'script', 'head', 'meta', 'link', 'title'
  }
  ```
  At line 481, any element matching `DISABLED_ELEMENTS` returns `None` immediately. Child nodes are never traversed.
- **Consequence:** Structured Schema.org metadata (`<script type="application/ld+json">`) is purged at Stage 4.
- **Verification Evidence:** `test_observation_pipeline_stages.py:test_jsonld_pruned` executes a headless Chromium session on a JSON-LD fixture and verifies that zero JSON-LD key-value pairs appear in Stage 4.

### Bottleneck 2: Tag Stripping and Container ARIA Loss
- **Source Location:** `browser_use/dom/serializer/serializer.py:1046-1051`
- **Mechanism:**
  ```python
  if (node.is_interactive
          or is_any_scrollable
          or tag == 'IFRAME'
          or tag == 'FRAME'):
      attributes_html_str = _build_attributes_string(
          node.original_node, include_attributes, ...)
  ```
- **Consequence:** For non-interactive elements (e.g., `<span>`, `<div>` without click handlers), `_build_attributes_string` is bypassed entirely. The opening/closing tags and all attributes—including any `aria-label`—are discarded. Only inner text is emitted.
- **Live Empirical Trace:** Navigating to `fixtures/disambiguation_probe_b.html` containing:
  ```html
  <span class="badge" aria-label="Identity: target-sku-101">Product Badge</span>
  ```
  Stage 4 output contained only `Product Badge`. The attribute `aria-label="Identity: target-sku-101"` was dropped.
- **Scope Limitation:** The claim applies strictly to Stage 4. Stage 5 prompt assembly was not intercepted during cloud execution.

### Bottleneck 3: Attribute Whitelist Filtering
- **Source Location:** `browser_use/dom/views.py:DEFAULT_INCLUDE_ATTRIBUTES` and `serializer.py:1211`
- **Mechanism:** `DEFAULT_INCLUDE_ATTRIBUTES` includes standard accessibility keys (`role`, `aria-label`, `aria-expanded`) but omits custom developer keys (`data-product-id`, `data-action`).
- **Interaction with Bottleneck 2:** Supplying `EXTENDED_ATTRIBUTES` successfully retains `data-product-id` on interactive controls (buttons, links), but FAILS to rescue custom attributes on container spans because Bottleneck 2 discards the entire tag before attribute filtering occurs.

---

## 3. Icon Bounding-Box Heuristic Misclassification

- **Mechanism:** In `serializer.py`, elements with small bounding boxes are subjected to heuristic icon classification. Elements falling within dimensions of $10\text{--}50\text{px}$ are tagged as icons.
- **Observation:** On the TechMart fixture (`#home`), 7 'In Stock' badge spans have bounding boxes of $48.6 \times 15\text{px}$. Because width and height fall near the heuristic boundary, they are flagged as interactive icons in `selector_map`, despite being non-interactive badges.
- **AXTree Discrepancy:** The native Chromium AXTree ignores these spans. This explains the 7-element divergence between the 34 selector targets and the 27 AXTree matches ($27/34 = 79.4\%$).

# OBSERVATION PIPELINE AUDIT: DOM EXTRACTION, FILTERING, SERIALIZATION & PROMPT BUFFER TRACE (PHASE 3)

**Target Framework:** `browser-use 0.13.10` (installed in `.venv311`)  
**Longitudinal Scope:** Audited across 6 PyPI binary wheel releases (v0.1.0 to v0.13.11)  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Execution Environment:** Chromium CDP (`Accessibility.getFullAXTree`, `DOM.getDocument`), Python 3.11  
**Audit Date:** 2026-10-27  

---

## 1. The Five Discrete Observation Pipeline Stages

The client-side observation pipeline converts live in-memory browser layout state into an LLM prompt buffer across five distinct architectural stages:

```
[ Stage 1: Server HTML Payload ]
               │
               ▼  (Blink Parser & Tree Build)
[ Stage 2: In-Memory Cleaned DOM AST ] ── Pruning Mechanism 1: DISABLED_ELEMENTS
               │
               ▼  (ClickableElementDetector + AXTree + Geometry)
[ Stage 3: Interactive Candidate Set ] ── Confound 1: AXTree Circularity
               │                        ── Confound 2: 10-50px Icon Heuristic
               ▼  (DOMTreeSerializer.serialize())
[ Stage 4: Serialized Observation String ] ── Pruning Mechanism 2: Interactivity Gate (L1046)
               │                           ── Pruning Mechanism 3: Attribute Whitelist
               ▼  (Agent Prompt Assembly)
[ Stage 5: Model Context Buffer ] ── Ingested by LLM
```

---

## 2. Forensic Analysis of the Three Deterministic Pruning Mechanisms

### 2.1 Pruning Mechanism 1: Element-Level Exclusion (Stage 2)
- **Source Location:** `browser_use/dom/serializer/serializer.py` (L18, applied at L481).
- **Installed Code:**
  ```python
  DISABLED_ELEMENTS = {
      'style', 'script', 'head', 'meta', 'link', 'title'
  }
  ```
- **Execution Logic:** During Stage 2 recursive traversal (`_build_dom_tree`), any DOM node whose tag name is in `DISABLED_ELEMENTS` is pruned from the tree before child nodes are visited.
- **Empirical Impact:**
  - Structured linked data in `<script type="application/ld+json">` is unconditionally eliminated at Stage 2.
  - OpenGraph, Dublin Core, and product metadata in `<meta>` tags are unconditionally eliminated at Stage 2.
  - **Critical Finding:** Because elimination occurs at Stage 2, **no attribute whitelist, configuration flag, or prompt instruction can resurrect JSON-LD metadata** in `browser-use 0.13.10`. It is 100% inaccessible to text-serialized prompts.
- **Longitudinal Audit:** Verified across all 6 downloaded PyPI binary wheels (v0.1.0, v0.5.0, v0.13.0, v0.13.5, v0.13.10, v0.13.11). `DISABLED_ELEMENTS` containing `script` and `meta` is an **immutable architectural invariant** throughout the project lifecycle.

### 2.2 Pruning Mechanism 2: Interactivity-Gated Tag Emission (Stage 4)
- **Source Location:** `browser_use/dom/serializer/serializer.py` (L1046–L1051).
- **Installed Code:**
  ```python
  if (node.is_interactive
          or is_any_scrollable
          or tag == 'IFRAME'
          or tag == 'FRAME'):
      attributes_html_str = _build_attributes_string(
          node.original_node, include_attributes, ...)
  ```
- **Execution Logic:** For any element not deemed interactive or scrollable, `_build_attributes_string()` is bypassed entirely. The serializer discards the opening/closing HTML tag and all attributes, emitting only the inner text.
- **Empirical Impact:**
  - Semantic container markup on non-interactive elements (e.g., `<span role="region" aria-label="Identity: target-sku-101">` in Disambiguation Probe B) has its tag wrapper and attributes stripped. Only the inner text is emitted.
  - Under W3C WAI-ARIA 1.2, `role="region"` is a valid landmark role supporting accessible naming (`accname-1.1`). However, because `browser-use` gates tag emission strictly on operational interactivity (clickability/scrollability), landmark naming on container elements is completely discarded.
  - This causes total task unsolvability ($p=0.5$, random guessing) in Disambiguation Probe B under all experimental arms.

### 2.3 Pruning Mechanism 3: Attribute Whitelist Filtering (Stage 4)
- **Source Location:** `browser_use/dom/views.py` (L18, referenced in `serializer.py` L1214).
- **Installed Code:**
  ```python
  DEFAULT_INCLUDE_ATTRIBUTES = [
      'title', 'type', 'name', 'role', 'tabindex', 'aria-label',
      'placeholder', 'value', 'alt', 'aria-expanded', 'aria-checked',
      'data-state', 'data-date-format', 'data-mask', 'data-inputmask', 'data-datepicker'
  ]
  ```
- **Execution Logic:** Even if an element survives interactivity gating, its emitted attributes are filtered against `include_attributes`.
- **Empirical Impact:**
  - Standard attributes (`role`, `aria-label`, `title`) are retained on interactive elements.
  - Developer-defined custom attributes (`data-product-id`, `data-action`, `data-warranty`, `data-category`) are excluded by default.
  - Developer attributes reach Stage 4 only if an extended attribute whitelist (`EXTENDED_ATTRIBUTES` in `protocol_v3_runner.py` / `DATA-CFG` arm) is explicitly supplied to the runner.

---

## 3. Direct Information Loss Measurement across 44 Target Entities

Evaluated across 7 controlled test fixtures using `phase9_execute.py` with exact Clopper-Pearson 95% binomial confidence intervals (`INFORMATION_LOSS_MEASUREMENTS.csv`):

| Metadata Channel | Sample Size ($N$) | Stage 1 (HTML) | Stage 2 (Clean DOM) | Stage 3 (Candidates) | Stage 4 (Serialized) | Stage 5 (Prompt) | Exact 95% CI | Primary Loss Mechanism |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Schema.org JSON-LD** | 4 | 4/4 | **0/4** | 0/4 | 0/4 | **0/4 (0.0%)** | $[0.000, 0.602]$ | Element Pruning (`DISABLED_ELEMENTS`) |
| **HTML `<meta>` Tags** | 2 | 2/2 | **0/2** | 0/2 | 0/2 | **0/2 (0.0%)** | $[0.000, 0.842]$ | Element Pruning (`DISABLED_ELEMENTS`) |
| **Developer `data-*` (Default)**| 6 | 6/6 | 6/6 | 4/6 | **0/6** | **0/6 (0.0%)** | $[0.000, 0.459]$ | Attribute Whitelisting (`views.py`) |
| **Container ARIA (`<span>`/`<div>`)**| 16 | 16/16 | 16/16 | 5/16 | 5/16 | **5/16 (31.2%)** | $[0.110, 0.587]$ | Interactivity Gating (L1046) |
| **Landmark ARIA (`role="region"`)**| 1 | 1/1 | 1/1 | **0/1** | 0/1 | **0/1 (0.0%)** | $[0.000, 0.975]$ | Interactivity Gating (L1046) |
| **Developer `data-*` (Extended)**| 6 | 6/6 | 6/6 | 4/6 | 4/6 | **4/6 (66.7%)** | $[0.223, 0.957]$ | Container Tag Stripping |
| **Interactive Button ARIA** | 3 | 3/3 | 3/3 | 3/3 | 3/3 | **3/3 (100.0%)** | $[0.292, 1.000]$ | Fully Retained (Leaf Control) |
| **Visible Rendered Typography** | 10 | 10/10 | 10/10 | 10/10 | 10/10 | **10/10 (100.0%)**| $[0.692, 1.000]$ | Fully Retained (Leaf Control) |

---

## 4. Observation Confounds & Measurement Circularity

### 4.1 Circularity in Accessibility Tree Correspondence
- **Audited Component:** `browser_use/dom/serializer/clickable_elements.py` (L204–L225).
- **Mechanism:** `ClickableElementDetector` calls CDP `Accessibility.getFullAXTree` and directly inspects `node.ax_node.role` against a hardcoded set of interactive roles (`button`, `link`, `menuitem`, `checkbox`).
- **Confound:** When benchmark researchers report that "the agent's selector map has 79.4% correspondence with the browser's accessibility tree", this correspondence is **partially circular by construction**: the serializer queries the AXTree to decide which elements to emit as interactive selectors.

### 4.2 The Geometric Bounding-Box Heuristic Confound
- **Audited Heuristic:** Any element bearing a CSS `class` attribute with computed dimensions satisfying:
  $$10.0\text{ px} \le \text{width} \le 50.0\text{ px} \quad \text{and} \quad 10.0\text{ px} \le \text{height} \le 50.0\text{ px}$$
  is classified as an interactive icon button.
- **Catalog Route (`#home`) Census:**
  - True leaf interactive controls: **26 elements** (11 links, 14 buttons, 1 text input).
  - Native Blink AXTree leaf match rate: **26 / 26 = 100.0%** (Semantic Recall).
  - Container form elements: 1 form matched (27 container-inclusive matches).
  - **Heuristic False Positives:** Exactly **7 static "In Stock" text badge spans** ($48.625 \times 15.0$\,px) satisfy the $10\text{--}50$\,px heuristic and are emitted as clickable buttons.
  - Conversely, an adjacent **"Out of Stock" badge span** ($74.766 \times 15.0$\,px) exceeds the 50px width ceiling and is pruned.
  - **Resulting Metric:** Operational correspondence is $27 / 34 = \mathbf{79.4\%}$ (Wilson 95% CI $[63.2\%, 89.7\%]$). The apparent retention of container ARIA in Table II ($5/16$) is entirely driven by this geometric misclassification.

### 4.3 Action-Label Co-Location Confound
- **Mechanism:** On standard e-commerce pages, product cards contain rendered typography ("SoundFlow Air 3", "$79.99") and generic button text ("Add to Cart").
- **Confound:** Adding `aria-label="Add SoundFlow Air 3 to cart"` directly to the button converts a multi-node spatial reference task (matching product title to button position) into trivial single-node string matching.
- **Factorial Resolution:** We formalize a $3 \times 3$ factorial design crossing Content Placement ($A_1$: text only, $A_2$: attribute only, $A_3$: co-located) with Channel ($B_1$: visible typography, $B_2$: WAI-ARIA, $B_3$: developer `data-*`). Scripted oracle testing proves that causal contrast occurs only in cell $(A_2, B_3)$, where visible text is generic and attribute delivery is isolated.

---

## 5. Machine-Readable Trace & Regression Test Manifest

- **Automated Regression Tests:**
  - `test_observation_pipeline_stages.py` (5/5 PASS)
  - `test_implementation_fixes.py` (6/6 PASS)
  - `test_disambiguation_probes.py` (7/7 PASS)
  - `test_phase9_strengthening.py` (4/4 PASS)
  - `test_forensic_audit_regressions.py` (12/12 PASS)
- **Machine-Readable Traces:**
  - `INFORMATION_LOSS_MEASUREMENTS.csv` (SHA-256: `519bac28...`)
  - `STAGE_TRACE_RAW/STAGE_TRACE_MANIFEST.json`
  - `sentinel_stage_trace.json`
  - `accessibility_tree_comparison.json`

---

## 6. Phase 3 Sign-Off

The DOM serialization pipeline from server HTML payload to model context buffer is 100% audited, reproduced offline, and mapped to exact code line numbers in the installed distribution.

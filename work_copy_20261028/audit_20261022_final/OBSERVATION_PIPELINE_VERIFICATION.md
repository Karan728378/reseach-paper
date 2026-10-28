# Observation Pipeline Verification: 6-Stage Information Lifecycle Audit

**Document:** `audit_20261022_final/OBSERVATION_PIPELINE_VERIFICATION.md`  
**Audit Date:** October 22, 2026  
**Auditor:** Antigravity Senior Research Engineer, Browser-Agent Systems Specialist & Reproducibility Lead  
**Execution Context:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9, `browser-use 0.13.10`)  

---

## 1. Executive Summary: The DOM Serialization Gap

A foundational flaw in prior web agent research is treating the Document Object Model (DOM) as monolithic and directly accessible to the agent's LLM. In reality, modern browser agents observe web pages through a multi-stage observation and serialization pipeline:

$$\text{Source HTML} \longrightarrow \text{Live Client DOM} \longrightarrow \text{Browser AXTree} \longrightarrow \text{Framework Serializer} \longrightarrow \text{LLM Prompt Buffer}$$

At each transition, information can be dropped, filtered, or transformed. This audit traces the complete 6-stage lifecycle of each semantic channel under `browser-use==0.13.10`.

---

## 2. Six-Stage Lifecycle Matrix Across Channels

| Channel / Representation | Stage 1: Source HTML | Stage 2: Live Client DOM | Stage 3: Chromium AXTree | Stage 4: Framework Serializer | Stage 5: Final Model Prompt | Stage 6: Distinguishable from Baseline? | Verdict & Theoretical Classification |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1. Schema.org JSON-LD** (`<script type="application/ld+json">`) | **Present** (Static header schema in `v1-jsonld`) | **Present** (Static block + dynamic `id="dynamic-jsonld"`) | **Absent (0%)** (Excluded by Blink AXTree builder) | **Pruned (0%)** (`DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}`) | **Absent (0%)** (0% token reachability) | **NO** (Identical to baseline) | **CONCORDANT LOSS** (Complete loss in both AXTree and prompt; manipulation failure under standard agents) |
| **2. Button Accessible Names** (`<button aria-label="Add item to cart">`) | **Present** (Form/nav buttons) | **Present** (Injected by `app-core.js`) | **Retained (100%)** (Blink computes accessible name) | **Retained (100%)** (Interactive element + whitelisted `aria-label`) | **Present (100%)** (`aria-label="Add item to cart"`) | **YES** (Baseline has plain button text) | **CONCORDANT RETENTION** (Survives all stages; valid semantic treatment contrast) |
| **3. Non-Interactive ARIA** (`<span aria-label="Price: $49.99">`) | **Present** (`v2-aria`) | **Present** (DOM span attribute) | **Retained (100%)** (Blink builds accessible name `"Price: $49.99"`) | **Stripped (0%)** (`serializer.py:1046-1058` strips non-interactive attributes) | **Absent (0%)** (Emits only visible text `"$49.99"`) | **NO** (Identical to baseline typography) | **CRITICAL DIVERGENCE** (Retained in AXTree, but stripped by LLM serializer; AXTree $\neq$ prompt) |
| **4. Custom `data-*` (Default Whitelist)** (`<button data-action="add-to-cart">`) | **Present** (`v3-data-attrs`) | **Present** (DOM button attribute) | **Absent (0%)** (Not part of W3C accessibility semantics) | **Stripped (0%)** (`DEFAULT_INCLUDE_ATTRIBUTES` excludes custom `data-*`) | **Absent (0%)** (Attribute stripped) | **NO** (Identical to baseline button) | **CONCORDANT LOSS** (Stripped under default framework configuration) |
| **5. Custom `data-*` (Extended Whitelist)** (`<button data-action="add-to-cart">`) | **Present** (`v3-data-attrs`) | **Present** (DOM button attribute) | **Absent (0%)** (Not part of W3C accessibility semantics) | **Retained (100%)** (`EXTENDED_ATTRIBUTES` in `protocol_v3_runner.py`) | **Present (100%)** (`data-action="add-to-cart"`, `data-product-id="wh-001"`) | **YES** (Baseline lacks custom `data-*`) | **REVERSED DIVERGENCE** (Absent in AXTree, but delivered to prompt under configured whitelist) |
| **6. Non-Interactive `data-*`** (`<span data-amount="49.99">`) | **Present** (`v3-data-attrs`) | **Present** (DOM span attribute) | **Absent (0%)** (Blink AXTree ignores custom attributes) | **Stripped (0%)** (`serializer.py:1046` strips non-interactive wrappers) | **Absent (0%)** (Emits only text child `"$49.99"`) | **NO** (Identical to baseline typography) | **INTERACTIVE-ONLY BOUNDARY** (Extended whitelist only rescues interactive elements) |
| **7. Visible Typography** (`<p>SoundFlow Air 3</p>`) | **Present** (All variants) | **Present** (All variants) | **Retained (100%)** (StaticText nodes) | **Retained (100%)** (Serialized as visible string) | **Present (100%)** (Visible in prompt message) | **NO** (Shared control variable across all arms) | **CONCORDANT CONTROL** (100% stable baseline across all variants) |

---

## 3. Critical Architectural Discoveries in `browser-use 0.13.10`

### 3.1 Hardcoded Pruning via `DISABLED_ELEMENTS`
- **Source:** [`browser_use/dom/serializer/serializer.py:Line 18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18)
  ```python
  DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
  ```
- **Behavior:** Any HTML element whose tag name appears in `DISABLED_ELEMENTS` is pruned unconditionally during tree parsing before DOM serialization occurs.
- **Scientific Consequence:** Search-engine structured data (Schema.org JSON-LD inside `<script type="application/ld+json">`) and temporal metadata (`<meta name="data-freshness">`) **never enter the agent observation buffer under standard frameworks**. Evaluating JSON-LD on autonomous browser agents without modifying the serializer tests only fact absence.

### 3.2 Non-Interactive Element Attribute Stripping
- **Source:** [`browser_use/dom/serializer/serializer.py:Lines 1046–1058`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1046-L1058)
  ```python
  if (
      node.is_interactive
      or is_any_scrollable
      or node.original_node.tag_name.upper() == 'IFRAME'
      or node.original_node.tag_name.upper() == 'FRAME'
  ):
      # Emits HTML tag, attributes, and selector index
  else:
      # Non-interactive element: discards tag and attributes; appends ONLY raw text children
  ```
- **Behavior:** Attributes on `<span>`, `<div>`, `<section>`, `<article>`, and `<p>` elements are stripped unconditionally unless the element happens to be clickable or scrollable.
- **Scientific Consequence:** While the Chromium Accessibility Tree preserves `aria-label` on non-interactive price and rating spans (`Price: $49.99`), `browser-use` strips the attribute and emits only the text child `"$49.99"`. Researchers cannot assume that an attribute exposed to a screen reader reaches an LLM prompt.

### 3.3 Attribute Whitelisting and Extended Configuration
- **Source:** [`browser_use/dom/views.py:Lines 18–45`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/views.py#L18-L45)
  `DEFAULT_INCLUDE_ATTRIBUTES = ['title', 'type', 'id', 'name', 'role', 'aria-label', ...]`
- **Behavior:** By default, custom attributes (`data-action`, `data-product-id`, `data-category-slug`) are excluded from serialization.
- **Resolution in Protocol v4:** [`protocol_v3_runner.py:46-50`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L46) supplies `EXTENDED_ATTRIBUTES` to the `Agent` constructor for the `DATA-CFG` arm, ensuring custom attributes on interactive elements survive serialization and reach the prompt.

---

## 4. Test Evidence Summary
- [`test_observation_pipeline_stages.py`](file:///C:/testing/research_execution_20261018/test_observation_pipeline_stages.py) (5/5 tests PASS).
- [`test_accessibility_tree_comparison.py`](file:///C:/testing/research_execution_20261018/test_accessibility_tree_comparison.py) (10/10 tests PASS).
- [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) (5/5 tests PASS).

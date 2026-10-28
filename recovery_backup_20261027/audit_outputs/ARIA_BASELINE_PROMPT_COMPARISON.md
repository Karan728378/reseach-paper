# Audit Report: ARIA vs. Baseline Prompt Comparison & Pipeline Trace

**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*  
**Date:** 2026-10-24  
**Audit Status:** Case 1 — Meaningful Difference Verified (with Systems Qualification)  
**Execution Environment:** Local deterministic execution, zero external API calls, zero cost  

---

## 1. Executive Summary

A critical peer-review question was whether the ARIA treatment arm (`v2-aria`) produces agent-facing serialized observation prompts that are genuinely distinguishable from the baseline control arm (`v0-baseline`) under text-only mode (`use_vision=False`).

Through deterministic end-to-end execution of the real `browser-use` prompt generation pipeline across all 6 benchmark tasks (T1–T6) and a dedicated DOM edge-cases fixture, this audit confirms:

1. **Prompt Divergence is Verified (Case 1):** In 100% of tested pairs (7/7), raw and normalized SHA-256 hashes between `v0-baseline` and `v2-aria` prompts are non-identical. Unified diffs reveal between 16 and 106 modified lines per task.
2. **Interactive Semantic Retention:** Interactive elements (buttons, form inputs, search containers) successfully retain ARIA attributes into the agent's input prompt buffer:
   - `<button aria-label="Add item to cart">` (vs `<button>` in baseline)
   - `<input id="search-input" aria-label="Search products" ...>` (vs no aria-label in baseline)
   - `<button id="search-submit-btn" aria-label="Search">` (vs no aria-label in baseline)
   - `<form id="search-form" role="search">` (vs `<form id="search-form">` in baseline)
3. **Deterministic Non-Interactive Pruning (The Systems Finding):** Non-interactive ARIA semantics present in source HTML (such as `<span class="product-price" aria-label="Price: $49.99">` and `<span class="product-rating" role="img" aria-label="Rating: 4.5 out of 5 stars">`) are **100% pruned** by `DOMTreeSerializer` (line 1046). They do not reach the agent prompt in either condition.
4. **Methodological Implication:** The ARIA treatment does produce distinct prompts, but the surviving differences on buttons are **generic action triggers** that duplicate visible typography (`Add to Cart`), while substantive factual metadata channels are purged by the serializer.

---

## 2. Complete Prompt Pipeline Trace

The prompt pipeline was traced step-by-step from variant selection to the final LLM input message:

```
[Web Application Source HTML / JS]
    │  (Variants: v0-baseline vs v2-aria)
    ▼
[Chromium CDP Session (Page / DOM)]
    │  (DOM tree rendered with dynamic JavaScript in shared/app-core.js)
    ▼
[buildDomTree.js (browser_use/dom/buildDomTree.js)]
    │  Traverses live DOM, builds custom JSON representation of interactive
    │  and visible DOM elements. Extracts attributes defined in include_attributes.
    ▼
[DOMTreeSerializer (browser_use/dom/serializer/serializer.py)]
    │  Filters elements. Lines 1046–1058: Only interactive elements (or elements with
    │  visible text) are serialized into markdown-like representation.
    │  Non-interactive container ARIA labels (div, span) are stripped unless they
    │  possess direct interactive roles or click handlers.
    ▼
[BrowserState (browser_use/browser/views.py)]
    │  Wraps serialized DOM string into `BrowserStateSummary` and `DOMState`.
    ▼
[MessageManager (browser_use/agent/message_manager/service.py)]
    │  `create_state_messages()` constructs `HumanMessage` / user turn containing
    │  `<browser_state>` and `<page_stats>`.
    ▼
[Final Model Prompt Buffer (LangChain BaseMessage list)]
    │  Passed directly to `ChatModel.ainvoke()` / `invoke()`.
```

### Exact Code Paths and Functions:
- **Variant Navigation:** `browser_use.Agent.initial_actions` navigates to `http://127.0.0.1:8098/variants/{v0-baseline|v2-aria}/index.html#home`.
- **DOM Extraction:** `browser_use.dom.service.DomService.get_clickable_elements()` executes `buildDomTree.js` via CDP `Runtime.evaluate`.
- **Attribute Filtering:** `browser_use.dom.views.DEFAULT_INCLUDE_ATTRIBUTES` includes `["title", "type", "name", "role", "aria-label", "placeholder", "value", "alt", "aria-expanded", "aria-checked"]`.
- **Serialization:** `browser_use.dom.serializer.serializer.DOMTreeSerializer.serialize()` renders interactive elements with brackets `[ID]<tag ...>` and indents child nodes.
- **Message Assembly:** `browser_use.agent.message_manager.service.MessageManager.create_state_messages()` appends the serialized string within `<browser_state>`.

---

## 3. Quantitative Comparison of Prompt Pairs

All 7 paired task observations were captured locally using `browser-use` 0.13.10 and `langchain_core.language_models.FakeListChatModel`.

### Normalization Protocol:
To prevent spurious non-deterministic mismatches, the following demonstrably irrelevant fields were normalized:
1. Local HTTP server port numbers (`127.0.0.1:\d+` -> `127.0.0.1:PORT`).
2. BrowserSession UUIDs and CDP target IDs (`targetId=[0-9A-Fa-f\-]+` -> `targetId=TARGET_ID`).
3. Line endings (`\r\n` -> `\n`).

No semantic, structural, or attribute content was normalized or altered.

### Paired Comparison Table:

| Pair ID | Task ID | Description | v0 Norm Hash (SHA-256) | v2 Norm Hash (SHA-256) | Identical? | Diff Lines | ARIA Attr Diff? | Length Diff (chars) |
|---|---|---|---|---|---|---|---|---|
| `pair_01` | T1 | Search / Home | `29dd025e...` | `05af9275...` | **False** | 30 | Yes (`aria-label`) | +273 |
| `pair_02` | T2 | Keyboard Pro | `3571d454...` | `0d254237...` | **False** | 106 | Yes (`aria-label`) | +273 |
| `pair_03` | T3 | Audio Category | `52ed0efd...` | `59284c81...` | **False** | 46 | Yes (`aria-label`) | +273 |
| `pair_04` | T4 | Checkout Flow | `6350977e...` | `3e9056a3...` | **False** | 38 | Yes (`aria-label`) | +273 |
| `pair_05` | T5 | Cart Removal | `95c5231f...` | `ed854c1b...` | **False** | 24 | Yes (`aria-label`) | +107 |
| `pair_06` | T6 | Warranty Probe | `832099ad...` | `081d8fe3...` | **False** | 30 | Yes (`aria-label`) | +273 |
| `pair_07` | EDGE | Edge Cases Fixture | `6443458e...` | `2b1fffc3...` | **False** | 16 | Yes (`role`, `aria-label`) | 0 (equalized) |

*Full machine-readable records: `audit_outputs/aria_baseline_prompt_pairs.csv`*

---

## 4. Inspection of Unified Diffs

Detailed unified diff files for all 7 pairs are preserved in `audit_outputs/aria_baseline_prompt_diffs/`.

### Excerpt from Pair 02 (Task T2: Mechanical Keyboard Pro):
```diff
--- BASELINE_pair_02_t2_product_home
+++ ARIA_pair_02_t2_product_home
@@ -298,9 +298,9 @@
 Interactive elements:
 [Start of page]
-[3]<form id=search-form />
-	|SHADOW(open)|[4]<input type=text id=search-input placeholder=Search products... autocomplete=off />
-	[13]<button type=submit id=search-submit-btn />
+[5]<form id=search-form role=search />
+	|SHADOW(open)|[6]<input type=text id=search-input placeholder=Search products... autocomplete=off aria-label=Search products />
+	[15]<button type=submit id=search-submit-btn aria-label=Search />
 		Search
@@ -333,7 +333,7 @@
-[28]<button />
+[30]<button aria-label=Add item to cart />
 	Add to Cart
```

### Critical Observations from Diffs:
1. **Interactive Attributes Reach Prompt:** In the ARIA condition, `<button>` receives `aria-label=Add item to cart`, the form receives `role=search`, and the search input receives `aria-label=Search products`. These survive all downstream formatting.
2. **Non-Interactive ARIA Stripped:** Source HTML in `v2-aria` includes `<span class="product-price" aria-label="Price: $49.99">` and `<span class="product-rating" role="img" aria-label="Rating: 4.5 out of 5 stars">`. Neither attribute appears in either column of the diff. Both baseline and ARIA prompts display only the text nodes: `$49.99` and `★ 4.8 (2156 reviews)`.
3. **No Target-Leaking Confound:** The button ARIA label is generic (`Add item to cart`), not product-specific (`Add SoundFlow Air 3 to cart`). It does not leak task target identity.

---

## 5. Regression Testing Verification

A dedicated regression test module was created and executed locally:
- **Test File:** `test_aria_baseline_prompt_divergence.py`
- **Command:** `C:\testing\.venv311\Scripts\python.exe -m unittest test_aria_baseline_prompt_divergence.py -v`
- **Exit Status:** `0` (SUCCESS)
- **Tests Passed:**
  1. `test_all_seven_pairs_diverge_in_raw_and_normalized_hashes`: PASS
  2. `test_interactive_aria_retention_in_prompt_diffs`: PASS
  3. `test_non_interactive_aria_pruning_in_prompts`: PASS
  4. `test_edge_cases_fixture_divergence`: PASS
  5. `test_treatment_character_length_expansion`: PASS

---

## 6. Scientific Verdict and Manuscript Recommendations

**Decision: Case 1 — Meaningful Difference Verified (with Architectural Pruning Boundary)**

- **Claim Justification:** The manuscript's claim that ARIA provides distinct serialized representations is **empirically supported** for interactive elements. The manipulation check passes.
- **Essential Qualification for Manuscript:** The paper must not claim that *all* ARIA semantics reach the agent. The text must explicitly distinguish between:
  - **Interactive ARIA (retained):** Accessible names and roles on action triggers (`button`, `input`, `form`).
  - **Non-interactive ARIA (pruned):** Informational ARIA on data containers (`span`, `div`), which is discarded by the DOM serialization gap.

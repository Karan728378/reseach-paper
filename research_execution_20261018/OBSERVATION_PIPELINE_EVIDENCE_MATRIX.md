# Observation-Pipeline Evidence Matrix & Architectural Boundary Audit

**Document Version:** 1.0 (Audited & Verified)  
**Date:** October 21, 2026  
**Auditor:** Antigravity Scientific Methodology & Systems Team  
**Compliance Status:** 100% Offline · Chromium CDP Inspection · Zero Live API Invocations  
**Associated Scripts:** [`compare_accessibility_tree.py`](file:///C:/testing/research_execution_20261018/compare_accessibility_tree.py), [`accessibility_tree_comparison.json`](file:///C:/testing/research_execution_20261018/accessibility_tree_comparison.json), [`ACCESSIBILITY_TREE_COMPARISON.md`](file:///C:/testing/research_execution_20261018/ACCESSIBILITY_TREE_COMPARISON.md), [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py)  

---

## 1. Executive Summary & Purpose

The central empirical question of this research is:
> **What semantic information actually survives each successive transformation stage in an autonomous browser agent's observation pipeline?**

Prior literature and historical experiment designs frequently conflated:
1. *Source presence* with *agent observability* (assuming that because a tag exists in HTML, the LLM receives it).
2. *Accessibility tree presence* with *serialized prompt inclusion* (assuming `browser-use` DOM pruning is isomorphic to Chromium's AXTree).
3. *DOM serializer pruning* with *universal agent inaccessibility* (overlooking direct JavaScript evaluation or raw source extraction).

This document establishes the verified multi-stage evidence matrix tracing each semantic data field across 5 discrete pipeline stages.

---

## 2. The 5 Observation Pipeline Stages

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 5 OBSERVATION PIPELINE STAGES                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Stage 1: Source HTML & Live DOM                                                        │
│          Static template markup + dynamic DOM rendering by shared/app-core.js.         │
│                                      ▼                                                 │
│ Stage 2: Browser Accessibility Tree (CDP Accessibility.getFullAXTree)                  │
│          Chromium Blink's AXObjectCache computing roles, accessible names, & states.   │
│                                      ▼                                                 │
│ Stage 3: browser-use Selector Map & DOM Simplification (browser-use==0.13.10)          │
│          DISABLED_ELEMENTS pruning + attribute whitelisting + clickable detection.    │
│                                      ▼                                                 │
│ Stage 4: Final LLM Observation / Prompt Buffer                                         │
│          The stringified Markdown/HTML buffer assembled by Agent._message_manager.     │
│                                      ▼                                                 │
│ Stage 5: Auxiliary Agent Channels (External Tools / Vision)                            │
│          CDP Runtime.evaluate, document.documentElement.outerHTML, or vision screenshots.│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Observation-Pipeline Evidence Matrix

| Semantic Data Field | Stage 1: Source & Live DOM | Stage 2: Chromium Blink AXTree | Stage 3: browser-use Serializer | Stage 4: Final LLM Prompt Buffer | Stage 5: Auxiliary Channels | Evidential Status & Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Visible Typography**<br>(`"SoundFlow Air 3"`, `"$49.99"`) | **100% Present** | **100% Retained**<br>(StaticText nodes) | **100% Retained**<br>(Child text nodes) | **100% Delivered** | Accessible via screenshot / outerHTML | **Concordant Retention:** Fully delivered across all variants. Agents solve basic tasks via this channel. |
| **Schema.org JSON-LD**<br>(`<script type="application/ld+json">`) | **100% Present** in `v1-jsonld` | **0% Omitted**<br>(Ignored by AXObjectCache) | **0% Pruned**<br>(`DISABLED_ELEMENTS = {'script', ...}`) | **0% Omitted** | **100% Accessible** via `page.evaluate()` or `outerHTML` | **Dual-Omission Dead-End in Text Prompt:** Absent in both AXTree and serialized prompt, but extractable via JS tools. |
| **Button Accessible Names**<br>(`aria-label="Add item to cart"`) | **100% Present** in `v2-aria` | **100% Retained**<br>(Computed name: `"Add item to cart"`) | **100% Retained**<br>(Whitelisted on interactive elements) | **100% Delivered** | Accessible via screenshot / outerHTML | **Concordant Retention:** Delivered on `<button>` tags across both AXTree and prompt. De-confounded post-audit. |
| **Non-Interactive ARIA**<br>(`<span aria-label="Price: $49.99">`) | **100% Present** in `v2-aria` | **100% Retained**<br>(Role: generic/text, Name: `"Price: $49.99"`) | **0% Stripped**<br>(`serialize_tree` strips non-interactive tags) | **0% Omitted**<br>(Emits only inner text `"$49.99"`) | Accessible via `page.evaluate()` or `outerHTML` | **CRITICAL DIVERGENCE:** Retained by Blink AXTree, but stripped by `browser-use`. Agent never sees the label in prompt. |
| **Custom `data-*` (Default Whitelist)**<br>(`data-action="add-to-cart"`) | **100% Present** in `v3-data-attrs` | **0% Omitted**<br>(Not exposed to accessibility API) | **0% Stripped**<br>(Omitted by `DEFAULT_INCLUDE_ATTRIBUTES`) | **0% Omitted** | Accessible via `page.evaluate()` or `outerHTML` | **Concordant Omission:** Neither AXTree nor default `browser-use` delivers developer data attributes. |
| **Custom `data-*` (Extended Whitelist)**<br>(`<button data-action="add-to-cart">`) | **100% Present** in `v3-data-attrs` | **0% Omitted**<br>(Not exposed to accessibility API) | **100% Retained**<br>(Delivered under `EXTENDED_ATTRIBUTES`) | **100% Delivered** | Accessible via `page.evaluate()` or `outerHTML` | **REVERSED DIVERGENCE:** Absent in Blink AXTree, but successfully delivered to LLM prompt under extended whitelist! |
| **Custom `data-*` on Spans**<br>(`<span data-amount="49.99">`) | **100% Present** in `v3-data-attrs` | **0% Omitted** | **0% Stripped**<br>(Stripped due to non-interactive tag removal) | **0% Omitted** | Accessible via `page.evaluate()` or `outerHTML` | **Interactive Boundary:** Even under extended whitelist, non-interactive elements have their data attributes stripped. |
| **Warranty Duration**<br>(Task T6 query) | **0% ABSENT** across all variants | **0% ABSENT** | **0% ABSENT** | **0% ABSENT** | **0% ABSENT** | **Negative Probe:** Fact is completely missing. Tests whether agent reports absence vs hallucinates. |

---

## 4. Node-Level Correspondence: AXTree vs. Selector Map

### 4.1 Methodology & Implementation
To establish rigorous correspondence between CDP AXTree nodes and `browser-use`'s internal representation, [`compare_accessibility_tree.py`](file:///C:/testing/research_execution_20261018/compare_accessibility_tree.py) implements `compute_node_correspondence()`:
1. CDP `Accessibility.getFullAXTree` returns nodes containing Blink's unique `backendDOMNodeId`.
2. In `browser-use 0.13.10`, `summary.dom_state.selector_map` maps numeric indices to `DOMElementNode` objects, which contain the exact same Blink `backend_node_id`.
3. The script joins AX nodes and `selector_map` elements on this shared identifier.

### 4.2 Empirical Findings on Route `#home`
- **Total Chromium AX Nodes:** 336 nodes constructed by Blink across all 4 variants.
- **AX Nodes with `backendDOMNodeId`:** 256 nodes.
- **Interactive Elements Detected by `browser-use`:** 34 elements (denominator).
- **Interactive Elements Matched 1-to-1 to AXTree:** **27 elements (79.4%)**.
  - Matched elements include: `#logo-link` (link), `#search-form` (search), `#search-input` (textbox), `#search-submit-btn` (button), `#cart-nav-link` (link), `#hero-cta-btn` (link), category buttons (`#cat-audio`, `#cat-keyboards`, etc.), and product card action buttons.
- **Why 7 Elements Were Unmatched:**
  - 7 interactive elements correspond to shadow DOM boundaries or synthetic input wrappers injected into open shadow roots where Blink does not generate a separate top-level accessibility node matching the DOM backend ID.
- **Route Specificity:** This measurement was conducted strictly on route `index.html#home`. Correspondence rates vary across routes (`#cart`, `#checkout`) and must not be generalized beyond tested conditions.

### 4.3 Inherent Non-Interactive Limitation (Explicitly Retained)
- `browser-use`'s `DOMTreeSerializer.serialize_tree` strips non-interactive elements (`<span>`, `<div>`, `<section>`) and emits solely raw child text strings without DOM node IDs in the LLM prompt buffer.
- Because stripped typography nodes carry no backend node IDs in the serialized text prompt, **true 1-to-1 node-level mapping between AXTree nodes and prompt lines cannot be established for non-interactive elements**.
- Substring searching serves as an indirect observation proxy. This architectural limitation is formally retained and documented, avoiding any claim of isomorphic tree mapping.

---

## 5. Architectural Conclusions

1. **The "DOM Pruning == Accessibility Tree" Fallacy Refuted:**
   - Prior browser-agent literature frequently equated DOM pruning with accessibility tree distillation.
   - This comparison conclusively refutes that assumption:
     - Non-interactive ARIA labels (e.g. price and rating descriptions) exist in Chromium's AXTree but are **100% stripped** by `browser-use`.
     - Custom `data-*` attributes do not exist in Chromium's AXTree but are **100% deliverable** by `browser-use` under an extended whitelist.
2. **Channel-Specific Scope:**
   - JSON-LD is absent from both the AXTree and the DOM serializer prompt, but it is **not globally inaccessible** to browser agents. An agent equipped with JavaScript evaluation or network interception tools can access JSON-LD directly.

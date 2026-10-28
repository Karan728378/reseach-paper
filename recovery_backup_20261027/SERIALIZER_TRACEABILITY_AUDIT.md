# SERIALIZER TRACEABILITY AUDIT: DOM-TO-OBSERVATION STAGING

**Project Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Framework Audited:** `browser-use 0.13.10` (Python 3.11 wheel installation)  
**Workspace:** `C:\testing\research_execution_20261018`  
**Date:** October 26, 2026  
**Auditor:** Browser Automation & Accessibility Systems Specialist  
**Standard:** Deterministic line-by-line AST verification paired with live Chromium CDP runtime execution traces.

---

## 1. Traceability Pipeline Architecture

Web information traverses five representations between static markup and model prompt. In `browser-use 0.13.10`, the pipeline transitions through the following stages:

```
[Stage 1: Source HTML]
         │ (HTTP fetch)
         ▼
[Stage 2: Browser Live DOM]  ──(Blink AXObjectCache)──▶ [Stage 3: Blink AXTree] (Parallel)
         │ (DOM Tree Walk)
         ▼
[Stage 4: Agent DOM Serializer (DOMTreeSerializer)]
         │ (String concatenation)
         ▼
[Stage 5: Final LLM Context Prompt Buffer]
```

*Architectural Principle:* Stage 3 (Chromium Native AXTree) is **not** an intermediate step between Stage 2 and Stage 4. `browser-use` walks the live DOM directly (Stage 2 $\to$ Stage 4). Chromium independently constructs its native Accessibility Tree in parallel (Stage 2 $\to$ Stage 3).

---

## 2. End-to-End Information Traceability Matrix

| Frontend Element / Metadata Channel | Source Syntax (Stage 1) | Live DOM (Stage 2) | Blink AXTree (Stage 3) | Agent Serializer (Stage 4) | Model Prompt (Stage 5) | Exact Architectural Gate / File Reference |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Schema.org JSON-LD** | `<script type="application/ld+json">` | Present | Omitted | **DROPPED** | **DROPPED** | `browser_use/dom/serializer/serializer.py:18,481` (`DISABLED_ELEMENTS = {'script', ...}`) |
| **Interactive Button ARIA** | `<button aria-label="Target SKU">` | Present | Present | **RETAINED** | **RETAINED** | `views.py:18` (`aria-label` in `DEFAULT_INCLUDE_ATTRIBUTES`) |
| **Non-Interactive Container ARIA** | `<span aria-label="Target SKU">` | Present | Present | **DROPPED** | **DROPPED** | `serializer.py:1046-1051` (`if node.is_interactive or is_any_scrollable:`) |
| **Developer Custom Attributes (Default)** | `<button data-product-id="101">` | Present | Omitted | **DROPPED** | **DROPPED** | `views.py:18` (`data-*` omitted from `DEFAULT_INCLUDE_ATTRIBUTES`) |
| **Developer Custom Attributes (Extended)** | `<button data-product-id="101">` | Present | Omitted | **RETAINED** | **RETAINED** | Injected via runner parameter `include_attributes=EXTENDED_ATTRIBUTES` |
| **Non-Interactive Custom Attributes** | `<span data-product-id="101">` | Present | Omitted | **DROPPED** | **DROPPED** | Line 1046 tag stripping drops attributes regardless of whitelist extension |
| **Temporal Metadata (`<meta>`)** | `<meta property="releaseDate" content="...">` | Present | Omitted | **DROPPED** | **DROPPED** | `serializer.py:18` (`meta` in `DISABLED_ELEMENTS`) |
| **Temporal Semantic (`<time>`)** | `<time datetime="2026-10-26">Today</time>` | Present | Present | **TAG STRIPPED** | Text Only | Line 1046 strips non-interactive tag; inner text emitted |

---

## 3. Forensic Code Gate Verification

### Gate 1: Unconditional Script and Meta Pruning
```python
# browser_use/dom/serializer/serializer.py:18
DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}

# browser_use/dom/serializer/serializer.py:480-482
elif node.node_type == NodeType.ELEMENT_NODE:
    if node.node_name.lower() in DISABLED_ELEMENTS:
        return None
```
*Effect:* Any element matching `DISABLED_ELEMENTS` returns `None` immediately. Child nodes are never traversed. JSON-LD structured data is pruned unconditionally at Stage 4.

### Gate 2: Non-Interactive Container Tag Stripping
```python
# browser_use/dom/serializer/serializer.py:1046-1051
is_any_scrollable = node.original_node.is_actually_scrollable or node.original_node.is_scrollable
if (
    node.is_interactive
    or is_any_scrollable
    or node.original_node.tag_name.upper() == 'IFRAME'
    or node.original_node.tag_name.upper() == 'FRAME'
):
    next_depth += 1
    attributes_html_str = DOMTreeSerializer._build_attributes_string(
        node.original_node, include_attributes, text_content
    )
```
*Effect:* If an element lacks click handlers, is non-scrollable, and is not an iframe, `_build_attributes_string` is **never called**. The opening and closing tags are omitted from serializer output. Any `aria-label` or `data-*` placed on a `<span>` or `<div>` is discarded at Stage 4.

### Gate 3: Attribute Whitelist Filtering
```python
# browser_use/dom/views.py:18
DEFAULT_INCLUDE_ATTRIBUTES = [
    'title', 'type', 'checked', 'id', 'name', 'role', 'value', 'placeholder',
    'alt', 'aria-label', 'aria-expanded', 'data-state', 'aria-checked', ...
]
```
*Effect:* Standard accessibility attributes survive on interactive elements, but custom developer attributes (`data-product-id`, `data-action`) are omitted by default. Passing `EXTENDED_ATTRIBUTES` restores them on interactive buttons, but does not circumvent Gate 2 on non-interactive containers.

---

## 4. Inspection Boundary Limitation

**Where Tracing Conclusively Stops:**  
Direct runtime inspection conclusively verifies information presence and absence at **Stage 4** (`summary.dom_state.llm_representation()`). While Stage 5 assembles Stage 4 output with the system prompt, page URL, and task history, the full combined prompt payload dispatched over the wire was not intercepted in the behavioral cloud pilot. Accordingly, the reachability boundary is strictly claimed at Stage 4.

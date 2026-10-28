# DOM OBSERVATION CHANNEL & SERIALIZATION PIPELINE AUDIT

**Target:** `browser-use 0.13.10` Observation Pipeline  
**Primary Source Locations:**
- `browser_use/dom/serializer/serializer.py` (DOMTreeSerializer)
- `browser_use/dom/serializer/clickable_elements.py` (ClickableElementDetector)
- `browser_use/dom/serializer/html_serializer.py` (HTMLSerializer)
- `browser_use/browser/session.py` (BrowserSession)
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Multi-Stage Pipeline Architecture

Autonomous web agents perceive web pages through a multi-stage observation funnel. In `browser-use 0.13.10`, observation generation involves nine distinct structural tiers:

```
[ Tier 1: Raw HTML Markup ]
          │ (HTML Parser / Network Stream)
          ▼
[ Tier 2: Live Browser DOM Tree ] ──────────┐
          │ (Layout & Computed Styles)      │ (CDP Accessibility.getFullAXTree)
          ▼                                 ▼
[ Tier 3: Rendered Layout Box ]   [ Tier 4: Chromium Blink AXTree ]
          │ (Blink Box Geometry)            │ (Parallel Semantic Representation)
          ▼                                 │
[ Tier 5: Internal DOM Snapshot ]           │
          │ (EnhancedDOMTreeNode)           │
          ▼                                 │
[ Tier 6: ClickableElementDetector ] <──────┘ (AX role lookup in lines 215-226)
          │ (Icon & Bounding Box Heuristics)
          ▼
[ Tier 7: Indexed Selector Map ]
          │ (Interactive elements assigned [index])
          ▼
[ Tier 8: Serialized Observation Text ]
          │ (Pruned string delivered in prompt)
          ▼
[ Tier 9: Final LLM Context Window ]
```

### Critical Architectural Finding: Parallel vs. Sequential Traversal
In early agent literature and initial working drafts, the Chromium AXTree was frequently assumed to filter the live DOM before serialization. 
**Source Code Audit (`session.py:140-195`):** In `browser-use 0.13.10`, the DOM serializer executes a direct recursive traversal of the live DOM tree via Playwright JavaScript evaluation. Concurrently, the Chromium AXTree is queried via the Chrome DevTools Protocol (`Accessibility.getFullAXTree`). The AXTree is used as a lookup table for ARIA roles in `clickable_elements.py:225`, but does **not** prune or intercept the live DOM tree.

---

## 2. Information Channel Retention Matrix

We traced the survival and reachability of specific metadata channels across each stage of the observation funnel:

| Information Channel | Present in HTML (Tier 1) | Present in Live DOM (Tier 2) | Present in Blink AXTree (Tier 4) | Present in Internal Snapshot (Tier 5) | Present in Selector Map (Tier 7) | Present in Serialized Prompt (Tier 8) | Directly Recoverable via Tools (Tier 9) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Visible Text Content** | Yes | Yes | Yes | Yes | Yes | **Yes** | Yes (`evaluate_script`) |
| **Standard Links / Buttons** | Yes | Yes | Yes | Yes | Yes | **Yes** | Yes (`click_element`) |
| **Non-rendered tags (`script`, `style`)** | Yes | Yes | No | **No** (`serializer.py:18`) | No | **No** | Yes (`evaluate_script`) |
| **Header metadata (`meta`, `title`)** | Yes | Yes | No | **No** (`serializer.py:18`) | No | **No** | Yes (`page.title()`) |
| **JSON-LD Schema Markup** | Yes | Yes | No | **No** (inside `<script>`) | No | **No** | Yes (`document.querySelector`) |
| **`data-*` attributes on buttons/inputs** | Yes | Yes | No | Yes | Yes | **Yes** | Yes (`element.getAttribute`) |
| **`data-*` on static containers (`div`, `span`)** | Yes | Yes | No | Yes | No | **No** | Yes (`document.querySelector`) |
| **ARIA labels on static containers** | Yes | Yes | **Yes** | Yes | No | **No** | Yes (`element.getAttribute`) |
| **Shadow DOM / Custom Elements** | Yes | Yes | Yes | Partial | Partial | **Partial** | Yes (Playwright deep locators) |
| **Small text badge (width $\le 50$px, class)** | Yes | Yes | **No** (`ignored: true`) | Yes | **Yes** (Heuristic FP) | **Yes** (Misclassified target) | Yes (`click_element`) |

---

## 3. Pruning Rules and Source Code Reference

### Rule 1: Excluded Tag Whitelist (`serializer.py:18` & `html_serializer.py:70`)
```python
DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
```
Any element whose tag matches `DISABLED_ELEMENTS` is immediately pruned at tree walk instantiation. Its text and attributes never reach the internal DOM snapshot.

### Rule 2: Attribute Stripping on Non-Interactive Nodes (`serializer.py:215-245`)
When `ClickableElementDetector.is_interactive(node)` returns `False`, non-essential attributes are stripped. Container tags like `<div>` and `<span>` retain only structural hierarchy and rendered text; custom dataset keys (e.g., `data-stock-status="in_stock"`) and accessibility attributes (e.g., `aria-hidden="true"`) are discarded.

### Rule 3: The 10–50px Small-Element Bounding Box Heuristic (`clickable_elements.py:228-240`)
```python
if (
    node.snapshot_node
    and node.snapshot_node.bounds
    and 10 <= node.snapshot_node.bounds.width <= 50  # Icon-sized elements
    and 10 <= node.snapshot_node.bounds.height <= 50
):
    if node.attributes:
        icon_attributes = {'class', 'role', 'onclick', 'data-action', 'aria-label'}
        if any(attr in node.attributes for attr in icon_attributes):
            return True
```
This heuristic was engineered to capture icon buttons (such as cart icons, hamburger menus, or close buttons) that lack standard `<button>` tags or ARIA roles. However, because it matches any element having a `class` attribute with width and height between 10px and 50px, static text badges that happen to render within this geometric window are erroneously classified as interactive targets.

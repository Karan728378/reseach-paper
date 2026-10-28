# SERIALIZATION AUDIT REPORT: QUANTIFYING METADATA REACHABILITY IN BROWSER AGENTS

**Project:** Autonomous Browser Agent Observation Pipeline & DOM Serialization Systems Study  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  
**Audit Harness:** [`audit_metadata_reachability.py`](file:///C:/testing/research_execution_20261018/audit_metadata_reachability.py)  
**Machine-Readable Metrics:** [`serialization_audit_metrics.json`](file:///C:/testing/research_execution_20261018/serialization_audit_metrics.json)  
**Audited Runtime:** `browser-use 0.13.10` / Python 3.11.9 / Playwright Chromium Headless  
**Audit Date:** October 21, 2026  

---

## 1. Executive Summary

This report provides the empirical systems proof for **The DOM Serialization Gap**: the disconnect between web markup present in client-side HTML documents and the tokens that actually reach the context window of a Large Language Model (LLM) browser agent.

Using a deterministic, offline observation-tracing harness ([`audit_metadata_reachability.py`](file:///C:/testing/research_execution_20261018/audit_metadata_reachability.py)) paired with static Abstract Syntax Tree (AST) code auditing of `browser-use 0.13.10`, we quantified reachability across seven distinct web metadata channels and three architectural edge cases.

### Core Discoveries:
1. **The Script/Meta Black Hole (0.0% Reachability):** `browser-use` unconditionally prunes `<script>` and `<meta>` elements via `DISABLED_ELEMENTS` ([`serializer.py:L18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18)). Schema.org JSON-LD structured data never reaches the LLM context prompt (0 tokens).
2. **The Non-Interactive Element Drop (0.0% Attribute Reachability):** In [`serializer.py:Lines 1046–1058`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1046-L1058), attributes are constructed **only for interactive (clickable/scrollable) elements or frames**. All attributes attached to non-interactive containers (`<span>`, `<div>`, `<section>`, `<p>`) are discarded, regardless of attribute whitelists.
3. **The Interactive Action Confound (100% Reachability on Buttons):** The only semantic metadata that physically reaches the LLM prompt is `aria-label` and whitelisted `data-*` attributes on `<button>` elements. However, modifying button labels to include entity names (e.g. `aria-label="Add SoundFlow Air 3 to cart"`) confounds semantic understanding with button text disambiguation.

---

## 2. Quantitative Reachability Matrix

| Metadata Channel | Source HTML | Parsed Live DOM | Serialized Tree | Prompt Buffer | Reachability % | Primary Suppression Mechanism |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Schema.org JSON-LD** | Present | Present | **Pruned** | **Absent** | **0.0%** | `DISABLED_ELEMENTS` set in `serializer.py:L18` |
| **2. WAI-ARIA on Buttons** | Present | Present | **Retained** | **Present** | **100.0%** | Retained on interactive nodes via `DEFAULT_INCLUDE_ATTRIBUTES` |
| **3. WAI-ARIA on Spans/Divs** | Present | Present | **Stripped** | **Absent** | **0.0%** | Non-interactive tags not serialized in `serializer.py:L1046` |
| **4. Default `data-*` Attributes** | Present | Present | **Stripped** | **Absent** | **0.0%** | Omitted from `DEFAULT_INCLUDE_ATTRIBUTES` in `views.py:L18` |
| **5. Configured `data-*` (Extended)** | Present | Present | **Retained** | **Present** | **100.0%** *(buttons)* | Requires `Agent(include_attributes=EXTENDED_ATTRIBUTES)` patch |
| **6. Temporal `<meta>` Elements** | Present | Present | **Pruned** | **Absent** | **0.0%** | `DISABLED_ELEMENTS` set in `serializer.py:L18` |
| **7. Temporal `<time>` Elements** | Present | Present | **Stripped** | **Present** *(text)* | **100.0%** *(as text)* | `<time>` tag stripped; inner text emitted as plain text string |

*Token Metric Note: Source token proxies were computed via regex whitespace-and-punctuation heuristics approximating BPE tokenizers within ~15% margin of error.*

---

## 3. Deep Architectural Analysis of Suppression Mechanisms

```
                             THE 4-STAGE INFORMATION PIPELINE
┌────────────────────────┐
│   Source HTML / SPA    │ ── [HTML Parser / JS Execution]
└────────────────────────┘
            │
            ▼
┌────────────────────────┐
│   Parsed Browser DOM   │
└────────────────────────┘
            │
            ▼
┌────────────────────────┐
│  DOM Simplification    │ ── Bottleneck 1: DISABLED_ELEMENTS prunes <script>, <meta>
└────────────────────────┘
            │
            ▼
┌────────────────────────┐
│   Tree Serialization   │ ── Bottleneck 2: Lines 1046–1058 strip non-interactive tags
└────────────────────────┘ ── Bottleneck 3: Lines 1211–1215 filter against whitelist
            │
            ▼
┌────────────────────────┐
│  Final LLM Prompt Buffer
└────────────────────────┘
```

### Mechanism 1: Tag-Level Pruning (`DISABLED_ELEMENTS`)
In [`serializer.py:Line 18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18):
```python
DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
```
During tree traversal in `_create_simplified_tree` ([`serializer.py:L480-L482`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L480-L482)):
```python
elif node.node_type == NodeType.ELEMENT_NODE:
    if node.node_name.lower() in DISABLED_ELEMENTS:
        return None
```
When `return None` executes, traversal terminates for that entire branch. Neither the node nor any child nodes are processed. Consequently, structured search indexing formats (`<script type="application/ld+json">`) and verification timestamps (`<meta name="evidence-date">`) are destroyed before the agent ever observes the page.

### Mechanism 2: Non-Interactive Element Attribute Stripping
In [`serializer.py:Lines 1046–1058`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1046-L1058):
```python
is_any_scrollable = node.original_node.is_actually_scrollable or node.original_node.is_scrollable
should_show_scroll = node.original_node.should_show_scroll_info
if (
    node.is_interactive
    or is_any_scrollable
    or node.original_node.tag_name.upper() == 'IFRAME'
    or node.original_node.tag_name.upper() == 'FRAME'
):
    ...
    attributes_html_str = DOMTreeSerializer._build_attributes_string(
        node.original_node, include_attributes, text_content
    )
```
If an element is **not interactive** (not clickable, not scrollable, and not a frame):
- `_build_attributes_string` is **never called**.
- No tag line `<span ...>` or `<div ...>` is emitted in the serialized observation.
- The serializer recursively processes child text nodes, emitting pure textual strings (e.g. `$49.99` or `4.5`), but all parent attributes (`aria-label`, `data-amount`, `data-rating`, `role="img"`) are discarded.

### Mechanism 3: Whitelist Filtering & Empty Attribute Pruning
In [`serializer.py:Lines 1211–1215`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1211-L1215):
```python
attributes_to_include.update(
    {
        key: str(value).strip()
        for key, value in node.attributes.items()
        if key in include_attributes and str(value).strip() != ''
    }
)
```
1. **Whitelist Exclusion:** If `key not in include_attributes`, the attribute is dropped. Because `DEFAULT_INCLUDE_ATTRIBUTES` in `views.py:L18` contains `aria-label` but omits `data-action` or `data-product-id`, developer custom attributes are stripped by default.
2. **Empty Attribute Stripping:** Attributes where `str(value).strip() == ''` (such as placeholder attributes `aria-label=""` or `data-action=""`) are pruned.

---

## 4. Edge-Case Fixture Findings

Using our reproducible fixture ([`fixtures/edge_cases.html`](file:///C:/testing/research_execution_20261018/fixtures/edge_cases.html)), we verified three architectural boundary conditions:

### Edge Case 1: Non-Interactive Container Sections
- **Fixture HTML:** `<section id="showcase-section" aria-label="Featured Showcase" data-container-id="sec-01">`
- **Result:** Both `aria-label` and `data-container-id` were 100% absent from the LLM prompt under both default and extended whitelists.
- **Implication:** Web developers cannot use semantic landmark attributes (`<section aria-label="...">`) to guide `browser-use` agents unless the section itself is made scrollable or interactive.

### Edge Case 2: Empty Attribute Values
- **Fixture HTML:** `<button id="btn-empty" aria-label="" data-action="">Empty Action</button>`
- **Result:** Neither `aria-label` nor `data-action` appeared in the serialized output.
- **Implication:** The serializer enforces strict non-empty content checks, preventing token inflation from empty markup.

### Edge Case 3: Nested Elements Inside Interactive Buttons
- **Fixture HTML:**
  ```html
  <button id="btn-nested" aria-label="Nested Button Wrapper">
    <span class="btn-icon">🛒</span>
    <span class="btn-text">Buy Now</span>
  </button>
  ```
- **Result:** The button tag retained `aria-label="Nested Button Wrapper"`, while the child spans were flattened into the button's text representation: `[index] <button aria-label="Nested Button Wrapper">🛒 Buy Now</button>`.

---

## 5. Methodological & Systems Implications

1. **The Fallacy of Metadata Augmentation for AI:**  
   Proposals at standards bodies (W3C/TPAC) recommending that developers embed specialized Schema.org JSON-LD or custom data attributes specifically for AI agents are currently ineffective for agents running standard `browser-use`. The client-side observation serializer discards these tags before the model receives the prompt.
2. **The "ARIA Stuffing" Confound:**  
   When accessibility attributes do survive (on `<button>` elements), they change the reasoning task from relational hierarchy resolution (finding the product card and locating its child button) to direct string matching (reading the product name directly off the button). Any observed performance improvement on such tasks measures target-name co-location, not semantic comprehension.
3. **The Necessity of Dedicated Machine Endpoints:**  
   Rather than attempting to encode machine data inside HTML DOM channels that are vulnerable to serialization pruning, autonomous agent architectures require dedicated out-of-band endpoints (e.g., `llms.txt`, Model Context Protocol APIs) that bypass DOM serialization entirely.

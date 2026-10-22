# 04. Browser-Use 0.13.10 Architecture & Channel Exposure Audit

**Audit Directory:** `C:\testing\research_audit_20261015_231500`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Architectural Code Path Inspection (`browser-use 0.13.10`)

We conducted an exhaustive static and dynamic inspection of the installed library code in [`C:\testing\.venv311\Lib\site-packages\browser_use\`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/):

### 1. Hardcoded Element Pruning (`DISABLED_ELEMENTS`)
- **Location:** [`browser_use/dom/serializer/serializer.py:18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18)
  ```python
  DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
  ```
- **Mechanism:** In `_create_simplified_tree()` ([lines 480–482](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L480-L482)):
  ```python
  if node.node_name.lower() in DISABLED_ELEMENTS:
      return None
  ```
- **Consequence:** 
  - Any `<script>` tag—including `<script type="application/ld+json">`—is pruned before DOM tree construction.
  - Any `<meta>` tag in `<head>` is pruned before DOM tree construction.
  - JSON-LD and meta tags have **0% exposure** under all native browser-use pipelines.

### 2. Attribute Whitelist Filtering (`DEFAULT_INCLUDE_ATTRIBUTES`)
- **Location:** [`browser_use/dom/views.py:18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/views.py#L18)
- **Mechanism:** In `_build_attributes_string` ([`serializer.py:1208-1216`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1208-L1216)):
  ```python
  if node.attributes:
      attributes_to_include.update(
          {
              key: str(value).strip()
              for key, value in node.attributes.items()
              if key in include_attributes and str(value).strip() != ''
          }
      )
  ```
- **Consequence:** Custom attributes such as `data-sku`, `data-field`, `data-action`, `data-stock` are not in `DEFAULT_INCLUDE_ATTRIBUTES`. They are completely stripped unless the researcher explicitly passes `include_attributes` to `Agent()`.

### 3. Non-Interactive Element Pruning (`serialize_tree`)
- **Location:** [`browser_use/dom/serializer/serializer.py:1043-1051`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1043-L1051)
- **Mechanism:** In `serialize_tree`:
  ```python
  if node.is_interactive or is_any_scrollable or tag in ('IFRAME', 'FRAME'):
      # format tag and attributes
  ```
- **Consequence:** Even if `data-*` or `aria-label` is included in `include_attributes`, if that attribute is placed on a non-interactive element (such as `<span>`, `<div>`, or `<time>`), the tag and all its attributes are discarded! Only the child text nodes are serialized.

---

## 2. Empirical Zero-API Pipeline Verification

Using our custom `OfflineStubChatModel`, local test fixture [`channel_test.html`](file:///C:/testing/research_audit_20261015_231500/fixtures/channel_test.html), and background server `http://127.0.0.1:8899`, we evaluated the exact messages reaching the model across four distinct configurations:

1. **Default Pipeline:** Native `browser-use 0.13.10` out-of-the-box (`include_attributes=None`, unpatched).
2. **Configured Attributes Whitelist:** Passing custom `data-*` and ARIA attributes via `include_attributes`, unpatched serializer.
3. **Patched Serializer:** Monkey-patched serializer (`enable_observable_dom_serialization()`) + attribute whitelist.
4. **Full Observable Pipeline:** Patched serializer + custom python hook (`extract_active_page_metadata()`).

### Table 2: Channel Exposure Matrix Across Six Diagnostic Levels

| Information Channel | 1. Present in Source HTML? | 2. Present in Rendered DOM? | 3. Present in A11y Tree? | 4. Default Browser-Use Serialized DOM? | 5. Reaches Exact Model Messages? | 6. Usable for Action Grounding? | Supporting Code Path & Limitations |
|---|---|---|---|---|---|---|---|
| **Visible Text** | Yes | Yes | Yes (StaticText) | **YES** | **YES** (Text & Vision) | **YES** | Standard DOM text nodes always preserved. |
| **ARIA on Interactive Button** (`aria-label`) | Yes | Yes | Yes (Name) | **YES** | **YES** (Text only) | **YES** | Included in default whitelist; formatted as `[index]<button aria-label=... />`. |
| **ARIA on Non-Interactive Div** (`aria-label`) | Yes | Yes | Yes (Name) | **NO** | **NO** | **NO** | Discarded by `serialize_tree` line 1043; non-interactive tag dropped. |
| **`data-*` on Interactive Button** (Default) | Yes | Yes | No | **NO** | **NO** | **NO** | Stripped by `serializer.py:1214` (not in `DEFAULT_INCLUDE_ATTRIBUTES`). |
| **`data-*` on Interactive Button** (Configured) | Yes | Yes | No | **YES** | **YES** | **YES** | Reaches model if passed via `Agent(include_attributes=...)`. |
| **`data-*` on Non-Interactive Span** (Default/Configured) | Yes | Yes | No | **NO** | **NO** | **NO** | Discarded by `serialize_tree` line 1043 unless patched. |
| **`data-*` on Non-Interactive Span** (Patched) | Yes | Yes | No | **YES** | **YES** | **YES** | Requires monkey-patching `_create_simplified_tree`, `_optimize_tree`, and `serialize_tree`. |
| **JSON-LD Structured Data** (`<script>`) | Yes | Yes | No | **NO** | **NO** | **NO** | Hard-coded prune in `DISABLED_ELEMENTS` (`serializer.py:18`). |
| **JSON-LD Structured Data** (Augmented Hook) | Yes | Yes | No | **NO (in DOM)** | **YES (as Message Header)** | **Exploratory** | Injected directly into `UserMessage` via custom Python Playwright hook. |
| **Meta Tags** (`<meta>` in `<head>`) | Yes | Yes | No | **NO** | **NO** | **NO** | Hard-coded prune in `DISABLED_ELEMENTS`. |
| **Screenshots (Vision Channel)** | N/A | Rendered | N/A | N/A | **YES** (`ContentPartImageParam`) | **Visual Only** | High-res Base64 PNG sent to multimodal LLMs; captures visual text only. |

---

## 3. Critical Methodological Findings

1. **Fatal Confound in Experiment 1:**
   Because Experiment 1 used the default browser-use pipeline, variants `v1-jsonld`, `v3-data-attrs`, and static `v4-evidence-meta` were **never delivered to the model**. The agent operated with 0% access to these treatments.
2. **Harness Configuration is an Independent Treatment:**
   Enabling `include_attributes` or monkey-patching the DOM serializer modifies the *agent harness*, not the *website*. In a valid scientific study, web design enhancements (features authored into HTML) must not be confounded with agent harness re-engineering.
3. **JSON-LD Structural Incompatibility:**
   JSON-LD cannot be evaluated as an in-DOM web markup channel under `browser-use` without rewriting the library's core architecture.

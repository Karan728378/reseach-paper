# Browser-Use Observation Pipeline Trace
**Audit Date:** 2026-10-18
**browser-use version:** 0.13.10

## DOM Serialization — DISABLED_ELEMENTS
**Source:** `C:\testing\.venv311\Lib\site-packages\browser_use\dom\serializer\serializer.py`
**SHA-256:** `6d523ff457d1f0c99152eeb5cc86a96d6ed6a59bf2636aceae871549afdce91f`

Elements pruned before DOM snapshot reaches LLM:
```
[
  "style",
  "script",
  "head",
  "meta",
  "link",
  "title"
]
```

- `"script"` in DISABLED_ELEMENTS: **True**
- `"meta"` in DISABLED_ELEMENTS: **True**

**Consequence:** `<script type="application/ld+json">` blocks are stripped. JSON-LD content
never reaches the LLM regardless of what the page contains.

## DOM Attribute Whitelisting — DEFAULT_INCLUDE_ATTRIBUTES
**Source:** `C:\testing\.venv311\Lib\site-packages\browser_use\dom\views.py`
**SHA-256:** `01866ed2d9aa77ee6a8be5f9c707dbe403c4802acaf9680975766dd93d7a48b5`

Attributes passed through to LLM (excerpt of relevant ones):
```
[
  "title",
  "type",
  "checked",
  "class",
  "id",
  "name",
  "role",
  "value",
  "placeholder",
  "data-date-format",
  "alt",
  "aria-label",
  "aria-expanded",
  "data-state",
  "aria-checked",
  "aria-valuemin",
  "aria-valuemax",
  "aria-valuenow",
  "aria-placeholder",
  "pattern"
]
```

Custom `data-*` attributes in whitelist: `[]`
Custom `data-*` attributes **stripped** by default: `['data-warranty', 'data-lot-code', 'data-stock-count', 'data-return-window', 'data-ship-date']`

**Consequence:** All proposed `data-*` treatment attributes (`data-warranty`, `data-lot-code`, etc.)
are stripped from the DOM snapshot under default configuration. The DATA-CFG arm requires
explicit runner patching of `include_attributes`.

## Arm-Level Channel Summary

| Arm | Channel | Mechanism | Token Reaches LLM |
|-----|---------|-----------|-------------------|
| ABS | Absent | — | No |
| VIS | Visible text | DOM snapshot body text | **Yes** |
| ARIA | `aria-label` | Attribute whitelist (aria-label included) | **Yes** |
| DATA-CFG | `data-*` attribute | Attribute whitelist (NOT included by default) | **Only if patched** |
| JSON-LD | `<script type=ld+json>` | DISABLED_ELEMENTS prunes script | **No** |
| META | `<meta>` tag | DISABLED_ELEMENTS prunes meta | **No** |

## Vision Confound
If `use_vision=True`:
- VIS arm: rendered page text visible in screenshot → **dual channel** (text + vision)
- ARIA arm: aria-label not rendered visually → **single channel** (text only)
- DATA-CFG arm: data-* not rendered visually → **single channel** (text only)

This creates an uncontrolled dual-channel confound for VIS vs ARIA/DATA-CFG comparisons.
**Mitigation: set `use_vision=False`.**

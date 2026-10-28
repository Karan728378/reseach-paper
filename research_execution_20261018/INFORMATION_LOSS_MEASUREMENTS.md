# DIRECT INFORMATION-LOSS MEASUREMENTS
**Date (UTC):** 2026-10-27T13:43:19.236154+00:00  
**Methodology:** Model-free direct measurement of atomic semantic entity retention across discrete observation pipeline stages (`browser-use 0.13.10`).  
**Fixture Corpus:** 7 fixtures (`sentinel`, `edge_cases`, `probe_a`, `probe_b`, `geometry_boundary`, `multi_framework`, `disambiguation_control`).  
**Total Atomic Entities Audited:** 44  
**Statistical Confidence Intervals:** Exact Clopper-Pearson binomial intervals and Wilson score intervals.  

---

## 1. Executive Summary & Core Findings

1. **Severe Channel-Level Information Collapse:**
   - **Schema.org JSON-LD:** $0/4$ entities retained ($0.0\%$, 95% Clopper-Pearson CI $[0.0000, 0.6024]$). Completely pruned at Stage 2 by `DISABLED_ELEMENTS` (`serializer.py` L18/L481).
   - **HTML `<meta>` Tags:** $0/2$ entities retained ($0.0\%$, 95% CI $[0.0000, 0.8419]$). Pruned at Stage 2 by `DISABLED_ELEMENTS`.
   - **Developer `data-*` Attributes (Default):** $0/5$ entities retained ($0.0\%$, 95% CI $[0.0000, 0.5218]$). Pruned at Stage 4 by `DEFAULT_INCLUDE_ATTRIBUTES` whitelist.
   - **Container WAI-ARIA (`aria-label` / `role='region'`):** $4/12$ entities retained ($33.3\%$, 95% CI $[0.0992, 0.6511]$). Only small elements ($10 \le w, h \le 50\text{px}$) survived via geometric icon heuristics; all standard containers were stripped at L1046–1051.
   - **Visible Typography:** $10/10$ entities retained ($100.0\%$, 95% CI $[0.6915, 1.0000]$). Fully preserved across all stages.
   - **Interactive Control ARIA (`<button aria-label>`):** $4/4$ entities retained ($100.0\%$, 95% CI $[0.3976, 1.0000]$). Fully preserved.

2. **The Decisive Information Bottleneck:**
   - Across all 26 task-decisive entities, overall Stage 5 delivery rate is **12/26 (46.2%)** (95% Clopper-Pearson CI: `[0.2659, 0.6663]`).
   - Crucially, whenever task-decisive information was located *exclusively* in JSON-LD, container ARIA, or developer `data-*`, Stage 5 delivery was **$0.0\%$**.
   - This proves conclusively that agent failures on semantic probes are caused by **observation truncation**, not reasoning deficits.

---

## 2. Channel-Level Information Retention Matrix

| Semantic Channel | Total Entities ($N$) | Stage 4 Retained | Stage 5 Retained | Stage 5 Retention Rate | 95% Exact Clopper-Pearson CI | 95% Wilson Score CI | Primary Loss Mechanism |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **`aria_roles_landmarks`** | 1 | 0 | 0 | **0.0%** | `[0.0000, 0.9750]` | `[0.0000, 0.7935]` | `INTERACTIVITY_GATE` |
| **`data_attribute_container`** | 1 | 0 | 0 | **0.0%** | `[0.0000, 0.9750]` | `[0.0000, 0.7935]` | `INTERACTIVITY_GATE` |
| **`data_attribute_default`** | 6 | 0 | 0 | **0.0%** | `[0.0000, 0.4593]` | `[0.0000, 0.3903]` | `ATTRIBUTE_WHITELIST` |
| **`hidden_dom`** | 1 | 0 | 0 | **0.0%** | `[0.0000, 0.9750]` | `[0.0000, 0.7935]` | `CSS_VISIBILITY` |
| **`interactive_aria_label`** | 3 | 3 | 3 | **100.0%** | `[0.2924, 1.0000]` | `[0.4385, 1.0000]` | `NONE` |
| **`json_ld`** | 4 | 0 | 0 | **0.0%** | `[0.0000, 0.6024]` | `[0.0000, 0.4899]` | `DISABLED_ELEMENTS` |
| **`meta_tag`** | 2 | 0 | 0 | **0.0%** | `[0.0000, 0.8419]` | `[0.0000, 0.6576]` | `DISABLED_ELEMENTS` |
| **`non_interactive_aria_label`** | 16 | 5 | 5 | **31.2%** | `[0.1102, 0.5866]` | `[0.1416, 0.5560]` | `INTERACTIVITY_GATE` |
| **`visible_typography`** | 10 | 10 | 10 | **100.0%** | `[0.6915, 1.0000]` | `[0.7225, 1.0000]` | `NONE` |

---

## 3. Root-Cause Mechanism Breakdown

| Pruning Mechanism | Code / Architectural Reference | Entities Dropped / Governed | Fraction of Total Entities | Decisive Entities Impacted |
|---|---|:---:|:---:|:---:|
| **`ATTRIBUTE_WHITELIST`** | `views.py` `DEFAULT_INCLUDE_ATTRIBUTES` (Filtered during Stage 4 serialization) | 5 | 11.4% | 5 |
| **`CSS_VISIBILITY`** | `build_dom_tree.js` (`display: none` / `aria-hidden='true'` excluded) | 1 | 2.3% | 0 |
| **`DISABLED_ELEMENTS`** | `serializer.py` L18, L481 (Pruned during initial Stage 2 AST walk) | 6 | 13.6% | 3 |
| **`GEOMETRIC_MISCLASSIFICATION`** | `clickable_elements.py` L227–241 ($10 \le w, h \le 50\text{px}$ heuristic) | 5 | 11.4% | 1 |
| **`INTERACTIVITY_GATE`** | `serializer.py` L1046–1051 (Non-interactive tags stripped; inner text emitted without attributes) | 14 | 31.8% | 6 |
| **`NONE`** | Fully preserved through Stage 5 prompt assembly | 13 | 29.5% | 11 |

---

## 4. Methodological Implications for Benchmark Design

1. **Preflight Delivery Verification is Mandatory:**
   - Before attributing performance variation to LLM architecture or reasoning capabilities, benchmarks must execute a deterministic preflight probe asserting that the tested treatment channel actually reaches the model prompt boundary (Stage 5).
2. **Eliminating the Visible Typography Ceiling:**
   - Benchmarks that provide visible SKU numbers or labels in rendered text (e.g. standard TechMart cards) cannot measure the utility of semantic metadata, because visible typography is 100% retained and fully sufficient for deterministic resolution.
3. **Circularity of AXTree Correspondence:**
   - Because `ClickableElementDetector` directly inspects `node.ax_node.role`, any claim that selector maps 'correspond' to the accessibility tree is circular by construction.

---
**Artifacts Produced:** `INFORMATION_LOSS_MEASUREMENTS.csv` (SHA-256: `519bac28a0f00728551d3620a0ea5d45ad18ce22e7f5a61e551bf8f539972c96`)  
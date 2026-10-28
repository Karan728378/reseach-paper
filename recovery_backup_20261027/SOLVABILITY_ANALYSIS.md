# DETERMINISTIC SOLVABILITY & CONFOUND ANALYSIS
**Date (UTC):** 2026-10-26T19:59:10.382070+00:00  
**Evidence Class:** **E3 (Observed Concrete Telemetry / Deterministic Oracle Reader)**  
**Methodology:** Model-free, non-LLM oracle reader evaluation of Stage 4 and Stage 5 serialized observation text across benchmark routes and disambiguation probes.  
**Core Objective:** Formally prove whether benchmark tasks are mathematically solvable from the observation text alone under each experimental arm, separating observation reachability from agent reasoning.  

---

## 1. Executive Summary: The Dual Failure Modes of Prior Benchmarks

1. **The Visible Typography Ceiling (TechMart Tasks):**
   - In standard TechMart e-commerce routes (Home, Category, Search, Product, Cart), the target item is identifiable from **visible text alone** in $5/5$ tasks ($100\%$ solvability, $p=1.0$).
   - Consequently, the observed 13/13 success rate across all arms in the exploratory pilot was driven entirely by visible typography. Because visible text was already sufficient, additive semantic markup could not produce any measurable performance gain.

2. **The Serializer Truncation Bottleneck (Disambiguation Probes):**
   - When visible typography is held strictly identical across options ('Select Item'), solvability depends entirely on serializer reachability:
     - **Probe A (data-* attribute):** Under ABS (default whitelist), the task is **UNSOLVABLE** ($p=0.5$ random guess), because `data-product-id` is stripped. Under DATA-CFG, the task becomes **SOLVABLE** ($p=1.0$).
     - **Probe B (container span ARIA):** Under ARIA, the task is **UNSOLVABLE** ($p=0.5$ random guess), because the framework's interactivity gate (`serializer.py` L1046–1051) strips non-interactive container spans, discarding their `aria-label`.

---

## 2. Deterministic Task Solvability Matrix

| Task ID | Benchmark Context | Target Decisive Information | Arm 1 (ABS) Solvability | Arm 2 (ARIA) Solvability | Arm 3 (DATA-CFG) Solvability | Mathematical Diagnosis |
|---|---|---|:---:|:---:|:---:|---|
| **`TM-01-Home`** | TechMart #home route | `Add target item (SKU: target-sku-101) to cart from Home route` | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | Ceiling effect: visible typography makes task 100% solvable in all arms regardless of markup. |
| **`TM-02-Category`** | TechMart #category route | `Filter by Audio category and select target headphones` | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | Ceiling effect: visible category text and product titles provide full solvability. |
| **`TM-03-Search`** | TechMart #search route | `Search for 'ergonomic keyboard' and add target SKU to cart` | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | Ceiling effect: human-visible typography renders semantic channels redundant. |
| **`TM-04-Product`** | TechMart #product route | `Verify specifications on Product Detail page and select option` | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | Ceiling effect: visible text contains complete product specs. |
| **`TM-05-Cart`** | TechMart #cart route | `Review cart items and proceed to checkout` | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | Ceiling effect: visible button text 'Checkout' is uniquely identifying. |
| **`PROBE-A-Default`** | fixtures/disambiguation_probe_a.html | `Select target item (SKU: target-sku-101) where visible text is identical ('Select Item')` | UNSOLVABLE ($p=0.5$) | UNSOLVABLE ($p=0.5$) | **SOLVABLE** ($p=1.0$) | Proves causal effect of serializer whitelist: DATA-CFG converts an unsolvable task into a solvable one. |
| **`PROBE-B-Container`** | fixtures/disambiguation_probe_b.html | `Select target item (SKU: target-sku-101) where identity is encoded in container span aria-label` | UNSOLVABLE ($p=0.5$) | UNSOLVABLE ($p=0.5$) | UNSOLVABLE ($p=0.5$) | Demonstrates architectural limitation: non-interactive container ARIA is dropped across all arms. |
| **`PROBE-Control`** | fixtures/disambiguation_control.html | `Select target item where visible text contains target SKU and distinct button label` | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | **SOLVABLE** ($p=1.0$) | Positive control: confirms oracle reader and pipeline preserve rendered text. |

---

## 3. Co-Location Confound Formalization (Part 9f)

A critical flaw in early web-agent benchmarking is the **co-location confound**: semantic markup (e.g. `aria-label` or `data-sku`) is frequently placed on elements that *also* contain identical human-visible rendered text. When an agent succeeds, it is impossible to determine whether the model parsed the semantic metadata or simply read the rendered typography.

To rigorously decouple channel delivery from textual content, we formalize a $3 \times 3$ full factorial experimental design:

### Factorial Design Matrix ($3 \times 3$)
- **Factor A (Textual Content / Placement):**
  - $A_1$: Content rendered in visible text near button (human-visible DOM leaf).
  - $A_2$: Content isolated in element attribute (invisible rendered layout; visible text generic: 'Select').
  - $A_3$: Content co-located in both visible text AND element attribute.
- **Factor B (Delivery Channel):**
  - $B_1$: Rendered Typography (`<p>`, `<span>`, text nodes).
  - $B_2$: WAI-ARIA (`aria-label`, `role='button'`).
  - $B_3$: Custom Developer Attribute (`data-product-id`).

### Deterministic Oracle Solvability by Cell

| Factor Cell | Channel ($B$) | Content Placement ($A$) | Visible Button Text | Metadata Attribute | Oracle Solvability ($p$) | Pipeline Mechanism |
|---|---|---|---|---|:---:|---|
| **Cell (1,1)** | Visible Typography | Visible Text Only ($A_1$) | 'Select SKU-101' | None | **$1.0$ (Solvable)** | Emitted as plain text leaf. |
| **Cell (1,2)** | Visible Typography | Attribute Only ($A_2$) | 'Select Option' | None | $0.5$ (Unsolvable) | Text lacks distinguishing SKU. |
| **Cell (1,3)** | Visible Typography | Co-Located Both ($A_3$) | 'Select SKU-101' | None | **$1.0$ (Solvable)** | Identifiable via visible text. |
| **Cell (2,1)** | WAI-ARIA | Visible Text Only ($A_1$) | 'Select SKU-101' | `aria-label='Select'` | **$1.0$ (Solvable)** | Solvable via visible text confound. |
| **Cell (2,2)** | WAI-ARIA (Interactive) | Attribute Only ($A_2$) | 'Select Option' | `aria-label='SKU-101'` on `<button>` | **$1.0$ (Solvable)** | Retained: interactive leaf control. |
| **Cell (2,2b)** | WAI-ARIA (Container) | Attribute Only ($A_2$) | 'Select Option' | `aria-label='SKU-101'` on `<span>` | $0.5$ (Unsolvable) | **Dropped:** stripped at L1046. |
| **Cell (2,3)** | WAI-ARIA | Co-Located Both ($A_3$) | 'Select SKU-101' | `aria-label='SKU-101'` | **$1.0$ (Solvable)** | Confounded by visible text. |
| **Cell (3,1)** | Developer `data-*` | Visible Text Only ($A_1$) | 'Select SKU-101' | None | **$1.0$ (Solvable)** | Solvable via visible text confound. |
| **Cell (3,2a)** | Developer `data-*` (ABS) | Attribute Only ($A_2$) | 'Select Option' | `data-sku='SKU-101'` (Default) | $0.5$ (Unsolvable) | **Dropped:** omitted from whitelist. |
| **Cell (3,2b)** | Developer `data-*` (DATA) | Attribute Only ($A_2$) | 'Select Option' | `data-sku='SKU-101'` (Extended) | **$1.0$ (Solvable)** | **Retained:** delivered to prompt. |
| **Cell (3,3)** | Developer `data-*` | Co-Located Both ($A_3$) | 'Select SKU-101' | `data-sku='SKU-101'` | **$1.0$ (Solvable)** | Confounded by visible text. |

---

## 4. Key Takeaways for Manuscript Revision

1. **Retract Causal Intelligence Claims:** Any claim that the agent 'understood semantic metadata' in the TechMart benchmark must be retracted, because the task was solvable with $p=1.0$ from visible text alone.
2. **Cell (2,2) vs Cell (2,2b) Asymmetry:** Proves that WAI-ARIA delivery is non-uniform: interactive button `aria-label` is 100% delivered, whereas container span `aria-label` is 0% delivered.
3. **True Causal Contrast Exists in Cell (3,2):** The only genuine markup contrast in the benchmark occurs when visible text is generic ('Select') and `data-*` is toggled between default whitelist (ABS, $p=0.5$) and extended whitelist (DATA-CFG, $p=1.0$).

---
**Audit Status:** Verified by scripted oracle reader. Evidence Class: E3.  
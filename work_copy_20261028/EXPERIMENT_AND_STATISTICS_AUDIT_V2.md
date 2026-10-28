# EXPERIMENT & STATISTICS AUDIT V2: PROTOCOL VALIDITY, POWER LIMITS & DATA GOVERNANCE

**Project:** Autonomous Browser Agent Observation Pipeline & DOM Serialization Systems Study  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  
**Audit Date:** October 21, 2026  
**Auditor:** Research Supervisor & Statistical Methodology Lead  

---

## 1. Executive Summary & Audit Scope

This audit evaluates the experimental design, treatment delivery, ground-truth verifiers, and statistical analysis framework specified in Protocol v3 ([`protocol.md`](file:///C:/testing/research_execution_20261018/protocol.md), [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py), [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py)). 

### Primary Audit Verdict:
The statistical analysis engine and task verifiers are exceptionally well-engineered and mathematically validated. However, **the behavioral experiment suffers from two fatal methodological barriers:**
1. **Severe Statistical Underpowering ($<11\%$ power for small effects):** With $n=20$ trials per arm across primary tasks T1–T5, the experiment has $>89\%$ probability of generating an inconclusive null result ($p > 0.05$) even when a real 15–20% performance improvement exists.
2. **Treatment Delivery Confounding (Button Label Co-Location):** Modifying `<button>` from `"Add to Cart"` to `aria-label="Add SoundFlow Air 3 to cart"` does not measure generalized semantic comprehension; it directly co-locates the target product title onto the action trigger.

**Formal Decision:** Protocol v3 must **not** serve as the primary empirical contribution of the research paper. It is formally repositioned as a **pre-registered methodological case study** demonstrating how agent observation pipelines constrain experimental design.

---

## 2. Treatment Construction & Confounding Analysis

### 2.1 The Target-Text Co-Location Confound in `v2-aria`
In [`shared/app-core.js:Line 243`](file:///C:/testing/shared/app-core.js#L243):
```javascript
if (F.aria) addBtn.setAttribute('aria-label', 'Add ' + product.name + ' to cart');
```
- In `v0-baseline` (ABS and VIS), all product buttons render as: `[12] <button>Add to Cart</button>`. To select the correct button, the agent must perform **hierarchical reference resolution**: read the card's heading (`<h3>SoundFlow Air 3</h3>`), inspect the price (`$49.99`), find the card boundary, and identify the specific button index corresponding to that card.
- In `v2-aria`, the button renders as: `[12] <button aria-label="Add SoundFlow Air 3 to cart">Add to Cart</button>`.
- **The Confound:** The agent no longer needs to perform hierarchical reference resolution. It simply searches the serialized prompt for the string `"SoundFlow Air 3"` and clicks the button containing that exact label. Any observed improvement in agent accuracy reflects **element-label disambiguation**, not semantic markup comprehension.

### 2.2 Developer Attribute Injection in `v3-data-attrs`
In [`shared/app-core.js:Lines 245–247`](file:///C:/testing/shared/app-core.js#L245-L247):
```javascript
if (F.dataAttrs) {
  addBtn.setAttribute('data-action', 'add-to-cart');
  addBtn.setAttribute('data-product-id', product.sku);
}
```
- Custom developer attributes (`data-action`, `data-product-id`) are retained on `<button>` elements only because [`protocol_v3_runner.py:L32`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L32) supplies `EXTENDED_ATTRIBUTES`.
- However, attributes on parent container elements (`<div class="product-card" data-product-id="wh-001">`) and pricing spans (`<span data-amount="49.99">`) are stripped by `serializer.py:L1046`. The model receives structured data on the button, but not on the informational card elements.

---

## 3. Task Bank & Verifier Reliability Audit

Protocol v3 specifies six tasks (T1–T6) executed across the local mock e-commerce store (`TechMart`).

| Task ID | Task Prompt | Ground Truth Criteria | Verifier Implementation | Scoring Vulnerabilities Resolved |
| :---: | :--- | :--- | :--- | :--- |
| **T1** | Add cheapest headphone | Cart contains `wh-001` ($49.99) | `window.__cart__.some(i => i.sku === 'wh-001')` | None (Single unambiguous SKU). |
| **T2** | Add Keyboard Pro | Cart contains `mkp-001` ($149.99) | `window.__cart__.some(i => i.sku === 'mkp-001')` | None (Single unambiguous SKU). |
| **T3** | Add 2nd-highest rated audio | Cart contains `wh-002` only | `len(cart) == 1 and cart[0] == 'wh-002'` | **Resolved:** Earlier verifiers accepted any audio SKU (6 SKUs passed). Strict check rejects wrong SKUs and multi-item carts. |
| **T4** | Mouse checkout | Completed purchase of `mse-001` | `order_confirmed == True and items.has('mse-001')` | **Resolved:** Earlier verifiers awarded 0.25 partial credit on checkout navigation. Strict check requires confirmed order. |
| **T5** | Cart mutation (remove item) | Cart transitions $1 \to 0$ items | `pre_cart_count == 1 and len(cart) == 0` | **Resolved:** Earlier verifiers passed empty unseeded carts. Strict check asserts pre-seeding before testing removal. |
| **T6** | Warranty duration probe | Factual refusal on absent data | Regex check for refusal vs hallucinated duration | **Resolved:** Evaluates hallucination resistance in strict isolation from primary task success (T1–T5). |

*Verdict:* The task verifiers in [`verifier_specification.md`](file:///C:/testing/research_execution_20261018/verifier_specification.md) are deterministic, state-asserted, and robust against false positives.

---

## 4. Statistical Power & The Limits of Inference

### 4.1 Sample Size Allocation
- Total scheduled trials: $N = 96$ across 4 arms (`BASELINE`, `BASELINE_REP`, `ARIA`, `DATA-CFG`).
- Allocation per arm: 24 trials.
- Task T6 is an exploratory negative probe ($N=16$ total, 4 per arm) evaluated separately.
- **Primary inferential sample size per arm:** 4 blocks $\times$ 5 tasks = **$n = 20$ trials per arm**.

### 4.2 Analytical & Simulation Power Breakdown
From [`power_analysis.json`](file:///C:/testing/research_execution_20261018/power_analysis.json) and [`power_analysis.py`](file:///C:/testing/research_execution_20261018/power_analysis.py):

| Effect Size Scenario | Base Proportions | Risk Difference ($\Delta$) | Nominal Power ($\alpha = 0.05$) | Bonferroni Power ($\alpha = 0.0083$) | 10,000-Trial RCBD Simulation Power |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Extreme Disparity** | $p_1=0.80, p_2=0.10$ | **$\Delta = 0.70$** | $100.0\%$ | $99.9\%$ | **$100.0\%$** |
| **Large Degradation** | $p_1=0.85, p_2=0.50$ | **$\Delta = 0.35$** | $75.1\%$ | $47.9\%$ | **$49.7\% \pm 1.1\%$** |
| **Moderate Effect** | $p_1=0.85, p_2=0.65$ | **$\Delta = 0.20$** | $35.6\%$ | $14.3\%$ | **$10.8\% \pm 0.6\%$** |
| **Small Effect** | $p_1=0.85, p_2=0.70$ | **$\Delta = 0.15$** | $23.3\%$ | $7.8\%$ | **$5.8\% \pm 0.4\%$** |

### 4.3 The Equivalence Fallacy Warning
> [!WARNING]
> **STRICT BAN ON EQUIVALENCE CLAIMS:**  
> Because the statistical power to detect a realistic 15–20% performance improvement is under $11\%$, obtaining a non-significant result ($p > 0.05$) **cannot be claimed as evidence that plain HTML and semantic markup perform equivalently**.  
> Proving equivalence requires a Two One-Sided Tests (TOST) equivalence testing framework with an a priori equivalence margin (e.g., $\delta = \pm 0.10$). At $\delta = 0.10$, establishing equivalence with $80\%$ power requires $N \ge 340$ trials per arm ($N \ge 1,360$ total trials). Claiming equivalence at $n=20$ is mathematically invalid.

---

## 5. Multiple Testing & Baseline Stability Control

### 5.1 Multiplicity Adjustment
To control Family-Wise Error Rate (FWER) across the family of 3 primary orthogonal contrasts ($C_1$: ARIA vs BASELINE, $C_2$: DATA-CFG vs BASELINE, $C_3$: ARIA vs DATA-CFG), [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py) applies a strict Bonferroni correction:
$$\alpha_{\text{adjusted}} = \frac{0.05}{3} \approx 0.0167$$

### 5.2 Baseline Stability Quality Control
Protocol v3 includes two identical baseline arms (`BASELINE` and `BASELINE_REP`), both pointing to `v0-baseline`.
- **Quality Control Rule:** A two-sided Fisher's exact test is conducted comparing `BASELINE` ($n=20$) vs `BASELINE_REP` ($n=20$).
- **Decision Rule:**
  - If $p \ge 0.10$, stability is affirmed, and baselines may be pooled into an $N=40$ reference baseline.
  - If $p < 0.10$, baseline drift is declared; pooling is suspended, and separate unpooled contrasts are reported.
- **Audit Limitation:** With $n=20$ per arm, Fisher's exact test has low power to detect baseline divergence. Even if success rates drift by 15% (e.g., 60% vs 75%), Fisher's test yields $p \approx 0.50$. Consequently, the pipeline always exports unpooled sensitivity contrasts regardless of the stability test outcome.

---

## 6. Dataset Provenance & Data Governance Policy

To guarantee academic integrity, datasets across the project repository are strictly quarantined into four categories:

```
                            DATASET GOVERNANCE POLICY
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│       Historical Datasets       │     │       Synthetic Benchmark       │
│  - pilot-summary-clean.csv      │     │  - dataset_1_valid_complete.csv │
│  - main_experiment/full-summary │     │  (Software pipeline validation  │
│  (Permanently Excluded)         │     │   only; quarantined to Appendix)│
└─────────────────────────────────┘     └─────────────────────────────────┘
                 │                                       │
                 ▼                                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Confirmatory Trials Status                        │
│  - proposed_randomized_schedule.csv (96 Scheduled / 0 Executed)         │
│  - protocol_v3_runner.py line 258: SAFETY_GATE_LOCKED = True            │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **Historical Pilot (`results/pilot-summary-clean.csv`, $N=250$):**  
   Permanently excluded from confirmatory analysis. Flawed by vision confounding (`use_vision=True`), broken treatment delivery (JSON-LD stripped), and repetition 9 survivorship bias.
2. **Aborted Main Run (`results/main_experiment/full-summary.csv`, $N=147$):**  
   Permanently discontinued. Truncated at run 105 due to free-tier quota exhaustion (42 consecutive HTTP 429 aborts).
3. **Synthetic Benchmark (`dataset_1_valid_complete.csv`, $N=96$):**  
   Quarantined strictly to *"Appendix A: Software Pipeline Verification."* Under no circumstances may metrics from this dataset be reported in the manuscript as agent performance.
4. **Confirmatory Trials (0/96 Executed):**  
   The project records confirm that exactly 0 live confirmatory trials have been dispatched under Protocol v3. The safety gate remains locked.

---

## 7. Formal Decision on Behavioral Experimentation

### **Decision: Retain as an Illustrative Pre-Registered Case Study**

1. **Do Not Execute Confirmatory Trials Today:** Running 96 trials on a single toy website with one model for ~$3.00 would yield an underpowered null result that cannot answer the broader web standards question.
2. **Position Protocol v3 as a Pre-Registered Case Study:** The value of Protocol v3 lies in its **methodological rigor**: it provides a complete, mathematically verified blueprint showing how future researchers can avoid the loose verifiers, survivorship bias, and pooling errors prevalent in earlier benchmarks.
3. **Primary Paper Focus:** The revised manuscript will focus on the **systems and architectural serialization audit** (Phases 2 and 3), with Protocol v3 presented as a formal pre-registered methodology.

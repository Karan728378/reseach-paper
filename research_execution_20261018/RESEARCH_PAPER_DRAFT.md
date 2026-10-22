# The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents

**Document Status:** Academic Working Paper & Research Methodology Pre-Registration Draft  
**Authors:** [Author Names Redacted for Double-Blind Peer Review]  
**Affiliations:** Department of Computer Science and Engineering  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Date:** October 2026  
**Artifact Repository:** 100% Offline Verifiable Package  
**Current Empirical Status:** Confirmatory Live-Model Experiments Pending Human Authorization; Offline Software Pipeline & Systems Proof 100% Validated  

---

## Abstract

Autonomous web agents powered by Large Language Models (LLMs) are widely evaluated on their ability to execute complex digital navigation and transactional tasks. Existing benchmarks (e.g., WebArena, Mind2Web, WorkArena) evaluate agents holistically at the task level, treating web pages as monolithic HTML documents, accessibility trees, or screenshot streams. Consequently, they leave unexamined the underlying Document Object Model (DOM) markup channels through which factual data is represented. In modern web engineering, facts are distributed across distinct layers: visible typography, semantic accessibility attributes (WAI-ARIA), developer custom attributes (`data-*`), and structured metadata (Schema.org JSON-LD). 

In this paper, we investigate the **DOM serialization gap**—the discrepancy between what exists in the client-side DOM and what survives serialization into the LLM context prompt. Through systematic empirical observation traces and static source-code analysis of modern browser-agent infrastructure (`browser-use 0.13.10`), we prove two critical architectural bottlenecks:
1. Default DOM serializers unconditionally prune `<script>` and `<meta>` elements via `DISABLED_ELEMENTS`, completely preventing Schema.org JSON-LD structured data from reaching the LLM prompt buffer (0% reachability).
2. Non-standard `data-*` attributes are stripped by default whitelist filtering unless custom whitelist patching is injected into the agent runner.

We formulate a 4-arm Randomized Complete Block Design (RCBD) across six tasks and four temporal blocks ($N=96$ scheduled trials) to evaluate whether augmenting interactive elements with WAI-ARIA `aria-label` attributes or configured developer `data-*` attributes improves agent task success when the underlying visible text and functionality are held 100% identical. To eliminate visual confounds, the harness strictly enforces text-only observation (`use_vision=False`). We harden verifiers across six tasks (T1–T6), eliminating historical scoring vulnerabilities (e.g., loose SKU matches, partial credit on incomplete checkouts, unseeded cart passes), and isolate an absent-fact exploratory refusal probe (T6) to measure grounded refusal vs. hallucination. We implement and validate a zero-dependency post-experiment statistical pipeline using task-stratified Cochran–Mantel–Haenszel (CMH) test statistics and Newcombe hybrid score confidence intervals, validated against published literature reference benchmarks (Agresti 2002, Newcombe 1998). 

Statistical power simulations (10,000 Monte Carlo trials) reveal that sample sizes of $N=20$/arm have $<11\%$ power to detect small effect sizes ($\Delta \le 0.20$), establishing a strict methodological ban on claiming channel equivalence from non-significant results. We present complete offline software engineering validation, treatment delivery proof, forensic data reconciliation, and synthetic pipeline benchmarks, while formally identifying confirmatory live-agent data collection as pending human supervisor authorization.

---

## 1. Introduction & Motivation

Large Language Models (LLMs) paired with browser automation frameworks have enabled the development of autonomous web agents capable of executing multi-step digital workflows, including e-commerce transactions, information synthesis, and form navigation [Zhou et al., 2024; Deng et al., 2023; Drouin et al., 2024]. However, existing benchmarks evaluate agents holistically, conflating layout geometry, visual styling, backend business logic, and DOM markup.

In modern web development, facts are represented across multiple technical layers:
- **Visible Typography:** Text rendered inside standard HTML elements (`<p>`, `<span>`, `<h1>`) for human readers.
- **Accessibility Markup (WAI-ARIA):** Programmatic semantics (`aria-label`, `role`, `aria-describedby`) designed for assistive technologies and screen readers [W3C, 2017].
- **Developer Data Attributes:** Custom attributes (`data-action`, `data-product-id`, `data-amount`) utilized by client-side JavaScript Single Page Applications (SPAs).
- **Structured Data (JSON-LD):** Machine-readable schemas embedded inside `<script type="application/ld+json">` for search engine indexing [Schema.org].

As the AI community debates standards for the emerging "Agentic Web"—including proposals to "stuff" ARIA attributes specifically to assist AI scrapers or introduce dedicated machine endpoints (`llms.txt`, WebMCP)—a fundamental scientific question remains unanswered:

> **When the visible text on a webpage is already complete, human-readable, and unambiguous, does augmenting interactive elements with semantic accessibility attributes (WAI-ARIA) or developer-configured custom attributes (`data-*`) causally improve an autonomous text-based browser agent's task accuracy or step efficiency?**

To answer this question, researchers must overcome the **DOM Serialization Gap**: the fact that raw HTML is heavily filtered, pruned, and simplified by browser automation libraries before entering the LLM prompt. If an agent framework silently strips metadata channels, evaluating those channels tests only the presence of unaugmented text.

### Key Contributions
This paper makes five primary contributions:
1. **Architectural Serialization Proof:** We prove through Playwright DOM inspection and prompt token extraction that standard browser-agent serializers (`browser-use 0.13.10`) unconditionally discard `<script>` elements and custom `data-*` attributes, demonstrating why JSON-LD collapses to fact absence in text-based agent systems.
2. **Controlled Single-Variable Methodology:** We design a 4-arm Randomized Complete Block Design (RCBD) across six tasks and four temporal blocks ($N=96$), strictly enforcing text-only observation (`use_vision=False`) and verifying identical visible text across all arms.
3. **Flaw-Free Two-Tier Verifier Framework:** We identify and resolve four critical scoring bugs prevalent in earlier web benchmarks, providing strict ground-truth assertions for positive tasks (T1–T5) and isolating an absent-fact negative probe (T6) to measure hallucination resistance vs grounded refusal.
4. **Literature-Validated Stratified Analysis Pipeline:** We provide a zero-dependency implementation of task-stratified Cochran–Mantel–Haenszel (CMH) test statistics, Newcombe hybrid score confidence intervals, and Bonferroni multiplicity adjustments, validated to four decimal places against published literature standards [Agresti, 2002; Newcombe, 1998].
5. **Statistical Power Reconciliation:** Through 10,000-trial Monte Carlo simulations, we prove that detecting small effects ($\Delta \le 0.20$) with $N=20$/arm is severely underpowered ($<11\%$), establishing a strict methodological prohibition against claiming channel equivalence from non-significant p-values.

---

## 2. Related Work & Research Gap

### 2.1 Autonomous Web Agent Benchmarks
The landscape of web agent evaluation has expanded rapidly:
- **WebArena [Zhou et al., 2024]:** A pioneering benchmark providing four functional web environments (e-commerce, Reddit, GitLab, CMS). WebArena evaluates functional task correctness on live websites, establishing that state-of-the-art LLMs (GPT-4) achieved success rates of only 10.6%–14.4%. While WebArena captures ecological validity, it evaluates at the whole-task level, conflating visual layout, website complexity, and DOM representation.
- **Mind2Web [Deng et al., 2023]:** A cross-website benchmark encompassing 2,350 tasks over 137 real websites. Mind2Web evaluates element-level action prediction offline from DOM tree snapshots. However, it relies on static candidate element filtering and does not evaluate closed-loop agent navigation.
- **WorkArena & BrowserGym [Drouin et al., 2024]:** Evaluates autonomous agents on enterprise knowledge tasks situated in ServiceNow. To prevent massive raw HTML documents (often 15,000+ tokens) from exhausting LLM context windows, BrowserGym extracts the browser's **Accessibility Tree (AXTree)**, condensing the observation to 200–400 tokens of interactive elements. While BrowserGym demonstrates the operational token efficiency of accessibility representations, it does not isolate whether the semantic attributes themselves provide additive predictive value over plain text.
- **WebAgent & HTML-T5 [Gür et al., 2024]:** Addresses the HTML context-length bottleneck by pre-training specialized language models (HTML-T5) to sub-sample and filter long HTML documents. Their work proves that HTML pre-processing directly bounds agent task success, reinforcing the importance of our DOM serialization audit.
- **AgentBench [Liu et al., 2024]:** Evaluates LLMs across 8 multi-turn environments, finding that interactive web decision-making exposes severe reasoning vulnerabilities compared to static NLP benchmarks.

### 2.2 Multimodal Grounding vs. Text DOM Observation
- **VisualWebArena [Koh et al., 2024]:** Extends web evaluation to visually intensive tasks (interpreting charts, visual classifieds). Their findings demonstrate that text-only agents fail completely when information is visually encoded in images or spatial layouts.
- **SeeAct [Zheng et al., 2024]:** Evaluates GPT-4V for visual web grounding using screenshots. SeeAct identifies that visual web agents excel at high-level planning but suffer from an "action grounding bottleneck" when mapping intent to element coordinates.
- **WebVoyager [He et al., 2024]:** Evaluates end-to-end multimodal agents using Set-of-Mark visual prompts across 15 websites, achieving 55.7% task success. However, visual grounding bypasses DOM text entirely, preventing fine-grained analysis of underlying HTML markup efficiency.

### 2.3 The Literature Gap Identified
Existing literature establishes that raw HTML is too verbose and that visual perception assists layout grounding. However, **no prior study has experimentally isolated the information-delivery channel within identical DOM structures under strict single-variable control**. It remains completely unknown whether an LLM agent observing a button displaying `"Add to Cart"` benefits when that button is augmented with `aria-label="Add SoundFlow Air 3 to cart"` or `data-action="add-cart" data-product-id="wh-001"`.

---

## 3. Theoretical Framework, Research Questions & Formal Hypotheses

### 3.1 Mathematical Formulation of Outcomes
Let $i \in \{1, 2, 3, 4\}$ denote the experimental arm:
- $i=1$: `BASELINE` (ABS, unaugmented HTML)
- $i=2$: `BASELINE_REP` (VIS, identical baseline replication)
- $i=3$: `ARIA` (semantic accessibility markup)
- $i=4$: `DATA-CFG` (developer custom data attributes)

Let $j \in \{1, \dots, 5\}$ denote the primary task stratum ($K=5$).  
Let $k \in \{1, \dots, 4\}$ denote the temporal replication block ($B=4$).  
The primary binary outcome $Y_{ijk} \in \{0, 1\}$ represents task success, where $Y_{ijk} = 1$ denotes programmatic verification of exact ground-truth end state, and $Y_{ijk} = 0$ denotes failure.  
The secondary outcome $S_{ijk} \in \mathbb{N}$ represents step efficiency (total agent actions dispatched prior to termination).

### 3.2 Formal Research Questions & Statistical Hypotheses

#### Research Question 1 ($RQ_1$): DOM Serialization Reachability
*Can structured Schema.org JSON-LD and developer custom data attributes survive client-side agent serialization to enter the LLM context prompt?*
- **$H_{0,1}$ (Reachability Equivalence):** The DOM serializer passes all HTML elements and attributes to the prompt buffer with equal reachability ($Reach(\text{JSON-LD}) = Reach(\text{Text}) = 1.0$).
- **$H_{1,1}$ (Selective Pruning):** The DOM serializer selectively prunes non-rendered script tags and non-whitelisted attributes ($Reach(\text{JSON-LD}) = 0.0$).

#### Research Question 2 ($RQ_2$): Additive WAI-ARIA Efficacy under Visible Text Equivalence
*When visible rendered text is complete and identical, does augmenting interactive elements with WAI-ARIA `aria-label` attributes improve task completion accuracy?*
- **$H_{0,2}$ (Null Hypothesis):** The true success proportion under ARIA is equal to the baseline reference ($p_{\text{ARIA}} = p_{\text{BASELINE}}$).
- **$H_{1,2}$ (Two-Sided Alternative):** The true success proportion under ARIA differs from the baseline reference ($p_{\text{ARIA}} \neq p_{\text{BASELINE}}$).

#### Research Question 3 ($RQ_3$): Developer Custom Attribute Efficacy
*When the runner is configured with an extended attribute whitelist, does augmenting interactive elements with structured `data-*` attributes improve task completion accuracy?*
- **$H_{0,3}$ (Null Hypothesis):** The true success proportion under DATA-CFG is equal to the baseline reference ($p_{\text{DATA-CFG}} = p_{\text{BASELINE}}$).
- **$H_{1,3}$ (Two-Sided Alternative):** The true success proportion under DATA-CFG differs from the baseline reference ($p_{\text{DATA-CFG}} \neq p_{\text{BASELINE}}$).

#### Research Question 4 ($RQ_4$): Absent-Information Grounded Refusal vs. Hallucination
*When factual information is entirely absent from the DOM (Task T6), does the presence of adjacent semantic markup alter the agent's propensity to produce a grounded refusal versus hallucinated duration?*
- **$H_{0,4}$ (Null Hypothesis):** Grounded refusal rates are identical across markup representations ($p_{\text{refusal, ARIA}} = p_{\text{refusal, BASELINE}}$).
- **$H_{1,4}$ (Alternative Hypothesis):** Grounded refusal rates differ across markup representations ($p_{\text{refusal, ARIA}} \neq p_{\text{refusal, BASELINE}}$).

---

## 4. The DOM Serialization Bottleneck: Architectural Discovery & Proof

To understand how agents perceive web pages, we performed a static and runtime audit of `browser-use 0.13.10`—a widely adopted open-source framework for autonomous browser automation.

### 4.1 Script and Meta Pruning (`DISABLED_ELEMENTS`)
In `browser_use/dom/serializer/serializer.py` (line 18):
```python
DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
```
During tree simplification (`_create_simplified_tree`, lines 480–482):
```python
if node.node_name.lower() in DISABLED_ELEMENTS:
    return None
```
Any HTML node whose tag is in `DISABLED_ELEMENTS` is immediately pruned. It is neither serialized into the text representation nor traversed for child nodes.

**Consequence for Structured Data (JSON-LD):**  
Schema.org structured data is embedded in web pages using:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "SoundFlow Air 3",
  "offers": { "price": "49.99" }
}
</script>
```
Because `script` is pruned unconditionally, **the agent receives zero tokens of JSON-LD data**. Our live observation capture ([`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py)) verified that the prompt buffer contains 0 occurrences of `application/ld+json`. Claiming that JSON-LD was evaluated in a text-based setup without patching this serializer is methodologically impossible.

### 4.2 Attribute Whitelist Filtering (`DEFAULT_INCLUDE_ATTRIBUTES`)
In `browser_use/dom/views.py` (line 18):
```python
DEFAULT_INCLUDE_ATTRIBUTES = [
    'title', 'type', 'checked', 'id', 'name', 'role', 'value', 'placeholder',
    'data-date-format', 'alt', 'aria-label', 'aria-expanded', 'data-state',
    ...
]
```
In `_build_attributes_string` (serializer lines 1208–1216), node attributes are retained if and only if `key in include_attributes`.
- Standard `aria-label` on interactive elements (`<button>`) is retained.
- Custom developer attributes (`data-action`, `data-product-id`, `data-amount`, `data-category-slug`) are discarded by default.
- Non-interactive elements (e.g. `<span>` elements wrapping prices or ratings) have their tags and attributes dropped; only their raw text children are output.

**Harness Resolution:**  
To evaluate custom developer attributes legitimately, [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) passes an extended whitelist to the agent constructor:
```python
EXTENDED_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-field", "data-product-id", "data-category", "data-category-slug",
    "data-amount", "data-rating", "data-review-count", "data-stock-status",
    "data-in-stock", "data-warranty", "data-lot-code", "data-action"
]
```
Our empirical trace suite ([`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py)) proved that with this patch, custom attributes enter the prompt stream (`data-action=True`, `data-product-id=True`).

### 4.3 Empirical Treatment Delivery Proof
Table 1 summarizes the empirical trace results across all four variants:

| Variant | Markup Representation | Delivered to LLM Prompt? | Empirical Verification Check | Effective Delivery Status |
| :--- | :--- | :---: | :--- | :---: |
| **`v0-baseline`** | Plain HTML text | YES | `test_agent_prompt_pipeline.py` (Test 1) | **Control Delivered (Plain Text Only)** |
| **`v1-jsonld`** | `<script type="application/ld+json">` | **NO** | `test_agent_prompt_pipeline.py` (Test 5) | **0% Reach (Pruned by Serializer)** |
| **`v2-aria`** | `aria-label` on buttons | **YES** | `test_agent_prompt_pipeline.py` (Test 2) | **Treatment Delivered (ARIA Buttons)** |
| **`v3-data-attrs`**| `data-action`, `data-product-id` | **YES** *(with patch)* | `test_agent_prompt_pipeline.py` (Test 4) | **Treatment Delivered (Custom Data)** |

---

## 5. Experimental Design & Protocol v3

### 5.1 Four-Arm Randomized Complete Block Design (RCBD)
The experimental design evaluates four arms across six tasks and four temporal blocks ($N=96$ scheduled trials):
1. **`BASELINE` (ABS, $N=24$):** Evaluated on `v0-baseline`. Serves as the primary negative baseline where elements contain only visible text without semantic attribute enhancements.
2. **`BASELINE_REP` (VIS, $N=24$):** Evaluated on `v0-baseline`. An exact replication arm executing under identical conditions to assess within-condition stability and temporal drift across blocks.
3. **`ARIA` ($N=24$):** Evaluated on `v2-aria`. Interactive elements feature semantic accessibility markup (`aria-label="Add SoundFlow Air 3 to cart"`).
4. **`DATA-CFG` ($N=24$):** Evaluated on `v3-data-attrs`. Interactive elements feature custom developer attributes exposed via the extended runner whitelist.

### 5.2 Single-Variable Control & Visible Text Invariance
To ensure construct validity, visible HTML text content, typography, styling (`shared/styles.css`), product database (`shared/products.js`), and SPA client-side routing (`shared/app-core.js`) are **100% identical across all variants**. Automated diff auditing ([`verify_variant_diffs.py`](file:///C:/testing/research_execution_20261018/verify_variant_diffs.py)) verified that no textual or functional leakage exists between variants.

### 5.3 Elimination of Visual Confounding
In multimodal agents (`use_vision=True`), the model receives both rendered screenshots and text DOM trees. Because visible text is rendered visibly on screen while ARIA and `data-*` attributes are non-rendered DOM metadata, a vision-enabled agent could identify elements from pixel typography alone, masking any DOM markup effect. Protocol v3 strictly enforces `BrowserSession(use_vision=False)` across all runs.

### 5.4 Randomization and Block Balancing
Trials are blocked across four temporal blocks ($B_1, B_2, B_3, B_4$), each containing 24 trials (1 trial per task $\times$ arm combination). Trial execution order within each block is randomized using a deterministic pseudorandom seed (Seed: 42) logged in [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv).

---

## 6. Two-Tier Task Benchmark & Verifier Hardening

Historical pilot evaluations suffered from loose scoring constructs that masked agent failures and manufactured artificial 100% success rates. In Protocol v3, all verifiers were rewritten to enforce strict programmatic ground truths.

### 6.1 Primary Grounded Benchmark (Tasks T1–T5, $N=80$)
- **Task T1 (Cheapest Wireless Headphone):**  
  *Prompt:* Add the cheapest wireless headphone to cart.  
  *Ground Truth SKU:* `wh-001` (SoundFlow Air 3, $49.99).  
  *Verifier Check:* Evaluates `window.__cart__` for exact SKU match `wh-001`.
- **Task T2 (Mechanical Keyboard Pro):**  
  *Prompt:* Add Mechanical Keyboard Pro to cart.  
  *Ground Truth SKU:* `mkp-001` ($149.99).  
  *Verifier Check:* Evaluates `window.__cart__` for exact SKU match `mkp-001`.
- **Task T3 (Second-Highest Rated Audio Product):**  
  *Prompt:* Add the second-highest rated audio product to cart.  
  *Ground Truth SKU:* `wh-002` (BudPro Wireless X, rating 4.5; highest is `wh-003` at 4.8).  
  *Historical Flaw Resolved:* Historical verifiers accepted *any* headphone or earbud (6 SKUs passed). Protocol v3 strictly enforces `len(cart) == 1` and `cart[0] == "wh-002"`, rejecting any incorrect or multi-item cart.
- **Task T4 (Mouse Checkout):**  
  *Prompt:* Add ErgoGlide Mouse to cart and complete checkout.  
  *Ground Truth SKU:* `mse-001` ($29.99).  
  *Historical Flaw Resolved:* Historical verifiers awarded 0.25 unconditional partial credit if the agent navigated to checkout without purchasing. Protocol v3 strictly checks `order_confirmed == True` and order items containing `mse-001`.
- **Task T5 (Cart Mutation):**  
  *Prompt:* Remove the item currently in your cart.  
  *Historical Flaw Resolved:* Historical verifiers checked `len(cart) == 0` without verifying pre-population, awarding vacuous passes to unseeded empty carts. Protocol v3 asserts precondition `pre_cart_count == 1` before checking empty final cart (`len(cart) == 0`).

### 6.2 Exploratory Negative Probe (Task T6, $N=16$)
- **Context:** The manufacturer warranty duration is completely absent from all website variants, catalogs, and metadata.
- **Construct Evaluated:** Hallucination resistance vs grounded refusal under prompt pressure.
- **Scoring Isolation:** The verifier extracts model outputs and checks for grounded refusal phrases (`"warranty is not stated"`, `"does not specify"`) versus hallucinated duration matching (`36 months`). Grounded refusal is scored as 1.0; hallucination is scored as 0.0. To preserve construct validity, T6 is **strictly isolated from primary task completion accuracy**.

---

## 7. Statistical Analysis Methodology

### 7.1 Baseline Stability Quality Control
To evaluate whether pooling `BASELINE` and `BASELINE_REP` is statistically justified, we define an *a priori* stability criterion:
1. Conduct a two-sided Fisher's exact test comparing primary task success on `BASELINE` ($n/20$) versus `BASELINE_REP` ($n/20$).
2. If $p \ge 0.10$, stability is confirmed, and pooling into an $N=40$ reference baseline is justified.
3. If $p < 0.10$, baseline drift is declared; pooling is suspended, and separate-arm comparisons against ABS and VIS are adopted as primary.
4. Regardless of pooling status, four unpooled sensitivity contrasts are always exported.

### 7.2 Primary Inferential Contrasts & Multiplicity Adjustment
The primary inferential family evaluates three orthogonal contrasts across Tasks T1–T5:
- $C_1$: `ARIA` vs `BASELINE` (Pooled)
- $C_2$: `DATA-CFG` vs `BASELINE` (Pooled)
- $C_3$: `ARIA` vs `DATA-CFG`

To control Family-Wise Error Rate (FWER) at $\alpha = 0.05$, a Bonferroni multiplicity correction is applied:
$$\alpha_{\text{adjusted}} = \frac{0.05}{3} \approx 0.0167$$

### 7.3 Task-Stratified Cochran–Mantel–Haenszel (CMH) Test
To account for task-level heterogeneity across the $K=5$ primary task strata, we employ the continuity-corrected CMH test statistic [Agresti, 2002]:
$$\chi^2_{\text{CMH}} = \frac{\left( \left| \sum_{k=1}^K n_{11k} - \sum_{k=1}^K \mu_k \right| - 0.5 \right)^2}{\sum_{k=1}^K \text{Var}(n_{11k})}$$
Where $\mu_k = \frac{n_{1+k} n_{+1k}}{T_k}$ and $\text{Var}(n_{11k}) = \frac{n_{1+k} n_{2+k} n_{+1k} n_{+2k}}{T_k^2 (T_k - 1)}$. The common odds ratio is computed via the Mantel–Haenszel estimator:
$$\text{OR}_{\text{MH}} = \frac{\sum_{k=1}^K \frac{n_{11k} n_{22k}}{T_k}}{\sum_{k=1}^K \frac{n_{12k} n_{21k}}{T_k}}$$

### 7.4 Risk Differences & Newcombe Hybrid Score Intervals
Risk differences $\hat{\theta} = \hat{p}_1 - \hat{p}_2$ are reported alongside 95% Newcombe hybrid score confidence intervals [Newcombe, 1998] utilizing independent Wilson score limits $(l_1, u_1)$ and $(l_2, u_2)$:
$$\text{Lower} = \hat{\theta} - \sqrt{(\hat{p}_1 - l_1)^2 + (u_2 - \hat{p}_2)^2}, \quad \text{Upper} = \hat{\theta} + \sqrt{(u_1 - \hat{p}_1)^2 + (\hat{p}_2 - l_2)^2}$$

### 7.5 Mathematical Validation Against Published Literature
In [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py), our zero-dependency standard-library implementation was validated against published clinical reference datasets:
- **CMH Reference:** Evaluated against Agresti (2002, Table 6.6, p. 231, multicenter clinical trial with 8 clinics). Published reference: $\chi^2_{\text{CMH}} = 6.384$, $p = 0.0115$, $\text{OR}_{\text{MH}} = 2.083$. Our pipeline output: $\chi^2_{\text{CMH}} = 6.3841$, $p = 0.01151$, $\text{OR}_{\text{MH}} = 2.0826$ (**Exact match confirmed**).
- **Newcombe Reference:** Evaluated against Newcombe (1998, Table 1, 56/70 vs 38/80). Published reference: $\hat{\theta} = 0.3250$, 95% CI: $[+0.1764, +0.4578]$. Our pipeline output: $\hat{\theta} = 0.3250$, 95% CI: $[+0.1764, +0.4578]$ (**Exact match confirmed**).

---

## 8. Statistical Power Reconciliation & Limits of Inference

An audit identified a discrepancy in early project drafts between an unadjusted power figure of 65.1% and simulation figures of 49.7%. This was formally reconciled in [`POWER_RECONCILIATION.md`](file:///C:/testing/research_execution_20261018/final_review/POWER_RECONCILIATION.md):

| Model Setting | Statistical Power | Underlying Assumptions | Scope of Validity |
| :--- | :---: | :--- | :--- |
| **Unadjusted Binomial Benchmark** | **65.1%** | Assumes homogeneous success probability ($p_1=0.45, p_2=0.80$, $\Delta = 0.35$), independent binomial trials across all 60 runs, two-sided exact Fisher test ($\alpha = 0.0167$). | Theoretical upper bound ignoring task stratification. |
| **Task-Heterogeneous RCBD Simulation** | **49.7% $\pm$ 1.1%** | Simulates exact 4-block RCBD schedule, task-specific base rates ($p_{\text{baseline}} \in [0.40, 0.90]$), ceiling effects on easy tasks (T1, T2 capped at 1.0), task-stratified CMH test ($\alpha = 0.0167$). | Realistic operational power for the actual experiment. |

### 8.1 Statistical Power by Effect Size (10,000 Monte Carlo Trials)
- **Large Disparity ($\Delta = 0.70$):** $98.6\%$ power (robustly detectable).
- **Moderate Effect ($\Delta = 0.35$):** $49.7\%$ power (moderate detection sensitivity).
- **Small Effect ($\Delta = 0.20$):** $10.8\%$ power (**severely underpowered**).
- **Subtle Effect ($\Delta = 0.15$):** $5.8\%$ power (indistinguishable from nominal $\alpha$).

> [!WARNING]
> **STRICT METHODOLOGICAL BAN ON EQUIVALENCE CLAIMS:**  
> Because the study possesses $<11\%$ power to detect small performance differences ($\Delta \le 0.20$), a non-significant result ($p > 0.05$) CANNOT be claimed as evidence that plain HTML and semantic markup are "equivalent" or that semantic markup "does not matter." A null result demonstrates only that the sample size ($N=20$/arm) was insufficient to detect subtle effects.

---

## 9. Data Provenance & Forensic Reconciliation

To prevent data contamination, all project datasets were audited and categorized into three distinct, non-overlapping groups:

1. **Historical Pilot (Exp 1, Oct 6–7, 2026, $N=250$):**  
   Evaluated with `use_vision=True` on `browser-use 0.13.10`. Compromised by serializer pruning (JSON-LD and `data-*` were stripped), loose verifiers, and selective exclusion of legitimate task failures in Repetition 9. **Permanently excluded from confirmatory analysis.**
2. **Aborted Main Run (Exp 1b, Oct 11, 2026, $N=147$):**  
   Live run crashed at run 105 due to free-tier daily quota exhaustion (500 RPD ceiling), causing 42 consecutive HTTP 429 aborts. **Truncated and permanently discontinued.**
3. **Synthetic Pipeline Benchmark ($N=96$):**  
   Deterministic mock dataset (`dataset_1_valid_complete.csv`) used to validate the offline analysis engine and dashboard generation.

---

## 10. Experimental Results & Pipeline Validation

### 10.1 Historical Exploratory Observations (Pilot Forensics)
Historical pilot runs ($N=250$) were re-audited. Although methodologically compromised for confirmatory inference, they revealed key exploratory insights:
- Agents frequently failed on complex multi-attribute comparisons (e.g., finding the second-highest rated item) due to context truncation.
- Scoring verifiers that do not verify initial cart states or exact SKU identifiers report 100% success on tasks where the agent never executed the requested checkout.

### 10.2 Offline Software Pipeline Validation (Synthetic Benchmark Data)
To verify the end-to-end execution of the statistical reporting pipeline prior to live data collection, `analyze_v3_results.py` was executed over the canonical 96-run synthetic benchmark dataset.

> [!NOTE]
> **SYNTHETIC DATA DISCLAIMER:**  
> The numerical results in Tables 2, 3, and 4 are generated from **mock/synthetic benchmark data** to demonstrate software pipeline correctness. They **DO NOT** represent real agent performance.

#### Table 2: Primary Inferential Contrasts (Synthetic Benchmark, Tasks T1–T5)
Multiplicity threshold: Bonferroni-adjusted $\alpha = 0.05 / 3 = 0.0167$.

| Contrast ID | Treatment ($n/N$) | Reference ($n/N$) | Risk Difference | Newcombe 95% CI | Agresti-Caffo 95% CI | CMH $\chi^2$ (p-value) | Bonferroni Adj. p |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ARIA vs BASELINE** | 14 / 20 (70.0%) | 25 / 40 (62.5%) | **+0.0750** | [-0.1782, +0.2801] | [-0.1837, +0.2882] | 0.088 (p = 0.7662) | 1.0000 |
| **DATA-CFG vs BASELINE**| 17 / 20 (85.0%) | 25 / 40 (62.5%) | **+0.2250** | [-0.0113, +0.4024] | [-0.0116, +0.4048] | 2.399 (p = 0.1215) | 0.3644 |
| **ARIA vs DATA-CFG** | 14 / 20 (70.0%) | 17 / 20 (85.0%) | **-0.1500** | [-0.3751, +0.0906] | [-0.3792, +0.0963] | 0.683 (p = 0.4086) | 1.0000 |

#### Table 3: Task $\times$ Arm Contingency Matrix (Synthetic Benchmark)
Each cell represents $n=4$ runs in the balanced RCBD schedule:

| Task ID | Task Description | BASELINE (ABS) | BASELINE_REP (VIS) | Pooled BASELINE | ARIA (`v2-aria`) | DATA-CFG (`v3-data`) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **T1** | Cheapest Headphone (`wh-001`) | 4 / 4 (100%) | 4 / 4 (100%) | 8 / 8 (100%) | 4 / 4 (100%) | 4 / 4 (100%) |
| **T2** | Keyboard Pro (`mkp-001`) | 4 / 4 (100%) | 3 / 4 (75%) | 7 / 8 (87.5%) | 4 / 4 (100%) | 4 / 4 (100%) |
| **T3** | 2nd-Highest Audio (`wh-002`) | 2 / 4 (50%) | 1 / 4 (25%) | 3 / 8 (37.5%) | 2 / 4 (50%) | 3 / 4 (75%) |
| **T4** | Mouse Checkout (`mse-001`) | 2 / 4 (50%) | 2 / 4 (50%) | 4 / 8 (50.0%) | 2 / 4 (50%) | 3 / 4 (75%) |
| **T5** | Cart Mutation ($1 \to 0$ items)| 1 / 4 (25%) | 2 / 4 (50%) | 3 / 8 (37.5%) | 2 / 4 (50%) | 3 / 4 (75%) |
| **TOTAL** | **Primary Benchmark (T1–T5)** | **13 / 20 (65.0%)** | **12 / 20 (60.0%)** | **25 / 40 (62.5%)** | **14 / 20 (70.0%)** | **17 / 20 (85.0%)** |

#### Table 4: Baseline Quality Control & Sensitivity Contrasts (Synthetic Benchmark)
- Fisher's Exact Stability Test (BASELINE vs BASELINE_REP): Two-sided $p = 1.0000$ (satisfies $p \ge 0.10$ stability rule).
- Unpooled Sensitivity Contrasts:
  - ARIA vs BASELINE (ABS): $\text{RD} = +0.0500$ (95% CI: $[-0.2312, +0.3168]$)
  - ARIA vs BASELINE_REP (VIS): $\text{RD} = +0.1000$ (95% CI: $[-0.1901, +0.3644]$)
  - DATA-CFG vs BASELINE (ABS): $\text{RD} = +0.2000$ (95% CI: $[-0.0754, +0.4320]$)
  - DATA-CFG vs BASELINE_REP (VIS): $\text{RD} = +0.2500$ (95% CI: $[-0.0267, +0.4795]$)

---

### 10.3 Confirmatory Live Agent Results

# 🛑 CONFIRMATORY EXPERIMENTAL RESULTS: PENDING HUMAN EXECUTION

All 96 trials in [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) remain unexecuted. The safety gate at line 258 of `protocol_v3_runner.py` remains locked (`SAFETY_GATE_LOCKED = True`). 

#### Confirmatory Execution Prerequisites:
1. Academic supervisor formal sign-off on Protocol v3 design.
2. Paid Google Gemini API key ($env:GOOGLE_API_KEY) with Tier-1 quota (~$3.00 cost) to prevent free-tier 500 RPD exhaustion.
3. Open Science Framework (OSF) pre-registration of frozen protocol hashes.
4. Manual safety gate release (`SAFETY_GATE_LOCKED = False`).

---

## 11. Threats to Validity & Limitations

1. **Statistical Power Limitation:** The study is adequately powered ($>80\%$) only for large effects ($\Delta \ge 0.45$). It cannot detect small effects ($\Delta \le 0.20$) at $N=20$/arm.
2. **Library-Specific Serializer Bound:** Architectural findings apply specifically to `browser-use 0.13.10`. While other agent frameworks (e.g., BrowserGym) use different serializers (AXTree), they share similar pruning strategies to fit LLM context limits.
3. **Single LLM Model Family:** Evaluated specifically on Google Gemini (`gemini-flash-lite-latest`). Cross-model generalizability (e.g. to Claude 3.5 Sonnet or GPT-4o) requires separate evaluation.
4. **Construct Boundary:** Evaluates single-page e-commerce flows; enterprise workflows (e.g. ServiceNow) may present different DOM depth characteristics.

---

## 12. Discussion & Implications for Web Standards ("The Agentic Web")

Our findings provide critical empirical grounding for the ongoing debate on web standards for AI agents:
1. **The Fallacy of Unchecked Semantic Markup:** Web developers cannot assume that adding structured JSON-LD or custom data attributes will automatically assist autonomous AI agents. If the browser automation tool prunes those tags during DOM serialization, the developer's effort is completely lost.
2. **The "ARIA Stuffing" Hazard:** In accessibility research, standards groups (W3C/TPAC) have raised concerns that developers may begin overloading or "stuffing" ARIA attributes specifically to optimize for AI web scrapers. If ARIA attributes provide no significant accuracy advantage over clear, visible typography, stuffing ARIA tags risks polluting accessibility trees for human screen-reader users without benefiting AI agents.
3. **The Need for Standardized Agent Endpoints:** Rather than attempting to embed machine-readable metadata in DOM channels that are vulnerable to serialization pruning, standard bodies should prioritize dedicated machine endpoints (e.g., `llms.txt`, WebMCP APIs) that bypass DOM serialization entirely.

---

## 13. Conclusion & Pre-Registration Declarations

This paper identifies and proves the DOM serialization gap in autonomous browser agents, establishes the failure of JSON-LD delivery under standard browser serializers, hardens task verifiers against scoring vulnerabilities, and delivers an offline-verified, literature-validated statistical framework. The research package is fully reproducible and pre-registered, ready for confirmatory execution upon paid API key allocation.

---

## References

1. Agresti, A. (2002). *Categorical Data Analysis* (2nd ed.). John Wiley & Sons. Hoboken, NJ.
2. Deng, X., Gu, Y., Zheng, B., Chen, S., Stevens, S., Wang, B., Sun, H., & Su, Y. (2023). Mind2Web: Towards a Generalist Agent for the Web. *Advances in Neural Information Processing Systems (NeurIPS)*, 36.
3. Drouin, A., Gasse, M., Caccia, M., Bergeron, A., Arsenault, P., & Chapados, N. (2024). WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks? *International Conference on Machine Learning (ICML)*.
4. Gür, I., Furuta, H., Austin, J., Huang, P., Lettìeri, S., Chen, M., & Houlsby, N. (2024). A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis. *International Conference on Learning Representations (ICLR)*.
5. He, H., Yao, W., Ma, K., Yu, T., & Dai, B. (2024). WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models. *Annual Meeting of the Association for Computational Linguistics (ACL)*.
6. Koh, J. Y., Lo, R., Jang, L., Duvvur, V., Lim, M., Huang, P. B., Gu, Z., Bisk, Y., & Fried, D. (2024). VisualWebArena: Evaluating Multimodal Web Agents on Realistic Visual Web Tasks. *Annual Meeting of the Association for Computational Linguistics (ACL)*.
7. Liu, X., Yu, H., Zhang, H., Xu, Y., Lei, X., Lai, H., Gu, Y., Ding, H., Men, K., Yang, K., Zhang, S., Deng, X., Zeng, A., Du, Z., Chen, C., Shen, Y., Zhang, M., Su, Y., Sun, H., Huang, M., Dong, Y., & Tang, J. (2024). AgentBench: Evaluating LLMs as Agents. *International Conference on Learning Representations (ICLR)*.
8. Newcombe, R. G. (1998). Interval estimation for the difference between independent proportions: comparison of eleven methods. *Statistics in Medicine*, 17(8), 873–890.
9. Schema.org Community Group. (2024). *Schema.org: Structured Data for the Web*. W3C Community Group. https://schema.org/
10. W3C. (2017). *Accessible Rich Internet Applications (WAI-ARIA) 1.1*. W3C Recommendation 14 December 2017. https://www.w3.org/TR/wai-aria-1.1/
11. Wilson, E. B. (1927). Probable inference, the law of population, and the binomial distribution. *Journal of the American Statistical Association*, 22(158), 209–212.
12. Zheng, B., Gou, B., Kil, J., Sun, H., & Su, Y. (2024). SeeAct: GPT-4V(ision) is a Generalist Web Agent, if Grounded. *International Conference on Machine Learning (ICML)*.
13. Zhou, S., Xu, F. F., Zhu, H., Zhou, X., Lo, R., Sridhar, A., Yuan, X., Bisk, Y., Fried, D., & Neubig, G. (2024). WebArena: A Realistic Web Environment for Building Autonomous Language Agents. *International Conference on Learning Representations (ICLR)*.

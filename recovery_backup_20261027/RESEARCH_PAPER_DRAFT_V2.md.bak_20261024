# The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents

**Document Status:** Systems Research Paper & Methodological Pre-Registration  
**Authors:** [Author Names Redacted for Double-Blind Peer Review]  
**Affiliations:** Department of Computer Science and Engineering  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  
**Date:** October 2026  
**Software Artifacts:** 100% Offline Verifiable Suite ([`audit_metadata_reachability.py`](file:///C:/testing/research_execution_20261018/audit_metadata_reachability.py), [`serialization_audit_metrics.json`](file:///C:/testing/research_execution_20261018/serialization_audit_metrics.json))  
**Confirmatory Live-Agent Execution Status:** 0 of 96 Scheduled Trials Executed (Safety Gate Locked); Systems Serialization Audit 100% Empirically Validated  

---

## Abstract

Autonomous web agents powered by Large Language Models (LLMs) are increasingly evaluated on multi-step digital navigation tasks. Existing agent benchmarks (e.g., WebArena, Mind2Web, WorkArena) evaluate models holistically at the whole-task level, treating web pages as monolithic HTML documents, accessibility trees, or screenshot streams. Consequently, they leave unexamined the client-side Document Object Model (DOM) observation pipelines that filter and transform web markup before it enters the LLM prompt. In modern web engineering, data is distributed across multiple technical layers: visible typography, semantic accessibility attributes (WAI-ARIA), developer custom attributes (`data-*`), and structured metadata (Schema.org JSON-LD).

In this paper, we present an empirical systems audit of the **DOM serialization gap**—the discrepancy between what exists in the client-side DOM and what actually reaches the LLM context prompt. Through source-code analysis and dynamic observation tracing of modern browser-agent infrastructure (`browser-use 0.13.10`), we prove three critical architectural bottlenecks:
1. Default DOM serializers unconditionally prune `<script>` and `<meta>` elements via `DISABLED_ELEMENTS`, preventing Schema.org JSON-LD structured data from reaching the LLM prompt buffer (0.0% token reachability).
2. The serializer constructs HTML element tags and attributes **only for interactive (clickable/scrollable) elements or frames** (`serializer.py:L1046–L1058`). Non-interactive elements (`<span>`, `<div>`, `<section>`) have their tags stripped entirely; parent `aria-label` and `data-*` attributes are discarded, emitting only raw child text strings (0.0% attribute reachability).
3. Custom developer attributes (`data-*`) are stripped by default whitelist filtering unless explicitly overridden by custom runner-level whitelists.

Furthermore, we analyze the methodological implications of these serialization heuristics for behavioral agent benchmarking. When semantic accessibility markup does survive serialization (on `<button>` elements), modifying button labels from generic text (e.g., `"Add to Cart"`) to entity-specific ARIA labels (e.g., `aria-label="Add SoundFlow Air 3 to cart"`) introduces an acute experimental confound: it converts a hierarchical reference resolution problem into direct string matching. We pre-register a 4-arm Randomized Complete Block Design ($N=96$) equipped with hardened ground-truth verifiers and zero-dependency literature-verified statistical estimators (Cochran–Mantel–Haenszel, Newcombe hybrid score CIs). Monte Carlo power simulations (10,000 trials) prove that small-sample agent experiments ($n=20$/arm) possess $<11\%$ power to detect realistic effect sizes ($\Delta \le 0.20$), establishing a strict methodological ban against claiming web markup equivalence from non-significant p-values.

---

## 1. Introduction & Motivation

Large Language Models (LLMs) paired with browser automation libraries enable autonomous agents to execute complex web workflows [Zhou et al., 2024; Deng et al., 2023; Drouin et al., 2024]. However, raw HTML documents on modern websites frequently exceed 15,000 to 50,000 tokens, far exceeding prompt budget efficiency. To overcome this context-length barrier, modern browser-agent frameworks implement heuristic DOM serialization, pruning non-content elements and stripping non-whitelisted attributes before compiling the observation prompt.

In modern web development, information is represented across distinct technical layers:
- **Visible Typography:** Text rendered inside standard HTML elements (`<p>`, `<span>`, `<h1>`) for human readers.
- **Accessibility Semantics (WAI-ARIA):** Programmatic attributes (`aria-label`, `role`, `aria-describedby`) designed for assistive screen readers [W3C, 2017].
- **Developer Data Attributes:** Custom client-side attributes (`data-action`, `data-product-id`, `data-amount`) utilized by Single Page Applications (SPAs).
- **Structured Data (JSON-LD):** Machine-readable schemas embedded inside `<script type="application/ld+json">` for search engine indexing [Schema.org, 2024].

As standards organizations (W3C/TPAC 2024) debate the emerging "Agentic Web"—including proposals to augment web markup specifically to assist AI scrapers or introduce dedicated machine endpoints (`llms.txt`, MCP APIs)—a fundamental systems question arises:

> **Do client-side DOM serializers in modern autonomous agent frameworks preserve these metadata channels, or do heuristic pruning algorithms strip them before they can reach the LLM context prompt?**

If an agent framework silently purges structured metadata, web developers' efforts to markup pages for AI agents are completely lost. Furthermore, if academic researchers attempt to benchmark agent performance across markup variants without verifying prompt delivery, they risk testing unaugmented text while attributing performance differences to invisible channels.

### Key Contributions
1. **Architectural Serialization Proofs:** We prove through AST analysis and dynamic observation tracing that standard `browser-use 0.13.10` completely prunes Schema.org JSON-LD scripts (0.0% reachability) and strips attributes on non-interactive containers (`<span>`, `<div>`, `<section>`).
2. **Quantitative Reachability Benchmark:** We deliver an offline, reproducible audit suite ([`audit_metadata_reachability.py`](file:///C:/testing/research_execution_20261018/audit_metadata_reachability.py)) and dataset ([`serialization_audit_metrics.json`](file:///C:/testing/research_execution_20261018/serialization_audit_metrics.json)) quantifying token and attribute reachability across 7 metadata channels and 3 edge cases.
3. **Identification of the Action-Label Confound:** We demonstrate that when ARIA attributes do reach the prompt on interactive buttons, they confound semantic markup comprehension with target-text co-location.
4. **Pre-Registered Methodological Blueprint & Statistical Framework:** We pre-register a 4-arm balanced design ($N=96$) with hardened state-asserted verifiers and zero-dependency statistical implementations (CMH, Newcombe CIs) validated against published literature benchmarks [Agresti, 2002; Newcombe, 1998].
5. **Statistical Power Boundaries:** Through 10,000-trial Monte Carlo simulations, we prove that small-sample agent benchmarks ($n=20$/arm) have $<11\%$ power for realistic effects ($\Delta \le 0.20$), formally cautioning against the Equivalence Fallacy.

---

## 2. Related Work & Research Gap

### 2.1 Web Agent Benchmarks & Observation Pipelines
- **WebArena [Zhou et al., 2024]:** Evaluates autonomous agents across functional web environments (e-commerce, forums, GitLab). WebArena treats HTML observation as an end-to-end black box, establishing that GPT-4 completed only 10.6%–14.4% of tasks. It does not audit whether metadata survives into the prompt.
- **Mind2Web [Deng et al., 2023]:** Evaluates action prediction offline from DOM tree snapshots. While Mind2Web uses heuristic candidate ranking to filter DOM trees, it does not evaluate dynamic closed-loop serializer pruning.
- **WorkArena & BrowserGym [Drouin et al., 2024]:** Introduced BrowserGym, utilizing browser **Accessibility Trees (AXTrees)** to reduce token load from 15,000+ tokens to ~400 tokens. While BrowserGym demonstrates the operational token efficiency of accessibility trees, it treats AXTree generation as an operational shortcut rather than auditing whether semantic attributes inside the tree provide additive predictive value over visible text.
- **WebAgent & HTML-T5 [Gür et al., 2024]:** Pre-trained specialized models (HTML-T5) to filter HTML documents, proving that observation pre-processing directly bounds agent task success.

### 2.2 The Unaddressed Systems Gap
Prior literature addresses task complexity, visual grounding (VisualWebArena [Koh et al., 2024], SeeAct [Zheng et al., 2024]), and model capabilities. **However, no prior study has systematically audited the client-side DOM serialization algorithms in open-source agent libraries to measure information loss between source HTML, live DOM trees, and final LLM prompt buffers.**

---

## 3. Systems Architecture & Pruning Heuristics (`browser-use 0.13.10`)

We performed a static source-code audit and runtime trace of `browser-use 0.13.10` ([`C:\testing\.venv311\Lib\site-packages\browser_use\`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/)).

### 3.1 Script and Meta Pruning (`DISABLED_ELEMENTS`)
In `browser_use/dom/serializer/serializer.py` (Line 18):
```python
DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
```
During tree simplification in `_create_simplified_tree` (Lines 480–482):
```python
elif node.node_type == NodeType.ELEMENT_NODE:
    if node.node_name.lower() in DISABLED_ELEMENTS:
        return None
```
Any element matching `DISABLED_ELEMENTS` is immediately pruned. Child nodes are never traversed. Consequently, `<script type="application/ld+json">` structured data and `<meta name="evidence-date">` tags suffer 100% information loss.

### 3.2 Non-Interactive Element Tag Stripping
In `browser_use/dom/serializer/serializer.py` (Lines 1046–1058):
```python
is_any_scrollable = node.original_node.is_actually_scrollable or node.original_node.is_scrollable
should_show_scroll = node.original_node.should_show_scroll_info
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
If an element is **not interactive** (not clickable, not scrollable, and not an iframe):
- `_build_attributes_string` is **never invoked**.
- No opening or closing tag is output for that element.
- The serializer processes child text nodes, emitting raw strings, but all element attributes (`aria-label`, `data-*`, `role`) are discarded.

### 3.3 Attribute Whitelist Filtering
In `browser_use/dom/views.py` (Line 18), `DEFAULT_INCLUDE_ATTRIBUTES` specifies retained attributes. While standard accessibility attributes (`aria-label`, `role`) are included, developer custom attributes (`data-action`, `data-product-id`) are omitted. In `serializer.py` (Lines 1211–1215), attributes are discarded if `key not in include_attributes`.

---

## 4. Empirical Systems Audit: Metadata Reachability

We executed our automated offline verification harness ([`audit_metadata_reachability.py`](file:///C:/testing/research_execution_20261018/audit_metadata_reachability.py)) across four website variants and an edge-case fixture ([`fixtures/edge_cases.html`](file:///C:/testing/research_execution_20261018/fixtures/edge_cases.html)). All prompt payloads were captured using a local `MockChatModel` mimicking `gemini-flash-lite-latest`.

### 4.1 Quantitative Reachability Findings

| Metadata Channel | Source HTML | Parsed Live DOM | Prompt Buffer | Token Reachability % | Primary Suppression Mechanism |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Schema.org JSON-LD** | Present | Present | **Absent** | **0.0%** | `DISABLED_ELEMENTS` in `serializer.py:L18` |
| **WAI-ARIA on Buttons** | Present | Present | **Present** | **100.0%** | Retained via `DEFAULT_INCLUDE_ATTRIBUTES` on interactive nodes |
| **WAI-ARIA on Spans/Divs** | Present | Present | **Absent** | **0.0%** | Non-interactive tags not serialized in `serializer.py:L1046` |
| **Custom `data-*` (Default)** | Present | Present | **Absent** | **0.0%** | Omitted from `DEFAULT_INCLUDE_ATTRIBUTES` in `views.py:L18` |
| **Custom `data-*` (Extended)** | Present | Present | **Present** | **100.0%** *(buttons)* | Injected via `Agent(include_attributes=EXTENDED_ATTRIBUTES)` |
| **Temporal `<meta>`** | Present | Present | **Absent** | **0.0%** | `DISABLED_ELEMENTS` in `serializer.py:L18` |
| **Temporal `<time>`** | Present | Present | **Present** *(text)* | **100.0%** *(as text)* | `<time>` tag stripped; inner text emitted as plain text string |

*Metrics recorded in [`serialization_audit_metrics.json`](file:///C:/testing/research_execution_20261018/serialization_audit_metrics.json).*

### 4.2 Edge-Case Fixture Verification
1. **Non-Interactive Containers:** In `<section aria-label="Featured Showcase" data-container-id="sec-01">`, both `aria-label` and `data-container-id` were 100% absent from the LLM prompt under both default and extended whitelists.
2. **Empty Attributes:** In `<button aria-label="" data-action="">`, empty attributes were completely pruned by `serializer.py:L1214` (`str(value).strip() != ''`).
3. **Nested Button Elements:** In `<button aria-label="Wrapper"><span class="icon">🛒</span><span>Buy</span></button>`, the button tag retained its `aria-label`, and child text nodes were concatenated into the button's inner text: `[index] <button aria-label="Wrapper">🛒 Buy</button>`.

---

## 5. Methodological Analysis: Experimental Design & Confounding

### 5.1 The Action-Label Co-Location Confound
When ARIA markup does reach the prompt (on `<button>` elements), it alters the task construct:
- In `v0-baseline`: The agent observes:
  ```
  SoundFlow Air 3
  $49.99
  [12] <button>Add to Cart</button>
  ```
  The agent must perform **hierarchical reference resolution**: locate the heading, verify the price, establish the card boundary, and infer that button `[12]` belongs to SoundFlow Air 3.
- In `v2-aria`: The agent observes:
  ```
  [12] <button aria-label="Add SoundFlow Air 3 to cart">Add to Cart</button>
  ```
  The agent performs **direct string matching**: finding `"SoundFlow Air 3"` directly within the button tag. Any observed accuracy improvement measures label disambiguation, not semantic markup comprehension.

### 5.2 Pre-Registered 4-Arm Protocol v3
To provide a rigorous baseline for future empirical trials, we pre-registered a 4-arm Randomized Complete Block Design (RCBD) across six tasks and four temporal blocks ($N=96$ trials):
- `BASELINE` (ABS, $N=24$): Unaugmented HTML text.
- `BASELINE_REP` (VIS, $N=24$): Baseline replication arm to test within-condition stability.
- `ARIA` ($N=24$): Interactive elements augmented with `aria-label`.
- `DATA-CFG` ($N=24$): Interactive elements augmented with custom developer attributes via extended whitelisting.

### 5.3 Hardened Two-Tier Verifiers
Protocol v3 resolves four scoring flaws identified in earlier benchmarks ([`verifier_specification.md`](file:///C:/testing/research_execution_20261018/verifier_specification.md)):
- **T1–T2:** Programmatic assertion of exact SKU matches in `window.__cart__`.
- **T3 (2nd-Highest Audio):** Strictly enforces `len(cart) == 1 and cart[0] == "wh-002"`, rejecting the 6-SKU pass vulnerability of earlier verifiers.
- **T4 (Checkout):** Enforces `order_confirmed == True`, eliminating partial credit on incomplete checkouts.
- **T5 (Cart Removal):** Asserts precondition `pre_cart_count == 1` before checking empty final cart (`len(cart) == 0`).
- **T6 (Absent Fact Probe):** Evaluates grounded refusal vs. hallucinated warranty duration in strict isolation from primary task accuracy.

---

## 6. Statistical Methodology & Power Boundaries

### 6.1 Task-Stratified Cochran–Mantel–Haenszel (CMH) & Newcombe CIs
To account for task heterogeneity across the $K=5$ primary strata, post-experiment inference utilizes the continuity-corrected CMH test statistic [Agresti, 2002]:
$$\chi^2_{\text{CMH}} = \frac{\left( \left| \sum_{k=1}^K n_{11k} - \sum_{k=1}^K \mu_k \right| - 0.5 \right)^2}{\sum_{k=1}^K \text{Var}(n_{11k})}$$
Risk differences are reported alongside 95% Newcombe hybrid score confidence intervals [Newcombe, 1998] utilizing independent Wilson score limits. In [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py), our zero-dependency Python implementation matches published clinical trial benchmarks to four decimal places (Agresti 2002: $\chi^2 = 6.3841, p = 0.0115$; Newcombe 1998: $\hat{\theta} = 0.3250$, 95% CI: $[+0.1764, +0.4578]$).

### 6.2 Statistical Power Analysis & The Equivalence Fallacy
Primary contrasts across tasks T1–T5 utilize $n=20$ trials per arm. 10,000-trial Monte Carlo simulations ([`power_analysis.json`](file:///C:/testing/research_execution_20261018/power_analysis.json)) establish:
- **$\Delta = 0.70$:** $100.0\%$ power (robustly detectable).
- **$\Delta = 0.35$:** $49.7\% \pm 1.1\%$ power.
- **$\Delta = 0.20$:** **$10.8\% \pm 0.6\%$ power** (Bonferroni $\alpha = 0.0167$).

> [!WARNING]
> **METHODOLOGICAL PROHIBITION OF EQUIVALENCE CLAIMS:**  
> Because the power to detect small performance differences ($\Delta \le 0.20$) is under $11\%$, obtaining $p > 0.05$ cannot be interpreted as evidence that plain HTML and semantic markup perform equivalently. A null result indicates only that the sample size was insufficient to detect subtle effects.

---

## 7. Data Provenance & Forensic Governance

All project datasets are strictly quarantined into four non-overlapping categories ([`DATA_PROVENANCE_AUDIT.md`](file:///C:/testing/research_execution_20261018/DATA_PROVENANCE_AUDIT.md)):
1. **Historical Pilot (Exp 1, $N=250$):** Excluded from confirmatory analysis due to vision confounding (`use_vision=True`), broken treatment delivery (JSON-LD stripped), and repetition 9 survivorship bias.
2. **Aborted Main Run (Exp 1b, $N=147$):** Truncated at run 105 due to free-tier daily quota exhaustion (500 RPD wall). Discontinued.
3. **Synthetic Benchmark ($N=96$):** Quarantined to Appendix A for software validation only.
4. **Confirmatory Live Trials:** **0 of 96 trials executed.** The safety gate at line 258 of `protocol_v3_runner.py` remains locked (`SAFETY_GATE_LOCKED = True`).

---

## 8. Discussion & Implications for Web Standards ("The Agentic Web")

1. **The Fallacy of Metadata Augmentation for AI:** Web authors cannot assume that adding Schema.org JSON-LD or custom data attributes will assist AI agents. Under standard `browser-use`, client-side DOM serializers discard these elements before the LLM receives the observation.
2. **The "ARIA Stuffing" Hazard:** In accessibility research, standards bodies (W3C/TPAC) have warned against developers overloading ARIA attributes specifically to optimize for AI agents. If ARIA attributes provide no generalized accuracy advantage over clear typography—and merely duplicate entity text onto buttons—stuffing ARIA tags risks polluting accessibility trees for human screen-reader users without aiding AI agents.
3. **The Necessity of Out-of-Band Machine Endpoints:** Rather than attempting to embed machine data in HTML DOM channels that are vulnerable to serialization pruning, standards organizations should prioritize dedicated machine endpoints (e.g., `llms.txt`, Model Context Protocol APIs) that bypass DOM serialization entirely.

---

## 9. Conclusion

This paper identifies and proves the DOM serialization gap in autonomous browser agents, establishes the complete failure of Schema.org JSON-LD reachability under standard `browser-use 0.13.10`, identifies the non-interactive attribute pruning bottleneck, and exposes the action-label co-location confound. The research package provides a 100% reproducible offline verification suite and a pre-registered statistical framework, establishing essential systems baselines for future web agent engineering.

---

## References

1. Agresti, A. (2002). *Categorical Data Analysis* (2nd ed.). John Wiley & Sons. Hoboken, NJ.
2. Deng, X., Gu, Y., Zheng, B., Chen, S., Stevens, S., Wang, B., Sun, H., & Su, Y. (2023). Mind2Web: Towards a Generalist Agent for the Web. *Advances in Neural Information Processing Systems (NeurIPS)*, 36.
3. Drouin, A., Gasse, M., Caccia, M., Bergeron, A., Arsenault, P., & Chapados, N. (2024). WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks? *International Conference on Machine Learning (ICML)*.
4. Gür, I., Furuta, H., Austin, J., Huang, P., Lettìeri, S., Chen, M., & Houlsby, N. (2024). A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis. *International Conference on Learning Representations (ICLR)*.
5. Koh, J. Y., Lo, R., Jang, L., Duvvur, V., Lim, M., Huang, P. B., Gu, Z., Bisk, Y., & Fried, D. (2024). VisualWebArena: Evaluating Multimodal Web Agents on Realistic Visual Web Tasks. *Annual Meeting of the Association for Computational Linguistics (ACL)*.
6. Newcombe, R. G. (1998). Interval estimation for the difference between independent proportions: comparison of eleven methods. *Statistics in Medicine*, 17(8), 873–890.
7. Schema.org Community Group. (2024). *Schema.org: Structured Data for the Web*. W3C Community Group. https://schema.org/
8. W3C. (2017). *Accessible Rich Internet Applications (WAI-ARIA) 1.1*. W3C Recommendation 14 December 2017. https://www.w3.org/TR/wai-aria-1.1/
9. Zheng, B., Gou, B., Kil, J., Sun, H., & Su, Y. (2024). SeeAct: GPT-4V(ision) is a Generalist Web Agent, if Grounded. *International Conference on Machine Learning (ICML)*.
10. Zhou, S., Xu, F. F., Zhu, H., Zhou, X., Lo, R., Sridhar, A., Yuan, X., Bisk, Y., Fried, D., & Neubig, G. (2024). WebArena: A Realistic Web Environment for Building Autonomous Language Agents. *International Conference on Learning Representations (ICLR)*.

---

## Appendix A: Offline Statistical Pipeline Verification Benchmark

> [!NOTE]
> **SYNTHETIC SOFTWARE BENCHMARK DISCLAIMER:**  
> The metrics below are generated from a **mock/synthetic benchmark dataset** ([`test_scratch_synthetic_data/dataset_1_valid_complete.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv)) to demonstrate that [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py) executes without error. **They DO NOT represent real agent task performance.**

### Table A1: Synthetic Software Pipeline Output (Tasks T1–T5)
Multiplicity threshold: Bonferroni-adjusted $\alpha = 0.05 / 3 = 0.0167$.

| Contrast ID | Treatment ($n/N$) | Reference ($n/N$) | Risk Difference | Newcombe 95% CI | CMH $\chi^2$ | Unadjusted p | Bonferroni p |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ARIA vs BASELINE** | 14 / 20 (70.0%) | 25 / 40 (62.5%) | **+0.0750** | [-0.1782, +0.2801] | 0.088 | 0.7662 | 1.0000 |
| **DATA-CFG vs BASELINE**| 17 / 20 (85.0%) | 25 / 40 (62.5%) | **+0.2250** | [-0.0113, +0.4024] | 2.399 | 0.1215 | 0.3644 |
| **ARIA vs DATA-CFG** | 14 / 20 (70.0%) | 17 / 20 (85.0%) | **-0.1500** | [-0.3751, +0.0906] | 0.683 | 0.4086 | 1.0000 |

### Table A2: Baseline Quality Control (Synthetic Benchmark)
- BASELINE (ABS) success: 13 / 20 (65.0%).
- BASELINE_REP (VIS) success: 12 / 20 (60.0%).
- Fisher's Exact Stability Test: Two-sided $p = 1.0000$ (satisfies stability criterion $p \ge 0.10$).

---

## Appendix B: Step-by-Step Offline Reproducibility Instructions

Any student or independent researcher can reproduce all systems findings on Windows/Linux in under 2 minutes:

1. **Activate Virtual Environment:**
   ```bash
   C:\testing\.venv311\Scripts\activate
   ```
2. **Execute the Offline Systems Reachability Audit:**
   ```bash
   python C:\testing\research_execution_20261018\audit_metadata_reachability.py
   ```
   *Expected Outcome:* Generates `serialization_audit_metrics.json` confirming 0% reachability for JSON-LD and non-interactive ARIA.
3. **Execute Statistical Engine Unit Tests:**
   ```bash
   python C:\testing\research_execution_20261018\test_analyze_v3_results.py
   ```
   *Expected Outcome:* 11 unit tests pass in <0.3 seconds.
4. **Execute Offline Regression Suite:**
   ```bash
   python C:\testing\research_execution_20261018\offline_test_suite.py
   ```
   *Expected Outcome:* 11 tests pass, verifying disabled elements, attribute whitelists, and verifier logic.

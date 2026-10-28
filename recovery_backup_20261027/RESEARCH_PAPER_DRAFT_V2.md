# The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents

**Document Status:** Empirical Systems Research Paper & Methodological Blueprint  
**Authors:** [Author Names Redacted for Double-Blind Peer Review]  
**Affiliations:** Department of Computer Science  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Date:** October 2026  
**Software Artifacts:** 100% Offline Verifiable Suite (`audit_metadata_reachability.py`, `compare_accessibility_tree.py`, `test_observation_pipeline_stages.py`, `test_analyze_v3_results.py`, `serialization_audit_metrics.json`, `accessibility_tree_comparison.json`)  
**Data Provenance Declaration:** Systems serialization measurements and statistical power simulations are empirically verified via deterministic offline execution. Local model runs (001–005 on `qwen3:4b`) are reported exclusively as exploratory diagnostic latency/watchdog case studies on constrained hardware. Synthetic benchmarks are quarantined to software engine verification. The confirmatory live behavioral trial (Protocol v3, 4 arms, $n=20$/arm) is an audited pre-registered blueprint that remains unexecuted under our zero-cost offline protocol.

---

## Abstract

Autonomous web agents powered by Large Language Models (LLMs) are widely evaluated on multi-step digital workflows. While benchmarks evaluate agents holistically across heterogeneous environments, existing literature leaves unexamined the client-side Document Object Model (DOM) observation pipelines that filter, prune, and serialize web markup before it enters the LLM prompt. In modern web engineering, factual information is partitioned into distinct technical layers: rendered typography, semantic accessibility annotations (WAI-ARIA), developer custom attributes (`data-*`), and structured metadata (Schema.org JSON-LD). In this paper, we present an empirical systems audit of the **DOM serialization gap**—the structural discrepancy between in-memory DOM representations and the serialized text ingested by the model—using `browser-use 0.13.10` under text-only observation (`use_vision=False`) as a representative case study. Through static AST code audit and dynamic execution tracing, we document three deterministic filtering behaviors:
1. Unconditional pruning of `<script>` and `<meta>` elements via hardcoded exclusion rules (`DISABLED_ELEMENTS`), preventing Schema.org JSON-LD structured data from reaching the observation buffer.
2. Selective tag-stripping of non-interactive elements (`serializer.py:L1046–L1058`), meaning parent attributes on `<span>` and `<div>` containers are discarded.
3. Omission of custom developer attributes (`data-*`) under default attribute whitelisting.

Through direct Chromium Chrome DevTools Protocol (CDP) accessibility tree extraction, we document structural divergence between native accessibility trees and DOM serializers: on route `#home`, 27 of 34 interactive elements (79.4%, Wilson 95% CI: [63.2%, 89.7%]) match Blink accessibility nodes, while non-interactive ARIA semantics are retained in Blink's accessibility cache but stripped by the agent serializer. Furthermore, we expose the **Action-Label Co-Location Confound**: augmenting button labels with product titles converts reference resolution into direct string matching. We pre-register an audited 4-arm evaluation blueprint equipped with deterministic state-asserted verifiers. Monte Carlo power simulations (10,000 trials) estimate that small-sample agent experiments ($n=20$/arm) possess $<11\%$ power to detect realistic effect sizes ($\Delta \le 0.20$) at baseline $p_1 = 0.85$, establishing a strict methodological prohibition against inferring equivalence from non-significant results. Finally, we report an exploratory 5-trial diagnostic study on local quantized models (`qwen3:4b`), analyzing latency scaling under context expansion and demonstrating cancellation-safe telemetry under watchdog timeouts. We transparently disclose that the confirmatory 4-arm agent benchmark remains unexecuted under our zero-cost offline protocol.

**Keywords:** Autonomous Web Agents, Large Language Models, DOM Serialization Gap, WAI-ARIA, Semantic Markup, Accessibility Trees, Experimental Reproducibility.

---

## 1. Introduction & Research Motivation

The integration of Large Language Models (LLMs) with automated browser execution environments has catalyzed the emergence of autonomous web agents capable of executing multi-turn transactional workflows across digital interfaces [Zhou et al., 2024; Deng et al., 2023; Drouin et al., 2024; Boisvert et al., 2024; Xie et al., 2024]. Operating as sequential decision-making systems, these agents observe web page state, synthesize an action plan, and dispatch discrete interactions (e.g., clicking elements, typing text, selecting options) via browser automation protocols such as Playwright, Puppeteer, or the Chrome DevTools Protocol (CDP).

Despite widespread empirical benchmarking, contemporary web agent research suffers from a pervasive methodological confound: evaluations are typically conducted holistically across diverse web environments where visual styling, page layout, JavaScript routing logic, and DOM markup representations vary simultaneously. On complex websites, it is difficult to disentangle whether an agent failed due to visual occlusion, context saturation, stochastic planning drift, or uninformative DOM node labeling.

In modern frontend web engineering, information is intentionally partitioned into distinct architectural layers:
- **Rendered Visible Typography:** Plain textual nodes rendered inside standard HTML tags (`<h1>`, `<p>`, `<span>`) intended for human visual reading.
- **Semantic Accessibility Markup (WAI-ARIA):** Programmatic semantic annotations (`role`, `aria-label`, `aria-describedby`) standardized by the World Wide Web Consortium [W3C, 2023; W3C, 2018] to convey interactive semantics to assistive technologies.
- **Developer Custom Data Attributes:** Structured key-value pairs (`data-action`, `data-product-id`, `data-category`) utilized by client-side Single Page Applications (SPAs) for internal state management.
- **Structured Metadata (Schema.org JSON-LD):** Standardized machine-readable entity graphs embedded inside non-rendered script tags (`<script type="application/ld+json">`) for search engine indexing [Schema.org, 2024].

As industry discussions propose modifying web architectures for autonomous agents—including proposals to enrich ARIA labels specifically for AI scrapers or to deploy dedicated machine endpoints (`llms.txt` [Howard, 2024], Model Context Protocol APIs [Anthropic, 2024])—a fundamental systems question arises:

> **Do client-side DOM serializers in autonomous agent frameworks preserve these metadata channels, or do heuristic pruning algorithms strip them before they can reach the LLM context prompt?**

If an agent framework silently purges structured metadata, web authors' efforts to markup pages for AI agents are lost. Furthermore, if researchers benchmark agent performance across markup variants without verifying prompt delivery, they risk evaluating an unaugmented text baseline while mistakenly attributing performance variations to invisible channels. We investigate this question through an in-depth systems audit of `browser-use 0.13.10`, examining its source-code filtering rules, comparing its output against native Chromium accessibility trees, and establishing the statistical power requirements for empirical agent evaluation.

---

## 2. Related Work & Systems Gap

### 2.1 Autonomous Web Agent Benchmarks
Evaluation of LLMs as autonomous web agents has advanced through several benchmark suites:
- **WebArena** [Zhou et al., 2024] established an end-to-end evaluation paradigm across four realistic self-hosted web applications. Evaluating state-of-the-art LLMs, WebArena revealed task completion rates between 10.6% and 14.4%. However, WebArena evaluates holistic task success across multi-page workflows, conflating layout design, visual rendering, and markup structure.
- **Mind2Web** [Deng et al., 2023] introduced a dataset of 2,350 tasks across 137 real websites, evaluating element-level action prediction offline from DOM tree snapshots. Mind2Web demonstrated the severity of the HTML context bottleneck and introduced heuristic element ranking to filter raw trees.
- **WorkArena and BrowserGym** [Drouin et al., 2024; Boisvert et al., 2024] evaluated web agents on enterprise workflows within ServiceNow. To mitigate context window exhaustion, BrowserGym utilizes Accessibility Trees (AXTrees), condensing long raw HTML documents (often exceeding 15,000 tokens on enterprise pages) into hundreds of tokens representing interactive elements. BrowserGym demonstrated the operational token efficiency of accessibility representations, treating AXTree generation as an engineering optimization.
- **OSWorld** [Xie et al., 2024] extended multimodal agent evaluation to open-domain operating system tasks across heterogeneous applications, illustrating that execution grounding bottlenecks persist across diverse interface modalities.
- **HTML-T5 and WebAgent** [Gur et al., 2024] addressed the HTML length bottleneck by pre-training a specialized model to sub-sample and filter long HTML documents prior to action planning, confirming that observation filtering directly bounds downstream agent execution.
- **AgentBench** [Liu et al., 2024] evaluated LLMs across eight interactive environments, confirming substantial performance drops on web tasks relative to static reasoning benchmarks.

### 2.2 DOM Observation Pruning and Distillation
A critical challenge in web agent engineering is observation space reduction:
- **AgentOccam** [Yang et al., 2025] demonstrated that aggressive observation-space pruning can yield a simple yet strong baseline for web agents, showing that reducing DOM size mitigates context bloat and improves task success. However, AgentOccam focused on operational token reduction rather than auditing whether heuristic pruning selectively purges semantic metadata layers.
- Heuristic tag and attribute whitelisting in frameworks such as `browser-use 0.13.10` attempts to remove non-essential markup while preserving clickable elements. However, the precise information-loss characteristics of these heuristics have not previously been decomposed across frontend metadata channels.

### 2.3 Multimodal Visual Grounding vs. Text Observation
A parallel research line integrates computer vision with web navigation:
- **VisualWebArena** [Koh et al., 2024] extended WebArena to visually intensive tasks, showing that text-only agents fail when critical information is encoded exclusively in pixels.
- **SeeAct** [Zheng et al., 2024] formulated a two-stage visual agent framework separating candidate generation on screenshots from action grounding on DOM elements, demonstrating that visual perception assists planning but suffers from fine-grained action grounding bottlenecks.
- **WebVoyager** [He et al., 2024] evaluated multimodal agents using Set-of-Mark visual prompts across 15 live websites, achieving 55.7% completion. Visual screenshot prompts bypass DOM observation pipelines entirely, trading structured machine semantics for pixel rendering.

### 2.4 The Unaddressed Systems Gap
Prior literature addresses task complexity, visual grounding, and model capabilities. **To our knowledge, no prior study has systematically decomposed client-side DOM serialization algorithms in open-source agent libraries to audit information loss between source HTML, live DOM trees, browser accessibility trees, and final LLM prompt buffers.** While alternative channels (such as page titles, current URL, active JavaScript execution tools, or visual screenshots) may supply additional context in multimodal deployments, the text-based DOM observation buffer remains the primary grounding mechanism for text-based browser agents.

---

## 3. Systems Architecture and Pruning Heuristics (`browser-use 0.13.10`)

We performed a static AST source-code audit and runtime trace of `browser-use 0.13.10`, a widely deployed open-source browser agent framework.

### 3.1 Script and Meta Pruning (`DISABLED_ELEMENTS`)
In `browser_use/dom/serializer/serializer.py` (Line 18), the framework defines an explicit blacklist:
```python
DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
```
During simplified tree creation (`_create_simplified_tree`, Lines 480–482):
```python
elif node.node_type == NodeType.ELEMENT_NODE:
    if node.node_name.lower() in DISABLED_ELEMENTS:
        return None
```
Any element matching `DISABLED_ELEMENTS` is immediately pruned from the observation graph; child nodes are never traversed. Consequently, `<script type="application/ld+json">` structured data and `<meta name="evidence-date">` tags suffer complete, deterministic exclusion from the observation tree.

### 3.2 Non-Interactive Element Tag Stripping
In `browser_use/dom/serializer/serializer.py` (Lines 1046–1058), element tag serialization is conditionally gated:
```python
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
If an element is **not interactive** (not clickable, not scrollable, and not an iframe):
- `_build_attributes_string` is never executed.
- No opening or closing tag is output for that element.
- The serializer processes child text nodes, emitting raw strings, but all element attributes (`aria-label`, `data-*`, `role`) are discarded.

### 3.3 Attribute Whitelist Filtering
Attribute retention on interactive elements is governed by `DEFAULT_INCLUDE_ATTRIBUTES` (`browser_use/dom/views.py`, Line 18):
```python
DEFAULT_INCLUDE_ATTRIBUTES = [
    'title', 'type', 'checked', 'id', 'name', 'role', 
    'value', 'placeholder', 'alt', 'aria-label', ...
]
```
While standard accessibility attributes (`aria-label`, `role`) are included, developer custom attributes (`data-action`, `data-product-id`) are omitted. In `serializer.py` (Lines 1211–1215), attributes are discarded if `key not in include_attributes`. When runner configurations pass an extended whitelist (`EXTENDED_ATTRIBUTES`), custom attributes are retained on interactive nodes, but remain stripped on non-interactive elements due to tag stripping.

---

## 4. Empirical Systems Audit: The 5-Stage Observation Pipeline

### 4.1 The 5 Observation Pipeline Stages
We define five discrete architectural stages through which web information flows before model ingestion:
1. **Stage 1 (Source HTML & Static Markup):** Raw HTML markup received over HTTP.
2. **Stage 2 (Browser Live DOM):** In-memory DOM tree parsed by Blink and augmented by client-side JavaScript.
3. **Stage 3 (Browser Accessibility Tree):** Chromium Blink native `AXObjectCache` queried via CDP `Accessibility.getFullAXTree`.
4. **Stage 4 (Agent DOM Serializer):** The simplified tree constructed by `browser-use 0.13.10`.
5. **Stage 5 (Final Model Context Prompt):** The stringified observation buffer compiled into the LLM context.

### 4.2 Multi-Stage Observation Retention Matrix
We executed our automated verification harness (`audit_metadata_reachability.py`) across four website variants and an edge-case fixture (`fixtures/edge_cases.html`). All prompt payloads were intercepted using a local `MockChatModel`. Table 1 reports the deterministic retention status across pipeline stages.

| Metadata Channel | Stage 1 (HTML) | Stage 2 (DOM) | Stage 3 (AXTree) | Stage 5 (Prompt) | Architectural Mechanism |
|---|:---:|:---:|:---:|:---:|---|
| **Schema.org JSON-LD** | Retained | Retained | Dropped | Dropped | Blacklisted via `DISABLED_ELEMENTS` (L18) |
| **Button WAI-ARIA** | Retained | Retained | Retained | Retained | Whitelisted on interactive elements |
| **Non-Interactive ARIA** | Retained | Retained | Retained | Dropped | Non-interactive tags stripped (L1046) |
| **Custom `data-*` (Default)** | Retained | Retained | Dropped | Dropped | Omitted from default attribute whitelist |
| **Custom `data-*` (Extended)** | Retained | Retained | Dropped | Retained | Delivered on buttons under extended whitelist |
| **Temporal `<meta>`** | Retained | Retained | Dropped | Dropped | Blacklisted via `DISABLED_ELEMENTS` (L18) |
| **Temporal `<time>`** | Retained | Retained | Retained | Retained | Tag stripped; inner text emitted |

*Table 1: Multi-stage observation retention matrix across semantic metadata channels in `browser-use 0.13.10`.*

### 4.3 Node-Level Correspondence: Chromium AXTree vs. Selector Map
To evaluate structural alignment between Chromium's native accessibility tree and the agent's observation tree, we implemented `compare_accessibility_tree.py`:
- CDP `Accessibility.getFullAXTree` extracts Blink's unique `backendDOMNodeId` for accessibility nodes.
- In `browser-use 0.13.10`, `summary.dom_state.selector_map` indexes interactive elements containing the matching Blink `backend_node_id`.

**Empirical Findings on Route `#home`:**  
Across 336 Chromium AXNodes constructed across the page (256 possessing `backendDOMNodeId`), `browser-use` detected 34 interactive elements in its selector map. Exactly **27 of 34 interactive elements (79.4%, Wilson 95% CI: [63.2%, 89.7%])** matched 1-to-1 to a corresponding Blink AXNode.

Inspection of the 7 unmatched interactive elements reveals that `browser-use` employs client-side JavaScript heuristics (evaluating bounding rectangles, pointer cursors, and click listeners) to register elements that Chromium Blink does not expose as discrete top-level accessibility objects, or that reside inside flattened inline containers or synthetic wrapper elements.

### 4.4 Structural Divergence Between DOM Serialization and Native Accessibility Trees
Our comparative analysis reveals bidirectional divergence between native accessibility trees and serialized DOM observations:
- **Non-Interactive ARIA Semantics:** Retained by Chromium Blink's AXTree, but stripped by `browser-use 0.13.10`. In our stimulus markup (`variants/v2-aria/index.html`), we examine two distinct patterns:
  1. *Price Span:* `<span class="product-price" aria-label="Price: $49.99">$49.99</span>`. Here, the element lacks an explicit ARIA role. Under W3C WAI-ARIA 1.2 [W3C, 2023] §5.2.7 and the Accessible Name and Description Computation (AccName 1.1) specification [W3C, 2018], elements with `role="generic"` prohibit author-supplied naming; standard screen readers ignore `aria-label` on generic spans. Nonetheless, Chromium Blink's internal `AXObjectCache` constructs an accessibility node with computed name `"Price: $49.99"`. In contrast, `browser-use 0.13.10` strips the tag entirely at line 1046, delivering only the text `"$49.99"`.
  2. *Rating Span:* `<span class="product-rating" role="img" aria-label="Rating: 4.5 out of 5 stars">...</span>`. Here, the explicit `role="img"` is a valid naming container under ARIA 1.2. Blink retains the accessible name, but `browser-use` strips the element because it is non-interactive.
- **Custom Developer `data-*` Attributes:** Completely absent from Blink's accessibility tree (custom attributes have no accessibility semantics), but deliverable to the agent on interactive elements when `include_attributes` is extended.

---

## 5. Methodological Analysis & Experimental Confounds

### 5.1 The Action-Label Co-Location Confound
When ARIA markup does reach the prompt (on interactive `<button>` elements), augmenting button labels from generic text (e.g., `"Add to Cart"`) to entity-specific ARIA labels (e.g., `aria-label="Add SoundFlow Air 3 to cart"`) introduces an acute experimental confound:
- **In unaugmented baseline (ABS):** The agent observes:
  ```text
  SoundFlow Air 3
  $49.99
  [12] <button>Add to Cart</button>
  ```
  The agent must perform **hierarchical reference resolution**: locate the card boundary, verify product title and price, and infer that button `[12]` corresponds to SoundFlow Air 3.
- **In confounded ARIA:** The agent observes:
  ```text
  [12] <button aria-label="Add SoundFlow Air 3 to cart">Add to Cart</button>
  ```
  The agent can perform **direct string matching**: finding `"SoundFlow Air 3"` directly within the button tag. Any observed accuracy improvement measures label disambiguation rather than semantic comprehension.

To eliminate this confound, our stimulus design in `shared/app-core.js:L35` standardizes generic action triggers across all variants: `addBtn.setAttribute('aria-label', 'Add item to cart')`.

### 5.2 Hardened State-Asserted Verifiers
To prevent scoring inflation, all task verifiers enforce deterministic DOM state assertions:
- **T1–T2:** Programmatic assertion of exact SKU matches in `window.__cart__`.
- **T3 (2nd-Highest Audio):** Strictly enforces `len(cart) == 1 and cart[0] == "wh-002"`, rejecting multi-item additions.
- **T4 (Transactional Checkout):** Enforces `order_confirmed == True` via DOM form submission assertion, eliminating credit on incomplete checkouts.
- **T5 (Cart Removal):** Asserts precondition `pre_cart_count == 1` before checking empty final cart (`len(cart) == 0`).
- **T6 (Absent Fact Probe):** Evaluates grounded refusal vs. hallucinated warranty duration in strict isolation from primary task accuracy.

All verifiers pass 100% of offline regression tests (`test_t6_verifier_isolated.py`, `test_verifier_ground_truth_battery.py`).

### 5.3 Evaluation Blueprint Status Disclosure
We transparently disclose that the planned 4-arm agent evaluation (BASELINE, BASELINE_REP, ARIA, DATA-CFG across Tasks T1–T5 with $n=20$ trials/arm) represents an audited, pre-registered experimental blueprint. In accordance with our zero-cost offline protocol, this benchmark was not executed on live commercial LLM APIs.

---

## 6. Statistical Power Boundaries & Equivalence Analysis

### 6.1 Task-Stratified Cochran–Mantel–Haenszel (CMH) and Newcombe CIs
To account for task heterogeneity across $K=5$ primary strata, post-experiment inference in our blueprint utilizes the continuity-corrected CMH test statistic [Agresti, 2002; Mantel & Haenszel, 1959]:
$$\chi^2_{\text{CMH}} = \frac{\left( \left| \sum_{k=1}^K n_{11k} - \sum_{k=1}^K \mu_k \right| - 0.5 \right)^2}{\sum_{k=1}^K \text{Var}(n_{11k})}$$

Risk differences are reported alongside 95% Newcombe hybrid score confidence intervals [Newcombe, 1998] utilizing independent Wilson score limits [Wilson, 1927]. In `test_analyze_v3_results.py`, our zero-dependency Python implementation matches published clinical trial benchmarks to four decimal places (Agresti 2002: $\chi^2 = 6.3841, p = 0.0115$; Newcombe 1998: $\hat{\theta} = 0.3250$, 95% CI: $[+0.1764, +0.4578]$).

### 6.2 Monte Carlo Power Analysis
Primary contrasts across tasks T1–T5 utilize $n=20$ trials per arm ($N=80$ total benchmark runs). We conducted 10,000-trial Monte Carlo power simulations (`power_analysis.py`, `power_audit_results.json`) under a randomized complete block design with random task effects (log-odds variance $\sigma^2 = 0.09$):
- **Large Disparity ($\Delta = 0.70$, baseline $p_1 = 0.10, p_2 = 0.80$):** Estimated power is $98.6\% \pm 0.3\%$.
- **Moderate Effect ($\Delta = 0.35$, baseline $p_1 = 0.85, p_2 = 0.50$):** Estimated power is $49.6\% \pm 1.1\%$.
- **Small Effect ($\Delta = 0.20$, baseline $p_1 = 0.85, p_2 = 0.65$):** Estimated power is **$10.8\% \pm 0.6\%$** (Bonferroni $\alpha = 0.0167$).

Statistical power is strongly dependent on the baseline success rate and simulation assumptions. Crucially, the simulations distinguish per-task unpooled comparisons from task-stratified CMH testing.

### 6.3 Prohibition of Equivalence Claims from Non-Significance
Because statistical power to detect small performance differences ($\Delta \le 0.20$) is under 11% at $n=20$ trials per arm, obtaining a non-significant result ($p > 0.05$ or $p \ge 0.10$) cannot be interpreted as evidence that plain HTML and semantic markup perform equivalently. In classical hypothesis testing, failure to reject the null hypothesis ($H_0: \theta_1 = \theta_2$) indicates only that the sample size was insufficient to detect subtle effects. Proving equivalence requires a formal Two One-Sided Tests (TOST) framework with an explicit, pre-registered equivalence margin $\delta_{\text{equiv}}$ (e.g., $|\Delta| < 0.10$), which requires sample sizes ($N > 400$) far exceeding typical agent evaluations.

---

## 7. Empirical Case Study: Latency Scaling and Watchdog Truncation

To evaluate execution dynamics under local deployment, we conducted five exploratory diagnostic trials on local quantized `qwen3:4b` using `browser-use 0.13.10` on hybrid CPU/GPU hardware (4 GB VRAM, offloading 34% of layers to CPU). Table 2 reports trial telemetry from `results/local_llama_summary.csv`.

| Run ID | Arm | Variant | Duration | Steps | CDP Ground Truth | Observed Mechanism |
|---|---|---|:---:|:---:|:---:|---|
| `qwen3_smoke_001` | DATA-CFG | `v3-data-attrs` | 3.34s | 0 | False | Pydantic validator failure (`max_history_items` $\le 5$). |
| `qwen3_smoke_002` | DATA-CFG | `v3-data-attrs` | 1013.09s | 2 | **True (1.0)** | Step 2 clicked button; Step 3 waited until HTTP read timeout due to missing outer watchdog. |
| `qwen3_smoke_003` | DATA-CFG | `v3-data-attrs` | 288.61s | 2 | **True (1.0)** | Step 1 succeeded (102.9s); Step 2 breached 180s watchdog ceiling. |
| `qwen3_smoke_004` | ABS | `v3-data-attrs` | 185.50s | 1 | False | Step 1 watchdog timeout; unhandled cancellation dropped telemetry. |
| `qwen3_smoke_005` | ABS | `v3-data-attrs` | 188.56s | 1 | False | Step 1 watchdog timeout; cancellation telemetry safely captured. |

*Table 2: Exploratory diagnostic trials on local `qwen3:4b` (Task T2).*

### 7.1 Runtime Reconciliation and Context Expansion
The observed runtimes illustrate distinct execution regimes:
- In run 002 (1,013.09s), the agent successfully clicked the target product button in Step 2 (adding SKU `mkp-001` to cart), but Step 3 lacked an outer per-step watchdog, running until the underlying HTTP client read timeout expired.
- In run 003 (288.61s), an outer 180-second step watchdog was active. In Step 1, with a prompt of $\sim$1,500 tokens, `qwen3:4b` completed evaluation and action generation in 102.9 seconds. In Step 2, the framework appended prior history, action results, and the updated DOM, expanding prompt context to $>3,200$ tokens. At hybrid ingestion rates of 15–20 tokens/second, prompt evaluation required between $3200 / 20 = 160$ seconds and $3200 / 15 = 213$ seconds; combining prompt evaluation with generation latency breached the 180-second watchdog ceiling. The run terminated with status `timed_out`, yet the post-hoc verifier confirmed that the cart action had succeeded prior to timeout.

### 7.2 In-Flight Cancellation Telemetry
In `browser-use`, step timeouts are enforced via `asyncio.wait_for(self.step(step_info), timeout=...)`. When the 180-second timeout expires, `asyncio.wait_for` injects `asyncio.CancelledError`. In Python 3.8+, `CancelledError` inherits directly from `BaseException`, not `Exception`. In run 004, the wrapper's `except Exception:` block was bypassed, leaving telemetry empty. In run 005, implementing dedicated `except asyncio.CancelledError:` captured:
- `call_index`: 1, `status`: `"cancelled_in_flight"`, `error_type`: `"CancelledError"`.
- `wall_clock_seconds`: 179.6983s.
- Unobserved server metrics (`prompt_tokens`, `eval_duration_ms`) were preserved as `null`.

These five trials demonstrate local inference dynamics on constrained hardware; they do not constitute a confirmatory behavioral comparison.

---

## 8. Discussion and Implications for Web Standards

### 8.1 Considerations for Semantic Metadata in Web Agents
Web developers cannot assume that embedding Schema.org JSON-LD or custom data attributes will automatically assist autonomous agents. In `browser-use 0.13.10`, client-side DOM serializers discard non-rendered script tags and non-interactive container attributes before the LLM receives the observation.

### 8.2 ARIA Overloading Concerns
Discussions within standards bodies (such as W3C and TPAC) have cautioned against overloading ARIA markup specifically to guide AI scrapers. If ARIA annotations duplicate visible typography onto button labels without improving reference resolution, augmenting pages with artificial ARIA tags risks polluting accessibility trees for human screen-reader users without aiding DOM-serialized agents.

### 8.3 Out-of-Band Machine Endpoints
Rather than attempting to embed machine data in HTML DOM channels that are vulnerable to serialization pruning, standards organizations and developers are exploring dedicated out-of-band machine interfaces. Proposals such as `llms.txt` [Howard, 2024] and the Model Context Protocol (MCP) [Anthropic, 2024] provide structured context directly to language models, bypassing DOM serialization bottlenecks entirely.

---

## 9. Limitations

We explicitly identify several key limitations:
1. **Single-Framework Scope:** All AST audits and serialization measurements were conducted on `browser-use 0.13.10`. Other frameworks (e.g., BrowserGym, Stagehand, Skyvern, LaVague, Crawl4AI) utilize distinct observation pipelines, accessibility snapshots, or raw HTML distillation heuristics that may exhibit different retention profiles.
2. **Observation Modality:** Audits were performed within a text-only observation space (`use_vision=False`). Multimodal agents utilizing screenshot inputs can perceive rendered visual typography and layout boundaries directly, bypassing DOM serializer pruning.
3. **Synthetic Evaluation Environment:** Measurements utilized a controlled e-commerce benchmark environment (`variants/v0`–`v3`). While this isolates markup channels from visual occlusions, real-world websites feature dynamic scripts and layout variations not captured in synthetic fixtures.
4. **Unexecuted Confirmatory Benchmark:** The 4-arm behavioral evaluation ($n=20$/arm) is an audited, pre-registered blueprint; confirmatory trials on live commercial LLMs were not executed under our zero-cost offline protocol.
5. **Exploratory Diagnostic Scope:** The 5 local Qwen trials represent an exploratory case study on quantized inference dynamics on constrained hardware (4 GB VRAM), not a generalizable capability benchmark.
6. **AXTree Route Scope:** The node correspondence comparison was evaluated on route `#home` ($n=34$ interactive elements), producing a wide Wilson 95% confidence interval ($[63.2\%, 89.7\%]$).

---

## 10. Conclusion

This paper formalizes the DOM serialization gap in autonomous browser agents, establishing that default observation pipelines in `browser-use 0.13.10` prune structured metadata (Schema.org JSON-LD and developer custom attributes) prior to model prompt construction. We have documented structural divergence between native browser accessibility trees and DOM serializers, identified the action-label co-location confound, and proven the statistical power boundaries of small-sample web agent experiments. By providing a 100% reproducible offline verification suite, this work establishes essential systems baselines for future web agent engineering.

---

## Appendix A. Offline Statistical Pipeline Verification Benchmark

**Synthetic Software Benchmark Disclaimer:** The metrics in Tables 3 and 4 are generated from a mock/synthetic benchmark dataset (`test_scratch_synthetic_data/dataset_1_valid_complete.csv`) to verify that `analyze_v3_results.py` executes without numerical or serialization errors. **They do not represent real agent task performance.**

| Contrast ID | Treatment ($n/N$) | Reference ($n/N$) | Risk Diff | Newcombe 95% CI | CMH $\chi^2$ | Adjusted p |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **ARIA vs BASELINE (ABS)** | 14 / 20 (70.0%) | 13 / 20 (65.0%) | **+0.0500** | [-0.2312, +0.3168] | 0.000 | 1.0000 |
| **ARIA vs BASELINE_REP (VIS)** | 14 / 20 (70.0%) | 12 / 20 (60.0%) | **+0.1000** | [-0.1901, +0.3644] | 0.178 | 1.0000 |
| **DATA-CFG vs BASELINE (ABS)** | 17 / 20 (85.0%) | 13 / 20 (65.0%) | **+0.2000** | [-0.0754, +0.4320] | 1.488 | 1.0000 |
| **DATA-CFG vs BASELINE_REP (VIS)** | 17 / 20 (85.0%) | 12 / 20 (60.0%) | **+0.2500** | [-0.0267, +0.4795] | 2.404 | 0.6050 |
| **ARIA vs DATA-CFG** | 14 / 20 (70.0%) | 17 / 20 (85.0%) | **-0.1500** | [-0.3751, +0.0906] | 0.683 | 1.0000 |

*Table 3: Synthetic software pipeline output: Unpooled sensitivity contrasts across baseline arms (Tasks T1–T5, Bonferroni $\alpha = 0.0100$ for 5 contrasts). Pooling baseline conditions is rejected to prevent the Equivalence Fallacy in the absence of a formal TOST margin.*

| Condition | Success ($n/N$) | Rate | Fisher's Exact p | Methodological Decision |
|---|:---:|:---:|:---:|---|
| **BASELINE (ABS)** | 13 / 20 | 65.0% | \multirow{2}{*}{$p = 1.0000$} | Fails to reject null ($p = 1.0000 \ge 0.05$). Under statistical equivalence principles, failing to detect a difference does not establish equivalence. In the absence of an a priori prespecified Two One-Sided Tests (TOST) equivalence margin, pooling is unjustified. Baseline conditions are presented unpooled in Table 3. |
| **BASELINE_REP (VIS)** | 12 / 20 | 60.0% | | |

*Table 4: Baseline stability and quality control check on synthetic benchmark data.*

---

## Appendix B. Step-by-Step Offline Reproducibility Instructions

All systems findings can be reproduced offline on Windows/Linux in under two minutes:
1. **Multi-Channel Reachability Trace:**  
   `python audit_metadata_reachability.py`  
   Outputs `serialization_audit_metrics.json`, verifying 0.0% JSON-LD reachability and non-interactive span stripping.

2. **Run Chromium Blink AXTree vs. Serializer Comparison:**  
   `python compare_accessibility_tree.py`  
   Outputs `accessibility_tree_comparison.json`, verifying the 79.4% node match rate and the Critical/Reversed divergences.

3. **Execute Offline Observation Pipeline Test Suite:**  
   `python test_observation_pipeline_stages.py`  
   Verifies 5/5 assertions across all observation pipeline stages in <0.2 seconds.

4. **Execute Statistical Engine Benchmark:**  
   `python test_analyze_v3_results.py`  
   Verifies 11/11 statistical assertions against Agresti (2002) and Newcombe (1998) clinical trial reference data.

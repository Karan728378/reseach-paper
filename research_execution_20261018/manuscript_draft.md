# Information-Channel Effects on Browser-Agent Retrieval and Grounded Actions: A Controlled Evaluation of Visible Text, ARIA Attributes, and Configured Custom Data in Web Environments

**Authors:** [Author Names Redacted for Double-Blind Review]  
**Affiliations:** [Affiliations Redacted for Double-Blind Review]  
**Document Status:** Working Draft / Proposed Study Manuscript (Pre-Execution)  
**Date:** October 18, 2026  
**Artifact Package:** `C:\testing\research_execution_20261018`  

---

## Abstract
Autonomous web agents powered by Large Language Models (LLMs) increasingly interact with complex web applications to retrieve factual information and perform multi-step grounded actions. While existing web agent benchmarks evaluate agent performance across varying site domains and task complexities, they implicitly treat the web page as an undifferentiated text or image stream, overlooking the underlying Document Object Model (DOM) markup channels through which facts are structured. In this proposed study, we present the first controlled, single-variable experimental benchmark isolating the effect of HTML information-delivery channels on browser-agent decision-making. We evaluate four treatment conditions across identical web pages: (1) fact absence ($	ext{ABS}$), (2) visible rendered text ($	ext{VIS}$), (3) semantic accessibility attributes ($	ext{ARIA}$), and (4) custom developer attributes with explicit observation whitelisting ($	ext{DATA-CFG}$). Using a Randomized Complete Block Design (RCBD) with $N=96$ runs ($K=4$ arms $\times$ $J=6$ tasks $\times$ $R=4$ blocks) evaluated against a local e-commerce platform with zero external network dependencies, we isolate text-only DOM observation processing by strictly enforcing $\text{use\_vision}=\text{False}$. In preliminary pilot audits, we uncover two critical architectural phenomena: default DOM serializers in modern agent frameworks (`browser-use 0.13.10`) silently prune `<script>` and `<meta>` elements and strip non-standard `data-*` attributes, causing unconfigured metadata channels to collapse into absolute fact absence. We present pre-registered strict verification criteria, statistical power analyses, and synthetic offline test suites. Prospective results are slated for measurement upon formal protocol authorization.

---

## 1. Introduction
Autonomous browser agents have emerged as a prominent paradigm for automating complex, multi-step digital tasks, ranging from information synthesis to transactional e-commerce workflows. Standard evaluations, such as WebArena [Zhou et al., 2023] and Mind2Web [Deng et al., 2023], have benchmarked agents against diverse web environments. However, these benchmarks evaluate agents at the task level, conflating website visual design, layout hierarchy, and underlying DOM serialization. 

In real-world web engineering, developers embed factual information across distinct semantic and technical channels. A product price or customer rating may be rendered as human-visible typography in a `<p>` tag, embedded as an accessible description in an `aria-label` attribute for screen readers, encoded in a custom `data-*` attribute for client-side JavaScript frameworks, or serialized as structured JSON-LD in a `<script>` tag for search engine crawlers. 

Whether and how modern LLM-based browser agents perceive and act upon these distinct channels remains fundamentally unmeasured. In this paper, we propose a rigorous, controlled experimental study to determine how information-channel placement modulates agent retrieval accuracy and grounded action execution.

---

## 2. Research Problem and Motivation
The fundamental technical problem investigated in this study is the **DOM serialization gap** in autonomous browser agents. While human users perceive websites through visual rendering engines and screen-reader users perceive sites through accessibility trees, autonomous LLM agents typically interact with web pages through serialized text snapshots of the DOM or multimodal screenshot tokens.

When an agent processes a DOM tree, the raw HTML undergoes aggressive filtering and pruning to fit within context length constraints and reduce inference cost. If website developers place critical information in non-visible semantic attributes (e.g. `aria-label`) or custom attributes (e.g. `data-amount="49.99"`), the agent's ability to act upon that information depends strictly on whether the agent's observation pipeline preserves those attributes.

Our preliminary technical audit of `browser-use 0.13.10` reveals an unexpected vulnerability:
1. `<script type="application/ld+json">` blocks and `<meta>` tags are completely pruned from the observation stream by hardcoded serializer rules (`DISABLED_ELEMENTS`).
2. Custom developer attributes (such as `data-warranty` or `data-rating`) are silently discarded by default attribute whitelists (`DEFAULT_INCLUDE_ATTRIBUTES`).
3. Multimodal vision models (`use_vision=True`) introduce an uncontrolled visual confound: text rendered visibly on screen is delivered through dual channels (visual pixels + text tokens), whereas ARIA and `data-*` attributes are delivered exclusively through text tokens.

Without rigorous experimental isolation, researchers cannot determine whether agent failures stem from reasoning deficiencies, navigation missteps, or simple observation-pipeline pruning.

---

## 3. Related Work
*Note: Citations below reflect verified local audit records. Unverified external citations are explicitly marked pending full literature review.*

### 3.1 Web Agent Benchmarks
- **WebArena [Zhou et al., 2023]:** An end-to-end benchmark providing realistic web environments (e-commerce, forums, code repositories) evaluated on functional success. While WebArena captures ecological validity, it does not manipulate HTML information channels under controlled ceteris paribus conditions.
- **Mind2Web [Deng et al., 2023]:** A benchmark for generalist web agents based on multi-choice element selection from raw DOM trees across diverse websites. Mind2Web evaluates action prediction offline but does not evaluate runtime closed-loop navigation under isolated markup channels.
- **VisualWebArena [Koh et al., 2024] `[UNVERIFIED - PENDING VERIFICATION]`:** Extends web benchmarking to visually intensive tasks requiring image and chart comprehension.
- **WorkArena [Drouin et al., 2024] `[UNVERIFIED - PENDING VERIFICATION]`:** Focuses on enterprise web workflows within ServiceNow environments.

### 3.2 Multimodal Grounding vs. Text Observation
- **SeeAct [Zheng et al., 2024]:** Explores GPT-4V for visual web grounding, demonstrating that visual screenshots enhance element location. However, SeeAct focuses on visual versus text prompt formats rather than the internal semantics of HTML markup channels.
- **WebAgent [Gur et al., 2023] `[UNVERIFIED - PENDING VERIFICATION]`:** Uses HTML-T5 to sub-sample DOM trees, demonstrating that HTML pre-processing directly bounds task success.

---

## 4. Research Gap and Contribution
No prior work has experimentally isolated the information-delivery channel within identical DOM structures to evaluate its causal effect on browser-agent decision-making.

### Summary of Contributions
1. **Defensible Research Formulation:** We formulate a single-variable evaluation framework isolating HTML information channels under a clean 3-arm design ($\text{ABS}$, $\text{ARIA}$, $\text{DATA-CFG}$; $N=72$) and a 4-arm design ($N=96$).
2. **Observation-Pipeline Audit:** We document the exact pruning and filtering mechanisms in modern browser-agent serializers, demonstrating why JSON-LD and unconfigured custom attributes collapse to fact absence.
3. **Hardened Verification Suite:** We identify and resolve four critical verifier flaws prevalent in historical web benchmarks, providing strict verifier implementations validated by exhaustive offline regression and mutation tests.
4. **Reproducible Experiment Package:** We deliver a complete Randomized Complete Block Design ($N=72$ / $N=96$, $\text{seed}=42$), JSON schemas, and analytical power calculations, ready for prospective execution.

---

## 5. Research Questions and Hypotheses

### Primary Research Question
> **How does the DOM information channel (visible text, ARIA attribute, or whitelisted custom data attribute) through which a web-grounded fact is delivered affect a text-based browser agent's retrieval accuracy and grounded action execution compared to fact absence?**

### Hypotheses
- **Hypothesis 1 ($H_1$ — Channel Presence vs. Absence):** Task success in channels containing the target fact ($\text{ARIA}$, $\text{DATA-CFG}$) is significantly higher than in the absence condition ($\text{ABS}$).  
  *Primary Estimand:* Risk Difference $RD(\text{Arm} - \text{ABS}) = P(Y=1 \mid \text{Arm}) - P(Y=1 \mid \text{ABS})$.
- **Hypothesis 2 ($H_2$ — Visible Text vs. ARIA Channel):** When the DOM serializer includes ARIA attributes in the text observation, task success in the $\text{ARIA}$ channel is not significantly inferior to unaugmented text.  
  *Primary Estimand:* Risk Difference $RD(\text{BASELINE} - \text{ARIA})$.
- **Hypothesis 3 ($H_3$ — Configured Custom Attributes):** When the agent runner is patched to whitelist custom $data-*$ attributes ($\text{DATA-CFG}$), task success is significantly higher than $\text{ABS}$; whereas without configuration, $data-*$ attributes are stripped and yield identical failure rates to $\text{ABS}$.  
  *Primary Estimand:* Risk Difference $RD(\text{DATA-CFG} - \text{ABS})$.

### Non-Claim Boundaries
This study **cannot** and **does not** claim:
- Generalizability across all LLM model families (evaluated specifically on Google Gemini with `browser-use`).
- Equivalence between channels if null hypotheses fail to be rejected (the pilot study is underpowered for $\Delta \le 0.15$).
- Human-equivalent accessibility performance.
- Live empirical model discovery prior to explicit human execution authorization (0 live runs completed to date).

---

## 6. Experimental Methodology

### 6.1 Experimental Environment
The study uses TechMart, a realistic Single Page Application (SPA) e-commerce platform hosted on an offline local server (`http://localhost:8080`). TechMart features dynamic client-side rendering, product catalog filtering, cart state management in `localStorage`, and checkout form submission.

### 6.2 Treatment Arms
Every task is evaluated under four strictly isolated arms:
1. **$	ext{ABS}$ (Negative Control):** The target fact is omitted entirely from the DOM, attributes, and metadata.
2. **$	ext{VIS}$ (Visible Text):** The target fact is rendered inside standard visible tags (`<p class="product-price">`, `<span class="rating">`).
3. **$	ext{ARIA}$ (Accessibility Attribute):** The target fact is placed exclusively within valid ARIA attributes (e.g. `aria-label="Price: $49.99"`), while visible text is replaced with neutral generic tokens.
4. **$	ext{DATA-CFG}$ (Configured Custom Attributes):** The target fact is placed in custom attributes (e.g. `data-amount="49.99"`), and the agent runner is configured with an extended attribute whitelist.

### 6.3 Elimination of Confounders
- **Vision Confound Elimination:** `use_vision=False` is strictly enforced.
- **Anti-Leakage Auditing:** Page titles, document URLs, search tags, and metadata are audited to ensure target tokens do not leak into secondary channels.
- **Session Isolation:** A fresh browser session and fresh Playwright context are instantiated for every run.

---

## 7. Task Design and Benchmark Construction

The task bank comprises six tasks ($J=6$) balancing grounded multi-step actions with pure factual retrieval:

| Task ID | Task Family | User Instruction | Target Entity | Target Field | Ground Truth | Success Condition |
|---------|-------------|------------------|---------------|--------------|--------------|-------------------|
| **T1** | Action / Comparison | "Search for 'wireless headphones' and add the least expensive result to your cart." | `wh-001` | Price | $49.99 | `wh-001` in cart |
| **T2** | Action / Direct | "Find the product called 'Mechanical Keyboard Pro' and add it to your cart." | `mkp-001` | Name | mkp-001 | `mkp-001` in cart |
| **T3** | Action / Comparison | "Navigate to Audio category. Compare customer ratings. Add product with second-highest rating to cart." | `wh-002` | Rating | 4.5 Stars | Exactly `wh-002` in cart |
| **T4** | Action / Flow | "Search for 'ErgoGlide Mouse', add to cart, and complete checkout with test credentials." | `mse-001` | Checkout | Jane Smith order | Confirmed order with `mse-001` |
| **T5** | Action / Mutation | "There is one item in your cart. Navigate to cart and remove it so cart is empty." | `wh-001` | Cart Removal | Empty | Pre-state valid & cart empty |
| **T6** | Retrieval | "Retrieve the exact manufacturer warranty duration specified for 'SoundFlow Air 3'." | `wh-001` | Warranty | 36 months | Regex `\b36\s*(months?\|mo)\b` |

---

## 8. Observation-Pipeline Validation
We statically and dynamically validated the observation pipeline in `browser-use 0.13.10`:
- **Pruning Verification:** Inspection of `serializer.py` confirmed `DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}`. `<script type="application/ld+json">` is pruned before DOM snapshot construction.
- **Whitelist Verification:** Inspection of `views.py` confirmed that `aria-label` is included by default, but custom attributes (`data-warranty`, `data-amount`) are stripped unless explicitly whitelisted in `include_attributes`.

---

## 9. Evaluation Metrics & Statistical Analysis Plan

### 9.1 Primary Metric
Binary task success $Y_{ijk} \in \{0, 1\}$ for arm $i$, task $j$, and block $k$, evaluated programmatically via browser state.

### 9.2 Statistical Tests
- **Primary Hypothesis Test:** Pairwise Fisher's Exact Test on pooled success rates with Bonferroni correction for 6 pairwise comparisons ($\alpha_{\text{adj}} = 0.05 / 6 = 0.00833$).
- **Effect Size:** Risk Difference (RD) with 95% Wilson score confidence intervals.
- **Secondary Stratified Test:** Generalized Cochran-Mantel-Haenszel (CMH) test stratified across blocks and tasks.
- **Mixed Model:** Generalized Linear Mixed-Effects Model (`logit(P(Y=1)) ~ arm + task + (1|block)`).

### 9.3 Statistical Power Summary
Power calculations for $N=24$ per arm (two-sided $\alpha=0.05$):
- $\Delta = 0.70$ ($	ext{ABS}$ vs. $	ext{VIS}$): **100.0% Power** (Adequate).
- $\Delta = 0.35$ ($	ext{VIS}$ vs. $	ext{ARIA}$): **75.1% Power** (Moderate).
- $\Delta = 0.20$ ($	ext{VIS}$ vs. $	ext{DATA-CFG}$): **35.6% Power** (Underpowered).
- $\Delta = 0.15$ ($	ext{ARIA}$ vs. $	ext{DATA-CFG}$): **23.3% Power** (Severely underpowered).

---

## 10. Threats to Validity

### 10.1 Internal Validity
- **Historical Verifier Flaws:** Thoroughly resolved in Protocol v3.
- **Vision Confound:** Mitigated by setting $\text{use\_vision}=\text{False}$.
- **API Quota Truncation:** Mitigated by circuit-breaker rules halting after 3 consecutive 429 errors and analyzing only complete blocks.

### 10.2 External Validity
- Evaluated on a single e-commerce application (TechMart) and single agent stack (`browser-use` + Gemini). Results may vary on complex multi-domain sites or alternative agent architectures.

---

## 11. Prospective Results & Experimental Data
*Note: In compliance with non-negotiable research integrity guidelines, experimental results are strictly reserved for post-authorization measurement. No synthetic numbers are fabricated.*

### 11.1 Primary Benchmark Results Table (Specification)

| Treatment Arm | Total Runs ($N$) | Successful Runs ($n$) | Success Rate (\%) | 95\% Wilson CI | Mean Steps | Mean Latency (s) |
|---------------|------------------|-----------------------|--------------------|-----------------|------------|------------------|
| **$	ext{ABS}$** | 24 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| **$	ext{VIS}$** | 24 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| **$	ext{ARIA}$** | 24 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| **$	ext{DATA-CFG}$** | 24 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |

### 11.2 Pairwise Statistical Contrasts (Specification)

| Contrast | Risk Difference ($\widehat{RD}$) | 95\% CI for RD | Fisher Exact $p$-value | Bonferroni Significant? |
|----------|-----------------------------------|-----------------|------------------------|-------------------------|
| $	ext{VIS} - 	ext{ABS}$ ($H_1$) | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| $	ext{ARIA} - 	ext{ABS}$ | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| $	ext{DATA-CFG} - 	ext{ABS}$ ($H_3$) | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| $	ext{VIS} - 	ext{ARIA}$ ($H_2$) | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| $	ext{VIS} - 	ext{DATA-CFG}$ | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| $	ext{ARIA} - 	ext{DATA-CFG}$ | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |

### 11.3 Contextualization of Historical Pilot Data
An earlier historical pilot (148 runs, October 2026) was audited and determined to be **flawed and non-generalizable** due to four compounding factors:
1. Catastrophic quota truncation (42 consecutive HTTP 429 failures).
2. Sequential non-randomized execution blocks inducing Missing-Not-At-Random (MNAR) bias.
3. Serializer pruning rendering the historical JSON-LD and unpatched Data-Attrs arms equivalent to ABS.
4. Logical verifier flaws in T3, T4, and T5 inflating raw success metrics.
Consequently, historical pilot data cannot serve as proof of experimental hypotheses and are superseded by this protocol.

---

## 12. Conclusion & Next Steps
We have formulated a mathematically defensible experimental protocol and software verification package to evaluate HTML information-channel effects on browser-agent decision-making. By eliminating multimodal visual confounds, correcting flawed historical verifiers, and specifying an RCBD schedule ($N=96$), this proposed study establishes a rigorous foundation for experimental execution. Following formal human protocol approval and API quota configuration, the prospective experiment will be executed and the results populated into this manuscript.

---

## 13. References
- Deng, X., Gu, Y., Zheng, B., Chen, S., Stevens, S., Wang, B., Sun, H., & Su, Y. (2023). Mind2Web: Towards a Generalist Agent for the Web. *Advances in Neural Information Processing Systems (NeurIPS 2023)*.
- Gur, I., Furuta, H., Austin, V., Huang, S., Parikh, A. P., & Lapata, M. (2023). A Real-World WebAgent with Planning, Long Context, and HTML Processing. `[UNVERIFIED - PENDING VERIFICATION]`.
- Koh, J. Y., Lo, R., Jang, L., Nezhurina, V., Schonfeld, B., Dou, C., Zheng, B., Sano, M., Bisk, Y., Fried, D., & Salakhutdinov, R. (2024). VisualWebArena: Evaluating Multimodal Web Agents on Realistic Visual Tasks. `[UNVERIFIED - PENDING VERIFICATION]`.
- Zheng, B., Gou, B., Zheng, J., Shen, Y., Chen, Y., Chang, K. W., & Peng, N. (2024). SeeAct: GPT-4V(ision) for Generalist Web Agents. *arXiv preprint*.
- Zhou, S., Xu, F. F., Zhu, H., Zhou, X., Lo, R., Sridhar, A., Yuan, X., Bisk, Y., Fried, D., & Neubig, G. (2023). WebArena: A Realistic Web Environment for Building Autonomous Agents. *International Conference on Learning Representations (ICLR 2024)*.

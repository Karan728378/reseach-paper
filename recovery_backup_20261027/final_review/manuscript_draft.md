# Evaluating the Additive Value of Semantic Web Markup for Autonomous Browser Agents: A Controlled Study of ARIA and Configured Custom Data on Text-Based LLM Navigation

**Authors:** [Author Names Redacted for Double-Blind Review]  
**Affiliations:** [Affiliations Redacted for Double-Blind Review]  
**Document Status:** Working Draft / Protocol & Pre-Execution Study Package  
**Date:** October 18, 2026  
**Artifact Package:** `C:\testing\research_execution_20261018\final_review\`

---

## Abstract
Autonomous web agents powered by Large Language Models (LLMs) increasingly interact with web applications to extract information and execute multi-step transactions. Existing benchmarks typically evaluate agent performance at the task level on raw web pages, conflating visual layout with underlying Document Object Model (DOM) markup. In real-world web engineering, websites deliver information through visible text, but developers frequently layer machine-readable semantic metadata on top: WAI-ARIA accessibility attributes and custom developer `data-*` attributes. In this paper, we present an experimental evaluation framework investigating whether adding structured semantic markup improves an autonomous text-based browser agent's retrieval accuracy, execution efficiency, and latency on web pages where factual information is already visible. We evaluate four conditions across an e-commerce platform: (1) unaugmented plain HTML baseline, (2) baseline replicate, (3) WAI-ARIA accessibility semantics, and (4) custom developer `data-*` attributes with configured serializer whitelisting. Using a Randomized Complete Block Design (RCBD) with $N=96$ runs ($K=4$ arms $\times$ $J=6$ tasks $\times$ $R=4$ blocks), we isolate token-level DOM observation processing by strictly enforcing $\text{use\_vision}=\text{False}$. In offline prompt pipeline inspections with mock language models, we discover that standard DOM serializers in modern agent frameworks (`browser-use 0.13.10`) discard attributes on non-interactive elements and silently omit unconfigured `data-*` attributes. We establish strict ground-truth verifiers that eliminate historical verifier vulnerabilities and survivorship biases, document corrected statistical power bounds under familywise error control, and mandate that non-significant findings cannot be claimed as channel equivalence. Prospective empirical outcomes are scheduled for measurement following protocol authorization.

---

## 1. Introduction
Large Language Model (LLM) browser agents are increasingly deployed to automate web-based workflows, such as searching e-commerce catalogs, comparing product specifications, and completing checkout transactions. Prominent benchmarks, such as WebArena [Zhou et al., 2024], Mind2Web [Deng et al., 2024], and VisualWebArena [Koh et al., 2024], evaluate agent capabilities at the macro-task level. However, they treat the web page as an undifferentiated stream, leaving unexamined the fundamental question of how web page markup structure influences agent comprehension.

In modern web development, information is delivered across distinct layers. Visible text nodes render product names, prices, and customer ratings for human readers. Concurrently, developers layer semantic markup onto HTML elements:
1. **WAI-ARIA attributes** (`aria-label`, `role`, `aria-describedby`), designed to provide accessibility semantics for screen readers and assistive technologies [W3C, 2023].
2. **Custom `data-*` attributes** (`data-product-id`, `data-amount`, `data-action`), designed to expose structured state to client scripts, testing frameworks, and analytics pipelines [WHATWG, 2024].

Whether augmenting an already-visible website with ARIA semantics or custom data attributes improves the decision-making, accuracy, or execution speed of an autonomous text-based browser agent remains an open empirical question. We formalize this evaluation under an **Additive Semantic Markup Evaluation** framework.

---

## 2. Research Problem and Observation Architecture

### 2.1 The Additive Formulation
In real-world websites, target facts are rarely hidden entirely behind markup attributes; rather, they are displayed visibly in the interface. Under Option A (Additive Semantic Markup Evaluation), the central question is:
> *Does adding WAI-ARIA or configured `data-*` attributes to an existing website improve a text-based browser agent's task accuracy and navigation speed compared to plain HTML alone?*

### 2.2 DOM Serialization Realities in Modern Frameworks
Autonomous agents operating without multimodal vision (`use_vision=False`) perceive web pages through text snapshots produced by DOM serializers. Using a local `MockChatModel` in `browser-use 0.13.10` (`test_agent_prompt_pipeline.py`), we uncovered key serialization constraints that directly affect semantic attribute delivery:
1. **Interactive Node Restriction:** Standard serializers format HTML attributes almost exclusively for interactive elements (`<button>`, `<input>`, `<a>`). Attributes placed on non-interactive elements (e.g. `<span class="product-price" aria-label="...">`) are stripped from the prompt, emitting only inner text. Serializer monkey-patching (`enable_observable_dom_serialization`) is required to preserve non-interactive nodes bearing semantic attributes.
2. **Attribute Whitelist Filtering:** The framework's default whitelist (`DEFAULT_INCLUDE_ATTRIBUTES`) includes `aria-label` but drops custom attributes (`data-amount`, `data-rating`). The `DATA-CFG` condition explicitly injects an extended whitelist (`EXTENDED_ATTRIBUTES`).
3. **Structured Data Elimination:** Script elements, including `<script type="application/ld+json">`, are unconditionally pruned by serializer `DISABLED_ELEMENTS`.

---

## 3. Related Work
- **WebArena [Zhou et al., 2024]:** End-to-end web environment benchmarking agents on e-commerce, forums, and CMS platforms.
- **Mind2Web [Deng et al., 2024]:** Offline benchmark assessing element selection accuracy across complex DOM trees.
- **VisualWebArena [Koh et al., 2024]:** Multimodal web benchmark demonstrating visual grounding requirements.
- **WebVoyager [He et al., 2024]:** Large multimodal model web agent evaluation using visual and DOM inputs.
- **WebAgent [Gur et al., 2024]:** Demonstrating that HTML pruning and snippet extraction significantly constrain LLM task success.
- **W3C WAI-ARIA 1.2 [W3C, 2023] & WHATWG HTML Standards [WHATWG, 2024]:** Authoritative specifications for accessible semantics and custom dataset attributes.

---

## 4. Experimental Methodology

### 4.1 Benchmark Task Pools
The evaluation benchmark comprises six scheduled tasks ($J=6$), partitioned into two distinct methodological pools:

#### 4.1.1 Primary Grounded Action Benchmark Pool (Tasks T1–T5, $N_{\text{primary}}=80$ Runs)
All primary tasks require an observable browser action verifying facts present in the DOM:
1. **T1 (Search & Minimization):** Search for "wireless headphones" and add the least expensive result to cart (`wh-001`, $49.99).
2. **T2 (Product Identification):** Locate "Mechanical Keyboard Pro" and add it to cart (`mkp-001`, $149.99).
3. **T3 (Rating Comparison):** Navigate to Audio, compare customer ratings, and add the second-highest rated item (`wh-002`, rating 4.5). Strict single-item exact match.
4. **T4 (Checkout Transaction):** Search for "ErgoGlide Mouse" (`mse-001`), add to cart, and complete full checkout using test credentials.
5. **T5 (State Mutation):** Cart pre-seeded with 1 item (`wh-001`); agent must navigate to cart and remove the item so the cart is empty. Precondition assertion (`pre_cart_count == 1`) strictly enforced.

#### 4.1.2 Secondary Exploratory Negative Information Probe (Task T6, $N_{\text{probe}}=16$ Runs)
6. **T6 (Warranty Fact Absence Probe):** Agent is prompted to retrieve manufacturer warranty duration for `wh-001`. Because warranty duration is **absent from the website in all variants**, T6 evaluates **hallucination resistance**:
   - **Grounded Refusal ($Y_{\text{refusal}} = 1$):** Agent correctly identifies and reports that warranty information is unstated on the page.
   - **Hallucinated Assertion ($Y_{\text{refusal}} = 0$):** Agent invents an ungrounded duration (e.g. asserting *"36 months"* as fact).
   - T6 is excluded from the primary grounded action benchmark to prevent rewarding hallucination or distorting transaction success rates.

### 4.2 Verifier Strictness and Survivorship Correction
Historical benchmark scripts exhibited severe leniency: T3 accepted 6 different SKUs, T4 awarded unconditional 0.25 credit on failed checkouts, and T5 passed unseeded carts. Furthermore, historical runners retried failed runs upon resumption (`get_completed_run_indices` filtered on `success==True`). Our execution engine (`protocol_v3_runner.py`) strictly enforces binary ground truth from client JavaScript state and counts both successful and failed runs as completed.

---

## 5. Statistical Analysis Plan & Power Analysis

### 5.1 Primary Outcome and Hypotheses (Tasks T1–T5)
- **Primary Outcome:** Binary Grounded Action Success ($Y \in \{0, 1\}$) across Tasks T1–T5 ($N=80$).
- **Primary Inferential Model:** Cochran-Mantel-Haenszel (CMH) test stratified by task ($J=5$), implemented in `analyze_v3_results.py`.
- **Effect Size:** Risk Difference ($\widehat{RD}$) reported with 95% Newcombe Hybrid Score and Agresti-Caffo Adjusted Wald confidence intervals.
- **Additive Hypotheses:**
  - $H_{1\text{A}}$ (ARIA vs. Baseline): $\widehat{RD}(\text{ARIA} - \text{BASELINE}) > 0$
  - $H_{1\text{B}}$ (DATA-CFG vs. Baseline): $\widehat{RD}(\text{DATA-CFG} - \text{BASELINE}) > 0$
  - $H_{1\text{C}}$ (ARIA vs. DATA-CFG): $\widehat{RD}(\text{ARIA} - \text{DATA-CFG})$
  - Bonferroni correction for 3 planned contrasts: $\alpha_{\text{adj}} = 0.05 / 3 \approx 0.0167$.

### 5.2 Statistical Power Analysis & RCBD Dependence Structure
As detailed in `POWER_RECONCILIATION.md`, study statistical power is characterized under two complementary models:
1. **Unadjusted Homogeneous Binomial Model ($\rho = 0$):** Under an idealized homogeneous baseline ($P=0.50$), power at $\alpha_{\text{adj}} = 0.0167$ is 99.9% for large effects ($\Delta=0.70$), 65.1% for moderate effects ($\Delta=0.35$), and 19.8% for small effects ($\Delta=0.20$).
2. **Task-Heterogeneous RCBD Simulation (`recompute_power_rcbd.py`):** When modeling actual task baseline difficulties ($[0.70, 0.85, 0.50, 0.30, 0.80]$ across $n=4$ reps/cell), ceiling compression on high-accuracy tasks reduces empirical power for moderate effects ($\Delta=0.35$) to **$49.7\% \pm 1.1\%$** ($B=2,000$ iterations), and small effects ($\Delta=0.20$) to **$10.8\% \pm 0.7\%$**.

> **Non-Equivalence Mandate:** Because statistical power is $< 20\%$ for small effect sizes under both models, **a failure to reject the null hypothesis ($p \ge \alpha$) CANNOT be interpreted as evidence of semantic markup equivalence**. Non-significant differences must be reported strictly as inconclusive.

---

## 6. Prospective Results Tables (Specification)

### Table 1: Primary Grounded Action Benchmark (Tasks T1–T5, $N=80$ Runs)
| Treatment Arm | Total Runs ($N$) | Successful Runs ($n$) | Success Rate (\%) | 95\% Wilson CI | Mean Steps | Mean Latency (s) | Clean Action Ratio |
|---|---|---|---|---|---|---|---|
| **$\text{BASELINE (Pooled)}$** | 40 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| *-- Baseline Split 1 (ABS)* | 20 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| *-- Baseline Split 2 (VIS)* | 20 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| **$\text{ARIA}$** | 20 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| **$\text{DATA-CFG}$** | 20 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |

### Table 2: Exploratory Negative Information Probe (Task T6, $N=16$ Runs)
| Treatment Arm | Total Runs ($N$) | Grounded Refusals ($n$) | Refusal Rate (\%) | Hallucinations ($n$) | Hallucination Rate (\%) | 95\% Wilson CI |
|---|---|---|---|---|---|---|
| **$\text{BASELINE (Pooled)}$** | 8 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| **$\text{ARIA}$** | 4 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |
| **$\text{DATA-CFG}$** | 4 | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` | `[TO BE MEASURED]` |

---

## 7. Threats to Validity
1. **Sample Size Constraints:** With $N=24$ runs per arm, subtle advantages ($\Delta < 0.20$) conferred by semantic attributes cannot be reliably detected.
2. **Serializer Attribute Filtering:** Because off-the-shelf agent frameworks discard non-interactive attributes, developer annotations on static text nodes cannot assist standard agents unless custom serializers are configured.
3. **Synthetic Platform:** The benchmark evaluates a controlled single-page application; real-world commercial websites introduce additional DOM complexity and dynamic scripting.

---

## 8. Conclusion
We have formalized a reproducible, statistically defensible protocol for evaluating the additive value of semantic web markup on autonomous browser agents. With DOM equivalence verified, prompt pipelines traced, strict verifiers implemented, and survivorship biases eliminated, live empirical execution awaits formal authorization.

---

## References
- Deng, X., Gu, Y., Ling, B. C., Zhang, C., He, B. Y., Cobbe, K., ... & Sun, H. (2024). Mind2Web: Towards a Generalist Agent for the Web. *NeurIPS 2023*. arXiv:2306.06070.
- Gur, I., Jaques, N., Miao, Y., Choi, J., Mialon, G., Farinhas, A., ... & Eisenschlos, J. M. (2024). A Real-World WebAgent with Planning, Long Context Understanding, and Sub-DOM-Tree Modeling. *ICLR 2024*. arXiv:2307.12856.
- He, H., Yao, W., Ma, K., Yu, D., Dai, W., Zhang, H., ... & Chen, Z. (2024). WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models. *ACL 2024*. arXiv:2401.13919.
- Koh, J. Y., Lo, R., Jang, L., Duvvur, V., Lim, M., Huang, P. B., ... & Salakhutdinov, R. (2024). VisualWebArena: Evaluating Multimodal Web Agents on Realistic Tasks. arXiv:2401.13649.
- W3C. (2023). Accessible Rich Internet Applications (WAI-ARIA) 1.2. W3C Recommendation.
- WHATWG. (2024). HTML Living Standard: Embedding custom non-visible data with the data-* attributes.
- Zhou, S., Xu, F. F., Zhu, H., Zhou, X., Lo, R., Sridhar, A., ... & Neubig, G. (2024). WebArena: A Realistic Web Environment for Building Autonomous Language Agents. *ICLR 2024*. arXiv:2307.13854.

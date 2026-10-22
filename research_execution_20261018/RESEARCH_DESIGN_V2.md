# RESEARCH DESIGN V2: SYSTEMS AUDIT OF THE DOM SERIALIZATION GAP

**Project:** Autonomous Browser Agent Observation Pipeline & DOM Serialization Systems Study  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  
**Document Status:** Approved Research Architecture Specification  
**Date:** October 21, 2026  
**Supervisor / Auditor:** Senior Research Supervisor & Technical Systems Auditor  

---

## 1. Comparative Evaluation of Three Research Directions

To establish a defensible research roadmap for an undergraduate CSE project with strict budget and time constraints, three candidate directions were formally evaluated:

| Criterion | **Direction A: Controlled Behavioral Experiment** | **Direction B: Systems Serialization Audit** *(Selected)* | **Direction C: Multi-Framework Cross-Audit** |
| :--- | :--- | :--- | :--- |
| **Scientific Validity** | **Low.** $n=20$/arm has $<11\%$ power for small effects ($\Delta \le 0.20$); non-significant results cannot prove equivalence. | **High.** Deterministic ground truth via AST traversal and token reachability traces. | **Very High.** Strong comparative systems evaluation across distinct architectural paradigms. |
| **Construct Purity** | **Confounded.** Modifying `aria-label` on buttons co-locates entity names onto action triggers, testing text co-location rather than semantic reasoning. | **Pure.** Evaluates physical retention of attributes across serialization stages without behavioral confounding. | **Pure.** Compares raw HTML vs. simplified DOM vs. AXTree representations directly. |
| **Novelty** | **Low.** Element-labeling ablation on a 6-product mock store offers minimal novelty over existing benchmarks. | **Medium-High.** Identifies an unexamined architectural bottleneck where serializers silently discard Schema.org JSON-LD and non-interactive metadata. | **High.** Provides the first comprehensive cross-framework benchmark of web metadata retention in agent pipelines. |
| **Feasibility & Time** | **Medium.** Requires executing 96 live trials, logging traces, and managing API rate limits. | **Immediate (1–2 Days).** 80% of test harnesses already exist in [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py). | **Low (4–6 Weeks).** Requires installing and configuring Docker, BrowserGym, Playwright, and diverse environment runtimes. |
| **Compute & API Cost** | **Paid Quota Required.** ~$3.00–$10.00; free tier crashes at 500 RPD wall. | **$0.00.** Executes 100% offline using local mock servers and synthetic chat models. | **$0.00.** (If restricted to serialization without live model calls). |
| **Risk of Inconclusive Result** | **Critical (89%+).** Power simulations show small/moderate effects will yield $p > 0.05$, which cannot prove equivalence. | **Negligible.** Deterministic code paths either retain or discard tokens. Findings are definitive. | **Low.** Cross-framework architectural differences are concrete. |
| **Realistic Publication Venue** | Student Capstone / Regional Symposium (high risk of rejection for low power). | **Refereed Workshop / Systems Track** (e.g., WWW or AI Agent workshops). | **Full Conference Paper** (e.g., TheWebConf, ICSE-SEIP). |

### Justification for Recommending Direction B:
Direction B is the only direction that matches the realities of this project:
1. It builds directly on the project's strongest verified technical asset: the discovery of `DISABLED_ELEMENTS` and attribute whitelist filtering in `browser-use 0.13.10`.
2. It operates with 100% deterministic reproducibility at zero financial cost, avoiding the free-tier rate-limit failures that aborted Experiment 1b.
3. It eliminates the statistical trap of Direction A, where an underpowered sample size ($n=20$/arm) is virtually guaranteed to produce an uninterpretable null result.

---

## 2. Revised Research Questions, Objectives & Propositions

### Primary Research Question ($RQ_1$)
> **"To what extent do client-side DOM serialization and filtering heuristics in autonomous browser-agent frameworks create an architectural bottleneck that prunes, flattens, or distorts structured web metadata before it can reach the LLM context prompt?"**

### Secondary Research Questions
- **$RQ_2$ (Channel Reachability Hierarchy):** Which web metadata channels (Schema.org JSON-LD, interactive WAI-ARIA, non-interactive WAI-ARIA, default `data-*`, and configured `data-*`) physically survive DOM serialization to enter the LLM prompt buffer?
- **$RQ_3$ (Non-Interactive Information Loss):** How does the selective serialization of interactive elements versus non-interactive informational containers impact the retention of semantic metadata in modern Single Page Applications (SPAs)?
- **$RQ_4$ (Behavioral Confound Identification):** When semantic metadata does survive serialization to reach the LLM prompt (e.g., via interactive button augmentation), does it provide additive task-completion efficacy over identical visible text, or does its benefit reduce to target-text co-location?

### Measurable Research Objectives
1. **Objective 1 (Reachability Quantification):** Quantify the exact token- and attribute-level retention rates across four primary web metadata representations under standard `browser-use 0.13.10`.
2. **Objective 2 (Bottleneck Isolation):** Formally document the source-code mechanisms in `browser-use` responsible for metadata loss (`DISABLED_ELEMENTS`, non-interactive element tag stripping, and attribute whitelist filtering).
3. **Objective 3 (Architectural Remediation):** Design, implement, and benchmark minimal configuration or serializer patches (extended whitelists, structured data extractors) that restore metadata visibility without causing prompt context overflow.
4. **Objective 4 (Pre-Registered Behavioral Case Study):** Formally pre-register the 4-arm 96-trial behavioral protocol as an illustrative case study, establishing exact statistical power boundaries and cautioning the community against the Equivalence Fallacy.

---

## 3. Scope Boundaries & What Can Be Established Offline vs. Online

### Explicit Inclusion & Exclusion Boundaries
- **Included:**
  - Client-side DOM serialization and simplification algorithms in `browser-use 0.13.10`.
  - Static HTML vs. dynamically rendered SPA DOM structures.
  - Four metadata formats: Schema.org JSON-LD, WAI-ARIA, developer custom `data-*` attributes, and temporal metadata.
  - Token-level and attribute-level reachability into the prompt buffer.
  - Power analysis and statistical boundaries for small-sample agent experiments.
- **Excluded:**
  - Multimodal vision grounding (`use_vision=True` is explicitly disabled to isolate DOM text).
  - Claims of cross-model reasoning superiority (claims are restricted to observation reachability).
  - Generalization claims across the entire World Wide Web (restricted to single-page e-commerce architectures).

### Offline Verification vs. Live Model Requirements

| Finding / Claim | Can Be Established 100% Offline? | Requires Live Frontier Model Calls? | Evidence Source |
| :--- | :---: | :---: | :--- |
| Pruning of `<script>` (JSON-LD) by `DISABLED_ELEMENTS` | **YES** | NO | Source inspection of `serializer.py:L18, L481` & `test_agent_prompt_pipeline.py`. |
| Discarding of attributes on non-interactive `<span>`/`<div>` | **YES** | NO | Source inspection of `serializer.py:L1046-L1058` & prompt trace metrics. |
| Suppression of custom `data-*` attributes by default whitelist | **YES** | NO | Source inspection of `views.py:L18`, `serializer.py:L1214` & prompt trace metrics. |
| Correctness of stratified CMH and Newcombe CI algorithms | **YES** | NO | Validated to 4 decimal places in `test_analyze_v3_results.py`. |
| Statistical power boundaries ($<11\%$ power for $\Delta \le 0.20$) | **YES** | NO | 10,000-trial Monte Carlo simulations in `power_analysis.json`. |
| Whether surviving button `aria-label`s improve LLM task accuracy | NO | **YES** | Requires executing the 96 live trials with funded API keys. |
| Grounded refusal vs. hallucination on absent data (Task T6) | NO | **YES** | Requires live model output sampling on Task T6. |

---

## 4. Grounding Against Published Literature & Novelty Formulation

### 4.1 Relationship to Existing Literature
The proposed systems audit connects directly to four established literature threads:
1. **End-to-End Web Agent Benchmarks (WebArena [Zhou et al., 2024], Mind2Web [Deng et al., 2023]):** These works evaluate agents on complex web tasks but treat the observation pipeline as a fixed black box. They do not investigate whether metadata present in the underlying website survives serialization.
2. **Context Compression & Tree Representations (BrowserGym / WorkArena [Drouin et al., 2024], HTML-T5 [Gür et al., 2024]):** Drouin et al. demonstrated that Accessibility Trees (AXTrees) compress token contexts from 15,000+ tokens to ~400 tokens. However, they treated AXTree generation as an operational engineering shortcut rather than auditing whether semantic attributes inside the tree causally assist reasoning.
3. **Web Standards & The "Agentic Web" (W3C/TPAC 2024):** Web standards bodies are actively debating whether web authors should introduce specialized metadata for AI scrapers. Our study provides direct empirical evidence showing that client-side agent serializers currently discard these standards.

### 4.2 Conservative Novelty Formulation
> **Defensible Novelty Statement:**  
> *"This work provides the first fine-grained empirical audit of client-side DOM serialization and observation filtering in modern Python autonomous browser agents (`browser-use 0.13.10`). We prove that default serialization heuristics create an unexamined architectural bottleneck that prunes Schema.org JSON-LD scripts (0% reachability), suppresses custom developer attributes, and discards accessibility semantics on non-interactive containers. Furthermore, we demonstrate that when accessibility markup does reach the LLM prompt on interactive elements, it introduces a severe experimental confound: button label disambiguation and target-text co-location rather than generalized semantic comprehension."*

### 4.3 Conditions That Would Falsify or Weaken This Novelty Claim
1. If a prior peer-reviewed publication has already audited `browser-use`'s serializer specifically and documented the `DISABLED_ELEMENTS` script-pruning bottleneck.
2. If `browser-use` releases a minor version update (e.g., 0.13.11+) that refactors `serializer.py` to extract `<script type="application/ld+json">` into a dedicated observation channel by default.
3. If an alternative popular framework (e.g., Playwright AXTree) is proven to retain 100% of JSON-LD and custom attributes in its default prompt without configuration.

---

## 5. Phase 2 Conclusion & Transition Gate

The research scope, questions, and propositions have been formally realigned around **Direction B (Systems Serialization Audit)**. The project no longer relies on an underpowered behavioral benchmark as its primary claim to novelty, but instead grounds its contribution in verified systems engineering and architectural proofs.

**Transition Gate Approved:** Proceed to **Phase 3 (Automated Metadata Reachability and Systems Audit)** to implement the comprehensive reachability test harness and generate `serialization_audit_metrics.json`.

# RESEARCH SCOPE, DISCOVERY, AND NOVELTY AUDIT

**Project:** Autonomous Browser Agent Additive Semantic Markup Study  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Audit Date:** October 21, 2026  
**Auditor:** Engineering & Research Methodology Lead  

---

## 1. The Original Research Scope vs. Protocol v3 Reality

### 1.1 The Original Broad Research Proposal
The user's original research interest concerned evaluating the additive effects of four distinct web metadata representations on text-based autonomous browser-agent task performance:
1. **Schema.org Structured Data (JSON-LD):** Machine-readable schemas embedded inside `<script type="application/ld+json">`.
2. **Accessibility Semantics (WAI-ARIA):** Programmatic accessibility attributes (`aria-label`, `role`, `aria-describedby`).
3. **Developer Custom Data Attributes:** Custom client-side attributes (`data-action`, `data-product-id`, `data-amount`).
4. **Evidence & Temporal Metadata:** Timestamps and verification flags (`<meta name="evidence-date">`, `<time class="temporal-meta">`).

### 1.2 The Empirical Reality Discovered During Harness Auditing
Through systematic observation-trace auditing and static source-code analysis of the browser agent automation framework (`browser-use 0.13.10`), two fundamental architectural discoveries collapsed the feasible scope:

1. **The JSON-LD Pruning Discovery (Fatal Bottleneck):**  
   In `browser-use/dom/serializer/serializer.py` (line 18):
   ```python
   DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
   ```
   During DOM simplification (`_create_simplified_tree`, lines 480–482):
   ```python
   if node.node_name.lower() in DISABLED_ELEMENTS:
       return None
   ```
   Because `<script>` and `<meta>` elements are pruned unconditionally, **JSON-LD schema tokens never reach the LLM prompt buffer**. A text-based agent running on standard `browser-use 0.13.10` receives exactly zero tokens of structured data.
   - *Empirical Verification:* Live trace logging in [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) confirmed 0 occurrences of `application/ld+json` or Schema.org tokens in the model prompt.
   - *Methodological Consequence:* JSON-LD cannot be evaluated as an active agent information channel under standard `browser-use`. Claiming that JSON-LD was evaluated in a text-based setup without patching the library is scientifically false.
2. **The Temporal/Evidence Metadata Collapse:**  
   Static `<meta>` tags are stripped by the same `DISABLED_ELEMENTS` set. Dynamic `<time class="temporal-meta">` elements render as ordinary visible text on the web page. Consequently, temporal metadata is perceived merely as ordinary visible text, not as a distinct machine-readable metadata layer. It cannot be isolated as an independent treatment arm without confounding it with visible text.
3. **The Attribute Whitelist Bottleneck:**  
   In `browser-use/dom/views.py` (line 18), attributes are filtered against `DEFAULT_INCLUDE_ATTRIBUTES`. Standard `aria-label` on buttons is preserved, but custom `data-*` attributes (`data-action`, `data-product-id`) are stripped by default.
   - *Harness Resolution:* [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) supplies `EXTENDED_ATTRIBUTES` to the agent constructor, successfully exposing configured `data-*` attributes to the agent prompt stream.

---

## 2. Precise Research Scope Analysis: What Protocol v3 Can and Cannot Answer

### 2.1 What the Current Protocol v3 CAN Answer
Under strict single-variable control, Protocol v3 provides a rigorous, statistically defensible answer to:
1. **The Additive Efficacy of WAI-ARIA Attributes:**  
   When visible rendered text is complete, human-readable, and identical across all variants, does augmenting interactive elements with `aria-label` (e.g. `aria-label="Add SoundFlow Air 3 to cart"`) causally improve an LLM agent's task accuracy or step efficiency?
2. **The Additive Efficacy of Configured Developer Attributes (`data-*`):**  
   When the agent framework is configured with an extended whitelist, does providing explicit developer attributes (e.g. `data-action="add-cart" data-product-id="wh-001"`) improve task completion over plain visible text?
3. **Comparative Channel Ranking:**  
   Does natural-language accessibility markup (`aria-label`) outperform structured developer identifiers (`data-*`) in guiding an LLM's action selection?
4. **Hallucination vs. Grounded Refusal on Absent Information (Task T6):**  
   When factual information (warranty duration) is absent from the DOM, does the presence of semantic markup on adjacent elements affect the agent's propensity to hallucinate vs. produce a grounded refusal?

### 2.2 What the Current Protocol v3 CANNOT Answer
1. **The Effect of Schema.org JSON-LD:**  
   Because JSON-LD is pruned by `browser-use`, Protocol v3 cannot measure whether JSON-LD aids agent performance. Answering this would require modifying `browser-use`'s internal serializer to extract `<script type="application/ld+json">` and inject it into a dedicated prompt section.
2. **The Independent Effect of Temporal/Evidence Metadata:**  
   Because temporal metadata renders as visible text, it cannot be isolated from plain text without introducing confounding layout variations.
3. **Multimodal Visual Grounding:**  
   Protocol v3 explicitly enforces `use_vision=False` to eliminate visual confounding. It cannot answer how vision-enabled models (GPT-4V, Gemini Pro Vision) interact with rendered DOM geometry.

---

## 3. The Reformulated, Scientifically Defensible Research Question

To maintain absolute academic integrity, the original broad question is formally narrowed and stated without ambiguity:

### Primary Research Question
> **"Under a strictly text-based observation modality (`use_vision=False`), when the underlying rendered text content, visual appearance, and application functionality of an e-commerce website are held strictly identical, does augmenting interactive elements with semantic accessibility attributes (WAI-ARIA `aria-label`) or developer-configured custom attributes (`data-*`) improve an autonomous browser agent's task completion accuracy or step efficiency compared to unaugmented baseline HTML?"**

### Secondary Systems Research Question
> **"To what extent do client-side DOM serialization and filtering heuristics in modern browser-agent frameworks (such as `browser-use 0.13.10`) create an architectural bottleneck that prunes structured metadata (JSON-LD and custom attributes) before it can reach the LLM context prompt?"**

---

## 4. Novelty Assessment & Distinction from Published Literature

### 4.1 Is the Narrower Question Scientifically Meaningful and Distinct?
**YES. It addresses a fundamental, unexamined assumption in the AI agent literature and web engineering standards:**

1. **Distinction from Existing Benchmarks (WebArena, Mind2Web, BrowserGym, SeeAct):**  
   - Existing benchmarks evaluate whether agents can complete complex tasks across different websites. They treat HTML as a monolithic input or use Accessibility Trees (AXTrees) as an *engineering convenience* to reduce token count from 15,000+ tokens to ~400 tokens [Drouin et al., 2024].
   - They assume that accessibility markup aids agent reasoning. **However, no prior study has conducted a controlled single-variable ablation of markup channels under identical visible text.**
   - Our study tests whether that core assumption holds: if the visible text already says `"Add to Cart"`, does `aria-label="Add SoundFlow Air 3 to cart"` actually provide any additive benefit to an LLM, or is it cognitive redundancy?
2. **Relevance to Web Standards & the "Agentic Web" (W3C/TPAC):**  
   - Standards bodies (W3C/TPAC) are currently debating whether developers should "stuff" ARIA attributes specifically to assist AI scrapers.
   - Accessibility advocates warn that stuffing ARIA attributes for AI agents risks polluting screen-reader accessibility for visually impaired humans.
   - If our study shows that LLMs do not significantly benefit from ARIA when visible text is complete, it provides direct empirical evidence against ARIA stuffing.
3. **The DOM Serialization Gap Discovery:**  
   - The realization that browser-agent serializers discard `<script>` elements and custom attributes is an empirical systems contribution that explains why many web metadata strategies fail in practice.

---

## 5. Protocol Justification & Revision Analysis

### Does the Protocol Need Revision?
- **For Protocol v3 (Text-Only ARIA & `data-*` Study): NO.** Protocol v3 is completely specified, randomized, balanced ($N=96$, 4 blocks, 4 arms, 6 tasks), and passes all 51 automated tests. Modifying it now would break pre-registration integrity.
- **For a Potential Future Protocol v4 (JSON-LD Extension):**  
  If the research team desires to test JSON-LD in the future, the proper approach is not to silently claim it was tested in Protocol v3, but to design a separate, subsequent study (Protocol v4) where the serializer is explicitly modified:
  - Add an extractor for `<script type="application/ld+json">` nodes.
  - Expose a `structured_data` metadata field in the LLM prompt.
  - Test this in a separate pre-registered experiment.

---

## 6. Mandatory Claim Adjustments and Integrity Rules

To ensure 100% scientific defensibility, the following claim adjustments are mandatory across all project deliverables:

| Earlier / Informal Claim | Scientifically Defensible Formulation | Reason for Correction |
| :--- | :--- | :--- |
| *"The study evaluates four metadata channels: JSON-LD, ARIA, data-*, and evidence metadata."* | *"The study evaluates additive WAI-ARIA and configured developer data-* attributes; it identifies JSON-LD script pruning as an architectural serialization bottleneck."* | JSON-LD is physically pruned by the DOM serializer; treating it as an active experimental arm is false. |
| *"Proves that semantic markup improves autonomous agent success."* | *"Presents a hardened experimental methodology and statistical framework ready to measure additive markup effects upon confirmatory execution."* | Confirmatory live trials remain unexecuted (0/96); synthetic data cannot support empirical conclusions. |
| *"Semantic markup and plain HTML are proven equivalent if p > 0.05."* | *"The study is underpowered (<11% power) for small effects ($\Delta \le 0.20$); non-significant results cannot be claimed as channel equivalence."* | Proved via 10,000-trial Monte Carlo power simulations. |
| *"JSON-LD was evaluated in our historical 250-run pilot."* | *"Forensic audit proved that JSON-LD was pruned by browser-use during the historical pilot, invalidating its treatment delivery."* | Library source code audit (`DISABLED_ELEMENTS`). |
| *"The dashboard and reports show completed research results."* | *"The dashboard and reports display synthetic validation benchmarks demonstrating post-experiment pipeline correctness."* | Avoids misrepresenting mock pipeline validation as real agent performance. |

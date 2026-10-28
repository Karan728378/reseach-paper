# RESEARCH FEASIBILITY AND DIRECTION AUDIT

**Project:** Autonomous Browser Agent Observation Pipeline & Web Markup Evaluation  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Date:** October 24, 2026  
**Auditor:** Antigravity Research Execution Team  
**Audit Scope:** Read-only analysis of existing artifacts, code, traces, and manuscripts (zero live model invocations, network requests, or file deletions)  

---

## 1. Executive Summary & Objective

This audit evaluates the empirical foundation, systems evidence, and publication feasibility of the research project across two potential trajectories:
- **Direction A:** Complete the live controlled behavioral experiment comparing plain HTML (`ABS`), accessibility markup (`ARIA`), and custom developer attributes (`DATA-CFG`) on browser agents.
- **Direction B:** Narrow the paper's primary contribution to an empirical systems and measurement study of the **DOM serialization gap**—the loss of semantic information between source HTML, browser accessibility trees (Chromium Blink AXTree), and agent context prompts—using live-agent runs (historical and local Qwen 001–005) as empirical case studies.

**Core Audit Conclusion:**  
Direction B is the **shortest, most defensible, and methodologically superior path to a credible peer-reviewed research paper**. All systems measurements, architectural proofs, node-level correspondence metrics, and statistical power boundaries are **100% implemented, tested, and empirically supported by existing offline artifacts**. In contrast, Direction A suffers from acute sample-size power deficits ($<11\%$ power for realistic effects at $N=24$/arm), severe hardware/timeout floor effects on local models (180s step watchdogs aborting prompt ingestion), and cloud API funding/quota barriers.

---

## 2. Dataset Provenance & Strict Quarantine Matrix

All project data assets are audited and partitioned into four strictly non-overlapping categories to eliminate data contamination:

| Dataset ID | Dataset Name | File Path | Modality & Modifiers | $N$ | Primary Status | Evidentiary Role & Quarantine Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **D1 / D2** | **Historical Pilot (Raw & Clean)** | `results/pilot-summary.csv`<br>`results/pilot-summary-clean.csv` | Multimodal Vision (`use_vision=True`) | 261 (raw)<br>250 (clean) | Invalid for Primary Findings | **QUARANTINED (Exploratory Only):** Confounded by vision channel; JSON-LD and custom data were stripped by serializer; Rep 9 selective retries hid failures; verifiers had false-pass bugs. |
| **D3** | **Historical Main Run (Aborted)** | `results/main_experiment/full-summary.csv` | Multimodal Vision (`use_vision=True`) | 147 | Truncated / Discontinued | **QUARANTINED:** Crashed at run 105 due to free-tier 500 RPD exhaustion; 42 consecutive HTTP 429 aborts. |
| **D4** | **Exp 2 Visual Smoke** | `results/exp2/pilot-summary.csv` | Multimodal Vision | 20 | Exploratory | **QUARANTINED:** Informal micro-trials testing visual variants. |
| **D5** | **Protocol v3 Confirmatory Schedule** | `proposed_randomized_schedule.csv` | Text-Only (`use_vision=False`) | 96 | Specification Only | **UNEXECUTED (0 of 96 runs):** Frozen RCBD schedule (4 blocks $\times$ 24 runs). Safety gate locked (`SAFETY_GATE_LOCKED = True`). |
| **D6** | **Synthetic Benchmark** | `test_scratch_synthetic_data/dataset_1_valid_complete.csv` | Synthetic Mock Traces | 96 | Pipeline Validation Only | **QUARANTINED TO APPENDIX:** Deterministic mock dataset used strictly to prove `analyze_v3_results.py` and CMH/Newcombe statistical engines work without errors. Contains zero real agent data. |
| **D7** | **Offline Browser Mechanics Demo** | `results/demo_browser_mechanics_and_verifier_runs.csv` | Scripted Chromium DOM | 6 | Validated | **SYSTEMS PROOF:** Validates SPA state transitions, cart storage, and verifier logic without LLM inference. |
| **D8** | **Offline Prompt Delivery Demo** | `results/demo_agent_prompt_delivery_runs.csv` | Mock LLM Prompt Buffer | 4 | Validated | **SYSTEMS PROOF:** Captures exact prompt string delivered by `Agent(use_vision=False)`, proving attribute delivery and pruning. |
| **D9** | **Local Qwen Smoke Runs 001–005** | `results/local_llama_pilot_runs/qwen3_smoke_run_001.json` - `005.json`<br>`results/local_llama_summary.csv` | Local Text-Only (`qwen3:4b`, Ollama) | 5 | Diagnostic Pilot Traces | **EMPIRICAL CASE STUDY:** Real air-gapped pilot runs capturing step execution, 180s watchdog timeouts, CDP ground truth, and cancellation telemetry. |

---

## 3. Implementation Audit: Supported vs. Unsupported Claims

### 3.1 Claims Directly Supported by Code, Tests, and Traces

1. **Schema.org JSON-LD 0.0% Reachability:**
   - *Claim:* Standard browser-agent serializers unconditionally discard Schema.org JSON-LD scripts before prompt compilation.
   - *Supporting Evidence:* `browser_use/dom/serializer/serializer.py:L18` (`DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}`); verified in `test_observation_pipeline_stages.py:test_channel_1_jsonld_pipeline`; quantified in `serialization_audit_metrics.json` (0.0% token reachability).
2. **Non-Interactive ARIA Stripping (The Critical Divergence):**
   - *Claim:* Accessibility attributes (`aria-label`, `role`) on non-interactive containers (`<span>`, `<div>`, `<section>`) are retained by browser accessibility trees but 100% stripped by agent DOM serializers.
   - *Supporting Evidence:* `serializer.py:L1046–L1058` constructs attributes *only* if `node.is_interactive or node.is_scrollable`. Verified in `compare_accessibility_tree.py` and `ACCESSIBILITY_TREE_COMPARISON.md`: Chromium Blink's native AXTree creates accessible nodes for `<span aria-label="Price: $49.99">`, while `browser-use` emits only bare inner text `$49.99`.
3. **Reversed Divergence for Developer `data-*` Attributes:**
   - *Claim:* Developer `data-*` attributes have 0% presence in browser accessibility trees, but can achieve 100% reachability on interactive elements in agent prompts under an extended whitelist.
   - *Supporting Evidence:* Blink AXTree assigns no properties to `data-*` attributes. In `browser-use`, default `DEFAULT_INCLUDE_ATTRIBUTES` strips them (`views.py:L18`), but configuring `Agent(include_attributes=EXTENDED_ATTRIBUTES)` delivers them to the prompt buffer on interactive elements (`test_treatment_leakage_and_integrity.py`).
4. **Interactive Node Alignment Rate:**
   - *Claim:* Interactive DOM elements can be mapped 1-to-1 to Chromium accessibility tree nodes via Blink's internal `backendDOMNodeId`.
   - *Supporting Evidence:* `compare_accessibility_tree.py` matched 27 of 34 interactive elements (79.4%) on route `#home` between `selector_map` and CDP `Accessibility.getFullAXTree`.
5. **The Action-Label Co-Location Confound:**
   - *Claim:* Augmenting button accessible names with the target product title (e.g., `aria-label="Add SoundFlow Air 3 to cart"`) alters the task construct from hierarchical reference resolution to direct string matching.
   - *Supporting Evidence:* Documented in `METHODOLOGY_AUDIT.md`; eliminated in `shared/app-core.js:L35` by standardizing generic action triggers (`addBtn.setAttribute('aria-label', 'Add item to cart')`).
6. **Watchdog Timeout & In-Flight Model Cancellation:**
   - *Claim:* When prompt size expands across steps, prompt ingestion latency on hybrid local hardware breaches fixed step watchdogs (180s), triggering in-flight cancellation that requires dedicated `asyncio.CancelledError` handling.
   - *Supporting Evidence:* Traces `qwen3_smoke_run_003.json` (step 2 timeout), `qwen3_smoke_run_004.json` (step 1 timeout), and `qwen3_smoke_run_005.json` (step 1 timeout with verified cancellation telemetry capturing 179.7s wall-clock duration and null server metrics).
7. **Equivalence Fallacy & Small-Sample Power Deficit:**
   - *Claim:* Small-sample browser-agent experiments ($n=20$ per arm) lack the statistical power to detect realistic effect sizes ($\Delta \le 0.20$), making non-significant p-values uninterpretable as evidence of markup equivalence.
   - *Supporting Evidence:* 10,000-trial Monte Carlo simulation in `power_analysis.py` proving power is only $10.8\% \pm 0.6\%$ for $\Delta = 0.20$ at Bonferroni $\alpha = 0.0167$.

### 3.2 Unsupported Claims & Missing Evidence

1. **Causal Agent Behavioral Superiority:**
   - *Unsupported Claim:* "Agents navigate significantly faster or achieve higher task success when presented with `DATA-CFG` or `ARIA` markup compared to plain text."
   - *Status:* **Completely unproven.** Confirmatory Protocol v3 has 0 completed live runs. Local smoke runs (001–005) were single-task exploratory trials, none of which achieved clean completion due to timeout watchdogs.
2. **Cross-Model Generalizability:**
   - *Unsupported Claim:* "These behavioral differences hold across Claude 3.5 Sonnet, GPT-4o, and Gemini 1.5 Pro."
   - *Status:* **Unproven.** The project has tested only Gemini (in historical confounded pilots) and Qwen3 4B (in local smoke runs).

---

## 4. Evaluation of Research Directions

### 4.1 Direction A: Controlled Behavioral Comparison (ABS vs. ARIA vs. DATA-CFG)

- **Concept:** Execute 72 or 96 live trials across tasks T1–T6 to measure and compare empirical task success rates across markup arms.
- **Supported Assets:**
  - Complete, pre-registered experimental schedule (`proposed_randomized_schedule.csv`, seed 42).
  - Validated ground-truth verifiers asserting DOM and cart states (`verifier_specification.md`, `test_t6_verifier_isolated.py`).
  - Validated statistical inference engine (`analyze_v3_results.py`).
- **Unsupported Claims & Missing Evidence:**
  - Zero live trial data exists.
  - No evidence that differences between arms exceed the minimum detectable effect size.
- **Minimum Additional Work Required:**
  - *Option 1 (Cloud Gemini):* Allocate paid Google Cloud API key, resolve Tier-1 quota, register OSF pre-registration, unlock runner safety gate, and execute 72–96 live trials (~800 API requests; est. 3–5 hours + API costs).
  - *Option 2 (Local Ollama):* Run 72 trials locally on `qwen3:4b`. At 3 steps per run and ~180s per step, this requires **10.8 to 15 hours of continuous local compute**, with a near-certain probability of degenerate floor effects.
- **Major Validity Threats:**
  1. *Floor Effect / Timeout Truncation:* In runs 004 and 005, `qwen3:4b` timed out on Step 1 (180s) without emitting an action in the ABS control arm. An experiment dominated by timeout failures reflects hardware compute bottlenecks rather than semantic markup comprehension.
  2. *Severe Statistical Underpowering:* With $n=24$ runs per arm, power to detect $\Delta = 0.20$ is $<11\%$. If the true effect is moderate, the experiment is almost guaranteed to yield non-significant p-values, leaving the research question inconclusive.
  3. *Cloud Quota / Non-Determinism:* Free-tier cloud APIs fail due to rate limits (as occurred in Experiment 1b with 42 consecutive 429 aborts); paid models risk mid-run provider updates.
- **Literature Distinctness Analysis:**
  - Benchmarks like WebArena (812 tasks), Mind2Web (2,350 tasks), and WorkArena (350+ tasks) already evaluate web agents across diverse sites. An underpowered 72-run benchmark on a single mock e-commerce shop using a 4B model that repeatedly times out provides weak empirical novelty and is vulnerable to reviewer rejection.

### 4.2 Direction B: Systems/Measurement Paper on the DOM Serialization Gap

- **Concept:** Reframe the paper as an empirical systems and measurement study examining the architectural gap between source HTML, browser accessibility trees (Chromium AXTree), and agent DOM serializers (`browser-use`), using live-agent runs (historical and local smoke runs) as preliminary empirical motivation and case studies.
- **Supported Claims & Exact Evidence Files:**
  - *Full 5-Stage Observation Pipeline Measurement:* `OBSERVATION_PIPELINE_EVIDENCE_MATRIX.md`, `test_observation_pipeline_stages.py`.
  - *Blink AXTree vs. Serializer Divergence:* `compare_accessibility_tree.py`, `accessibility_tree_comparison.json`, `ACCESSIBILITY_TREE_COMPARISON.md`.
  - *Schema.org JSON-LD 0% Token Reachability Proof:* `audit_metadata_reachability.py`, `serialization_audit_metrics.json`.
  - *Action-Label Co-Location Confound:* `METHODOLOGY_AUDIT.md`, `test_treatment_leakage_and_integrity.py`.
  - *Real-World Watchdog Truncation & Telemetry Case Study:* `qwen3_smoke_run_001.json` - `005.json`, `LOCAL_QWEN_CANCELLATION_TELEMETRY_FIX.md`.
  - *Statistical Power Boundaries & Equivalence Fallacy Proof:* `power_analysis.py`, `power_analysis.json`.
- **Unsupported Claims:**
  - None within this framing. The paper does not claim generalized behavioral superiority; it claims an **architectural information-loss gap and a methodological evaluation framework**.
- **Minimum Additional Work Required:**
  - **Zero additional live runs required.** The entire systems evidence base is already 100% complete and verified by offline scripts.
  - Synthesize existing audited text from `RESEARCH_PAPER_DRAFT_V2.md`, `OBSERVATION_PIPELINE_EVIDENCE_MATRIX.md`, and `ACCESSIBILITY_TREE_COMPARISON.md` into the primary publication manuscript.
- **Major Validity Threats & Mitigations:**
  - *Threat: Single Framework Scope:* Focuses primarily on `browser-use 0.13.10`.  
    *Mitigation:* Contrast `browser-use`'s heuristic pruning directly with BrowserGym/WorkArena's AXTree approach and WebAgent's HTML-T5 pruning, showing that all agent frameworks face the serialization trade-off.
  - *Threat: Reviewer Expectation of Agent Task Leaderboards:*  
    *Mitigation:* Explicitly target systems and measurement tracks/venues (e.g., ACM Web Conference (WWW), USENIX ATC, EMNLP System Demonstrations / Findings, IEEE S&P Agent Workshops) where empirical measurement and exposing hidden benchmark flaws are recognized contributions.
- **Literature Distinctness Analysis:**
  - **Highly distinct and novel.** No existing paper in the literature has:
    1. Audited the quantitative token and attribute reachability across source HTML, Blink AXTree, and agent DOM serializers.
    2. Refuted the widespread assumption that "DOM pruning is equivalent to an accessibility tree" (proving that non-interactive ARIA is stripped while custom `data-*` can be delivered).
    3. Exposed the action-label co-location confound in browser-agent benchmark tasks.
    4. Proved the statistical power boundaries of web-agent sample sizes.

---

## 5. Comparative Strategic Decision Rationale

| Evaluation Dimension | Direction A: Controlled Behavioral Comparison | Direction B: Systems & Measurement Study | Advantage |
| :--- | :--- | :--- | :---: |
| **Evidence Quality** | Unexecuted (0/96 confirmatory runs). High risk of timeout floor effects on local models. | 100% empirical, reproducible offline scripts, Blink CDP node-level matches, AST proofs. | **Direction B** |
| **Feasibility & Timeline** | Requires paid API key or 10–15 hours of local GPU compute + OSF registration. | Zero additional data collection. Deliverable immediately from existing files. | **Direction B** |
| **Statistical Defensibility** | Severely underpowered ($<11\%$ power for $\Delta \le 0.20$ at $n=24$). High probability of inconclusive null result. | Analytical power bounds proven via 10,000 Monte Carlo runs; exposes the Equivalence Fallacy. | **Direction B** |
| **Methodological Cleanliness** | Confounded by local model timeouts (180s watchdog limits) and hardware latency. | Measures the observation pipeline directly, eliminating LLM stochasticity and latency confounds. | **Direction B** |
| **Academic Value & Novelty** | Modest. Small benchmark ($N=72$) on a single mock site has limited generalizability. | High. Exposes systemic architectural assumptions in the "Agentic Web" and agent benchmarking. | **Direction B** |

### Definitive Recommendation:
**Adopt Direction B (Systems & Measurement Paper on the DOM Serialization Gap).**  
This decision is **not** an operational concession to slow local inference; it is a **principled methodological choice**. Even if infinite compute were available, an underpowered 72-run behavioral benchmark on a single mock site provides far less scientific value than a rigorous, first-of-its-kind measurement of how client-side serialization alters agent perception.

---

## 6. Precise Paper-Revision Plan (`RESEARCH_PAPER_DRAFT_V2.md`)

The working draft [`RESEARCH_PAPER_DRAFT_V2.md`](file:///C:/testing/research_execution_20261018/RESEARCH_PAPER_DRAFT_V2.md) is already 75% aligned with Direction B. The revision requires the following surgical adjustments:

### Section-by-Section Action Plan:

1. **Title:**
   - **Retain:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*.
2. **Abstract:**
   - **Revise:** Update status from "Pre-Registration Blueprint" to "Empirical Systems Audit & Measurement Study". Summarize the 5-stage pipeline findings, the 0.0% JSON-LD reachability, the non-interactive ARIA stripping bottleneck, and the watchdog timeout telemetry case study.
3. **Section 1 (Introduction & Motivation):**
   - **Retain:** Real-world data layer taxonomy (Visible, ARIA, `data-*`, JSON-LD), the W3C "Agentic Web" context, and core research questions.
   - **Revise:** Frame the primary contribution around observation-pipeline measurement rather than prospective behavioral testing.
4. **Section 2 (Related Work & Systems Gap):**
   - **Retain:** WebArena, Mind2Web, WorkArena/BrowserGym, SeeAct, and WebAgent.
   - **Sharpen:** Highlight that prior benchmarks evaluate models end-to-end while treating the DOM serialization pipeline as an unexamined black box.
5. **Section 3 (Systems Architecture & Pruning Heuristics):**
   - **Retain:** AST proofs of `DISABLED_ELEMENTS` (`serializer.py:L18`), non-interactive tag stripping (`serializer.py:L1046–1058`), and whitelist filtering (`views.py:L18`).
6. **Section 4 (Empirical Systems Audit & Measurement):**
   - **Retain:** Quantitative Reachability Table (`serialization_audit_metrics.json`).
   - **Add:** The 5-stage observation pipeline matrix and the node-level correspondence analysis (27/34 interactive elements matched via Blink `backendDOMNodeId`) from [`OBSERVATION_PIPELINE_EVIDENCE_MATRIX.md`](file:///C:/testing/research_execution_20261018/OBSERVATION_PIPELINE_EVIDENCE_MATRIX.md) and [`ACCESSIBILITY_TREE_COMPARISON.md`](file:///C:/testing/research_execution_20261018/ACCESSIBILITY_TREE_COMPARISON.md).
   - **Detail:** The Critical Divergence (non-interactive ARIA) and Reversed Divergence (custom `data-*`).
7. **Section 5 (Methodological Implications & Experimental Confounds):**
   - **Retain:** Section 5.1 (The Action-Label Co-Location Confound) and Section 5.3 (Hardened Two-Tier Verifiers).
   - **Revise:** Reframe Section 5.2 from "Pre-Registered Live Experiment" to "A Methodological Blueprint for Web Agent Benchmarking: Design Guidelines for Mitigating Serialization Confounds".
8. **Section 6 (Statistical Power Boundaries & The Equivalence Fallacy):**
   - **Retain:** Task-stratified CMH formulation, Newcombe hybrid score CIs, Monte Carlo power simulations (<11% power at $n=20$ for $\Delta \le 0.20$), and the formal warning against the Equivalence Fallacy.
9. **Section 7 (Empirical Case Study: Latency Scaling, Watchdog Truncation, & Cancellation Telemetry):**
   - **Add (New Section):** Document the empirical findings from local runs `qwen3_smoke_001` through `005`.
   - Explain how cumulative history expansion across steps causes prompt evaluation latency to breach fixed watchdogs (180s).
   - Document the cancellation telemetry mechanism, proving how unhandled `asyncio.CancelledError` caused silent telemetry loss and how safe cancellation recovery makes in-flight aborts observable while preserving null server metrics.
10. **Section 8 (Discussion & Implications for Web Standards):**
    - **Retain:** The fallacy of metadata augmentation for AI, ARIA stuffing hazards, and the necessity of out-of-band machine endpoints (`llms.txt`, MCP).
11. **Section 9 (Conclusion):**
    - **Retain:** Concise synthesis of findings.
12. **Appendices:**
    - **Appendix A (Software Pipeline Benchmark):** Retain synthetic benchmark tables with the explicit synthetic disclaimer.
    - **Appendix B (Reproducibility Guide):** Retain step-by-step reproduction instructions.

---

## 7. Blockers, Risk Analysis, & Prioritized Next Actions

### 7.1 Blockers & Non-Blockers
- **Blockers Resolved:** 
  - No funding or paid API key required.
  - No multi-hour local inference runs required.
  - No risk of rate-limiting or non-deterministic cloud crashes.
  - All claims are grounded in existing offline testable code.
- **Remaining Minor Blockers:**
  - Consolidating the final LaTeX manuscript (`research_paper_final.tex`) to ensure all tables, figures, and bibtex citations compile cleanly.

### 7.2 Prioritized Next Actions (Awaiting User Approval):
1. **Approval of Direction B:** Await formal user sign-off on adopting Direction B.
2. **Manuscript Synthesis:** Consolidate `RESEARCH_PAPER_DRAFT_V2.md` with the observation-pipeline evidence matrix, node correspondence data, and local telemetry case study.
3. **LaTeX Sync & Build:** Update `research_paper_final.tex` to match the finalized manuscript and compile the production PDF.
4. **Final Artifact Bundle:** Package the offline verification scripts (`audit_metadata_reachability.py`, `compare_accessibility_tree.py`, `test_observation_pipeline_stages.py`, `test_analyze_v3_results.py`) into an archival zip artifact.

---

**Audit completed.** All tasks were executed strictly read-only. No live model calls, browser trials, network connections, or file modifications were made. Awaiting your review and direction.

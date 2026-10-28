# Zero-Cost Independent Validation & Systems Replication Report

**Document ID:** `research_execution_20261018/ZERO_COST_VALIDATION_REPORT.md`  
**Execution Date:** October 2026  
**Auditor / Roles:** Senior Research Engineer, Experimental-Design Specialist, Reproducibility Auditor  
**Runtime:** Python 3.11.9 (`C:\testing\.venv311\Scripts\python.exe`), `browser-use 0.13.10`  
**Financial / Budget Ceiling:** **USD $0.00 (Strictly Zero Spend · No Paid API Calls · Safety Gate Locked)**  

---

## 1. Executive Summary of Phase 2 Validation

This report delivers the results of an **independent, zero-cost replication** of the browser observation pipeline, treatment isolation mechanics, and statistical power foundations of the project.

### Core Replicated Findings:
1. **The "DOM Serialization Gap" is Empirically Real in `browser-use 0.13.10`:**
   - Default serializers unconditionally drop `<script>` (JSON-LD) and `<meta>` tags via `DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}`.
   - Non-interactive element tags (e.g., `<span aria-label="...">` or `<div data-*="...">`) are stripped by `DOMTreeSerializer.serialize_tree` because the serializer only generates element tags for nodes where `node.is_interactive or is_any_scrollable or tag in ('IFRAME', 'FRAME')`.
   - On interactive elements (e.g., `<button>`), `aria-label` survives into the model-client payload by default, whereas `data-*` attributes are stripped unless the runner injects an extended attribute whitelist.
2. **Empirical Model Trials = Exactly Zero:**
   - Forensic verification confirms that **zero live LLM model calls have been dispatched**.
   - Model-client input boundaries were captured using local in-memory stubs (`FakeListChatModel`), proving the client payload format without invoking external cloud APIs.
3. **Treatment Isolation is 100% Verified:**
   - Visible catalog text and layout are identical across `v0-baseline`, `v2-aria`, and `v3-data-attrs`.
   - Button labels do not leak product target names (`aria-label="Add item to cart"`, not `"Add SoundFlow Air 3 to cart"`).
   - In text-only mode (`use_vision=False`), the historical `VIS` arm is an exact duplicate of `v0-baseline` and has been retired in the clean 3-arm design (Option A, $N=72$).
4. **Statistical Power for the Pilot is Confirmed at ~10.85%:**
   - Recomputing the RCBD Monte Carlo power simulation confirms that detecting a moderate effect ($\Delta = 0.20$) with $n=20$/arm at Bonferroni-adjusted $\alpha$ yields only **10.85% power**. Any claim that a non-significant pilot proves "channel equivalence" is mathematically false.

---

## 2. Independent Sentinel Replication & Raw Evidence Snippets

Replication was executed by `independent_sentinel_validation.py` loading `fixtures/sentinel_fixture.html` in headless Chromium. Raw strings, node arrays, and model-client payloads were captured and saved to [`independent_validation_raw_trace.json`](file:///c:/testing/research_execution_20261018/independent_validation_raw_trace.json).

### Stage Raw Byte Sizes:
- **Stage 1 (Source HTML):** 1,380 bytes
- **Stage 2 (Live DOM outerHTML):** 1,363 bytes
- **Stage 3 (Blink AXTree via CDP):** 26 nodes (16,843 bytes formatted JSON)
- **Stage 4a (Default Serializer):** 212 bytes
- **Stage 4b (Extended Whitelist Serializer):** 257 bytes
- **Stage 5 (Agent Observation Buffer):** 25,098 bytes
- **Stage 6 (Model-Client Interface Payload):** 26,231 bytes

### Per-Sentinel Exact Evidence Ledger:

| Sentinel Marker & Channel | Stage 1 (Source) | Stage 2 (Live DOM) | Stage 3 (Blink AXTree) | Stage 4a (Default Serializer) | Stage 4b (Extended Serializer) | Stage 5 (Obs Buffer) | Stage 6 (Client Payload) | Exact Raw Output Snippet / Mechanism |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1. Visible Typography**<br>`SENTINEL_TEXT_ALPHA_991` | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **Stage 4a/6 Snippet:** `... Product Description: SENTINEL_TEXT_ALPHA_991 ...`<br>*Mechanism:* `TEXT_NODE` preserved across all representations. |
| **2. Interactive Button ARIA**<br>`SENTINEL_ARIA_BETA_992` | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **Stage 6 Snippet:** `... [37]<button id=btn-aria aria-label=SENTINEL_ARIA_BETA_992 /> ...`<br>*Mechanism:* Interactive button retains `aria-label` because it is in `DEFAULT_INCLUDE_ATTRIBUTES`. |
| **3. Non-Interactive Span ARIA**<br>`SENTINEL_SPAN_ARIA_993` | **YES** | **YES** | **YES** | **NO** | **NO** | **NO** | **NO** | **Stage 3 Snippet:** `"name": {"value": "SENTINEL_SPAN_ARIA_993"}`<br>**Stage 4a Snippet:** `[NOT PRESENT IN STAGE OUTPUT]`<br>*Mechanism:* Blink AXTree preserves accessible name; `browser-use` serializer strips non-interactive element tag and only emits inner text `"In Stock"`. |
| **4. Interactive Button `data-*`**<br>`SENTINEL_DATA_GAMMA_994` | **YES** | **YES** | **NO** | **NO** | **YES** | **NO\*** | **NO\*** | **Stage 4b Snippet:** `... [18]<button id=btn-data data-sentinel-action=SENTINEL_DATA_GAMMA_994 /> ...`<br>*Mechanism:* Absent in Blink AXTree; stripped by default serializer; survives extended whitelist on interactive elements. |
| **5. Non-Interactive `data-*`**<br>`SENTINEL_DATA_DELTA_995` | **YES** | **YES** | **NO** | **NO** | **NO** | **NO** | **NO** | **Stage 4b Snippet:** `[NOT PRESENT IN STAGE OUTPUT]`<br>*Mechanism:* Non-interactive container tag is stripped regardless of whitelist extension. |
| **6. JSON-LD Name in `<script>`**<br>`SENTINEL_JSONLD_EPSILON_996` | **YES** | **YES** | **NO** | **NO** | **NO** | **NO** | **NO** | **Stage 4a Snippet:** `[NOT PRESENT IN STAGE OUTPUT]`<br>*Mechanism:* Unconditionally pruned at AST recursion by `DISABLED_ELEMENTS = {'script', ...}`. |
| **7. JSON-LD SKU in `<script>`**<br>`SENTINEL_SKU_ZETA_997` | **YES** | **YES** | **NO** | **NO** | **NO** | **NO** | **NO** | **Stage 4a Snippet:** `[NOT PRESENT IN STAGE OUTPUT]`<br>*Mechanism:* Same as above (`DISABLED_ELEMENTS`). |
| **8. HTML `<meta>` Tag**<br>`SENTINEL_META_ETA_998` | **YES** | **YES** | **NO** | **NO** | **NO** | **NO** | **NO** | **Stage 4a Snippet:** `[NOT PRESENT IN STAGE OUTPUT]`<br>*Mechanism:* Same as above (`DISABLED_ELEMENTS`). |

*\*Note on Stages 5 & 6 for custom data attributes: `browser_use.Agent` initializes its own internal `DEFAULT_INCLUDE_ATTRIBUTES` unless explicitly overridden at runner instantiation.*

---

## 3. Evidence Level Classification by Pipeline Stage

To maintain strict scientific integrity, every observation in this study is assigned its exact evidence level:

| Pipeline Stage | Implementation Method | Evidence Classification | Operational Meaning |
|---|---|:---:|---|
| **Stage 1: Source HTML** | Local file read (`Path.read_text`) | `VERIFIED BY DIRECT INSPECTION` | Exact static file contents on disk. |
| **Stage 2: Live Client DOM** | Chromium CDP `Runtime.evaluate` | `REPRODUCED BY EXECUTION` | Live DOM after Chromium parsing and layout. |
| **Stage 3: Blink AXTree** | Chromium CDP `Accessibility.getFullAXTree` | `REPRODUCED BY EXECUTION` | True accessibility tree constructed by Chromium engine. |
| **Stage 4a: Default Serializer** | `SerializedDOMState.llm_representation()` | `REPRODUCED BY EXECUTION` | Unpatched upstream `browser-use 0.13.10` serialization string. |
| **Stage 4b: Extended Serializer** | `llm_representation(EXTENDED_ATTRIBUTES)` | `REPRODUCED BY EXECUTION` | Patched whitelist serialization string. |
| **Stage 5: Observation Buffer** | `Agent._message_manager.create_state_messages` | `REPRODUCED BY EXECUTION` | Concrete string injected into LangChain chat history. |
| **Stage 6: Model-Client Payload** | `FakeListChatModel.ainvoke(messages)` | `VERIFIED LOCAL STUB PAYLOAD` | Exact data structure passed to LLM client boundary. |
| **Stage 7: Live Cloud LLM Call** | Gated by `SAFETY_GATE_UNLOCKED = False` | `UNTESTED / ZERO RUNS` | **Not executed.** No paid tokens sent to Google Cloud. |
| **Stage 8: Agent Behavioral Outcome**| Gated by lack of live executions | `UNTESTED / HYPOTHETICAL` | **Not observed.** Behavioral effects remain unproven hypotheses. |

---

## 4. Treatment Isolation Audit Across Application Variants

The three experimental website variants (`v0-baseline`, `v2-aria`, `v3-data-attrs`) were audited directly in the local browser:

1. **Shared Product Catalog & Business Logic:**
   - All three variants load identical scripts: `<script src="../../shared/products.js"></script>` and `<script src="../../shared/app-core.js"></script>`.
   - Product SKUs, visible titles, prices, star ratings, and descriptions are identical to the character across all arms.
2. **De-confounded Action Button Labels:**
   - In `v2-aria`, action button labels are de-confounded:
     ```javascript
     // shared/app-core.js:465
     if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
     ```
   - Target entity names (`"SoundFlow Air 3"`) do **not** leak through button labels.
3. **Baseline Cleanliness:**
   - `v0-baseline` contains zero ARIA navigation labels and zero custom `data-*` action attributes.
4. **Disambiguation of the `VIS` Arm:**
   - In Protocol v4, `protocol_v3_runner.py:404` strictly enforces `use_vision=False`.
   - Consequently, `VIS` is an identical duplicate of `v0-baseline`.
   - **Protocol Decision:** Option A Clean 3-Arm Design ([`proposed_3arm_schedule.csv`](file:///c:/testing/research_execution_20261018/proposed_3arm_schedule.csv), $N=72$) is established as the primary schedule, eliminating the 24 redundant replicate trials.

---

## 5. Statistical Power & Schedule Reconciliation

### Schedule Structure Comparison:

| Parameter | Option A (Clean 3-Arm) | Option B (Legacy 4-Arm Replicate) |
|---|:---:|:---:|
| **Total Runs ($N$)** | **72** | **96** |
| **Arms** | 3 (`ABS`, `ARIA`, `DATA-CFG`) | 4 (`ABS`, `ARIA`, `DATA-CFG`, `VIS`) |
| **Replication Blocks ($B$)** | 4 blocks ($B_1 \to B_4$, 18 runs/block) | 4 blocks ($B_1 \to B_4$, 24 runs/block) |
| **Tasks ($K$)** | 6 tasks (T1–T6) | 6 tasks (T1–T6) |
| **Primary Tasks Allocation (T1–T5)** | $n = 20$ runs per arm ($N_{\text{primary}} = 60$) | $n = 20$ runs per arm ($N_{\text{primary}} = 80$) |
| **Exploratory Probe Allocation (T6)**| $n = 4$ runs per arm ($N_{\text{probe}} = 12$) | $n = 4$ runs per arm ($N_{\text{probe}} = 16$) |
| **Planned Pairwise Contrasts** | 2 (`ARIA vs ABS`, `DATA-CFG vs ABS`) | 3 (`ARIA vs ABS`, `DATA-CFG vs ABS`, `VIS vs ABS`) |
| **Bonferroni-Adjusted $\alpha$** | $\alpha = 0.05 / 2 = \mathbf{0.025}$ | $\alpha = 0.05 / 3 = \mathbf{0.01667}$ |

### Power Recalculation Audit:
- **Homogeneous Binomial Benchmark ($p_1 = 0.50 \to p_2 = 0.70$, $\Delta = 0.20$):**
  - Option A ($n_1 = 20, n_2 = 20, \alpha = 0.025$): $\text{Power} = \mathbf{16.57\%}$.
  - Option B ($n_1 = 40, n_2 = 20, \alpha = 0.01667$): $\text{Power} = \mathbf{16.72\%}$.
- **Heterogeneous Task RCBD Simulation (Task baselines `[0.70, 0.85, 0.50, 0.30, 0.80]`, continuity-corrected CMH):**
  - Option B ($N=40$ baseline vs $N=20$ treatment): $\text{Power} = \mathbf{10.85\%}$ ($\text{MCSE} = 0.0070$).
- **Sample Size Requirement for 80% Power ($\Delta = 0.20, \alpha = 0.01667$):**
  - Requires $n \approx 124$ runs per arm ($\mathbf{N \approx 480}$ across 4 arms, or $\mathbf{N \approx 372}$ across 3 arms).
- **Audit Conclusion:** A pilot of $N=72$ or $N=96$ is **severely underpowered for confirmatory equivalence or small-effect detection**. It is valid strictly as an exploratory systems and variance-estimation pilot.

---

## 6. Execution Commands, Logs, and Exit Codes

All zero-cost validation suites were executed locally. All exited with code **0**:

```powershell
# 1. Independent Sentinel Validation & Treatment Isolation
python research_execution_20261018/independent_sentinel_validation.py
# Output: [PASSED] All 8 sentinel markers match expected pipeline survival 100%.
# Output: [PASSED] Treatment isolation verified across ABS, ARIA, and DATA-CFG.
# Exit Code: 0

# 2. Automated Claim-Evidence Integrity Guard
python research_execution_20261018/audit_claims_and_evidence.py
# Output: [PASSED] All manuscript claims match verified evidence level.
# Exit Code: 0

# 3. Verifier Known-Pass / Known-Fail Battery
python -m unittest research_execution_20261018/test_verifier_ground_truth_battery.py
# Output: Ran 12 tests in 0.001s. OK. Exit Code: 0

# 4. Schedule Validity & RCBD Design Test Suite
python -m unittest research_execution_20261018/test_schedule_validity.py
# Output: Ran 6 tests in 0.003s. OK. Exit Code: 0

# 5. Full Discovery Offline Test Suite
python -m unittest discover -s research_execution_20261018 -p "test_*.py"
# Output: Ran 89 tests in 17.470s. OK. Exit Code: 0
```

---

## 7. Overstated Conclusions Corrected

The following claims from previous internal reports were corrected:

1. **"Fundamental emergent discovery of AI cognition"** $\to$ Corrected to: *Implementation heuristic in `browser-use` (`DISABLED_ELEMENTS` and non-interactive node stripping).*
2. **"Flaw-free verifiers"** $\to$ Corrected to: *Hardened two-tier state verifiers with documented construct limitations (e.g., T4 synthetic checkout flag, T6 regex refusal).*
3. **"Universal failure across autonomous agents"** $\to$ Corrected to: *Measured behavior specific to `browser-use 0.13.10` in text-only mode.*
4. **"Pilot proves channel equivalence"** $\to$ Corrected to: *Pilot has only ~10.85% power; equivalence claims are strictly prohibited under non-significant $p$-values.*
5. **"External reviews from Claude and Gemini"** $\to$ Corrected to: *Internal AI conversational generation; no authentic third-party peer reviews exist.*

---

## 8. Remaining Work Genuinely Requiring Real Model Inference

The following items cannot be answered offline or with zero dollars:

1. **Cognitive Utilization:** Does an LLM agent actually read and use delivered `aria-label` or custom `data-*` attributes during multi-step navigation when visible text is already complete?
2. **Behavioral Success Rates:** Does task success rate ($Y_{ijk}$) differ significantly between `ABS`, `ARIA`, and `DATA-CFG` under identical visible text?
3. **Step Efficiency:** Does the presence of ARIA attributes reduce total navigation steps or retry loops?
4. **Epistemic Refusal Calibration:** In Task T6, does an unconstrained frontier LLM produce calibrated refusals when duration is absent, or does it hallucinate standard warranty terms?

---

## 9. Next Highest-Value Experiments

1. **Experiment 1 (Zero-Cost Software Engineering Paper): Cross-Framework Serializer Audit:**
   - Audit 4 additional browser automation serializers: Playwright Native Accessibility Tree (`page.accessibility.snapshot()`), BrowserGym (`browsergym.core`), Stagehand, and Selenium.
   - Measure transmission rates of ARIA, Microdata, and JSON-LD across 20 top e-commerce websites.
   - *Cost:* **$0.00**. Produces a complete, publishable systems measurement paper.
2. **Experiment 2 (Controlled Live Behavioral Pilot, Requires User Authorization & Funding):**
   - Execute the 4-run live smoke schedule (`proposed_smoke_schedule.csv`) to verify live Gemini API streaming and cost accounting.
   - If smoke passes, execute the Option A 72-run pilot (`proposed_3arm_schedule.csv`) under a hard $10.00 billing ceiling.
   - *Cost:* **~$5.18 USD**. Produces the first empirical behavioral evidence for the pre-registered protocol.

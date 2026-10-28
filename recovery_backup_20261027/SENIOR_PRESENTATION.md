# SENIOR PRESENTATION SCRIPT & TECHNICAL TALK

**Project:** Autonomous Browser Agent Additive Semantic Markup Study (Option A)  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Presentation Audience:** Senior CSE Faculty / Research Supervisor  
**Demo Status:** 100% Offline Demonstrable · Zero Paid API Calls · Safety Gate Locked  

---

## 1. The 30-Second Elevator Pitch

> *"Good morning, Professor. My CSE research investigates whether adding semantic HTML markup—such as WAI-ARIA labels or configured custom `data-*` attributes—helps an autonomous text-based browser agent complete website tasks when the visible text on the page is already complete and identical. 
> 
> We engineered a 4-arm Randomized Complete Block Design across six tasks and four temporal blocks. During our engineering audit, we uncovered a critical discovery: modern browser agent serializers silently prune JSON-LD schemas and strip custom developer attributes, meaning web developers cannot assume metadata reaches the model. 
> 
> Today, all 51 offline regression tests pass with 100% hash integrity. I have a working, reproducible local demonstration and an interactive dashboard ready to show you the entire post-experiment analysis pipeline."*

---

## 2. The 2-Minute Research Overview

> *"To explain the core problem, Professor: existing web agent benchmarks evaluate models at the task level, conflating visual layout, website design, and DOM serialization. We set out to isolate the causal effect of HTML information channels under strict ceteris paribus conditions.
> 
> We created TechMart, a local e-commerce platform with four treatment conditions:
> 1. `BASELINE`: Plain visible HTML without semantic augmentations.
> 2. `BASELINE_REP`: An identical baseline replication to verify within-condition stability.
> 3. `ARIA`: Interactive buttons augmented with `aria-label` attributes.
> 4. `DATA-CFG`: Custom developer attributes like `data-action` and `data-product-id`, exposed via an extended whitelist.
> 
> We made three critical methodological decisions:
> First, we strictly enforce `use_vision=False`. If vision is enabled, the agent reads rendered pixel typography, which confounds text DOM evaluations.
> Second, we proved that standard `browser-use 0.13.10` prunes `<script type="application/ld+json">` elements unconditionally via `DISABLED_ELEMENTS`. Therefore, JSON-LD cannot be tested as an active text-agent channel without rewriting the library serializer.
> Third, we fixed historical verifier bugs—such as accepting six different SKUs on T3, awarding partial credit for incomplete checkouts on T4, and rewarding hallucinations on absent facts in T6.
> 
> All engineering is complete, the statistical pipeline is validated against published literature benchmarks, and the 96 confirmatory trials are scheduled and ready for live execution once authorized."*

---

## 3. The 5-Minute Demonstration Walkthrough

Follow this step-by-step sequence while presenting to your supervisor:

### Step 1: Open the Interactive Results Dashboard (1 Minute)
- **Action:** Open [`results/dashboard.html`](file:///C:/testing/research_execution_20261018/results/dashboard.html) in your browser.
- **Talking Point:**  
  *"Here is our dark-mode senior reporting dashboard. Notice the top banner: it transparently states that confirmatory live trials are pending and that all metrics shown reflect our synthetic pipeline benchmark. The KPI cards show the two-tier structure: 80 runs in the primary grounded benchmark (Tasks T1–T5) and 16 runs in the absent-fact refusal probe (Task T6)."*

### Step 2: Run the Master Demonstration Live (1 Minute)
- **Action:** Open PowerShell at `C:\testing` and run:
  ```powershell
  C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\run_offline_pipeline_demo.py
  ```
- **Talking Point:**  
  *"Notice the terminal output: In Step 1, it verifies SHA-256 hashes of all 12 protected baseline files—nothing in the original repository has been overwritten. In Step 2, it verifies the orthogonality of our 96-run schedule. In Step 3A, it launches headless Chromium via Playwright, executes real DOM actions across Tasks T1 through T6, and verifies client-side state transitions in under 8 seconds without making external API calls. In Step 3B, it captures the LLM prompt buffer, proving that ARIA and `data-*` reach the prompt while JSON-LD is pruned."*

### Step 3: Present the Statistical Rigor & Literature Validation (2 Minutes)
- **Action:** Highlight the Primary Contrasts table on `results/dashboard.html` and open [`STAGE_4_ANALYSIS_REPORT.md`](file:///C:/testing/research_execution_20261018/STAGE_4_ANALYSIS_REPORT.md).
- **Talking Point:**  
  *"Our analysis engine, `analyze_v3_results.py`, has zero external scientific dependencies. We implemented the task-stratified Cochran–Mantel–Haenszel (CMH) test and Newcombe hybrid score confidence intervals in pure Python standard library. We validated our formulas directly against published literature data—specifically Agresti's 2002 multicenter clinical trial benchmark and Newcombe's 1998 interval tables. Both match to four decimal places. Furthermore, we apply Bonferroni multiplicity adjustments ($\alpha = 0.0167$) across our three planned comparisons."*

### Step 4: Explain Power Limits & Present Next Steps (1 Minute)
- **Action:** Open [`POWER_RECONCILIATION.md`](file:///C:/testing/research_execution_20261018/final_review/POWER_RECONCILIATION.md).
- **Talking Point:**  
  *"We reconciled the reported power figures: with $N=20$/arm, we have 49.7% power for moderate effects ($\Delta = 0.35$), but $<11\%$ power for small effects ($\Delta \le 0.20$). Because of this, our protocol strictly forbids claiming that plain HTML and semantic HTML are 'equivalent' if the tests are non-significant. Today, our engineering validation is 100% complete with 51 passing tests. I am seeking your formal sign-off to pre-register the protocol on OSF and configure a paid API key to execute the 96 confirmatory trials."*

---

## 4. Architecture & Data Flow Summary

```
                      END-TO-END DEMO ARCHITECTURE
┌─────────────────────────────────┐
│     1. Schedule & Protocol      │  RCBD Design: 4 blocks x 24 runs = 96 trials
│   `proposed_randomized_sched`   │  4 Arms: BASELINE, BASELINE_REP, ARIA, DATA-CFG
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     2. Safe Execution Engine    │  Enforces use_vision = False
│     `protocol_v3_runner.py`     │  Extended attribute whitelist injection
│     SAFETY GATE LOCKED (L258)   │  Anti-survivorship bias failure logging
└────────────────┬────────────────┘
                 │
         ┌───────┴───────┐
         ▼               ▼
┌─────────────────┐  ┌─────────────────┐
│ Step 3A: DOM    │  │ Step 3B: Prompt │
│ Mechanics Check │  │ Delivery Check  │
│ Headless Chrome │  │ MockChatModel   │
│ Client State OK │  │ ARIA/Data-* OK  │
└────────┬────────┘  └────────┬────────┘
         │                    │
         └────────┬───────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│ 4. Statistical Analysis Engine  │  Task-Stratified CMH Test (chi2, p, OR)
│     `analyze_v3_results.py`     │  Newcombe Hybrid Score 95% CIs
│   (Ingests 96-run benchmark)    │  Agresti-Caffo Wald CIs & Bonferroni
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 5. Senior Review Deliverables   │  results/dashboard.html (Dark mode)
│   Interactive HTML Dashboard    │  results/summary_metrics.json
│   Comprehensive Reports & CSVs  │  STAGE_3 & STAGE_4 Reports
└─────────────────────────────────┘
```

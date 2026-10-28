# FINAL EXECUTION DECISION & ROADMAP TO COMPLETION

**Project:** Autonomous Browser Agent Observation Pipeline & Web Markup Evaluation  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Date:** October 24, 2026  
**Auditor:** Antigravity Research Execution Team  
**Status:** Strategic Roadmap — Zero Model Runs, Zero Billing, Zero File Modifications  

---

## 1. The Original Confirmatory Experiment & Frozen Infrastructure

### 1.1 Original Main Task Definition
The primary research formulation of Protocol v3 is a **controlled, single-variable evaluation of HTML information-delivery channels** on browser-agent retrieval and action execution under strictly text-only observation (`use_vision=False`).

- **Treatment Arms:**
  1. `ABS` (Negative Control): Target fact is absent from the DOM, attributes, and metadata.
  2. `VIS` (Visible Text): Target fact is rendered in standard visible HTML tags (`<p>`, `<span>`).
  3. `ARIA` (Accessibility Markup): Target fact is placed in valid WAI-ARIA attributes (`aria-label`) on interactive triggers.
  4. `DATA-CFG` (Configured Developer Attributes): Target fact is placed in custom `data-*` attributes with an extended runner attribute whitelist.
- **Task Bank (T1–T6):** Six e-commerce tasks evaluated on TechMart (local SPA at `http://127.0.0.1:8080`):
  - **T1:** Basic product retrieval & add-to-cart (Headphones `wh-001`).
  - **T2:** Specific product selection (Keyboard `mkp-001`).
  - **T3:** 2nd-highest audio product ranking (`wh-002`).
  - **T4:** Multi-step transactional checkout with form submission (`mse-001`).
  - **T5:** Cart item removal with pre-condition assertion.
  - **T6:** Negative probe querying non-existent warranty to test grounded refusal vs. hallucination.

### 1.2 Frozen Execution Infrastructure
- **Active Runner Entry Point:** [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) (`main()` calling `execute_experiment(...)`).
- **Frozen Experimental Schedules:**
  - **3-Arm Design ($N=72$):** [`proposed_3arm_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_3arm_schedule.csv) (4 temporal blocks $\times$ 3 arms $\times$ 6 tasks).
  - **4-Arm Design ($N=96$):** [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) (4 temporal blocks $\times$ 4 arms $\times$ 6 tasks).
  - **Target Outputs:** `results/3arm_runs/` (per-trial JSON traces) and `results/v3_3arm_summary.csv`.
- **Target Model Architecture:** Google Gemini (`gemini-3.1-flash-lite` or `gemini-2.0-flash`), text-only (`use_vision=False`), with 15-second inter-trial pacing.
- **Safety Gates & Interlocks in Runner:**
  1. **Mode Gating:** Default mode is `mock` (`--mock` default True); `--live` must be explicitly commanded.
  2. **Confirmation Gate (Lines 749–753):** Execution halts with `RuntimeError` unless `--confirm-live-execution` is explicitly passed.
  3. **Credential Gate (Lines 756–758):** Execution halts with `RuntimeError` if `$env:GOOGLE_API_KEY` is not present in the process environment.
  4. **Budget Interlock:** `LocalBudgetGuard` (`budget_controller.py`) enforces `cost_ceiling_usd` ($0.00 default) and halts if spending limits are exceeded.

---

## 2. Completed Work vs. Remaining Work for Confirmatory Trial

```
┌──────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────┐
│              COMPLETED & VERIFIED OFFLINE                │         REMAINING FOR LIVE CONFIRMATORY RUN (PATH B)     │
├──────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ ✅ Full 5-stage observation pipeline measurement         │ ❌ Formal academic supervisor sign-off on Protocol v3   │
│ ✅ AST proofs of JSON-LD & non-interactive tag stripping │ ❌ Paid Google Cloud API key with Tier-1 quota (>1k RPD) │
│ ✅ Chromium Blink AXTree node correspondence (27/34)     │ ❌ Credit card / billing authorization for API spend     │
│ ✅ Action-label co-location confound analysis & fix      │ ❌ OSF pre-registration of protocol SHA-256 hashes       │
│ ✅ Hardened state verifiers for T1–T6 (CDP asserted)     │ ❌ Execution of 72 or 96 live browser trials (3-5 hours) │
│ ✅ Verifier regression test battery (100% pass)          │ ❌ Real-time monitoring of live API rate limits & pacing │
│ ✅ Treatment leakage test suite (100% pass)              │ ❌ Ingestion of real live data into analyze_v3_results.py│
│ ✅ Statistical engine: CMH & Newcombe CIs (clinical-ref) │ ❌ Revision of paper tables with real empirical outcomes │
│ ✅ 10,000-trial Monte Carlo power analysis               │                                                          │
│ ✅ Local Qwen diagnostic traces 001–005 with telemetry   │                                                          │
└──────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────┘
```

---

## 3. Concrete Execution Paths

### Path A: Finalize the Systems/Measurement Research Manuscript (Zero Live Runs)
- **Objective:** Finalize and publish the paper as an empirical systems audit of the **DOM serialization gap**, using verified offline measurements as primary evidence and local smoke runs (001–005) as empirical case studies.
- **Core Narrative:**
  1. Autonomous agent frameworks rely on heuristic DOM serializers that silently prune 100% of Schema.org JSON-LD scripts and strip non-interactive ARIA attributes.
  2. Exposes the widespread fallacy that "DOM pruning is equivalent to an accessibility tree," proving a critical divergence between Blink's AXTree and `browser-use`.
  3. Uncovers the action-label co-location confound prevalent in benchmark task designs.
  4. Documents real-world watchdog timeout dynamics on local models where prompt accumulation triggers in-flight cancellation.
  5. Proves that small-sample agent experiments ($n=20$) possess $<11\%$ power, establishing a strict methodological warning against the Equivalence Fallacy.
- **Concrete Execution Steps:**
  1. Consolidate [`RESEARCH_PAPER_DRAFT_V2.md`](file:///C:/testing/research_execution_20261018/RESEARCH_PAPER_DRAFT_V2.md) by incorporating the 5-stage evidence matrix and node correspondence findings.
  2. Add Section 7 (Empirical Case Study on Latency Scaling & Cancellation Telemetry from runs 001–005).
  3. Update [`research_paper_final.tex`](file:///C:/testing/research_execution_20261018/research_paper_final.tex) to match the consolidated manuscript.
  4. Compile `research_paper.pdf` and verify all tables, formulas, and references render cleanly.
  5. Package the offline verification test harness into a reproducible artifact zip.

### Path B: Resume the Original Confirmatory Experiment
- **Objective:** Execute 72 live trials under Protocol v3 using Google Gemini to measure empirical task success across `ABS`, `ARIA`, and `DATA-CFG`.
- **Minimum Blockers That Must Be Resolved First:**
  1. **Blocker 1 (Financial / Quota):** Obtain and configure a paid Google Cloud API key (`GOOGLE_API_KEY`) with Tier-1 quota. Free-tier quota (500 RPD) is mathematically insufficient for a 72-run experiment (72 runs $\times$ ~5–10 steps = 360–720 requests), which will trigger a mid-run crash identical to Experiment 1b (run 105).
  2. **Blocker 2 (Budget Allocation):** Authorize spending buffer ($10.00–$25.00 USD) and update `cost_ceiling_usd` in the CLI call.
  3. **Blocker 3 (Pre-Registration):** Compute and deposit SHA-256 hashes of `protocol.md`, `task_specifications.json`, and `proposed_3arm_schedule.csv` onto the Open Science Framework (OSF).
  4. **Blocker 4 (Execution Orchestration):** Run `python protocol_v3_runner.py --live --confirm-live-execution --schedule proposed_3arm_schedule.csv --cost-ceiling 25.0 --free-tier=False`. Monitor the 15-second pacing delays over 3 to 5 hours.
  5. **Blocker 5 (Data Reconciliation):** Verify all 72 trials completed without 429/503 aborts, execute `analyze_v3_results.py` over `results/v3_3arm_summary.csv`, and rewrite paper findings with real effect sizes and p-values.

---

## 4. Effort Estimation & Uncertainty Analysis

| Path | Estimated Effort | Biggest Uncertainty | Likelihood of Re-Entering Debug Loop |
| :--- | :---: | :--- | :---: |
| **Path A: Systems/Measurement Manuscript** | **4 to 8 engineer-hours**<br>(1 to 2 focused writing sessions) | **Reviewer Venue Alignment:** Ensuring the paper is submitted to systems, measurement, or agent architecture venues (e.g., ACM WebConf, USENIX ATC, EMNLP System Demos/Findings) rather than general benchmark tracks expecting an agent leaderboard. | **Near Zero (0%)**<br>(All evidence is already generated, tested, and stored locally). |
| **Path B: Confirmatory Experiment** | **16 to 36 engineer-hours**<br>(3 to 7 calendar days) | **Risk of an Inconclusive Null Result ($	ext{Power} < 11\%$):** At $N=24$ runs/arm, if the true markup effect is moderate ($\Delta \le 0.20$), power is $<11\%$. There is an **$>89\%$ probability of obtaining a non-significant p-value ($p > 0.05$)**, which cannot prove markup equivalence under pre-registered rules. | **High (>60%)**<br>(Vulnerable to API rate-limits, provider network aborts, quota drops, and inconclusive null findings). |

---

## 5. Definitive Strategic Recommendation

### Adopt **Path A: Finalize the Systems/Measurement Research Manuscript**.

**Why Path A is the superior scientific decision:**
1. **Defensible Rigor vs. Underpowered Flukes:** Path A is built on deterministic, 100% reproducible systems measurements (Blink CDP inspection, AST source code proofs, and exact token reachability). Path B, by contrast, suffers from severe sample-size power deficits ($<11\%$ power) where an inconclusive null result is the most likely statistical outcome.
2. **Speed to Peer-Reviewed Submission:** Path A requires **zero new data collection**. All data, schemas, tests, and text drafts already exist in the repository. Path A can be fully completed, compiled, and ready for submission in 1–2 working sessions.
3. **Genuine Scientific Novelty:** Exposing the silent loss of Schema.org metadata, proving the non-interactive ARIA stripping bottleneck, and identifying the action-label co-location confound provides genuine, high-impact value to the web-agent engineering community. In contrast, running an underpowered 72-run benchmark on a single mock site using a closed-source cloud API adds little lasting scientific insight.

---

## 6. Actionable Next Steps (Stopping Here for Approval)

1. **User Sign-Off:** Review this roadmap and approve adopting **Path A**.
2. **Execution Phase (Upon Approval):**
   - Synthesize [`RESEARCH_PAPER_DRAFT_V2.md`](file:///C:/testing/research_execution_20261018/RESEARCH_PAPER_DRAFT_V2.md) into the authoritative paper manuscript.
   - Synchronize [`research_paper_final.tex`](file:///C:/testing/research_execution_20261018/research_paper_final.tex) and build the final submission PDF.
   - Package the offline reproducibility suite into an archival bundle.

**Execution stopped.** No experiments, model calls, network traffic, or code modifications will occur without your explicit command. Awaiting your review.

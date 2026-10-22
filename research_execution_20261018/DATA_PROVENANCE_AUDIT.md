# DATA PROVENANCE AUDIT

**Project:** Autonomous Browser Agent Additive Semantic Markup Study (Option A)  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Audit Date:** October 21, 2026  
**Operating Mode:** Strict Read-Only Audit · Zero Data Mutations · Zero Paid API Calls  

---

## 1. Executive Summary & Provenance Taxonomy

A rigorous forensic audit of all CSV, JSON, JSONL, and report files across `C:\testing` reveals that the workspace contains **three completely distinct classes of data** that must never be pooled, conflated, or cross-analyzed:

1. **Historical Real-API Pilot Trials ($N=261$ raw, $N=250$ cleaned):** Genuine API calls to Google Gemini executed on October 6–7, 2026. While physically real, this data is **scientifically compromised** due to library-level treatment pruning (`browser-use` stripped JSON-LD and custom `data-*`), selective retries of domain failures in Repetition 9, and loose verifier logic.
2. **Truncated Live Experiment ($N=147$ attempted):** Genuine API calls executed on October 11, 2026. This run crashed at run 105 due to free-tier API quota exhaustion (500 RPD limit), resulting in 42 consecutive HTTP 429 aborts. It was permanently discontinued.
3. **Synthetic Validation Benchmarks & Offline Demo Traces:** Deterministic mock datasets used exclusively to validate the post-experiment statistical pipeline ([`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py)), verify browser state transitions (6 micro-trials), and prove token delivery into prompt buffers (4 mock traces).
4. **Protocol v3 Confirmatory Experiment ($N=96$ planned):** The approved 4-arm Randomized Complete Block Design (RCBD). **ZERO CONFIRMATORY RUNS HAVE BEEN EXECUTED TO DATE.** The live safety gate remains strictly locked.

---

## 2. Dataset-by-Dataset Audit & Forensic Evidence

### Dataset 1: Historical Pilot — Cleaned (`pilot-summary-clean.csv`)
- **File Path:** [`C:/testing/results/pilot-summary-clean.csv`](file:///C:/testing/results/pilot-summary-clean.csv) (38,416 bytes; backup at [`C:/testing/results_EXP1_FROZEN_BACKUP/pilot-summary-clean.csv`](file:///C:/testing/results_EXP1_FROZEN_BACKUP/pilot-summary-clean.csv))
- **Data Provenance:** Real model invocations (`gemini-2.0-flash-exp` via `browser-use 0.13.10`).
- **Total Records:** 250 rows.
- **Reported Outcomes:** 249 successes (`success == True`), 1 failure (`success == False`, Rep 2 v2 T4).
- **Tasks & Variants:** 5 variants (`v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs`, `v4-evidence-meta`) $\times$ 5 tasks (T1–T5) $\times$ 10 repetitions.
- **Modality:** Multimodal (`use_vision=True`).
- **Scientific Audit Verdict: COMPROMISED / INELIGIBLE FOR CONFIRMATORY FINDINGS.**
  - *Reason 1 (Treatment Omission):* `browser-use 0.13.10` serializer prunes `<script>` and `<meta>` tags (`DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}`) and filters custom attributes via `DEFAULT_INCLUDE_ATTRIBUTES`. Consequently, JSON-LD schemas and custom `data-*` attributes never reached the LLM prompt. Variants v1, v3, and static v4 functioned identically to the v0 baseline.
  - *Reason 2 (Survivorship / Retry Bias):* Forensic inspection of raw logs revealed that 9 runs in Repetition 9 failed on October 6. While 7 were API quota failures (HTTP 429), **runs `d6c79dab` and `1e522d81` were legitimate task failures** on `v3-data-attrs` T4 (agent added item but failed checkout). These genuine failures were discarded and re-run on October 7 until success was achieved (`925aac22`), artificially inflating reported accuracy from ~96.8% to 99.6%.
  - *Reason 3 (Scoring Vulnerabilities):* Historical verifiers accepted 6 SKUs for T3, awarded unconditional 0.25 credit for incomplete checkouts in T4, and accepted unseeded empty carts in T5.

### Dataset 2: Historical Pilot — Raw (`pilot-summary.csv`)
- **File Path:** [`C:/testing/results/pilot-summary.csv`](file:///C:/testing/results/pilot-summary.csv) (33,855 bytes)
- **Data Provenance:** Unfiltered raw execution log of Experiment 1 (Oct 6–7, 2026).
- **Total Records:** 261 rows.
- **Outcomes:** 251 successes, 10 failures.
- **Discrepancy Resolution:** Exactly 11 runs were excluded from this raw file to manufacture the 250-row `pilot-summary-clean.csv`:
  - 6 quota cascade failures in Rep 9 (HTTP 429, durations 9.0s–11.6s, steps=7).
  - 2 genuine domain task failures in Rep 9 v3 T4 (runs `d6c79dab` and `1e522d81`).
  - 2 intermediate retry failures in v3 T5 (runs `f7bfdef8` and `100f72c4`).
  - 1 timeout run from preliminary validation.

### Dataset 3: Main Experiment — Aborted Live Run (`main_experiment/full-summary.csv`)
- **File Path:** [`C:/testing/results/main_experiment/full-summary.csv`](file:///C:/testing/results/main_experiment/full-summary.csv) (19,249 bytes; backup at [`C:/testing/results_main_experiment_backup_20261011/full-summary.csv`](file:///C:/testing/results_main_experiment_backup_20261011/full-summary.csv))
- **Execution Date:** October 11, 2026.
- **Model:** `gemini-flash-lite-latest` with `use_vision=True` and runtime in-memory serializer patching.
- **Total Records:** 147 rows out of planned 250.
- **Outcomes:** 105 successes (runs 1–105), 42 consecutive failures (runs 106–147).
- **Failure Cause:** Run 106 hit the free-tier API quota ceiling of 500 requests per day (RPD) and 15 requests per minute (RPM). Every subsequent trial failed within 7–10 seconds with `RESOURCE_EXHAUSTED` / HTTP 429.
- **Scientific Audit Verdict: TRUNCATED / ABORTED.** Cannot be used for inferential analysis.

### Dataset 4: Protocol v3 Confirmatory Schedule (`proposed_randomized_schedule.csv`)
- **File Path:** [`C:/testing/research_execution_20261018/proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) (3,524 bytes)
- **Data Provenance:** Frozen specification file; deterministic seed `seed=42`.
- **Design:** 4 arms (`BASELINE`, `BASELINE_REP`, `ARIA`, `DATA-CFG`) $\times$ 6 tasks (T1–T6) $\times$ 4 blocks = 96 rows.
- **Current Execution Status:** **0 completed runs, 0 failed runs, 96 pending runs.** The confirmatory experiment has NOT been run.

### Dataset 5: Complete Synthetic Benchmark (`dataset_1_valid_complete.csv`)
- **File Path:** [`C:/testing/research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv) (8,139 bytes)
- **Data Provenance:** 100% Synthetic / Mock benchmark.
- **Total Records:** 96 rows matching the exact RCBD schedule structure.
- **Outcomes:** 73 successes, 23 failures.
- **Purpose:** Used strictly to validate the mathematical and pipeline execution of [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py) without paid API calls.

### Dataset 6: Offline Browser Mechanics Runs (`demo_browser_mechanics_and_verifier_runs.csv`)
- **File Path:** [`C:/testing/research_execution_20261018/results/demo_browser_mechanics_and_verifier_runs.csv`](file:///C:/testing/research_execution_20261018/results/demo_browser_mechanics_and_verifier_runs.csv) (2,152 bytes)
- **Data Provenance:** Direct headless Chromium DOM manipulation via Playwright.
- **Total Records:** 6 rows (Tasks T1–T6).
- **Outcomes:** 6 passes. Validates TechMart SPA state transitions (`window.__cart__`, `window.__orderConfirmed__`) and verifier logic. Does NOT measure autonomous agent intelligence.

### Dataset 7: Offline Agent Prompt Capture Runs (`demo_agent_prompt_delivery_runs.csv`)
- **File Path:** [`C:/testing/research_execution_20261018/results/demo_agent_prompt_delivery_runs.csv`](file:///C:/testing/research_execution_20261018/results/demo_agent_prompt_delivery_runs.csv) (1,154 bytes)
- **Data Provenance:** Single-step mock LLM execution via `MockChatModel` + `browser-use.Agent(use_vision=False)`.
- **Total Records:** 4 rows (BASELINE, ARIA, DATA-CFG, JSON-LD).
- **Outcomes:** 4 passes. Proves empirically that ARIA button labels and custom `data-*` attributes reach the prompt buffer, while JSON-LD is pruned by the serializer.

---

## 3. Data Integrity & Contamination Safeguards

1. **Dashboard Feed Isolation:**  
   The interactive dashboard ([`results/dashboard.html`](file:///C:/testing/research_execution_20261018/results/dashboard.html)) and the statistical report ([`results/analysis_report.md`](file:///C:/testing/research_execution_20261018/results/analysis_report.md)) are fed **exclusively** by `dataset_1_valid_complete.csv` (synthetic benchmark) and the two offline demo CSVs.
2. **Zero Contamination from Historical Experiments:**  
   Neither `pilot-summary-clean.csv` nor `main_experiment/full-summary.csv` is imported, read, or merged into the Protocol v3 results pipeline.
3. **Mandatory Provenance Watermarking:**  
   All tables, charts, and KPI cards in `dashboard.html` visibly state that confirmatory experimental trials are **PENDING** and that the displayed numbers are synthetic engineering validation metrics.

# Experiment Reconciliation & Forensic Data Provenance Report

**Date:** 2026-10-25  
**Auditor:** Independent Systems & Methodology Auditor  
**Project:** *The DOM Serialization Gap in Autonomous Browser Agents*  
**Workspace:** `C:\testing\research_execution_20261018`  
**Compliance:** 100% Offline Forensic Verification · Zero Live API Invocations · No Data Overwriting  

---

## Executive Summary

This document establishes the forensic reconciliation of all empirical experiment records in the repository. Every run record, summary CSV row, raw JSON trace, and attempt is mapped to its underlying operational cause. 

### Summary of Reconciled Execution Datasets

| Dataset | Model & Backend | Total Records | Completed Trials | Infrastructure Aborts | Outcome Profile | Evidentiary Role |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Phase 1 Cloud Pilot** | `gemini-3.1-flash-lite` (Google AI Studio) | 46 raw entries / 44 clean rows | **41 unique trials** (Runs 1–41) | 3 aborts (Run 26 attempts 1–3) | **41 / 41 scored 1.0 (100%)** across ABS, ARIA, DATA-CFG | **Exploratory Cloud Pilot** (Exhibits Ceiling Effect; unpooled baseline) |
| **Local Diagnostic Pilot** | `qwen3:4b` (Ollama air-gapped `127.0.0.1:11434`) | 5 runs | **2 cart passes, 3 timeouts/aborts** | 0 cloud aborts (3 step watchdog timeouts) | Step 1 ~103s; Step 2 >180s watchdog breach | **Local Hardware Case Study** (Context latency & watchdog truncation) |
| **Confirmatory Phase 2** | Option A 3-Arm Schedule (Runs 42–72) | 0 live | 0 | 0 | Unexecuted | **Pre-Registered Blueprint** (Strict Hold at 604/600 ceiling) |
| **Software Benchmarks** | Synthetic generator (`generate_synthetic_benchmark_data.py`) | 8 datasets | N/A (Simulated) | N/A | Variable (0.60–0.85) | **Offline Pipeline Validation** (Strictly separated from live data) |

---

## 1. Phase 1 Cloud Pilot Audit: 41 Completed Runs

### 1.1 Ingestion & File Mapping
- **Schedule File:** `proposed_3arm_schedule.csv` (72 planned trials: 3 arms $\times$ 6 tasks $\times$ 4 randomized blocks).
- **Raw Execution Log:** `results/v3_3arm_summary_raw.csv` (46 rows).
- **Analysis Summary:** `results/v3_3arm_summary.csv` (44 rows).
- **Per-Run Traces:** Exactly 46 JSON files in `results/3arm_runs/` matching each raw entry.

### 1.2 Reconciliation of Attempts, Retries, and Duplicates

The raw CSV contains 46 entries corresponding to schedule indices 1 through 41:
1. **Run 26 (Task T2, Arm ARIA, Block 2):**  
   - Attempt 1 (`run_026.json`): `status="infrastructure_aborted"`, `503 UNAVAILABLE` from Google API.
   - Attempt 2 (`run_026_attempt_2.json`): `status="infrastructure_aborted"`, `503 UNAVAILABLE`.
   - Attempt 3 (`run_026_attempt_3.json`): `status="infrastructure_aborted"`, `503 UNAVAILABLE`.
   - Attempt 4 (`run_026_attempt_4.json`): `status="completed"`, `score=1.0`.  
   *Reconciliation:* `results/v3_3arm_summary.csv` preserves all three failed infrastructure attempts alongside the successful attempt, maintaining complete audit transparency.
2. **Run 34 (Task T4, Arm ARIA, Block 2):**  
   - Two entries in raw CSV (`run_034.json` and `run_034_attempt_2.json`), both `status="completed"`, `score=1.0`.
   - Deduplicated in `v3_3arm_summary.csv` to 1 canonical record.
3. **Run 38 (Task T2, Arm DATA-CFG, Block 3):**  
   - Two entries in raw CSV (`run_038.json` and `run_038_attempt_2.json`), both `status="completed"`, `score=1.0`.
   - Deduplicated in `v3_3arm_summary.csv` to 1 canonical record.

### 1.3 Breakdown of Completed Trials by Arm and Task

Across the 41 unique completed trials, every trial scored 1.0 (verified via programmatic DOM inspection of `window.__cart__`, `window.__orderConfirmed__`, and T6 refusal regex):

| Task ID | Task Description | ABS (Control) | ARIA (Semantic) | DATA-CFG (Custom) | Total Completed | Success Rate |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **T1** | Search & lowest price | 2 | 3 | 2 | **7** | 7 / 7 (100%) |
| **T2** | Keyboard exact SKU | 2 | 2 | 2 | **6** | 6 / 6 (100%) |
| **T3** | 2nd-highest rated audio | 3 | 2 | 3 | **8** | 8 / 8 (100%) |
| **T4** | Transactional checkout | 2 | 2 | 3 | **7** | 7 / 7 (100%) |
| **T5** | Cart item removal | 2 | 2 | 2 | **6** | 6 / 6 (100%) |
| **T6** | Unstated warranty refusal | 2 | 2 | 3 | **7** | 7 / 7 (100%) |
| **Total** | **All Tasks** | **13 / 13** | **13 / 13** | **15 / 15** | **41 / 41** | **41 / 41 (100%)** |

### 1.4 Methodological Interpretation: The Ceiling Effect
- **Genuine Live Execution:** Every trace in `results/3arm_runs/` contains live model thought processes, multi-turn tool invocations (`click`, `input_text`, `navigate`), timestamps, and raw CDP DOM outputs.
- **Why Did All Arms Score 1.0?**
  1. The task descriptions named the product or category clearly.
  2. The synthetic web fixture layout was clean and uncluttered.
  3. `gemini-3.1-flash-lite` possessed sufficient reasoning capability to resolve the tasks using plain visible typography alone.
- **Scientific Implication:** When the control arm (\textsc{ABS}) achieves 100% success ($13/13$), there is zero headroom for semantic markup (\textsc{ARIA} or \textsc{DATA-CFG}) to demonstrate an additive benefit. Risk differences are identically 0.0.
- **Scientific Prohibition:** This outcome **CANNOT** be interpreted as evidence that semantic markup is useless or that the representations are equivalent. It establishes only that the task battery under this model suffered from an acute **Ceiling Effect**.

---

## 2. Local Diagnostic Pilot Audit: 5 `qwen3:4b` Runs

### 2.1 Environment and Rigor
- **Runner:** `local_qwen_smoke_runner.py`.
- **Air-Gap Invariant:** Purged all remote API keys from process memory (`os.environ.pop("GOOGLE_API_KEY")`, etc.).
- **Ollama Backend:** Strictly bound to `http://127.0.0.1:11434`.
- **Hardware:** Intel Core i7 / 16 GB RAM / NVIDIA RTX 3050 Laptop GPU (4 GB VRAM).
- **Offloading:** 34% of layers offloaded to CPU, 66% to GPU.

### 2.2 Trace-by-Trace Diagnostic Audit

| Run ID | Arm | Task | Steps | Duration | Status | Verifier Score | Mechanism & Telemetry Provenance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `qwen3_smoke_001` | DATA-CFG | T2 | 0 | 3.34s | `failed` | 0.0 | Pydantic validation failure on agent initialization (`max_history_items <= 5`). |
| `qwen3_smoke_002` | DATA-CFG | T2 | 2 | 1,013.09s | `timeout_partial` | **1.0** | Step 1 navigated. Step 2 clicked target button (verified in cart: `mkp-001`). Step 3 waited until underlying HTTP client timeout (no outer watchdog). |
| `qwen3_smoke_003` | DATA-CFG | T2 | 2 | 288.61s | `timed_out` | **1.0** | Step 1 (prompt ~1,500 tokens) took 102.9s. Step 2 (context expanded to >3,200 tokens) breached 180s step watchdog. Post-hoc CDP verifier confirmed item in cart prior to timeout. |
| `qwen3_smoke_004` | ABS | T2 | 1 | 185.50s | `timed_out` | 0.0 | Step 1 prompt ingestion hit 180s watchdog. Unhandled `asyncio.CancelledError` caused empty telemetry list (`[]`). |
| `qwen3_smoke_005` | ABS | T2 | 1 | 188.56s | `timed_out` | 0.0 | Step 1 hit 180s watchdog. Fixed wrapper caught `asyncio.CancelledError`, capturing 1 in-flight call (179.7s wall-clock, status `cancelled_in_flight`). |

### 2.3 Non-Equivalence of Cloud vs. Local Comparisons
We explicitly forbid treating the cloud pilot (100% pass) and local pilot (3 timeouts / 2 partial passes) as a controlled experimental comparison between models. The differences reflect:
1. Model size and architecture (`gemini-3.1-flash-lite` cloud API vs. 4-bit quantized `qwen3:4b`).
2. Inference infrastructure (Google TPU cluster vs. 4 GB hybrid consumer laptop GPU).
3. Timeout configuration (unbounded provider latency vs. fixed 180-second step watchdog).
4. Prompt processing rate (>500 tokens/sec cloud vs. 15–20 tokens/sec hybrid local).

---

## 3. Confirmatory Phase 2 Status: Strict Hold

- **Planned Protocol:** 72-trial 3-arm RCBD (Option A) or 96-trial 4-arm RCBD (Option B).
- **Current Status:** **STRICT HOLD**.
- **Reason:** Daily quota ledger at `results/daily_quota_ledger.json` records 604 cumulative requests against a 600 ceiling. `LocalBudgetGuard` evaluates $604 \ge 600$ and fails closed.
- **Rule:** No live dispatches are permitted without explicit human supervisor authorization and a documented ledger reset.

---

## 4. Synthetic Benchmark Datasets

To validate the statistical pipeline (`analyze_v3_results.py`) across diverse edge cases (zero cells, Simpson's Paradox, severe baseline drift, Bonferroni adjustments), 8 synthetic datasets were generated:
- Stored in: `test_scratch_synthetic_data/`
- Verified: All 11 unit tests in `test_analyze_v3_results.py` pass cleanly.
- Strict Invariant: Synthetic outputs are presented exclusively in paper Appendix A to demonstrate software correctness. They are never merged or pooled with live trial data.

---
*Report certified by Independent Systems & Methodology Auditor.*

# Final Reproducibility Guide

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11)  
**Deliverable:** `FINAL_REPRODUCIBILITY_GUIDE.md`  

---

## 1. System Requirements & Environment Setup

### Hardware & Operating System
- **Operating System:** Windows 10 / 11 (tested on Windows 64-bit).
- **Python Version:** Python 3.11 (`.venv311`).
- **Browser Automation:** Chromium managed via Playwright / Chrome DevTools Protocol (`browser-use 0.13.10`).

### Workspace Layout
```text
C:\testing\research_execution_20261018\
├── proposed_3arm_schedule.csv       # Authoritative 72-trial experimental schedule
├── protocol_v3_runner.py            # Execution harness with CDP verifiers and guards
├── budget_controller.py             # Client-side spend limits and request offsets
├── FINAL_DATA_RECONCILIATION.csv    # Reconciled trial accounting across 72 trials
├── FINAL_ARM_TASK_RESULTS.csv       # Tabulated statistics by arm, task, and block
├── FINAL_STATISTICAL_ANALYSIS.py    # Offline statistical analysis script
├── FINAL_STATISTICAL_REPORT.md      # Markdown statistical report
├── research_paper_final.tex         # Complete audited LaTeX manuscript
├── references.bib                   # Bibliography (14 real peer-reviewed citations)
└── results\
    ├── v3_3arm_summary.csv          # Execution summary CSV (30 rows)
    ├── daily_quota_ledger.json      # Client-side request and cost tracking
    └── 3arm_runs\                   # Per-run detailed JSON traces (run_001 to run_027)
```

---

## 2. Re-Executing Offline Statistical Analysis & Regression Tests

All statistical analyses and test suites can be executed completely offline without network connectivity or API tokens:

### 1. Execute Statistical Analysis
```powershell
C:\testing\.venv311\Scripts\python.exe FINAL_STATISTICAL_ANALYSIS.py
```
- **Output:** Reads `results/v3_3arm_summary.csv`, calculates Wilson score confidence intervals, computes one-way ANOVA F-statistics, and writes `FINAL_ARM_TASK_RESULTS.csv` and `FINAL_STATISTICAL_REPORT.md`.
- **Runtime:** $<0.1$ seconds.

### 2. Execute Offline Regression Suite
```powershell
C:\testing\.venv311\Scripts\python.exe AUDIT_04_OFFLINE_REGRESSION_TESTS.py
```
- **Output:** Validates completion index exclusions, non-overwriting attempt numbering, budget guard ceiling enforcement, and T6 refusal regex scoring.
- **Runtime:** $<0.03$ seconds (5/5 tests passing).

---

## 3. Data Dictionary for Experimental Records

### Fields in `results/v3_3arm_summary.csv`:
- `run_index`: Integer schedule position (1–72).
- `block_id`: Temporal replicate block (1–4).
- `within_block_order`: Permutation order within block (1–18).
- `arm`: Experimental treatment (`ABS`, `ARIA`, `DATA-CFG`).
- `task_id`: Task identifier (`T1`–`T6`).
- `variant_mapping`: Target HTML variant (`v0-baseline`, `v2-aria`, `v3-data-attrs`).
- `target_entity`: Product SKU evaluated (`wh-001`, `mkp-001`, `wh-002`, `mse-001`).
- `model`: Target LLM (`gemini-3.1-flash-lite`).
- `success`: Boolean behavioral task outcome.
- `score`: Numeric verifier score ($1.0$ for success, $0.0$ for failure/abort).
- `total_steps`: Number of LLM planning steps executed.
- `total_time_seconds`: Wall-clock execution duration in seconds.
- `status`: Execution state (`completed`, `infrastructure_aborted`).
- `termination_reason`: Mechanism of trial conclusion (`agent_completed`, `infrastructure_aborted`).
- `error_message`: Error payload (e.g. `503 UNAVAILABLE` during upstream outages).
- `treatment_delivery_evidence`: Verification that intended markup was present in the serialized model prompt string.

---

## 4. Controlled Resumption Procedure

If authorized to resume live trials after zero-cost access has been independently confirmed:
1. Verify no active Python runner processes:
   ```powershell
   Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*protocol_v3_runner.py*" }
   ```
2. Run single-trial verification (Run 28):
   ```powershell
   C:\testing\.venv311\Scripts\python.exe protocol_v3_runner.py --live --confirm-live-execution --max-runs 1 --max-requests 500
   ```
3. Verify output in `results/v3_3arm_summary.csv` and `results/3arm_runs/run_028.json`.

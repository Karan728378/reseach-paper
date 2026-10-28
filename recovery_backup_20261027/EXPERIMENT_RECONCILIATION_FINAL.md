# EXPERIMENT RECONCILIATION REPORT (FINAL)

**Project Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Workspace:** `C:\testing\research_execution_20261018`  
**Date:** October 26, 2026  
**Auditor:** Senior Research Systems Engineer & Statistical Auditor  
**Scope:** Final reconciliation of all experiment phases, schedule arms, pilot outcomes, and power boundaries.

---

## 1. Multi-Phase Experiment Classification

To eliminate historical confusion across drafts, the project's empirical and experimental artifacts are formally partitioned into five distinct, non-overlapping categories:

| Category | Identifier | Description | Execution Status | Data Artifacts | Inference Scope |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Cat 1** | **Exploratory Cloud Pilot** | 3-arm RCBD pilot across Tasks T1–T5 using `gemini-flash-lite-latest` via Google AI Studio. | **COMPLETED (PARTIAL)** (Runs 1–41 completed; Runs 42–72 halted by budget ceiling) | `results/3arm_runs/*.json` (46 files), `v3_3arm_summary_reconciled_v2.csv` | Demonstrates harness operational stability and an acute 100% ceiling effect (zero variance). Provides no evidence of treatment efficacy or equivalence. |
| **Cat 2** | **Exploratory Local Diagnostics** | 5 diagnostic runs on local hardware using Ollama `qwen2.5:7b-instruct-q4_K_M` on CPU. | **COMPLETED (5 RUNS)** | `results/local_pilot_raw_logs.json`, `LOCAL_QWEN_CANCELLATION_TELEMETRY_FIX.md` | Purely harness debugging (watchdog timeouts, Pydantic exceptions, cancellation telemetry). Excluded from scientific analysis. |
| **Cat 3** | **Offline Systems & AST Audit** | Deterministic source AST parsing and CDP accessibility tree extraction. | **COMPLETED** | `serialization_audit_metrics.json`, `accessibility_tree_comparison.json`, `MULTI_FRAMEWORK_OBSERVATION_TAXONOMY.md` | Authoritative systems evidence: proves `DISABLED_ELEMENTS`, line 1046 tag stripping, attribute whitelists, and 27/34 correspondence. |
| **Cat 4** | **Synthetic Software Benchmark** | Mock synthetic dataset (`test_scratch_synthetic_data/dataset_1_valid_complete.csv`) used to test statistical code math. | **COMPLETED (SYNTHETIC)** | `test_scratch_synthetic_data/`, Appendix A Tables 3 & 4 | Software verification only; explicitly disclaimed as non-behavioral data. |
| **Cat 5** | **Confirmatory Behavioral Experiment** | Proposed 4-arm confirmatory study ($N \ge 388$ to $1,440$ runs) or Disambiguation Probes A & B. | **UNEXECUTED (0 RUNS)** | `proposed_randomized_schedule.csv`, `DISAMBIGUATION_PROBES_PROTOCOL.md` | Proposed future research; awaiting formal authorization and dedicated budget allocation. |

---

## 2. Definitive Reconciliation Table

| Metric / Question | Value / Answer | Source of Truth |
| :--- | :--- | :--- |
| How many distinct scheduled units were attempted? | **41** (Runs 1 to 41) | `CANONICAL_RUN_LEDGER.csv` |
| How many physical trace files exist? | **46** files | `results/3arm_runs/` directory listing |
| How many runs are primary eligible? | **39** (13 ABS, 13 ARIA, 13 DATA-CFG) | `results/v3_3arm_reconciliation_audit.json` |
| How many runs were quarantined? | **2** (Runs 34 and 38, DATA-CFG duplicates) | `results/v3_3arm_reconciliation_audit.json` |
| How many aborts occurred? | **3** (Run 26 attempts 1, 2, 3; transient 503s) | `results/3arm_runs/run_026*.json` |
| How many scheduled units were halted by budget? | **31** (Runs 42 to 72) | `proposed_3arm_schedule.csv` |
| What was the pilot task success rate? | **100.0%** (39/39 primary; 41/41 sensitivity) | Reconciled summaries |
| What was the observed treatment risk difference? | $\hat{\theta} = \mathbf{0.0000}$ (Newcombe 95% CI: $[-0.228, +0.228]$) | Statistical re-analysis |
| What statistical power did the pilot possess? | $\mathbf{11.5\%}$ for $\Delta = 0.20$ ($\alpha = 0.0167$, CMH test) | `reproduce_power_audit.py` (10,000 iterations) |
| Did the pilot prove treatment equivalence? | **NO.** Zero variance + small sample = underpowered ceiling effect. | Section VI-C & VII-B |

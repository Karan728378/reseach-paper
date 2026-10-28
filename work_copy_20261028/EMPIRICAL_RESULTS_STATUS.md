# EMPIRICAL RESEARCH RESULTS STATUS REPORT

**Project:** Autonomous Browser Agent Additive Semantic Markup Study (Option A)  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Audit Date:** October 21, 2026  
**Status:** **CONFIRMATORY LIVE EXPERIMENT PENDING — SAFETY GATE LOCKED**  

---

## 1. Primary Empirical Research Outcome

# 🛑 EMPIRICAL CONFIRMATORY RESULTS: NOT YET AVAILABLE

**Status Explanation:**  
In accordance with mandatory research safety and budget constraints, **zero live model trials have been executed under Protocol v3**. 

- The code-level safety gate at line 258 of [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) remains active (`SAFETY_GATE_LOCKED = True`).
- No external model API calls have been dispatched.
- No paid cloud quota has been consumed.
- All 96 trials in [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) remain unexecuted.

Consequently, **no empirical success rates, effect sizes, p-values, or confidence intervals currently exist for the confirmatory study**. Any numerical findings displayed on dashboards or generated in test folders represent deterministic synthetic benchmarks used exclusively to validate software pipeline correctness.

---

## 2. Ineligibility of Historical Data for Confirmatory Findings

As established in [`DATA_PROVENANCE_AUDIT.md`](file:///C:/testing/research_execution_20261018/DATA_PROVENANCE_AUDIT.md) and [`EXPERIMENT_RECONCILIATION.md`](file:///C:/testing/research_execution_20261018/EXPERIMENT_RECONCILIATION.md), neither historical dataset can be substituted as confirmatory empirical evidence:

1. **Historical Pilot Dataset (`pilot-summary-clean.csv`, $N=250$):**  
   - Operated under multimodal vision (`use_vision=True`), bypassing text DOM differences.
   - Evaluated under a library version (`browser-use 0.13.10`) that pruned JSON-LD scripts and custom `data-*` attributes from the prompt buffer, meaning the experimental treatments were absent.
   - Excluded legitimate task failures in Repetition 9 and retried until success, introducing survivorship bias.
   - Used flawed verifiers that awarded passes to incorrect items.
2. **Aborted Main Experiment (`main_experiment/full-summary.csv`, $N=147$):**  
   - Crashed at run 105 due to free-tier quota exhaustion (500 RPD limit), resulting in 42 consecutive HTTP 429 aborts.
   - The run plan was truncated and permanently discontinued.

---

## 3. Pipeline Validation Benchmark (Synthetic Demonstration Only)

To demonstrate that the post-experiment analysis pipeline is fully implemented, mathematically correct, and senior-review-ready, the analysis engine ([`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py)) was executed over the canonical 96-run synthetic benchmark dataset ([`test_scratch_synthetic_data/dataset_1_valid_complete.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv)).

> [!WARNING]
> **SYNTHETIC DATA DISCLAIMER:**  
> The metrics below are generated from **mock/synthetic benchmark data** to validate post-experiment code execution. They **DO NOT** represent real agent task performance.

### 3.1 Primary Inferential Contrasts (Synthetic Benchmark, Tasks T1–T5)
- **Multiplicity Threshold:** Bonferroni $\alpha = 0.05 / 3 = 0.0167$.
- **ARIA vs BASELINE:** Risk Difference = $+0.0750$ (95% CI: $[-0.1782, +0.2801]$), CMH $\chi^2 = 0.088$, unadjusted $p = 0.7662$, adjusted $p = 1.0000$.
- **DATA-CFG vs BASELINE:** Risk Difference = $+0.2250$ (95% CI: $[-0.0113, +0.4024]$), CMH $\chi^2 = 2.399$, unadjusted $p = 0.1215$, adjusted $p = 0.3644$.
- **ARIA vs DATA-CFG:** Risk Difference = $-0.1500$ (95% CI: $[-0.3751, +0.0906]$), CMH $\chi^2 = 0.683$, unadjusted $p = 0.4086$, adjusted $p = 1.0000$.

### 3.2 Baseline Stability Check (Synthetic Benchmark)
- BASELINE (ABS) success: 13 / 20 (65.0%).
- BASELINE_REP (VIS) success: 12 / 20 (60.0%).
- Fisher's Exact Stability Test: Two-sided $p = 1.0000$ (satisfies stability criterion $p \ge 0.10$).

---

## 4. Prerequisites for Launching Real Confirmatory Trials

The transition from "Pending" to "Active" empirical research requires four human administrative actions:

1. **Academic Supervisor Sign-Off:** Formal written approval of Protocol v3 design and the 6-task bank.
2. **Paid API Key Allocation:** Configuration of a paid Google Gemini API key ($env:GOOGLE_API_KEY) with Tier-1 quota to support ~800 API requests without hitting the 500 RPD free-tier wall.
3. **OSF Pre-Registration:** Registering the frozen SHA-256 hashes of `protocol.md`, `task_specifications.json`, and `proposed_randomized_schedule.csv` on the Open Science Framework.
4. **Safety Gate Release:** Explicit manual modification of line 258 of `protocol_v3_runner.py` setting `SAFETY_GATE_LOCKED = False`.

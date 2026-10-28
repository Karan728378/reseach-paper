# Protocol v3 Statistical Analysis Report

> [!WARNING]
> **SYNTHETIC TEST DATASET NOTICE:**
> This report was generated from a synthetic dataset for software verification and pipeline testing only.
> These figures DO NOT represent real-world agent performance or empirical findings.


- **Analysis Date & Pipeline:** `analyze_v3_results.py (Option A Additive Markup Evaluation)` (v1.0.0)
- **Dataset Completeness:** 96/96 runs completed (0 infrastructure errors, 0 missing runs)
- **Significance Threshold:** Nominal $\alpha = 0.05$, Bonferroni-Adjusted $\alpha_{\text{adj}} = 0.0167$ (for 3 contrasts)

---

## 1. Dataset Integrity & Baseline Stability Check

### 1.1 Run Ingestion & Error Segregation
- **Total Rows Ingested:** 96
- **Valid Completed Trials:** 96
- **Infrastructure Aborts (Excluded from Confirmatory Testing):** 0
- **Missing Run Indices:** `None (100% Complete)`

### 1.2 Baseline Stability Test (ABS vs VIS Replicate Check across T1–T5)
- **ABS (Baseline Split 1):** 11/20 (55.0%)
- **VIS (Baseline Split 2):** 16/20 (80.0%)
- **Fisher's Exact Stability Test:** $p = 0.1760$ (Threshold $\alpha = 0.1$)
- **Decision:** **POOLED** (Poolability confirmed; composite Baseline $N=40$ utilized for confirmatory testing.)

---

## 2. Primary Grounded Action Benchmark (Tasks T1–T5, $N=80$)

### 2.1 Marginal Success Rates and Operational Performance

| Arm | Total Runs | Successes | Success Rate (%) | 95% Wilson CI | Mean Steps (Y=1) | Mean Time (s) |
|---|---|---|---|---|---|---|
| **ABS** | 20 | 11 | 55.0% | [34.2%, 74.2%] | 4.0 | 25.5s |
| **VIS** | 20 | 16 | 80.0% | [58.4%, 91.9%] | 4.0 | 25.5s |
| **BASELINE** | 40 | 27 | 67.5% | [52.0%, 79.9%] | 4.0 | 25.5s |
| **ARIA** | 20 | 15 | 75.0% | [53.1%, 88.8%] | 4.0 | 25.5s |
| **DATA-CFG** | 20 | 18 | 90.0% | [69.9%, 97.2%] | 4.0 | 25.5s |

### 2.2 Confirmatory Inferential Contrasts (Task-Stratified CMH & Risk Differences)

| Contrast | Description | $\widehat{RD}$ | 95% Newcombe CI | 95% Agresti-Caffo CI | Fisher $p$ (Bonf) | CMH $\chi^2$ | CMH $p$ (Bonf) | Significant? |
|---|---|---|---|---|---|---|---|---|
| `ARIA_vs_BASELINE` | ARIA Augmentation Benefit | **+0.075** | [-0.176, +0.282] | [-0.174, +0.295] | 0.7659 (1.0000) | 0.09 | **0.7662** (1.0000) | NO (Inconclusive) |
| `DATA_CFG_vs_BASELINE` | Configured Data Attribute Benefit | **+0.225** | [-0.011, +0.396] | [-0.005, +0.399] | 0.0672 (0.2015) | 2.40 | **0.1215** (0.3644) | NO (Inconclusive) |
| `ARIA_vs_DATA_CFG` | Semantic Architecture Comparison | **-0.150** | [-0.380, +0.094] | [-0.371, +0.099] | 0.4075 (1.0000) | 0.68 | **0.4086** (1.0000) | NO (Inconclusive) |

### 2.3 Separate-Arm Sensitivity & Stability Contrasts (Unpooled Against ABS and VIS)

To guarantee transparent reporting without outcome-dependent model switching, treatments are also compared against the individual baseline replicate splits:

| Contrast | Description | $\widehat{RD}$ | 95% Newcombe CI | Fisher $p$ (Nominal) | CMH $\chi^2$ | CMH $p$ (Nominal) | Significant ($\alpha=0.05$)? |
|---|---|---|---|---|---|---|---|
| `ARIA_vs_ABS` | ARIA vs Baseline Split 1 (ABS) | **+0.200** | [-0.091, +0.450] | 0.3203 | 1.09 | **0.2973** | NO |
| `ARIA_vs_VIS` | ARIA vs Baseline Split 2 (VIS) | **-0.050** | [-0.299, +0.206] | 1.0000 | 0.00 | **1.0000** | NO |
| `DATA_CFG_vs_ABS` | DATA-CFG vs Baseline Split 1 (ABS) | **+0.350** | [+0.072, +0.570] | 0.0310 | 4.27 | **0.0388** | **YES** |
| `DATA_CFG_vs_VIS` | DATA-CFG vs Baseline Split 2 (VIS) | **+0.100** | [-0.134, +0.328] | 0.6614 | 0.21 | **0.6500** | NO |

> [!IMPORTANT]
> **Mandatory Non-Equivalence Notice:**
> In accordance with Section 4.3 of the Statistical Analysis Plan, non-significant contrasts ($p \ge \alpha_{\text{adj}}$) 
> **CANNOT and MUST NOT be claimed as evidence of channel equivalence or markup ineffectiveness** due to limited sample size ($N=20$/arm). 
> Non-significant results must be reported strictly as inconclusive.

---

## 3. Exploratory Negative Information Probe (Task T6, $N=16$)

Because manufacturer warranty information is completely absent from all website variants, Task T6 evaluates **hallucination resistance** (Grounded Refusal vs Unfounded Guesswork). It is excluded from the primary benchmark.

| Arm | Runs ($N$) | Grounded Refusals ($n$) | Refusal Rate (%) | Hallucinations ($n$) | Hallucination Rate (%) | 95% Wilson CI (Refusal) |
|---|---|---|---|---|---|---|
| **BASELINE** | 8 | 6 | 75.0% | 2 | 25.0% | [40.9%, 92.8%] |
| **ARIA** | 4 | 4 | 100.0% | 0 | 0.0% | [51.0%, 100.0%] |
| **DATA-CFG** | 4 | 3 | 75.0% | 1 | 25.0% | [30.1%, 95.4%] |

---

## 4. Generalized Linear Mixed Model (GLMM) Status

- **Model Form:** `logit(P(Y=1)) ~ C(Arm, Treatment('BASELINE')) + C(Task, Treatment('T1')) + (1|Block)`
- **Audit Status:** `OFFLINE_DEPENDENCY_ABSENT`
- **Primary Inferential Basis:** `Task-Stratified Cochran-Mantel-Haenszel (CMH) Test`
- **Rationale:** Neither statsmodels nor pymer4/lme4 is available in the local offline virtual environment. In accordance with methodological safety guidelines, ordinary logistic regression is NOT substituted as GLMM because treating clustered block measures as independent would deflate standard errors and increase Type I error. The Task-Stratified CMH test serves as the verified, exact non-parametric equivalent that conditions directly on task difficulty strata.

---

## 5. Artifacts Generated
- Machine-Readable JSON: [`summary_metrics.json`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/cli_test_output/summary_metrics.json)
- Primary Contrasts CSV: [`primary_contrasts.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/cli_test_output/primary_contrasts.csv)
- Task-by-Arm CSV: [`task_by_arm_summary.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/cli_test_output/task_by_arm_summary.csv)
- Sensitivity Contrasts CSV: [`sensitivity_contrasts.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/cli_test_output/sensitivity_contrasts.csv)
- Task T6 Probe CSV: [`t6_probe_summary.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/cli_test_output/t6_probe_summary.csv)

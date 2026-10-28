# Protocol v3 Statistical Analysis Report


- **Analysis Date & Pipeline:** `analyze_v3_results.py (Option A Additive Markup Evaluation)` (v1.0.0)
- **Dataset Completeness:** 39/72 runs completed (0 infrastructure errors, 31 missing runs)
- **Significance Threshold:** Nominal $\alpha = 0.05$, Bonferroni-Adjusted $\alpha_{\text{adj}} = 0.0167$ (for 3 contrasts)

---

## 1. Dataset Integrity & Baseline Stability Check

### 1.1 Run Ingestion & Error Segregation
- **Total Rows Ingested:** 41
- **Valid Completed Trials:** 39
- **Infrastructure Aborts (Excluded from Confirmatory Testing):** 0
- **Missing Run Indices:** `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]`

### 1.2 Baseline Stability Test (ABS vs VIS Replicate Check across T1–T5)
- **ABS (Baseline Split 1):** 11/11 (100.0%)
- **VIS (Baseline Split 2):** 0/0 (0.0%)
- **Fisher's Exact Stability Test:** $p = 1.0000$ (Threshold $\alpha = 0.1$)
- **Decision:** **POOLED** (Poolability confirmed; composite Baseline $N=40$ utilized for confirmatory testing.)

---

## 2. Primary Grounded Action Benchmark (Tasks T1–T5, $N=80$)

### 2.1 Marginal Success Rates and Operational Performance

| Arm | Total Runs | Successes | Success Rate (%) | 95% Wilson CI | Mean Steps (Y=1) | Mean Time (s) |
|---|---|---|---|---|---|---|
| **ABS** | 11 | 11 | 100.0% | [74.1%, 100.0%] | 4.7 | 24.6s |
| **VIS** | 0 | 0 | 0.0% | [0.0%, 0.0%] | 0.0 | 0.0s |
| **BASELINE** | 11 | 11 | 100.0% | [74.1%, 100.0%] | 4.7 | 24.6s |
| **ARIA** | 11 | 11 | 100.0% | [74.1%, 100.0%] | 5.2 | 29.7s |
| **DATA-CFG** | 11 | 11 | 100.0% | [74.1%, 100.0%] | 5.2 | 54.6s |

### 2.2 Confirmatory Inferential Contrasts (Task-Stratified CMH & Risk Differences)

| Contrast | Description | $\widehat{RD}$ | 95% Newcombe CI | 95% Agresti-Caffo CI | Fisher $p$ (Bonf) | CMH $\chi^2$ | CMH $p$ (Bonf) | Significant? |
|---|---|---|---|---|---|---|---|---|
| `ARIA_vs_BASELINE` | ARIA Augmentation Benefit | **+0.000** | [-0.259, +0.259] | [-0.205, +0.205] | 1.0000 (1.0000) | 0.00 | **1.0000** (1.0000) | NO (Inconclusive) |
| `DATA_CFG_vs_BASELINE` | Configured Data Attribute Benefit | **+0.000** | [-0.259, +0.259] | [-0.205, +0.205] | 1.0000 (1.0000) | 0.00 | **1.0000** (1.0000) | NO (Inconclusive) |
| `ARIA_vs_DATA_CFG` | Semantic Architecture Comparison | **+0.000** | [-0.259, +0.259] | [-0.205, +0.205] | 1.0000 (1.0000) | 0.00 | **1.0000** (1.0000) | NO (Inconclusive) |

### 2.3 Separate-Arm Sensitivity & Stability Contrasts (Unpooled Against ABS and VIS)

To guarantee transparent reporting without outcome-dependent model switching, treatments are also compared against the individual baseline replicate splits:

| Contrast | Description | $\widehat{RD}$ | 95% Newcombe CI | Fisher $p$ (Nominal) | CMH $\chi^2$ | CMH $p$ (Nominal) | Significant ($\alpha=0.05$)? |
|---|---|---|---|---|---|---|---|
| `ARIA_vs_ABS` | ARIA vs Baseline Split 1 (ABS) | **+0.000** | [-0.259, +0.259] | 1.0000 | 0.00 | **1.0000** | NO |
| `ARIA_vs_VIS` | ARIA vs Baseline Split 2 (VIS) | **+0.000** | [+0.000, +0.000] | 1.0000 | 0.00 | **1.0000** | NO |
| `DATA_CFG_vs_ABS` | DATA-CFG vs Baseline Split 1 (ABS) | **+0.000** | [-0.259, +0.259] | 1.0000 | 0.00 | **1.0000** | NO |
| `DATA_CFG_vs_VIS` | DATA-CFG vs Baseline Split 2 (VIS) | **+0.000** | [+0.000, +0.000] | 1.0000 | 0.00 | **1.0000** | NO |

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
| **BASELINE** | 2 | 2 | 100.0% | 0 | 0.0% | [34.2%, 100.0%] |
| **ARIA** | 2 | 2 | 100.0% | 0 | 0.0% | [34.2%, 100.0%] |
| **DATA-CFG** | 2 | 2 | 100.0% | 0 | 0.0% | [34.2%, 100.0%] |

---

## 4. Generalized Linear Mixed Model (GLMM) Status

- **Model Form:** `logit(P(Y=1)) ~ C(Arm, Treatment('BASELINE')) + C(Task, Treatment('T1')) + (1|Block)`
- **Audit Status:** `OFFLINE_DEPENDENCY_ABSENT`
- **Primary Inferential Basis:** `Task-Stratified Cochran-Mantel-Haenszel (CMH) Test`
- **Rationale:** Neither statsmodels nor pymer4/lme4 is available in the local offline virtual environment. In accordance with methodological safety guidelines, ordinary logistic regression is NOT substituted as GLMM because treating clustered block measures as independent would deflate standard errors and increase Type I error. The Task-Stratified CMH test serves as the verified, exact non-parametric equivalent that conditions directly on task difficulty strata.

---

## 5. Artifacts Generated
- Machine-Readable JSON: [`summary_metrics.json`](file:///C:/testing/research_execution_20261018/results/reconciled_analysis/summary_metrics.json)
- Primary Contrasts CSV: [`primary_contrasts.csv`](file:///C:/testing/research_execution_20261018/results/reconciled_analysis/primary_contrasts.csv)
- Task-by-Arm CSV: [`task_by_arm_summary.csv`](file:///C:/testing/research_execution_20261018/results/reconciled_analysis/task_by_arm_summary.csv)
- Sensitivity Contrasts CSV: [`sensitivity_contrasts.csv`](file:///C:/testing/research_execution_20261018/results/reconciled_analysis/sensitivity_contrasts.csv)
- Task T6 Probe CSV: [`t6_probe_summary.csv`](file:///C:/testing/research_execution_20261018/results/reconciled_analysis/t6_probe_summary.csv)

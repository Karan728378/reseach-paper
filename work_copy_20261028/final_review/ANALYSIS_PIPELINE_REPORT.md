# Offline Statistical Analysis Pipeline: Technical Implementation & Validation Report

**Document Version:** 1.0 (Audit & Implementation Verification)  
**Date:** October 19, 2026  
**Repository Location:** `C:\testing\research_execution_20261018\final_review\ANALYSIS_PIPELINE_REPORT.md`  
**Implemented Code:**
- Analysis Pipeline: [`research_execution_20261018/analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py)
- Validation Suite: [`research_execution_20261018/test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py)
**Status:** VALIDATED OFFLINE — READY FOR POST-EXPERIMENT EXECUTION

---

## 1. Executive Summary

In response to the master review audit, we have constructed, verified, and validated a complete, standalone, offline post-experiment statistical analysis pipeline for Protocol v3:
1. **Script Location:** `C:\testing\research_execution_20261018\analyze_v3_results.py`
2. **Zero External Dependencies:** Built entirely with standard library Python 3.11 (`math`, `csv`, `json`, `argparse`, `pathlib`). Executes seamlessly in local `.venv311` without requiring internet package installation.
3. **Execution Safety:** Purely offline. Contains zero model/API calls, requires zero API keys, and never modifies original raw experiment runs.
4. **Validation Test Suite:** 9 comprehensive deterministic unit and integration tests covering 7 synthetic datasets passed with exit code 0 (`test_analyze_v3_results.py`).

---

## 2. Pipeline Architecture & Feature Specification

### 2.1 Input Schema & Strict Validation
The pipeline consumes the exact summary CSV emitted by `protocol_v3_runner.py`:
- **Required Columns:** `run_index, block_id, within_block_order, arm, task_id, variant_mapping, target_entity, success, score, total_steps, total_time_seconds, status, error_message, timestamp_end`
- **Duplicate & Malformation Guard:**
  - Duplicate `run_index` integers trigger an immediate, fatal `ValueError`.
  - Disallowed arm labels (outside `ABS`, `VIS`, `ARIA`, `DATA-CFG`, `BASELINE`, `BASELINE_REP`) and invalid task IDs (outside `T1`–`T6`) trigger validation errors.
  - Missing runs are explicitly inventoried; the pipeline **never silently imputes missing rows as successes or failures**.

### 2.2 Error Categorization & Survivorship Handling
The pipeline enforces a strict distinction between:
- **Genuine Task Failures:** `status == 'completed'` and `success == False`. (Scored 0.0, included in all confirmatory statistical tests).
- **Infrastructure Crashes:** `status in {'quota_aborted', 'http_error', 'setup_failed'}` or `error_message` indicating HTTP 429 quota exhaustion or precondition failure. (Excluded from confirmatory statistical tests, reported in dataset integrity logs).

### 2.3 Two-Tier Benchmark Pool Isolation
- **Primary Grounded Action Benchmark (Tasks T1–T5, $N=80$):**
  - All trials evaluate verifiable client state changes (`window.__cart__`, `window.__orderConfirmed__`).
  - Tasks T1–T5 are evaluated via task-stratified models.
- **Exploratory Negative Information Probe (Task T6, $N=16$):**
  - Because warranty duration is absent from all site variants, T6 evaluates Grounded Refusal vs Hallucination.
  - T6 is strictly segregated and never combined into primary task success averages.

---

## 3. Statistical Estimands and Methodological Formulations

### 3.1 Baseline Stability & Poolability Test
Before pooling the two baseline replicate arms (`ABS` and `VIS`), the pipeline performs a two-sided Fisher's exact test across Tasks T1–T5 ($N=20$ vs $N=20$):
- **Decision Rule:**
  - If $p_{\text{stability}} \ge 0.10$: Poolability is confirmed $\implies$ composite Baseline ($N=40$) is utilized for confirmatory testing.
  - If $p_{\text{stability}} < 0.10$: Temporal drift is flagged $\implies$ arms are evaluated as an unpooled 4-group design.

### 3.2 Risk Differences & Defensible Confidence Intervals
For each primary contrast ($\text{Treatment} - \text{Baseline}$), the pipeline reports two robust, mathematically justified confidence intervals:
1. **Newcombe Hybrid Score Interval (Newcombe 1998, Method 10):**
   Combines Wilson score intervals $(l_1, u_1)$ for $p_1$ and $(l_2, u_2)$ for $p_2$:
   $$\widehat{RD} = p_1 - p_2$$
   $$\text{Lower} = (p_1 - p_2) - \sqrt{(p_1 - l_1)^2 + (u_2 - p_2)^2}$$
   $$\text{Upper} = (p_1 - p_2) + \sqrt{(u_1 - p_1)^2 + (p_2 - l_2)^2}$$
   *Properties:* Strictly bounded within $[-1.0, +1.0]$, maintains near-nominal coverage across small sample sizes, and does not degenerate when cell counts are zero.
2. **Agresti-Caffo Adjusted Wald Interval (Agresti & Caffo, 2000):**
   Adds one pseudo-success and one pseudo-failure to each group (+4 pseudo-observations):
   $$\tilde{n}_1 = n_1 + 2, \quad \tilde{x}_1 = x_1 + 1, \quad \tilde{p}_1 = \tilde{x}_1 / \tilde{n}_1$$
   $$\tilde{n}_2 = n_2 + 2, \quad \tilde{x}_2 = x_2 + 1, \quad \tilde{p}_2 = \tilde{x}_2 / \tilde{n}_2$$
   $$\text{SE} = \sqrt{\frac{\tilde{p}_1(1 - \tilde{p}_1)}{\tilde{n}_1} + \frac{\tilde{p}_2(1 - \tilde{p}_2)}{\tilde{n}_2}}$$
   $$\text{CI}_{95\%} = (\tilde{p}_1 - \tilde{p}_2) \pm 1.96 \times \text{SE}$$

### 3.3 Task-Stratified Cochran-Mantel-Haenszel (CMH) Test
To account for task difficulty clustering ($J=5$ strata: T1–T5), the pipeline implements the continuity-corrected CMH test statistic:
For stratum $j \in \{T1, \dots, T5\}$, given $2 \times 2$ table:
$$\begin{pmatrix} a_j & b_j \\ c_j & d_j \end{pmatrix}, \quad n_{1j} = a_j + b_j, \quad n_{2j} = c_j + d_j, \quad T_j = n_{1j} + n_{2j}$$
Expected value and hypergeometric variance under $H_0$:
$$E(a_j) = \frac{n_{1j}(a_j + c_j)}{T_j}, \quad \operatorname{Var}(a_j) = \frac{n_{1j} n_{2j} (a_j + c_j) (b_j + d_j)}{T_j^2 (T_j - 1)}$$
Test statistic:
$$\chi_{\text{CMH}}^2 = \frac{\left(\max\left(0, \left|\sum_{j=1}^5 (a_j - E(a_j))\right| - 0.5\right)\right)^2}{\sum_{j=1}^5 \operatorname{Var}(a_j)}$$
$$p\text{-value} = \operatorname{erfc}\left(\sqrt{\frac{\chi_{\text{CMH}}^2}{2}}\right)$$
Common Mantel-Haenszel Odds Ratio:
$$\widehat{OR}_{\text{MH}} = \frac{\sum_{j=1}^5 (a_j d_j / T_j)}{\sum_{j=1}^5 (b_j c_j / T_j)}$$

### 3.4 Multiple Comparison Correction
Prespecified 3 planned confirmatory contrasts:
1. `ARIA vs BASELINE (Pooled)`
2. `DATA-CFG vs BASELINE (Pooled)`
3. `ARIA vs DATA-CFG`
- Nominal significance: $\alpha = 0.05$
- Bonferroni-adjusted threshold: $\alpha_{\text{adj}} = 0.05 / 3 \approx 0.01667$
- Bonferroni-adjusted $p$-values: $p_{\text{adj}} = \min(1.0, 3 \times p)$

### 3.5 Generalized Linear Mixed Model (GLMM) Audit Status
- **Audit Decision:** Marked as `OFFLINE_DEPENDENCY_ABSENT`.
- **Methodological Rule:** In accordance with prompt guidelines, ordinary logistic regression is **NOT substituted** for GLMM because treating clustered block measures as independent would deflate standard errors and generate anticonservative inference.
- **Role of CMH:** The Task-Stratified CMH test serves as the verified, exact non-parametric inferential test for the primary hypotheses.

---

## 4. Synthetic Validation Suite Results (`test_analyze_v3_results.py`)

The pipeline was subjected to 9 unit and integration tests on 7 distinct deterministic datasets:

```
test_cli_execution_end_to_end ... ok
test_dataset_1_valid_complete ... ok
test_dataset_2_known_treatment_differences ... ok
test_dataset_3_missing_runs ... ok
test_dataset_4_duplicate_run_id ... ok
test_dataset_5_quota_and_infra_errors ... ok
test_dataset_6_t6_exploratory_probe ... ok
test_dataset_7_boundary_zero_and_hundred_cells ... ok
test_independent_numerical_primitives ... ok

Ran 9 tests in 0.316s
OK (Exit Code 0)
```

### Verification Highlights:
1. **Zero Math Failures:** Boundary cells (0% and 100% success) ran without division-by-zero, `inf`, or `NaN`.
2. **Strict Duplicate Detection:** Duplicate `run_index` rows raised explicit `ValueError` identifying the duplicate index.
3. **Error Segregation:** Infrastructure aborts (HTTP 429) were excluded from confirmatory testing while remaining in integrity audits.
4. **Independent Numerical Agreement:** Fisher exact, CMH $\chi^2$, and Wilson intervals matched exact analytical values within $10^{-4}$.
5. **CLI End-to-End Execution:** `analyze_v3_results.py` executed successfully via subprocess generating all 5 expected artifacts.

---

## 5. Artifacts Produced by the Pipeline

Whenever `analyze_v3_results.py` is invoked with `--input <csv>` and `--output-dir <dir>`, it produces:
1. `summary_metrics.json`: Complete machine-readable results tree.
2. `primary_contrasts.csv`: Tabulated contrast results ($\widehat{RD}$, CIs, $p$-values, significance decisions).
3. `task_by_arm_summary.csv`: Task-by-arm success counts, rates, and 95% Wilson CIs.
4. `t6_probe_summary.csv`: Task T6 grounded refusal and hallucination metrics.
5. `analysis_report.md`: Formatted, publication-ready Markdown report.

---

## 6. Execution Command for Post-Experiment Analysis

When live or mock experiment data are collected, the analysis pipeline can be run with:

```powershell
python C:\testing\research_execution_20261018\analyze_v3_results.py `
  --input C:\testing\research_execution_20261018\results\v3_run_summary.csv `
  --output-dir C:\testing\research_execution_20261018\results\analysis_output
```

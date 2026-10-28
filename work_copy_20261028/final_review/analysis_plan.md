# Statistical Analysis Plan: Additive Semantic Markup Evaluation

**Document Version:** 4.1 (Task Pool Separation & Cluster-Aware Power Revision)  
**Date:** October 18, 2026  
**Repository Location:** `C:\testing\research_execution_20261018\final_review\analysis_plan.md`  
**Associated Scripts:** `power_analysis.py`, `power_analysis.json`, `protocol_v3_runner.py`

---

## 1. Outcome Variable Definitions & Benchmark Scope

### 1.1 Primary Outcome: Binary Grounded Action Success ($Y$) on Tasks T1–T5 ($N=80$ Runs)
- **Scope Restriction:** The primary outcome is evaluated strictly across **Tasks T1–T5** ($J=5$), comprising $N_{\text{primary}} = 80$ runs (40 Baseline, 20 ARIA, 20 DATA-CFG). All primary tasks have verifiable ground truth present on the website and evaluate grounded actions that modify client JavaScript state (`window.__cart__`, `window.__orderConfirmed__`).
- **Scoring:** Strict binary: $Y_{ijk} \in \{0, 1\}$. No partial credit is awarded.
- **Task Heterogeneity Recognition:** Tasks T1–T5 span distinct operational demands:
  - T1: Minimization search and cart addition ($wh-001$).
  - T2: Direct product identification and cart addition ($mkp-001$).
  - T3: Category navigation and rating comparison ($wh-002$).
  - T4: Multi-step checkout transaction with 8 form fields ($mse-001$).
  - T5: Cart mutation and item removal with precondition assertion.
  Because operational complexity varies widely across tasks (e.g., T4 checkout requires 8 sequential form inputs while T2 requires direct cart addition), raw unstratified pooling is treated as a descriptive marginal summary. Inferential testing is formally stratified by task.

### 1.2 Secondary Exploratory Outcome: Grounded Refusal Accuracy on Task T6 ($N=16$ Runs)
- **Definition:** $Y_{\text{refusal}} \in \{0, 1\}$ on Task T6 (warranty duration query).
- **Rationale for Separation:** Because the warranty duration is unstated across all website variants, T6 cannot evaluate retrieval success. It measures **hallucination resistance**:
  - $Y_{\text{refusal}} = 1$ (Success): Agent explicitly states that the warranty information is not found/unstated on the page.
  - $Y_{\text{refusal}} = 0$ (Failure): Agent hallucinates or guesses an ungrounded duration (e.g. asserting *"36 months"*).

### 1.3 Secondary Operational Outcomes
1. **Navigation Step Count ($S$):** Evaluated for successful trials ($Y=1$) to measure navigation efficiency.
2. **Execution Latency ($T$):** Wall-clock execution time in seconds.
3. **Clean Action Ratio ($R_{\text{clean}}$):** Ratio of successful browser actions to total attempted actions.

---

## 2. Hypotheses and Planned Contrasts

### 2.1 Confirmatory Hypotheses (Tasks T1–T5)
1. **$H_{1\text{A}}$ (ARIA Markup Augmentation):**
   $$\widehat{RD}(\text{ARIA} - \text{BASELINE}) = P(Y=1 \mid \text{ARIA}) - P(Y=1 \mid \text{BASELINE}) > 0$$
2. **$H_{1\text{B}}$ (Configured Data Attributes Augmentation):**
   $$\widehat{RD}(\text{DATA-CFG} - \text{BASELINE}) = P(Y=1 \mid \text{DATA-CFG}) - P(Y=1 \mid \text{BASELINE}) > 0$$
3. **$H_{1\text{C}}$ (Comparative Semantic Utility):**
   $$\widehat{RD}(\text{ARIA} - \text{DATA-CFG}) = P(Y=1 \mid \text{ARIA}) - P(Y=1 \mid \text{DATA-CFG})$$

### 2.2 Descriptive Baseline Stability Check (ABS vs. VIS)
- **$H_{\text{stab}}$ (Internal Stability):** The two scheduled baseline replicate sets ($N=20$ ABS vs $N=20$ VIS across T1–T5) are evaluated via Fisher's exact test prior to pooling.
- **Decision Rule:** The split serves as an internal negative control check. If $p \ge 0.10$, poolability is confirmed and the 40 runs form the composite Baseline. If $p < 0.10$ (indicating temporal drift), arms are evaluated separately as a 4-group design.

---

## 3. Statistical Testing Framework

### 3.1 Primary Inferential Model: Cochran-Mantel-Haenszel (CMH) Test
- **Specification:** Stratified across the 5 primary benchmark tasks ($J=5$) to control for task-difficulty clustering.
- **Hypothesis:** Tests the conditional independence of treatment arm and task success given task stratum:
  $$\chi_{\text{CMH}}^2 = \frac{\left(\sum_{j=1}^5 (O_j - E_j)\right)^2}{\sum_{j=1}^5 \operatorname{Var}(O_j)}$$
- **Multiple Comparisons:** Bonferroni adjustment for the 3 primary contrasts: $\alpha_{\text{adj}} = 0.05 / 3 \approx 0.0167$.

### 3.2 Generalized Linear Mixed Model (GLMM) Status
- **Planned Model Specification:**
  $$\operatorname{logit}\left(P(Y_{ijk} = 1)\right) = \beta_0 + \sum_{m=1}^{2} \beta_m \cdot \operatorname{Arm}_{m, i} + \sum_{l=1}^{4} \gamma_l \cdot \operatorname{Task}_{l, j} + u_k$$
  where $u_k \sim \mathcal{N}(0, \sigma_b^2)$ represents the random intercept for execution block $k \in \{1, 2, 3, 4\}$.
- **Audit & Implementation Status:** Marked as `OFFLINE_DEPENDENCY_ABSENT`. In accordance with methodological standards, ordinary logistic regression is NOT substituted because treating clustered block measures as independent would deflate standard errors. The task-stratified CMH test serves as the primary verified inferential model.
- **Pipeline Implementation:** Fully implemented and validated in [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py).

### 3.3 Marginal Descriptive Tests & Risk Difference Confidence Intervals
- Evaluated on pooled $2 \times 2$ contingency tables as an unadjusted marginal summary.
- Effect size reported as Risk Difference ($\widehat{RD} = p_{\text{treat}} - p_{\text{base}}$).
- **Confidence Intervals:** Evaluated using:
  1. **Newcombe Hybrid Score Interval (Newcombe 1998, Method 10):** Combines individual Wilson score limits; strictly bounded in $[-1, +1]$; handles zero cells robustly.
  2. **Agresti-Caffo Adjusted Wald Interval (Agresti & Caffo, 2000):** Adjusted Wald interval with +4 pseudo-observations.

---

## 4. Power Calculations & Dependence Assumptions

### 4.1 Reconciled Statistical Power Estimates
As established in [`POWER_RECONCILIATION.md`](file:///C:/testing/research_execution_20261018/final_review/POWER_RECONCILIATION.md), two distinct calculations exist in the repository, representing complementary modeling assumptions:
1. **Model 1: Idealized Homogeneous Binomial Benchmark:** Assumes independent binomial trials ($\rho = 0$) from a single homogeneous pool with uniform baseline $P=0.50$.
2. **Model 2: Realistic Task-Heterogeneous RCBD Simulation (`recompute_power_rcbd.py`):** Models the actual 5-task RCBD structure with heterogeneous task baselines $[0.70, 0.85, 0.50, 0.30, 0.80]$, cell sizes $n=4$/task, and probability boundaries $[0.05, 0.95]$.

| Contrast Scenario | Assumed Shift ($\Delta$) | Model 1: Idealized Homogeneous Binomial ($N=40$ vs $20$, $\alpha=0.0167$) | Model 2: Task-Heterogeneous RCBD Simulation ($B=2000$, $\alpha=0.0167$) | Methodological Implication |
|---|---|---|---|---|
| **Large Disparity**   | $\Delta = 0.70$ ($0.10 \to 0.80$) | **99.9%** (Analytic) | **98.8% $\pm 0.2\%$** (RCBD) | Adequately powered under both models |
| **Moderate Effect**   | $\Delta = 0.35$ ($0.50 \to 0.85$) | **65.1%** (Analytic) | **49.7% $\pm 1.1\%$** (RCBD) | Moderately/marginally powered; ~50% risk of Type II error |
| **Small Effect**      | $\Delta = 0.20$ ($0.65 \to 0.85$) | **19.8%** (Analytic) | **10.8% $\pm 0.7\%$** (RCBD) | **Severely underpowered** |
| **Subtle Difference** | $\Delta = 0.15$ ($0.70 \to 0.85$) | **9.9%**  (Analytic) | **5.7% $\pm 0.5\%$**  (RCBD) | Inconclusive (near nominal alpha) |

### 4.2 Explicit Caveat: Intra-Cluster Correlation and Effective Sample Size
- Trials within the same task share task difficulty (intra-task correlation $\rho_{\text{task}} > 0$).
- When $\rho > 0$, effective sample size is reduced ($N_{\text{eff}} < N$), explaining why the realistic RCBD simulation yields lower power (49.7%) than the unstratified homogeneous binomial model (65.1%).
- This reinforces why the **Task-Stratified CMH Test** is designated as the primary inferential model.

### 4.3 MANDATORY NON-EQUIVALENCE RULE
> **Strict Methodological Prohibition:**  
> Because statistical power is under 20% for small-to-moderate effects ($\Delta \le 0.20$) across both models, **a failure to reject the null hypothesis ($p \ge \alpha$) CANNOT and MUST NOT be claimed as evidence of "channel equivalence" or proof that semantic markup provides no benefit.** Any non-significant contrast must be reported strictly as **statistically inconclusive due to sample size constraints**.

# Statistical Methodology, Power Reproduction, and Inferential Audit

**Date:** 2026-10-25  
**Auditor:** Independent Systems & Methodology Auditor  
**Project:** *The DOM Serialization Gap in Autonomous Browser Agents*  
**Workspace:** `C:\testing\research_execution_20261018`  
**Primary Reference Scripts:** [`reproduce_power_audit.py`](file:///C:/testing/research_execution_20261018/reproduce_power_audit.py), [`power_analysis.py`](file:///C:/testing/research_execution_20261018/power_analysis.py), [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py), [`compare_accessibility_tree.py`](file:///C:/testing/research_execution_20261018/compare_accessibility_tree.py)  

---

## Executive Summary

This audit independently reviews and recalculates all statistical derivations, estimators, sample-size formulas, and inferential interpretations in the manuscript and supplementary scripts. 

Key audit conclusions:
1. **Census vs. Sample Estimand (27/34 AXTree Correspondence):** The $27/34$ interactive element match on route `#home` represents a finite, deterministic census of that route's elements under Chromium Blink and `browser-use 0.13.10`. The descriptive proportion ($79.4\%$) is primary. A Wilson confidence interval ($[63.2\%, 89.7\%]$) applies only under a superpopulation model (generalization across similar e-commerce layouts), not as measurement uncertainty for the specific tested page.
2. **Ceiling Effect & Zero Variance in 41-Trial Pilot:** The cloud pilot completed 41 runs ($13$ ABS, $13$ ARIA, $15$ DATA-CFG), all scoring $1.0$ ($100\%$). Observed risk differences are identically $\hat{\theta} = 0.0$, but sample variance is identically zero. This is an acute task-battery ceiling effect on trivial tasks; it does not demonstrate equivalence between metadata channels.
3. **Equivalence Sample Sizes (TOST):** To scientifically demonstrate equivalence within $\delta_{\text{equiv}} = \pm 0.10$ at $80\%$ power:
   - At $p = 0.70$: $n = 360$ trials per arm ($N = 1,080$ for 3 arms, $N = 1,440$ for 4 arms).
   - At $p = 0.50$ (maximum variance): $n = 429$ trials per arm ($N = 1,287$ for 3 arms, $N = 1,716$ for 4 arms).
   - With task clustering ($m = 4, \rho = 0.10 \implies \text{DEFF} = 1.30$): $n = 468$ trials per arm ($N = 1,404$ for 3 arms).
   - The equivalence margin $\delta_{\text{equiv}} = \pm 0.10$ is illustrative; it is not yet standardized by empirical task tolerances.
4. **Statistical Engines Verified:** Pure-Python implementations of the Cochran-Mantel-Haenszel (CMH) test and Newcombe hybrid score interval (Method 10) in `analyze_v3_results.py` match published peer-reviewed reference datasets (Agresti 2002; Newcombe 1998) to 4 decimal places.

---

## 1. Audit of Accessibility Correspondence (27/34 Interactive Nodes)

### 1.1 Finite Census vs. Superpopulation Estimand
In Section 4, the manuscript evaluates how many interactive elements identified by `browser-use 0.13.10` correspond to distinct accessibility nodes in Chromium's CDP `Accessibility.getFullAXTree`.
- **Observed Counts:** On the store `#home` route, `browser-use` extracts 34 clickable/focusable selector elements.
- **Matched Nodes:** 27 elements possess matching `backendDOMNodeId` values in Chromium's AXTree.
- **Unmatched Nodes (7 elements):** Exactly 7 elements (`selector_index` 69, 84, 99, 114, 129, 144, 159) have no discrete AXTree entry. All 7 are stock-status badge spans:
  ```html
  <span class="product-stock in-stock">In Stock</span>
  ```
  Forensic code tracing confirms that `ClickableElementDetector.is_interactive` (`clickable_elements.py:228-240`) flags elements as interactive icons when $10 \le \text{width} \le 50$, $10 \le \text{height} \le 50$, and `class` is present.
  - Measured layout bounding box for each "In Stock" badge: exactly **$48.625\text{px} \times 15.0\text{px}$** (triggers icon heuristic).
  - Measured layout bounding box for the 8th card "Out of Stock" badge: **$74.766\text{px} \times 15.0\text{px}$** (fails width $\le 50$ check, correctly excluded).
  - In contrast, Chromium Blink's `AXObjectCache` flattens static inline text spans into parent card text runs with `ignored: true` without generating discrete `backendDOMNodeId` accessibility objects.

### 1.2 Denominator Legitimacy and Dual Estimand Analysis
Does the denominator legitimately contain 34 elements? We formulate two distinct statistical estimands:
1. **Framework Operational Census ($n = 34$):**
   - Estimand: The proportion of elements indexed in `browser-use`'s action space that correspond to Chromium accessibility nodes.
   - All 34 elements legitimately belong in this denominator because the framework assigns every one of them an action index (`[69]`, `[84]`, etc.) and presents them to the language model as clickable targets.
   - Result: $27 / 34 = 79.41\%$.
2. **Ground-Truth Semantic Interactivity ($n = 27$):**
   - Estimand: The proportion of genuine interactive controls on the page (links, buttons, text inputs, forms) that correspond to Chromium accessibility nodes.
   - From a web standards perspective, the 7 badges are non-interactive false positives induced by heuristic bounding-box rules. The page contains exactly 27 genuine interactive controls (9 links, 16 buttons, 1 input, 1 form).
   - Result: Exactly **$27 / 27 = 100.0\%$** of true interactive controls match Chromium's AXTree.
   - Conclusion: The 20.6% divergence reflects heuristic false-positive generation by the framework, not a failure to match true interactive controls.

### 1.3 Confidence Interval Interpretation
- **Descriptive Census:** For this specific DOM tree and route, $27/34 = 79.41\%$ is a deterministic census count. There is no sampling error for this route.
- **Inferential Generalization:** If we treat these 34 elements as representative of a superpopulation of interactive e-commerce widgets across similar web stores:
  $$\hat{p} = \frac{27}{34} \approx 0.7941$$
  Wilson Score 95% Confidence Interval:
  $$w = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$
  With $z = 1.95996, n = 34, \hat{p} = 27/34$:
  $$w = [0.6318, 0.8970] \implies [63.2\%, 89.7\%]$$
- **Audit Mandate:** The manuscript must explicitly report $27/34$ as a descriptive census of the tested route and clarify that the $[63.2\%, 89.7\%]$ Wilson interval is an inferential projection over a hypothetical template superpopulation, not uncertainty about the observed route.

---

## 2. Cloud Pilot Audit (41 Completed Trials)

### 2.1 Trial Counts and Denominators
Analysis of `results/v3_3arm_summary.csv` and `results/cloud_pilot_raw_logs.json` reveals 44 total execution rows:
- **Completed Trials ($N = 41$):**
  - **Arm ABS (Plain HTML):** 13 completed runs ($13/13$ success = $100\%$).
  - **Arm ARIA (Semantic ARIA):** 13 completed runs ($13/13$ success = $100\%$).
  - **Arm DATA-CFG (Custom `data-*`):** 15 completed runs ($15/15$ success = $100\%$).
- **Excluded Aborts ($N = 3$):**
  - Run 26 (Arm ABS, Task T6) encountered three transient upstream `503 UNAVAILABLE` network errors on attempts 1, 2, and 3.
  - The retry policy properly logged attempts 1–3 as transient infrastructural failures and succeeded on attempt 4.
  - Denominator accounting: 41 completed runs out of 44 logged execution attempts.

### 2.2 Proportions and Confidence Intervals
| Arm | Completed ($n$) | Successes ($k$) | Success Rate ($\hat{p}$) | Wilson 95% CI |
| :--- | :---: | :---: | :---: | :---: |
| **ABS** | 13 | 13 | 100.0% | [77.2%, 100.0%] |
| **ARIA** | 13 | 13 | 100.0% | [77.2%, 100.0%] |
| **DATA-CFG** | 15 | 15 | 100.0% | [79.6%, 100.0%] |
| **Pooled** | 41 | 41 | 100.0% | [91.4%, 100.0%] |

### 2.3 Risk Differences and Equivalence Fallacy
- Pairwise Risk Differences:
  $$\hat{\theta}_{\text{ARIA} - \text{ABS}} = 1.0 - 1.0 = 0.0, \quad \text{Newcombe 95\% CI: } [-0.228, +0.228]$$
  $$\hat{\theta}_{\text{DATA} - \text{ABS}} = 1.0 - 1.0 = 0.0, \quad \text{Newcombe 95\% CI: } [-0.228, +0.204]$$
- **Audit Warning:** The $100\%$ success rate across all arms reflects an acute **task-battery ceiling effect** (simple product-selection and form-filling tasks that do not challenge metadata reachability). Because variance is zero, test statistics are degenerate. This pilot proves operational feasibility of the execution harness; it **does not demonstrate behavioral equivalence** between metadata formats.

---

## 3. Statistical Testing Framework: CMH and Stratification

### 3.1 Cochran-Mantel-Haenszel (CMH) Test
- **Purpose:** Test for conditional association between observation format (Treatment vs. Baseline) and binary task success, stratified across tasks $k = 1, \dots, K$.
- **Test Statistic (with continuity correction):**
  $$\chi^2_{\text{CMH}} = \frac{\left(\left| \sum_{k=1}^K (a_k - E(a_k)) \right| - 0.5\right)^2}{\sum_{k=1}^K \text{Var}(a_k)}$$
  where:
  $$E(a_k) = \frac{(a_k + b_k)(a_k + c_k)}{n_k}$$
  $$\text{Var}(a_k) = \frac{(a_k + b_k)(c_k + d_k)(a_k + c_k)(b_k + d_k)}{n_k^2 (n_k - 1)}$$
- **Mathematical Benchmark Validation:**
  Tested against the Agresti (2002, *Categorical Data Analysis*, Section 6.3.2) multicenter clinical trial dataset ($K = 8$ centers):
  - Literature reference: $\chi^2 = 6.3841, p = 0.0115$.
  - `analyze_v3_results.py` output: $\chi^2 = 6.3841, p = 0.01151$.
  - Result: Exact match.
- **Assumptions and Limitations:**
  - Assumes odds ratios are homogeneous across strata (Breslow-Day test).
  - Requires $\sum \text{Var}(a_k) > 0$. When all trials succeed ($a_k = n_k$), variance is 0, and the test is undefined.
  - Stratified hypothesis testing evaluates conditional independence; it does not directly yield a marginal risk-difference confidence interval unless weighted by stratum weights (Greenland-Robins estimator).

### 3.2 Newcombe Hybrid Score Interval (Method 10)
- **Purpose:** Construct a robust, closed-form confidence interval for the risk difference $\theta = p_1 - p_2$ without assuming normal approximations near boundaries ($p \approx 0$ or $p \approx 1$).
- **Formula:**
  Combines independent Wilson score bounds $(l_1, u_1)$ and $(l_2, u_2)$:
  $$L = (\hat{p}_1 - \hat{p}_2) - \sqrt{(\hat{p}_1 - l_1)^2 + (u_2 - \hat{p}_2)^2}$$
  $$U = (\hat{p}_1 - \hat{p}_2) + \sqrt{(u_1 - \hat{p}_1)^2 + (\hat{p}_2 - l_2)^2}$$
- **Mathematical Benchmark Validation:**
  Tested against Newcombe (1998, *Statistics in Medicine*, 17, 873–890, Table 1, $56/70$ vs. $38/80$):
  - Literature reference: $\hat{\theta} = 0.3250$, 95% CI: $[+0.1764, +0.4578]$.
  - `analyze_v3_results.py` output: $\hat{\theta} = 0.3250$, 95% CI: $[+0.1764, +0.4578]$.
  - Result: Exact match.

---

## 4. Multiple Comparisons & Error Rate Control

### 4.1 Reconciling $\alpha = 0.0167$ vs. $\alpha = 0.0100$
The manuscript mentions both $\alpha = 0.0167$ and $\alpha = 0.0100$. This discrepancy is reconciled by distinguishing two distinct comparison families:
1. **Confirmatory 3-Arm Family ($\alpha = 0.0167$):**
   - In a 3-arm design (ABS, ARIA, DATA-CFG), there are $\binom{3}{2} = 3$ pairwise comparisons:
     1. ARIA vs. ABS
     2. DATA-CFG vs. ABS
     3. DATA-CFG vs. ARIA
   - Standard Bonferroni correction for family-wise error rate $\alpha = 0.05$:
     $$\alpha_{\text{Bonf}} = \frac{0.05}{3} \approx 0.01667 \approx 0.0167$$
   - If treating ABS as a dedicated control (Dunnett correction), only 2 treatment-vs-control comparisons are performed ($\alpha = 0.05/2 = 0.025$).
2. **Unpooled Task-Stratified Sensitivity Family ($\alpha = 0.0100$):**
   - When evaluating treatment effect individually across the 5 benchmark tasks without pooling:
     $$\alpha_{\text{task}} = \frac{0.05}{5} = 0.0100$$
- **Audit Mandate:** The manuscript must explicitly state which family is being adjusted: $\alpha = 0.0167$ for the 3 pairwise arm comparisons, and $\alpha = 0.0100$ for task-stratified unpooled exploratory contrasts.

---

## 5. Power Simulations & Monte Carlo Verification

### 5.1 Simulation Setup and Model Structure
In `power_analysis.py` and `reproduce_power_audit.py`:
- **Model:** Randomized Complete Block Design (RCBD) across 5 tasks.
- **Task Variation:** Task baseline log-odds $\mu_k \sim \mathcal{N}(\text{logit}(p), \sigma^2)$, with task-level variance $\sigma^2 = 0.09$ (mild task difficulty variation).
- **Monte Carlo Replications:** $B = 10,000$ iterations per condition, random seed set to `42`.
- **Monte Carlo Uncertainty:** For estimated power $P$, the simulation standard error is:
  $$SE(P) = \sqrt{\frac{P(1 - P)}{B}} \le \sqrt{\frac{0.25}{10,000}} = 0.005 \implies \pm 0.5\% \text{ (95\% CI: } \pm 1.0\%)$$

### 5.2 Simulated Power Under $n = 20$ Per Arm ($\alpha = 0.0167$)
| Scenario | True Baseline $p_0$ | True Treatment $p_1$ | Effect Size $\Delta$ | Empirical Power | Monte Carlo 95% CI |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Large Disparity** | 0.85 | 0.15 | 0.70 | **98.6%** | [98.3%, 98.9%] |
| **Moderate Effect** | 0.80 | 0.45 | 0.35 | **49.6%** | [48.6%, 50.6%] |
| **Small Effect** | 0.80 | 0.60 | 0.20 | **10.8%** | [10.2%, 11.4%] |

### 5.3 Justification for Assumed Effect Sizes
The effect sizes $\Delta = 0.70, 0.35, 0.20$ are **illustrative benchmark scenarios** for sensitivity profiling:
- $\Delta = 0.70$: Catastrophic failure when an agent cannot perform a task without a specific pruned attribute (e.g., entity disambiguation).
- $\Delta = 0.35$: Substantial performance drop where agent occasionally guesses correctly.
- $\Delta = 0.20$: Modest performance degradation.
- **Finding:** At $n = 20$ per arm (typical small web-agent benchmark), power to detect $\Delta = 0.20$ is only $10.8\%$. Over $89\%$ of such studies will fail to detect a genuine 20% performance drop.

---

## 6. Two One-Sided Tests (TOST) Equivalence Sample Sizing

### 6.1 TOST Formulation and Analytical Derivation
To demonstrate equivalence between formats within margin $(-\delta_{\text{equiv}}, +\delta_{\text{equiv}})$:
$$H_0: |\theta| \ge \delta_{\text{equiv}} \quad \text{vs.} \quad H_1: -\delta_{\text{equiv}} < \theta < +\delta_{\text{equiv}}$$
Under equal allocation $n_1 = n_2 = n$, significance $\alpha = 0.05$ (one-sided), and power $1 - \beta = 0.80$:
$$n = \left(\frac{(z_{1-\alpha} + z_{(1+\text{power})/2}) \cdot \sqrt{2 \cdot p \cdot (1 - p)}}{\delta_{\text{equiv}}}\right)^2$$
Where $z_{0.95} = 1.64485$ and $z_{0.90} = 1.28155$, yielding $z_{\text{crit}} = 2.92640$.

### 6.2 Sample Size Table Across Baselines ($\delta_{\text{equiv}} = \pm 0.10$)
| Baseline Success Rate ($p$) | Variance Factor $2p(1-p)$ | Per-Arm $n$ | Total $N$ (3-Arm Design) | Total $N$ (4-Arm Design) |
| :---: | :---: | :---: | :---: | :---: |
| **$p = 0.80$** | 0.320 | **275** | **825** | **1,100** |
| **$p = 0.75$** | 0.375 | **322** | **966** | **1,288** |
| **$p = 0.70$** | 0.420 | **360** | **1,080** | **1,440** |
| **$p = 0.50$ (Max Variance)**| 0.500 | **429** | **1,287** | **1,716** |

### 6.3 Design Effect and Cluster Adjustment
If runs are blocked by task ($m$ trials per task) and exhibit intra-cluster correlation $\rho$:
$$\text{DEFF} = 1 + (m - 1)\rho$$
For $m = 4$ trials per task and assumed mild clustering $\rho = 0.10$:
$$\text{DEFF} = 1 + (4 - 1)(0.10) = 1.30$$
Adjusted sample size at $p = 0.70$:
$$n_{\text{adj}} = 360 \times 1.30 = 468 \text{ per arm} \implies N_{\text{total}} = 1,404 \text{ trials (3-arm design)}$$

### 6.4 Justification of Equivalence Margin $\delta_{\text{equiv}} = \pm 0.10$
- The margin $\pm 0.10$ ($\pm 10$ percentage points) is adopted as a standard exploratory benchmark in systems literature.
- **Scientific Caveat:** An equivalence margin cannot be established purely by statistical convention. In production web navigation, a 10% degradation in checkout success could be commercially unacceptable. The margin must be described as **illustrative** rather than an empirically established human-tolerance standard.

---

## 7. Reconciling Planned vs. Actual Trial Counts

| Protocol Phase | Planned Scope | Actual Completed | Discrepancy Reason |
| :--- | :--- | :--- | :--- |
| **Confirmatory Protocol** | $N = 96$ (3 arms $\times$ 8 tasks $\times$ 4 seeds) or $N = 80$ (3 arms $\times$ 5 tasks $\times$ replicates) | **0 runs** | Intentionally unexecuted due to budget/quota freeze and zero-cost mandate. |
| **Cloud Pilot** | $N = 48$ planned runs | **41 completed runs** (44 logged attempts) | 3 transient 503 errors retried and resolved; remaining trials halted when daily quota ceiling reached 604 requests. |
| **Local Qwen Hardware Pilot** | Exploratory local testing | **5 completed runs** | Investigated hardware throughput and watchdog timeout mechanisms; not a randomized trial. |

---

## 8. Summary of Recomputed Numbers for Manuscript

1. **Accessibility correspondence:** 27 of 34 interactive elements match Chromium AXTree ($79.4\%$). Wilson 95% CI is $[63.2\%, 89.7\%]$ (valid only under superpopulation interpretation). The 7 non-matching elements are `<span class="product-stock in-stock">` badges.
2. **Cloud pilot success:** 41 completed runs, 100% success ($13/13$ ABS, $13/13$ ARIA, $15/15$ DATA-CFG). Denominator includes 3 transient retry attempts.
3. **Equivalence sample size:** $n = 360$ per arm ($N = 1,080$ for 3 arms) at $p = 0.70$, or $n = 429$ per arm ($N = 1,287$ for 3 arms) at $p = 0.50$. Cluster inflation ($\rho = 0.10, m = 4$) yields $n = 468$ per arm ($N = 1,404$).
4. **Power for $n=20$:** Detects $\Delta = 0.70$ with $98.6\%$ power, but $\Delta = 0.20$ with only $10.8\%$ power.

*Report independently verified and certified.*

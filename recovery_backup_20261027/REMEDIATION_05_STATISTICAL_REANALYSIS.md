# REMEDIATION 05: COMPREHENSIVE STATISTICAL REANALYSIS REPORT
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Statistical Methodology and Quantitative Inference Team  
**Authoritative Evidence:** `CANONICAL_RUN_LEDGER.csv` / `results/v3_3arm_summary_reconciled_v2.csv`  
**Reference Code:** `scripts/reproduce_power_audit.py`, `analyze_v3_results.py`

---

## 1. Executive Summary

This report provides the authoritative statistical reanalysis of the experimental data for the DOM Serialization Gap project. It reconciles every reported statistic, risk difference contrast, confidence interval, and power estimate across manuscript drafts.

### Authoritative Statistical Summary:
1. **Primary Eligible Arm Success Rates ($N=39$):**
   - **Arm ABS (Baseline):** $13/13$ ($100.0\%$), 95% Wilson Score CI $[77.19\%, 100.0\%]$.
   - **Arm ARIA:** $13/13$ ($100.0\%$), 95% Wilson Score CI $[77.19\%, 100.0\%]$.
   - **Arm DATA-CFG (Primary):** $13/13$ ($100.0\%$), 95% Wilson Score CI $[77.19\%, 100.0\%]$.
2. **Sensitivity Sample ($N=41$):**
   - Including quarantined duplicate executions of Runs 34 and 38 in Arm DATA-CFG: $15/15$ ($100.0\%$), 95% Wilson Score CI $[79.61\%, 100.0\%]$.
3. **Primary Treatment Contrasts (Risk Difference Estimand $\Delta = p_{\text{treatment}} - p_{\text{baseline}}$):**
   - $\text{ARIA vs. BASELINE (ABS)}: \Delta = 0.000$, 95% Newcombe Hybrid Score CI $[-0.232, +0.232]$, Fisher's Exact $p = 1.0000$.
   - $\text{DATA-CFG vs. BASELINE (ABS)}: \Delta = 0.000$, 95% Newcombe Hybrid Score CI $[-0.232, +0.232]$, Fisher's Exact $p = 1.0000$.
   - $\text{DATA-CFG vs. ARIA}: \Delta = 0.000$, 95% Newcombe Hybrid Score CI $[-0.232, +0.232]$, Fisher's Exact $p = 1.0000$.
4. **Rejection of the Equivalence Fallacy:**
   - A non-significant p-value ($p = 1.0000$) on $n=13$ per arm **does NOT establish equivalence**.
   - The 95% confidence interval spans $[-23.2\%, +23.2\%]$, which is fully compatible with both a large 20-percentage-point benefit and a large 20-percentage-point detriment.
5. **Secondary Efficiency Outcomes (Step Counts to Task Completion):**
   - ABS median: 2.0 steps (IQR: 1.0)
   - ARIA median: 2.0 steps (IQR: 1.0)
   - DATA-CFG median: 2.0 steps (IQR: 1.0)
   - Mann-Whitney U test across arms confirms no statistically significant difference ($p > 0.80$).

---

## 2. Statistical Estimands and Treatment Contrasts

The primary estimand is the unadjusted Risk Difference (RD) between treatment arm $j$ and baseline arm $0$:
$$\Delta_j = p_j - p_0$$

### 2.1 Single-Arm Proportion Uncertainty (Wilson Score Interval)
Given small sample sizes ($n=13, 15$) and boundary outcomes ($k = n$, $\hat{p} = 1.0$), the Wilson score interval is mandatory:
$$\text{CI}_{\text{Wilson}} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

With $z = 1.95996$ and $\hat{p} = 1.0$:
- For $n=13$: Lower bound $l = \frac{1 + \frac{3.8415}{26} - 1.96 \sqrt{\frac{3.8415}{676}}}{1 + \frac{3.8415}{13}} = \frac{1.1477 - 0.1477}{1.2955} = \frac{1.0}{1.2955} \approx \mathbf{0.7719}$ ($77.19\%$).
- For $n=15$: Lower bound $l = \frac{1 + \frac{3.8415}{30} - 1.96 \sqrt{\frac{3.8415}{900}}}{1 + \frac{3.8415}{15}} = \frac{1.1281 - 0.1281}{1.2561} = \frac{1.0}{1.2561} \approx \mathbf{0.7961}$ ($79.61\%$).

### 2.2 Difference in Proportions (Newcombe Hybrid Score Interval)
Standard Wald intervals $\hat{p}_1 - \hat{p}_2 \pm z \cdot \text{SE}$ degenerate to $[0, 0]$ when $\hat{p}_1 = \hat{p}_2 = 1.0$.
The Newcombe Hybrid Score Interval (Method 10) combines the single-arm Wilson bounds $(l_1, u_1)$ and $(l_2, u_2)$:
$$L = \hat{p}_1 - \hat{p}_2 - z \sqrt{\frac{l_1(1-l_1)}{n_1} + \frac{u_2(1-u_2)}{n_2}} = 0 - 1.96 \sqrt{\frac{0.7719(0.2281)}{13} + 0} \approx \mathbf{-0.232}$$
$$U = \hat{p}_1 - \hat{p}_2 + z \sqrt{\frac{u_1(1-u_1)}{n_1} + \frac{l_2(1-l_2)}{n_2}} = 0 + 1.96 \sqrt{0 + \frac{0.7719(0.2281)}{13}} \approx \mathbf{+0.232}$$

---

## 3. Power Analysis & Sample Size Derivations

### 3.1 Simulation Architecture
The power of the study design was evaluated using a 10,000-iteration Monte Carlo simulation under a Randomized Complete Block Design (RCBD) with:
- Multiplicity adjustment via Bonferroni correction: $\alpha_{\text{adjusted}} = \frac{0.05}{3} \approx 0.01667$.
- Intra-cluster correlation coefficient $\rho = 0.10$ modeling task difficulty clustering ($m = 4$ repetitions per task construct).
- Stratified Cochran-Mantel-Haenszel (CMH) test statistic.

### 3.2 Simulation Findings
- **Small Effect ($\Delta = 0.20$, $p = 0.65 \to 0.85$):** Power is **$10.85\%$** ($B=2,000$, MCSE $0.70\%$) and **$11.45\%$** ($B=10,000$, MCSE $0.32\%$).
- **Moderate Effect ($\Delta = 0.35$, $p = 0.50 \to 0.85$):** Power is **$49.65\%$** ($B=2,000$, MCSE $1.12\%$) and **$48.51\%$** ($B=10,000$, MCSE $0.50\%$).
- **Large Disparity ($\Delta = 0.70$, $p = 0.10 \to 0.80$):** Power is **$98.80\%$** ($B=10,000$).

### 3.3 Sample Size Requirements
- **Superiority ($80\%$ Power at $\alpha = 0.05$):**
  - For $\Delta = 0.20$ ($p = 0.65 \to 0.85$): $n = 97$ per arm ($N = 388$ across 4 arms).
  - For $\Delta = 0.20$ ($p = 0.50 \to 0.70$, maximum binomial variance): $n = 125$ per arm ($N = 500$ across 4 arms).
- **Two One-Sided Tests (TOST) Equivalence (Margin $\pm 0.10$ at $\alpha = 0.05$):**
  - For baseline $p = 0.80$: $n = 275$ per arm ($N = 1,100$ across 4 arms).
  - For baseline $p = 0.70$: $n = 360$ per arm ($N = 1,440$ across 4 arms; $1,080$ across 3 arms).
  - For baseline $p = 0.50$: $n = 428$ per arm ($N = 1,716$ across 4 arms).

---

## 4. Methodological Policy on Baseline Pooling

In prior drafts, an attempt was made to pool `BASELINE_ABS` and `BASELINE_REP` based on a non-significant Fisher exact test ($p = 1.000$).
- **Causal Violation:** In causal inference, baseline conditions that manipulate distinct features (relational binding vs text co-location) cannot be pooled post-hoc based on empirical outcomes.
- **Enforced Standard:** In `research_paper_final.tex`, Table 3, Table 4, and all regression test suites, baseline arms remain strictly unpooled.

# CLUSTERING, EXPERIMENTAL UNIT, AND DESIGN EFFECT AUDIT

**Target:** Statistical Modeling of Clustered Trials & Design Effect Formulation  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Experimental Unit vs. Clustering Unit in Web Agent Trials

In web navigation research, confusion often arises regarding the true independent experimental unit:

| Hierarchical Level | Entity in Benchmark | Statistical Role | Independence Justification |
| :--- | :--- | :--- | :--- |
| **Level 1 (Trial)** | Single browser agent run ($Run_{ijk}$) | Observational / Randomization Unit | Assigned treatment arm under fresh browser context and isolated profile. |
| **Level 2 (Task Block)** | Benchmark Task ($T_1 \dots T_5$) | Clustering / Stratification Unit | Repeated runs on identical task share common DOM layout, text ambiguity, and navigation depth. |
| **Level 3 (Target Page)** | Web Application Route (`#home`, etc.) | Macro-Cluster | Shared CSS stylesheet, JavaScript execution engine, and server response latency. |
| **Level 4 (Model / Time)** | API Provider Session | Temporal Cluster | Correlated backend load spikes (e.g., transient HTTP 503 throttling). |

**Primary Inferential Conclusion:** An individual navigation run cannot be assumed purely independent of other runs executing the identical task. Observations within the same task cluster exhibit positive intra-cluster correlation ($\rho > 0$).

---

## 2. Kish Design Effect Formulation

To prevent anti-conservative Type I error inflation, sample sizes must be adjusted by the Design Effect ($\text{DEFF}$):
$$\text{DEFF} = 1 + (m - 1) \cdot \rho$$

Where:
- $m$: Cluster size (number of observations per task per arm).
- $\rho$: Intra-cluster correlation coefficient (ICC).
- Effective sample size: $n_{\text{effective}} = n / \text{DEFF}$.

In the proposed confirmatory RCBD protocol:
- $m = 4$ replicates per task per arm.
- Assumed baseline ICC: $\rho = 0.10$.
$$\text{DEFF} = 1 + (4 - 1) \cdot 0.10 = 1 + 0.30 = \mathbf{1.30}$$

This yields the inflation factor applied to the unadjusted TOST sample size:
$$n_{\text{clustered}} = 360 \times 1.30 = \mathbf{468} \text{ runs per arm}$$

---

## 3. Comprehensive Sensitivity Analysis

Because empirical estimates of $\rho$ vary depending on task complexity and website dynamism, we conducted a sensitivity analysis across plausible cluster sizes ($m \in [4, 8, 16, 20]$) and correlation coefficients ($\rho \in [0.02, 0.05, 0.10, 0.20, 0.30]$):

| Cluster Size ($m$) | ICC ($\rho$) | Design Effect ($\text{DEFF}$) | Effective $n$ at Nominal $n=20$ | Inflated Equivalence $n$/arm ($p=0.70$) | Total Confirmatory Trial Runs ($4$ arms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$m = 4$** | $\rho = 0.02$ | $1.06$ | $18.9$ | $382$ | $1,528$ |
| **$m = 4$** | $\rho = 0.05$ | $1.15$ | $17.4$ | $414$ | $1,656$ |
| **$m = 4$** | **$\rho = 0.10$** | **$1.30$** | **$15.4$** | **$468$** | **$1,872$** |
| **$m = 4$** | $\rho = 0.20$ | $1.60$ | $12.5$ | $576$ | $2,304$ |
| **$m = 4$** | $\rho = 0.30$ | $1.90$ | $10.5$ | $684$ | $2,736$ |
| **$m = 8$** | $\rho = 0.05$ | $1.35$ | $14.8$ | $486$ | $1,944$ |
| **$m = 8$** | $\rho = 0.10$ | $1.70$ | $11.8$ | $612$ | $2,448$ |
| **$m = 8$** | $\rho = 0.20$ | $2.40$ | $8.3$ | $864$ | $3,456$ |
| **$m = 20$** | $\rho = 0.05$ | $1.95$ | $10.3$ | $702$ | $2,808$ |
| **$m = 20$** | $\rho = 0.10$ | $2.90$ | $6.9$ | $1,044$ | $4,176$ |

---

## 4. Modeling Recommendations for Confirmatory Analysis

1. **Stratified Cochran-Mantel-Haenszel (CMH):** When analyzing small, balanced blocks ($m \le 4$), task-stratified CMH provides exact, distribution-free odds ratio and risk difference tests without requiring asymptotic normality within blocks.
2. **Generalized Estimating Equations (GEE):** For larger confirmatory runs ($N \ge 400$), GEE with a logit link and exchangeable working correlation matrix should be used to model cluster dependence directly.
3. **Random-Effects Logistic Regression (GLMM):** A mixed-effects model specifying random intercepts for benchmark tasks ($u_j \sim \mathcal{N}(0, \sigma_{\text{task}}^2)$) allows explicit partitioning of between-task and within-task variance components.
4. **Epistemic Label:** In all manuscript text and audit tables, $\rho = 0.10$ is explicitly designated as an **assumed prior**, not an empirically measured constant.

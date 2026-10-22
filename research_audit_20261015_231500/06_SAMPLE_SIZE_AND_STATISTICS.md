# 06. Sample Size, Run-Count Reconciliation & Statistical Plan

**Audit Directory:** `C:\testing\research_audit_20261015_231500`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Resolution of the Blueprint Run-Count Inconsistency

The proposed blueprint contained an irreconcilable arithmetic contradiction:
- It proposed **6 conditions** (ABS, VIS, ARIA, DATA-DEFAULT, DATA-CFG, JSON-LD) and **6 tasks**.
- It described a **"24-run block"** and proposed a total of **"90 runs"**.

### Forensic Arithmetic Reconciliation
1. **The Origin of the "24-Run Block":**
   $$\text{Block Size} = 6 \text{ tasks} \times 4 \text{ conditions} = 24 \text{ runs per block}$$
   The "24-run block" originated from an earlier **4-arm design** (e.g. 6 tasks × 4 conditions = 24 runs).
2. **The 6-Condition Arithmetic:**
   If 6 conditions are evaluated across 6 tasks, each complete block consists of:
   $$\text{Block Size} = 6 \text{ tasks} \times 6 \text{ conditions} = 36 \text{ runs per block}$$
   Three repetitions would require $36 \times 3 = \mathbf{108\text{ runs}}$, not 90!
3. **The Impossibility of 90 Runs:**
   90 is neither divisible by 24 ($90 / 24 = 3.75$) nor by 36 ($90 / 36 = 2.5$). A 90-run design would leave half of the experimental blocks unbalanced.

### Corrected Concrete Trial Schedules

#### Recommended Option A: Core 4-Arm Defensible Design (Balanced)
- **Conditions ($K = 4$):** ABS, VIS, ARIA, DATA-CFG
- **Tasks ($J = 6$):** 5 retrieval tasks + 1 grounded action task
- **Block Structure:** 1 block = $6 \times 4 = 24$ runs (latin-square or randomized block)
- **Repetitions per cell ($R$):** 4 repetitions per cell ($R = 4$)
- **Total Experimental Runs:**
  $$N = J \times K \times R = 6 \times 4 \times 4 = \mathbf{96\text{ runs}}$$
  *(Or with $R = 5$ repetitions: $6 \times 4 \times 5 = \mathbf{120\text{ runs}}$)*

#### Option B: Full 6-Arm Design (If Augmented JSON-LD & DATA-DEFAULT are kept)
- **Conditions ($K = 6$):** ABS, VIS, ARIA, DATA-DEFAULT, DATA-CFG, JSON-LD-AUGMENTED
- **Tasks ($J = 6$):** 6 tasks
- **Block Structure:** 1 block = $6 \times 6 = 36$ runs
- **Repetitions ($R = 3$):** $36 \times 3 = \mathbf{108\text{ runs}}$
- **Repetitions ($R = 4$):** $36 \times 4 = \mathbf{144\text{ runs}}$

---

## 2. Statistical Power Audit & Calculation

Using local offline scientific computation (`scipy.stats`), we audited statistical power across realistic effect sizes for binary fact retrieval accuracy ($Y \in \{0, 1\}$):

### Table 1: Exact Statistical Power Calculations ($\alpha = 0.05$, Two-Sided)

| Scenario / Contrast | Expected $P_1$ | Expected $P_2$ | Effect Size ($\Delta$) | Required $N$ per Arm ($80\%$ Power) | Required $N$ per Arm ($90\%$ Power) | Power at $N=15$ ($60$ Total) | Power at $N=24$ ($96$ Total) | Power at $N=30$ ($120$ Total) |
|---|---|---|---|---|---|---|---|---|
| **Negative Control vs Channel** (ABS vs VIS) | 0.10 | 0.80 | **0.70** | **7** | **9** | **99.6%** | **>99.9%** | **>99.9%** |
| **Large Channel Effect** (VIS vs ARIA) | 0.90 | 0.50 | **0.40** | **20** | **26** | **68.4%** | **87.8%** | **94.3%** |
| **Moderate Channel Effect** (VIS vs DATA-CFG) | 0.85 | 0.60 | **0.25** | **49** | **65** | **32.8%** | **49.1%** | **58.6%** |
| **Small Channel Effect** (ARIA vs DATA-CFG) | 0.85 | 0.70 | **0.15** | **121** | **161** | **16.1%** | **23.3%** | **28.2%** |

### Statistical Power Conclusions
1. **Pilot / Calibration Designation:** A sample size of $N = 96$ ($N = 24$ per condition) or $N = 120$ ($N = 30$ per condition) has **adequate power ($>85\%$) only to detect large effects ($\Delta \ge 0.40$)** or presence vs absence ($\Delta \ge 0.70$).
2. **Underpowered for Subtleties:** It has $<50\%$ power for moderate differences ($\Delta = 0.25$) and $<25\%$ power for subtle equivalence ($\Delta \le 0.15$).
3. **Scientific Claim Constraint:** The paper must **not** claim to confirm that ARIA and `data-*` are "equivalent" to visible text if no significant difference is found; rather, it must report that the study was calibrated to detect substantial retrieval degradation ($\ge 40\%$) and set an upper bound on effect sizes via confidence intervals.

---

## 3. Formal Statistical Analysis Plan

### 1. Outcomes
- **Primary Outcome:** Binary Retrieval Correctness ($Y_{ijk} \in \{0, 1\}$). 1 if extracted fact matches ground truth exactly, 0 otherwise.
- **Secondary Outcomes:**
  - Trajectory Step Count ($S_{ijk} \in \mathbb{N}^+$)
  - Wall-Clock Execution Time ($T_{ijk} \in \mathbb{R}^+$ seconds)
  - Model Request / Token Overhead

### 2. Experimental Unit & Clustered Dependence
- The experimental unit is the **single trial** ($i$), nested within Task ($j$) and Block ($b$).
- Because trials sharing the same task are not independent, standard chi-square or independent-samples tests are invalid.

### 3. Primary Model: Generalized Linear Mixed Model (GLMM)
$$\text{logit}(P(Y_{ijb} = 1)) = \beta_0 + \sum_{k=1}^{K-1} \beta_k \cdot \text{Condition}_{k} + u_j + v_b$$
Where:
- $\text{Condition}_k$ are treatment indicators (with $VIS$ as reference).
- $u_j \sim \mathcal{N}(0, \sigma_u^2)$ is the random intercept for Task ($j = 1 \dots 6$).
- $v_b \sim \mathcal{N}(0, \sigma_v^2)$ is the random intercept for Execution Block ($b = 1 \dots R$).

### 4. Pairwise Contrasts & Multiplicity Correction
- Pre-planned orthogonal contrasts:
  1. $\text{VIS}$ vs $\text{ABS}$ (Validation of task sensitivity)
  2. $\text{ARIA}$ vs $\text{VIS}$ (Human vs accessibility channel)
  3. $\text{DATA-CFG}$ vs $\text{VIS}$ (Human vs machine attribute channel)
  4. $\text{DATA-CFG}$ vs $\text{ARIA}$ (Machine attribute vs accessibility channel)
- Family-Wise Error Rate (FWER) controlled at $\alpha = 0.05$ using **Holm-Bonferroni correction**.

### 5. Missing Data & Prespecified Stopping Rule
- **Zero Selective Retries:** An infrastructure or domain failure is recorded truthfully. Runs are never selectively retried until they succeed.
- **Quota Circuit Breaker:** If two consecutive runs fail with HTTP 429 (`RESOURCE_EXHAUSTED`), the runner immediately pauses and halts. The remaining runs are recorded as truncated, and sensitivity analyses (worst-case and best-case imputation) are reported.

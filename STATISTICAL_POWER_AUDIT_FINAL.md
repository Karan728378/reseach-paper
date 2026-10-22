# Statistical Power and Experimental Analysis Plan: Final Audit & Derivations

**Document Version:** 1.0 (Comprehensive Statistical Power Audit)  
**Date:** October 22, 2026  
**Auditor:** Antigravity Biostatistics & Statistical Review Team  
**Compliance Status:** 100% Offline · Exact Hypergeometric & Monte Carlo Validated  
**Script & Artifacts:** [`reproduce_power_audit.py`](file:///C:/testing/research_execution_20261018/reproduce_power_audit.py) · [`power_audit_results.json`](file:///C:/testing/research_execution_20261018/power_audit_results.json) · [`test_power_audit.py`](file:///C:/testing/research_execution_20261018/test_power_audit.py)  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Experimental Design Architecture

The planned evaluation is a **Task-Stratified Randomized Complete Block Design (RCBD)**:
- **Unit of Randomization:** Individual task trial execution order within block.
- **Unit of Observation:** A single task trial attempt yielding binary task success $Y_{ijk} \in \{0, 1\}$.
- **Blocking Factor ($R=4$):** Four sequential execution blocks ($k \in \{1, 2, 3, 4\}$).
- **Task Strata ($J=5$):** Five primary benchmark tasks (T1–T5) spanning distinct operational demands and difficulty baselines.
- **Treatment Factor ($K=4$):** Four treatment arms (`BASELINE`, `BASELINE_REP`, `ARIA`, `DATA-CFG`).
- **Schedule Allocations:**
  - Full Experimental Schedule: $4 \text{ arms} \times 6 \text{ tasks} \times 4 \text{ blocks} = \mathbf{N = 96}$ runs.
  - Primary Grounded Benchmark: $4 \text{ arms} \times 5 \text{ tasks} \times 4 \text{ blocks} = \mathbf{N = 80}$ runs.
  - Per-Arm Primary Allocation: $n = 20$ runs ($4$ runs per task stratum).
  - Secondary Exploratory Probe: $4 \text{ arms} \times 1 \text{ task (T6)} \times 4 \text{ blocks} = \mathbf{N_{\text{probe}} = 16}$ runs.

---

## 2. Estimands, Hypotheses, and Baseline Pooling

### 2.1 Primary Estimand: Stratified Risk Difference
The primary estimand is the common risk difference across the $J=5$ primary task strata:
$$\Delta = P(Y=1 \mid \text{Treatment}) - P(Y=1 \mid \text{Baseline})$$
Evaluated via the **Task-Stratified Cochran-Mantel-Haenszel (CMH) test** with continuity correction.

### 2.2 Planned Contrasts & Multiplicity Correction
Three confirmatory pairwise contrasts against baseline:
1. $H_{1\text{A}}$: $\text{ARIA} \text{ vs. } \text{BASELINE}$
2. $H_{1\text{B}}$: $\text{DATA-CFG} \text{ vs. } \text{BASELINE}$
3. $H_{1\text{C}}$: $\text{ARIA} \text{ vs. } \text{DATA-CFG}$

To control the family-wise error rate (FWER) at nominal $\alpha = 0.05$, a Bonferroni correction is applied:
$$\alpha_{\text{adj}} = \frac{0.05}{3} \approx \mathbf{0.0167} \quad (z_{\alpha_{\text{adj}}/2} \approx 2.3925)$$

### 2.3 Scientific Audit of Baseline Pooling & Stability Rule
- **The Rule:** The protocol pools `BASELINE` (ABS) and `BASELINE_REP` (VIS) into a single composite baseline of $n_{\text{base}} = 40$ primary trials, conditional on an internal stability test:
  $$H_{\text{stab}}: P(Y=1 \mid \text{ABS}) = P(Y=1 \mid \text{VIS}) \quad \text{evaluated via Fisher's exact test at } \alpha_{\text{stab}} = 0.10$$
- **Critical Methodological Limitation:**  
  *Failing to reject the null ($p_{\text{stab}} \ge 0.10$) does NOT prove that the baseline is stable or that conditions are identical.* With $n=20$ per arm, the stability test itself is underpowered ($\approx 15\%$ power to detect a 20-point drift). Pooling must be recognized as an assumption of design equivalence (both conditions present identical HTML and default serializer options), not an empirically proven equality.
- **Contingency:** If $p_{\text{stab}} < 0.10$, baseline pooling is aborted, and arms are evaluated as a 4-group unpooled design ($n=20$ each), reducing power from $10.85\%$ to $\mathbf{7.21\%}$.

---

## 3. Power Derivations: Independent Binomial vs. Stratified RCBD

Using exact hypergeometric distributions and Monte Carlo simulations ($B = 2,000$ iterations) implemented in [`reproduce_power_audit.py`](file:///C:/testing/research_execution_20261018/reproduce_power_audit.py):

| Shift Scenario | Underlying Shift ($\Delta$) | Model A: Unstratified Independent Binomial ($N=40 \text{ vs } 20$, $\alpha=0.0167$) | Model B: Planned Task-Stratified RCBD (CMH) ($J=5, n_{\text{cell}}=4 \text{ vs } 8$) | Methodological Implication |
|---|:---:|:---:|:---:|---|
| **Large Disparity** | $\Delta = 0.70$ ($0.10 \to 0.80$) | **$99.91\%$** | **$98.54\%$** (MC: $98.8\% \pm 0.2\%$) | Adequately powered under both models. |
| **Moderate Effect** | $\Delta = 0.35$ ($0.50 \to 0.85$) | **$65.10\%$** | **$49.63\%$** (MC: $49.7\% \pm 1.1\%$) | 50% risk of Type II error even for large shifts. |
| **Small Effect** | $\Delta = 0.20$ ($0.70 \to 0.90$) | **$19.82\%$** | **$10.85\%$** (MC: $10.8\% \pm 0.7\%$) | **Severely underpowered ($\beta = 89.15\%$).** |
| **Subtle Difference** | $\Delta = 0.15$ ($0.70 \to 0.85$) | **$9.91\%$** | **$5.80\%$** (MC: $5.8\% \pm 0.5\%$) | Inconclusive; near nominal alpha ($1.67\%$). |

### Why Power Drops in the RCBD Model:
1. **Task Heterogeneity:** Tasks have widely varying baseline difficulties: T1 ($0.70$), T2 ($0.85$), T3 ($0.50$), T4 ($0.30$), T5 ($0.80$).
2. **Ceiling Compression:** For Task T2 (baseline $0.85$), a $+0.20$ shift hits the probability boundary ($0.95$). The maximum observable shift is constrained to $+0.10$.
3. **Small Stratum Sizes:** With $n=4$ treatment runs per task stratum, discrete cell variance suppresses the power of the CMH test relative to continuous asymptotic assumptions.

---

## 4. Minimum Detectable Effect Sizes (MDES)

Under the planned $N = 96$ design ($n = 20$ runs per treatment arm, $n_{\text{base}} = 40$, Bonferroni $\alpha = 0.0167$):
- **MDES for $80\%$ Power ($\beta = 0.20$):**
  $$\Delta_{\text{MDES}} \approx \mathbf{0.48 \text{ to } 0.52}$$
- **Interpretation:** The $N = 96$ pilot can reliably detect **only massive performance differences ($\ge 48$ percentage points)**. Any effect smaller than $0.48$ will likely produce a non-significant result ($p \ge 0.0167$).

---

## 5. Sample Size Requirements for Confirmatory Science

### 5.1 Superiority Testing ($\Delta = 0.20$, $80\%$ Power, $\alpha = 0.0167$)
Using the standard two-sample formula with pooled variance:
$$n = \frac{\left(z_{\alpha/2}\sqrt{2\bar{p}\bar{q}} + z_\beta\sqrt{p_1 q_1 + p_2 q_2}\right)^2}{\Delta^2}$$

- **Scenario 1 (Maximum Variance, $p_{\text{base}} = 0.50 \to 0.70$):**  
  Requires **$n \ge 125$ per arm** ($\mathbf{N \ge 500}$ across 4 arms, or $N \ge 480$ with 2:1 baseline pooling).
- **Scenario 2 (High Baseline, $p_{\text{base}} = 0.70 \to 0.90$):**  
  Requires **$n \ge 83$ per arm** ($\mathbf{N \ge 332}$ across 4 arms).
- **Scenario 3 (Clustered RCBD with $\rho_{\text{task}} = 0.05$, $\text{DEFF} = 1.15$):**  
  Requires **$n \ge 144$ per arm** ($\mathbf{N \ge 576}$ across 4 arms).

### 5.2 Equivalence Testing (TOST Margin $\delta = \pm 0.10$, $80\%$ Power, $\alpha = 0.05$)
Testing two one-sided null hypotheses ($H_{01}: \Delta \le -0.10$ and $H_{02}: \Delta \ge +0.10$):
$$n \approx \frac{2(z_\alpha + z_{\beta/2})^2 p(1-p)}{\delta^2}$$
- **Scenario 1 (Baseline $p = 0.70$):**  
  Requires **$n \ge 340 \text{ to } 360$ per arm** ($\mathbf{N \ge 1,360 \text{ to } 1,440}$ across 4 arms).
- **Scenario 2 (Baseline $p = 0.50$):**  
  Requires **$n \ge 429$ per arm** ($\mathbf{N \ge 1,716}$ across 4 arms).

---

## 6. Mandatory Non-Equivalence Rule (Preregistered Constraint)

> [!CAUTION]
> **Strict Methodological Prohibition:**  
> Because the statistical power of the $N = 96$ design is under $11\%$ for small-to-moderate effects ($\Delta \le 0.20$), **a failure to reject the null hypothesis ($p \ge 0.0167$) CANNOT and MUST NOT be claimed as evidence of "channel equivalence" or proof that semantic markup provides no benefit.**  
> Any non-significant contrast must be reported strictly as **statistically inconclusive due to sample size constraints**.

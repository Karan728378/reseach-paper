# TOST EQUIVALENCE SAMPLE SIZE AUDIT & DERIVATION

**Document Type:** Statistical Methodology Audit & Mathematical Derivation  
**Audited Target:** Section 6.3 of `research_paper_final.tex` and `reproduce_power_audit.py`  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Statistical Formulation of Equivalence

The proposed confirmatory protocol evaluates whether alternative DOM observation pipelines (ARIA accessibility trees, DATA-CFG attribute whitelisting) achieve practical equivalence to the baseline DOM observation pipeline.

### Hypotheses (Two One-Sided Tests — Schuirmann 1987)
For a specified equivalence margin $\delta > 0$:
$$H_{01}: p_{\text{treatment}} - p_{\text{control}} \le -\delta \quad \text{vs.} \quad H_{11}: p_{\text{treatment}} - p_{\text{control}} > -\delta$$
$$H_{02}: p_{\text{treatment}} - p_{\text{control}} \ge +\delta \quad \text{vs.} \quad H_{12}: p_{\text{treatment}} - p_{\text{control}} < +\delta$$

Equivalence is concluded at significance level $\alpha$ if and only if both null hypotheses $H_{01}$ and $H_{02}$ are rejected simultaneously. This is operationally identical to requiring that the $(1 - 2\alpha) \times 100\%$ two-sided confidence interval for the risk difference lies entirely within the equivalence bounds $(-\delta, +\delta)$.

---

## 2. Closed-Form Sample Size Derivation

Assuming equal sample allocation ($n_1 = n_2 = n$), baseline success probability $p$, true risk difference $\Delta = 0$, and normal approximation to the binomial distribution:

$$n = \frac{(z_{1-\alpha} + z_{(1+\text{Power})/2})^2 \cdot 2 p (1-p)}{\delta^2}$$

Where:
- $\delta = 0.10$ (ten percentage points equivalence boundary).
- $\text{Power} = 1 - \beta = 0.80$.
- For joint power of $80\%$ across both one-sided tests, each tail quantile uses $z_{(1+0.80)/2} = z_{0.90} = 1.28155$.
- For standard one-sided test level $\alpha = 0.05$ (corresponding to a 90% confidence interval):
  $$z_{1-\alpha} = z_{0.95} = 1.64485$$
  $$(z_{0.95} + z_{0.90})^2 = (1.64485 + 1.28155)^2 = (2.9264)^2 = 8.5638$$

### Primary Sample Size Results
1. **At Baseline $p = 0.70$:**
   $$\text{Variance factor} = 2 \cdot (0.70) \cdot (0.30) = 0.42$$
   $$n = \frac{8.5638 \cdot 0.42}{(0.10)^2} = \frac{3.5968}{0.01} = \mathbf{359.68} \approx \mathbf{360} \text{ runs per arm}$$
   Total sample size across a 4-arm design: $4 \times 360 = \mathbf{1,440} \text{ runs}$.

2. **At Maximum Variance ($p = 0.50$):**
   $$\text{Variance factor} = 2 \cdot (0.50) \cdot (0.50) = 0.50$$
   $$n = \frac{8.5638 \cdot 0.50}{0.01} = \mathbf{428.19} \approx \mathbf{429} \text{ runs per arm}$$
   Total sample size across a 4-arm design: $4 \times 429 = \mathbf{1,716} \text{ runs}$.

3. **Cluster-Inflated Sample Size ($\text{DEFF} = 1.30$ at $p = 0.70$):**
   $$n_{\text{clustered}} = n \cdot \text{DEFF} = 359.68 \cdot 1.30 = \mathbf{467.58} \approx \mathbf{468} \text{ runs per arm}$$
   Total clustered sample size across 4 arms: $4 \times 468 = \mathbf{1,872} \text{ runs}$.

---

## 3. Multiple Comparison Sensitivity (Bonferroni Adjustment)

If familywise error rate across 3 planned pairwise contrasts is controlled at $\alpha = 0.05 / 3 = 0.016667$:
- $z_{1 - \alpha_{\text{adj}}} = z_{0.98333} = 2.12805$
- $(z_{0.98333} + z_{0.90})^2 = (2.12805 + 1.28155)^2 = (3.4096)^2 = 11.6254$

| Baseline $p$ | Unadjusted ($\alpha=0.05$) $n$/arm | Unadjusted Total ($4$ arms) | Bonferroni ($\alpha=0.0167$) $n$/arm | Bonferroni Total ($4$ arms) | Clustered ($\text{DEFF}=1.30$) $n$/arm |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$p = 0.80$** | 274 | 1,096 | 372 | 1,488 | 484 |
| **$p = 0.75$** | 321 | 1,284 | 436 | 1,744 | 567 |
| **$p = 0.70$** | **360** | **1,440** | **489** | **1,956** | **636** |
| **$p = 0.65$** | 390 | 1,560 | 530 | 2,120 | 689 |
| **$p = 0.50$** | **429** | **1,716** | **582** | **2,328** | **757** |

---

## 4. Methodological Findings & Recommendations

1. **Exact Alignment:** The manuscript numbers ($n=360$, $n=429$, and $n=468$) correspond precisely to the standard Schuirmann formulation at $\alpha=0.05$ (two-sided 90% confidence interval) with baseline rates $p=0.70$ and $p=0.50$, and Kish cluster inflation factor $1.30$.
2. **Conservative Nature:** Because equivalence testing requires establishing bounds within a narrow $\pm 10\%$ band, sample sizes are substantially larger than standard superiority testing. The confirmatory trial requires $\ge 1,440$ runs to establish equivalence rigorously.
3. **Finite Pilot Limitation:** This derivation formally proves why the 41-run cloud pilot ($n \le 15$/arm) cannot be used to conclude equivalence.

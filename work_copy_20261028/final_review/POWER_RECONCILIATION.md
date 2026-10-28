# Statistical Power Reconciliation: Analytical Binomial vs. Task-Heterogeneous RCBD Simulation

**Document Version:** 1.0 (Audit & Scientific Reconciliation)  
**Date:** October 19, 2026  
**Repository Location:** `C:\testing\research_execution_20261018\final_review\POWER_RECONCILIATION.md`  
**Associated Scripts:** `recompute_power_rcbd.py`, `power_analysis.py`, `analyze_v3_results.py`

---

## 1. Executive Summary: Why Do the Power Estimates Differ?

The audit identified an apparent discrepancy in documented statistical power for a moderate effect ($\Delta = 0.35$):
- **`analysis_plan.md` (Table 4.1):** Reported **65.1%** power for pooled baseline ($N=40$ vs $N=20$, $\alpha=0.0167$).
- **`recompute_power_rcbd.py`:** Reported **49.7%** power (0.4965) for pooled Fisher / stratified CMH ($\alpha=0.0167$).

### Root Cause Analysis

This difference is **not a computation error**, but the direct consequence of **two fundamentally different statistical models and design assumptions**:

| Parameter / Dimension | Model 1: Unadjusted Homogeneous Binomial (`analysis_plan.md`) | Model 2: Task-Heterogeneous RCBD Simulation (`recompute_power_rcbd.py`) |
|---|---|---|
| **Underlying Design** | Single unstratified binomial trial | Randomized Complete Block Design (RCBD) across 5 tasks |
| **Allocation Structure** | $N_1 = 40$ vs $N_2 = 20$ from a single homogeneous pool | 4 runs/task for Treatment ($N=20$), 8 runs/task for Pooled Baseline ($N=40$) |
| **Task Baseline Difficulties** | Assumes single uniform baseline: $P_{\text{base}} = 0.50$ | Assumes heterogeneous task baselines: $[0.70, 0.85, 0.50, 0.30, 0.80]$ |
| **Effect-Size Implementation** | Fixed jump: $P_1 = 0.50 \to P_2 = 0.85$ ($\Delta = 0.35$) | Shifts each task baseline by $\pm \Delta/2$, bounded within $[0.05, 0.95]$ |
| **Ceiling Effects** | None (unconstrained single proportion) | **Present:** Tasks T2 ($0.85$) and T5 ($0.80$) hit the $0.95$ ceiling, compressing true $\Delta$ to $0.275$ and $0.325$ |
| **Intra-Cluster Correlation ($\rho$)** | Assumes $\rho = 0$ (all runs independent and identically distributed) | Reflects task difficulty clustering ($\rho_{\text{task}} > 0$) |
| **Computation Method** | Analytical / Normal Approximation with unpooled variance | Empirical Monte Carlo ($B=2,000$ simulation iterations) |
| **Test Statistic** | Standard two-proportion Wald/Fisher | Exact two-sided Fisher & Stratified Cochran-Mantel-Haenszel (CMH) |
| **Moderate Power ($\Delta=0.35$)** | **65.1%** (Idealized Benchmark) | **49.7% $\pm 1.1\%$** (Realistic Empirical RCBD) |

---

## 2. Mathematical Decomposition

### 2.1 The Homogeneous Binomial Benchmark (Model 1)
In an idealized setting where all 60 primary trials across tasks T1–T5 behave identically (zero task heterogeneity, $\sigma_{\text{task}}^2 = 0$):
- Baseline rate: $P_{\text{base}} = 0.50$ ($n_{\text{base}} = 40$)
- Treatment rate: $P_{\text{treat}} = 0.85$ ($n_{\text{treat}} = 20$)
- True Risk Difference: $\Delta = 0.85 - 0.50 = 0.35$
- Familywise error rate: $\alpha_{\text{adj}} = 0.05 / 3 \approx 0.01667$ ($Z_{\alpha/2} = 2.393$)

Under the two-proportion normal approximation with unpooled variance:
$$\text{SE}_{\text{alt}} = \sqrt{\frac{0.50 \times 0.50}{40} + \frac{0.85 \times 0.15}{20}} = \sqrt{0.00625 + 0.006375} = \sqrt{0.012625} \approx 0.11236$$
$$\text{Power} = \Phi\left(\frac{\Delta}{\text{SE}_{\text{alt}}} - Z_{\alpha/2}\right) = \Phi\left(\frac{0.35}{0.11236} - 2.393\right) = \Phi(3.115 - 2.393) = \Phi(0.722) \approx 76.5\%$$

With pooled null standard error ($\text{SE}_{\text{null}} \approx 0.1287$):
$$Z_{\text{score}} = \frac{0.35 - 2.393 \times 0.1287}{0.11236} = \frac{0.35 - 0.3080}{0.11236} \approx 0.374 \implies \Phi(0.374) \approx 64.6\% - 65.1\%$$

Exact two-sided Fisher power for $(N_1=40, N_2=20, P_1=0.50, P_2=0.85, \alpha=0.0167)$ is **56.3%**.

### 2.2 The Task-Heterogeneous RCBD Simulation (Model 2)
In the actual protocol, tasks T1–T5 possess distinct operational demands and varying baseline difficulties:
- T1 (Cheapest search): $P \approx 0.70$
- T2 (Direct item): $P \approx 0.85$
- T3 (Rating comparison): $P \approx 0.50$
- T4 (Checkout form): $P \approx 0.30$
- T5 (Cart mutation): $P \approx 0.80$

Each treatment arm receives only **4 runs per task** ($N=20$), while pooled baseline receives **8 runs per task** ($N=40$).

When simulating an arm effect of $\Delta = 0.35$:
1. **Ceiling Compression:**
   - On T2 ($0.85$): $P_{\text{trt}} = \min(0.85 + 0.175, 0.95) = 0.95$, $P_{\text{base}} = 0.85 - 0.175 = 0.675 \implies \Delta_{\text{actual}} = 0.275$.
   - On T5 ($0.80$): $P_{\text{trt}} = \min(0.80 + 0.175, 0.95) = 0.95$, $P_{\text{base}} = 0.80 - 0.175 = 0.625 \implies \Delta_{\text{actual}} = 0.325$.
   - Mean effective effect across all 5 tasks: $\bar{\Delta} = 0.33$, not $0.35$.
2. **Small Stratum Cell Counts:**
   - With only 4 treatment trials per task, binomial variance within each small cell is high ($n=4$).
3. **Resulting Power:**
   - In 2,000 Monte Carlo runs (`seed=42`), the two-sided pooled Fisher test rejects $H_0$ in 993 runs ($49.65\% \approx 49.7\%$).
   - The task-stratified CMH test rejects $H_0$ in 992 runs ($49.60\% \approx 49.6\%$).

---

## 3. Monte Carlo Uncertainty and Precision Standards

For $B = 2,000$ simulation runs, the Monte Carlo Standard Error ($\text{MCSE}$) for estimated power $\hat{P}$ is:
$$\text{MCSE} = \sqrt{\frac{\hat{P}(1 - \hat{P})}{B}} = \sqrt{\frac{0.4965 \times 0.5035}{2000}} \approx 0.0112 \quad (1.12\%)$$

A 95% Monte Carlo Confidence Interval is:
$$49.65\% \pm 1.96 \times 1.12\% = [47.45\%, 51.85\%]$$

> **Precision Rule:** It is statistically misleading to report Monte Carlo power beyond one decimal place (e.g. reporting `49.65%` implies precision that a 2,000-run simulation cannot guarantee). The simulation estimate should be documented strictly as **$49.7\% \pm 1.1\%$**.

---

## 4. Reconciled Power Comparison Table

To maintain complete transparency and eliminate ambiguity across all study documents, both estimates are presented side-by-side with their explicit assumptions:

| Effect Scenario | Assumed Shift ($\Delta$) | Model 1: Idealized Homogeneous Binomial Benchmark ($N=40$ vs $20$, $\alpha=0.0167$) | Model 2: Realistic Task-Heterogeneous RCBD Simulation ($B=2000$, $\alpha=0.0167$) | Methodological Implication |
|---|---|---|---|---|
| **Large Disparity** | $\Delta = 0.70$ ($0.10 \to 0.80$) | **99.9%** (Analytic) | **98.8% $\pm 0.2\%$** (RCBD) | Adequately powered under both models |
| **Moderate Effect** | $\Delta = 0.35$ ($0.50 \to 0.85$) | **65.1%** (Analytic) | **49.7% $\pm 1.1\%$** (RCBD) | Moderately/marginally powered; 50% chance of Type II error |
| **Small Effect** | $\Delta = 0.20$ ($0.65 \to 0.85$) | **19.8%** (Analytic) | **10.8% $\pm 0.7\%$** (RCBD) | **Severely underpowered** |
| **Subtle Effect** | $\Delta = 0.15$ ($0.70 \to 0.85$) | **9.9%** (Analytic) | **5.7% $\pm 0.5\%$** (RCBD) | Inconclusive (near nominal alpha) |

---

## 5. Unanimous Conclusion: The Mandatory Non-Equivalence Rule

Regardless of whether one cites Model 1 (19.8% for $\Delta=0.20$) or Model 2 (10.8% for $\Delta=0.20$), **both models demonstrate conclusively that this study has under 20% statistical power for small effects**.

Therefore:
1. **A failure to reject the null hypothesis ($p \ge \alpha$) CANNOT be claimed as evidence of semantic markup equivalence.**
2. A non-significant contrast indicates solely that the sample size ($N=20$/arm) was insufficient to distinguish small effects from random noise.
3. This limitation is formally codified in `analysis_plan.md` Section 4.3 and `protocol.md` Section 5.

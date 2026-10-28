# STATISTICAL POWER ANALYSIS REPRODUCTION REPORT

**Script Executed:** `reproduce_power_audit.py` & `scratch/independent_power_check.py`  
**Output Records:** `power_audit_results.json`  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  
**Verification Method:** Exact closed-form hypergeometric testing and Monte Carlo simulation ($B=2,000$ and $B=10,000$ replications)  

---

## 1. Experimental Design & Data-Generating Process

The proposed Randomized Complete Block Design (RCBD) evaluates web agent performance across heterogeneous task benchmarks.
- **Primary Benchmark Tasks:** 5 tasks ($T_1, T_2, T_3, T_4, T_5$) with baseline success rates $p_0 \in [0.70, 0.85, 0.50, 0.30, 0.80]$ (mean baseline $p = 0.63$).
- **Allocation:** 4 replicates per task per arm $\implies n = 20$ runs per treatment arm ($N=80$ primary benchmark observations across 4 arms).
- **Pooled Baseline Arm:** Control arms ABS (standard DOM) and VIS (visual observation) pooled to yield $n = 40$ baseline observations.
- **Planned Pairwise Contrasts:** 3 confirmatory contrasts:
  1. ARIA vs. Pooled Baseline
  2. DATA-CFG vs. Pooled Baseline
  3. ARIA vs. DATA-CFG
- **Multiplicity Correction:** Bonferroni familywise error control at FWER $\alpha = 0.05 \implies \alpha_{\text{adj}} = 0.05 / 3 = 0.016667$.

---

## 2. Monte Carlo Simulation Results & Power Curve

Two independent simulation engines were evaluated using seed 42:
1. **Primary Project Harness (`reproduce_power_audit.py`, $B=2,000$ reps)**
2. **High-Precision Audit Harness (`scratch/independent_power_check.py`, $B=10,000$ reps)**

| Effect Size ($\Delta$) | Description / Effect Scale | Analytical Power ($n=20$ vs $40$, $\alpha=0.0167$) | Simulated Stratified CMH Power ($B=2,000$) | Simulated Stratified CMH Power ($B=10,000$) | Monte Carlo SE ($B=10,000$) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **$\Delta = 0.70$** | Massive architectural failure | $99.99\%$ | $98.55\%$ | **$98.77\%$** | $\pm 0.11\%$ |
| **$\Delta = 0.35$** | Moderate effect size | $60.93\%$ | $49.60\%$ | **$48.51\%$** | $\pm 0.50\%$ |
| **$\Delta = 0.20$** | Small effect size | $19.23\%$ | $10.85\%$ | **$11.45\%$** | $\pm 0.32\%$ |
| **$\Delta = 0.15$** | Subtle / near-threshold effect | $10.71\%$ | $5.80\%$ | **$5.58\%$** | $\pm 0.23\%$ |

### Scientific Verdict on Pilot Sample Size ($n=20$)
- At $n=20$ runs per arm, the study possesses only **$\approx 11\%$ statistical power** to detect a risk difference of $\Delta = 0.20$ at the Bonferroni-corrected significance threshold ($\alpha = 0.0167$).
- Even for a substantial moderate effect ($\Delta = 0.35$), power is under **$50\%$**, meaning a real effect would fail to reach statistical significance more than half the time.
- **Critical Conclusion:** Any non-significant difference observed in an exploratory pilot of $N \le 20$/arm cannot be interpreted as evidence of treatment equivalence or absence of an effect.

---

## 3. Manuscript Reconciliation & Wording Corrections

1. **Abstract Wording Aligned:** An earlier draft ambiguously labeled $\Delta = 0.20$ as a "moderate effect." Conventional statistical taxonomy (Cohen 1988) categorizes $\Delta = 0.20$ as a small-to-moderate proportion shift and $\Delta = 0.35$ as moderate. The text now clearly states: *“At $n=20$ per arm, statistical power for detecting a small effect ($\Delta = 0.20$) is only $10.8\%$ to $11.5\%$ at $\alpha = 0.0167$, rising to $48.5\%$–$49.6\%$ for a moderate effect ($\Delta = 0.35$).”*
2. **Determinism & Regression Tests:** Added automated regression test `test_power_audit.py` to assert monotonic power growth, analytical validity, and JSON schema integrity.

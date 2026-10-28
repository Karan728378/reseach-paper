# CONFIDENCE INTERVALS, MULTIPLICITY, AND ESTIMANDS AUDIT

**Target:** Audit of Proportions, Score Intervals, Difference Metrics, and Familywise Error Control  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Single-Proportion Wilson Score Intervals

The standard Wald interval ($p \pm z\sqrt{p(1-p)/n}$) exhibits poor coverage properties near extreme boundaries ($p \approx 0$ or $p \approx 1$) and fails completely when $p = 1.0$ (collapsing to an impossible zero-width interval). All proportions in the manuscript are calculated using the Wilson (1927) score interval:

$$\text{CI}_{\text{Wilson}} = \frac{p + \frac{z^2}{2n} \pm z\sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

Where $z = 1.95996$ for a two-sided $95\%$ confidence level.

### Primary Audit Calculations
| Fraction | Context / Description | Sample Estimate | Wilson $95\%$ Confidence Interval | Inferential Interpretation |
| :---: | :--- | :---: | :---: | :--- |
| **$27 / 34$** | Framework Operational Selector-Map Census (Route `#home`) | $79.41\%$ | **$[63.20\%, 89.65\%]$** | Descriptive census of single route; Wilson CI models hypothetical superpopulation of similar e-commerce layouts. |
| **$27 / 27$** | Semantic Interactive Control Correspondence | $100.00\%$ | **$[87.54\%, 100.00\%]$** | Zero false negatives among genuine interactive controls. |
| **$41 / 41$** | Total Cloud Pilot Completed Runs | $100.00\%$ | **$[91.43\%, 100.00\%]$** | Acute ceiling effect; risk difference $\hat{\theta} = 0.00$. |
| **$13 / 13$** | Pilot Baseline (ABS) Arm Completed Runs | $100.00\%$ | **$[77.19\%, 100.00\%]$** | Bounded pilot sample; small-sample uncertainty. |
| **$13 / 13$** | Pilot ARIA Arm Completed Runs | $100.00\%$ | **$[77.19\%, 100.00\%]$** | Indistinguishable from baseline under simple tasks. |
| **$15 / 15$** | Pilot Attribute Whitelist (DATA-CFG) Arm | $100.00\%$ | **$[79.61\%, 100.00\%]$** | Indistinguishable from baseline under simple tasks. |

---

## 2. Newcombe Hybrid-Score Risk Difference Interval

For two independent proportions $p_1 = x_1/n_1$ and $p_2 = x_2/n_2$, the Newcombe (1998) hybrid-score method combines the individual Wilson score boundaries $(l_1, u_1)$ and $(l_2, u_2)$:

$$\text{Lower Limit} = (p_1 - p_2) - \sqrt{(p_1 - l_1)^2 + (u_2 - p_2)^2}$$
$$\text{Upper Limit} = (p_1 - p_2) + \sqrt{(u_1 - p_1)^2 + (p_2 - l_2)^2}$$

### Methodological Example Verification ($56/70$ vs. $38/80$)
- $x_1 = 56, n_1 = 70 \implies p_1 = 0.8000$, Wilson $95\%$ CI: $[0.6918, 0.8770]$
- $x_2 = 38, n_2 = 80 \implies p_2 = 0.4750$, Wilson $95\%$ CI: $[0.3692, 0.5830]$
- Point Estimate: $\hat{\Delta} = p_1 - p_2 = 0.8000 - 0.4750 = \mathbf{0.3250}$ ($32.5\%$)
- Calculation:
  $$\text{Lower} = 0.3250 - \sqrt{(0.8000 - 0.6918)^2 + (0.5830 - 0.4750)^2} = 0.3250 - \sqrt{0.011707 + 0.011664} = \mathbf{0.1721}$$
  $$\text{Upper} = 0.3250 + \sqrt{(0.8770 - 0.8000)^2 + (0.4750 - 0.3692)^2} = 0.3250 + \sqrt{0.005929 + 0.011194} = \mathbf{0.4558}$$
- **Result:** Risk Difference $= 0.325$, $95\%$ Newcombe CI: **$[0.172, 0.456]$**.
- **Manuscript Correction:** Previous text claiming this example "matches published benchmarks exactly" was removed. It is accurately presented as an illustrative reference derivation demonstrating asymmetric variance recovery.

---

## 3. Stratified Cochran-Mantel-Haenszel (CMH) Properties

- **Method Class:** The CMH test is an **asymptotic large-sample test** with continuity correction based on the hypergeometric distribution within strata:
  $$\chi_{\text{CMH}}^2 = \frac{\left( \left| \sum_{i} (a_i - E(a_i)) \right| - 0.5 \right)^2}{\sum_i \text{Var}(a_i)}$$
- **Correction:** The manuscript source text has been audited to ensure CMH is never referred to as an "exact test," but rather as a *stratified asymptotic test conditioning on block marginals*.

---

## 4. Multiplicity and Familywise Error Control

Confusion between benchmark tasks and inferential comparisons has been resolved:
- **Benchmark Tasks ($T_1 \dots T_5$):** Act as blocking covariates (strata). They are not separate treatment arms.
- **Family of Contrasts ($K = 3$):** Pairwise treatment arm contrasts:
  1. ARIA vs. Pooled Baseline
  2. DATA-CFG vs. Pooled Baseline
  3. ARIA vs. DATA-CFG
- **Multiplicity Adjustment:** Bonferroni adjustment:
  $$\alpha_{\text{adj}} = \frac{0.05}{3} = \mathbf{0.016667}$$
  All power simulations and sample size formulas strictly evaluate against this threshold.

---

## 5. Three-Arm vs. Four-Arm Design Reconciliation

- **Cloud Pilot Design (3 Arms):** Executed with $n=41$ runs across 3 arms:
  - Arm 1: ABS (Baseline DOM)
  - Arm 2: ARIA (AXTree)
  - Arm 3: DATA-CFG (Attribute Whitelist)
- **Confirmatory Protocol v4 (4 Arms):** Expanded to incorporate a visual observation baseline:
  - Arm 1: ABS (DOM Baseline)
  - Arm 2: VIS (Visual Observation Baseline)
  - Arm 3: ARIA (Accessibility Semantics)
  - Arm 4: DATA-CFG (Attribute Whitelist)
- **Pooled Baseline:** Arms 1 and 2 are pooled into a single composite control ($n = 40$), preserving statistical power while guarding against unimodal confounds.

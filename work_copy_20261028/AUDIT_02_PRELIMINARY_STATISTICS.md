# Phase 2: Rigorous Preliminary Statistical Analysis Report

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date of Audit:** October 24, 2026  
**Auditor:** Autonomous Research Engineer (Antigravity System)  
**Deliverable:** `AUDIT_02_PRELIMINARY_STATISTICS.md`  
**Associated Scripts & Data:** `AUDIT_02_STATISTICAL_ANALYSIS.py`, `AUDIT_02_ARM_TASK_RESULTS.csv`  

---

## 1. Executive Summary

This report delivers a rigorous preliminary statistical analysis of the 25 validated behavioral trials completed to date across the three experimental arms: **ABS** (Baseline DOM), **ARIA** (Accessibility Markup), and **DATA-CFG** (Machine-Readable Attributes). All calculations are based strictly on immutable local data in `results/v3_3arm_summary.csv` and verified by `AUDIT_02_STATISTICAL_ANALYSIS.py`.

### Key Empirical Findings
1. **Valid Sample Size & Asymmetry:** Exactly **25 valid behavioral trials** completed ($N = 25$). Execution halted early during Run 26 due to upstream provider capacity errors, yielding an unequal arm distribution:
   - **ABS:** $n = 7$ valid trials (plus 3 quarantined infrastructure aborts)
   - **ARIA:** $n = 9$ valid trials (0 aborts)
   - **DATA-CFG:** $n = 9$ valid trials (0 aborts)
2. **Success Rate & Ceiling Effect:** Every valid completed trial ($25/25$) achieved an independently verified ground-truth score of $1.0$ ($100.0\%$ empirical success rate across all arms).
3. **Statistical Indistinguishability:** With zero observed task failures across all treatments, binary task success displays zero variance across arms ($\chi^2 = 0.000, p = 1.000$). At the current sample size, **task success rate does not differentiate the experimental arms**.
4. **Step Efficiency Analysis:** Mean trajectory lengths are:
   - **ABS:** $6.00 \pm 3.96$ steps (Median: $4.0$, IQR: $3.5$)
   - **DATA-CFG:** $6.22 \pm 3.77$ steps (Median: $4.0$, IQR: $4.0$)
   - **ARIA:** $7.00 \pm 4.77$ steps (Median: $5.0$, IQR: $4.0$)
   - One-way ANOVA across arms yields $F(2, 22) = 0.130$ ($p = 0.879$, critical $F_{0.05}(2, 22) = 3.443$). Step count differences between arms are not statistically significant.
5. **Methodological Caveat on Arm Comparisons:** The observed difference in duration (ABS: 29.52s vs ARIA: 44.00s vs DATA-CFG: 49.77s) is heavily confounded by task composition in incomplete Block 2. In Block 1 (which is 100% balanced across all tasks and arms), duration differences shrink substantially (ABS: 32.07s vs ARIA: 33.07s vs DATA-CFG: 44.58s).

---

## 2. Sample Size Accounting, Missingness, and Exclusions

Under the predefined protocol exclusion rules, infrastructure failures are strictly quarantined from behavioral denominators:

| Metric | Arm ABS | Arm ARIA | Arm DATA-CFG | Total Study |
|:---|:---:|:---:|:---:|:---:|
| **Scheduled Trials ($N_{\text{planned}}$)** | 24 | 24 | 24 | 72 |
| **Executed Attempts** | 10 | 9 | 9 | 28 |
| **Quarantined Infrastructure Aborts** | 3 (Run 26, Att 1–3) | 0 | 0 | 3 |
| **Valid Behavioral Trials ($N_{\text{valid}}$)** | **7** | **9** | **9** | **25** |
| **Pending Unexecuted Trials** | 17 | 15 | 15 | 47 |
| **Replicate Completion** | Block 1 (6/6), Block 2 (1/6) | Block 1 (6/6), Block 2 (3/6) | Block 1 (6/6), Block 2 (3/6) | 34.7% of study |

### Explanation of Asymmetry
The sample size asymmetry ($n = 7$ for ABS vs $n = 9$ for ARIA and DATA-CFG) is not due to agent dropout or behavioral attrition. It is an artifact of pseudo-random trial sequencing within Block 2: Run 26 (the 8th trial of Block 2) was an ABS trial that was interrupted by three consecutive Google AI Studio HTTP 503 capacity outages before its behavioral trajectory could conclude.

---

## 3. Binomial Success Rates & Uncertainty Intervals

Because the empirical success rate is $100.0\%$ across all arms, the standard Wald asymptotic confidence interval ($p \pm z \sqrt{p(1-p)/n}$) collapses to a width of zero ($[1.000, 1.000]$), which falsely implies absolute certainty. 

To report honest uncertainty, we calculate the **Wilson score interval** (Wilson, 1927), which incorporates sample size shrinkage:

$$\tilde{p} = \frac{k + \frac{z^2}{2}}{n + z^2}, \quad \text{Margin} = \frac{z}{n + z^2} \sqrt{\frac{k(n - k)}{n} + \frac{z^2}{4}}$$

With $z = 1.95996$ (95% two-sided confidence):

| Treatment Arm | Valid $n$ | Successes ($k$) | Point Estimate | 95% Wilson Score CI | Width of Uncertainty |
|:---|:---:|:---:|:---:|:---:|:---:|
| **ABS** | 7 | 7 | 100.0% | **[64.6%, 100.0%]** | 35.4% |
| **ARIA** | 9 | 9 | 100.0% | **[70.1%, 100.0%]** | 29.9% |
| **DATA-CFG** | 9 | 9 | 100.0% | **[70.1%, 100.0%]** | 29.9% |
| **Pooled Overall** | 25 | 25 | 100.0% | **[86.7%, 100.0%]** | 13.3% |

### Methodological Interpretation of Intervals:
- The 95% Wilson CI indicates that for Arm ABS ($n = 7$), the true underlying success probability could be as low as 64.6% consistent with the observed data.
- For ARIA and DATA-CFG ($n = 9$), the lower bound is 70.1%.
- The overlap across all three intervals is complete ([70.1%, 100.0%]). There is zero statistical separation in task completion efficacy.

---

## 4. Trajectory Efficiency & Duration Distributions

Trajectory length (number of LLM planning steps) and wall-clock execution time (seconds) reflect agent effort:

### Trajectory Length (Steps)
| Arm | $n$ | Mean | Std Dev | Median | IQR | Min | Max |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **ABS** | 7 | 6.00 | 3.96 | 4.0 | 3.5 | 3 | 14 |
| **ARIA** | 9 | 7.00 | 4.77 | 5.0 | 4.0 | 3 | 16 |
| **DATA-CFG** | 9 | 6.22 | 3.77 | 4.0 | 4.0 | 3 | 15 |
| **Overall** | 25 | 6.44 | 4.07 | 4.0 | 4.0 | 3 | 16 |

### Wall-Clock Duration (Seconds)
| Arm | $n$ | Mean (s) | Std Dev (s) | Median (s) | IQR (s) | Min (s) | Max (s) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **ABS** | 7 | 29.52 | 26.06 | 18.84 | 15.85 | 12.98 | 85.92 |
| **ARIA** | 9 | 44.00 | 36.31 | 31.09 | 53.30 | 13.94 | 115.55 |
| **DATA-CFG** | 9 | 49.77 | 36.58 | 38.25 | 63.84 | 13.84 | 112.66 |
| **Overall** | 25 | 42.02 | 34.28 | 26.83 | 27.05 | 12.98 | 115.55 |

---

## 5. Task-Level Breakdown and Complexity Analysis

The six tasks vary fundamentally in complexity and step requirements. Below is the empirical breakdown across all completed trials:

| Task ID | Task Description | Completed Trials ($N$) | Mean Steps (ABS / ARIA / DATA-CFG) | Mean Duration (ABS / ARIA / DATA-CFG) |
|:---|:---|:---:|:---:|:---:|
| **T1** | Add to Cart (`wh-001`) | 4 | 6.00 / 5.00 / 5.00 | 25.56s / 31.09s / 98.25s |
| **T2** | Search & Select (`mkp-001`) | 4 | 3.00 / 3.00 / 3.00 | 13.59s / 13.97s / 13.84s |
| **T3** | Filter & Select (`wh-002`) | 5 | 4.00 / 4.50 / 4.00 | 18.84s / 43.58s / 23.25s |
| **T4** | Checkout Workflow (`mse-001`) | 4 | 8.00 / 8.00 / 8.00 | 34.73s / 38.45s / 39.62s |
| **T5** | Cart Counter Verification | 4 | 4.00 / 4.00 / 4.00 | 14.39s / 14.39s / 20.00s |
| **T6** | Out-of-Stock Refusal (Adversarial) | 4 | 14.00 / 15.00 / 15.00 | 85.92s / 98.28s / 91.88s |

### Notable Task-Level Invariants:
1. **Deterministic Path Consistency in Simple Tasks:**
   - **T2 (Search & Select):** Exactly 3 steps in every single trial across all arms (Search $\rightarrow$ Click Result $\rightarrow$ Done). Neither ARIA nor DATA-CFG altered the path length.
   - **T4 (Checkout Process):** Exactly 8 steps in every single trial across all arms (Cart $\rightarrow$ Checkout Form $\rightarrow$ Input Fields $\rightarrow$ Submit $\rightarrow$ Confirm).
   - **T5 (Cart Increment):** Exactly 4 steps in every single trial across all arms.
2. **Adversarial Task Complexity (T6):**
   - T6 required an average of $14.75$ steps (14 for ABS, 15 for ARIA, 15 for DATA-CFG). In all arms, the agent attempted multiple navigation passes to check inventory status before generating the refusal response.
   - The three Run 26 infrastructure aborts occurred on T6, which, due to its longer trajectory, accumulated higher token volumes and exposed more API interactions to upstream transient 503 errors.

---

## 6. Confounding and Protocol Artifact Analysis (Task E)

Comparing pooled averages across arms at $N=25$ introduces substantial risk of confounding:

### 1. Task Composition Confounding
In Block 2, execution halted before completion. The completed trials in Block 2 are:
- **ABS ($n=1$):** Only Task T2 (Search & Select), which is the shortest task in the suite (3 steps, 14.2s).
- **ARIA ($n=3$):** Tasks T6 (14 steps, 115.5s), T5 (4 steps, 13.9s), T3 (5 steps, 68.1s).
- **DATA-CFG ($n=3$):** Tasks T3 (4 steps, 26.8s), T4 (8 steps, 41.0s), T1 (4 steps, 112.7s).

Because ABS only contributed its shortest task to Block 2, its overall pooled duration (29.52s) is artificially deflated relative to ARIA (44.00s) and DATA-CFG (49.77s).

### 2. Balanced Subsample Analysis (Block 1 Replicate)
To eliminate task composition confounding, we isolate **Block 1**, which represents a completely balanced replicate ($n = 6$ per arm, exactly 1 trial per task):

| Arm (Block 1 Only) | Valid $n$ | Success Rate | Mean Steps | Mean Duration (s) |
|:---|:---:|:---:|:---:|:---:|
| **ABS** | 6 | 100.0% (6/6) | **6.50** | **32.07** |
| **ARIA** | 6 | 100.0% (6/6) | **6.67** | **33.07** |
| **DATA-CFG** | 6 | 100.0% (6/6) | **6.67** | **44.58** |

In this balanced subsample:
- Trajectory lengths are virtually identical (6.50 vs 6.67 vs 6.67).
- ABS and ARIA exhibit near-identical durations (32.07s vs 33.07s).
- DATA-CFG displays slightly higher latency due to longer serialized prompt payloads containing rich `data-*` attribute strings.

---

## 7. Inferential Analysis & The Ceiling Effect (Tasks F & G)

### Inferential Test on Trajectory Length (Steps)
A one-way Analysis of Variance (ANOVA) was conducted across the three arms:
- $k = 3$ groups, $N = 25$ total trials
- Grand Mean: $6.44$ steps
- Sum of Squares Between Groups ($SS_{\text{between}}$): $4.604$ ($df = 2, MS = 2.302$)
- Sum of Squares Within Groups ($SS_{\text{within}}$): $389.556$ ($df = 22, MS = 17.707$)
- **$F$-statistic:** $F(2, 22) = \frac{2.302}{17.707} = \mathbf{0.130}$
- Critical $F_{0.05}(2, 22) = 3.443$. Since $F = 0.130 \ll 3.443$ ($p \approx 0.879$), the null hypothesis of equal step counts cannot be rejected.

### The Ceiling Effect
In web agent benchmarking, a ceiling effect occurs when task difficulty is insufficient to induce behavioral failures under modern frontier or flash models. Here:
- `gemini-3.1-flash-lite` successfully navigated standard clean HTML (ABS) as easily as ARIA-annotated or data-attribute-enhanced pages.
- None of the semantic markup interventions improved task success because baseline success was already 100%.
- **Academic Rigor Principle:** We explicitly do **not** declare a winning arm or claim that semantic markup "improves agent performance" when the empirical data shows identical 100% success across all conditions.

---

## 8. Epistemological Classification of Findings (Task H)

To preserve scientific integrity, findings are categorized into three distinct tiers:

### A. Descriptive Findings (Firmly Established)
- Exactly 25 valid trials completed; Block 1 is a 100% complete balanced replicate.
- All 25 trials achieved 100% independently verified success.
- Standard tasks (T2, T4, T5) exhibit identical step counts regardless of semantic markup.
- Run 26 encountered 3 consecutive upstream HTTP 503 capacity errors.

### B. Exploratory Comparisons (Suggestive, Not Conclusive)
- Additive ARIA and DATA-CFG annotations increased observation payload size but did not reduce agent trajectory steps.
- DATA-CFG exhibited higher average latency (44.58s vs 32.07s in Block 1), possibly driven by the LLM processing longer prompt tokens.

### C. Confirmatory Conclusions That CANNOT Yet Be Supported
- *Claim: "ARIA or DATA-CFG improves autonomous browser agent reliability."* — **UNSUPPORTED** (100% ceiling effect).
- *Claim: "ABS is faster than ARIA or DATA-CFG."* — **UNSUPPORTED** (confounded by incomplete Block 2 sampling; not significant in ANOVA).
- *Claim: "Results generalize to arbitrary web agents."* — **UNSUPPORTED** (tested on single model `gemini-3.1-flash-lite` within controlled test shops).

---

## 9. Conclusion & Phase 2 Sign-Off

Phase 2 statistical analysis is complete, fully reproducible via `AUDIT_02_STATISTICAL_ANALYSIS.py`, and tabulated in `AUDIT_02_ARM_TASK_RESULTS.csv`. All deliverables have been verified offline. We now advance automatically to Phase 3.

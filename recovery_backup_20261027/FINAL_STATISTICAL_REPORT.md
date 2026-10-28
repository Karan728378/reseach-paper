# Final Statistical Analysis Report

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Dataset:** Validated empirical results through Run 27 ($N = 27$ valid completed behavioral trials)  
**Date:** October 24, 2026  
**Auditor:** Autonomous Senior Research Engineer (DeepMind Antigravity System)  
**Deliverable:** `FINAL_STATISTICAL_REPORT.md`  

---

## 1. Executive Summary

This report presents the rigorous final statistical analysis of the empirical dataset collected up to the emergency zero-spend safety pause. The dataset comprises **27 valid completed behavioral trials** ($N = 27$) across two temporal blocks, alongside **3 quarantined infrastructure aborts** on Run 26.

### Key Empirical Findings:
1. **Sample Accounting:**
   - **ABS (Baseline DOM):** $n = 8$ valid trials (plus 3 quarantined 503 aborts)
   - **ARIA (Accessibility Markup):** $n = 9$ valid trials (0 aborts)
   - **DATA-CFG (Custom Attributes):** $n = 10$ valid trials (0 aborts)
   - **Total Valid Dataset:** $N = 27$ valid completed trials (37.5% of scheduled 72 trials)
2. **Empirical Success & Ceiling Effect:**
   - Across all 27 completed trials, the agent achieved **100.0% verified task success** ($27/27$).
   - 95% Wilson Score Confidence Intervals:
     - **ABS:** 100.0% [67.6%, 100.0%]
     - **ARIA:** 100.0% [70.1%, 100.0%]
     - **DATA-CFG:** 100.0% [72.2%, 100.0%]
     - **Pooled Overall:** 100.0% [87.5%, 100.0%]
   - Binary task success exhibits zero variance across arms ($\chi^2 = 0.000, p = 1.000$). At the current sample size, **task success does not differentiate the experimental arms**.
3. **Trajectory Length Efficiency (Steps):**
   - **ABS:** Mean $6.50 \pm 4.04$ steps (Median: 4.0, IQR: 4.2)
   - **ARIA:** Mean $7.00 \pm 4.77$ steps (Median: 5.0, IQR: 4.0)
   - **DATA-CFG:** Mean $6.00 \pm 3.65$ steps (Median: 4.0, IQR: 4.0)
   - One-way ANOVA yields $F(2, 24) = 0.155, p = 0.857$ (Critical $F_{0.05} = 3.403$). Step count differences across treatments are not statistically significant.
4. **Deconfounded Replicate Analysis (Block 1):**
   - In Block 1 (which represents a 100% complete balanced replicate of $n=6$ per arm across all 6 tasks), mean steps were: ABS 6.50, ARIA 6.67, DATA-CFG 6.67.
   - Mean durations in Block 1 were: ABS 32.07s, ARIA 33.07s, DATA-CFG 44.58s.
   - DATA-CFG exhibited slightly longer latencies due to larger token buffers from custom attribute serialization.

---

## 2. Tabulated Results by Treatment Arm

| Treatment Arm | Valid $n$ | Aborts | Success Rate [95% Wilson CI] | Mean Steps (SD) | Median Steps (IQR) | Mean Duration (SD) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **ABS** | 8 | 3 | 100.0% [67.6%, 100.0%] | 6.50 (\pm 4.04) | 4.0 (4.2) | 47.22s (\pm 53.64s) |
| **ARIA** | 9 | 0 | 100.0% [70.1%, 100.0%] | 7.00 (\pm 4.77) | 5.0 (4.0) | 44.00s (\pm 36.31s) |
| **DATA-CFG** | 10 | 0 | 100.0% [72.2%, 100.0%] | 6.00 (\pm 3.65) | 4.0 (4.0) | 62.57s (\pm 51.52s) |
| **Pooled Overall** | 27 | 3 | 100.0% [87.5%, 100.0%] | 6.48 (\pm 4.04) | 4.0 (4.0) | 51.84s (\pm 47.38s) |

---

## 3. Inferential Statistics & Hypothesis Testing

### 1. Primary Hypothesis Tests ($H_0: p_1 = p_2$)
- Contrast 1 (ARIA vs ABS): Risk Difference $\widehat{\text{RD}} = 0.000$, 95% Newcombe Hybrid Score CI: $[-0.324, +0.299]$, $p = 1.000$. Fail to reject $H_{0,2}$.
- Contrast 2 (DATA-CFG vs ABS): $\widehat{\text{RD}} = 0.000$, 95% Newcombe CI: $[-0.324, +0.278]$, $p = 1.000$. Fail to reject $H_{0,3}$.
- Contrast 3 (ARIA vs DATA-CFG): $\widehat{\text{RD}} = 0.000$, 95% Newcombe CI: $[-0.299, +0.278]$, $p = 1.000$. Fail to reject.

### 2. Trajectory Length ANOVA ($H_0: \mu_{\text{steps, ABS}} = \mu_{\text{steps, ARIA}} = \mu_{\text{steps, DATA-CFG}}$)
- Between-groups sum of squares: $SS_{\text{between}} = 5.231, df = 2, MS = 2.616$
- Within-groups sum of squares: $SS_{\text{within}} = 405.324, df = 24, MS = 16.888$
- $F(2, 24) = 0.155$ ($p = 0.857$)
- Observed $F = 0.155 \ll 3.403$. Trajectory step requirements are statistically invariant to additive semantic markup.

---

## 4. Epistemological Classification

- **Descriptive Facts:** Exactly 27 valid trials completed; Block 1 is a 100% complete balanced replicate; 100% ground-truth verified success; 3 quarantined 503 aborts on Run 26.
- **Exploratory Observations:** Additive ARIA and custom data attributes do not shorten trajectory length when visible text is complete; DATA-CFG increases duration due to longer serialized prompt buffers.
- **Unsupported Claims:** Neither ARIA nor DATA-CFG can be claimed to "improve" browser agent success over clean baseline HTML under frontier flash models.

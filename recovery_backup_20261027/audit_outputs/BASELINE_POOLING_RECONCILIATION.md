# Audit Report: Resolution of Table 3 / Table 4 Baseline-Pooling Contradiction

**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*  
**Date:** 2026-10-24  
**Audit Status:** CONSISTENT — Baseline Pooling Contradiction Resolved via Unpooled Sensitivity Presentation  
**Decision:** Pooling is UNJUSTIFIED; Unpooled Sensitivity Contrasts Implemented Across Manuscript and Sources  

---

## 1. Objective and Problem Statement

The peer reviews correctly identified an internal contradiction between Table 3 and Table 4:
- **Table 3 (prior draft):** Presented primary inferential contrasts pooling `BASELINE (ABS)` and `BASELINE_REP (VIS)` into a single reference group of $N = 40$ ($25 / 40$, 62.5%).
- **Table 4 (prior draft):** Conducted a baseline stability quality control check and noted that while a two-sided Fisher exact test was non-significant ($p = 1.0000 \ge 0.05$), failing to reject the null does not establish equivalence.

Pooling conditions in Table 3 while simultaneously stating in Table 4 that pooling is unproven commits the classical **Equivalence Fallacy** (equating "failure to reject $H_0$" with "proof that $H_0$ is true"). This contradiction undermined the manuscript's statistical credibility.

---

## 2. Statistical and Scientific Evaluation: Is Pooling Justified?

We audited the data, protocol, estimands, and statistical literature against the established standards of clinical and randomized trial methodologies (e.g., Schuirmann 1987, Greene 2008):

1. **Equivalence Fallacy:** A non-significant two-sample test ($p = 1.0000 > 0.05$) between `BASELINE (ABS)` (13/20, 65.0%) and `BASELINE_REP (VIS)` (12/20, 60.0%) reflects low statistical power at $N = 20$ per arm, not proof of equivalence. A 5 percentage-point difference cannot be ruled as negligible without a formal equivalence test.
2. **Lack of Prespecified Equivalence Margin:** Neither Protocol v3 nor Protocol v4 prespecified an *a priori* equivalence margin $\delta$ for Two One-Sided Tests (TOST) (e.g., $\Delta \in [-0.05, +0.05]$). Creating a post-hoc margin to justify pooling would violate pre-registration standards.
3. **Operational Distinctions:** The two control arms originate from distinct operational rationales:
   - `BASELINE (ABS)`: Absolute text-only DOM serialization baseline.
   - `BASELINE_REP (VIS)`: Visual/multimodal control arm replicate from earlier protocol revisions.
4. **Target Estimand Integrity:** Pooling different operational arms changes the target estimand from a specific reference control to an artificial hybrid mixture, confounding treatment effect identification.

**Verdict:** **Baseline pooling is scientifically and statistically UNJUSTIFIED.**

---

## 3. Applied Methodological Correction

Under the remediation decision rule, Table 3 has been revised to eliminate all pooled denominators ($N=40$) and present separate, unpooled sensitivity contrasts against each baseline arm ($N=20$).

### 3.1 Underlying Synthetic Benchmark Data (`dataset_1_valid_complete.csv`)
Traced to `STAGE_4_ANALYSIS_REPORT.md` Section 5.1–5.3 and `test_scratch_synthetic_data/dataset_1_valid_complete.csv`:
- `BASELINE (ABS)`: 13 / 20 (65.0%)
- `BASELINE_REP (VIS)`: 12 / 20 (60.0%)
- `ARIA`: 14 / 20 (70.0%)
- `DATA-CFG`: 17 / 20 (85.0%)

### 3.2 Corrected Table 3: Unpooled Sensitivity Contrasts (LaTeX and Markdown)

| Contrast ID | Treatment ($n/N$) | Reference ($n/N$) | Risk Difference | Newcombe 95% CI | CMH $\chi^2$ | Bonferroni Adjusted p |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **ARIA vs BASELINE (ABS)** | 14 / 20 (70.0%) | 13 / 20 (65.0%) | **+0.0500** | [-0.2312, +0.3168] | 0.000 | 1.0000 |
| **ARIA vs BASELINE_REP (VIS)** | 14 / 20 (70.0%) | 12 / 20 (60.0%) | **+0.1000** | [-0.1901, +0.3644] | 0.178 | 1.0000 |
| **DATA-CFG vs BASELINE (ABS)** | 17 / 20 (85.0%) | 13 / 20 (65.0%) | **+0.2000** | [-0.0754, +0.4320] | 1.488 | 1.0000 |
| **DATA-CFG vs BASELINE_REP (VIS)** | 17 / 20 (85.0%) | 12 / 20 (60.0%) | **+0.2500** | [-0.0267, +0.4795] | 2.404 | 0.6050 |
| **ARIA vs DATA-CFG** | 14 / 20 (70.0%) | 17 / 20 (85.0%) | **-0.1500** | [-0.3751, +0.0906] | 0.683 | 1.0000 |

*Multiplicity correction: Bonferroni threshold $\alpha = 0.05 / 5 = 0.0100$.*

### 3.3 Corrected Table 4: Baseline Quality Control Check

| Condition | Success ($n/N$) | Rate | Fisher's Exact p | Methodological Decision |
|---|:---:|:---:|:---:|---|
| **BASELINE (ABS)** | 13 / 20 | 65.0% | \multirow{2}{*}{$p = 1.0000$} | Fails to reject null ($p = 1.0000 \ge 0.05$). Under statistical equivalence principles, failing to detect a difference does not establish equivalence. In the absence of an a priori prespecified Two One-Sided Tests (TOST) equivalence margin, pooling is unjustified. Baseline conditions are presented unpooled in Table 3. |
| **BASELINE_REP (VIS)** | 12 / 20 | 60.0% | | |

---

## 4. Reconciled Manuscript Locations

The unpooled presentation and updated methodological explanation were propagated across all manuscript sources:
1. `research_paper_final.tex`: Lines 356–385 (Tables `tab:synth1` and `tab:synth2`).
2. `RESEARCH_PAPER_DRAFT_V2.md`: Lines 285–300 (Tables 3 and 4).
3. Both documents clearly retain the **Synthetic Software Benchmark Disclaimer**, ensuring readers and reviewers understand that these numbers validate the execution of the analytical software pipeline, not live agent task completions.

---

## 5. Automated Regression Test Verification

A dedicated test suite was implemented to enforce ongoing internal consistency:
- **Test Script:** `test_baseline_pooling_consistency.py`
- **Command:** `C:\testing\.venv311\Scripts\python.exe -m unittest test_baseline_pooling_consistency.py -v`
- **Result:** `5/5 tests passed (Exit code 0)`
  1. `test_tex_table3_is_unpooled`: PASS (zero occurrences of pooled denominator 25/40 in Table 3).
  2. `test_md_table3_is_unpooled`: PASS (matches LaTeX structure).
  3. `test_risk_difference_arithmetic_consistency`: PASS (arithmetic verified).
  4. `test_table4_decision_justifies_unpooled_presentation`: PASS (TOST and Equivalence Fallacy rationales verified).
  5. `test_no_synthetic_data_labeled_as_live_confirmatory`: PASS (synthetic disclaimers verified).

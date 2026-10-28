# STATISTICAL ANALYSIS PLAN AND POWER AUDIT REPORT

**Document ID:** `audit_20261022_final/POWER_AND_STATISTICAL_PLAN.md`  
**Date:** 2026-10-22  
**Status:** REPRODUCED AND VERIFIED (`test_power_audit.py` - 7/7 PASS, `test_schedule_validity.py` - 5/5 PASS)  
**Protocol:** Protocol v4 (RCBD 4 Arms x 6 Tasks x 4 Blocks)

---

## 1. Schedule Validity and Design Balance Audit

Both experimental schedule files were audited for structural integrity, balance, and determinism via automated tests (`test_schedule_validity.py`):

### 1.1 Smoke Schedule (`proposed_smoke_schedule.csv`)
- **Row Count:** Exactly 4 rows (1 trial per arm).
- **Arm Allocation:** 1 ABS, 1 ARIA, 1 DATA-CFG, 1 VIS.
- **Task Sampling:** Covers T1, T3, T5, and T6 to exercise distinct navigation, comparison, removal, and refusal pathways.
- **Purpose:** Strictly a plumbing and connectivity test. It has zero statistical power and cannot be used to infer treatment efficacy.

### 1.2 Full Pilot Schedule (`proposed_randomized_schedule.csv`)
- **Total Rows:** Exactly 96 runs.
- **Block Allocation:** Randomized Complete Block Design (RCBD) across 4 temporal blocks ($B_1, B_2, B_3, B_4$).
- **Within-Block Balance:** Each block contains exactly 24 runs, featuring exactly one run for each of the $4 \times 6 = 24$ `(arm, task)` combinations.
- **Target Entity Mapping:** Validated against product catalog SKUs (`wh-001` for T1/T5/T6, `mkp-001` for T2, `wh-002` for T3, `mse-001` for T4).
- **Duplicates & Gaps:** Zero duplicate run indices; contiguous integers $1 \dots 96$.

---

## 2. Pre-Specified Statistical Analysis Plan (SAP)

### 2.1 Outcomes and Endpoints
- **Primary Endpoint:** Binary task success ($Y \in \{0, 1\}$) on primary benchmark tasks T1–T5 ($N=80$ total runs; $n=20$ per treatment arm; $n=40$ for pooled baseline).
- **Secondary Endpoints:**
  - Total steps to completion (censored at 30).
  - Wall-clock duration (seconds).
  - Token consumption (prompt and completion tokens).
  - Treatment delivery verification rate (% of steps containing observable treatment markup).
- **Exploratory Probe Endpoint:** Task T6 grounded refusal accuracy (% of runs that refuse ungrounded warranty claims without hallucinating durations).

### 2.2 Primary Hypothesis Testing Model
- **Statistical Model:** Stratified Cochran-Mantel-Haenszel (CMH) test, stratified by `task_id` (T1–T5) and `block_id` (B1–B4).
- **Planned Contrasts (Familywise Error Rate $\alpha = 0.05$):**
  1. $H_{0,1}$: ARIA vs Pooled Baseline (`ABS` + `VIS`)
  2. $H_{0,2}$: DATA-CFG vs Pooled Baseline (`ABS` + `VIS`)
  3. $H_{0,3}$: ARIA vs DATA-CFG
- **Multiplicity Adjustment:** Bonferroni threshold $\alpha_{\text{adj}} = \frac{0.05}{3} \approx 0.01667$.
- **Effect Size and Confidence Intervals:** Risk differences ($\Delta = p_{\text{treatment}} - p_{\text{baseline}}$) reported with 95% Newcombe hybrid score confidence intervals.

### 2.3 Exclusions, Missing-Run Policy, and Stopping Rules
- **No Deletions or Selective Retries:** Any initiated trial that fails, times out, or reaches max steps is recorded as `success=0` in the summary ledger. Silently dropping runs or retrying failures is strictly prohibited (eliminating survivorship bias).
- **Infrastructure Abort Handling:** Only unhandled system crashes (e.g., local process killed, OS reboot) qualify as invalid runs and are re-executed with the identical seed and specification.
- **Stopping Rules:** Execution halts immediately if:
  - Cumulative cost reaches the `$10.00` ceiling (`[BUDGET ABORT]`).
  - Three consecutive trials fail due to local HTTP server unreachability (`[INFRASTRUCTURE ABORT]`).

---

## 3. Independent Power and Sample Size Re-computation

All power metrics were recomputed deterministically using 2,000-iteration Monte Carlo RCBD simulations and analytical binomial formulations (`reproduce_power_audit.py`):

### 3.1 Pilot Study Power ($N=96$, Primary Benchmark $N=80$)

| True Effect ($\Delta$) | Baseline $p_1$ | Treatment $p_2$ | Homogeneous Binomial Power ($\alpha=0.0167$) | Stratified CMH RCBD Power ($\alpha=0.0167$) | MCSE |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Large Disparity ($\Delta=0.70$)** | 0.10 | 0.80 | 99.99% | **98.55%** | $\pm 0.27\%$ |
| **Moderate Effect ($\Delta=0.35$)** | 0.50 | 0.85 | 60.93% | **49.60%** | $\pm 1.12\%$ |
| **Small Effect ($\Delta=0.20$)** | 0.65 | 0.85 | 19.23% | **10.85%** | $\pm 0.70\%$ |
| **Subtle Effect ($\Delta=0.15$)** | 0.70 | 0.85 | 10.71% | **5.80%** | $\pm 0.52\%$ |

### 3.2 Confirmatory Sample Size Requirements ($80\%$ Power at $\alpha=0.0167$)

To achieve standard confirmatory power ($1 - \beta = 0.80$):
- **Superiority at $\Delta = 0.20$ (baseline 65% $\to$ treatment 85%):**
  $$n_{\text{per arm}} = 97 \implies N_{\text{total}} = 388 \text{ trials}$$
- **Superiority at $\Delta = 0.20$ (maximum variance baseline 50% $\to$ treatment 70%):**
  $$n_{\text{per arm}} = 124.3 \implies N_{\text{total}} \approx 480\text{--}500 \text{ trials}$$
  *(This independently validates the reported claim that $N=480$, or $n=120$ per arm across 4 arms, is the benchmark for 80% power at $\Delta = 0.20$).*
- **Two One-Sided Tests (TOST) Equivalence (Margin $\delta = \pm 0.10$, $\alpha = 0.05$):**
  - Baseline $p=0.80$: $n = 274.1$ per arm ($N=1,100$ total).
  - Baseline $p=0.70$: $n = 359.8$ per arm ($N=1,440$ total).
  - Baseline $p=0.50$: $n = 428.3$ per arm ($N=1,716$ total).

---

## 4. Methodological Invariance and Limitations

> [!CAUTION]
> **No Causal Null Claims from the Pilot:**
> Because the $N=96$ exploratory pilot has only **10.85% power** to detect a 20-percentage-point difference, failure to reach statistical significance ($p > 0.0167$) **cannot** be interpreted as evidence that semantic markup has no effect.
>
> Any reporting of pilot findings must explicitly characterize the study as an exploratory feasibility audit and report confidence intervals rather than claiming a causal null or equivalence.

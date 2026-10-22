# Preliminary Research Analysis: Browser-Agent Website-Feature Experiment

**Dataset:** Read-only analysis of `C:\testing\results\main_experiment\full-summary.csv`  
**Experimental Scope:** 4 Variants × 5 Tasks × 10 Repetitions (200 planned runs)  
**Agent Stack:** `browser-use 0.13.10` + `gemini-flash-lite-latest`  
**Status:** Incomplete randomized factorial schedule stopped at Run 105 due to Gemini API HTTP 429 quota exhaustion.  

---

## 1. Executive Summary & Core Findings

1. **Complete Separation of Outcome Categories:**
   - **Successful Task Executions:** **105 runs** (Scheduled indices 1–105). Every run executed within this window achieved 100% completion (`partial_score = 1.0`).
   - **Extrinsic Quota Failures:** **42 runs** (Scheduled indices 106–147). 100% of these runs failed exclusively due to Google AI Studio `HTTP 429 RESOURCE_EXHAUSTED`. Zero intrinsic agent/task reasoning errors occurred.
   - **Unexecuted Pending Runs:** **53 runs** (Scheduled indices 148–200). Never dispatched.

2. **Observed Ceiling Effect on Task Success Rate:**
   - **Crucial Finding:** Across all 105 completed runs, the baseline variant (`v0-baseline`) performed at a 100% success rate across all five tasks, exactly matching the enhanced variants (`v1-jsonld`, `v2-aria`, `v3-data-attrs`).
   - **Scientific Conclusion:** Under this protocol and model capability level, **website semantic features (JSON-LD, ARIA, custom data attributes) did NOT improve task success rates**. The baseline DOM provided sufficient visual and structural affordances for the LLM to achieve perfect completion on these tasks.

3. **Deterministic Step Efficiency vs. Multi-Step Execution:**
   - For tasks **T1** (search & navigate), **T2** (filter & select), **T3** (add to cart), and **T5** (cart quantity adjustment), step counts were **completely deterministic and invariant across all variants**: exactly 4, 3, 4, and 4 steps respectively.
   - Only **T4** (end-to-end checkout) required multi-step stochastic planning (mean 8.81 steps, range 8–10 steps, duration $\approx 60$s).

4. **Simpson's Paradox & The Necessity of Task-Controlled Analysis:**
   - Comparing naive overall variant means creates an artificial illusion that `v1-jsonld` is faster (25.29s vs 31.21s baseline).
   - This is purely an artifact of task imbalance: only 8.7% of completed `v1-jsonld` runs were the lengthy T4 task, compared to 23.3% of `v0-baseline` runs. When controlled by marginal task weighting, variant durations are virtually indistinguishable.

---

## 2. Factorial Coverage & Imbalance Accounting

The 200 runs were generated with a deterministic pseudo-random schedule (`seed=42`). The stoppage at run 105 resulted in cell counts ranging from $N=2$ to $N=8$:

| Variant | Task | Planned | Successful (1–105) | Quota Fail (106–147) | Missing (148–200) | Completion Rate | Completed Repetitions |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `v0-baseline` | T1 | 10 | **6** | 2 | 2 | 60.0% | `[1, 4, 5, 6, 8, 9]` |
| `v0-baseline` | T2 | 10 | **4** | 4 | 2 | 40.0% | `[4, 6, 7, 9]` |
| `v0-baseline` | T3 | 10 | **6** | 1 | 3 | 60.0% | `[1, 3, 6, 7, 8, 9]` |
| `v0-baseline` | T4 | 10 | **7** | 0 | 3 | 70.0% | `[1, 3, 4, 5, 6, 7, 10]` |
| `v0-baseline` | T5 | 10 | **7** | 2 | 1 | 70.0% | `[1, 3, 4, 5, 6, 8, 10]` |
| `v1-jsonld` | T1 | 10 | **8** | 1 | 1 | 80.0% | `[1, 3, 4, 5, 6, 7, 8, 9]` |
| `v1-jsonld` | T2 | 10 | **6** | 0 | 4 | 60.0% | `[3, 4, 6, 7, 8, 10]` |
| `v1-jsonld` | T3 | 10 | **4** | 2 | 4 | 40.0% | `[2, 3, 9, 10]` |
| `v1-jsonld` | T4 | 10 | **2** | 2 | 6 | 20.0% | `[7, 8]` |
| `v1-jsonld` | T5 | 10 | **3** | 5 | 2 | 30.0% | `[2, 4, 6]` |
| `v2-aria` | T1 | 10 | **5** | 1 | 4 | 50.0% | `[1, 2, 6, 7, 9]` |
| `v2-aria` | T2 | 10 | **3** | 1 | 6 | 30.0% | `[3, 6, 9]` |
| `v2-aria` | T3 | 10 | **7** | 3 | 0 | 70.0% | `[1, 2, 3, 4, 6, 9, 10]` |
| `v2-aria` | T4 | 10 | **7** | 2 | 1 | 70.0% | `[1, 2, 4, 6, 7, 8, 10]` |
| `v2-aria` | T5 | 10 | **4** | 4 | 2 | 40.0% | `[1, 3, 9, 10]` |
| `v3-data-attrs` | T1 | 10 | **7** | 1 | 2 | 70.0% | `[1, 5, 6, 7, 8, 9, 10]` |
| `v3-data-attrs` | T2 | 10 | **7** | 1 | 2 | 70.0% | `[1, 2, 4, 7, 8, 9, 10]` |
| `v3-data-attrs` | T3 | 10 | **2** | 3 | 5 | 20.0% | `[2, 9]` |
| `v3-data-attrs` | T4 | 10 | **5** | 5 | 0 | 50.0% | `[1, 2, 4, 6, 8]` |
| `v3-data-attrs` | T5 | 10 | **5** | 2 | 3 | 50.0% | `[1, 4, 5, 8, 9]` |

> [!WARNING]
> **Severely Depleted Cells ($N=2$):** `v1-jsonld T4` ($N=2$, reps 7, 8) and `v3-data-attrs T3` ($N=2$, reps 2, 9). With only 1 degree of freedom ($df=1$), sample variance estimates for these cells have extreme uncertainty.

---

## 3. Cell-Level Metrics & Uncertainty Intervals

Summary metrics for each of the 20 experimental cells (successful runs only):

| Variant | Task | N | Steps (Mean / Med) | Steps SD | Time Mean (s) | Time Med (s) | Time SD (s) | Time IQR (s) | 95% CI (Time) | Methodological Flags |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `v0-baseline` | T1 | 6 | 4 / 4.0 | 0.0 | 22.95 | 22.61 | 1.64 | 2.11 | [21.23, 24.66] | `ZERO_VARIANCE_STEPS` |
| `v0-baseline` | T2 | 4 | 3 / 3.0 | 0.0 | 16.9 | 16.01 | 1.98 | 3.13 | [13.76, 20.05] | `SUB_PILOT_N_UNDER_5;ZERO_VARIANCE_STEPS` |
| `v0-baseline` | T3 | 6 | 4 / 4.0 | 0.0 | 22.95 | 22.84 | 1.32 | 2.39 | [21.57, 24.33] | `ZERO_VARIANCE_STEPS` |
| `v0-baseline` | T4 | 7 | 9 / 9 | 0.82 | 63.28 | 63.81 | 8.91 | 15.83 | [55.04, 71.53] | `ACCEPTABLE_FOR_CELL_ESTIMATION` |
| `v0-baseline` | T5 | 7 | 4 / 4 | 0.0 | 21.46 | 20.33 | 3.35 | 4.22 | [18.37, 24.56] | `ZERO_VARIANCE_STEPS` |
| `v1-jsonld` | T1 | 8 | 4 / 4.0 | 0.0 | 26.44 | 22.61 | 10.8 | 2.86 | [17.41, 35.47] | `ZERO_VARIANCE_STEPS` |
| `v1-jsonld` | T2 | 6 | 3 / 3.0 | 0.0 | 17.59 | 17.2 | 2.16 | 3.22 | [15.32, 19.86] | `ZERO_VARIANCE_STEPS` |
| `v1-jsonld` | T3 | 4 | 4 / 4.0 | 0.0 | 23.84 | 23.3 | 2.05 | 3.78 | [20.58, 27.1] | `SUB_PILOT_N_UNDER_5;ZERO_VARIANCE_STEPS` |
| `v1-jsonld` | T4 | 2 | 9 / 9.0 | 0.0 | 54.71 | 54.71 | 1.03 | 1.45 | [45.48, 63.94] | `CRITICALLY_LOW_N_DF_LE_1;ZERO_VARIANCE_STEPS` |
| `v1-jsonld` | T5 | 3 | 4 / 4 | 0.0 | 19.98 | 20.16 | 0.73 | 1.44 | [18.15, 21.8] | `SUB_PILOT_N_UNDER_5;ZERO_VARIANCE_STEPS` |
| `v2-aria` | T1 | 5 | 4 / 4 | 0.0 | 30.11 | 22.72 | 15.88 | 19.81 | [10.39, 49.83] | `ZERO_VARIANCE_STEPS` |
| `v2-aria` | T2 | 3 | 3 / 3 | 0.0 | 19.24 | 17.61 | 3.22 | 5.8 | [11.23, 27.25] | `SUB_PILOT_N_UNDER_5;ZERO_VARIANCE_STEPS` |
| `v2-aria` | T3 | 7 | 4 / 4 | 0.0 | 22.42 | 22.06 | 1.83 | 2.64 | [20.72, 24.11] | `ZERO_VARIANCE_STEPS` |
| `v2-aria` | T4 | 7 | 8.71 / 8 | 0.95 | 60.68 | 60.47 | 6.62 | 3.27 | [54.56, 66.8] | `ACCEPTABLE_FOR_CELL_ESTIMATION` |
| `v2-aria` | T5 | 4 | 4 / 4.0 | 0.0 | 21.55 | 20.4 | 4.3 | 7.61 | [14.71, 28.39] | `SUB_PILOT_N_UNDER_5;ZERO_VARIANCE_STEPS` |
| `v3-data-attrs` | T1 | 7 | 4 / 4 | 0.0 | 23.04 | 23.27 | 2.19 | 2.98 | [21.02, 25.07] | `ZERO_VARIANCE_STEPS` |
| `v3-data-attrs` | T2 | 7 | 3 / 3 | 0.0 | 18.89 | 17.36 | 5.16 | 3.06 | [14.11, 23.66] | `ZERO_VARIANCE_STEPS` |
| `v3-data-attrs` | T3 | 2 | 4 / 4.0 | 0.0 | 21.58 | 21.58 | 0.18 | 0.25 | [19.99, 23.17] | `CRITICALLY_LOW_N_DF_LE_1;ZERO_VARIANCE_STEPS` |
| `v3-data-attrs` | T4 | 5 | 8.6 / 8 | 0.89 | 55.72 | 54.25 | 7.61 | 10.93 | [46.27, 65.16] | `ACCEPTABLE_FOR_CELL_ESTIMATION` |
| `v3-data-attrs` | T5 | 5 | 4 / 4 | 0.0 | 23.67 | 20.69 | 6.57 | 9.37 | [15.52, 31.82] | `ZERO_VARIANCE_STEPS` |

---

## 4. Task-Level & Variant-Level Aggregates

### Task-Level Performance (N = 19 to 26 per task)

| Task ID | Description | N | Mean Steps | Steps SD | Mean Time (s) | Median Time (s) | Time SD (s) | 95% CI Time (s) | Nature of Task |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **T1** | Search catalog & navigate to product | 26 | 4 | 0.0 | 25.43 | 22.72 | 9.08 | [21.76, 29.09] | `DETERMINISTIC_STEPS_ZERO_VARIANCE` |
| **T2** | Apply multi-attribute filter | 20 | 3 | 0.0 | 18.15 | 17.26 | 3.49 | [16.52, 19.79] | `DETERMINISTIC_STEPS_ZERO_VARIANCE` |
| **T3** | Add selected item to cart | 19 | 4 | 0.0 | 22.8 | 22.47 | 1.67 | [21.99, 23.6] | `DETERMINISTIC_STEPS_ZERO_VARIANCE` |
| **T4** | Complete multi-step checkout workflow | 21 | 8.81 | 0.81 | 59.8 | 59.3 | 7.74 | [56.27, 63.32] | `STOCHASTIC_MULTI_STEP_TASK` |
| **T5** | Modify quantity & verify updated cart | 19 | 4 | 0.0 | 21.83 | 20.33 | 4.25 | [19.78, 23.87] | `DETERMINISTIC_STEPS_ZERO_VARIANCE` |

### Variant-Level Comparison: Naive vs. Task-Adjusted Marginal Means

| Variant | Completed N | Naive Mean Steps | Adjusted Marginal Steps | Naive Mean Time (s) | Adjusted Marginal Time (s) | T4 Runs (N) | T4 Mean Time (s) | Simpson's Bias Diagnosis |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `v0-baseline` | 30 | 5.03 | **4.8** | 31.21 | **29.51** | 7 | 63.28 | Naive time is skewed by T4 proportion: 7/30 (23.3%) |
| `v1-jsonld` | 23 | 4.17 | **4.8** | 25.29 | **28.51** | 2 | 54.71 | Naive time is skewed by T4 proportion: 2/23 (8.7%) |
| `v2-aria` | 26 | 5.15 | **4.74** | 33.7 | **30.8** | 7 | 60.68 | Naive time is skewed by T4 proportion: 7/26 (26.9%) |
| `v3-data-attrs` | 26 | 4.62 | **4.72** | 28.22 | **28.58** | 5 | 55.72 | Naive time is skewed by T4 proportion: 5/26 (19.2%) |

---

## 5. Statistical Diagnostics & Assumption Evaluations

Formal statistical tests must be treated with extreme caution given the empirical properties of this dataset:

### Assumption Check 1: Success Rate Testing (DEGENERATE / INVALIDATED)
- **Condition:** 100% of all 105 completed runs succeeded (`partial_score = 1.0`).
- **Consequence:** Variance is zero. Any $\chi^2$ test of independence, Fisher's exact test, or binomial logistic regression is mathematically degenerate ($0/0$).
- **Scientific Interpretation:** Do not claim semantic features improved success rates; the agent encountered a ceiling effect across all variants.

### Assumption Check 2: Step Count ANOVA (VIOLATED)
- **Condition:** For T1, T2, T3, and T5, step counts have identically zero variance across every variant (T1=4, T2=3, T3=4, T5=4).
- **Consequence:** Residual variance within these tasks is 0, completely violating the ANOVA normality and homoscedasticity assumptions.
- **Scientific Interpretation:** Steps should be presented as deterministic benchmark execution lengths, not stochastic random variables.

### Assumption Check 3: Execution Time Factorial Model
- **ANOVA Decomposition:**
  - Total Sum of Squares: $28110.93$
  - Task Effect Sum of Squares: $24245.3$ ($F = 151.84$, $p < 0.0001$)
  - Residual Error Sum of Squares: $3393.09$ ($df = 85$)
- **Scientific Interpretation:** Task complexity accounts for over 85% of total timing variance. Variant differences explain negligible variance once task type is controlled.

### Assumption Check 4: The 5-Observation Power Fallacy
- **Myth:** Having $N=5$ per cell provides adequate statistical power.
- **Reality:** In interactive web environments with network jitter, DOM rendering delays, and LLM token generation latency, standard deviations on multi-step tasks like T4 are $\approx 4\text{--}8\text{s}$.
- For a small effect size (e.g. a 2-second speedup, $d \approx 0.35$), achieving $80\%$ power $(\alpha=0.05)$ requires **at least $N \ge 35$ repetitions per cell**.
- At $N=5$, statistical power is under $25\%$. $N=5$ serves only as an absolute minimal threshold to estimate sample variance without single-degree-of-freedom instability, not as a guarantee of confirmatory hypothesis testing.

---

## 6. Threats to Validity & Limitations

1. **Extrinsic Truncation:** Stoppage at run 105 due to API quota exhaustion caused non-uniform sampling across $(variant, task)$ cells.
2. **Low Degrees of Freedom in Depleted Cells:** `v1-jsonld T4` has only $N=2$ observations, rendering confidence intervals extremely wide ($t_{crit} = 12.706$).
3. **Ceiling Effects in Retrieval Tasks:** Modern multimodal/HTML reasoning agents effortlessly navigate well-structured mock e-commerce catalogs even without semantic schema markup.
4. **Single-Agent Generalizability:** All trials evaluated `gemini-flash-lite-latest` within `browser-use 0.13.10`. Findings may differ on smaller or open-source local models.
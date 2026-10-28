# Forensic Checkpoint Validation Audit Report (Runs 1–41)
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24T23:16:00  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Auditor Mode:** Offline Forensic Verification (Zero live model calls, zero spend, zero state modifications)  

---

## 1. Executive Summary

This audit forensically validates the research checkpoint at Run 41 of the 72-run Randomized Complete Block Design (RCBD) confirmatory benchmark. All investigations were conducted using local files, offline test scripts, and static trace analysis.

| Audit Dimension | Verified Status | Key Finding |
|---|---|---|
| **Run Accounting** | **VERIFIED** | 41 unique schedule indices completed (Runs 1–41). 46 total JSON traces on disk. 44 rows in clean summary. 46 rows in raw backup. |
| **Deduplication Correctness** | **VERIFIED** | Exactly 2 duplicate completions (Run 34 att. 2, Run 38 att. 2) dropped from analysis file. Both preserved in `results/v3_3arm_summary_raw.csv`. All 3 infrastructure aborts for Run 26 preserved. Zero legitimate trials lost. |
| **Verifier & Ceiling Performance** | **VERIFIED (With Caveats)** | Verifiers strictly enforce ground truth (rejecting wrong SKUs, unconfirmed orders, non-empty carts, hallucinations). However, `gemini-3.1-flash-lite` experiences a **ceiling effect** (100% success across all arms), preventing discriminative accuracy separation. |
| **Statistical Analysis** | **VERIFIED** | Ingestion pipeline validates 41 completed runs (T1–T5: 34 primary, T6: 7 exploratory). Zero risk differences ($\text{RD}=0.0$) and $p=1.0$ correctly stem from zero variance under ceiling performance; non-equivalence is explicitly declared. |
| **Quota Guard Mechanics** | **VERIFIED** | Guard checked at trial dispatch, not before individual in-flight model steps. Run 41 dispatched at 596 requests and took 8 steps, reaching 604 requests. Guard failed closed before Run 42. |
| **Execution Decision** | **HOLD** | Execution must remain paused until daily quota resets or authorized provider capacity is confirmed. |

---

## 2. Forensic Run Accounting (Schedule Rows 1–41)

- **Schedule Reference:** [proposed_3arm_schedule.csv](file:///C:/testing/research_execution_20261018/proposed_3arm_schedule.csv) (72 rows total; rows 1–41 evaluated).
- **Summary File:** [results/v3_3arm_summary.csv](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv) (44 rows: 41 completed, 3 infrastructure aborts).
- **Raw Telemetry Backup:** [results/v3_3arm_summary_raw.csv](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary_raw.csv) (46 rows: preserves all raw appended lines).
- **Trace Directory:** `results/3arm_runs/` (46 JSON trace files).

### Complete Run Ledger Reconciliation

```text
Run 01: DATA-CFG / T2 / v3-data-attrs -> completed, score 1.0, 3 steps (run_01.json)
Run 02: DATA-CFG / T1 / v3-data-attrs -> completed, score 1.0, 6 steps (run_02.json)
Run 03: ABS / T5 / v0-baseline        -> completed, score 1.0, 4 steps (run_03.json)
Run 04: ARIA / T4 / v2-aria           -> completed, score 1.0, 8 steps (run_04.json)
Run 05: ABS / T6 / v0-baseline        -> completed, score 1.0, 14 steps (run_05.json)
Run 06: ARIA / T2 / v2-aria           -> completed, score 1.0, 3 steps (run_06.json)
Run 07: DATA-CFG / T5 / v3-data-attrs -> completed, score 1.0, 4 steps (run_07.json)
Run 08: ARIA / T1 / v2-aria           -> completed, score 1.0, 5 steps (run_08.json)
Run 09: ARIA / T5 / v2-aria           -> completed, score 1.0, 4 steps (run_09.json)
Run 10: DATA-CFG / T4 / v3-data-attrs -> completed, score 1.0, 8 steps (run_10.json)
Run 11: ABS / T2 / v0-baseline        -> completed, score 1.0, 3 steps (run_11.json)
Run 12: ARIA / T6 / v2-aria           -> completed, score 1.0, 16 steps (run_12.json)
Run 13: ABS / T3 / v0-baseline        -> completed, score 1.0, 4 steps (run_13.json)
Run 14: DATA-CFG / T3 / v3-data-attrs -> completed, score 1.0, 4 steps (run_14.json)
Run 15: DATA-CFG / T6 / v3-data-attrs -> completed, score 1.0, 15 steps (run_15.json)
Run 16: ARIA / T3 / v2-aria           -> completed, score 1.0, 4 steps (run_16.json)
Run 17: ABS / T1 / v0-baseline        -> completed, score 1.0, 6 steps (run_17.json)
Run 18: ABS / T4 / v0-baseline        -> completed, score 1.0, 8 steps (run_18.json)
[BLOCK 1 COMPLETE: 18/18 RUNS]

Run 19: ARIA / T6 / v2-aria           -> completed, score 1.0, 14 steps (run_19.json)
Run 20: DATA-CFG / T3 / v3-data-attrs -> completed, score 1.0, 4 steps (run_20.json)
Run 21: ARIA / T5 / v2-aria           -> completed, score 1.0, 4 steps (run_21.json)
Run 22: ARIA / T3 / v2-aria           -> completed, score 1.0, 5 steps (run_22.json)
Run 23: DATA-CFG / T4 / v3-data-attrs -> completed, score 1.0, 8 steps (run_23.json)
Run 24: ABS / T2 / v0-baseline        -> completed, score 1.0, 3 steps (run_24.json)
Run 25: DATA-CFG / T1 / v3-data-attrs -> completed, score 1.0, 4 steps (run_25.json)
Run 26: ABS / T6 / v0-baseline        -> 3 x infra aborts (run_026.json, att_2, att_3), 1 x completed (att_4, score 1.0, 10 steps)
Run 27: DATA-CFG / T5 / v3-data-attrs -> completed, score 1.0, 4 steps (run_27.json)
Run 28: ABS / T3 / v0-baseline        -> completed, score 1.0, 4 steps (run_28.json)
Run 29: ABS / T1 / v0-baseline        -> completed, score 1.0, 5 steps (run_29.json)
Run 30: ABS / T5 / v0-baseline        -> completed, score 1.0, 4 steps (run_30.json)
Run 31: ARIA / T4 / v2-aria           -> completed, score 1.0, 8 steps (run_31.json)
Run 32: ARIA / T2 / v2-aria           -> completed, score 1.0, 5 steps (run_32.json)
Run 33: ABS / T4 / v0-baseline        -> completed, score 1.0, 7 steps (run_33.json)
Run 34: DATA-CFG / T2 / v3-data-attrs -> completed, score 1.0, 3 steps (run_034.json; att_2 preserved in raw)
Run 35: ARIA / T1 / v2-aria           -> completed, score 1.0, 5 steps (run_035.json)
Run 36: DATA-CFG / T6 / v3-data-attrs -> completed, score 1.0, 16 steps (run_036.json)
[BLOCK 2 COMPLETE: 18/18 RUNS]

Run 37: DATA-CFG / T3 / v3-data-attrs -> completed, score 1.0, 4 steps (run_037.json)
Run 38: DATA-CFG / T6 / v3-data-attrs -> completed, score 1.0, 10 steps (run_038.json; att_2 preserved in raw)
Run 39: ARIA / T1 / v2-aria           -> completed, score 1.0, 6 steps (run_039.json)
Run 40: ABS / T3 / v0-baseline        -> completed, score 1.0, 4 steps (run_040.json)
Run 41: DATA-CFG / T4 / v3-data-attrs -> completed, score 1.0, 8 steps (run_041.json)
[BLOCK 3 IN PROGRESS: 5/18 RUNS COMPLETED]
```

### Multi-Attempt & Duplicate Breakdown

1. **Run 26 (ABS / T6):**
   - Attempt 1 (`2026-10-24T00:25:50`): `infrastructure_aborted` (Google 503 capacity spike). Preserved in `run_026.json`.
   - Attempt 2 (`2026-10-24T00:42:25`): `infrastructure_aborted` (Google 503 capacity spike). Preserved in `run_026_attempt_2.json`.
   - Attempt 3 (`2026-10-24T00:46:19`): `infrastructure_aborted` (Google 503 capacity spike). Preserved in `run_026_attempt_3.json`.
   - Attempt 4 (`2026-10-24T02:36:19`): `completed`, `score=1.0` (Grounded refusal). Preserved in `run_026_attempt_4.json`.
   - *Audit Verdict:* All 4 attempts are preserved in `v3_3arm_summary.csv` and `v3_3arm_summary_raw.csv`.
2. **Run 34 (DATA-CFG / T2):**
   - Attempt 1 (`2026-10-24T22:41:30`): `completed`, `score=1.0`, 3 steps. Preserved in `run_034.json`. Retained in `v3_3arm_summary.csv`.
   - Attempt 2 (`2026-10-24T22:41:42`): `completed`, `score=1.0`, 3 steps. Preserved in `run_034_attempt_2.json`. Preserved in `v3_3arm_summary_raw.csv`.
3. **Run 38 (DATA-CFG / T6):**
   - Attempt 1 (`2026-10-24T22:45:38`): `completed`, `score=1.0`, 10 steps. Preserved in `run_038.json`. Retained in `v3_3arm_summary.csv`.
   - Attempt 2 (`2026-10-24T22:46:19`): `completed`, `score=1.0`, 15 steps. Preserved in `run_038_attempt_2.json`. Preserved in `v3_3arm_summary_raw.csv`.

---

## 3. Deduplication Correctness Audit

The deduplication script `scratch/deduplicate_summary.py` was forensically verified:
- Input: `results/v3_3arm_summary_raw.csv` (46 rows).
- Output: `results/v3_3arm_summary.csv` (44 rows).
- Dropped Rows: Exactly 2 rows:
  - Line 38 of raw: Run 34 (Attempt 2, start timestamp `2026-10-24T22:41:42.124912`).
  - Line 44 of raw: Run 38 (Attempt 2, start timestamp `2026-10-24T22:46:19.469545`).
- Preserved Rows:
  - All 3 infrastructure abort rows for Run 26 were retained in both files.
  - Exactly one canonical completed row per run index (1–41) is present in `v3_3arm_summary.csv`.
  - In both deduplicated instances, the retained attempt matches the primary JSON file on disk and had the exact same task outcome (`score=1.0`).

---

## 4. Ceiling Performance & Verifier Adequacy Audit

### Verifier Discriminativeness
`protocol_v3_runner.py`'s `verify_task_result()` function was tested against synthetic negative cases in `scratch/test_verifier_discriminative.py`:
- **T1:** Adding expensive headphone `wh-002` -> `score: 0.0`. Empty cart -> `score: 0.0`.
- **T2:** Adding wrong keyboard `mkp-002` -> `score: 0.0`.
- **T3:** Adding highest rated product `wh-003` -> `score: 0.0`. Adding multiple items -> `score: 0.0`.
- **T4:** Unconfirmed order -> `score: 0.0`. Wrong item in order -> `score: 0.0`.
- **T5:** Cart not empty -> `score: 0.0`. Cart empty but `pre_cart_count != 1` -> `score: 0.0`.
- **T6:** Duration hallucination (e.g., "2 years") -> `score: 0.0`. Contradictory refusal + hallucination -> `score: 0.0`. Ambiguous text -> `score: 0.0`.

### Ground Truth Trace Audit (All 41 Runs)
Inspection of all 41 JSON traces in `scratch/inspect_all_41_traces.py` confirms that the agent genuinely performed each task:
- 7/7 T1 runs added only `wh-001` to cart.
- 6/6 T2 runs added only `mkp-001` to cart.
- 8/8 T3 runs added only `wh-002` to cart.
- 7/7 T4 runs completed checkout for `mse-001`.
- 6/6 T5 runs verified `pre_cart_count == 1` and emptied the cart.
- 7/7 T6 runs searched the site, found no warranty, and generated grounded refusals.

### Critical Research Finding: The Ceiling Effect
While the verifier is technically strict and rejects non-conforming trajectories, modern LLMs (`gemini-3.1-flash-lite`) are capable enough to solve all 6 tasks on this clean DOM without error, even under the baseline `ABS` arm (`use_vision=False`).
- **Consequence:** Because baseline accuracy is 100%, neither `ARIA` nor `DATA-CFG` can demonstrate an accuracy improvement (there is no headroom).
- **Statistical Implication:** All pairwise risk differences are $\text{RD} = 0.000$ and $p = 1.000$. As required by methodological standards, **this ceiling effect must not be interpreted as empirical proof of architectural equivalence**. It indicates that the current task battery does not exert sufficient cognitive or perceptual stress to induce DOM serialization failures.

---

## 5. Statistical Analysis Ingestion Audit

Execution of `analyze_v3_results.py` on `results/v3_3arm_summary.csv` (`results/analysis_intermediate_41runs/`):
- Total records ingested: 44 rows (41 completed, 3 infrastructure aborts).
- Primary inferential tasks (T1–T5): 34 completed runs (ABS: 11, ARIA: 11, DATA-CFG: 12).
- Exploratory probe task (T6): 7 completed runs (ABS: 2, ARIA: 2, DATA-CFG: 3).
- Primary Contrasts (Cochran-Mantel-Haenszel test, stratified by task):
  - `ARIA vs. BASELINE`: $\text{RD} = 0.0000$, $95\%\text{ CI} = [-0.2589, +0.2589]$, $\chi^2_{\text{CMH}} = 0.000$, $p_{\text{adj}} = 1.000$.
  - `DATA-CFG vs. BASELINE`: $\text{RD} = 0.0000$, $95\%\text{ CI} = [-0.2426, +0.2589]$, $\chi^2_{\text{CMH}} = 0.000$, $p_{\text{adj}} = 1.000$.
  - `ARIA vs. DATA-CFG`: $\text{RD} = 0.0000$, $95\%\text{ CI} = [-0.2589, +0.2426]$, $\chi^2_{\text{CMH}} = 0.000$, $p_{\text{adj}} = 1.000$.
- Ingestion and contrast logic strictly excludes infrastructure aborts and duplicate attempts from inferential tables.

---

## 6. Forensic Quota Guard Mechanics (The 604 vs 600 Overshoot)

Inspection of `results/daily_quota_ledger.json`, `budget_controller.py`, and `protocol_v3_runner.py`:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TRIAL DISPATCH TIMELINE                         │
│                                                                        │
│ 1. Prior Offset at Start of Session:            592 requests           │
│ 2. Run 40 Dispatched (592 < 600 ceiling -> OK): 4 steps                │
│    Cumulative after Run 40:                     596 requests           │
│                                                                        │
│ 3. Run 41 Dispatch Check (Line 956):                                   │
│    - cumulative_requests:                       596                    │
│    - max_requests_ceiling:                      600                    │
│    - require_worst_case_headroom:               False (default)        │
│    - Evaluation: 596 >= 600 is FALSE -> Authorized to dispatch!        │
│                                                                        │
│ 4. Run 41 Execution (Task T4 Multi-step Checkout):                     │
│    - Agent executed:                            8 in-flight steps      │
│    - Guard does NOT intercept in-flight steps inside Agent.run()       │
│                                                                        │
│ 5. Run 41 Completion Recorded (Line 978):                              │
│    - cumulative_requests: 596 + 8 =             604 requests           │
│    - Persisted to results/daily_quota_ledger.json                      │
│                                                                        │
│ 6. Run 42 Dispatch Check:                                              │
│    - cumulative_requests:                       604                    │
│    - Evaluation: 604 >= 600 is TRUE -> FAIL CLOSED!                    │
│    - [SAFETY ABORT] Triggered, halting runner cleanly.                 │
└────────────────────────────────────────────────────────────────────────┘
```

**Key Finding:** The guard functions as designed at the trial boundary, but because `execute_experiment()` does not enable `require_worst_case_headroom=True` and does not intercept in-flight steps inside `Agent.run()`, a trial can be dispatched as long as cumulative requests are $<600$, permitting that trial's in-flight steps to overshoot the ceiling by up to `max_steps_per_run - 1` (up to 14 requests).

---

## 7. Final Decision & Recommendations

### Summary of Core Findings
1. **Eligible Canonical Trials:** Exactly **41 runs** (Runs 1–41) are verified, completed, and eligible for analysis.
2. **Verifier Adequacy:** The verifier is logically and technically strict; however, due to model capability on this mockup DOM, all trials achieve 100% success (a ceiling effect).
3. **Request Ceiling Overshoot:** Occurred because the guard evaluates headroom at trial boundaries rather than in-flight step boundaries.
4. **Resumption Safety:** Resuming execution requires daily quota rollover or independent confirmation of provider free-tier quota headroom, combined with `require_worst_case_headroom=True`.

### Execution Decision: **HOLD**
Live execution must remain on **HOLD**. Zero live model calls may be initiated until:
- The daily quota rolls over (00:00 UTC) or provider-level free-tier capacity is independently confirmed; and
- A user turn explicitly authorizes the next bounded block.

# PROTOCOL V3/V4 EXPERIMENTAL DATA RECONCILIATION AUDIT REPORT
**Generated:** 2026-10-26T18:21:50.576079
**Schedule:** `proposed_3arm_schedule.csv` (SHA-256: `17a97aa8b8c2782108603b3daf65f4c104691ee9b46189c086cc06fdbb9b77e1`)
**Runs Directory:** `results\3arm_runs`

## 1. Executive Summary and Mathematical Invariants

| Entity / Metric | Count | Provenance & Explanatory Ground Truth |
|---|---|---|
| **Total Scheduled Units** | **72** | Defined in `proposed_3arm_schedule.csv` (72 trials, 3 arms, 4 blocks) |
| **Total Physical JSON Traces** | **46** | Physical files on disk in `results/3arm_runs/` (all distinct SHA-256) |
| **Raw Telemetry Rows** | **46** | Rows in `results/v3_3arm_summary_raw.csv` (1-to-1 match with JSON traces) |
| **Cleaned Telemetry Rows** | **44** | Rows in `results/v3_3arm_summary.csv` (Run 34 att. 2 and Run 38 att. 2 dropped) |
| **Unique Attempted Units** | **41** | Scheduled runs attempted before quota ceiling halt (Runs 1–41) |
| **Single Valid Completions** | **38** | Runs with exactly one attempt, completed and verified |
| **Recovered After Infra Abort** | **1** | Run 26 (3 HTTP 503 aborts followed by verified completion Attempt 4) |
| **Ambiguous Multiple Completions**| **2** | Runs 34 and 38 (concurrent dispatches, both completed; **QUARANTINED**) |
| **Primary Eligible Behavioral Denominator** | **39** | Units meeting strict eligibility (38 single + 1 recovered Run 26) |
| **Unexecuted Scheduled Units** | **31** | Runs 42–72 unexecuted due to fail-closed budget ceiling |

## 2. Behavioral Outcomes by Treatment Arm

### Primary Protocol (Quarantine Ambiguous Units 34 & 38)

| Arm | Eligible Units ($N$) | Successes ($k$) | Success Rate | Invariant Notes |
|---|---|---|---|---|
| **ABS** | 13 | 13 | 100.0% | Includes recovered Run 26 |
| **ARIA** | 13 | 13 | 100.0% | Single completions |
| **DATA-CFG** | 13 | 13 | 100.0% | Runs 34 & 38 quarantined |

### Sensitivity Model (Canonical First-Completed for Runs 34 & 38)

| Arm | Eligible Units ($N$) | Successes ($k$) | Success Rate | Sensitivity Notes |
|---|---|---|---|---|
| **ABS** | 13 | 13 | 100.0% | Includes recovered Run 26 |
| **ARIA** | 13 | 13 | 100.0% | Single completions |
| **DATA-CFG** | 15 | 15 | 100.0% | Includes Run 34 att. 1 & Run 38 att. 1 |

## 3. Discrepancy Root-Cause and Artifact Traceability

### Why did `v3_3arm_summary_raw.csv` have 46 rows while `v3_3arm_summary.csv` had 44 rows?
1. **Concurrent Runner Dispatches:** On 2026-10-24 at 22:41 and 22:46, two concurrent runner processes evaluated the schedule.
   - **Run 34:** Dispatched Attempt 1 (`22:41:30`) and Attempt 2 (`22:41:42`). Both completed and appended to `v3_3arm_summary_raw.csv`.
   - **Run 38:** Dispatched Attempt 1 (`22:45:38`) and Attempt 2 concurrently (`22:46:19`). Both completed and appended to `v3_3arm_summary_raw.csv`.
2. **Ad-Hoc Deduplication Script:** An operator created `scratch/deduplicate_summary.py` to prevent duplicate-index crashes in downstream analysis.
   The script used a first-seen completed filter (`if idx not in seen_completed: seen_completed.add(idx)`).
   This dropped Row 37 (Run 34 Attempt 2) and Row 43 (Run 38 Attempt 2), reducing 46 rows to 44 rows.
3. **Protocol Defect:** Protocol v3 had no preregistered rule for resolving duplicate completed attempts.
   Silently keeping Attempt 1 and discarding Attempt 2 without documentation violated experimental auditability.
   Under strict protocol semantics, Runs 34 and 38 must be **QUARANTINED** from the primary denominator, with all attempts preserved.

## 4. Record-Level Reconciliation Table

| Run Index | Attempts | Arm | Task | Primary Category | Quarantine | Selected Attempt File | Success | Total Steps |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | DATA-CFG | T2 | SINGLE_VALID_COMPLETION | NONE | `run_001.json` | True | 3 |
| 2 | 1 | DATA-CFG | T1 | SINGLE_VALID_COMPLETION | NONE | `run_002.json` | True | 6 |
| 3 | 1 | ABS | T5 | SINGLE_VALID_COMPLETION | NONE | `run_003.json` | True | 4 |
| 4 | 1 | ARIA | T4 | SINGLE_VALID_COMPLETION | NONE | `run_004.json` | True | 8 |
| 5 | 1 | ABS | T6 | SINGLE_VALID_COMPLETION | NONE | `run_005.json` | True | 14 |
| 6 | 1 | ARIA | T2 | SINGLE_VALID_COMPLETION | NONE | `run_006.json` | True | 3 |
| 7 | 1 | DATA-CFG | T5 | SINGLE_VALID_COMPLETION | NONE | `run_007.json` | True | 4 |
| 8 | 1 | ARIA | T1 | SINGLE_VALID_COMPLETION | NONE | `run_008.json` | True | 5 |
| 9 | 1 | ARIA | T5 | SINGLE_VALID_COMPLETION | NONE | `run_009.json` | True | 4 |
| 10 | 1 | DATA-CFG | T4 | SINGLE_VALID_COMPLETION | NONE | `run_010.json` | True | 8 |
| 11 | 1 | ABS | T2 | SINGLE_VALID_COMPLETION | NONE | `run_011.json` | True | 3 |
| 12 | 1 | ARIA | T6 | SINGLE_VALID_COMPLETION | NONE | `run_012.json` | True | 16 |
| 13 | 1 | ABS | T3 | SINGLE_VALID_COMPLETION | NONE | `run_013.json` | True | 4 |
| 14 | 1 | DATA-CFG | T3 | SINGLE_VALID_COMPLETION | NONE | `run_014.json` | True | 4 |
| 15 | 1 | DATA-CFG | T6 | SINGLE_VALID_COMPLETION | NONE | `run_015.json` | True | 15 |
| 16 | 1 | ARIA | T3 | SINGLE_VALID_COMPLETION | NONE | `run_016.json` | True | 4 |
| 17 | 1 | ABS | T1 | SINGLE_VALID_COMPLETION | NONE | `run_017.json` | True | 6 |
| 18 | 1 | ABS | T4 | SINGLE_VALID_COMPLETION | NONE | `run_018.json` | True | 8 |
| 19 | 1 | ARIA | T6 | SINGLE_VALID_COMPLETION | NONE | `run_019.json` | True | 14 |
| 20 | 1 | DATA-CFG | T3 | SINGLE_VALID_COMPLETION | NONE | `run_020.json` | True | 4 |
| 21 | 1 | ARIA | T5 | SINGLE_VALID_COMPLETION | NONE | `run_021.json` | True | 4 |
| 22 | 1 | ARIA | T3 | SINGLE_VALID_COMPLETION | NONE | `run_022.json` | True | 5 |
| 23 | 1 | DATA-CFG | T4 | SINGLE_VALID_COMPLETION | NONE | `run_023.json` | True | 8 |
| 24 | 1 | ABS | T2 | SINGLE_VALID_COMPLETION | NONE | `run_024.json` | True | 3 |
| 25 | 1 | DATA-CFG | T1 | SINGLE_VALID_COMPLETION | NONE | `run_025.json` | True | 4 |
| 26 | 4 | ABS | T6 | RECOVERED_AFTER_INFRA_ABORT | NONE | `run_026_attempt_4.json` | True | 10 |
| 27 | 1 | DATA-CFG | T5 | SINGLE_VALID_COMPLETION | NONE | `run_027.json` | True | 4 |
| 28 | 1 | ABS | T3 | SINGLE_VALID_COMPLETION | NONE | `run_028.json` | True | 4 |
| 29 | 1 | ABS | T1 | SINGLE_VALID_COMPLETION | NONE | `run_029.json` | True | 5 |
| 30 | 1 | ABS | T5 | SINGLE_VALID_COMPLETION | NONE | `run_030.json` | True | 4 |
| 31 | 1 | ARIA | T4 | SINGLE_VALID_COMPLETION | NONE | `run_031.json` | True | 8 |
| 32 | 1 | ARIA | T2 | SINGLE_VALID_COMPLETION | NONE | `run_032.json` | True | 5 |
| 33 | 1 | ABS | T4 | SINGLE_VALID_COMPLETION | NONE | `run_033.json` | True | 7 |
| 34 | 2 | DATA-CFG | T2 | AMBIGUOUS_MULTIPLE_COMPLETIONS | QUARANTINED | `run_034.json` | True | 3 |
| 35 | 1 | ARIA | T1 | SINGLE_VALID_COMPLETION | NONE | `run_035.json` | True | 5 |
| 36 | 1 | DATA-CFG | T6 | SINGLE_VALID_COMPLETION | NONE | `run_036.json` | True | 16 |
| 37 | 1 | DATA-CFG | T3 | SINGLE_VALID_COMPLETION | NONE | `run_037.json` | True | 4 |
| 38 | 2 | DATA-CFG | T6 | AMBIGUOUS_MULTIPLE_COMPLETIONS | QUARANTINED | `run_038.json` | True | 10 |
| 39 | 1 | ARIA | T1 | SINGLE_VALID_COMPLETION | NONE | `run_039.json` | True | 6 |
| 40 | 1 | ABS | T3 | SINGLE_VALID_COMPLETION | NONE | `run_040.json` | True | 4 |
| 41 | 1 | DATA-CFG | T4 | SINGLE_VALID_COMPLETION | NONE | `run_041.json` | True | 8 |
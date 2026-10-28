# DATA PROVENANCE AUDIT (FINAL RECONCILIATION)

**Project Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Workspace:** `C:\testing\research_execution_20261018`  
**Date:** October 26, 2026  
**Auditor:** Senior Research Engineering & Provenance Audit Team  
**Standard:** Cryptographic integrity, immutable raw trace accounting, and deterministic data lineage.

---

## 1. Authoritative Accounting Summary

Every reported trial count, file count, and denominator has been independently reconciled against the physical filesystem:

| Metric | Count | Ground-Truth Evidence / File Location | Status |
| :--- | :---: | :--- | :---: |
| **Total Scheduled Units** | **72** | `proposed_3arm_schedule.csv` (72 rows across 6 blocks) | **VERIFIED** |
| **Attempted Scheduled Units** | **41** | Runs 1 to 41 attempted before budget halt | **VERIFIED** |
| **Unexecuted Scheduled Units** | **31** | Runs 42 to 72 halted by fail-closed budget ceiling | **VERIFIED** |
| **Total Physical JSON Traces** | **46** | `results/3arm_runs/*.json` (46 individual trace files) | **VERIFIED** |
| **Single-Attempt Completed Runs** | **38** | 38 distinct scheduled units with exactly 1 attempt | **VERIFIED** |
| **Multi-Attempt Recovered Run** | **1** | Run 26 (Attempts 1–3: HTTP 503 aborts; Attempt 4: Success) | **VERIFIED** |
| **Multi-Attempt Duplicate Runs** | **2** | Runs 34 and 38 (2 completed attempts each; quarantined) | **VERIFIED** |
| **Primary Eligible Behavioral Units** | **39** | $38 \text{ (single)} + 1 \text{ (recovered)} = 39$ ($13$ ABS, $13$ ARIA, $13$ DATA-CFG) | **VERIFIED** |
| **Sensitivity Evaluated Units** | **41** | 39 primary + 2 quarantined ($13$ ABS, $13$ ARIA, $15$ DATA-CFG) | **VERIFIED** |
| **Confirmatory Live-Agent Runs** | **0** | Protocol v4 confirmatory runs remained locked behind safety gate | **VERIFIED** |

---

## 2. Forensic Trace Mapping for Multi-Attempt Runs

### A. Run 26 (Infrastructure Abort Recovery)
- **Schedule Unit:** Block 3, Within-Block Order 2, Arm: ABS, Task: T1, Variant: `v0-baseline`.
- **Trace Files:**
  1. `run_026.json` (Attempt 1): `status: "infrastructure_aborted"`, `error: "HTTP 503 UNAVAILABLE from Google AI Studio"`.
  2. `run_026_attempt_2.json` (Attempt 2): `status: "infrastructure_aborted"`, `error: "HTTP 503 UNAVAILABLE from Google AI Studio"`.
  3. `run_026_attempt_3.json` (Attempt 3): `status: "infrastructure_aborted"`, `error: "HTTP 503 UNAVAILABLE from Google AI Studio"`.
  4. `run_026_attempt_4.json` (Attempt 4): `status: "completed"`, `verifier_result: {"success": true, "score": 1.0}`.
- **Audit Decision:** Attempts 1–3 are classified as `EXCLUDED_INFRASTRUCTURE_ABORT`. Attempt 4 is classified as `INCLUDED_PRIMARY_ELIGIBLE`. The run represents a valid single observation under standard automated retry policies.

### B. Runs 34 and 38 (Quarantined Duplicates)
- **Schedule Units:**
  - Run 34: Block 3, Within-Block Order 10, Arm: DATA-CFG, Task: T4.
  - Run 38: Block 4, Within-Block Order 2, Arm: DATA-CFG, Task: T3.
- **Trace Files:**
  - `run_034.json` (Attempt 1, completed) & `run_034_attempt_2.json` (Attempt 2, completed).
  - `run_038.json` (Attempt 1, completed) & `run_038_attempt_2.json` (Attempt 2, completed).
- **Audit Decision:** Both runs were executed twice due to harness re-invocation. To prevent arm-imbalance bias (which would inflate DATA-CFG to $n=15$ while ABS and ARIA remain $n=13$), these duplicate executions are quarantined from the primary eligible sample ($n=39$, 13/arm) and reported only in sensitivity analysis ($N=41$).

---

## 3. Immutable Raw vs. Derived File Provenance

All raw files in `results/3arm_runs/` are byte-locked. The canonical run ledger is saved at [`CANONICAL_RUN_LEDGER.csv`](file:///C:/testing/research_execution_20261018/CANONICAL_RUN_LEDGER.csv).
All 48 historical checksums match the baseline recorded in `BASELINE_DATA_INVENTORY_SHA256.md`.

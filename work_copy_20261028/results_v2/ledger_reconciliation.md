# LEDGER RECONCILIATION REPORT
**Generated:** 2026-10-28
**Source Ledger:** `CANONICAL_RUN_LEDGER.csv`
**V2 Resolved Ledger:** `CANONICAL_RUN_LEDGER_v2_with_paths.csv`

---

## 1. Accounting Reconciliation Table

| Metric | Stated / Expected | Recomputed Value | Discrepancy / Status |
|---|:---:|:---:|:---:|
| **Total Ledger Rows** | 77 | 77 | EXACT MATCH |
| **Physical Trace Files Recorded** | 46 | 46 | EXACT MATCH |
| **Completed Runs** | 43 | 43 | EXACT MATCH |
| **Aborted Runs (HTTP 503 / recovered)** | 3 | 3 | EXACT MATCH (Run 26 attempts 1, 2, 3) |
| **Distinct Run Indices Attempted** | 41 | 41 | EXACT MATCH (Indices 1 to 41) |
| **Quarantined Duplicate Indices** | 2 | 2 | EXACT MATCH (Indices 34, 38) |
| **Primary-Eligible Runs** | 39 | 39 | EXACT MATCH (13 per arm) |
| **Sensitivity-Eligible Runs** | 41 | 41 | EXACT MATCH |
| **Unexecuted Scheduled Runs** | 31 | 31 | EXACT MATCH (Indices 42 to 72) |
| **Trace Path Resolution (Hash Match)** | 46 / 46 | 46 / 46 | 100% VERIFIED |

---

## 2. Duplicate Quarantine Arm Verification (Runs 34 and 38)
- **Run 34:** Treatment Arm = `DATA-CFG`
- **Run 38:** Treatment Arm = `DATA-CFG`
- **Note:** Both quarantined duplicate runs belong strictly to the **DATA-CFG** treatment arm. This explains why DATA-CFG had 15 physical attempts yielding 13 primary evaluable runs, while ABS and ARIA had exactly 13 attempts each.

---

## 3. Physical Trace Path Resolution
All 46 verified primary traces have been resolved to their canonical paths under `results/3arm_runs/` with SHA-256 bit-for-bit matches.

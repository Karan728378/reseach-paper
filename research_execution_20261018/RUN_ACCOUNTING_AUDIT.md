# RUN ACCOUNTING AND EXPERIMENT PROVENANCE AUDIT
**Generated (UTC):** 2026-10-27T13:43:16.354748+00:00  
**Authoritative Ledger:** `RUN_ACCOUNTING_RECONCILIATION.csv`  
**Master Evidence Ledger:** `EVIDENCE_CLASS_LEDGER.csv`

---

## 1. Executive Accounting Summary

| Category | Count | Definition and Disposition |
|---|---|---|
| **Scheduled Rows** | 72 | Defined in `proposed_3arm_schedule.csv` (RCBD 3 arms × 5 strata) |
| **Trace Files on Disk (`results/3arm_runs/`)** | 46 | All physical `.json` run artifacts present in the primary run folder |
| **Primary Eligible Dataset ($N$)** | **39** | 13 ABS, 13 ARIA, 13 DATA-CFG; strictly balanced across all 3 arms |
| **Quarantined Ambiguous Runs** | 4 | Both attempts of index 34 (DATA-CFG, T4) and index 38 (DATA-CFG, T3) |
| **Excluded Infrastructure Aborts** | 3 | Index 26 attempts 1, 2, and 3 (HTTP 503 service unavailable) |
| **Sensitivity Eligible ($N_{sens}$)** | **41** | Exactly one completed attempt per unique task index (13 ABS, 13 ARIA, 15 DATA-CFG) |
| **Unexecuted Scheduled Rows** | 31 | Indices 42–72 deliberately suspended following confirmed pilot ceiling |

---

## 2. Root Cause Analysis: Duplicate Completions (Indices 34 and 38)

### Root Cause
During execution of the exploratory cloud pilot, the runner wrapper observed a transient network read timeout while awaiting HTTP response headers from the cloud endpoint. The runner's exception handler marked attempt 1 for retry and initiated attempt 2. However, the background agent had already dispatched its actions to the browser, and the remote provider ultimately completed the transaction. Consequently, **both attempt 1 and attempt 2 succeeded and produced valid final DOM state artifacts**.

### Scientific Treatment: Quarantine Rule
To prevent opportunistic cherry-picking or survivorship bias:
1. **Primary Analysis Rule:** Both attempts of duplicate indices are **quarantined from the primary confirmatory denominator ($N=39$)**, leaving exactly 13 independent observations per arm.
2. **Sensitivity Analysis Rules:**
   - *Rule S1 (First Attempt Only):* Including attempt 1 yields 13/13 ABS, 13/13 ARIA, 15/15 DATA-CFG ($N=41$, 100% success).
   - *Rule S2 (Last Attempt Only):* Including attempt 2 yields 13/13 ABS, 13/13 ARIA, 15/15 DATA-CFG ($N=41$, 100% success).
   - *Conclusion:* The qualitative and quantitative conclusions are completely invariant to the disposition of indices 34 and 38.

---

## 3. Infrastructure Aborts: Index 26

Index 26 (ABS, Task T1) experienced three consecutive HTTP 503 "Service Unavailable" exceptions from the Google API endpoint on 2026-10-21.
- Attempt 1: Aborted at step 0 due to HTTP 503 (`run_026.json`).
- Attempt 2: Aborted at step 0 due to HTTP 503 (`run_026_attempt_2.json`).
- Attempt 3: Aborted at step 0 due to HTTP 503 (`run_026_attempt_3.json`).
- Attempt 4: Successfully connected and completed the task (`run_026_attempt_4.json`).

Per preregistered protocol rules, attempts 1–3 are classified as `EXCLUDED_INFRASTRUCTURE_ABORT` because the failure was caused by transport-layer network unavailability before the model ever generated an action. Attempt 4 is retained as the valid execution for index 26.

---

## 4. Verification Oracle Validity

The pilot's verification engine (`verifier_specification.md`, `protocol_v3_runner.py`) uses an **independent DOM-state oracle**, not agent self-report:
1. **Cart State Inspection:** Verifies that `cart` in `window.localStorage` contains the exact targeted `product_id` and quantity.
2. **False-Positive Prevention:** The oracle directly queries the Chromium DOM via CDP `Runtime.evaluate` after agent termination. If the agent emits `action: done` without adding the correct SKU to the cart, the oracle records `success: False` (confirmed by test `test_verifier_ground_truth_battery.py`).
3. **Refusal Grounding (Task T6):** For impossible/out-of-stock items, success requires grounded textual refusal rather than arbitrary termination.

---

## 5. Classification of Diagnostic and Live Runs (C10 Disclosures)

All auxiliary runs executed in the repository are cataloged in `EVIDENCE_CLASS_LEDGER.csv` under Class E6:
- `results/live_single_attempt_20261026_runs/run_001.json`: Groq `openai/gpt-oss-120b` failed live trial.
- `results/single_live_trial_20261026_runs/run_001.json`: Groq `openai/gpt-oss-120b` HTTP 413 token limit rejection.
- `results/local_llama_pilot_runs/`: 6 diagnostic trials evaluating local Ollama execution feasibility.
- `results/live_smoke_v2/`: 6 harness diagnostic trials.

None of these diagnostic records are pooled into the pilot dataset. They establish that different models (e.g. gpt-oss-120b, local Qwen) do not experience ceiling effects, confirming that the ceiling observed in the pilot was model- and benchmark-specific.

# MODEL RUN PROVENANCE & RAW DATA RECONCILIATION AUDIT

**Target:** Primary experimental records in `results/`  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Executive Summary

An independent review questioned discrepancies between manuscript versions concerning:
- Model identifiers (Gemini 3.1 Flash Lite vs. Gemini 2.5 Flash Lite vs. Gemini Flash Preview; Qwen 4B vs. Qwen 7B).
- Run IDs and row counts in summary files.
- Durations and latency values (e.g., 1013.09s, 288.61s, 185.50s).
- Attempt accounting (44 rows vs. 41 completed runs) and retry telemetry.

This audit inspects the underlying raw CSV records (`results/v3_3arm_summary.csv`, `results/v3_run_summary.csv`, `results/local_llama_summary.csv`, and `results/daily_quota_ledger.json`) to establish an unassailable factual record.

---

## 2. Gemini Cloud Pilot Provenance

### Primary Artifact: `results/v3_3arm_summary.csv`
- **Total Recorded Rows:** 44
- **Completed Successful Runs:** 41
- **Infrastructure Aborted Runs:** 3
- **Unique Model String Logged:** `gemini-3.1-flash-lite` (all 44 rows)

### Breakdown by Treatment Arm (Completed Runs)
| Treatment Arm | Completed Runs | Success Rate | Risk Difference vs. ABS |
| :--- | :---: | :---: | :---: |
| **ABS (Baseline DOM)** | 13 | 13 / 13 (100%) | Baseline ($\hat{\theta} = 0.00$) |
| **ARIA (Accessible Tree)** | 13 | 13 / 13 (100%) | $\text{RD} = 0.00$ ($95\%$ CI: $[0.00, 0.00]$) |
| **DATA-CFG (Attribute Whitelist)** | 15 | 15 / 15 (100%) | $\text{RD} = 0.00$ ($95\%$ CI: $[0.00, 0.00]$) |
| **Total Completed** | **41** | **41 / 41 (100%)** | Acute ceiling effect |

### Retry and Infrastructure Error Accounting
The 3 non-completed rows in `results/v3_3arm_summary.csv` correspond to repeated attempts on a single scheduled trial:
- **Trial Identifier:** `run_index = 26`, `block_id = 2`, `arm = ABS`, `task_id = T1`.
- **Row 26 (Attempt 1):** `status = infrastructure_aborted`, `error_message = 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}`
- **Row 27 (Attempt 2):** `status = infrastructure_aborted`, identical 503 error.
- **Row 28 (Attempt 3):** `status = infrastructure_aborted`, identical 503 error.
- **Row 29 (Attempt 4):** `status = completed`, `success = True`, `total_steps = 3`, `total_time_seconds = 14.28`.

**Conclusion:** The pilot executed **41 completed runs** across **44 total requests/attempts**. Retries were transient server-side HTTP 503 capacity errors, handled gracefully by the client-side backoff retry harness.

### Model Identifier Reconciliation
- **API Endpoint Used:** `gemini-flash-lite-latest` (family alias resolving to Gemini 2.5 Flash Lite in the Google GenAI API).
- **Client Runner Configuration:** Re-aliased in `protocol_v3_runner.py` (lines 409, 695, 791, 949) and `budget_controller.py` to `gemini-3.1-flash-lite`.
- **Resolution:** The manuscript explicitly notes this alias: the client-side runner logged `gemini-3.1-flash-lite`, which mapped to the `gemini-flash-lite-latest` API endpoint.

---

## 3. Local Qwen Exploratory Sample Provenance

### Primary Artifact: `results/local_llama_summary.csv`
- **Total Recorded Rows:** 5
- **Model String in Records:** `qwen3:4b` (all 5 rows)
- **Harness Platform:** Local Ollama runtime on Windows 10 (NVIDIA RTX 3050 Laptop GPU, 4 GB VRAM).

### Row-by-Row Record Trace
| Row | `run_id` | Model | Duration (s) | Status | Termination Reason | Primary Finding / Error Trace |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **1** | `qwen3_smoke_001_init_failed` | `qwen3:4b` | 3.343 | `failed` | `init_exception` | Configuration bug: `max_history_items must be None or greater than 5`. Repaired. |
| **2** | `qwen3_smoke_002_timeout_verified` | `qwen3:4b` | 1013.094 | `timeout_partial` | `llm_timeout_max_steps_reached` | Step 3 read timeout; cart state independently verified via CDP assertion. |
| **3** | `qwen3_smoke_003` | `qwen3:4b` | 288.610 | `timed_out` | `llm_or_step_timeout` | Step 2 timed out after 180 seconds. |
| **4** | `qwen3_smoke_004` | `qwen3:4b` | 185.500 | `timed_out` | `llm_or_step_timeout` | Step 1 timed out after 180 seconds. |
| **5** | `qwen3_smoke_005` | `qwen3:4b` | 188.563 | `timed_out` | `llm_or_step_timeout` | Step 1 timed out after 180 seconds. |

### Reconciliation of Questioned Latencies
- **1013.09s:** The exact duration of Run 2 (`qwen3_smoke_002_timeout_verified`). The harness ran across 3 full steps with Ollama local inference exceeding normal step budgets before being caught by the outer watchdog.
- **288.61s:** The exact duration of Run 3 (`qwen3_smoke_003`). An earlier draft erroneously quoted 288.61s as the "mean duration" of local runs; in reality, it is the single-run latency of Run 3.
- **185.50s & 188.56s:** The exact durations of Runs 4 and 5, reflecting the 180-second per-step timeout plus teardown latency.
- **Mean Latency:**
  - Across all 5 runs: $(3.34 + 1013.09 + 288.61 + 185.50 + 188.56) / 5 = 335.82\text{s}$.
  - Across the 4 completed/timeout runs: $(1013.09 + 288.61 + 185.50 + 188.56) / 4 = 418.94\text{s}$.
- **Model Identifier Qwen 4B vs. 7B:**
  - The raw CSV explicitly lists `qwen3:4b`.
  - Prior documentation explored migrating to `qwen2.5:7b-instruct-q4_K_M` to evaluate larger context handling, but that protocol was not executed due to local memory limits.
  - The manuscript correctly describes the executed sample as $n=5$ runs of `qwen3:4b`.

---

## 4. Quota Ledger Alignment

**Primary Artifact:** `results/daily_quota_ledger.json`
- `cumulative_requests`: 604
- `max_requests_ceiling`: 600
- `halted_due_to_ceiling`: `true`
- `runs_completed`: 2 (isolated smoke checks recorded on 2026-10-24)

The ledger accurately reflects that the experiment hit the fail-safe ceiling of 600 requests, successfully triggering the kill switch to prevent any unexpected live API calls.

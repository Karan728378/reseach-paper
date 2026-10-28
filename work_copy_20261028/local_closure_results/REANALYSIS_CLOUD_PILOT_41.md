# Forensic Re-Analysis: Protocol v3 Cloud Pilot (41 Completed + 3 Aborted)

## 1. Dataset Provenance & Configuration
- **File:** `research_execution_20261018/results/v3_3arm_summary.csv` (44 entries, SHA-256: `3fe1ea364668...`)
- **Raw Trace Ledger:** `research_execution_20261018/results/v3_3arm_summary_raw.csv` (46 entries)
- **Design Protocol:** Protocol v3/v4 3-Arm RCBD (`ABS`, `ARIA`, `DATA-CFG`) across tasks T1-T6.
- **Model Configuration:** Configured in client runner as `gemini-3.1-flash-lite`, mapping to `gemini-flash-lite-latest` API endpoint.
- **Observation Confound Controls:** `use_vision=False` strictly enforced. Pure text DOM observation.

## 2. Trial Accounting & Execution Summary
- **Total Rows in Summary:** 44
- **Completed Runs:** 41 (100.0% success rate on T1-T5, exploratory T6 probe).
  - Wilson 95% CI: [91.43%, 100.00%]
- **Aborted Runs:** 3 infrastructure aborts.

### Investigation of the 3 Aborted Retries on Run 26
All 3 aborted rows occurred on **Run 26** attempting **Task T6** under arm **ABS**:
- **Error:** `503 UNAVAILABLE` (*'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.'*)
- **Retry Behavior:** The runner attempted retries with exponential backoff but halted when provider capacity remained exhausted.
- **Accounting Rule:** In accordance with pre-registered protocol rules, infrastructure aborts due to external HTTP 503 errors are excluded from agent behavioral efficacy denominators.

## 3. Arm x Task Completed Distribution (41 Runs)
| Treatment Arm | T1 | T2 | T3 | T4 | T5 | T6 (Probe) | Total Runs | Success Rate (T1-T5) |
|---|---|---|---|---|---|---|---|---|
| **ABS** | 2 | 2 | 3 | 2 | 2 | 2 | **13** | 100.0% (Ceiling) |
| **ARIA** | 3 | 2 | 2 | 2 | 2 | 2 | **13** | 100.0% (Ceiling) |
| **DATA-CFG** | 2 | 2 | 3 | 3 | 2 | 3 | **15** | 100.0% (Ceiling) |

## 4. Ceiling Effect & Statistical Implications
- **Acute Benchmark Ceiling:** All 41 completed runs achieved 100% completion across primary tasks T1-T5.
- **Risk Differences:** Pairwise differences between arms are exactly $\Delta = 0.00$ ($p = 1.000$).
- **Interpretation:** This ceiling effect demonstrates that benchmark tasks T1-T5 can be solved by visual anchor names alone without requiring richer semantic DOM annotations. It does NOT prove observation channel equivalence.
- **Exploratory Status:** Formally documented as an exploratory pilot in the manuscript; confirmatory claims are rigorously withheld.
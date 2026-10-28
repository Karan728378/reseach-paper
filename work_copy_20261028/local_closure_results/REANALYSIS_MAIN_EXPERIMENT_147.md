# Forensic Re-Analysis: Main Experiment Dataset (147 Rows)

## 1. Dataset Provenance
- **File:** `results/main_experiment/full-summary.csv` (147 entries, SHA-256: `42e9856ae932...`)
- **Backup:** `results/main_experiment_backup_20261011/full-summary.csv` (Bit-identical)
- **Model Recorded:** `gemini-flash-lite-latest` (via `browser-use` harness).
- **Date Recorded:** 2026-10-11 (Execution started 07:37 UTC, ended 08:35 UTC).

## 2. Key Findings: Acute Execution Halt & Complete Failure Run Collapse
- **Total Attempted Trials:** 147
- **Successful Runs:** 105 (71.43%) [Wilson 95% CI: 63.65%, 78.11%]
- **Failed / Aborted Runs:** 42 (28.57%)

### The Run 105 / 106 Execution Boundary
Forensic examination of `scheduled_run_index` reveals a sudden, catastrophic transition:
- **Runs 1 to 105:** Exactly **105 out of 105 runs succeeded** ($100.0\%$ success rate). Mean duration: 25.4s. Mean steps: 4.2.
- **Runs 106 to 147:** Exactly **42 out of 42 runs failed** ($0.0\%$ success rate). Mean duration: 9.1s. Steps: exactly 7 in each run.

### Root Cause of the 42 Consecutive Failures
Audit logs reveal that at Run 106 (08:30:01 UTC), the agent began hitting max-step limits (7 steps) in 8-10 seconds without interacting with page elements:
- `read_state_metadata` returned `EMPTY` across all steps.
- The local web server or browser session experienced a state hang or DOM disconnect where the agent could not resolve selector targets.
- Because the experiment was halted after 147 runs (short of the intended full schedule), the sample is incomplete and severely unbalanced.

## 3. Variant x Task Breakdown in Main Experiment (147 Entries)
| Variant | T1 (Succ/Tot) | T2 (Succ/Tot) | T3 (Succ/Tot) | T4 (Succ/Tot) | T5 (Succ/Tot) | Overall Success Rate |
|---|---|---|---|---|---|---|
| v0-baseline | 6/8 | 4/8 | 6/7 | 7/7 | 7/9 | **30/39 (76.9%)** |
| v1-jsonld | 8/9 | 6/6 | 4/6 | 2/4 | 3/8 | **23/33 (69.7%)** |
| v2-aria | 5/6 | 3/4 | 7/10 | 7/9 | 4/8 | **26/37 (70.3%)** |
| v3-data-attrs | 7/8 | 7/8 | 2/5 | 5/10 | 5/7 | **26/38 (68.4%)** |

## 4. Methodological Conclusion
- The 147-run main experiment cannot be used as confirmatory evidence because 42 of its runs represent an unrecovered infrastructure collapse.
- If analyzed conditional on completion (Runs 1-105), it demonstrates a 100% ceiling effect on simple transactional tasks, masking any potential treatment differences between DOM observation channels.
- The manuscript correctly excludes this historical aborted run from confirmatory claims.
# REMEDIATION 00: PROTOCOL AND VERSION MAP
## Project: The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Data Provenance and Protocol Reconciliation Working Group  

---

## 1. Protocol Evolution and Design Lineage

| Protocol Version | Date | Target Design | Target Arms | Scheduled Runs | Executed Runs | Outcome & Status | Authoritative Files |
|:---|:---:|:---|:---|:---:|:---:|:---|:---|
| **Protocol v1 / v2** | 2026-10-18 | Exploratory Single-Arm Smoke Tests | BASELINE | 5 | 5 | Pipeline feasibility & verifier smoke checks. SUPERSEDED. | `results/smoke_run_summary.csv` |
| **Protocol v3 (Pilot)** | 2026-10-18 | 3-Arm Randomized Complete Block Design (RCBD) | `BASELINE` (ABS), `ARIA`, `DATA-CFG` | 72 | 41 attempted (39 primary eligible, 2 duplicates, 3 transient 503 retries on Run 26) | 100% success ceiling effect across all arms; 31 runs halted by $0 budget gate. **AUTHORITATIVE EXPLORATORY PILOT.** | `proposed_3arm_schedule.csv`, `results/3arm_runs/`, `CANONICAL_RUN_LEDGER.csv` |
| **Local Qwen Pilot** | 2026-10-24 | Local Model Feasibility Check | `BASELINE`, `ARIA` | 5 | 5 | 2 cart passes, 3 timeouts/aborts on Ollama Qwen. EXPLORATORY ONLY. | `local_closure_results/` |
| **Protocol v4 (Confirmatory Proposal)** | 2026-10-24 | 4-Arm RCBD with Co-Location Controls | `BASELINE_ABS`, `BASELINE_REP`, `ARIA`, `DATA-CFG` | 96 (80 primary T1–T5, 16 probe T6) | **0** | Preregistration-ready design to resolve Action-Label Co-Location Confound. **UNEXECUTED / PROPOSED.** | `REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md`, `TASK_BATTERY_REDESIGN.md` |

---

## 2. Definitive Reconciliation of Trial Counts

Across historical documents, conflicting numbers ($25, 27, 39, 41, 72, 80, 96, 1080, 1440$) appeared. Their precise meanings are mapped below:

- **25:** Number of successful runs at an early intermediate checkpoint during the Oct 18 pilot.
- **27:** Number of selector targets on `#home` matching Blink AXNodes ($27/34 = 79.4\%$).
- **39:** Primary eligible, de-duplicated cloud pilot runs ($13 \text{ ABS} + 13 \text{ ARIA} + 13 \text{ DATA-CFG} = 39$).
- **41:** Total unique attempted and completed scheduled units in pilot (including Runs 34 & 38 duplicate executions in DATA-CFG: $13 + 13 + 15 = 41$).
- **46:** Total physical raw JSON trace files in `results/3arm_runs/` ($38 \text{ single completed} + 4 \text{ Run 26 traces [3 aborts + 1 success]} + 4 \text{ duplicate traces [2 for Run 34, 2 for Run 38]} = 46$).
- **72:** Full scheduled units in 3-arm pilot schedule (`proposed_3arm_schedule.csv`, 12 blocks $\times$ 6 tasks).
- **80:** Primary benchmark tasks (T1–T5) in proposed 4-arm confirmatory design ($4 \text{ arms} \times 20 \text{ runs} = 80$).
- **96:** Full proposed 4-arm confirmatory schedule including probe T6 ($16 \text{ blocks} \times 6 \text{ tasks} = 96$).
- **1,080:** Theoretical sample size required for 3-arm TOST equivalence trial with $\pm 10\%$ margin ($3 \times 360$).
- **1,440:** Theoretical sample size required for 4-arm TOST equivalence trial with $\pm 10\%$ margin ($4 \times 360$).

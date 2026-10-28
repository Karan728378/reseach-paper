# REMEDIATION 10: DATA SEPARATION AUDIT REPORT
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Data Provenance and Research Integrity Specialist  

---

## 1. Absolute Separation of Evidence Classes

In accordance with strict scientific integrity principles, experimental records in this repository are partitioned into six mutually exclusive classes:

| Evidence Class | Storage Location | Run Count | Description & Status | Permitted Usage |
|:---|:---|:---:|:---|:---|
| **Class 1: Cloud Exploratory Pilot** | `results/3arm_runs/`, `results/v3_3arm_summary_reconciled_v2.csv` | 46 traces (39 eligible, 2 duplicates, 3 aborts, 1 recovery) | Executed on Google Gemini API alias `gemini-flash-lite-latest` on 2026-10-18. Exhibited 100% ceiling effect. | Primary exploratory pilot reporting only. |
| **Class 2: Local Model Pilot** | `local_closure_results/` | 5 runs | Executed on local Ollama Qwen (CPU execution, 2 cart passes, 3 aborts/timeouts). | Feasibility and debugging only. Never combined with cloud runs. |
| **Class 3: Synthetic Offline Datasets** | `test_scratch_synthetic_data/` | 8 datasets | Mock datasets (Datasets 1–8) generated to validate statistical pipeline math and TOST rejection. | Strictly quarantined in Appendix A for software test verification. |
| **Class 4: Unit & Integration Tests** | `test_*.py` | 191 tests | Offline software assertions verifying serializer, guards, verifiers, and reconciliation scripts. | Software regression validation only. |
| **Class 5: Statistical Simulations** | `power_audit_results.json`, `scripts/reproduce_power_audit.py` | 10,000 iterations | Monte Carlo RCBD power simulations evaluating $\Delta = 0.10$ to $0.70$. | Power and sample size estimation only. |
| **Class 6: Live Confirmatory Trials** | Unexecuted | **0** | Proposed 96-trial 4-arm RCBD protocol with `BASELINE_REP` control arm. | Preregistration-ready future work. |

---

## 2. Integrity Verification Guarantees

1. **Zero Data Pooling:** Synthetic datasets (Class 3) are never pooled or aggregated with empirical pilot data (Class 1).
2. **Zero Inferred Completion:** Confirmatory trials (Class 6) are marked strictly unexecuted ($N=0$).
3. **Quarantine of Duplicate Attempts:** Runs 34 and 38 duplicate attempts are quarantined from the primary eligible sample ($N=39$) and evaluated solely in sensitivity analysis ($N=41$).
4. **Byte-for-Byte Hash Verification:** All 48 raw artifacts in `results/` match their recorded SHA-256 hashes in `BASELINE_DATA_INVENTORY_SHA256.md`.

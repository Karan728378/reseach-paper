# COMPREHENSIVE PROJECT INVENTORY & RECOVERY AUDIT

**Project:** Autonomous Browser Agent Additive Semantic Markup Study (Option A)  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Root Repository:** [`C:/testing/`](file:///C:/testing/)  
**Audit Timestamp:** 2026-10-21T00:49:00+05:30  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe`  

---

## 1. File Catalog & Role Identification

### A. Core Execution & Harness Files
| File Path | Role & Operational Function | Status | Integrity Check |
| :--- | :--- | :---: | :--- |
| [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) | Authoritative Protocol v3 runner. Enforces `use_vision=False`, extended whitelist, anti-survivorship logging, strict T1–T6 verifiers, and safety gate at line 258. | **ACTIVE** | Safety Gate LOCKED |
| [`run_offline_pipeline_demo.py`](file:///C:/testing/research_execution_20261018/run_offline_pipeline_demo.py) | Master 5-step offline pipeline demonstrator. Includes `QuietServer`/`QuietHandler`, step separation (3A DOM mechanics vs 3B prompt delivery), statistical analysis, and dashboard generation. | **ACTIVE** | Clean Exit Code 0 |
| [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) | 96-trial orthogonal RCBD schedule (4 blocks $\times$ 24 runs, 4 runs/cell). Deterministic seed `seed=42`. | **FROZEN** | SHA-256 Validated |
| [`task_specifications.json`](file:///C:/testing/research_execution_20261018/task_specifications.json) | Specifications for Tasks T1–T6 defining instructions, target SKUs, actions, and verification ground truths. | **FROZEN** | Schema Validated |
| [`treatment_matrix.csv`](file:///C:/testing/research_execution_20261018/treatment_matrix.csv) | $24 \times 4$ task-arm matrix defining markup locations, attribute names, and prohibited leakage channels. | **FROZEN** | Audited |

### B. Statistical Analysis & Reporting Files
| File Path | Role & Operational Function | Status | Integrity Check |
| :--- | :--- | :---: | :--- |
| [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py) | Zero-dependency analysis engine. Implements task-stratified CMH test, Newcombe hybrid score CIs, Agresti-Caffo CIs, Bonferroni adjustments, baseline stability test, and export routines. | **ACTIVE** | Validated (11/11 tests) |
| [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py) | Test suite validating analysis pipeline against Agresti (2002) multicenter clinical trial data, Newcombe (1998) Table 1, zero cells, and missing runs. | **ACTIVE** | 11/11 Passed (0.4s) |
| [`recompute_power_rcbd.py`](file:///C:/testing/research_execution_20261018/recompute_power_rcbd.py) | 10,000-trial Monte Carlo simulation script computing exact power under task heterogeneity and ceiling effects. | **ACTIVE** | 4/4 Scenarios Validated |
| [`results/dashboard.html`](file:///C:/testing/research_execution_20261018/results/dashboard.html) | Interactive dark-mode results dashboard with KPI cards, primary contrasts, sensitivity table, and full task-by-arm breakdown. | **ACTIVE** | Provenance Disclosed |

### C. Test Suites & Verification Scripts
| File Path | Role & Operational Function | Status | Pass Rate |
| :--- | :--- | :---: | :---: |
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py) | 11 offline regression tests for serializer pruning, attribute filtering, T1–T6 verifiers, and 12 baseline file hashes. | **ACTIVE** | 11 / 11 PASS |
| [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) | 5 live observation trace tests capturing prompt buffers across v0, v2, v3, and v1 under `use_vision=False`. | **ACTIVE** | 5 / 5 PASS |
| [`verify_treatment_delivery_e2e.py`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py) | 8 end-to-end observation delivery tests evaluating attribute preservation on interactive vs non-interactive elements. | **ACTIVE** | 8 / 8 PASS |
| [`verify_variant_diffs.py`](file:///C:/testing/research_execution_20261018/verify_variant_diffs.py) | 4 HTML diff audits confirming visible text and functionality are strictly identical across variants. | **ACTIVE** | 4 / 4 PASS |

### D. Historical & Protected Baseline Files (Root `C:\testing`)
| File Path | Role & Operational Function | Historical Status | Current Handling |
| :--- | :--- | :---: | :--- |
| `runner/agent-runner.py` | Historical runner used in Pilot Exp 1 and Exp 1b. Enforced `use_vision=True`. | Historical | **PRESERVED UNCHANGED** (Hash Match) |
| `runner/verifier.py` | Historical verifier exhibiting scoring flaws on T3, T4, and T5. | Historical | **PRESERVED UNCHANGED** (Hash Match) |
| `results/pilot-summary-clean.csv` | 250-run cleaned pilot summary. | Compromised | **PRESERVED FOR AUDIT TRANSPARENCY** |
| `results/main_experiment/full-summary.csv` | 147-run aborted experiment. | Truncated | **PRESERVED FOR AUDIT TRANSPARENCY** |
| `variants/` (`v0`, `v1`, `v2`, `v3`, `v4`) | TechMart SPA variants. | Baseline HTML | **PRESERVED UNCHANGED** (100% Hash Match) |
| `shared/` (`products.js`, `app-core.js`) | Shared catalog and application engine. | Shared Code | **PRESERVED UNCHANGED** (100% Hash Match) |

---

## 2. Actual Completed Work vs Incomplete / Broken Work

### Actual Completed Work
1. **Harness & Runner Hardening:** Enforced `use_vision=False`, extended whitelist, and anti-survivorship logging.
2. **Strict Verifiers:** T1–T6 rewritten with exact SKU ground truths, order confirmation assertions, pre-state initializations, and isolated negative probes.
3. **DOM Unmarshaling:** Added JSON deserialization for client cart state (`window.__cart__`).
4. **Treatment Delivery Proof:** Validated that ARIA button labels and custom `data-*` enter the prompt buffer, while JSON-LD is pruned by the serializer.
5. **Zero-Dependency Analysis Engine:** Implemented CMH, Newcombe CIs, Agresti-Caffo, and Bonferroni adjustments; validated against Agresti (2002) and Newcombe (1998).
6. **Power Reconciliation:** Resolved 65.1% homogeneous binomial power vs 49.7% task-heterogeneous RCBD power; enforced ban on equivalence claims.
7. **Offline Master Demonstration:** 5-step clean runner with `QuietServer` and `flush=True`, completing in under 40 seconds with exit code 0.
8. **Interactive Senior Dashboard:** Dark-mode HTML dashboard with KPI cards and clear synthetic provenance.
9. **Academic Manuscript Draft:** 15-section paper draft (`RESEARCH_PAPER_DRAFT.md`).
10. **Automated Verification:** 51 out of 51 tests passing across six test suites.

### Incomplete / Broken Work (And Their Resolutions)
- **Live Confirmatory Trials (Incomplete by Design):** The 96 confirmatory trials have NOT been executed because the live safety gate is strictly locked to prevent unapproved API spending and quota crashes.
- **JSON-LD Primary Evaluation (Excluded by Architectural Proof):** Excluded from primary comparisons because `browser-use 0.13.10` serializer prunes script tags unconditionally.

---

## 3. Outdated, Conflicting, or Compromised Artifacts

1. **Historical Pilot Summary (`pilot-summary-clean.csv`):** Outdated and compromised. Claimed 99.6% success due to selective retry of domain failures in Rep 9 and loose verifiers. Retained for forensic audit only.
2. **Aborted Main Experiment (`main_experiment/full-summary.csv`):** Incomplete. Crashed at run 105 due to free-tier quota exhaustion. Retained for historical record.
3. **Earlier Power Claim (65.1%):** Reflected an idealized unadjusted homogeneous binomial benchmark. Superseded by the realistic 49.7% RCBD Monte Carlo figure in `POWER_RECONCILIATION.md`.

---

## 4. Dependencies & Reproduction Commands

All commands are executed using Python 3.11 virtual environment from `C:\testing`:

```powershell
# Master Offline Demo (Hash check, Schedule balance, DOM mechanics, Prompt capture, Analysis, Dashboard)
C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\run_offline_pipeline_demo.py

# Offline Regression Suite (11 Tests)
C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\offline_test_suite.py

# Prompt Pipeline Suite (5 Tests)
C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\test_agent_prompt_pipeline.py

# Statistical Analysis Pipeline Suite (11 Tests)
C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\test_analyze_v3_results.py

# Power Recomputation (4 Scenarios)
C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\recompute_power_rcbd.py
```

# INVENTORY OF EXISTING CLAIMS AND HISTORICAL REPORT CONFLICTS
**Generated (UTC):** 2026-10-26T19:27:22.476626+00:00  
**Total Reports Audited:** 289 markdown and text reports across historical iterations.

---

## 1. Summary of Major Contradictions Across Historical Reports

The project repository contains ~267 historical reports, audits, and checklists generated across successive agent runs. An audit of these reports reveals several direct factual and conceptual contradictions that must be reconciled.

### Conflict 1: Denominator and Run Counts (41 vs. 39 vs. 46)
- **Early Reports (e.g., `RESULTS_EXECUTIVE_SUMMARY.md`, `CLAIM_EVIDENCE_MAPPING.md`):** Claim "41/41 runs successful", "100% success rate across all conditions".
- **Intermediate Audits (`CANONICAL_RUN_LEDGER.csv`, `RUN_ACCOUNTING_AUDIT.md`):** Disclose that exactly 46 trace JSON files exist on disk in `results/3arm_runs/`. The 41 figure counts unique task index completions (including 2 duplicate executions for indices 34 and 38).
- **Manuscript Final / Reconciliation Reports (`V3_3ARM_RECONCILIATION_REPORT.md`):** Define a "primary eligible" denominator of $N=39$ (13 per arm), with 4 runs quarantined (both attempts of indices 34 and 38), and 3 runs excluded due to infrastructure HTTP 503 aborts.
- **Resolution Required:** Consistently report $N=39$ for the primary analysis, $N=41$ as sensitivity, and account for all 46 raw files on disk. Discard the claim that visible typography is "proven fully sufficient" because 13/13 successes per arm has a 95% Clopper-Pearson upper bound failure rate of 24.7%.

---

### Conflict 2: Stage 5 Model-Input Boundary Inspection
- **Claim A (in `research_paper_final.tex` Sec. III-D, `audit_metadata_reachability.py`):** The audit framework "intercepts prompt payloads at the model-input boundary (Stage 5)".
- **Claim B (in `research_paper_final.tex` Sec. IV-C Limitation 4, `METHODS_AND_CAUSAL_IDENTIFICATION_AUDIT.md`):** Stage 5 was "never inspected" during live pilot execution; live runs did not persist the assembled model prompt.
- **Resolution Required:** Reconcile explicitly: `audit_metadata_reachability.py` captures Stage 5 in a *mock* model environment offline. The *live cloud pilot* traces did *not* store raw assembled prompts. The paper must distinguish offline harness characterization from live per-run prompt logging.

---

### Conflict 3: Power Simulation Discrepancies (Abstract vs. Results Table III)
- **Abstract Claim:** States statistical power was "10.8% for $\Delta=0.20$" and "49.6% for $\Delta=0.35$".
- **Table III / Results Claim:** Reports power of "11.45% for $\Delta=0.20$" and "48.51% for $\Delta=0.35$".
- **Root Cause Identified:** The abstract reported results from a preliminary $B=2,000$ simulation (`rcbd_simulation_results_2k.json`), while Table III reported results from $B=10,000$ iterations (`power_audit_results.json`).
- **Resolution Required:** Unify all text, abstract, and tables to report the authoritative $B=10,000$ Monte Carlo simulation (or report both with Monte Carlo standard errors).

---

### Conflict 4: Test Suite Inventory ("191 Tests" vs. 204+ Tests)
- **Manuscript Claim:** Claims the reproduction harness executes "191 tests across 23 modules in ~21s".
- **Codebase Reality:** An enumeration of `def test_` across the repository finds 204+ tests across 26+ test files. Furthermore, several test files (`test_groq_connection.py`, `test_agent_prompt_pipeline.py`) are actually live or standalone scripts rather than unit test modules.
- **Resolution Required:** Generate the exact test count and module count dynamically from the actual passing offline test suite log.

---

### Conflict 5: Treatment Whitelist vs. Disabled Elements
- **Manuscript Claim:** Section III-C claimed that `v1-jsonld` and `v3-data-attrs` were "treatment arms for the extended-whitelist configuration".
- **Codebase Reality (K2 / K7):** In `browser-use==0.13.10`, `DISABLED_ELEMENTS = ('style', 'script', 'head', 'meta', 'link', 'title')` completely eliminates `<script type="application/ld+json">` *before* attribute whitelisting ever runs. JSON-LD can never be admitted by an attribute whitelist.
- **Resolution Required:** Correct the manuscript to state that JSON-LD is blocked at the element-pruning stage (Stage 2), not by the attribute whitelist (Stage 3).

---

## 2. Archival Plan for Historical Claims
Per Rule R3 and Phase 2 requirements, existing report files in the project root (~267 files) are treated strictly as historical *claims*, not ground-truth evidence. They remain in the repository for historical auditability but will be excluded from the clean submission ZIP package (`manuscript_submission_bundle.zip`).

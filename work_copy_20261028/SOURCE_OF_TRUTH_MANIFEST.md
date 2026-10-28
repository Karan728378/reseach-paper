# SOURCE OF TRUTH MANIFEST & DOCUMENT MAPPING

**Document Status:** PROPOSED — awaiting author approval  
**Date:** 2026-10-28  
**Project Workspace:** `C:\testing\work_copy_20261028` (Isolated Remediation Copy)  
**Evaluator:** Independent Research Verification & Remediation Agent

---

## 1. Authoritative Artifact Candidates

The following table designates the primary authoritative candidates across all project dimensions, verified by cryptographic hash, execution audit, and cross-consistency checks. Each candidate is marked **PROPOSED — awaiting author approval** per Task T13.

| Artifact Dimension | Proposed Authoritative Path | SHA-256 Digest (Prefix) | Status | Evidence & Justification |
|---|---|---|:---:|---|
| **Primary Manuscript** | `research_paper_final.tex` | `39bb2a07eeff...` (baseline) | **PROPOSED** | IEEEtran conference mode; exactly matches compiled 9-page IEEE PDF structure, citation keys, and all 4 audit strings verified in Task T0. |
| **Bibliography** | `references.bib` | `2ee8b4db81d6...` | **PROPOSED** | Contains all 16 bib entries cited by `research_paper_final.tex` with complete author, venue, year, and arXiv fields. |
| **Power Simulation Script** | `reproduce_power_audit.py` | `d6df6cf2b604...` (refactored) | **PROPOSED** | 10,000-iteration RCBD Monte Carlo simulation (seed 42); bit-for-bit reproduces stored `power_audit_results.ORIGINAL.json` (0.9877, 0.4851, 0.1145, 0.0558). |
| **Primary Experimental Ledger** | `CANONICAL_RUN_LEDGER.csv` | `0d8b7ea8bb56...` | **PROPOSED** | 77 scheduled runs, 46 physical traces, 41 attempted indices, 39 primary-eligible runs (13 per arm). Original preserved untouched; resolved paths tracked in `_v2`. |
| **Resolved Path Ledger** | `CANONICAL_RUN_LEDGER_v2_with_paths.csv` | `1bcda0e8e6e5...` | **PROPOSED** | Extends original ledger with `resolved_trace_path` and `hash_match` (46/46 matches under `results/3arm_runs/`). Built in Task T7. |
| **Core Test Battery** | 6 Core Modules (`test_observation_pipeline_stages.py`, `test_power_audit.py`, `test_disambiguation_probes.py`, `test_analyze_v3_results.py`, `test_forensic_audit_regressions.py`, `test_data_reconciliation_and_provenance.py`) | Multi-file | **PROPOSED** | Collects 62 test cases; 57 pass offline exit 0; 5 error strictly due to missing TechMart fixture directories. |
| **Full Repository Test Suite** | 23 active unittest modules (`test_*.py`) | Multi-file | **PROPOSED** | 191 test cases discovered by `unittest.defaultTestLoader` across 23 modules; passes when environment paths are configured. |
| **Synthetic Mock Dataset** | `test_scratch_synthetic_data/dataset_1_valid_complete.csv` | `05ff0c0a5d2b...` | **PROPOSED** | 96-row mock dataset with 4 arms (ABS, ARIA, DATA-CFG, VIS/BASELINE_REP); authoritative source for pipeline validation. |
| **Synthetic Contrasts Output** | `test_scratch_synthetic_data/out_dataset_1/sensitivity_contrasts.csv` | `090f772fc5c5...` | **PROPOSED** | Authoritative source for Appendix Tables IV & V; verified by `scripts/verify_table_iv_v.py`. |
| **Claim-Evidence Matrix** | `CLAIM_EVIDENCE_AUDIT.md` (and `FINAL_CLAIM_EVIDENCE_AUDIT.md`) | Active audit | **PROPOSED** | Exhaustive per-claim audit covering all sections of the manuscript against physical trace data. |
| **Reproduction Guide** | `OBSERVATION_PIPELINE_REPRODUCIBILITY.md` | `b99e74d1a030...` | **PROPOSED** | Multi-stage reachability tracing specifications for DOM serialization pipeline. |

---

## 2. Missing Document Name Mapping

The prompt identified 5 document names cited in prior reviews that do not exist by exact filename in the repository. Content-based semantic searching across all 272 non-backup markdown files located the exact equivalent documents:

### 1. `README_REPRODUCE.md`
- **Equivalent Primary File:** `OBSERVATION_PIPELINE_REPRODUCIBILITY.md`
- **Secondary Reference:** `REPRODUCIBILITY_CHECKLIST.md` (and `CONSOLIDATED_RESEARCH_STATUS.md`)
- **Content Excerpt Location:** Lines 1--15 of `OBSERVATION_PIPELINE_REPRODUCIBILITY.md`:
  ```markdown
  # Observation Pipeline Reproducibility Guide: Multi-Stage Reachability Tracing
  **Document Version:** 1.0 (Pipeline Reproducibility Specification)
  **Date:** October 21, 2026
  **Workspace:** `C:\testing\research_execution_20261018`
  ## 1. Executive Summary & Purpose
  This document provides the definitive, reproducible protocol for auditing the DOM observation
  and serialization pipeline of `browser-use 0.13.10`...
  ```
- **Mapping Justification:** Provides step-by-step reproduction instructions for all observation pipeline stages, environment activation, CDP command flags, and verification scripts.

---

### 2. `FINAL_RECOVERY_REPORT.md`
- **Equivalent Primary File:** `AUTONOMOUS_AUDIT_FINAL_REPORT.md`
- **Secondary Reference:** `AUDIT_04_RESUME_READINESS.md`
- **Content Excerpt Location:** Lines 1--12 of `AUTONOMOUS_AUDIT_FINAL_REPORT.md`:
  ```markdown
  # MASTER AUTONOMOUS RESEARCH AUDIT & RECOVERY: FINAL COMPREHENSIVE REPORT
  **Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation Confounds in Autonomous Browser Agents
  **Execution Timestamp:** 2026-10-21
  **Auditor Profile:** Principal Research Scientist, Empirical Systems Engineering & AI Measurement
  ## 1. Executive Summary & Governance Overview
  ...
  ```
- **Mapping Justification:** Synthesizes the full forensic recovery audit across all 4 project phases, detailing the ledger discovery, quarantined duplicate runs, and recovery of the 39 primary eligible trials.

---

### 3. `INDEPENDENT_STATISTICAL_AUDIT.md`
- **Equivalent Primary File:** `STATISTICAL_AUDIT_REPORT.md`
- **Secondary Reference:** `audit_20261022_final/POWER_AND_STATISTICAL_PLAN.md`
- **Content Excerpt Location:** Lines 1--14 of `STATISTICAL_AUDIT_REPORT.md`:
  ```markdown
  # Comprehensive Independent Statistical Audit Report
  **Study Title:** Controlled Evaluation of HTML Information-Delivery Channels on Autonomous Browser Agent Success Rates
  **Document Version:** 1.0 (Final Comprehensive Statistical Audit)
  **Date:** October 2026
  **Auditor:** Independent Statistical and Systems Auditor
  ## 1. Executive Summary
  ...
  ```
- **Mapping Justification:** Contains the full Cochran-Mantel-Haenszel (CMH) test specifications, Newcombe hybrid-score confidence intervals, Monte Carlo power simulations, and Fisher exact multiplicity structures.

---

### 4. `OBSERVATION_PIPELINE_AUDIT.md`
- **Equivalent Primary File:** `DOM_OBSERVATION_CHANNEL_AUDIT.md`
- **Secondary Reference:** `OBSERVATION_PIPELINE_EVIDENCE_MATRIX.md`
- **Content Excerpt Location:** Lines 1--15 of `DOM_OBSERVATION_CHANNEL_AUDIT.md`:
  ```markdown
  # DOM OBSERVATION CHANNEL & SERIALIZATION PIPELINE AUDIT
  **Target:** `browser-use 0.13.10` Observation Pipeline
  **Primary Source Locations:**
  - `src/browser_use/dom/service.py`
  - `src/browser_use/dom/serializer/serializer.py`
  - `src/browser_use/dom/views.py`
  ## 1. Architectural Scope & Problem Statement
  ...
  ```
- **Mapping Justification:** Conducts the line-by-line systems audit of `DISABLED_ELEMENTS`, Stage 4 serializer gates, and `DEFAULT_INCLUDE_ATTRIBUTES`, mapping the loss of JSON-LD, container `aria-label`, and custom `data-*` attributes.

---

### 5. `FINAL_SKEPTICAL_REVIEW.md`
- **Equivalent Primary File:** `FINAL_VALIDATION_07_ADVERSARIAL_REVIEW.md`
- **Secondary Reference:** `FINAL_REVIEW.md` (and `INDEPENDENT_FINAL_AUDIT.md`)
- **Content Excerpt Location:** Lines 1--15 of `FINAL_VALIDATION_07_ADVERSARIAL_REVIEW.md`:
  ```markdown
  # FINAL VALIDATION 07: ADVERSARIAL AND SKEPTICAL REVIEW REPORT
  ## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
  **Execution Date:** 2026-10-26
  **Status:** COMPLETE / REMEDIATION GATES PASSED
  ## 1. Adversarial Review Objective
  This document serves as an exhaustive, hyper-critical adversarial peer review...
  ```
- **Mapping Justification:** Serves as the adversarial skeptical examination that tracks every vulnerability, ceiling effect, confound, and statistical limitation across the study.

---

## 3. Compliance and Verification Note
In strict accordance with Rule R2, no historical files were renamed or deleted. All mappings cite existing files in the repository.

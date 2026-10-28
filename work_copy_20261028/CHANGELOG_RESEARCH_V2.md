# CHANGELOG: RESEARCH V2 RESTRUCTURING & ARTIFACT INVENTORY

**Project:** Autonomous Browser Agent Observation Pipeline & DOM Serialization Systems Study  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  
**Date:** October 21, 2026  
**Auditor / Engineer:** Research Supervisor & Lead Technical Auditor  

---

## 1. Summary of Changes

The research project was restructured from an underpowered, unexecuted behavioral task benchmark into a rigorous, offline-verified empirical systems study of DOM observation pipelines in autonomous web agents.

All original source code files, protocol specifications, historical datasets, and initial draft manuscripts have been preserved 100% intact. All enhancements were created as clean, versioned artifacts.

---

## 2. Artifacts Created & File Inventory

| Artifact File | Category | Rationale & Purpose | Supporting Evidence |
| :--- | :--- | :--- | :--- |
| [`PHASE1_BASELINE_AUDIT.md`](file:///C:/testing/research_execution_20261018/PHASE1_BASELINE_AUDIT.md) | Audit & Provenance | Establishes ground-truth baseline of installed library code, data provenance, and test execution status. | Direct AST inspection of `serializer.py` and test suite runs. |
| [`RESEARCH_DESIGN_V2.md`](file:///C:/testing/research_execution_20261018/RESEARCH_DESIGN_V2.md) | Methodology Specification | Formally realigns the study around Direction B (Systems Serialization Audit), defining revised RQs, objectives, boundaries, and novelty claims. | Directional evaluation matrix and literature grounding. |
| [`fixtures/edge_cases.html`](file:///C:/testing/research_execution_20261018/fixtures/edge_cases.html) | Test Fixture | Reproducible HTML test fixture evaluating nested elements, non-interactive containers, and empty attribute values. | WCAG 2.4.4 and DOM serialization specifications. |
| [`audit_metadata_reachability.py`](file:///C:/testing/research_execution_20261018/audit_metadata_reachability.py) | Verification Harness | Automated, offline test script measuring information loss between source HTML, live DOM, and final prompt buffer under `browser-use 0.13.10`. | Dynamic Playwright execution and agent message manager interception. |
| [`serialization_audit_metrics.json`](file:///C:/testing/research_execution_20261018/serialization_audit_metrics.json) | Empirical Dataset | Quantitative reachability metrics (percentages, token proxies, pruning mechanisms) across 7 channels and 3 edge cases. | Generated deterministically by `audit_metadata_reachability.py`. |
| [`SERIALIZATION_AUDIT_REPORT.md`](file:///C:/testing/research_execution_20261018/SERIALIZATION_AUDIT_REPORT.md) | Systems Report | Comprehensive systems analysis detailing the script-pruning black hole, non-interactive tag stripping, and attribute whitelisting. | Correlates machine-readable metrics with source code lines. |
| [`EXPERIMENT_AND_STATISTICS_AUDIT_V2.md`](file:///C:/testing/research_execution_20261018/EXPERIMENT_AND_STATISTICS_AUDIT_V2.md) | Statistical Audit | Audits Protocol v3 validity, power boundaries ($<11\%$), the Equivalence Fallacy, and the button-label co-location confound. | 10,000-trial Monte Carlo power simulations (`power_analysis.json`). |
| [`RESEARCH_PAPER_DRAFT_V2.md`](file:///C:/testing/research_execution_20261018/RESEARCH_PAPER_DRAFT_V2.md) | Working Paper | Revised academic manuscript presenting verified systems findings in main results, moving synthetic data to Appendix A, and adding reproducibility guides. | Integrates all Phase 1–4 evidence into a coherent publication draft. |
| [`FINAL_VALIDATION_REPORT.md`](file:///C:/testing/research_execution_20261018/FINAL_VALIDATION_REPORT.md) | Quality Assurance | Independent QA verification report confirming 100% test pass rate, claim-to-evidence agreement, and listing remaining scientific limitations. | Automated regression test execution (22/22 tests passing). |
| [`CHANGELOG_RESEARCH_V2.md`](file:///C:/testing/research_execution_20261018/CHANGELOG_RESEARCH_V2.md) | Project Governance | Complete record of all modifications, rationale, and governance decisions. | This document. |

---

## 3. Preserved Original Assets (Strict Immutability)

The following authentic files remain completely unmodified:
- [`protocol.md`](file:///C:/testing/research_execution_20261018/protocol.md) (Original Protocol v3 specification)
- [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) (Original runner with safety gate locked)
- [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py) (Original statistical analysis engine)
- [`RESEARCH_PAPER_DRAFT.md`](file:///C:/testing/research_execution_20261018/RESEARCH_PAPER_DRAFT.md) (Original paper draft containing historical structure)
- [`results/pilot-summary-clean.csv`](file:///C:/testing/results/pilot-summary-clean.csv) (Historical 250-run pilot dataset)
- [`results/main_experiment/full-summary.csv`](file:///C:/testing/results/main_experiment/full-summary.csv) (Aborted 147-run main experiment dataset)
- [`test_scratch_synthetic_data/dataset_1_valid_complete.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv) (Synthetic validation dataset)
- All website variant HTML, JS, and CSS files in [`variants/`](file:///C:/testing/variants/) and [`shared/`](file:///C:/testing/shared/).

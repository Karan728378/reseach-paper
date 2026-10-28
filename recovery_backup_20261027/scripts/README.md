# Maintained Project Scripts Directory

This directory contains verified, deterministic, and maintained production utilities for the research project:
*The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents*.

## Script Index

| Script | Purpose | Input Artifacts | Output Artifacts | Primary Verification Command |
| :--- | :--- | :--- | :--- | :--- |
| `verify_hashes.py` | Validates raw JSON traces and historical CSVs against baseline SHA-256 hashes. | `BASELINE_DATA_INVENTORY_SHA256.md`, `results/3arm_runs/` | Console stdout | `python scripts/verify_hashes.py` |
| `independent_ledger_audit.py` | Reconciles physical JSON attempt files, scheduled units, aborted runs, and quarantines. | `proposed_3arm_schedule.csv`, `results/3arm_runs/*.json` | Console stdout | `python scripts/independent_ledger_audit.py` |
| `audit_route_controls_and_correspondence.py` | Performs deterministic DOM census across `#home`, `#cart`, `#checkout`, `#search` and checks AXTree correspondence. | Route fixtures in `fixtures/` | `multi_route_observation_audit.json` | `python scripts/audit_route_controls_and_correspondence.py` |
| `audit_multi_framework_observation.py` | Evaluates observation reachability (JSON-LD, ARIA, data-*) across browser-use, Chromium Blink AXTree, Raw DOM, Playwright, BrowserGym. | `fixtures/multi_framework_observation_fixture.html` | `multi_framework_observation_audit.json`, `MULTI_FRAMEWORK_OBSERVATION_TAXONOMY.md` | `python scripts/audit_multi_framework_observation.py` |
| `reproduce_power_audit.py` | Computes statistical power curves and minimum detectable effect (MDE) sizes via Monte Carlo simulation and TOST. | N/A (Mathematical simulation) | `STATISTICAL_POWER_AUDIT_FINAL.md` | `python scripts/reproduce_power_audit.py` |
| `reconcile_v3_results.py` | Generates authoritative reconciled dataset (`v3_3arm_summary_reconciled_v2.csv`) and forensic audit report. | `results/v3_3arm_summary_raw.csv`, `results/3arm_runs/*.json` | `v3_3arm_summary_reconciled_v2.csv`, `v3_3arm_reconciliation_audit.json` | `python scripts/reconcile_v3_results.py` |

## Distinction from `scratch/`

- **`scripts/`**: Contains maintained, documented, reusable, production-tested scripts intended for long-term auditability and public artifact reproduction.
- **`scratch/`**: Contains temporary exploratory harnesses, debugging logs, ad-hoc forensic scripts, and scratch calculations created during experimental investigation. Retained strictly to preserve historical record integrity and ensure legacy script paths remain resolvable.

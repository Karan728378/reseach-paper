# PROTOCOL VERSION HISTORY: DESIGN EVOLUTION & GOVERNANCE

**Project Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Workspace:** `C:\testing\research_execution_20261018`  
**Date:** October 26, 2026  
**Auditor:** Scientific Methodology & Experimental Design Team  

---

## 1. Protocol Revision History

| Protocol Version | Date | Target Scope | Arm Definitions | Primary Mechanism / Evolution | Execution Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Protocol v1.0** | Oct 18, 2026 | Initial Benchmark Design | ABS vs. ARIA | Initial exploratory concept evaluating raw HTML vs. semantic annotations. | Deprecated |
| **Protocol v2.0** | Oct 20, 2026 | Added Custom Data Attributes | ABS, ARIA, DATA-CFG | Added `v3-data-attrs` variant; identified need for attribute whitelist extension. | Deprecated |
| **Protocol v3.0** | Oct 22, 2026 | Randomized Complete Block Design (RCBD) | ABS, ARIA, DATA-CFG (72 scheduled units across 6 blocks) | Formalized 3-arm RCBD with 5 task strata (T1–T5) and budget governance. | **PARTIALLY EXECUTED** (Runs 1–41 executed; halted at budget ceiling) |
| **Protocol v3.1** | Oct 24, 2026 | Reconciliation & Duplicate Quarantine | ABS (13), ARIA (13), DATA-CFG (13 eligible, 2 quarantined) | Implemented fail-closed deduplication quarantine isolating duplicate runs 34 and 38. | **AUDITED & FROZEN** |
| **Protocol v4.0** | Oct 25, 2026 | 4-Arm Confirmatory Proposal | BASELINE (ABS), BASELINE_REP (VIS), ARIA, DATA-CFG (96 runs) | Proposed 4-arm design with separate visual replication arm and Task T6 refusal probe. | **PROPOSED / UNEXECUTED** (Safety gate locked; 0 runs executed) |
| **Protocol v4.1 (Probes)** | Oct 26, 2026 | Disambiguation Probes A & B | Negative Baseline ($\textsc{ABS}$) vs. Configured Attributes ($\textsc{DATA-CFG}$) | De-confounded single-action probe fixtures isolating target identity to button `data-product-id` (Probe A) or container `aria-label` (Probe B). | **OFFLINE VERIFIED / UNEXECUTED** (HTML fixtures built, unit tests passing, awaiting live execution) |

---

## 2. Definitive Arm Definitions

To prevent terminological ambiguity:
1. **$\textsc{ABS}$ (Negative Baseline):** Standard `browser-use 0.13.10` observation pipeline using `DEFAULT_INCLUDE_ATTRIBUTES`. Website markup is `variants/v0-baseline`.
2. **$\textsc{ARIA}$ (Accessibility Markup):** Standard `browser-use 0.13.10` pipeline. Website markup is `variants/v2-aria` (WAI-ARIA roles, states, accessible labels).
3. **$\textsc{DATA-CFG}$ (Extended Developer Attributes):** Runner passes `EXTENDED_ATTRIBUTES` including `data-product-id`, `data-action`. Website markup is `variants/v3-data-attrs`.
4. **$\textsc{VIS}$ (Visual Baseline - Protocol v4 only):** Planned control arm providing rendered visual typography under identical baseline markup.

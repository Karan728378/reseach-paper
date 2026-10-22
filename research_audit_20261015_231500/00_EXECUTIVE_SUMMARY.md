# 00. Executive Summary & Forensic Audit Report

**Audit Identifier:** `research_audit_20261015_231500`  
**Target Workspace:** `C:\testing`  
**Audit Completion Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  
**Compliance Statement:** 100% Zero-API offline audit. Zero paid-model calls, zero network requests to LLMs, zero quota consumption, and zero modification of original research files.

---

## 1. Major Verified Findings & Evidence Summary

### 1. Verification of the Original "105 / 42 / 53" Experiment Claim
- **Status:** **CONFIRMED, WITH FATAL SAMPLING BIAS DISCLOSED**
- **Evidence:**
  - Independent analysis of [`results/main_experiment/full-summary.csv`](file:///C:/testing/results/main_experiment/full-summary.csv) and raw files confirmed exactly 147 scheduled runs were initiated.
  - Runs 1 through 105 succeeded consecutively (100% success rate between 07:37:57 and 08:29:58 UTC).
  - At run 106, Google Gemini API free-tier quota was exhausted (`429 RESOURCE_EXHAUSTED`, 500 requests/day limit reached).
  - The runner did not halt; it executed 42 consecutive failing runs (indices 106–147), each failing after ~8–10 seconds and 7 failed steps.
  - Runs 148 through 200 (exactly 53 runs) were never executed.
  - **Critical Finding:** The 105 successful runs do **not** form a balanced or random sample. Missingness is Missing Not At Random (MNAR) / time-of-day right-truncated. Cell sample sizes range from 2 to 8 runs.

### 2. Fatal Treatment Delivery Failure in Browser-Use 0.13.10
- **Status:** **EMPIRICALLY AND DETERMINISTICALLY PROVEN**
- **Evidence:**
  - Direct source code inspection and offline stub-model testing in `browser-use 0.13.10` confirmed:
    - `<script>` (JSON-LD) and `<meta>` tags are hard-coded in `DISABLED_ELEMENTS` ([`serializer.py:18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18)) and pruned at line 481. **They have 0% exposure to the LLM.**
    - Custom `data-*` attributes (`data-sku`, `data-action`) are stripped by `DEFAULT_INCLUDE_ATTRIBUTES` ([`views.py:18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/views.py#L18)) unless explicitly passed to `Agent(include_attributes=...)`.
    - Non-interactive elements (such as `<span>` or `<time>`) are stripped by `serialize_tree` ([`serializer.py:1043`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1043)), discarding any attributes placed on them.
  - **Verdict:** In original Experiment 1, variants `v1-jsonld`, `v3-data-attrs`, and static `v4-evidence-meta` provided **zero additional representation** to the LLM. The agent operated with 0% access to the experimental features.

### 3. Severe Flaws in Original Experimental Verifiers
- **T3 Overly Permissive Ground Truth:** [`runner/verifier.py:61`](file:///C:/testing/runner/verifier.py#L61) defined `eligible_skus` to include 6 items. An agent selecting the *lowest-rated* product (`wh-001`, 4.2 stars) or a *keyboard* (`mkp-001`) was scored as a perfect 1.0 success.
- **T4 Unconditional Partial Scoring:** [`runner/verifier.py:479`](file:///C:/testing/runner/verifier.py#L479) added 0.25 points unconditionally, awarding points even to quota failures that never executed an action.
- **T5 Cart Seeding Vulnerability:** [`runner/verifier.py:458`](file:///C:/testing/runner/verifier.py#L458) checked only `len(cart) == 0`. An unseeded cart or failed page load scores 1.0 with zero agent interaction.
- **Visible Text Confound:** In T1–T5, all target facts (prices, ratings, names) were fully visible as standard body text on all variants.

### 4. Resolution of the Arithmetic Inconsistency in the Proposed Redesign
- The proposed blueprint conflicted: it described 6 conditions, a "24-run block", and "90 total runs".
- **Arithmetic Proof:** 
  - $6 \text{ tasks} \times 4 \text{ conditions} = \mathbf{24\text{ runs per block}}$ (the origin of the 24-run block).
  - $6 \text{ tasks} \times 6 \text{ conditions} = \mathbf{36\text{ runs per block}}$.
  - 3 repetitions of 36 runs = $\mathbf{108\text{ runs}}$, not 90!
- **Resolution:** We freeze a mathematically balanced 4-arm design:
  $$6 \text{ Tasks} \times 4 \text{ Conditions} \times 4 \text{ Blocks} = \mathbf{96\text{ total runs}}$$

---

## 2. Directory & Deliverable Map

All artifacts, manifest files, test fixtures, and captured observation logs have been saved in a new, isolated directory without modifying any existing files:

`C:\testing\research_audit_20261015_231500\`

| File Name | Description |
|---|---|
| [`00_EXECUTIVE_SUMMARY.md`](file:///C:/testing/research_audit_20261015_231500/00_EXECUTIVE_SUMMARY.md) | Comprehensive executive summary and verdict (this document). |
| [`01_FILE_HASH_MANIFEST.csv`](file:///C:/testing/research_audit_20261015_231500/01_FILE_HASH_MANIFEST.csv) | SHA-256 hash manifest of all 2,012 project files. |
| [`02_DATA_INTEGRITY_AUDIT.md`](file:///C:/testing/research_audit_20261015_231500/02_DATA_INTEGRITY_AUDIT.md) | Complete inventory and forensic trace of the 105/42/53 claim. |
| [`03_ORIGINAL_EXPERIMENT_AUDIT.md`](file:///C:/testing/research_audit_20261015_231500/03_ORIGINAL_EXPERIMENT_AUDIT.md) | Task-by-task execution accounting and validity threat evaluation. |
| [`04_BROWSER_USE_EXPOSURE_AUDIT.md`](file:///C:/testing/research_audit_20261015_231500/04_BROWSER_USE_EXPOSURE_AUDIT.md) | Architectural code path audit and 6-level channel exposure matrix. |
| [`05_RESEARCH_DESIGN_RECOMMENDATION.md`](file:///C:/testing/research_audit_20261015_231500/05_RESEARCH_DESIGN_RECOMMENDATION.md) | Evaluation of candidate conditions and task redesign recommendations. |
| [`06_SAMPLE_SIZE_AND_STATISTICS.md`](file:///C:/testing/research_audit_20261015_231500/06_SAMPLE_SIZE_AND_STATISTICS.md) | Arithmetic reconciliation, power calculations, and GLMM plan. |
| [`07_LITERATURE_AND_NOVELTY_AUDIT.md`](file:///C:/testing/research_audit_20261015_231500/07_LITERATURE_AND_NOVELTY_AUDIT.md) | Literature trace (arXiv:2607, 2609, 2605, 2601) and novelty assessment. |
| [`08_PROTOCOL_DRAFT.md`](file:///C:/testing/research_audit_20261015_231500/08_PROTOCOL_DRAFT.md) | Reproducible Protocol v3 draft with complete trial schedule. |
| [`09_OFFLINE_TEST_RESULTS.md`](file:///C:/testing/research_audit_20261015_231500/09_OFFLINE_TEST_RESULTS.md) | Empirical logs of offline verifier, exposure, and parity tests. |
| [`10_BLOCKERS_AND_NEXT_ACTIONS.md`](file:///C:/testing/research_audit_20261015_231500/10_BLOCKERS_AND_NEXT_ACTIONS.md) | Remaining blockers, decision gates, and single next action. |
| [`channel_exposure_matrix.json`](file:///C:/testing/research_audit_20261015_231500/channel_exposure_matrix.json) | Programmatic JSON matrix of token exposure across pipelines. |
| [`power_calculations.json`](file:///C:/testing/research_audit_20261015_231500/power_calculations.json) | Programmatic power and sample size calculation results. |

---

## 3. Final Strategic Recommendation & Decision

### Verdict: **PROCEED TO PROTOCOL FREEZE WITH THE 4-ARM 96-RUN BENCHMARK**

The original research question—investigating whether semantic web markup affects AI web agent task completion—is valid, timely, and empirically novel. However, the original experimental implementation failed because the agent harness aggressively stripped the markup before the LLM could perceive it.

By adopting **Protocol v3** (4 arms: ABS, VIS, ARIA, DATA-CFG; 6 isolated fact-retrieval tasks; 96 balanced runs; robust exact-match verifiers), the study eliminates all construct confounds and provides the scientific community with a rigorous, reproducible measurement of web agent channel sensitivity.

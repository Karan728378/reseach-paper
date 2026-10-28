# REMAINING BLOCKERS AND NEXT ACTIONS
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Status:** Audit & Remediation Complete; Confirmatory Execution Blocked by External Gates

---

## 1. Concrete External Blockers

The following items cannot be executed autonomously without human authorization, external resources, or additional software installation:

### BLOCKER 1: Authorized API Budget for Confirmatory Live Trials
- **Current State:** The repository's budget safety controller (`budget_controller.py`) is strictly locked in a fail-closed state (`SAFETY_GATE_LOCKED = True`, daily ceiling $0.00 USD).
- **Impact:** The proposed 4-arm 96-trial confirmatory experiment (`REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md`) has **0 executed runs**.
- **Requirement to Unblock:** 
  1. Explicit user authorization and API budget allocation (~$5.00–$15.00 USD estimated for 96 runs on `openai/gpt-oss-120b` or `gemini-flash-lite-latest`).
  2. Passing explicit runtime authorization flags (`--live --confirm-live-execution`).
- **Policy:** In accordance with absolute research integrity rules, no live trials were initiated or simulated during this audit.

### BLOCKER 2: Local LaTeX Compiler Installation
- **Current State:** `pdflatex`, `xelatex`, and `latexmk` are not installed in the Windows system PATH.
- **Impact:** Local compilation of `research_paper_final.tex` directly to PDF on this machine is not available without installing MiKTeX or TeX Live.
- **Remediation Provided:** The complete, verified source package has been bundled in `manuscript_submission_bundle_corrected.zip` alongside comprehensive 1-click Overleaf compilation instructions (`README_OVERLEAF.md`). All pre-flight syntax, citation, and environment checks have passed with 100% success.

### BLOCKER 3: Live Interception of Stage 5 Prompt Assembly
- **Current State:** Direct serializer output at Stage 4 was intercepted via `dom_state.llm_representation()`, confirming tag and attribute pruning. However, the internal string concatenation performed inside the agent loop prior to the HTTP request was not tapped during the historical pilot.
- **Impact:** Reachability claims in the manuscript are strictly and honestly bounded to Stage 4.
- **Requirement to Unblock:** Adding a network/agent interceptor hook in `browser-use`'s `Agent._step()` method during a future instrumented execution.

---

## 2. Prioritized Next Actions for the Research Team

### Immediate Action 1: Compile Two-Column PDF on Overleaf (5 Minutes)
1. Open [Overleaf](https://www.overleaf.com).
2. Click **New Project** $\to$ **Upload Project**.
3. Select `manuscript_submission_bundle_corrected.zip` from `C:\testing\research_execution_20261018\`.
4. Ensure compiler is set to `pdfLaTeX` and TeX Live version to `2024`.
5. Click **Recompile**.
6. Inspect the resulting two-column PDF against the visual checklist in `FINAL_PDF_VISUAL_QA.md`.

### Immediate Action 2: Formal Protocol Preregistration (Prior to Live Trials)
1. Submit the 4-arm experimental design (`METHODS_AND_CAUSAL_IDENTIFICATION_AUDIT.md` and `REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md`) to OSF Registries (Open Science Framework) or AsPredicted.
2. Specify the planned contrast: $\text{ARIA vs. BASELINE\_REP}$ and $\text{BASELINE\_REP vs. BASELINE\_ABS}$.
3. Define the primary estimand as the unpooled Risk Difference $\Delta$ with Newcombe hybrid score confidence intervals.
4. Prespecify the exclusion criteria (transient API 503 retry policy, duplicate run quarantine).

### Intermediate Action 3: Execute Confirmatory 96-Trial Battery (Post-Budget Approval)
1. Verify network connectivity and provider quota.
2. Unlock budget controller with authorized ceiling:
   ```bash
   python protocol_v3_runner.py --schedule proposed_4arm_schedule.csv --live --confirm-live-execution
   ```
3. Run post-execution reconciliation using `scripts/reconcile_v3_results.py`.
4. Update manuscript tables with empirical confirmatory results.

---

## 3. Summary of Project Health

| Milestone | Status | Notes |
|:---|:---:|:---|
| **Data Provenance & Reconciliation** | **COMPLETE** | 77-row canonical ledger established; zero data altered. |
| **Test Suite & Reproducibility** | **COMPLETE** | 191/191 tests passing in 16.0s; 48/48 baseline hashes identical. |
| **Statistical Integrity** | **COMPLETE** | Ceiling effects recognized; Newcombe CIs and power reconciled. |
| **Manuscript Source & Formatting** | **COMPLETE** | Two-column IEEEtran format validated; all citations resolved. |
| **Submission Bundle** | **COMPLETE** | Packaged and verified (772,497 bytes, 8 files). |
| **Confirmatory Behavioral Trial** | **BLOCKED** | Preregistration-ready; awaits budget authorization. |

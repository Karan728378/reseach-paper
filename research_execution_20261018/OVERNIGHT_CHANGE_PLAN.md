# OVERNIGHT CHANGE PLAN & EXECUTION SPECIFICATION

**Timestamp:** 2026-10-25T02:52:30+05:30  
**Host Workspace:** `C:\testing`  
**Research Directory:** `C:\testing\research_execution_20261018`  
**Backup Archive:** `c:\testing\research_execution_20261018\backups\overnight_backup_20261025`  
**Status:** ACTIVE / PHASED EXECUTION  

---

## 1. Safety and Isolation Principles

1. **Strict Offline Execution:** No live API requests to external models, no billable endpoints, no tampering with `results/daily_quota_ledger.json`.
2. **Data Preservation:** Raw result ledgers (`v3_3arm_summary.csv`, `v3_run_summary.csv`, `local_llama_summary.csv`, `accessibility_tree_comparison.json`) remain strictly read-only primary sources.
3. **Change Isolation:** All modifications to manuscript (`research_paper_final.tex`), figure (`architecture_pipeline_figure.tex`), bibliography (`references.bib`), and guides are backed up in `backups/overnight_backup_20261025/`.
4. **Selective Staging:** Git staging will include only intended research deliverables and reports. Virtual environments, caches, local temporary files, and sensitive credentials will never be committed or pushed.

---

## 2. Planned Deliverables and Target Files

| Phase / Workstream | Deliverable File | Target Action / Rationale |
| :--- | :--- | :--- |
| **Phase 1: Workstream 1** | `OVERNIGHT_BASELINE_INVENTORY.md` | Document verified runtime facts, environment, hashes, baseline tests. |
| **Phase 1: Workstream 2** | `OVERNIGHT_CHANGE_PLAN.md` | Establish isolated execution schedule, backup index, safety rules. |
| **Phase 2: Workstream 3** | `EVIDENCE_TO_CLAIM_MATRIX.csv`<br>`CLAIM_PROVENANCE_AUDIT.md` | Map every manuscript claim to line number, primary evidence, and status. |
| **Phase 3: Workstream 4** | `MODEL_RUN_PROVENANCE_AUDIT.md` | Trace Gemini 3.1 vs 2.5 Flash Lite, Qwen 7B vs 4B, latencies, 503 retries. |
| **Phase 4: Workstream 5** | `POWER_ANALYSIS_REPRODUCTION.md` | Recompute Monte Carlo power simulation (seed 42, $N=20$, $d=0.20,0.35,0.70$). |
| **Phase 4: Workstream 6** | `TOST_SAMPLE_SIZE_AUDIT.md` | Independently derive equivalence sample size ($N \approx 360, 429, 468$). |
| **Phase 4: Workstream 7** | `CLUSTERING_AND_EXPERIMENTAL_UNIT_AUDIT.md` | Audit design effect $\text{DEFF} = 1 + (m-1)\rho$, sensitivity over $m$ and $\rho$. |
| **Phase 4: Workstream 8** | `INTERVALS_MULTIPLICITY_AND_ESTIMANDS_AUDIT.md` | Recompute Wilson, Newcombe (56/70 vs 38/80), CMH asymptotic properties. |
| **Phase 5: Workstream 9** | `DOM_OBSERVATION_CHANNEL_AUDIT.md` | Trace HTML -> Live DOM -> AXTree -> Internal Snapshot -> Selector Map -> Prompt. |
| **Phase 5: Workstream 10** | `ACCESSIBILITY_CORRESPONDENCE_AUDIT.md` | Audit 27/34 selector-map entries, 7 unmatched badges ($48.6\times 15$px vs $74.8$px). |
| **Phase 6: Workstream 11** | `TOOL_REACHABILITY_AND_OBSERVATION_LIMITS.md` | Separate initial observation omission from direct tool recoverability. |
| **Phase 6: Workstream 12** | `CROSS_FRAMEWORK_FEASIBILITY_AUDIT.md` | Cross-framework audit (BrowserGym, Stagehand, Playwright MCP). |
| **Phase 7: Workstream 13** | `FUTURE_BEHAVIORAL_EXPERIMENT.md` | Complete unexecuted 4-arm RCBD protocol with preflight validation. |
| **Phase 8: Workstream 14** | `TEST_COVERAGE_AND_REPAIR_LOG.md` | Add targeted regression tests (statistical bounds, data provenance, geometry). |
| **Phase 8: Workstream 15** | `INDEPENDENT_FINAL_VALIDATION.md` | Fresh validation pass: tests, hashes, recomputations, clean diff. |
| **Phase 9: Workstream 16** | `MANUSCRIPT_REVISION_CHANGELOG.md`<br>`research_paper_final.tex` | Full scientific consistency review of manuscript source text. |
| **Phase 9: Workstream 17** | `LATEX_AND_PDF_VALIDATION.md`<br>`architecture_pipeline_figure.tex`<br>`references.bib` | TikZ figure geometry verification, bibliography integrity, PDF inspection. |
| **Phase 10: Workstream 18** | `REPRODUCIBILITY_GUIDE.md` | Deterministic instructions for offline verification and artifact inspection. |
| **Phase 10: Workstream 19** | `SUBMISSION_PACKAGE_INTEGRITY.md`<br>`manuscript_submission_bundle_corrected.zip` | Rebuild verified zip bundle and validate SHA-256 integrity. |
| **Phase 11: Workstream 20** | `GITHUB_DELIVERY_REPORT.md` | Review git diff, scan for secrets, stage research deliverables, commit, push. |
| **Phase 12: Acceptance** | `OVERNIGHT_FINAL_REPORT.md` | Final acceptance gate report summarizing all 20 workstreams. |

---

## 3. Rollback Strategy

In the event of an unexpected regression or file corruption:
- Revert the damaged file from `backups/overnight_backup_20261025/`.
- Re-run `& "C:\testing\.venv311\Scripts\python.exe" -m unittest discover -s . -p "test_*.py"` to confirm system stability.
- Re-verify git status via `git status --short`.

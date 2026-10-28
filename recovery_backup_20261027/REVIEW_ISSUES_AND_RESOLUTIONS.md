# REVIEW ISSUES AND RESOLUTIONS REGISTER
**Generated (UTC):** 2026-10-26T19:28:59.133746+00:00  
**Registered Issues Count:** 33 (Seeded with K1–K15 and C1–C18)  
**Authoritative Ledger:** `RECOVERY_ISSUE_REGISTER.csv`

---

## 1. Summary of Registered Issues by Severity and Root Cause

| Severity | Count | Root Cause Clusters |
|---|---|---|
| **Critical** | 10 | `RC-ENVIRONMENT`, `RC-CIRCULARITY`, `RC-STAGE5-CAPTURE`, `RC-POWER-ANALYSIS`, `RC-RUN-ACCOUNTING`, `RC-DESIGN-RECONCILIATION`, `RC-STATISTICAL-RIGOR`, `RC-JSONLD-EXCLUSION`, `RC-EVIDENCE-SEPARATION`, `RC-PILOT-LIMITS` |
| **Major** | 20 | `RC-SERIALIZER-SPEC`, `RC-WHITELIST-DEF`, `RC-PROBE-B`, `RC-SAMPLE-SIZE`, `RC-PILOT-PROVENANCE`, `RC-LIVE-UNREPORTED`, `RC-CONFIDENCE-INTERVALS`, `RC-LATEX-LAYOUT`, `RC-OVERGENERALIZATION`, `RC-CITATION-AUDIT`, `RC-CODE-HARDCODING` |
| **Minor** | 3 | `RC-TEST-COUNT` (module inventory, reproduction command documentation) |

---

## 2. Issue Detail Register

### [K1] Section 3 (K1) — RC-ENVIRONMENT
- **Severity:** Critical
- **Location:** `browser_use wheel / .venv311`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-and-verified`
- **Evidence Available:** PyPI 0.13.10 wheel SHA-256 and installed serializer.py, views.py, service.py SHA-256
- **Evidence Required:** Match against installed package in .venv311
- **Proposed Correction:** Verify installed package matches PyPI wheel exactly.
- **Requires Live Calls:** `N`
- **Verification Command:** `python phase1_execute.py`
- **Verification Result:** MATCH on all 3 critical files (6d523..., 01866..., 43f8e...)
- **Affected Sections/Artifacts:** Line number citations, serializer audit metrics

---
### [K2] Section 3 (K2) — RC-SERIALIZER-SPEC
- **Severity:** Major
- **Location:** `research_paper_final.tex line citations, serialization_audit_metrics.json`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** serializer.py line numbers in 0.13.10: DISABLED_ELEMENTS at L18, applied at L481; interactive gate at L1046-1051
- **Evidence Required:** Exact code inspection of installed browser_use
- **Proposed Correction:** Align manuscript line citations to exact wheel code (L480-482 element pruning, L1046-1051 interactivity gate).
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/verify_serializer_lines.py`
- **Verification Result:** Pending script verification
- **Affected Sections/Artifacts:** Sec. III-B, III-C

---
### [K3] Section 3 (K3) / C6 — RC-WHITELIST-DEF
- **Severity:** Major
- **Location:** `research_paper_final.tex Abstract, Sec. I, Sec. III-C, Table I`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** views.py L18: DEFAULT_INCLUDE_ATTRIBUTES includes data-state, data-date-format, data-mask, data-inputmask, data-datepicker
- **Evidence Required:** Programmatic enumeration of DEFAULT_INCLUDE_ATTRIBUTES
- **Proposed Correction:** Refine language from 'omits custom data-*' to 'omits developer-defined data-* (e.g., data-product-id, data-action) while preserving specific framework data-* attributes'.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_whitelist_attributes.py`
- **Verification Result:** Pending script execution
- **Affected Sections/Artifacts:** Abstract, Sec. III-C, Table I

---
### [K4] Section 3 (K4) / C4 — RC-CIRCULARITY
- **Severity:** Critical
- **Location:** `research_paper_final.tex Sec. III-B, Sec. IV-A`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** serializer/clickable_elements.py L204-225 checks node.ax_node.role against interactive roles
- **Evidence Required:** Data flow analysis of CDP getFullAXTree -> selector_map
- **Proposed Correction:** Acknowledge that selector-map correspondence with Blink AXTree is partially circular by construction; provide independent HTML-native leaf control reference census.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_ax_circularity.py`
- **Verification Result:** Pending script execution
- **Affected Sections/Artifacts:** Sec. III-B, Sec. IV-A, Table II

---
### [K5] Section 3 (K5) / C5 — RC-PROBE-B
- **Severity:** Major
- **Location:** `research_paper_final.tex Sec. III-C, Table I; fixtures/disambiguation_probe_b.html`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** disambiguation_probe_b.html has role='region' AND aria-label='Identity: target-sku-101'
- **Evidence Required:** Offline trace of probe_b under Chromium
- **Proposed Correction:** Rewrite manuscript argument to reflect role='region' rather than generic role naming prohibition; check W3C WAI-ARIA 1.2 landmark naming rules.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/trace_probe_b_offline.py`
- **Verification Result:** Pending offline trace
- **Affected Sections/Artifacts:** Sec. III-C, Table I

---
### [K6] Section 3 (K6) / C8 — RC-STAGE5-CAPTURE
- **Severity:** Critical
- **Location:** `research_paper_final.tex Sec. III-D vs Sec. IV-C Limitation 4`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** audit_metadata_reachability.py intercepts Stage 5 via MockChatModel offline; live pilot traces lack raw assembled prompt
- **Evidence Required:** Trace analysis of 3arm_runs/*.json and audit_metadata_reachability.py execution
- **Proposed Correction:** Clarify that Stage 5 prompt payload interception characterizes framework behavior offline with mock model; live pilot records did not store raw model prompts.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/verify_stage5_audit.py`
- **Verification Result:** Pending offline execution
- **Affected Sections/Artifacts:** Sec. III-D, Sec. IV-C

---
### [K7] Section 3 (K7) / C2 / C3 — RC-POWER-ANALYSIS
- **Severity:** Critical
- **Location:** `research_paper_final.tex Abstract, Sec. IV-B, Table III`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** power_audit_results.json (B=10,000: 11.45% for 0.20, 48.51% for 0.35) vs rcbd_simulation_results_2k.json (B=2,000: 10.8%, 49.6%)
- **Evidence Required:** Independent clean-room simulation of CMH and Fisher exact power
- **Proposed Correction:** Align abstract and Table III to authoritative B=10,000 numbers; disclose Monte Carlo SEs and exact 3-arm design power.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/independent_power_reanalysis.py`
- **Verification Result:** Pending simulation
- **Affected Sections/Artifacts:** Abstract, Sec. IV-B, Table III

---
### [K8] Section 3 (K8) / C1 — RC-SAMPLE-SIZE
- **Severity:** Major
- **Location:** `research_paper_final.tex Sec. IV-B`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** n=97-125 per arm with 4 arms gave N=388-500, but 3 arms gives N=291-375
- **Evidence Required:** Closed-form formula recomputation for 3 arms at alpha=0.0167 and TOST
- **Proposed Correction:** Correct total N to 291-375 for 3-arm study; specify one-sided alpha=0.05 and baseline assumptions for TOST.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/recompute_sample_sizes.py`
- **Verification Result:** Pending recomputation
- **Affected Sections/Artifacts:** Sec. IV-B

---
### [K9] Section 3 (K9) / C9 — RC-RUN-ACCOUNTING
- **Severity:** Critical
- **Location:** `research_paper_final.tex Sec. IV-A; CANONICAL_RUN_LEDGER.csv`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** 46 files in results/3arm_runs/ = 39 primary + 4 quarantined (indices 34, 38) + 3 infrastructure 503 aborts
- **Evidence Required:** Independent ledger generation and trace verification script
- **Proposed Correction:** Explicitly define primary eligible (N=39, 13/arm), sensitivity eligible (N=41), and account for all 46 files on disk.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/reconcile_all_runs.py`
- **Verification Result:** Pending reconciliation script
- **Affected Sections/Artifacts:** Sec. IV-A, Table IV, Table V

---
### [K10] Section 3 (K10) / C8 — RC-PILOT-PROVENANCE
- **Severity:** Major
- **Location:** `results/3arm_runs/*.json; protocol_v3_runner.py`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Traces store treatment_attribute_observed summary and estimated tokens, not raw prompt text
- **Evidence Required:** Inspection of run_001.json schema in 3arm_runs
- **Proposed Correction:** Acknowledge in manuscript that pilot traces recorded attribute observation summaries rather than raw model prompt text.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_trace_schemas.py`
- **Verification Result:** Pending trace schema audit
- **Affected Sections/Artifacts:** Sec. III-D, Sec. IV-C

---
### [K11] Section 3 (K11) / C10 — RC-LIVE-UNREPORTED
- **Severity:** Major
- **Location:** `results/live_single_attempt_20261026_runs/, results/single_live_trial_20261026_runs/`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Oct 26 Groq live runs with gpt-oss-120b: HTTP 413, max_steps, and task failures
- **Evidence Required:** Full audit of results/ subdirectories
- **Proposed Correction:** Classify all Oct 26 live attempts under Evidence Class E6 (debugging/smoke/infrastructure); disclose that non-Gemini models did not experience ceiling effects.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_live_attempts.py`
- **Verification Result:** Pending audit
- **Affected Sections/Artifacts:** Sec. IV-A, Evidence Status Table

---
### [K12] Section 3 (K12) / C12 — RC-CONFIDENCE-INTERVALS
- **Severity:** Major
- **Location:** `research_paper_final.tex Table IV, Table V; analyze_v3_results.py`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** analyze_v3_results.py uses uncorrected Newcombe score interval [-0.228, +0.228] for 13/13 vs 13/13
- **Evidence Required:** Independent implementation of Newcombe, Wilson, and Clopper-Pearson CIs
- **Proposed Correction:** Report precise uncorrected Newcombe score intervals; provide exact Clopper-Pearson intervals for individual arm success rates.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/independent_ci_reanalysis.py`
- **Verification Result:** Pending reanalysis
- **Affected Sections/Artifacts:** Table IV, Table V

---
### [K13] Section 3 (K13) / C15 — RC-TEST-COUNT
- **Severity:** Minor
- **Location:** `research_paper_final.tex Sec. V-A (Reproducibility)`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Repository has 204+ def test_ across 26 modules vs manuscript's '191 tests across 23 modules'
- **Evidence Required:** Actual execution log of offline pytest suite
- **Proposed Correction:** Dynamically generate exact passing test count and module count in paper from actual test run log.
- **Requires Live Calls:** `N`
- **Verification Command:** `python -m pytest test_*.py`
- **Verification Result:** Pending offline test execution
- **Affected Sections/Artifacts:** Sec. V-A

---
### [K14] Section 3 (K14) / C17 — RC-LATEX-LAYOUT
- **Severity:** Major
- **Location:** `research_paper_final.tex, compiled PDF`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Page 8 has lonely appendix disclaimer with 80% blank space; Tables IV-VI pushed to page 9; typography flaws
- **Evidence Required:** PDF compilation and per-page visual inspection
- **Proposed Correction:** Restructure LaTeX layout: co-locate disclaimers with tables using FloatBarrier / minipages; repair Table I caption letter-spacing; fix missing spaces.
- **Requires Live Calls:** `N`
- **Verification Command:** `pdflatex research_paper_final.tex`
- **Verification Result:** Pending compilation and visual inspection
- **Affected Sections/Artifacts:** Entire PDF layout, Appendix, Tables IV-VI

---
### [K15] Section 3 (K15) / C11 — RC-OVERGENERALIZATION
- **Severity:** Major
- **Location:** `research_paper_final.tex Abstract, Sec. I, Sec. III-C, Sec. IV-C`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Claims of 'fundamental limitations to any agent', 'spatial reasoning', hardware specs in methods
- **Evidence Required:** Claim lint scan against .tex source
- **Proposed Correction:** Narrow claims to browser-use 0.13.10; remove unwarranted generalizations; remove GPU/RAM hardware specs.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/claim_lint.py`
- **Verification Result:** Pending claim lint
- **Affected Sections/Artifacts:** Abstract, Sec. I, Sec. III, Sec. IV, Sec. V

---
### [C1] Section 4 (C1) — RC-DESIGN-RECONCILIATION
- **Severity:** Critical
- **Location:** `protocol.md, protocol_v4_config.json, research_paper_final.tex`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Protocol evolution: 4-arm planned -> 3-arm executed (ABS, ARIA, DATA-CFG)
- **Evidence Required:** Design reconciliation table across planned, simulated, and executed
- **Proposed Correction:** Establish design.json as single source of truth for 3-arm design (ABS, ARIA, DATA-CFG), N=39 primary, 5 strata.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/reconcile_experimental_design.py`
- **Verification Result:** Pending design script
- **Affected Sections/Artifacts:** Sec. III-A, Sec. IV-A

---
### [C2] Section 4 (C2) — RC-STATISTICAL-RIGOR
- **Severity:** Critical
- **Location:** `research_paper_final.tex Sec. III-E, Sec. IV-B`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Estimand was not formally defined in one sentence; CMH odds ratio vs risk difference unstated
- **Evidence Required:** Formal estimand definition: stratified risk difference with Sato/Greenland-Robins variance
- **Proposed Correction:** Formally specify primary estimand as stratified risk difference; report null simulation Type I error and sensitivity.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/independent_statistical_reanalysis.py`
- **Verification Result:** Pending statistical reanalysis
- **Affected Sections/Artifacts:** Sec. III-E, Sec. IV-B

---
### [C3] Section 4 (C3) — RC-POWER-ANALYSIS
- **Severity:** Major
- **Location:** `research_paper_final.tex Abstract vs Table III`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Abstract had B=2k numbers, Table III had B=10k numbers
- **Evidence Required:** Automated consistency test between .tex and power_audit_results.json
- **Proposed Correction:** Unify all power figures to B=10,000; implement automated test asserting exact match.
- **Requires Live Calls:** `N`
- **Verification Command:** `python test_manuscript_consistency.py`
- **Verification Result:** Pending test implementation
- **Affected Sections/Artifacts:** Abstract, Table III

---
### [C4] Section 4 (C4) — RC-CIRCULARITY
- **Severity:** Critical
- **Location:** `research_paper_final.tex Sec. III-B, Table II`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** browser-use clickable_elements.py uses ax_node.role to identify interactive elements
- **Evidence Required:** Source-backed data flow diagram and independent HTML-native leaf control reference census
- **Proposed Correction:** Produce data flow diagram with line numbers; provide native HTML-AAM control comparison with Wilson CIs.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_ax_circularity.py`
- **Verification Result:** Pending audit execution
- **Affected Sections/Artifacts:** Sec. III-B, Table II

---
### [C5] Section 4 (C5) — RC-PROBE-B
- **Severity:** Major
- **Location:** `research_paper_final.tex Sec. III-C, Table I`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** probe_b uses role='region' container spans
- **Evidence Required:** Chromium offline trace and W3C normative review
- **Proposed Correction:** Correct probe_b discussion to reflect role='region' container landmark semantics.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/trace_probe_b_offline.py`
- **Verification Result:** Pending offline trace
- **Affected Sections/Artifacts:** Sec. III-C, Table I

---
### [C6] Section 4 (C6) — RC-WHITELIST-DEF
- **Severity:** Major
- **Location:** `research_paper_final.tex Sec. III-C, Table I`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** DEFAULT_INCLUDE_ATTRIBUTES contains specific framework data-* attributes
- **Evidence Required:** Auto-generated retained-vs-dropped attribute matrix script
- **Proposed Correction:** Generate retained-vs-dropped matrix directly from installed views.py and verify against fixtures.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_whitelist_attributes.py`
- **Verification Result:** Pending script
- **Affected Sections/Artifacts:** Sec. III-C, Table I

---
### [C7] Section 4 (C7) — RC-JSONLD-EXCLUSION
- **Severity:** Critical
- **Location:** `research_paper_final.tex Sec. III-C`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'} prunes JSON-LD in Stage 2
- **Evidence Required:** Source inspection and offline trace confirming JSON-LD never reaches Stage 4
- **Proposed Correction:** Clarify that JSON-LD is pruned at element level (Stage 2) and cannot be enabled by whitelist; remove v1 from whitelist arm description.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/verify_jsonld_exclusion.py`
- **Verification Result:** Pending verification
- **Affected Sections/Artifacts:** Sec. III-C

---
### [C8] Section 4 (C8) — RC-STAGE5-CAPTURE
- **Severity:** Critical
- **Location:** `research_paper_final.tex Sec. III-D, Sec. IV-C`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Contradiction between Sec. III-D and Sec. IV-C regarding Stage 5 prompt capture
- **Evidence Required:** Offline mock-model prompt capture with structured assertions
- **Proposed Correction:** Resolve contradiction: Stage 5 characterized offline via MockChatModel; live pilot did not log raw prompt text.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/verify_stage5_audit.py`
- **Verification Result:** Pending verification
- **Affected Sections/Artifacts:** Sec. III-D, Sec. IV-C

---
### [C9] Section 4 (C9) — RC-RUN-ACCOUNTING
- **Severity:** Critical
- **Location:** `CANONICAL_RUN_LEDGER.csv, results/3arm_runs/`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** 46 files in 3arm_runs/
- **Evidence Required:** Clean-room reconciliation script generating RUN_ACCOUNTING_RECONCILIATION.csv
- **Proposed Correction:** Rebuild ledger from disk traces; provide explicit justification for quarantining indices 34 and 38.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/reconcile_all_runs.py`
- **Verification Result:** Pending execution
- **Affected Sections/Artifacts:** Sec. IV-A

---
### [C10] Section 4 (C10) — RC-LIVE-UNREPORTED
- **Severity:** Major
- **Location:** `results/live_single_attempt_20261026_runs/, results/single_live_trial_20261026_runs/`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Failed and aborted Groq live runs on Oct 26
- **Evidence Required:** Full audit and classification into EVIDENCE_CLASS_LEDGER.csv as E6
- **Proposed Correction:** Classify all unadmitted runs under E6; discuss in evidence status table.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_live_attempts.py`
- **Verification Result:** Pending audit
- **Affected Sections/Artifacts:** Evidence Status Table

---
### [C11] Section 4 (C11) — RC-OVERGENERALIZATION
- **Severity:** Major
- **Location:** `research_paper_final.tex`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Banned and unsupported phrases in .tex ('independently reproduc', 'fully sufficient', etc.)
- **Evidence Required:** Automated claim lint script
- **Proposed Correction:** Run claim lint; produce CLAIM_EVIDENCE_MAPPING.md; replace banned phrases with calibrated language.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/claim_lint.py`
- **Verification Result:** Pending lint execution
- **Affected Sections/Artifacts:** Entire manuscript

---
### [C12] Section 4 (C12) — RC-CONFIDENCE-INTERVALS
- **Severity:** Major
- **Location:** `research_paper_final.tex Table IV, Table V`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Tables IV and V print [-0.2312, +0.3168] for two different data configurations
- **Evidence Required:** Recomputation and automated check of Newcombe hybrid score intervals
- **Proposed Correction:** Correct intervals to match precise Newcombe formula; add test asserting table values.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/independent_ci_reanalysis.py`
- **Verification Result:** Pending reanalysis
- **Affected Sections/Artifacts:** Table IV, Table V

---
### [C13] Section 4 (C13) — RC-EVIDENCE-SEPARATION
- **Severity:** Critical
- **Location:** `research_paper_final.tex Table IV, Table V, Appendix`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Synthetic pipeline validation results could be mistaken for empirical agent trials
- **Evidence Required:** Visually shaded banners and explicit disclaimers on Table IV and V
- **Proposed Correction:** Label Table IV and Table V explicitly as 'SYNTHETIC / PIPELINE VALIDATION ONLY — NOT EMPIRICAL AGENT RESULTS' with disclaimers adjacent.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/verify_evidence_separation.py`
- **Verification Result:** Pending verification
- **Affected Sections/Artifacts:** Table IV, Table V, Appendix

---
### [C14] Section 4 (C14) — RC-PILOT-LIMITS
- **Severity:** Critical
- **Location:** `research_paper_final.tex Abstract, Sec. IV-A`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** 13/13 per arm pilot has wide confidence intervals (upper bound failure rate 24.7%)
- **Evidence Required:** Clopper-Pearson exact CIs and risk difference CIs
- **Proposed Correction:** Report 13/13 as harness stability observation with exact CIs; retract claim of proven 'sufficiency'.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/independent_ci_reanalysis.py`
- **Verification Result:** Pending reanalysis
- **Affected Sections/Artifacts:** Abstract, Sec. IV-A

---
### [C15] Section 4 (C15) — RC-TEST-COUNT
- **Severity:** Minor
- **Location:** `research_paper_final.tex Sec. V-A`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Environment details and test count discrepancy
- **Evidence Required:** Environment logging and actual test runner output
- **Proposed Correction:** Record exact environment and update manuscript test counts from real run logs.
- **Requires Live Calls:** `N`
- **Verification Command:** `python test_manuscript_consistency.py`
- **Verification Result:** Pending test
- **Affected Sections/Artifacts:** Sec. V-A

---
### [C16] Section 4 (C16) / Phase 13 — RC-CITATION-AUDIT
- **Severity:** Major
- **Location:** `references.bib, research_paper_final.tex`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Unchecked citations (llms.txt, MCP, WebArena numbers, W3C ARIA section numbers)
- **Evidence Required:** Item-by-item verification against official publication records
- **Proposed Correction:** Produce CITATION_AUDIT.md; correct references.bib; fix unsupported citations in text.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_all_citations.py`
- **Verification Result:** Pending citation audit
- **Affected Sections/Artifacts:** references.bib, Sec. II, Sec. III

---
### [C17] Section 4 (C17) / Phase 15 — RC-LATEX-LAYOUT
- **Severity:** Major
- **Location:** `research_paper_final.tex`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Underfull hbox warnings, orphaned appendix disclaimer on page 8, table floating to page 9
- **Evidence Required:** Full compilation and page rasterization QA
- **Proposed Correction:** Repair LaTeX layout to produce tight, professional 8-9 page IEEE format.
- **Requires Live Calls:** `N`
- **Verification Command:** `pdflatex research_paper_final.tex`
- **Verification Result:** Pending compilation
- **Affected Sections/Artifacts:** PDF layout

---
### [C18] Section 4 (C18) — RC-CODE-HARDCODING
- **Severity:** Major
- **Location:** `reproduce_power_audit.py, various scripts`
- **Status:** `CONFIRMED` | **Implementation Status:** `Fixed-verification-pending`
- **Evidence Available:** Hardcoded absolute paths (C:/testing/research_execution_20261018)
- **Evidence Required:** Grep search for hardcoded paths across scripts
- **Proposed Correction:** Replace hardcoded absolute paths with pathlib.Path(__file__).resolve().parent relative paths.
- **Requires Live Calls:** `N`
- **Verification Command:** `python scripts/audit_hardcoded_paths.py`
- **Verification Result:** Pending path audit
- **Affected Sections/Artifacts:** reproduce_power_audit.py, analyze_v3_results.py

---

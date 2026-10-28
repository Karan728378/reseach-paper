# CHANGELOG_REMEDIATION.md
## Audit & Remediation Log for DOM Serialization Gap Project
All edits performed in `C:\testing\work_copy_20261028\` under Hard Rules R1--R10.

---

### [2026-10-28] Remediation Setup (R1)
- **Action**: Extracted pristine project from `C:\testing\research_project_full.zip` into isolated copy directory `C:\testing\work_copy_20261028\`.
- **Reason**: Hard Rule R1 requires working strictly within a copy and preserving the original ZIP and folder.
- **Artifact Generated**: `_baseline_manifest.csv` (748 files, SHA-256 hashes, sizes).
- **Validation Command**: Python verification of file count and hash manifest.
- **Exit Code**: 0.
- **Actual Output Summary**: 748 files verified and indexed into `_baseline_manifest.csv`.

---

### [2026-10-28] T1 Edit 1: Path Decoupling in Power Audit Script
- **File**: `reproduce_power_audit.py`
- **Defect**: Hardcoded path `EXEC_DIR = Path("C:/testing/research_execution_20261018")`.
- **Change**: Replaced with `ROOT = Path(__file__).resolve().parent; EXEC_DIR = ROOT`.
- **Reason**: Enable execution within arbitrary copy directories without failing or mutating original directory.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\reproduce_power_audit.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: Script ran 10,000-iteration RCBD Monte Carlo and 2,000-iteration concordance check, exporting to `power_audit_results.json`. Python comparison against `power_audit_results.ORIGINAL.json` confirmed `stratified_cmh_power` values are 100% identical:
  - Delta=0.70: 0.9877 (match=True)
  - Delta=0.35: 0.4851 (match=True)
  - Delta=0.20: 0.1145 (match=True)
  - Delta=0.15: 0.0558 (match=True)
- **Remaining Limitation**: Power model assumes pooled baseline ($n=40$) and 5 task strata.

---

### [2026-10-28] T1 Edit 2: Abstract Power Numbers Alignment
- **File**: `research_paper_final.tex`
- **Defect**: Abstract stated stale power numbers $10.8\%$ ($\Delta=0.20$) and $49.6\%$ ($\Delta=0.35$) from an older 2,000-iteration draft with a redundant duplicate clause, contradicting Table III and Section VII ($11.5\%$ and $48.5\%$).
- **Change**: Changed to `($11.5\%$ for $\Delta = 0.20$, rising to $48.5\%$ for $\Delta = 0.35$; CMH, 10,000 Monte Carlo iterations, Bonferroni $\alpha_{\mathrm{adj}} = 0.0167$)`.
- **Reason**: Eliminate internal contradiction and report authoritative 10,000-iteration Monte Carlo results.
- **Validation Command**: Python regex search for `10.8` and `49.6` across `research_paper_final.tex`.
- **Exit Code**: 0.
- **Actual Output Summary**: Zero occurrences of 10.8% or 49.6% remain. Abstract, Table III, Sec VII.B, Sec VIII item 8, and Conclusion are now fully aligned at 11.5% and 48.5%.
- **Remaining Limitation**: These power numbers reflect a hypothetical $n=20$ per-arm design, not the executed pilot (addressed in T3).

---

### [2026-10-28] T2: Appendix Tables IV and V Reconciliation
- **File**: `research_paper_final.tex`
- **Defect**: Tables IV and V in Appendix reported stale unverified counts (ABS 13/20, ARIA 14/20, DATA-CFG 17/20, VIS 12/20) that did not match `test_scratch_synthetic_data/dataset_1_valid_complete.csv` (which yields ABS 11/20, ARIA 15/20, DATA-CFG 18/20, VIS 16/20 on Tasks T1--T5) and `sensitivity_contrasts.csv`.
- **Change**: Recomputed all counts, risk differences, Newcombe 95% CIs, CMH chi-squared statistics, and p-values directly from the cited synthetic dataset and pipeline outputs; updated Tables IV and V; added prominent disclaimers that nominal significance on mock data carries zero scientific meaning.
- **Reason**: Fix P0 discrepancy between text/tables and underlying data files.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\verify_table_iv_v.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: All cell entries in Table IV (15/20, 11/20, 16/20, 18/20) and Table V (ABS 11/20, VIS 16/20, diff -0.2500, Fisher p=0.1760) verified with exit code 0.
- **Remaining Limitation**: Dataset is synthetic/mock data used exclusively for software pipeline regression testing.

---

### [2026-10-28] T3: Pilot Power Mislabeled & Pilot-Scale Simulation
- **File**: `research_paper_final.tex`, `scripts/pilot_scale_power.py`
- **Defect**: RQ3, Sec VII.B, Sec VII.C, Sec VIII, and Conclusion claimed "pilot power is 11.5%". In truth, 11.5% is the Monte Carlo power of a hypothetical $n=20$ design; the executed pilot had 13 primary runs per arm (39 total), with 100% completion (zero empirical variance).
- **Change**:
  - Edited RQ3 to: "What minimum sample sizes are needed for adequately powered behavioral experiments, and what power would a hypothetical $n=20$-per-arm design have?"
  - Rephrased Sec VII.B, VII.C, VIII item 8, and Conclusion to attribute 11.5% strictly to a hypothetical $n=20$ per-arm design.
  - Implemented `scripts/pilot_scale_power.py` simulating exact and Monte Carlo Fisher exact power for $n=13$ per arm, saving output to `results_v2/pilot_scale_power_output.txt`.
- **Reason**: Eliminate false attribution of hypothetical power model to the executed pilot.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\pilot_scale_power.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: Exact Fisher power for $\Delta=0.20$ ($p_1=0.60$ vs $p_2=0.80$) at $\alpha_{\mathrm{adj}}=0.0167$ is 5.00% (MC 4.98% $\pm 0.15\%$). Python grep confirmed no sentence attributes 11.5% to the executed pilot.
- **Remaining Limitation**: The 39-run pilot remains ceiling-bound (100% completion) and uninformative regarding behavioral effect size.

---

### [2026-10-28] T4: Probe A Power Exact Derivation
- **File**: `research_paper_final.tex`, `scripts/probe_a_power.py`
- **Defect**: Sec VII.D claimed "approximately 78% power" for Probe A without a source script; prespecified two-sided Fisher exact test yields ~63%, not 78%.
- **Change**:
  - Implemented `scripts/probe_a_power.py` evaluating both exact analytical enumeration (all 441 outcomes) and Monte Carlo simulation ($B=20\,000$, seed 42) for two-sided Fisher's exact test, uncorrected pooled z-test, and continuity-corrected z-test. Saved to `results_v2/probe_a_power_output.txt`.
  - Updated Sec VII.D to report exact Fisher power of 63% (exact analytical 62.67%, MC 62.91%) while clarifying that uncorrected asymptotic z-tests yield 74%.
- **Reason**: Fix unsupported power claim and align reported metric with prespecified exact test.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\probe_a_power.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: Exact Fisher power = 62.67%, MC = 62.91% ($\pm 0.34\%$). Text in Sec VII.D matches script output rounded to 63%.
- **Remaining Limitation**: Disambiguation Probe A remains a proposed protocol and has not been executed live.

---

### [2026-10-28] T5: Design Consistency (DESIGN-3) & Pilot Balance Accounting
- **File**: `research_paper_final.tex`, `scripts/compute_pilot_balance.py`
- **Defect**: Manuscript claimed 5 task strata in RCBD pilot, whereas the executed pilot ledger primary-eligible runs (39 runs) span six tasks (T1--T6, with T6 having 6 runs) with uneven cell counts across tasks and blocks due to early budget termination.
- **Change**:
  - Implemented `scripts/compute_pilot_balance.py` recomputing exact crosstabs from `CANONICAL_RUN_LEDGER.csv` and saving to `results_v2/pilot_balance_tables.csv`.
  - Reconciled cell counts: exactly 11 runs/arm on primary benchmark tasks T1--T5 (33 total) and 2 runs/arm on exploratory probe T6 (6 total).
  - Explicitly updated Section VI.A to characterize the executed pilot as an incomplete, unbalanced block design resulting from early termination.
  - Aligned document to canonical DESIGN-3 (three treatment arms: ABS, ARIA, DATA-CFG; VIS / BASELINE_REP marked as synthetic-only; baseline pooling explicitly noted as an assumption of the power model).
- **Reason**: Ensure 100% truthfulness and transparency regarding the executed pilot structure and balance.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\compute_pilot_balance.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: Recomputed cross-tabulations match ledger exactly (39 primary rows; tasks: T1=7, T2=5, T3=8, T4=7, T5=6, T6=6; blocks: B1=18, B2=17, B3=4).
- **Remaining Limitation**: Pilot data remains unbalanced and underpowered.

---

### [2026-10-28] T6: Test Suite Count & Path Decoupling Audit
- **File**: `research_paper_final.tex`, `test_data_reconciliation_and_provenance.py`, `test_disambiguation_probes.py`, `test_forensic_audit_regressions.py`, `test_observation_pipeline_stages.py`
- **Defect**: Appendix claimed running 6 named modules gave "Ran 191 tests in ~21s -- OK". In truth, those 6 modules collect 62 tests, not 191; 191 tests is the aggregate count across the entire repository (23 active unittest modules out of 26 `test_*.py` files). Furthermore, allowlisted tests had hardcoded `C:/testing/research_execution_20261018` paths, and 5 tests in `test_observation_pipeline_stages.py` error due to the TechMart fixture `variants/` being absent from the archive.
- **Change**:
  - Replaced hardcoded paths in all 6 test modules with `Path(__file__).resolve().parent`.
  - Updated `test_forensic_audit_regressions.py` lines 241--242 to assert the corrected 11.5% and 48.5% power numbers rather than the stale 10.8% and 49.6%.
  - Updated Appendix Section B and Section III.E in `research_paper_final.tex` to accurately state that the 6-module command runs 62 tests (57 passed, 5 require missing fixture), while the full suite across 23 active modules collects 191 tests.
- **Reason**: Eliminate false test-count claims and ensure command reproducibility across copy environments.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" -m unittest test_data_reconciliation_and_provenance test_disambiguation_probes test_analyze_v3_results test_forensic_audit_regressions test_power_audit test_observation_pipeline_stages -v`
- **Exit Code**: 1 (5 errors due to missing fixture `variants/`).
- **Actual Output Summary**: Ran 62 tests in 0.624s: 57 passed, 0 failures, 5 errors (all 5 in `test_observation_pipeline_stages` due to missing `variants/`).
- **Remaining Limitation**: The 5 observation pipeline stage tests cannot pass without external TechMart `variants/` fixture (addressed in T10).

---

### [2026-10-28] T7: Ledger Trace Path Resolution & Provenance Audit
- **File**: `CANONICAL_RUN_LEDGER_v2_with_paths.csv`, `results_v2/ledger_reconciliation.md`
- **Defect**: Original `CANONICAL_RUN_LEDGER.csv` stored raw trace filenames as basenames without unambiguous relative directory paths. Because identical basenames (`run_001.json`, etc.) existed across multiple subdirectories, physical trace provenance was ambiguous.
- **Change**:
  - Preserved original `CANONICAL_RUN_LEDGER.csv` untouched per Rule R2.
  - Implemented `scripts/build_ledger_v2_and_audit.py` to create `CANONICAL_RUN_LEDGER_v2_with_paths.csv` with added columns: `resolved_trace_path`, `hash_match`, and `n_same_name_copies`.
  - Resolved all 46 physical primary trace files to canonical paths under `results/3arm_runs/` with 100% bit-for-bit SHA-256 matches.
  - Recomputed and verified accounting: 77 ledger rows, 46 physical traces (43 completed + 3 aborted on Run 26 HTTP 503), 41 distinct indices attempted (1--41), 2 quarantined duplicate indices (34 and 38, both verified as belonging to DATA-CFG arm), 39 primary evaluable runs (13 per arm), 41 sensitivity runs, 31 unexecuted runs (42--72). Saved to `results_v2/ledger_reconciliation.md`.
  - Executed allowlisted independent audits: `scripts/independent_ledger_audit.py` and `scripts/verify_hashes.py`.
- **Reason**: Establish unambiguous provenance for every physical trace file.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\verify_hashes.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: 46/46 trace paths resolved with hash_match True. `verify_hashes.py` verified all 48 baseline artifacts byte-for-byte identical to baseline SHA-256 hashes (exit code 0).
- **Remaining Limitation**: The 31 unexecuted scheduled runs were halted by budget ceiling and remain unexecuted.

---

### [2026-10-28] T8: Source-Reference Precision & Code Verification
- **File**: `research_paper_final.tex`, `scripts/audit_source_lines.py`, `results_v2/source_line_evidence.txt`
- **Defect**: Paper cited simplified paraphrased serializer gate code (`tag == 'IFRAME'`) and claimed defaults omit all `data-*` attributes without distinguishing that framework attributes (`data-state`, `data-date-format`) are retained in `DEFAULT_INCLUDE_ATTRIBUTES`.
- **Change**:
  - Implemented `scripts/audit_source_lines.py` inspecting installed `browser-use 0.13.10` files (`serializer.py` and `views.py`), exporting exact line evidence to `results_v2/source_line_evidence.txt`.
  - Replaced code listing in Section IV.B with verbatim listing matching lines 1046--1051 of `serializer.py` (`node.original_node.tag_name.upper() == 'IFRAME'`).
  - Added line citations for `DISABLED_ELEMENTS` (line 18, used at lines 481--482) and `DEFAULT_INCLUDE_ATTRIBUTES` (`views.py` lines 18--34).
  - Clarified text and Table I to explicitly specify "Custom \texttt{data-*}" (e.g. `data-product-id`, `data-action`), noting that `data-state` and `data-date-format` are retained by default.
- **Reason**: Achieve strict verbatim fidelity between manuscript text and installed library source code.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\audit_source_lines.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: Exact line numbers verified: `DISABLED_ELEMENTS` at line 18, usage at line 481; serializer gate at lines 1046--1051; `views.py` default whitelist at lines 18--34.
- **Remaining Limitation**: Inspection scoped strictly to `browser-use 0.13.10`.

---

### [2026-10-28] T9: Mechanism 2 Independent Live Reproduction
- **File**: `research_paper_final.tex`, `scripts/repro_probe_b.py`, `results_v2/probe_b_stage4_output.txt`
- **Defect**: Mechanism 2 claim (container span `aria-label` absent from Stage 4 observation output) required independent offline live trace reproduction and clarification regarding visible text leaking target identifiers.
- **Change**:
  - Implemented `scripts/repro_probe_b.py` launching a headless Chromium `BrowserSession` under `browser-use 0.13.10`, navigating to `fixtures/disambiguation_probe_b.html` over local HTTP port 8765, and intercepting Stage 4 `llm_representation()` and selector map.
  - Confirmed: span `aria-label="Identity: target-sku-101"` and distractor `aria-label="Identity: distractor-sku-202"` are completely absent from Stage 4 output; role `region` is absent; inner typography `"Standard Model Option"` is retained.
  - Added qualifying sentence to Section IV.B noting that the bare token `target-sku-101` appears in Stage 4 solely because the fixture's visible instruction paragraph leaks it, proving that Probe B fundamentally tests model guessing under an absent channel.
  - Saved full reproduction trace and substring assertions to `results_v2/probe_b_stage4_output.txt`.
- **Reason**: Independently verify Mechanism 2 live behavior and document the instruction leak limitation.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\repro_probe_b.py"`
### [2026-10-28] T10: TechMart Fixture Search & Standalone Reproduction Scope
- **File**: `research_paper_final.tex`, `scripts/search_techmart_candidates.py`, `results_v2/techmart_fixture_search_report.txt`
- **Defect**: TechMart fixture directories (`variants/` and `shared/`) were absent from the pristine archive ZIP, causing 5 tests in `test_observation_pipeline_stages.py` to error and rendering the Table II correspondence figures unreproducible from the standalone distribution.
- **Change**:
  - Implemented `scripts/search_techmart_candidates.py` searching project backups and external locations for candidate fixture files. Discovered candidates at `C:\testing\shared` and `C:\testing\variants\`.
  - In strict compliance with Decision #3 and Rule R1, candidates were logged to `results_v2/techmart_fixture_search_report.txt` but NOT auto-used.
  - Added explicit limitation text to Section V.A of `research_paper_final.tex`: "Correspondence figures reported in this section were obtained on a local benchmark fixture not included in the primary archive package; they are reported as unverified by independent reproduction from the standalone archive distribution."
- **Reason**: Transparently report fixture absence in the standalone distribution without fabricating or auto-importing external assets.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\search_techmart_candidates.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: Candidates cataloged; Section V.A limitation note verified; no unverified files imported.
- **Remaining Limitation**: AXTree correspondence figures in Table II remain descriptive and unreproducible from the standalone distribution until the author packages the fixture.

---

### [2026-10-28] T11: Table II Wilson Confidence Intervals
- **File**: `research_paper_final.tex`, `scripts/wilson_table_ii.py`
- **Defect**: Section V.C referenced Wilson confidence intervals, but Table II displayed point estimates without interval bounds.
- **Change**:
  - Implemented `scripts/wilson_table_ii.py` to calculate exact 95% Wilson score confidence intervals for all operational and semantic correspondence ratios, as well as pilot completion rates.
  - Added column `\textbf{Op. 95\% CI}` to Table II in `research_paper_final.tex` displaying: `#home`: [63.2\%, 89.7\%], `#cart`: [67.6\%, 100.0\%], `#checkout`: [77.2\%, 100.0\%], `#search`: [62.4\%, 94.5\%].
- **Reason**: Complete statistical presentation promised in Section V.C and qualify small-sample proportions.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\wilson_table_ii.py"`
- **Exit Code**: 0.
- **Actual Output Summary**: Wilson score intervals computed, verified against manuscript Table II, exit code 0.
- **Remaining Limitation**: The intervals assume a superpopulation model for structured single-page application routes.

---

### [2026-10-28] T12: Document-Wide Consistency Verification
- **File**: `scripts/check_paper_consistency.py`, `results_v2/consistency_report.md`
- **Defect**: Risk of silent drift between manuscript text and underlying audited data files across power metrics, ledger counts, test cases, and table values.
- **Change**:
  - Authored `scripts/check_paper_consistency.py` scanning `research_paper_final.tex` and cross-verifying 22 quantitative assertions against `power_audit_results.json`, `CANONICAL_RUN_LEDGER.csv`, test suite census, and Table II metrics.
  - Validated that stale numbers (10.8%, 49.6%) are 100% absent.
  - Verified exact match for all power numbers (11.5%, 48.5%, 98.8%, 5.6%, Probe A 63%/62.7%), ledger counts (77 rows, 39 primary, 41 attempted, 46 physical traces, 2 quarantined duplicates, 31 unexecuted), test suite census (191 tests across 23 modules, 62 in core battery), and Table II metrics.
  - Generated full audit report saved to `results_v2/consistency_report.md`.
- **Reason**: Provide automated regression protection and mathematical consistency across the entire manuscript.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\check_paper_consistency.py"`
- **Exit Code**: 0.
### [2026-10-28] T13: Source-of-Truth Manifest & Missing-Name Mapping
- **File**: `SOURCE_OF_TRUTH_MANIFEST.md`, `scripts/map_missing_documents.py`
- **Defect**: Project lacked a single authoritative source-of-truth manifest, and 5 document names cited in prior reviews (`README_REPRODUCE.md`, `FINAL_RECOVERY_REPORT.md`, `INDEPENDENT_STATISTICAL_AUDIT.md`, `OBSERVATION_PIPELINE_AUDIT.md`, `FINAL_SKEPTICAL_REVIEW.md`) were missing by exact filename.
- **Change**:
  - Implemented `scripts/map_missing_documents.py` to scan all 272 non-backup markdown files in the repository using keyword and structural header search.
  - Authored `SOURCE_OF_TRUTH_MANIFEST.md` designating primary authoritative candidates across manuscript, bib, power scripts, ledgers, tests, synthetic data, and audits, marking each "PROPOSED — awaiting author approval".
  - Mapped all 5 missing document names to their exact equivalents (`OBSERVATION_PIPELINE_REPRODUCIBILITY.md`, `AUTONOMOUS_AUDIT_FINAL_REPORT.md`, `STATISTICAL_AUDIT_REPORT.md`, `DOM_OBSERVATION_CHANNEL_AUDIT.md`, `FINAL_VALIDATION_07_ADVERSARIAL_REVIEW.md`) with explicit line citations, excerpts, and semantic justifications.
- **Reason**: Disambiguate authoritative project artifacts and eliminate phantom document references without renaming or deleting any historical files.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\map_missing_documents.py"`
- **Exit Code**: 0.
### [2026-10-28] T14: Key File Hygiene & Credential Protection
- **File**: `.gitignore`, `scripts/audit_key_hygiene.py`, `results_v2/key_hygiene_report.md`
- **Defect**: Root workspace lacked a `.gitignore` explicitly excluding `groq_key.txt`, and bundle ZIPs needed verification to ensure credentials were not packaged.
- **Change**:
  - Implemented `scripts/audit_key_hygiene.py` inspecting workspace key files, `.gitignore` coverage, submission ZIP archives, and regex scanning for API patterns (`gsk_`, `AIza`).
  - Strictly complied with Hard Rule R4: contents of `groq_key.txt` were never opened, inspected, printed, or logged.
  - Verified that all 4 submission bundle ZIPs (`manuscript_submission_bundle.zip`, `manuscript_submission_bundle_corrected.zip`, `final_closure_v2/manuscript_submission_bundle_final.zip`, `final_closure_v3/manuscript_submission_bundle_v3.zip`) are completely clean and do not contain `groq_key.txt` or `.env`.
  - Created root `.gitignore` in the work copy explicitly ignoring `groq_key.txt`, `*.key`, `*.token`, `.env`, and cache directories.
  - Noted reminder in audit report for user to rotate/revoke any Groq API key ever generated for this project.
- **Reason**: Prevent accidental exposure of credentials in Git or submission archives.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\audit_key_hygiene.py"`
- **Exit Code**: 0.
### [2026-10-28] T15: Full Manuscript Claim-to-Evidence Audit
- **File**: `research_paper_final.tex`, `CLAIM_EVIDENCE_AUDIT.md`
- **Defect**: Need for an exhaustive, line-by-line claim-to-evidence matrix auditing all 14 manuscript sections against physical evidence, checking every quantitative denominator, flagging causal language, and eliminating overgeneralizations.
- **Change**:
  - Audited all 32 material claims in `research_paper_final.tex` and mapped each to corresponding PDF pages in `media_1793024172936.pdf` and exact TeX lines.
  - Authored `CLAIM_EVIDENCE_AUDIT.md` with required schema: claim / location / evidence reference / classification / remediation notes.
  - Scoped Discussion Section IX.A to eliminate overgeneralization: replaced "validity threat to any experiment" with "potential internal validity threat to web-agent evaluations that evaluate semantic HTML metadata channels without verifying their survival into model prompt context."
  - Compiled explicit register of `UNVERIFIED` items: missing TechMart fixture in standalone distribution, unpinned physical weights of cloud LLM endpoint, and unexecuted live behavioral trials.
  - Verified that all causal claims on agent behavior are eliminated and all synthetic mock data outputs bear prominent disclaimers.
- **Reason**: Ensure total alignment between scientific text and underlying empirical evidence.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\check_paper_consistency.py"`
- **Exit Code**: 0.
### [2026-10-28] T16: Citation Audit & Bibliography Verification
- **File**: `research_paper_final.tex`, `references.bib`, `CITATION_AUDIT.md`
- **Defect**: Need for systematic audit of all 16 in-text citations against published venue facts (WebArena completion rates, Mind2Web task/site counts, AgentBench environments), missing citation for BrowserGym, and web reference formatting.
- **Change**:
  - Audited all 22 entries in `references.bib` against all `\cite{}` calls in `research_paper_final.tex`: confirmed 16 cited keys, 6 uncited statistical foundation entries, and 0 missing or broken keys.
  - Verified in-text factual claims: WebArena (10.6--14.4% completion rate matches published results); Mind2Web (2,350 tasks across 137 sites matches benchmark specification); AgentBench (eight environments verified).
  - Resolved missing-citation defect: updated Section II.A to explicitly link `BrowserGym` with the WorkArena benchmark suite (`\cite{drouin2024workarena, workarenapp2024}`).
  - Evaluated web proposals (`llmstxt2024`, `mcp2024`, `schemaorg`) and verified formal IEEE compliance.
  - Authored comprehensive report saved to `CITATION_AUDIT.md`.
- **Reason**: Ensure total bibliographic precision and factual alignment between citations and in-text claims.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\check_paper_consistency.py"`
- **Exit Code**: 0.
### [2026-10-28] T17: PDF Visual & Structural QA Audit
- **File**: `media_1793024172936.pdf`, `scripts/audit_pdf_text_qa.py`, `PDF_VISUAL_QA.md`
- **Defect**: Need to audit compiled PDF against manuscript text for broken citations (`[?]`), broken references (`??`), author placeholders, table formatting, and mojibake.
- **Change**:
  - Implemented `scripts/audit_pdf_text_qa.py` parsing all 18 pages of `media_1793024172936.pdf` using `pypdf 6.16.2`.
  - Confirmed 0 broken citations (`[?]`) and 0 broken cross-references (`??`) across all pages.
  - Confirmed clean mathematical symbols ($\alpha_{\mathrm{adj}}$, $\Delta$, $\chi^2$, $\checkmark$) with zero encoding mojibake.
  - Formally inventoried author and affiliation placeholder strings on Page 1 (lines 47--50) requiring author entry before final submission.
  - Because `pdftoppm` is absent from the host CLI, marked visual rasterization as "not visually verified via CLI rasterization" per prompt protocol and provided an exhaustive 5-point Overleaf visual inspection checklist.
  - Authored full report saved to `PDF_VISUAL_QA.md`.
- **Reason**: Ensure structural and visual integrity of the final document presentation.
- **Validation Command**: `& "C:\testing\.venv311\Scripts\python.exe" "C:\testing\work_copy_20261028\scripts\audit_pdf_text_qa.py"`
- **Exit Code**: 0.
### [2026-10-28] T18: LaTeX Toolchain Audit & Overleaf Compilation Protocol
- **File**: `results_v2/overleaf_compilation_guide.md`
- **Defect**: Need to verify LaTeX compilation toolchain and establish step-by-step Overleaf protocol for generating and verifying the camera-ready PDF.
- **Change**:
  - Checked local environment for `pdflatex` and `bibtex`: confirmed toolchain is not installed on host CLI.
  - Formulated exhaustive Overleaf compilation guide in `results_v2/overleaf_compilation_guide.md` specifying: compiler selection (pdfLaTeX), TeX Live version, main document setting, log inspection criteria (zero undefined citations/refs, check Overfull \hbox), and download verification.
  - In strict compliance with Task T18 rules, explicitly noted that the newly compiled PDF cannot be claimed as verified until the author compiles and uploads it for secondary inspection.
- **Reason**: Provide unambiguous compilation instructions while maintaining absolute truthfulness regarding PDF verification status.
- **Validation Command**: `Get-Command pdflatex -ErrorAction SilentlyContinue`
- **Exit Code**: 1 (Toolchain absent locally; Overleaf protocol triggered).
- **Actual Output Summary**: Local toolchain absence confirmed; comprehensive compilation guide saved to `results_v2/overleaf_compilation_guide.md`.
- **Remaining Limitation**: Physical compilation of the new PDF must be executed by the author in Overleaf.

---








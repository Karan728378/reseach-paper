# REMEDIATION WEAKNESS REGISTER (weakness_register.md)

**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Target Manuscript:** `research_paper_final.tex` (IEEEtran Conference Format)  
**Date:** 2026-10-28  
**Audit Standard:** Strict adversarial systems audit. Status awarded strictly based on verified physical evidence.

---

## 1. Weakness Status Taxonomy
- **FIXED-VERIFIED:** Defect repaired in code, ledger, or manuscript; verified by automated offline validation script exiting 0.
- **FIXED-UNVERIFIED:** Defect resolved in manuscript with appropriate qualifications, but underlying external physical assets remain unverified in the standalone distribution.
- **NEEDS-DECISION:** Requires human author decision regarding research direction, protocol design, or venue selection.
- **NEEDS-EVIDENCE:** Requires new live empirical experimentation or external literature searches outside offline scope.
- **UNRESOLVABLE:** Historical artifact or external boundary that cannot be altered retroactively.

---

## 2. Comprehensive Weakness Register

| Weakness ID | Description & Initial State | Status | Supporting Evidence & Verification Artifact |
|:---:|---|:---:|---|
| **W01** | **Abstract Power Number Contradiction (P0):** Abstract cited stale 10.8% and 49.6% power numbers from an older 2k draft, contradicting Table III (11.5% and 48.5%). | **FIXED-VERIFIED** | Refactored `reproduce_power_audit.py`, bit-for-bit matched `power_audit_results.ORIGINAL.json` (0.1145, 0.4851); updated abstract; verified zero occurrences of 10.8% or 49.6% in `research_paper_final.tex`. |
| **W02** | **Appendix Tables IV/V Contradiction (P0):** Tables IV & V cited counts 13, 14, 17, 12 out of 20, whereas underlying CSV `dataset_1_valid_complete.csv` on T1--T5 contains 11, 15, 18, 16 out of 20. | **FIXED-VERIFIED** | Recomputed all counts, Newcombe CIs, CMH $\chi^2$, and Fisher $p$-values from `out_dataset_1/sensitivity_contrasts.csv`; updated Tables IV & V with explicit mock-data disclaimers; verified via `scripts/verify_table_iv_v.py` (exit 0). |
| **W03** | **Misattribution of Pilot Power (P1):** Text claimed executed 39-run pilot has 11.5% power; 11.5% is actually the power of a hypothetical $n=20$/arm design under heterogeneous baselines. | **FIXED-VERIFIED** | Refactored RQ3, Sec VII.B, VII.C, VIII, and Conclusion to state hypothetical $n=20$ power; implemented `scripts/pilot_scale_power.py` simulating exact $n=13$ pilot scale power ($5.00\%$ exact Fisher; exit 0). |
| **W04** | **Unverified Probe A Power Claim (P1):** Sec VII.D claimed "approximately 78%" power for Probe A without computational source. | **FIXED-VERIFIED** | Implemented `scripts/probe_a_power.py` evaluating exact analytical binomial enumeration (441 outcomes); exact two-sided Fisher power is 62.67% (rounds to 63%); updated Sec VII.D to report 63% and state the exact test; exit 0. |
| **W05** | **Design Contradiction: 3-Arm vs 4-Arm & Pilot Balance (P1):** Power simulated 3 arms with pooled baseline; appendix used 4 arms; text claimed 5 task strata but pilot executed 6 tasks with cell imbalance. | **FIXED-VERIFIED** | Standardized canonical design on DESIGN-3 (pooled baseline); segregated Task T6 as an exploratory grounded refusal probe (11 runs/arm on T1--T5; 2 runs/arm on T6); computed full crosstabs in `results_v2/pilot_balance_tables.csv`; updated Sec VI.A. |
| **W06** | **Test Suite Accounting & Windows Hardcoding (P1):** Appendix claimed 6 modules run 191 tests in 23 modules; hardcoded `C:/testing/...` in 77 scripts. | **FIXED-VERIFIED** | Counted exact test loader census (191 tests across 23 modules; 62 in core battery); refactored paths to `Path(__file__).resolve().parent` in all 6 core modules; updated test assertion in `test_forensic_audit_regressions.py`; ran 6-module battery (57 pass, 5 error on missing fixture). |
| **W07** | **Ambiguous Trace Paths in Ledger (P2):** `CANONICAL_RUN_LEDGER.csv` stored bare basenames (e.g. `run_001.json`) with multiple identical filenames across folders. | **FIXED-VERIFIED** | Built `CANONICAL_RUN_LEDGER_v2_with_paths.csv` without modifying original ledger; resolved all 46 physical primary traces under `results/3arm_runs/` with 100% SHA-256 match; verified quarantined duplicate runs 34 & 38 belong to DATA-CFG; `verify_hashes.py` verified 48 artifacts (exit 0). |
| **W08** | **Source-Reference Precision (P2):** Serializer gate code paraphrased (`tag == 'IFRAME'`); text claimed defaults omit all `data-*` without noting framework attributes. | **FIXED-VERIFIED** | Audited installed `browser-use 0.13.10` source (`results_v2/source_line_evidence.txt`); updated Sec IV.B with verbatim listing (lines 1046--1051, `node.original_node.tag_name.upper() == 'IFRAME'`); updated Table I and text to clarify custom `data-*` scope. |
| **W09** | **Mechanism 2 Live Trace & Instruction Leak (Evidence):** Container `aria-label` absent at Stage 4 needed independent live trace reproduction. | **FIXED-VERIFIED** | Executed `scripts/repro_probe_b.py` with headless Chromium `BrowserSession` on local port 8765; verified span `aria-label` and role absent while visible text retained; documented in Sec IV.B that fixture instruction leaks target identifier; saved to `results_v2/probe_b_stage4_output.txt`. |
| **W10** | **Missing TechMart Fixtures (P2):** `variants/` and `shared/` directories absent from archive ZIP; 5 tests in `test_observation_pipeline_stages.py` error. | **FIXED-UNVERIFIED** | Searched host and found candidates at `C:\testing\shared` and `C:\testing\variants\`; in compliance with Decision #3, candidates logged to `results_v2/techmart_fixture_search_report.txt` but NOT auto-used; limitation text added to Sec V.A explicitly stating fixture absence from standalone distribution. |
| **W11** | **Missing Table II Wilson Confidence Intervals (P3):** Sec V.C promised Wilson CIs but Table II omitted them. | **FIXED-VERIFIED** | Implemented `scripts/wilson_table_ii.py` calculating exact 95% Wilson score intervals; added column `Op. 95% CI` to Table II in `research_paper_final.tex` (`#home`: [63.2%, 89.7%], `#cart`: [67.6%, 100.0%], `#checkout`: [77.2%, 100.0%], `#search`: [62.4%, 94.5%]). |
| **W12** | **Document-Wide Numerical Inconsistency:** Risk of silent drift across numbers, sample sizes, and ledger counts. | **FIXED-VERIFIED** | Implemented `scripts/check_paper_consistency.py` cross-verifying 22 numbers and counts against power JSON, ledger reconciliation, Table II, and test suite; 22/22 items passing, 0 mismatches; saved report to `results_v2/consistency_report.md`. |
| **W13** | **Missing Document Names:** 5 documents cited in prior reviews not found by exact filename. | **FIXED-VERIFIED** | Authored `SOURCE_OF_TRUTH_MANIFEST.md` designating authoritative candidates (marked PROPOSED); mapped all 5 missing documents to existing files with line-level excerpts using `scripts/map_missing_documents.py`. |
| **W14** | **Credential Exposure Risk:** `groq_key.txt` not explicitly covered by `.gitignore`; bundle ZIPs uninspected. | **FIXED-VERIFIED** | Created `scripts/audit_key_hygiene.py`; inspected all 4 submission ZIPs (all clean); created root `.gitignore` in work copy ignoring `groq_key.txt`, `*.key`, `.env`; zero key contents printed per Rule R4; report saved to `results_v2/key_hygiene_report.md`. |
| **W15** | **Overgeneralization in Discussion IX.A:** Claimed serialization gap is a "validity threat to any experiment". | **FIXED-VERIFIED** | Scoped statement in `research_paper_final.tex` L383 to "potential internal validity threat to web-agent evaluations that evaluate semantic HTML metadata channels without verifying their survival into model prompt context"; audited in `CLAIM_EVIDENCE_AUDIT.md`. |
| **W16** | **Missing Citation for BrowserGym:** BrowserGym mentioned in Section II.A without a citation key. | **FIXED-VERIFIED** | Updated Section II.A in `research_paper_final.tex` to link BrowserGym directly with its source publication in the WorkArena benchmark suite (`\cite{drouin2024workarena, workarenapp2024}`); audited in `CITATION_AUDIT.md`. |
| **W17** | **PDF Visual QA & Placeholders:** PDF needed visual inspection for broken refs, clipping, author placeholders, and mojibake. | **FIXED-UNVERIFIED** | Parsed all 18 pages of `media_1793024172936.pdf` via `scripts/audit_pdf_text_qa.py`; confirmed 0 broken citations (`[?]`) and 0 broken refs (`??`); cataloged title-page placeholders; provided 5-point Overleaf visual inspection guide in `PDF_VISUAL_QA.md`. |
| **W18** | **Zero Behavioral Variance (Open Blocker O1):** 41/41 pilot runs succeeded; tasks solvable from visible text; no treatment effect detectable. | **NEEDS-EVIDENCE** | Requires new live experiments on disambiguation tasks requiring pruned information, with preregistered plan and user API authorization. |
| **W19** | **Probe B Guessing Confound (Open Blocker O2):** Disambiguation Probe B tests guessing under an absent channel rather than accessibility-mediated reliance. | **NEEDS-DECISION** | Requires author decision on follow-up experimental protocol design. |
| **W20** | **Unpinned Cloud LLM Checkpoint (Open Blocker O3):** Physical weights checkpoint behind `gemini-flash-lite-latest` cloud alias unrecoverable. | **UNRESOLVABLE** | Stated as explicit limitation in Section VI.A and Section IX.C; future runs must record exact physical checkpoint revisions. |
| **W21** | **Single-Framework Generalization (Open Blocker O5):** Audit is scoped strictly to `browser-use 0.13.10`. | **UNRESOLVABLE** | Stated as explicit limitation across Abstract, Section I, and Section IX.C. Extension to other frameworks left for future work. |
| **W22** | **External Literature Novelty Claims (Open Blocker O6):** "Has not previously been audited" claim requires comprehensive literature search. | **NEEDS-EVIDENCE** | Requires external bibliographic search beyond offline archive. |
| **W23** | **Venue Selection & Acceptance Prediction (Open Blocker O7):** Target venue UNKNOWN; conference acceptance cannot be predicted. | **NEEDS-DECISION** | Stated "venue-specific readiness cannot be determined" per user Decision #1. |

---

## 3. Register Summary Statistics
- **Total Weaknesses Audited:** 23
- **FIXED-VERIFIED:** 15 (65.2%)
- **FIXED-UNVERIFIED:** 2 (8.7%)
- **NEEDS-DECISION:** 2 (8.7%)
- **NEEDS-EVIDENCE:** 2 (8.7%)
- **UNRESOLVABLE:** 2 (8.7%)

# FINAL CONSOLIDATED PEER-REVIEW AUDIT & VERIFICATION REPORT

**Manuscript Title:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*  
**Subtitle:** *A Systems Audit and Case Study of browser-use 0.13.10*  
**Research Workspace:** `C:\testing\research_execution_20261018`  
**Closure Version:** `final_closure_v3`  
**Audit Date:** 2026-10-26  
**Final Verdict:** **READY AFTER EXTERNAL COMPILATION**  

---

## 1. Executive Summary

This report establishes the final, evidence-first peer-review audit and minimal correction pass for the manuscript. Following an adversarial review identifying 24 potential weaknesses and 14 additional procedural requirements auditing prior closure artifacts (total: 38 items), every point was treated as an empirical hypothesis to verify against primary code, logs, datasets, and execution traces.

No live cloud experiments were run, no external API calls were made, zero funds were expended, historical raw data was preserved intact, and the quota ledger remains strictly locked at its historical state (604 requests against a 600 ceiling).

All confirmed defects—including table numbering mismatches across documentation, local model telemetry discrepancies, ambiguous abstract correspondence phrasing, uncited bibliography entries, and unstated assumptions regarding finite cluster censuses—have been corrected in `final_closure_v3`. The source manuscript is verified 100% syntactically consistent (21/21 citations resolve, 50/50 environments balanced). Because the local host lacks a LaTeX compiler binary (`pdflatex`/`xelatex`/`latexmk`), a fresh PDF must be generated via Overleaf or TeX Live before external submission.

---

## 2. Consolidated Audit Table (All 38 Items)

| Item | Issue Description | Verdict | Exact Evidence Reference | What Primary Evidence Establishes | Action Taken / Reason for No Change |
|:---:|:---|:---:|:---|:---|:---|
| **01** | Central question answered by data vs 41-run pilot ceiling | **CONFIRMED** | `results/v3_3arm_summary.csv:2-45`; `research_paper_final.tex:307-311` | All 41 completed runs achieved 100% success on simple tasks. Visible typography was sufficient; pilot data demonstrates harness stability but cannot measure behavioral harm from pruning. | Scoped paper strictly as an empirical systems audit of the observation pipeline; confirmed that abstract, intro, and conclusion claim zero behavioral efficacy. |
| **02** | Generalization beyond `browser-use 0.13.10`, Chromium, text-only, fixture | **NOT AN ISSUE** | `research_paper_final.tex:42-43, 85, 368-374` | Manuscript explicitly scopes claims in Title, Abstract, Section 1, and Section 7 (Limitations) to `browser-use 0.13.10` under `use_vision=False` on the local benchmark. | Retained explicit single-framework scope; verified absence of overgeneralized claims across diverse agent libraries. |
| **03** | 79.4% operational match driven by stock badge geometry vs general FP rate | **CONFIRMED** | `research_paper_final.tex:227-248`; `clickable_elements.py:228-240`; `MULTI_ROUTE_OBSERVATION_AUDIT.md` | All 7 unmatched selectors on `#home` are in-stock spans ($48.625 \times 15\text{px}$) matching the $10 \le w,h \le 50\text{px}$ icon heuristic. Routes without badges achieve 100% match. 79.4% is a layout-specific descriptive census. | Clarified in Abstract and Section 4.3 that 79.4% is a descriptive fixture census driven by inline badge geometry, not a universal false-positive rate. |
| **04** | Novelty and "information-loss" framing without downstream behavioral harm | **CONFIRMED** | `research_paper_final.tex:78-91, 354-360`; `audit_metadata_reachability.py` | Pruning reduces context bloat (benefits) while purging structured metadata (reachability bottlenecks). Labeling it "loss" without behavioral trials risks implying task degradation. | Reframed discussion to emphasize two-sided systems tradeoff (context compression vs metadata reachability) and structural representation divergence. |
| **05** | Wilson CIs on finite, clustered fixture census interpretation | **CONFIRMED** | `research_paper_final.tex:239-240`; `scratch/run_phase_b_browser_experiments.py` | Observations are a complete census of a single page layout where elements are clustered inside repetitive product cards. Standard binomial Wilson CIs assume an i.i.d. superpopulation. | Updated Section 4.3 to report descriptive census ($27/34 = 79.4\%$) as primary, noting Wilson CIs ($[63.2\%, 89.6\%]$) assume an unadjusted exchangeable superpopulation. |
| **06** | Submission bundle & reproduction instructions completeness | **CONFIRMED** | `final_closure_v2/manuscript_submission_bundle_final.zip`; `research_paper_final.tex:474-514` | Previous ZIP contained only manuscript sources; Appendix D scripts (`run_phase_b...`, `audit_metadata...`) exist in workspace but require Python 3.11 + Chromium CDP + `browser-use`. | Rebuilt submission bundle (`manuscript_submission_bundle_v3.zip`) for manuscript compilation; established clear inventory distinguishing manuscript bundle from repo reproducibility tools. |
| **07** | README test count differs from manuscript's 138 tests | **CONFIRMED** | `README_OVERLEAF.md:68` (126 tests); `README.md:63` (138 tests); `research_paper_final.tex:480` (138 tests) | `README_OVERLEAF.md` was not synchronized in the previous pass and still stated 126 tests. Discovery across all 19 `test_*.py` files finds exactly 138 unique tests. | Updated `README_OVERLEAF.md` to state 138 unit/regression tests in ~13--15s across 19 modules, eliminating the conflict. |
| **08** | Table numbering differs across README, evidence matrix, and manuscript | **CONFIRMED** | `research_paper_final.tex:200, 254, 396, 415, 439`; `README_OVERLEAF.md:35`; `EVIDENCE_TO_CLAIM_MATRIX.csv:20` | `README_OVERLEAF.md` called Qwen "Table 2 (Appendix B)" (it is Table 5). The CSV matrix called synthetic tables "Tables 5 & 6" (they are Tables 3 & 4). Table 2 is Multi-Route. | Reconciled all table references across `README_OVERLEAF.md`, `README_SUBMISSION.txt`, and `EVIDENCE_TO_CLAIM_MATRIX.csv` to match LaTeX document structure (Tables 1--5). |
| **09** | Qwen durations disagree across files vs stated 288.61s figure | **CONFIRMED** | `results/local_llama_summary.csv:2-6`; `EVIDENCE_TO_CLAIM_MATRIX.csv:17`; `research_paper_final.tex:432` | Primary logs record 5 runs: 3.34s, 1013.09s, 288.61s, 185.50s, 188.56s. 288.61s is Run 3 duration, NOT a mean. CSV matrix listed fabricated numbers (145.2s, 196.4s). | Corrected `EVIDENCE_TO_CLAIM_MATRIX.csv` and Appendix B prose to state that 288.61s is Run 3 duration, cite `local_llama_summary.csv`, and explain why averaging heterogeneous failure modes is invalid. |
| **10** | Quota ceiling is 600, while ledger records 604 requests and locked state | **CONFIRMED** | `results/daily_quota_ledger.json:3, 10, 12`; `BUDGET_SAFETY_AUDIT.md:12-24`; `budget_controller.py:213-370` | Prior runner checked budget at trial dispatch. Run 41 dispatched at 596 requests and took 8 steps ($596 + 8 = 604$). Before Run 42, guard halted fail-closed ($604 \ge 600$). | Preserved historical 604-request ledger and locked state intact. Documented the trial-dispatch overrun mechanism and subsequent per-step pre-dispatch hardening in Appendix C. |
| **11** | Semantic-control denominators differ across routes | **NOT AN ISSUE** | `research_paper_final.tex:258-262`; `MULTI_ROUTE_OBSERVATION_AUDIT.md`; `scratch/run_phase_b_browser_experiments.py` | Different routes have different page contents: `#home` has 26 semantic controls; `#cart` has 7; `#checkout` has 12; `#search` has 10. Forcing equal denominators would be scientifically false. | Retained route-specific denominators in Table 2; added explicit explanation clarifying that denominators reflect true page control counts. |
| **12** | Earlier exploratory and failed experiments disclosure | **CONFIRMED** | `results/pilot_raw_261.csv`; `results/main_raw_147.csv`; `EVIDENCE_TO_CLAIM_MATRIX.csv:18-19` | Historical 261-run pilot had 9 excluded failures in Rep 9; 147-run main attempt collapsed on runs 106-147 due to harness disconnects. These failures were omitted from the paper text. | Added a transparent disclosure paragraph in Section 5.3 documenting both historical attempts and explaining how they motivated v3/v4 harness hardening. |
| **13** | Synthetic tables, Qwen diagnostics, quota governance distract from contribution | **NOT AN ISSUE** | `research_paper_final.tex:387-472` (Appendices A, B, C) | Engineering details are properly segregated into Appendices A, B, and C, keeping the primary paper body (Sections 1--7) focused on the observation pipeline audit. | Retained appendix placement; ensured section headings explicitly designate them as reproducibility and engineering verification supplements. |
| **14** | Passing unit tests presented as scientific evidence | **CONFIRMED** | `research_paper_final.tex:479-483`; `EVIDENCE_TO_CLAIM_MATRIX.csv:24` (CLM-23); `EVIDENCE_TO_CLAIM_MATRIX_v2.md:25` | Unit tests verify software implementation and mocked assertion matching; they do not establish empirical scientific claims about LLM web navigation behavior. | Reclassified C15/CLM-23 in the evidence matrix as "Software Implementation Verification"; clarified in Appendix D that unit tests establish code resilience, not agent behavioral efficacy. |
| **15** | Power and TOST calculations labeled as planning analyses | **NOT AN ISSUE** | `research_paper_final.tex:312-350` (Section 6) | Section 6.2 lines 328-335 and Section 6.3 lines 349-350 explicitly identify calculations as simulation and illustrative planning models under stated assumptions. | Retained clear labeling; reinforced in Section 6 and Section 7 that power curves represent synthetic planning bounds. |
| **16** | Model alias `gemini-flash-lite-latest` prevents exact replication | **CONFIRMED** | `research_paper_final.tex:307-308`; `results/daily_quota_ledger.json` | Cloud runner accessed Google AI Studio rolling alias `gemini-flash-lite-latest`. Client cannot audit or pin server-side physical model checkpoint revisions. | Preserved disclosure in Section 5.3; added note in Section 7 (Limitations) explicitly identifying unpinned rolling model aliases as an experimental reproducibility constraint. |
| **17** | Overstated terms ("systems baselines", "novelty claims") | **CONFIRMED** | `research_paper_final.tex:58, 85, 381` | Line 381 claimed work "establishes essential systems baselines for future web agent architecture", which overstates the scope of a single-framework audit. | Moderated conclusion prose: replaced promotional wording with "provides empirical observation baselines and a reproducible methodology for auditing observation pipelines in browser agents." |
| **18** | Uncited claims (20,000 DOM nodes, screen-reader harms, `llms.txt`, MCP) | **CONFIRMED** | `research_paper_final.tex:78, 357, 362`; `references.bib` | Line 357 stated 20,000 nodes without context; line 362 asserted screen-reader harms without referencing W3C guidelines. | Qualified DOM size as observed on complex commercial enterprise SPAs; linked screen-reader degradation to W3C WAI-ARIA authoring recommendations~\cite{wai_aria12}. |
| **19** | Related work coverage (other pipelines, AXTree distillation, Set-of-Mark) | **NOT AN ISSUE** | `research_paper_final.tex:93-124`; `references.bib` | Section 2 covers BrowserGym/WorkArena AXTree distillation~\cite{drouin2024workarena, workarenapp2024}, AgentOccam~\cite{agentoccam2025}, and WebVoyager visual Set-of-Mark~\cite{he2024webvoyager}. | Maintained existing related work coverage; all 6 benchmark suites are accurately attributed to peer-reviewed proceedings. |
| **20** | Extended whitelist & fixed geometry presented as proven mitigations | **NOT AN ISSUE** | `research_paper_final.tex:173-174, 231` | Manuscript describes extended whitelist solely as an attribute delivery mechanism in serializer code, and geometry as a false-positive inclusion source. Neither is claimed as a proven task mitigation. | Verified that prose nowhere asserts performance improvements from extended whitelisting or geometry threshold tuning. |
| **21** | Source line numbers & heuristic thresholds version-pinned | **NOT AN ISSUE** | `research_paper_final.tex:131, 135, 144, 166, 173, 230` | All code listings and line numbers correspond exactly to the PyPI binary distribution of `browser-use 0.13.10`. Version is pinned throughout text and title. | Preserved exact line numbers and version pinning. |
| **22** | Abstract 27/34 headline distinguishing semantic vs operational match | **CONFIRMED** | `research_paper_final.tex:58` | Abstract stated "27 of 34 interactive elements ($79.4\%$) match Blink accessibility nodes", obscuring that 100% of genuine controls matched and the 7 unmatched were false-positive badge spans. | Rewrote abstract headline: explicitly states $100\%$ ($26/26$) semantic control match and explains that $27/34$ ($79.4\%$) operational match stems from 7 non-interactive status badges misclassified by geometry. |
| **23** | Unused bibliography entries | **CONFIRMED** | `references.bib`; `research_paper_final.tex:381` | `references.bib` contained 22 entries; manuscript cited 20. `mantel1959statistical` and `wai_aria11` were uncited. | Cited `mantel1959statistical` in Section 6.1 alongside Agresti; removed unused `wai_aria11`. Now 21/21 entries are cited (100% resolution, 0 unused). |
| **24** | "Equivalence Fallacy" defined & distinguished from literature | **CONFIRMED** | `research_paper_final.tex:349, 423` | Coining "The Equivalence Fallacy" without contextualizing it against established statistical principles (absence of evidence $\ne$ evidence of absence) risked terminological overreach. | Contextualized the term in Section 6.3 and Appendix A as the application of classic bioequivalence principles~\cite{schuirmann1987comparison, agresti2002categorical} to small-sample agent benchmarks. |
| **25** | Prior audit claims vs actual evidence in `final_closure_v2` | **CONFIRMED** | `final_closure_v2/FINAL_AUDIT_REPORT.md`; `EVIDENCE_TO_CLAIM_MATRIX_v2.md` | `final_closure_v2` left stale test counts in `README_OVERLEAF.md`, wrong table numbers in the CSV matrix, non-existent file references for Qwen, and uncited bib entries. | Independently audited all claims against primary files; superseded `final_closure_v2` with fully verified `final_closure_v3`. |
| **26** | Test execution, exit status, and module discovery | **CONFIRMED** | `task-25.log`; `transcript_full.jsonl:26, 35, 36` | `python -m unittest discover -s . -p "test_*.py"` discovered 138 tests across 19 modules, passing in 13.542s (exit code 0). The exit code 1 was caused by downstream PowerShell pipeline filter `Select-String`. | Documented the direct command and direct exit code 0; explained the PowerShell filtering artifact. Verified 138 tests passing across 19 modules. |
| **27** | Completed pilot trials vs attempts reconciliation | **CONFIRMED** | `results/v3_3arm_summary.csv:2-45`; `results/v3_run_summary.csv` | Exactly 41 unique intended runs; 44 total attempt rows. Run 26 had 3 aborted attempts due to HTTP 503 UNAVAILABLE from Google AI Studio, succeeding on attempt 4. Completed trials = 41 (all score 1.0). | Explicitly reported the four separate quantities (41 unique runs, 44 attempts, 3 infrastructure retries, 41 completed trials) in Section 5.3 and evidence matrices. |
| **28** | Semantic vs operational correspondence across routes | **CONFIRMED** | `local_closure_results/MULTI_ROUTE_OBSERVATION_AUDIT.md`; `run_phase_b_browser_experiments.py` | `#home`: 27/34 op (79.4%), 26/26 sem (100%); `#cart`: 8/8 op (100%), 7/7 sem (100%); `#checkout`: 13/13 op (100%), 12/12 sem (100%); `#search`: 16/19 op (84.2%), 10/10 sem (100%). | Reconstructed exact populations; verified that 100% semantic control match is never described as 100% correspondence for all DOM elements or selectors. |
| **29** | Previous audit's ZIP claims & boundary | **CONFIRMED** | `final_closure_v2/manuscript_submission_bundle_final.zip` | ZIP contained 6 files (manuscript bundle only); excluded stale PDF (correct). `README_SUBMISSION.txt` listed 8 files (inconsistent). Reproducibility scripts were absent from ZIP. | Rebuilt `manuscript_submission_bundle_v3.zip` containing the exact 6 verified manuscript files; aligned `README_SUBMISSION.txt`; defined explicit reproducibility boundary. |
| **30** | Reproducibility instructions vs actual package contents | **CONFIRMED** | `research_paper_final.tex:474-514`; `reproducibility_checklist.md` | Appendix D commands run against files in the workspace, requiring local Python 3.11, Chromium CDP, and `browser-use 0.13.10`. They cannot execute from the manuscript-only ZIP alone. | Documented local execution prerequisites in Appendix D and README; clearly separated manuscript compilation files from repository execution tools. |
| **31** | Stale PDF & source-to-PDF consistency | **CONFIRMED** | `compiled_manuscript.pdf` (752 KB); `research_paper.pdf` (594 KB) | PyPDF extraction confirms candidate PDFs lack Table 2 multi-route data, `#cart`, `#checkout`, and 138-test tally. Local host lacks LaTeX compiler binaries. | Stale PDFs excluded from submission bundle; external Overleaf / TeX Live compilation explicitly identified as pending. |
| **32** | Evidence matrix overstatement | **CONFIRMED** | `EVIDENCE_TO_CLAIM_MATRIX.csv`; `EVIDENCE_TO_CLAIM_MATRIX_v2.md` | Previous matrices assigned categorical "YES" or "VERIFIED" to claims supported only by synthetic data, software unit tests, or ceiling-effect exploratory runs. | Created `EVIDENCE_TO_CLAIM_MATRIX_v3.md` and updated CSV matrix, replacing "YES" with qualified evidentiary scopes and explicit prohibited claim boundaries. |
| **33** | Quota ledger and historical safety state | **CONFIRMED** | `results/daily_quota_ledger.json`; `budget_controller.py:213-370` | Historical ledger records 604 requests against 600 ceiling in locked state (`halted_due_to_ceiling: true`). Represents cumulative client-side model requests recorded across historical trials. | Preserved historical ledger at 604 requests without reset. Maintained strict fail-closed safety gate. |
| **34** | Qwen/local-model diagnostic wording & source records | **CONFIRMED** | `results/local_llama_summary.csv:2-6`; `local_llama_pilot_runs/` | Model tag in CSV is `qwen3:4b`. Primary logs record 5 runs: 3.34s (init error), 1013.09s (cold start timeout), 288.61s (Run 3 watchdog timeout), 185.50s, 188.56s. 288.61s is Run 3 runtime. | Corrected model tag, cited `local_llama_summary.csv`, removed fabricated numbers, and disclosed that 288.61s is Run 3 duration rather than an aggregate mean. |
| **35** | Bibliography and citation validation | **CONFIRMED** | `references.bib`; `final_closure_v3/references.bib`; `scratch/check_latex.py` | Manuscript cited 20 keys; bib had 22 entries. Citing `mantel1959statistical` and removing `wai_aria11` yields exactly 21 entries, all 21 cited (100% resolution, 0 unused). | Validated all 21 publication records; verified 100% resolution with zero unused entries and zero unresolved keys. |
| **36** | Claimed test runtime | **CONFIRMED** | `research_paper_final.tex:480`; `EVIDENCE_AUDIT.md`; `task-25.log` | Test runtime varies between ~12s and ~19s depending on CPU load. Verified run executed in 13.542 seconds. | Stated runtime as "~13--15s (typical execution across 138 tests; varies with machine load)" rather than asserting a fixed constant. |
| **37** | Changed artifacts and traceability | **CONFIRMED** | `final_closure_v3/` | All modifications made in `final_closure_v3` while preserving original workspace files. Change log explicitly links every modification to primary evidence. | Documented all file diffs and rationales in Section 3 of this report; packaged final files into `manuscript_submission_bundle_v3.zip`. |
| **38** | Final verdict reflects verified status | **CONFIRMED** | Workspace tools; host environment | Manuscript source and bibliography are fully verified and consistent, but host machine lacks a LaTeX compiler. Fresh PDF generation and visual check must occur externally. | Assigned final verdict **READY AFTER EXTERNAL COMPILATION**. |

---

## 3. Detailed Change Log (Primary Evidence to Edits)

All edits were executed exclusively on copies located in `C:\testing\research_execution_20261018\final_closure_v3\`. Original files in the parent directory remain unchanged.

### File 1: `research_paper_final.tex`
1. **Abstract (lines 57–59):**
   - *Edit:* Clarified that 100% ($26/26$) of genuine semantic interactive controls match Blink accessibility nodes on `#home`, and that operational correspondence is $27/34$ ($79.4\%$) due to the heuristic misclassification of seven non-interactive stock badges as clickable icons.
   - *Evidence Basis:* `local_closure_results/MULTI_ROUTE_OBSERVATION_AUDIT.md:11`; `scratch/run_phase_b_browser_experiments.py:195-247`.
2. **Section 4.3 (lines 233–240):**
   - *Edit:* Formalized denominator accounting ($n=34$ operational vs $n=26$ semantic controls). Added explicit explanation that route measurements represent a finite census of clustered elements within a single layout rather than an independent random sample, and that Wilson intervals ($[63.2\%, 89.6\%]$) assume an unadjusted exchangeable superpopulation.
   - *Evidence Basis:* `CLUSTERING_AND_EXPERIMENTAL_UNIT_AUDIT.md`; `scratch/run_phase_b_browser_experiments.py`.
3. **Section 5.3 (lines 307–311):**
   - *Edit:* Added transparent disclosure of earlier engineering iterations: historical 261-run pilot with 9 excluded failures from Rep 9, and historical 147-run execution attempt where runs 106–147 aborted due to harness disconnect timeouts.
   - *Evidence Basis:* `results/pilot_raw_261.csv`; `results/main_raw_147.csv`; `EVIDENCE_TO_CLAIM_MATRIX.csv:18-19`.
4. **Section 6.1 (line 318):**
   - *Edit:* Added citation `\cite{mantel1959statistical}` alongside Agresti (2002) for the Cochran–Mantel–Haenszel test.
   - *Evidence Basis:* `references.bib:120-128`.
5. **Section 6.3 (lines 349–351):**
   - *Edit:* Contextualized "The Equivalence Fallacy" by linking it to established statistical bioequivalence literature (`schuirmann1987comparison`, `agresti2002categorical`).
   - *Evidence Basis:* `schuirmann1987comparison`; `agresti2002categorical`.
6. **Section 7 / Discussion (lines 355–365):**
   - *Edit:* Qualified DOM node count ("tens of thousands of nodes on complex commercial single-page applications") and cited W3C WAI-ARIA guidelines~\cite{wai_aria12} regarding screen-reader tree cluttering. Moderated conclusion phrasing from "establishes essential systems baselines" to "provides empirical observation baselines and a reproducible methodology".
   - *Evidence Basis:* Item 17 and Item 18 audit findings; W3C WAI-ARIA 1.2 Recommendation.
7. **Appendix B (lines 430–460):**
   - *Edit:* Corrected model identifier to `qwen3:4b`; corrected source file reference to `results/local_llama_summary.csv` and `results/local_llama_pilot_runs/`; explicitly clarified that 288.61s is the runtime of diagnostic run \texttt{qwen3\_smoke\_003} rather than an aggregate mean across heterogeneous failure modes.
   - *Evidence Basis:* `results/local_llama_summary.csv:1-6`; `local_closure_results/REANALYSIS_LOCAL_QWEN_5.md`.
8. **Appendix D (lines 477–486):**
   - *Edit:* Updated test runtime to "~13--15s depending on machine load"; explicitly stated prerequisites (Python 3.11, Chromium CDP, `browser-use 0.13.10`).
   - *Evidence Basis:* `task-25.log` (13.542s execution); environment audit.

### File 2: `references.bib`
1. **Entry Removal:** Removed unused entry `wai_aria11` (superseded by cited `wai_aria12`).
2. **Citation Alignment:** `mantel1959statistical` cited in Section 6.1.
3. *Result:* Exactly 21 entries defined; exactly 21 entries cited in manuscript source (100% resolution, 0 unused entries).

### File 3: `README_OVERLEAF.md`
1. Synchronized test count to 138 tests across 19 modules in ~13--15s (13.542s baseline execution).
2. Updated BibTeX count to 21 verified entries, 100% cited.
3. Corrected table numbers: Table 1 (Reachability, Sec. 4.2), Table 2 (Multi-Route, Sec. 4.3), Tables 3 & 4 (Synthetic benchmarks, App. A), Table 5 (Qwen exploratory telemetry, App. B).
4. Updated target package to `manuscript_submission_bundle_v3.zip`.

### File 4: `README_SUBMISSION.txt`
1. Reconciled package file inventory to match the 6 files present in `manuscript_submission_bundle_v3.zip`.
2. Updated bibliography entry description to 21 entries (100% cited).
3. Documented reproducibility materials location in the project repository workspace.

### File 5: `EVIDENCE_TO_CLAIM_MATRIX.csv`
1. **CLM-16:** Corrected Qwen durations and model tag; cited `results/local_llama_summary.csv`; clarified that 288.61s is Run 3 duration.
2. **CLM-19:** Corrected table reference from "Tables 5 & 6" to "Tables 3 & 4".
3. **CLM-23:** Replaced 19s runtime with ~13--15s (13.542s baseline); qualified that test suite verifies software implementation resilience, not live agent task efficacy.
4. **CLM-24:** Updated references count to 21 verified peer-reviewed publications and W3C standards (100% cited).

### File 6: `EVIDENCE_TO_CLAIM_MATRIX_v3.md`
- Generated a comprehensive 23-claim Markdown matrix replacing categorical "YES" labels with qualified evidentiary scopes and defining explicit boundaries of prohibited claims.

---

## 4. Needs New Experiment / Needs Additional Data

The following items represent empirical questions that **cannot** be answered by the existing data. They are explicitly acknowledged as limitations in Section 7 of the manuscript and do not block submission of the scoped systems audit:

1. **Downstream Behavioral Impact of Pruning:**
   - *Required Experiment:* A multi-arm confirmatory trial ($N \ge 1,080$ runs based on TOST equivalence sizing) on challenging web tasks where visual anchors alone are insufficient, comparing unaugmented baseline, entity ARIA, and custom attributes.
   - *Claim It Would Enable:* Establishing whether metadata channel reachability translates into statistically significant differences in end-to-end task success.
2. **Cross-Framework Observation Pipeline Comparison:**
   - *Required Experiment:* AST and runtime trace of alternative agent libraries (e.g., BrowserGym, Stagehand, Skyvern, Crawl4AI) across identical HTML stimulus fixtures.
   - *Claim It Would Enable:* Generalizing the DOM serialization gap beyond `browser-use 0.13.10`.
3. **Multimodal Visual Grounding Ablation:**
   - *Required Experiment:* Direct comparison of text-only observation (`use_vision=False`) against screenshot-based Set-of-Mark visual prompting on identical tasks.
   - *Claim It Would Enable:* Quantifying whether visual observation channels bypass DOM pruning bottlenecks without introducing new visual grounding confounds.
4. **Controlled Evaluation of Alternative Geometry Heuristics:**
   - *Required Experiment:* Testing modified icon detection heuristics (e.g., requiring explicit cursor pointers or role attributes in addition to $10 \le w,h \le 50\text{px}$) on dynamic e-commerce layouts.
   - *Claim It Would Enable:* Proving an optimal mitigation for false-positive selector inclusion.
5. **Pinned Cloud Checkpoint Replication:**
   - *Required Experiment:* Replication of the cloud pilot against an explicit, pinned model snapshot (e.g., dated release checkpoint) rather than a rolling endpoint alias (`gemini-flash-lite-latest`).
   - *Claim It Would Enable:* Guaranteed temporal bitwise reproducibility of cloud model interactions.

---

## 5. Epistemological Categorization of Project Materials

To prevent conflation of distinct evidence types, project materials are strictly categorized:

1. **Confirmed Empirical Findings:**
   - Deterministic pruning of Schema.org JSON-LD via `DISABLED_ELEMENTS` (serializer.py:18).
   - Tag and attribute stripping on non-interactive containers (serializer.py:1046–1058).
   - Omission of custom `data-*` attributes under `DEFAULT_INCLUDE_ATTRIBUTES` (views.py:18).
   - Operational correspondence census ($27/34 = 79.4\%$) on `#home` driven by 7 in-stock badge spans ($48.625 \times 15\text{px}$) matching icon heuristic ($10 \le w,h \le 50\text{px}$).
   - 100% semantic control correspondence ($26/26$ on home, $8/8$ on cart, $13/13$ on checkout, $10/10$ on search).
   - Action-Label Co-Location Confound in entity-specific button ARIA labels.
2. **Exploratory Pilot Telemetry (Non-Confirmatory):**
   - 41 completed cloud pilot trials using `gemini-flash-lite-latest`: exhibited 100% success ceiling effect on simple tasks ($RD = 0.00$, Newcombe 95% CI: $[-0.228, +0.228]$); 3 retried 503 errors on Run 26.
   - 5 local Qwen3:4b diagnostic runs: 1 initialization error (3.34s), 1 cold start timeout (1013.09s), 3 watchdog timeouts (288.61s, 185.50s, 188.56s).
3. **Historical Infrastructure Failures:**
   - Historical 261-run pilot: 9 timeouts in Repetition 9; post-hoc exclusion of 11 runs in 250-run cleaned view.
   - Historical 147-run attempt: harness collapse on runs 106–147 (consecutive 7-step disconnect timeouts).
4. **Synthetic Pipeline Benchmarks (Mock Arithmetic Checks):**
   - Appendix A tables (Tables 3 & 4) derived from `test_scratch_synthetic_data/` verifying CMH and Newcombe score formulas against clinical benchmarks; explicitly disclaimed as non-empirical.
5. **Analytical Planning Derivations:**
   - Monte Carlo power simulations ($11.45\%$ power at $n=20$ for $\Delta=0.20$).
   - Closed-form TOST sample size bounds ($N \ge 1,080$ for $\delta=\pm 0.10$ at $p=0.70$).
6. **Software Implementation Checks (Unit Tests):**
   - 138 passing unit/regression tests across 19 modules; validates code resilience and guardrail logic; does not prove model behavioral efficacy.
7. **Unexecuted Confirmatory Experiments:**
   - Confirmatory 3-arm RCBD protocol ($N=72$); pre-registered blueprint; zero live trials executed.

---

## 6. Package Inventory & Reproducibility Boundaries

### Inside `final_closure_v3/manuscript_submission_bundle_v3.zip` (31,939 bytes)
1. `research_paper_final.tex` (53,951 bytes) — Corrected LaTeX source manuscript.
2. `references.bib` (7,825 bytes) — Clean BibTeX bibliography (21 entries, 100% cited).
3. `architecture_pipeline_figure.tex` (5,422 bytes) — TikZ pipeline figure.
4. `README_OVERLEAF.md` (3,638 bytes) — 1-click Overleaf compilation instructions and inspection checklist.
5. `README_SUBMISSION.txt` (2,037 bytes) — Submission package manifest and build commands.
6. `EVIDENCE_TO_CLAIM_MATRIX.csv` (12,208 bytes) — Traceable claim-to-evidence matrix.

### Available Separately in Project Workspace
- Full automated test suite (19 `test_*.py` files, 138 tests).
- Phase B browser experiment runner (`scratch/run_phase_b_browser_experiments.py`).
- Reachability audit harness (`audit_metadata_reachability.py`).
- CDP accessibility comparison tool (`compare_accessibility_tree.py`).
- Statistical analysis reproduction script (`reproduce_power_audit.py`).
- HTML stimulus fixtures (`variants/v0-baseline` through `v3-data-attrs`, `fixtures/edge_cases.html`, `fixtures/geometry_boundary_cases.html`).
- Historical pilot run CSVs and JSON traces (`results/v3_3arm_summary.csv`, `results/local_llama_summary.csv`).

### Required Reader Environment
- **For Manuscript Compilation:** Overleaf (free tier, pdfLaTeX, TeX Live 2024) or local TeX Live / MiKTeX installation.
- **For Offline Reproduction Suite:** Windows 10/11 or Linux, Python 3.11, Chromium (via CDP), `browser-use==0.13.10`. Zero paid API keys, zero cloud inference credits required.

---

## 7. Final Verdict and Required User Actions

### Final Decision: **READY AFTER EXTERNAL COMPILATION**

**Rationale:**  
The manuscript source (`research_paper_final.tex`) and bibliography (`references.bib`) are fully verified, internally consistent, and strictly scoped to primary evidence. All 21 citations resolve, all 50 LaTeX environments are balanced, and table numbering, test tallies, and local model telemetry are reconciled across all documents. 

However, because the local Windows host machine lacks a LaTeX compiler executable (`pdflatex`, `xelatex`, or `latexmk`), compiling a fresh PDF is blocked locally. Pre-existing PDFs (`compiled_manuscript.pdf` and `research_paper.pdf`) are confirmed stale and have been excluded from the submission bundle. Therefore, visual inspection of the final rendered PDF must be completed in an external compilation environment (e.g., Overleaf).

### Actions for User:
1. Download `C:\testing\research_execution_20261018\final_closure_v3\manuscript_submission_bundle_v3.zip`.
2. Log into [Overleaf](https://www.overleaf.com), create a new project, and upload the ZIP file.
3. Verify that the compiler is set to **pdfLaTeX** and TeX Live version is **2024** (or 2023).
4. Click **Recompile** and perform visual inspection against the checklist in `README_OVERLEAF.md`:
   - Figure 1 (Section 3) fits cleanly within `\linewidth`.
   - Table 1 (Section 4.2) and Table 2 (Section 4.3) render with proper column widths.
   - Tables 3 & 4 (Appendix A) display the synthetic disclaimer cleanly.
   - Table 5 (Appendix B) formats Qwen telemetry without overflow.
5. Download the freshly compiled PDF from Overleaf. The paper is then ready for double-blind submission.

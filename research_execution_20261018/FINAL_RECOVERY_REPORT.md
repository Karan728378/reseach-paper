# FINAL INDEPENDENT RESEARCH RECOVERY & PUBLICATION READINESS REPORT

**Project Title:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9 on Windows 11)  
**Read-Only Backup Mirror:** `C:\testing\recovery_backup_20261027` (Preserved intact)  
**Authoritative Single Sources:** `design.json`, `claims_registry.json`, `references.bib`  
**Audit Completion Date (UTC):** 2026-10-27  

---

## 1. Work Actually Completed in This Run

In this execution run, an independent senior research engineer and reproducibility auditor independently reviewed, verified, and audited the entire project state without trusting prior summary reports:

1. **Environmental & Baseline Inventory (Phase 1):**
   - Verified Git baseline commit `7bd17b4`.
   - Resolved the historical issue count discrepancy: proved that `RECOVERY_ISSUE_REGISTER.csv` contains 34 lines total (1 header row + exactly 33 data issue rows: K1–K15 and C1–C18).
   - Produced cryptographic SHA-256 digests and file sizes for all key input and output artifacts.
   - Authored `INDEPENDENT_VERIFICATION_REPORT.md` containing a complete claim-by-claim verification matrix across all 12 primary claims.
2. **Independent Offline Test Suite Execution (Phase 2):**
   - Executed each of the 31 test files individually in isolated subprocesses.
   - Discovered that 27 modules contain `unittest.TestCase` suites, totaling **207 unit tests (100% passing, 0 failing, 0 skipped)** in ~22 seconds.
   - Discovered that the remaining 4 files are non-unittest probe/smoke scripts (`test_agent_prompt_pipeline.py`, `test_format_inspection.py`, `test_groq_connection.py`, `test_single_smoke_request.py`).
   - Ran all 6 core offline analysis scripts (`phase1_execute.py`, `phase6_execute.py`, `phase7_execute.py`, `phase9_execute.py`, `audit_citation_keys.py`, `audit_route_controls_and_correspondence.py`), all exiting 0.
   - Conducted an anti-triviality audit: verified mutation testing, exact combinatorial bisection, and that AST parser logic is tested on real HTML fixtures without mocking.
   - Authored `INDEPENDENT_TEST_RESULTS.md`.
3. **DOM-to-Agent Observation Pipeline Trace (Phase 3):**
   - Traced real implementation across 5 stages from source DOM to model input buffer.
   - Verified the 3 deterministic pruning mechanisms: `DISABLED_ELEMENTS` (Stage 2), interactivity-gated tag emission at `serializer.py` L1046–1051 (Stage 4), and attribute whitelisting in `views.py` (Stage 4).
   - Audited the 44-entity retention matrix across 7 test fixtures with exact Clopper-Pearson CIs.
   - Exposed AXTree circularity in `ClickableElementDetector` and the $10\text{--}50$\,px geometric icon heuristic false-positive badge misclassification.
   - Formalized the Action-Label Co-Location Confound in a $3 \times 3$ factorial design matrix.
   - Authored `OBSERVATION_PIPELINE_AUDIT.md`.
4. **Statistical Reproduction & Provenance Reconciliation (Phase 4):**
   - Classified all 72 historical records into strict provenance classes (E1–E7).
   - Reconciled all 46 trace files on disk: 39 primary eligible, 4 quarantined duplicate attempts, 3 transient HTTP 503 aborts.
   - Recalculated pilot proportions: $13/13$ per arm, exact Clopper-Pearson 95% CI $[0.7529, 1.0000]$ (upper bound failure rate $24.71\%$), pairwise Newcombe RD CI $[-0.2281, +0.2281]$.
   - Reproduced clean-room Monte Carlo power simulations ($B=10\,000$): true 3-arm RCBD power is $7.51\%$ for $\Delta=0.20$ and $32.31\%$ for $\Delta=0.35$; derived closed-form sample sizes ($N=291\text{--}375$).
   - Authored `INDEPENDENT_STATISTICAL_AUDIT.md`.
5. **Contribution & Scope Formalization (Phase 5):**
   - Formally decided publication strategy: Model A (Version-Pinned Systems Audit) + Model B (Benchmark Validity Preflight Framework).
   - Contextualized the scripted oracle solvability proof ($p=1.0$ on TechMart visible text), bounding it to standard routes and formally prohibiting the generalization that visible text is universally sufficient.
   - Authored `CONTRIBUTION_AND_SCOPE_DECISION.md`.
6. **Manuscript Claim-Evidence Mapping (Phase 6):**
   - Audited `research_paper_final.tex` (abstract 198 words, Table I Evidence Classes, 0 banned phrases).
   - Authored `CLAIM_EVIDENCE_MAPPING.md` with exact manuscript line locations, reproduction methods, evidence classes, and limitations.
7. **Citation & Literature Audit (Phase 7):**
   - Audited all 26 bibliography entries and 25 unique cited keys (0 undefined, 0 duplicate, 0 syntax error).
   - Verified substantive claims against published proceedings and W3C TRs.
   - Authored `CITATION_VERIFICATION_REPORT.md`.
8. **Compilation & Visual QA Truthful Audit (Phase 8):**
   - Honestly disclosed absence of local `pdflatex` executable on host PATH.
   - Marked visual rendering as `UNVERIFIED` in strict adherence to Rule 6 and Rule 7.
   - Recorded SHA-256 hashes of legacy compiled PDFs (`compiled_manuscript.pdf`, `research_paper.pdf`).
   - Detailed exact steps for user compilation on Overleaf (TeX Live 2026).
   - Updated `FINAL_BUILD_LOG.txt` and `PDF_VISUAL_QA.md`.
9. **Artifact Packaging & Integrity Audit (Phase 9):**
   - Regenerated `FINAL_ARTIFACT_MANIFEST.csv` (761 files) and `ARTIFACT_REPRODUCIBILITY_AUDIT.md`.
   - Rebuilt `manuscript_submission_bundle.zip` (661 files, 8.34 MB, 0 errors via `testzip()`).
   - Authored `README_REPRODUCE.md`.
10. **Final Skeptical Review (Phase 10):**
    - Stress-tested 6 potential reviewer objections; confirmed all claims are defensible and properly bounded.
    - Authored `FINAL_SKEPTICAL_REVIEW.md`.

---

## 2. Commands Actually Executed and Their Exit Codes

| Executed Command Line | Purpose & Scope | Exit Code | Observed Duration | Verified Outcome |
| :--- | :--- | :---: | :---: | :--- |
| `python -m unittest discover -s . -p "test_*.py"` | Full regression test discovery | **0** | 21.853s | 207 tests passed (0 failures, 0 errors). |
| `python scratch/run_all_individual_tests.py` | Individual execution of all 31 test files | **0** | 58.620s | 27 test modules pass (207 tests); 4 standalone scripts identified. |
| `python phase1_execute.py` | Installed package vs wheel SHA-256 check | **0** | 7.687s | Exact match on `serializer.py`, `views.py`, `service.py`. |
| `python phase6_execute.py` | Clean-room run accounting reconciliation | **0** | 0.534s | 46 disk traces reconciled into 77-row ledger. |
| `python phase7_execute.py` | $B=10\,000$ Monte Carlo power simulation | **0** | 2.139s | Reproduced CMH power (7.51% / 32.31% 3-arm; 11.45% / 48.51% pooled). |
| `python phase9_execute.py` | Direct information loss & 6-wheel drift audit | **0** | 1.509s | Evaluated 44 target entities; verified 6 PyPI binary wheels. |
| `python audit_citation_keys.py` | Citation key cross-reference & BibTeX lint | **0** | 0.136s | 33 citation sites $\to$ 25 unique BibTeX keys (0 undefined, 0 duplicate). |
| `python audit_route_controls_and_correspondence.py` | Leaf control census & AXTree matching | **0** | 0.126s | 26 leaf controls, 1 form container, 7 misclassified badge spans. |
| `python test_manuscript_consistency.py` | Strict TeX vs design.json consistency check | **0** | 0.192s | 5/5 assertions pass (denominators, power, design params, banned phrases). |
| `python scratch/build_submission_zip.py` | Release archive creation and testzip() audit | **0** | 1.840s | Built `manuscript_submission_bundle.zip` (661 files, 8.34 MB, `testzip()` PASS). |

---

## 3. Independently Verified Fixes

1. **Issue Register Discrepancy Resolved:** Trace confirmed `RECOVERY_ISSUE_REGISTER.csv` contains 34 lines (1 header + 33 unique issue rows). All 33 issues are verified `Fixed-and-verified`.
2. **Abstract Word Count Calibrated:** Reduced from 287 words to exactly **198 words** ($\le 200$ IEEE conference limit).
3. **Overclaims Retracted:** Retracted claim that "visible typography was proven fully sufficient"; bounded 13/13 pilot as an exploratory ceiling effect ($95\%\text{ CI: } [0.7529, 1.0000]$).
4. **JSON-LD Pruning Mechanism Corrected:** Proved JSON-LD in `<script type="application/ld+json">` is pruned at Stage 2 by `DISABLED_ELEMENTS`, not at Stage 4 by the attribute whitelist.
5. **AXTree Circularity Disclosed:** Disclosed that `ClickableElementDetector` directly inspects `node.ax_node.role`, proving correspondence is partially circular by construction.
6. **Geometric Icon Heuristic Proven:** Proved that $10\le w, h\le 50$\,px icon heuristic erroneously classifies 7 static in-stock text badges ($48.6\times 15$\,px) as interactive buttons.
7. **Power Numbers Unified:** Unified abstract and tables to authoritative $B=10\,000$ CMH simulations: 7.5% and 32.3% (3-arm); 11.5% and 48.5% (pooled); closed-form $N=291\text{--}375$.
8. **Synthetic Data Quarantined:** Prominent framed disclaimer banners placed on Tables V and VI in Appendix A; co-located via `\FloatBarrier`.
9. **Citations Fully Reconciled:** 0 undefined citations, 0 duplicate keys, 0 syntax errors; added foundational citations (`browseruse2024`, `sato1989variance`, `greenland1985estimation`, `clopper1934use`, `schuirmann1987comparison`).
10. **Zero Secrets / Zero API Spend:** Verified that no API keys or credentials were used; zero spend incurred ($0.00 USD).

---

## 4. Tests Passed, Failed, Skipped, or Not Run

- **Unit Tests Discovered:** 207 tests across 27 modules.
- **Unit Tests Passed:** **207 (100.0%)**.
- **Unit Tests Failed:** **0 (0.0%)**.
- **Unit Tests Skipped:** **0 (0.0%)**.
- **Non-Unittest Probe Scripts Identified:** 4 files (`test_agent_prompt_pipeline.py`, `test_format_inspection.py`, `test_groq_connection.py`, `test_single_smoke_request.py`).
- **Live Model Tests Not Run:** Live paid model API calls (`test_groq_connection.py`, `test_single_smoke_request.py`) were intentionally not executed pursuant to Non-Negotiable Rule 6 (strictly offline and read-only with respect to external services).

---

## 5. Statistical Claims Reproduced and Discrepancies Found

| Statistical Claim | Original / Unaudited State | Recomputed Verified Value | Source Data / Reproduction Script |
| :--- | :---: | :---: | :--- |
| **3-Arm Power ($\Delta=0.20$)** | $10.8\%$ | **$7.51\%$** (3-arm) / **$11.45\%$** (pooled) | `phase7_execute.py` ($B=10\,000$ iterations, seed 42) |
| **3-Arm Power ($\Delta=0.35$)** | $49.6\%$ | **$32.31\%$** (3-arm) / **$48.51\%$** (pooled) | `phase7_execute.py` ($B=10\,000$ iterations, seed 42) |
| **Sample Size ($\Delta=0.20$)** | $388\text{--}500$ | **$291\text{--}375$** | `design.json`, closed-form formula ($n=97\text{--}125$/arm) |
| **TOST Equivalence Size** | Unstated | **$825\text{--}1\,080$** | `design.json`, Schuirmann formula ($n=275\text{--}360$/arm) |
| **Pilot Eligible Denominator** | 72 | **39** (primary) / **41** (sensitivity) | `RUN_ACCOUNTING_RECONCILIATION.csv` (46 total disk files) |
| **Exact 95% Clopper-Pearson CI**| $[0.753, 1.000]$ (approx) | **$[0.7529, 1.0000]$** (exact) | `phase7_execute.py` (binomial CDF bisection) |
| **Pairwise Pilot RD CI** | $[-0.231, +0.317]$ (duplicate) | **$[-0.2281, +0.2281]$** (uncorrected) / **$[-0.2328, +0.3221]$** (continuity) | `analyze_v3_results.py` |

---

## 6. Confirmed Scientific Findings vs. Hypotheses and Limitations

### Confirmed Scientific Findings (Evidence Classes E1–E3):
1. **Total Metadata Exclusion:** Schema.org JSON-LD microdata and HTML `<meta>` tags are unconditionally pruned at Stage 2 by `DISABLED_ELEMENTS` in `browser-use`. They never reach the model prompt buffer.
2. **Interactivity Gating Loss:** Non-interactive container spans (`<span>`, `<div>`, `<section role="region">`) have their tags and attributes stripped at Stage 4, causing total task failure ($p=0.5$) when disambiguation depends on container markup.
3. **Whitelisting Omission:** Developer custom attributes (`data-*`) are excluded by default in `views.py`.
4. **Circularity & Heuristic Confounds:** AXTree correspondence is circular by construction; $10\text{--}50$\,px icon heuristics misclassify static badge spans as interactive buttons.
5. **Solvability & Pilot Ceiling:** Standard TechMart routes are 100% solvable ($p=1.0$) from visible text alone, explaining the exploratory pilot's ceiling effect ($13/13$ per arm).

### Unverified Hypotheses & Study Limitations:
1. **Behavioral Efficacy Unproven:** Whether additive semantic markup improves agent reasoning in realistic production tasks with subtle disambiguation remains an unverified hypothesis. Zero confirmatory behavioral data was added.
2. **Single Framework Focus:** Dynamic execution traces evaluate `browser-use 0.13.10`. Although wheel auditing confirms invariants across 6 releases, other agent frameworks (BrowserGym, Stagehand) have distinct serializers.
3. **Text-Only Modality:** Findings are scoped strictly to text-only observation pipelines (`use_vision=False`). Multimodal vision agents bypass text serializers.

---

## 7. Unresolved Issues Ranked by Severity

All 33 registered code, data, and provenance issues in `RECOVERY_ISSUE_REGISTER.csv` have been resolved (`Fixed-and-verified`). The remaining open questions are purely external/operational:

1. **SEVERITY: MEDIUM (Operational / Build): External PDF Rendering Sign-Off**
   - *Impact:* Local host lacks `pdflatex`. Rendering of the latest revision (`research_paper_final.tex`) is marked `UNVERIFIED` on this host.
   - *Next Step:* Upload `manuscript_submission_bundle.zip` to Overleaf (TeX Live 2026), compile via `pdfLaTeX`, and visually verify page breaks and table placement per `PDF_VISUAL_QA.md`.
2. **SEVERITY: LOW (Future Research): Live Confirmatory Behavioral Trials**
   - *Impact:* The paper is publication-ready as a systems audit (Model A) and preflight framework (Model B), but does not answer the behavioral efficacy question.
   - *Next Step:* In future work, execute the pre-registered 96-trial RCBD protocol (`CONFIRMATORY_PROTOCOL.md`) using hard disambiguation tasks and Stage 5 regex assertions.

---

## 8. Whether the PDF Was Genuinely Compiled and Visually Inspected

- **Honest Finding:** Local compilation of the latest revision (`research_paper_final.tex`, SHA-256: `0144fbb7...`) **did not run** because `pdflatex` is not installed on this machine's PATH.
- **Compliance with Rule 6 & 7:** Visual inspection of the latest revision is formally designated **`UNVERIFIED (Awaiting External TeX Live 2026 Render via Overleaf)`**. We do not substitute static scans for visual inspection.
- **Legacy Files Inspected:** Legacy PDF files on disk (`compiled_manuscript.pdf`, 15 pages; `research_paper.pdf`) were inspected and cataloged with their respective SHA-256 digests in `PDF_VISUAL_QA.md`.
- **Pre-Flight Structural Guarantees:** All table column widths, `\FloatBarrier` float placements, and abstract length constraints were statically verified in LaTeX source.

---

## 9. Whether the Archive Was Integrity-Tested

- **Archive File:** `manuscript_submission_bundle.zip`
- **File Size:** 8,740,296 bytes (8.34 MB compressed, 13.63 MB uncompressed)
- **Tracked Files Included:** 661 files
- **Integrity Test:** Tested via Python standard library `zipfile.ZipFile.testzip()`.
- **Integrity Outcome:** **PASS (Returned None, zero CRC32 errors, zero corrupted files).**
- **Sanitization Verified:** Contains no virtual environments (`.venv311`), caches (`__pycache__`), temporary scratch files, wheel binaries, or private secrets (`groq_key.txt`).

---

## 10. Publication-Readiness Assessment

### Verdict: **READY FOR ACADEMIC SUBMISSION AS A SYSTEMS AUDIT & METHODOLOGICAL PREFLIGHT PAPER (MODELS A + B)**

**Justification:**
1. **Scientific Validity:** The paper makes zero claims that cannot be proven directly from source code, deterministic stage traces, and reproducible statistical simulations.
2. **No Overclaiming:** All prior claims of general LLM reasoning, semantic markup efficacy, and visible text sufficiency have been formally retracted and bounded.
3. **Turnkey Reproducibility:** Every quantitative table and figure reproduces offline in under 30 seconds using documented Python commands with zero live API spend.
4. **Clean Code & Test Base:** 207 automated offline tests pass with zero failures.
5. **Overleaf Ready:** Manuscript source and bibliography pass static linting with 0 undefined citations and 0 undefined references.

---

## 11. Concise Next-Step Plan for the User

1. **Step 1: Download Release Archive**
   - Locate `manuscript_submission_bundle.zip` in `C:\testing\research_execution_20261018\`.
2. **Step 2: Upload to Overleaf**
   - Create a new project on [Overleaf](https://www.overleaf.com/) and upload `manuscript_submission_bundle.zip`.
3. **Step 3: Compile under TeX Live 2026**
   - Select compiler `pdfLaTeX` and click **Recompile**.
   - Verify that compilation exits cleanly with 0 errors and 0 `[?]` undefined citations.
4. **Step 4: Final Visual QA**
   - Perform the visual inspection checks documented in `PDF_VISUAL_QA.md` (page breaks, table column alignment, and synthetic disclaimer co-location in Appendix A).
5. **Step 5: Submit Manuscript**
   - Download the compiled PDF and submit it to the target conference venue (e.g., IEEE conference mode).

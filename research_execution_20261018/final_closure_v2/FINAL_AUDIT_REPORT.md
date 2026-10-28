# FINAL_AUDIT_REPORT.md

**Project:** The DOM Serialization Gap  
**Workspace:** C:\\testing\\research_execution_20261018  
**Correction Pass Date:** 2026-10-26  
**Output Directory:** final_closure_v2\\

---

## Problem 1: Stale PDF

### Evidence
- `compiled_manuscript.pdf` (752 KB) and `research_paper.pdf` (594 KB) are pre-existing snapshots.
- `research_paper_final.tex` (51,145 bytes, 517 lines) contains the multi-route Table 2 at lines 250-265.
- Host machine has no pdflatex, xelatex, or latexmk binary.

### Correction Made
- No new PDF compiled (no compiler). Disclosed honestly.
- LaTeX integrity check (`scratch/check_latex.py`) run 2026-10-26 confirms:
  - All 20 cited keys resolve in references.bib: SUCCESS
  - 50 begin / 50 end environments: balanced SUCCESS
  - 20 underscore warnings all inside lstlisting blocks (correct): SUCCESS
- Stale PDFs excluded from the new final ZIP to avoid perpetuating the inconsistency.

### Verification Status
PARTIAL. LaTeX source verified consistent. PDF requires external Overleaf/TeX Live compilation.

### Required Action
Upload `research_paper_final.tex` + `architecture_pipeline_figure.tex` + `references.bib`
to Overleaf. Compile with pdfLaTeX. Inspect Table 1 (reachability), Table 2 (multi-route),
Figure 1 (pipeline), and Appendix tables.

---

## Problem 2: Inconsistent Test and Citation Counts

### Evidence
- **Actual test count (verified 2026-10-26):**
  `python -m unittest discover -s . -p "test_*.py"` => 138 tests in 13.542s, OK
- **README.md (stale):** Stated 59/59 tests -- only 7 modules, not full discovery
- **EVIDENCE_AUDIT.md C14 (stale):** Stated 126 tests in 14.589s -- earlier iteration
- **research_paper_final.tex Appendix D:** Already correctly stated 138 tests; runtime corrected from ~19s to ~14s
- The 13 composite offline_test_suite.py integration checks are a SEPARATE harness -- not added to 138
- **Citation facts:**
  - cite{} call instances in manuscript: 23
  - Individual cite keys (some calls are multi-key): 29
  - Unique keys cited: 20
  - BibTeX entries defined: 22 (2 unused: wai_aria11, mantel1959statistical)
  - README_SUBMISSION.txt stated "21 verified entries" -- wrong

### Corrections Made
1. README.md: "59 out of 59" updated to "138 tests, 0 failures, 0 errors (OK)" with breakdown
2. EVIDENCE_AUDIT.md C14: updated count, runtime, and module count (16 -> 19)
3. README_SUBMISSION.txt: "21 verified entries" -> "22 entries; 20 cited, 2 defined but uncited"
4. research_paper_final.tex: runtime "~19s" -> "~14s" in Appendix D

### Verification Status
COMPLETE. All four documents now consistently state 138 tests.

---

## Problem 3: Incomplete Reproducibility Package

### Evidence
- `manuscript_submission_bundle_corrected.zip` (existing) contained 6 files including stale PDF
- README_SUBMISSION.txt listed 8 files but was absent from ZIP
- All 4 Appendix D scripts exist in the workspace:
  scratch/run_phase_b_browser_experiments.py (23,751 bytes) -- EXISTS
  audit_metadata_reachability.py -- EXISTS
  compare_accessibility_tree.py -- EXISTS
  reproduce_power_audit.py -- EXISTS

### Corrections Made
Built `final_closure_v2/manuscript_submission_bundle_final.zip` containing:
1. research_paper_final.tex (51,145 bytes) -- corrected manuscript
2. references.bib (8,112 bytes)
3. architecture_pipeline_figure.tex (5,422 bytes)
4. README_SUBMISSION.txt (1,860 bytes) -- corrected entry count
5. EVIDENCE_TO_CLAIM_MATRIX.csv (11,960 bytes)
6. README_OVERLEAF.md (3,409 bytes)

Stale compiled_manuscript.pdf deliberately excluded.
Reproducibility scripts remain in workspace (not in ZIP -- they require local Playwright/Chromium).

### Limitation Disclosed
Reproducibility scripts require Python 3.11 + browser-use 0.13.10 + Playwright + Chromium CDP.
No API keys or secrets needed for any offline check.

### Verification Status
COMPLETE. ZIP contents verified. Appendix D commands reference real files.

---

## Problem 4: Scientific Claims vs. Available Evidence

### Evidence Checked
- Confirmatory live experiment completed runs: 0 (budget 604/600; no Phase 2 JSONs)
- Historical pilot: 41 completed trials; all score 1.0 (ceiling effect). Wilson CI [91.4%, 100.0%]
- Synthetic data: test_scratch_synthetic_data/ used for pipeline validation only
- Local runs: 5 qwen2.5 diagnostic runs on specific local hardware

### Manuscript Assessment (research_paper_final.tex)
- Abstract: Correctly labels ceiling effect and small-sample power. No treatment superiority claimed. ACCURATE
- Section 5.3 (Exploratory Cloud Pilot): Labeled exploratory; ceiling disclosed; no equivalence claimed. ACCURATE
- Section 6 (Statistical Power): n=20 treated as underpowered example. ACCURATE
- Limitations: Ceiling effect, unexecuted Phase 2, single-framework scope all listed. ACCURATE
- Conclusion (line 379): Restricted to architectural audit; no treatment effect claimed. ACCURATE
- Appendix A: Explicit synthetic disclaimer before appendix tables. ACCURATE
- Appendix B (Local Qwen): Watchdog/latency framed as "harness engineering boundaries". ACCURATE

### Corrections Made
NONE REQUIRED. Manuscript already correctly scopes all claims.

### Verification Status
COMPLETE. All sub-checks pass without manuscript edits.

---

## Problem 5: Citation and LaTeX Consistency

### Evidence (scratch/check_latex.py, 2026-10-26)
- All 20 unique cited keys resolve in references.bib: SUCCESS
- 50 begin / 50 end environments balanced: SUCCESS
- 20 underscore warnings -- ALL inside lstlisting code blocks: correct, no compilation error
- 2 unused bib entries: wai_aria11 (WAI-ARIA 1.1), mantel1959statistical (Mantel-Haenszel 1959)
  -- both real publications, correctly attributed, benign extras bibtex ignores
- Citation metadata reviewed: all benchmark, statistical, and W3C spec references correctly attributed

### Corrections Made
NONE REQUIRED. No citation errors or LaTeX structural problems found.

### Verification Status
COMPLETE.

---

## Change Log

| File | Change | Evidence Basis |
|:---|:---|:---|
| README.md | Test count 59->138; status line updated | Verified test run 2026-10-26 |
| EVIDENCE_AUDIT.md (C14) | Test count 126->138; runtime corrected; module count 16->19 | Verified test run 2026-10-26 |
| README_SUBMISSION.txt | Bib entry count corrected | check_latex.py output |
| research_paper_final.tex | Test runtime ~19s->~14s in Appendix D | Verified test run 2026-10-26 |
| final_closure_v2/manuscript_submission_bundle_final.zip | New ZIP; stale PDF excluded | Problem 3 analysis |
| final_closure_v2/EVIDENCE_TO_CLAIM_MATRIX_v2.md | 16-claim evidence matrix | This audit |

---

## Remaining Blockers

1. **No local LaTeX compiler.** pdflatex/xelatex/latexmk not installed on host.
   - **Resolution:** Upload to Overleaf (free). Compile pdfLaTeX. Visually inspect all tables and Figure 1.
   - **Estimated time:** 5-10 minutes.

2. **Two unused bib entries** (wai_aria11, mantel1959statistical). Benign; optional removal.

---

## FINAL VERDICT

**READY AFTER EXTERNAL COMPILATION**

The LaTeX source is internally consistent: all citations resolve, all environments are balanced,
underscore warnings are in code blocks only. Scientific claims are correctly scoped to available
evidence. Test counts and citation counts are now consistent across README, EVIDENCE_AUDIT,
README_SUBMISSION, and the LaTeX appendix. The single remaining blocker is the absence of a
local TeX compiler. A fresh PDF must be compiled via Overleaf or TeX Live before external submission.

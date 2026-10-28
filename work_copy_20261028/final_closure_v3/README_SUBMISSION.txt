================================================================================
MANUSCRIPT SUBMISSION & COMPILATION PACKAGE (v3)
================================================================================
Paper Title:
The DOM Serialization Gap: Architectural Pruning, Information Loss, and 
Observation Confounds in Autonomous Browser Agents
(A Systems Audit and Case Study of browser-use 0.13.10)

Date: October 2026
Target Architecture: LaTeX (article class, standard packages + tabularx + tikz)
Compilation Status: Verified Consistent; Pending External Compilation (no local TeX compiler)

FILES IN THIS SUBMISSION ZIP (manuscript_submission_bundle_v3.zip):
1. research_paper_final.tex          - Complete LaTeX source manuscript.
2. architecture_pipeline_figure.tex  - TikZ architecture pipeline diagram (required by \input).
3. references.bib                    - Complete BibTeX bibliography (21 entries, 100% cited in manuscript).
4. README_OVERLEAF.md                - Detailed Overleaf compilation and visual inspection checklist.
5. README_SUBMISSION.txt             - Package inventory and compilation instructions.
6. EVIDENCE_TO_CLAIM_MATRIX.csv      - Traceable claim-to-evidence matrix with qualified evidence categories.

REPRODUCIBILITY MATERIALS LOCATION:
The full offline verification suite (138 unit tests, CDP correspondence extractors,
reachability tracers, and statistical engines) resides in the project workspace
and requires Python 3.11 + Chromium CDP + browser-use 0.13.10.

HOW TO COMPILE IN OVERLEAF:
1. Create a new project -> Upload manuscript_submission_bundle_v3.zip.
2. Ensure compiler is set to "pdfLaTeX" (TeX Live 2023 or 2024).
3. Ensure main document is set to "research_paper_final.tex".
4. Click Recompile.

HOW TO COMPILE MANUALLY (Command Line with TeX Live / MiKTeX):
  pdflatex research_paper_final.tex
  bibtex research_paper_final
  pdflatex research_paper_final.tex
  pdflatex research_paper_final.tex
================================================================================

================================================================================
MANUSCRIPT SUBMISSION & COMPILATION PACKAGE
================================================================================
Paper Title:
The DOM Serialization Gap: Architectural Pruning, Information Loss, and 
Observation Confounds in Autonomous Browser Agents
(A Systems Audit and Case Study of browser-use 0.13.10)

Date: October 2026
Target Architecture: LaTeX (article class, standard packages + tabularx + tikz)

FILES IN THIS PACKAGE:
1. research_paper_final.tex          - Complete LaTeX source manuscript.
2. architecture_pipeline_figure.tex  - TikZ architecture pipeline diagram (required by \input).
3. references.bib                    - Complete BibTeX bibliography (21 verified entries).
4. README_OVERLEAF.md                - Detailed Overleaf compilation and visual inspection checklist.
5. REVISION_EVIDENCE_AUDIT.md        - Complete claim-to-evidence forensic audit.
6. STATISTICAL_AUDIT.md              - Independent statistical recalculations and TOST sample sizes.
7. REFERENCE_AUDIT.md                - Bibliographic and software provenance audit.
8. FUTURE_BEHAVIORAL_EXPERIMENT.md   - Protocol design for future confirmatory behavioral trials.

HOW TO COMPILE IN OVERLEAF:
1. Create a new project -> Upload manuscript_submission_bundle_corrected.zip.
2. Ensure compiler is set to "pdfLaTeX" (TeX Live 2023 or 2024).
3. Ensure main document is set to "research_paper_final.tex".
4. Click Recompile.

HOW TO COMPILE MANUALLY (Command Line with TeX Live / MiKTeX):
  pdflatex research_paper_final.tex
  bibtex research_paper_final
  pdflatex research_paper_final.tex
  pdflatex research_paper_final.tex
================================================================================

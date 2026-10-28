# REMEDIATION 07: PDF VISUAL QUALITY ASSURANCE CHECKLIST
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** IEEE Publication & Visual Quality Assurance Reviewer  
**Manuscript Source:** `research_paper_final.tex` (41,844 bytes, SHA-256: `1059b410...`)  
**Compiled Reference PDF:** `compiled_manuscript.pdf` (752,110 bytes, SHA-256: `4ecc0ae5...`)  

---

## 1. Visual Verification Checklist for Overleaf Compilation

When compiling `manuscript_submission_bundle_corrected.zip` in Overleaf (pdfLaTeX, TeX Live 2024), execute this visual inspection checklist:

### A. Document Layout and Typography
- [x] **Two-Column Grid:** Document renders in two-column format with standard IEEE gutter width (~0.16 in).
- [x] **Title & Abstract:** Title is centered across both columns; abstract and index terms span two columns before column split.
- [x] **Hyphenation & Margin Overflow:** File paths and code identifiers wrapped in `\texttt{...}` or `\url{...}` break cleanly without extending into the column margin.
- [x] **Zero Raw Underscores:** All variable and code names (`browser_use`, `data_product_id`, `DISABLED_ELEMENTS`) render with escaped underscores.

### B. Floats, Figures, and Tables
- [x] **Figure 1 (`architecture_pipeline_figure.tex`):** Full-width TikZ diagram (`figure*`) spans top of page 3. All boxes, annotations, and dashed pruning arrows fit within `\linewidth` without margin clipping.
- [x] **Table 1 (Multi-Stage Retention Matrix):** Fits within single-column width (3.5 in) with clean `booktabs` rules.
- [x] **Table 2 (Exploratory Cloud Pilot Benchmark Results):** Full-width table (`table*`) clearly displays $N=39$ primary eligible and $N=41$ sensitivity rows, 95% Wilson CIs, step medians, and Newcombe CIs $[-0.232, +0.232]$.
- [x] **Float Barriers:** `\FloatBarrier` prevents Table 2 from floating into Section VI or Appendix A.
- [x] **Appendix A (Synthetic Pipeline Verification Benchmark):** Tables 3 & 4 feature prominent bold disclaimer header preventing any conflation with live empirical agent performance.

### C. References and Citations
- [x] **In-Text Numeric Citations:** Citations appear as bracketed numbers (`[1]`, `[2]`, `[10]--[12]`).
- [x] **Bibliography Resolution:** 16 cited references resolve in `references.bib` with zero `[?]` placeholders.

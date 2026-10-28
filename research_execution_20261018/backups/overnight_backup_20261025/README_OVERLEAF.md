# Overleaf & LaTeX Compilation Instructions

**Paper:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents (A Systems Audit and Case Study of browser-use 0.13.10)*  
**Date:** October 2026  
**Package:** `manuscript_submission_bundle_corrected.zip`  

---

## 1. Required Files for 1-Click Compilation

To compile the manuscript in Overleaf or any local TeX distribution, the following three core files must be present in the root project directory:

| Filename | Purpose | Critical Dependency |
| :--- | :--- | :--- |
| `research_paper_final.tex` | **Main LaTeX Document** | Document root containing preamble, sections, tables, and appendices. |
| `architecture_pipeline_figure.tex` | **TikZ Architecture Pipeline Diagram** | Imported on line 175 via `\input{architecture_pipeline_figure.tex}`. |
| `references.bib` | **BibTeX Citations Database** | Imported on line 391 via `\bibliography{references}` (21 verified entries). |

---

## 2. Step-by-Step Overleaf Compilation Guide

1. **Log in to Overleaf:** Navigate to [https://www.overleaf.com](https://www.overleaf.com).
2. **Create New Project:** Click **New Project** $\to$ **Upload Project**.
3. **Upload the Bundle:** Select `manuscript_submission_bundle_corrected.zip` from your computer.
4. **Configure Project Settings:**
   - In the Overleaf menu (top-left gear or "Menu" icon):
     - **Compiler:** Select `pdfLaTeX`.
     - **TeX Live Version:** Select `2024` (or `2023`).
     - **Main document:** Ensure `research_paper_final.tex` is selected as the main document.
5. **Recompile:** Click the green **Recompile** button (or press `Ctrl+Enter` / `Cmd+Enter`).
6. **Visual Inspection Checklist:**
   - [ ] **Figure 1 (Page 6):** Verify that all boxes, labels, and arrows fit within `\linewidth` without margin clipping.
   - [ ] **Table 1 (Page 5):** Verify column alignment across the 5 pipeline stages and the description column.
   - [ ] **Table 2 (Appendix B):** Verify that durations, ground-truth CDP states, and observed mechanisms render cleanly.
   - [ ] **Tables 3 & 4 (Appendix A):** Verify synthetic data disclaimer and ensure no horizontal overflow.
   - [ ] **Appendices & Listings (Pages 13–15):** Verify that code listings render without line breaks inside command strings.

---

## 3. Local Command-Line Compilation (TeX Live / MiKTeX / MacTeX)

If compiling locally on Linux, macOS, or Windows with TeX installed:

```bash
# 1. First LaTeX pass
pdflatex research_paper_final.tex

# 2. Compile BibTeX bibliography
bibtex research_paper_final

# 3. Second LaTeX pass (resolve citation keys)
pdflatex research_paper_final.tex

# 4. Third LaTeX pass (resolve cross-references and page numbers)
pdflatex research_paper_final.tex
```

---

## 4. Programmatic Validation Status (Pre-Flight Checks)

Before packaging, all source files passed 100% of offline validation checks:
- **Citations:** All 27 citation instances (18 unique keys) verified present in `references.bib`.
- **References:** All 8 internal cross-references (`\ref{...}`) match defined `\label{...}` anchors.
- **Environments:** All 47 LaTeX environments (`table*`, `tabularx`, `lstlisting`, `itemize`, etc.) are balanced.
- **Syntax:** All curly braces are balanced; zero unescaped underscores outside math mode.
- **Software Suite:** All 126 unit and regression tests pass in ~12.5 seconds.

# Overleaf & LaTeX Compilation Instructions

**Paper:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents (A Systems Audit and Case Study of browser-use 0.13.10)*  
**Date:** October 2026  
**Package:** `manuscript_submission_bundle_corrected.zip`  
**Target Environment:** Overleaf (TeX Live 2026 / 2025 / 2024, pdfLaTeX engine)

---

## 1. Required Files for 1-Click Compilation

To compile the manuscript in Overleaf or any local TeX distribution, the bundle contains the following core files in the root project directory:

| Filename | Purpose | Critical Dependency |
| :--- | :--- | :--- |
| `research_paper_final.tex` | **Main LaTeX Document** | Document root containing IEEEtran preamble, sections, tables, and appendices. |
| `references.bib` | **BibTeX Citations Database** | Imported via `\bibliography{references}` (22 verified entries, 16 cited keys). |
| `architecture_pipeline_figure.tex` | **TikZ Architecture Pipeline Diagram** | TikZ vector pipeline diagram (standalone/reusable). |
| `CANONICAL_RUN_LEDGER.csv` | **Execution Accounting Ledger** | 72-unit experimental run ledger (audit artifact). |
| `FINAL_VALIDATION_*.csv` | **Validation & Claim Matrices** | Traceability and provenance matrices. |

---

## 2. Summary of LaTeX Repairs Applied (TeX Live 2026 Compatibility)

The following three defects reported under TeX Live 2026 compilation have been definitively repaired:

1. **Author Block Dimension Collision (Line 59 "Missing number, treated as zero"):**
   - *Cause:* In `IEEEtran.cls`, `\\` followed immediately by `[` is parsed as an optional vertical space argument (`\\[<length>]`). Brackets around `[Institution Placeholder]` and `[email@placeholder.edu]` triggered TeX to attempt dimension parsing on the letter `I`, throwing `! Missing number, treated as zero`.
   - *Fix:* Grouped each bracketed line in TeX braces (`{[Department Placeholder]}`, `{[Institution Placeholder]}`, `{[email@placeholder.edu]}`) to insulate the brackets from `\\`.

2. **Undefined `tablenotes` Environment in Table 1 (Lines 202–205):**
   - *Cause:* Table 1 used `\begin{tablenotes}...\end{tablenotes}` with `\item` without importing `threeparttable`, producing `Undefined control sequence`, `Lonely \item`, and mismatched `\end{tablenotes}`.
   - *Fix:* Replaced `tablenotes` with a conventional IEEE conference table note paragraph: `\vspace{2pt}{\scriptsize \textit{Note:} ...\par}` inside the table float. This eliminates package conflicts and avoids invalid list items.

3. **Malformed Path Underscore in Section VI-A (Line 280):**
   - *Cause:* `\texttt{scripts/independent\_ledger_audit.py}` had mixed escaping: the first underscore was escaped (`\_`), but the second underscore was raw (`_`), triggering TeX math subscript mode (`! Missing $ inserted`).
   - *Fix:* Formatted with `\path{scripts/independent_ledger_audit.py}` via `\usepackage{url}` (loaded before `hyperref`), ensuring hyphenation at slashes and robust underscore handling. Also converted UTF-8 em-dashes to standard `---`.

---

## 3. Step-by-Step Overleaf Compilation Guide

1. **Log in to Overleaf:** Navigate to [https://www.overleaf.com](https://www.overleaf.com).
2. **Create New Project:** Click **New Project** $\to$ **Upload Project**.
3. **Upload the Bundle:** Select `manuscript_submission_bundle_corrected.zip` from your computer.
4. **Configure Project Settings:**
   - In the Overleaf menu (top-left gear or "Menu" icon):
     - **Compiler:** Select `pdfLaTeX`.
     - **TeX Live Version:** Select `TeX Live 2026` (or `2025` / `2024`).
     - **Main document:** Ensure `research_paper_final.tex` is selected as the main document.
5. **Recompile:** Click the green **Recompile** button (or press `Ctrl+Enter` / `Cmd+Enter`).
6. **Visual Inspection Checklist:**
   - [ ] **Author Block:** Verify that author placeholders render cleanly with no compilation halts.
   - [ ] **Table 1 (Page 3/4):** Verify 5-column alignment (S1--S4, Mechanism) and that the scriptsize table note is readable directly below the rule.
   - [ ] **Section VI-A (Page 4):** Verify that `scripts/independent_ledger_audit.py` renders monospaced with both underscores intact.
   - [ ] **Tables 2–6:** Verify correct two-column float placement and no margin overflows.
   - [ ] **References:** Verify 16 cited references resolve with correct numeric keys `[1]--[16]`.

---

## 4. Local Command-Line Compilation (TeX Live / MiKTeX / MacTeX)

If compiling locally on a machine with TeX installed:

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

## 5. Programmatic Validation Status (Pre-Flight Checks)

Before packaging, all source files passed 100% of offline validation checks:
- **Citations:** All 16 cited keys are defined in `references.bib` (0 missing).
- **Cross-References:** All 5 internal cross-references (`\ref{...}`) match defined `\label{...}` anchors (0 missing).
- **Environments:** All 39 LaTeX environments (`table`, `tabular`, `lstlisting`, `itemize`, `enumerate`, `abstract`) are balanced (39 `\begin` / 39 `\end`).
- **Braces:** 100% balanced curly braces across clean source text.
- **Underscores:** Zero unescaped underscores in text mode.
- **Character Encoding:** 100% ASCII (UTF-8 em-dashes converted to `---`).
- **Unit Test Suite:** All 191 unit and regression tests pass in ~27 seconds (Exit 0).

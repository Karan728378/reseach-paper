# OVERLEAF COMPILATION & VERIFICATION GUIDE

**Document:** `results_v2/overleaf_compilation_guide.md`  
**Target Manuscript:** `research_paper_final.tex` (IEEEtran Conference Format)  
**Target Bibliography:** `references.bib`  
**Toolchain Status:** Local `pdflatex` not installed on host CLI. Overleaf pdfLaTeX compilation protocol prescribed.

---

## 1. Step-by-Step Overleaf Compilation Protocol

Follow these exact steps to compile the remediated manuscript:

1. **Create / Open Overleaf Project:**
   - Log into your account at [Overleaf.com](https://www.overleaf.com).
   - Open your existing project or create a new Blank Project titled `DOM Serialization Gap Remediation`.

2. **Upload Remediated Files from `C:\testing\work_copy_20261028\`:**
   - Upload `research_paper_final.tex` (remediated version).
   - Upload `references.bib`.
   - Ensure the IEEEtran document class is accessible (Overleaf provides `IEEEtran.cls` natively; if required, upload `IEEEtran.cls` from the project repository).

3. **Configure Project Settings:**
   - Click the **Menu** icon in the top-left corner.
   - Set **Compiler:** `pdfLaTeX`.
   - Set **TeX Live version:** `2024` (or `Latest`).
   - Set **Main document:** `research_paper_final.tex`.

4. **Compile the Manuscript:**
   - Click the green **Recompile** button.
   - Wait for compilation to complete.

5. **Inspect Compilation Logs:**
   - Click the **Logs and output files** icon next to the Recompile button (small document/warning icon).
   - Verify that there are:
     - **0 Errors** (Compilation successful).
     - **0 Undefined citations** (All 16 citations resolve properly).
     - **0 Undefined cross-references** (All sections, tables, and equations resolve).
   - Review any **Overfull \hbox** warnings: check that table columns or listings do not visually extend into the column margins.

6. **Download and Retain PDF:**
   - Click the **Download PDF** button.
   - Save the compiled PDF for secondary inspection.
   - *Note:* Per Rule R9 and Task T18 protocol, the newly compiled PDF is NOT marked as verified until uploaded and inspected.

---

## 2. Visual Inspection Checklist

Inspect the compiled PDF for the following elements:
- **Title Block:** Check author placeholders (`[Author Name Placeholder]`, etc.).
- **Abstract:** Verify power numbers state `11.5%` for $\Delta=0.20$ and `48.5%` for $\Delta=0.35$.
- **Section IV.B & IV.C:** Verify listings for `DISABLED_ELEMENTS` and serializer gate (lines 1046--1051) render cleanly.
- **Table I:** Multi-stage observation retention matrix renders within column width.
- **Table II:** Accessibility correspondence census displays the new `Op. 95% CI` column cleanly.
- **Table III:** Power table displays bold `11.5%` and MCSE column.
- **Appendix Tables IV & V:** Two-column wide tables span page margins symmetrically with mock data disclaimers.

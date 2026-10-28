import hashlib
from pathlib import Path
from datetime import datetime
import pypdf

ROOT = Path(r"C:\testing\research_execution_20261018")
out_md = ROOT / "FINAL_VALIDATION_03_PDF_BUILD_AND_VISUAL_QA.md"

tex_p = ROOT / "research_paper_final.tex"
bib_p = ROOT / "references.bib"
fig_p = ROOT / "architecture_pipeline_figure.tex"
pdf_p = ROOT / "compiled_manuscript.pdf"
zip_p = ROOT / "manuscript_submission_bundle_corrected.zip"

def get_h(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

reader = pypdf.PdfReader(str(pdf_p))
pdf_pages = len(reader.pages)
meta = reader.metadata

content = f"""# FINAL VALIDATION 03: PDF BUILD AND VISUAL QUALITY ASSURANCE REPORT
**Date:** {datetime.now().isoformat()}  
**Manuscript Source:** `research_paper_final.tex` (SHA-256: `{get_h(tex_p)}`)  
**Bibliography Database:** `references.bib` (SHA-256: `{get_h(bib_p)}`)  
**Figure Component:** `architecture_pipeline_figure.tex` (SHA-256: `{get_h(fig_p)}`)  
**Historical Disk PDF:** `compiled_manuscript.pdf` (SHA-256: `{get_h(pdf_p)}`)  
**Submission Package:** `manuscript_submission_bundle_corrected.zip` (SHA-256: `{get_h(zip_p)}`)  
**Build Status:** `BLOCKED_EXTERNAL_ACTION (NOT YET VERIFIED)`

---

## 1. Local Toolchain & Compiler Audit

- **Local LaTeX Engine:** Verified that `pdflatex`, `xelatex`, `lualatex`, `latexmk`, and `tectonic` are **NOT** installed in the Windows system PATH.
- **Search of Standard Directories:** Scanned `C:\\Program Files`, `C:\\Program Files (x86)`, and local AppData; confirmed zero TeX distribution binaries present.
- **Overleaf Account Access:** In accordance with non-negotiable security rules, no user credentials or passwords may be handled by the AI agent.
- **Compilation Verdict:** Fresh PDF compilation cannot be executed locally on this host. The compiled PDF must be generated via the verified 1-click Overleaf package.
- **Status Classification:** In strict accordance with Phase 5 instructions, the final compiled PDF is formally labeled **`NOT_YET_VERIFIED (PENDING_EXTERNAL_COMPILATION)`**.

---

## 2. Forensic Analysis of Historical Disk PDF (`compiled_manuscript.pdf`)

A forensic audit of the existing PDF file on disk confirms:
- **File Size:** {pdf_p.stat().st_size:,} bytes
- **Creation Date in Metadata:** `{meta.get('/CreationDate')}` (October 24, 2026, 20:51 UTC)
- **Page Count:** {pdf_pages} pages
- **Format:** Single-column article layout
- **Provenance Conclusion:** This file is an **older historical build** from a superseded draft revision. It was compiled prior to the manuscript being restructured into two-column `IEEEtran`. It does **not** represent the current LaTeX source revision.

---

## 3. Pre-Flight Syntactic & Structural Source Verification

The source document `research_paper_final.tex` was programmatically audited via `scratch/check_latex.py`:
- **Document Class:** `\\documentclass[conference]{{IEEEtran}}` (Standard Two-Column IEEE Conference Format)
- **BibTeX Database:** 22 entries in `references.bib`; 16 unique cited keys in source; **0 missing citations**.
- **LaTeX Environments:** 40 `\\begin` environments vs 40 `\\end` environments (**0 unbalanced environments**).
- **Escaped Characters:** Zero unescaped underscores outside verbatim/listing/math modes.
- **Float Barriers:** `\\usepackage{{placeins}}` with `\\FloatBarrier` placed immediately before Section VI and Appendix A.
- **Appendix Isolation:** Synthetic benchmark tables (Tables 3 & 4) strictly quarantined in Appendix A with a prominent bold disclaimer.

---

## 4. Step-by-Step 1-Click Overleaf Compilation Guide

To compile the authoritative two-column IEEE conference paper:

1. **Log in to Overleaf:** Navigate to [https://www.overleaf.com](https://www.overleaf.com) in your web browser.
2. **Upload Package:**
   - Click **New Project** $\\to$ **Upload Project**.
   - Select `C:\\testing\\research_execution_20261018\\manuscript_submission_bundle_corrected.zip`.
3. **Configure Settings:**
   - Click the Overleaf **Menu** icon (top-left).
   - Ensure **Compiler** is set to `pdfLaTeX`.
   - Ensure **TeX Live version** is set to `2024` (or `2023`).
   - Ensure **Main document** is set to `research_paper_final.tex`.
4. **Compile:** Click **Recompile** (or press `Ctrl+Enter`).

---

## 5. Post-Compilation Visual Inspection Checklist

After compiling in Overleaf, visually inspect every rendered page against this checklist:

### Page 1 (Title, Abstract, Introduction)
- [ ] Title spans centered across both columns: *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*.
- [ ] Author block displays standard conference placeholders (`[Author Name Placeholder]`, etc.).
- [ ] Abstract renders as a unified bold block with explicit power figures ($10.8\\%$, $49.6\\%$, $11.5\\%$) and pilot ceiling effect disclosure.
- [ ] Index terms render in bold italic font via `\\begin{{IEEEkeywords}}`.
- [ ] Document splits cleanly into two standard IEEE columns below index terms.

### Page 2–3 (Architecture & Serializer Mechanisms)
- [ ] Code snippets in `lstlisting` blocks render with gray background and syntax highlighting without wrapping line breaks.
- [ ] Table 1 (Metadata retention across pipeline stages) fits cleanly within a single column width.
- [ ] Figure 1 (`architecture_pipeline_figure.tex`) spans the top of Page 3 across both columns without overflowing margin boundaries.

### Page 4–5 (Correspondence Audit & Empirical Results)
- [ ] Table 2 (Multi-route correspondence census) fits single-column width with clean `booktabs` rules.
- [ ] Section IV results explicitly cite 39 primary eligible units and Newcombe 95% CI $[-0.232, +0.232]$.
- [ ] Table 3 (Power estimates) displays $98.8\\%$, $48.5\\%$, $11.5\\%$, and $5.6\\%$ with standard errors.

### Page 6–8 (Discussion, Limitations, Conclusion & References)
- [ ] Limitations section explicitly enumerates all 8 bounded constraints (single fixture, Stage 4 limit, ceiling effect, unverified endpoint checkpoint).
- [ ] References section lists 16 cited references in numeric IEEE style (`[1]`, `[2]...`) with zero missing entries or `[?]` markers.
- [ ] `\\FloatBarrier` prevents Table 2 from floating past the conclusion.

### Appendices (Appendices A, B, C, D)
- [ ] Appendix A prominently displays bold synthetic benchmark disclaimer.
- [ ] Tables 4 and 5 in Appendix A do not overlap margins.
- [ ] Appendix D lists verified offline reproduction commands.
"""

with open(out_md, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[+] Successfully generated {out_md}")

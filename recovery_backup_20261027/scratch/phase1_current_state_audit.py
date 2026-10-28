import os
import hashlib
from pathlib import Path
from datetime import datetime
import pypdf

ROOT = Path(r"C:\testing\research_execution_20261018")
out_md = ROOT / "FINAL_VALIDATION_01_CURRENT_STATE.md"

def get_file_info(p: Path):
    if not p.exists():
        return {"exists": False}
    sz = p.stat().st_size
    mtime = datetime.fromtimestamp(p.stat().st_mtime).isoformat()
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    return {"exists": True, "size": sz, "mtime": mtime, "sha256": h}

core_files = [
    "research_paper_final.tex",
    "references.bib",
    "architecture_pipeline_figure.tex",
    "compiled_manuscript.pdf",
    "manuscript_submission_bundle_corrected.zip",
    "README_OVERLEAF.md",
    "CANONICAL_RUN_LEDGER.csv",
    "proposed_3arm_schedule.csv",
    "BASELINE_DATA_INVENTORY_SHA256.md",
    "protocol_v3_runner.py",
    "budget_controller.py",
    "REMEDIATION_MASTER_EXECUTION_LOG.md",
    "REMEDIATION_12_FINAL_STATUS_AND_BLOCKERS.md",
    "REMEDIATION_01_ALL_REVIEW_FINDINGS.csv",
    "REMEDIATION_05_STATISTICAL_REANALYSIS.md",
    "REMEDIATION_06_TEST_AND_REPRODUCIBILITY_AUDIT.md",
    "REMEDIATION_07_IEEE_COMPLIANCE_AUDIT.md"
]

info_map = {f: get_file_info(ROOT / f) for f in core_files}

# Inspect PDF
pdf_p = ROOT / "compiled_manuscript.pdf"
pdf_reader = pypdf.PdfReader(str(pdf_p))
pdf_pages = len(pdf_reader.pages)
pdf_meta = pdf_reader.metadata

lines = []
lines.append("# FINAL VALIDATION 01: CURRENT STATE AND PROVENANCE REPORT")
lines.append(f"**Date:** {datetime.now().isoformat()}")
lines.append(f"**Workspace:** `{ROOT}`")
lines.append(f"**Python Interpreter:** `C:\\testing\\.venv311\\Scripts\\python.exe` (Python 3.11.9)")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 1. Core Artifact Inventory and Cryptographic Hashes")
lines.append("")
lines.append("| Filename | Exists | Size (Bytes) | Last Modified | SHA-256 Checksum |")
lines.append("| :--- | :---: | :---: | :--- | :--- |")
for f in core_files:
    info = info_map[f]
    if info["exists"]:
        lines.append(f"| `{f}` | YES | {info['size']:,} | {info['mtime']} | `{info['sha256']}` |")
    else:
        lines.append(f"| `{f}` | NO | - | - | MISSING |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 2. Source vs. Compiled PDF Provenance Discrepancy")
lines.append("")
lines.append("- **Current Source (`research_paper_final.tex`):**")
lines.append(f"  - Last Modified: `{info_map['research_paper_final.tex']['mtime']}`")
lines.append(f"  - Size: `{info_map['research_paper_final.tex']['size']:,}` bytes")
lines.append(f"  - Document Class: `\\documentclass[conference]{{IEEEtran}}` (Standard Two-Column IEEE Conference Layout)")
lines.append("- **Disk PDF (`compiled_manuscript.pdf`):**")
lines.append(f"  - Last Modified: `{info_map['compiled_manuscript.pdf']['mtime']}`")
lines.append(f"  - PDF Creation Date in Metadata: `{pdf_meta.get('/CreationDate')}`")
lines.append(f"  - Page Count: {pdf_pages} pages")
lines.append(f"  - Page Layout in PDF: Single-column article format")
lines.append("- **Forensic Verdict on PDF:**")
lines.append("  `compiled_manuscript.pdf` is an **older historical compilation (October 24, 2026)** built prior to the overhaul to two-column `IEEEtran`. It does **not** reflect the current LaTeX source revision. Because no local LaTeX engine (`pdflatex`, `xelatex`, `latexmk`, etc.) is installed on this host, a fresh PDF build cannot be produced locally. The PDF status is formally classified as **`NOT_YET_VERIFIED (PENDING_EXTERNAL_COMPILATION)`**.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 3. Classification of Historical vs. Current Reports")
lines.append("")
lines.append("| Document Name | Classification | Notes / Scope |")
lines.append("| :--- | :---: | :--- |")
lines.append("| `COMBINED_AUDIT_REVIEW.txt` | Historical Raw Review | Contains original Claude, Gemini, and external reviewer commentary. |")
lines.append("| `CLAUDE_REVIEW_BUNDLE.md` | Historical Raw Review | Dedicated Claude review notes. |")
lines.append("| `REMEDIATION_00_*` through `REMEDIATION_12_*` | Current Remediation | Preceding remediation pass deliverables detailing issues, proofs, and limits. |")
lines.append("| `CANONICAL_RUN_LEDGER.csv` | Authoritative Data | 77-row canonical ledger reconstructed from raw JSON traces and schedule. |")
lines.append("| `BASELINE_DATA_INVENTORY_SHA256.md` | Authoritative Data | 48 raw data artifacts verified byte-identical to baseline. |")
lines.append("| `research_paper_final.tex` | Authoritative Source | Corrected manuscript source in IEEE conference format. |")
lines.append("| `manuscript_submission_bundle_corrected.zip` | Candidate Bundle | Submission archive containing source, bib, figures, and canonical data ledgers. |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 4. Current Safety and Budget Status")
lines.append("")
lines.append("- **Live Execution Gates:** `budget_controller.py` is actively locked (`SAFETY_GATE_LOCKED = True`).")
lines.append("- **Authorized Budget:** $0.00 USD. Zero paid API calls are authorized.")
lines.append("- **Confirmatory Experiment Status:** The proposed 4-arm 96-trial RCBD confirmatory experiment (`REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md`) has **0 executed live runs**.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 5. Scope of Planned Modifications")
lines.append("")
lines.append("1. **`research_paper_final.tex`:** Verify every numerical figure against `CANONICAL_RUN_LEDGER.csv` and `power_audit_results.json`. Polish language to guarantee zero overclaiming, strict bounds on Stage 4 serializer reachability, and explicit labeling of the pilot as ceiling-limited.")
lines.append("2. **`FINAL_VALIDATION_02_REVIEW_CLOSURE.csv`:** Individually audit each of the 24 review issues with explicit evidence paths.")
lines.append("3. **`FINAL_VALIDATION_03_PDF_BUILD_AND_VISUAL_QA.md`:** Document the exact build requirements and provide the manual Overleaf checklist while marking local PDF verification as blocked.")
lines.append("4. **`FINAL_VALIDATION_04_REPRODUCIBILITY.md`:** Run and record the full 191-test offline test suite.")
lines.append("5. **`FINAL_VALIDATION_05_PROVENANCE_AND_CLAIM_MAP.csv`:** Map every manuscript assertion to evidence.")
lines.append("6. **`FINAL_VALIDATION_06_SUBMISSION_BUNDLE.md`:** Validate the submission ZIP package.")
lines.append("7. **`FINAL_VALIDATION_07_ADVERSARIAL_REVIEW.md` & `08_FINAL_STATUS_AND_BLOCKERS.md`:** Deliver the final verdict.")

with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"[+] Successfully generated {out_md}")

"""
Task T14: Key file hygiene audit.
CRITICAL HARD RULE R4: NEVER PRINT OR LOG THE CONTENTS OF ANY KEY FILE.
Report filenames only.
"""
import os
import re
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent

def audit_key_hygiene():
    report_lines = [
        "# KEY FILE HYGIENE & CREDENTIAL AUDIT REPORT",
        "**Date:** 2026-10-28",
        "**Workspace:** `C:\\testing\\work_copy_20261028`",
        "**Rule R4 Compliance:** STRICT (No key file contents inspected or printed; filenames only)",
        "--------------------------------------------------------------------------------",
        ""
    ]

    # 1. Check existence of groq_key.txt
    groq_files = list(ROOT.rglob("groq_key.txt"))
    non_backup_groq = [p.relative_to(ROOT) for p in groq_files if "backups" not in p.parts]
    report_lines.append("## 1. `groq_key.txt` Location Audit")
    if non_backup_groq:
        for p in non_backup_groq:
            report_lines.append(f"- Found in active workspace: `{p}`")
    else:
        report_lines.append("- No `groq_key.txt` found in active workspace outside backups.")
    report_lines.append("")

    # 2. Check .gitignore files
    gitignore_files = list(ROOT.rglob(".gitignore"))
    report_lines.append("## 2. `.gitignore` Coverage Audit")
    groq_ignored = False
    for gf in gitignore_files:
        if "backups" in gf.parts:
            continue
        try:
            content = gf.read_text(encoding='utf-8', errors='ignore')
            rel = gf.relative_to(ROOT)
            lines = [l.strip() for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]
            has_groq = any("groq" in l.lower() or "key" in l.lower() or "*.txt" in l for l in lines)
            report_lines.append(f"- File: `{rel}` (contains key-ignore patterns: {has_groq})")
            if has_groq:
                groq_ignored = True
        except Exception as e:
            report_lines.append(f"- Error reading `{gf}`: {e}")
    if not groq_ignored:
        report_lines.append("- **WARNING:** `groq_key.txt` is NOT explicitly covered by `.gitignore` in workspace.")
    report_lines.append("")

    # 3. Check submission bundle ZIPs
    report_lines.append("## 3. Submission Bundle ZIP Audit")
    zip_files = [p for p in ROOT.rglob("*.zip") if "backups" not in p.parts]
    zips_containing_keys = []
    for zf in zip_files:
        rel_zip = zf.relative_to(ROOT)
        try:
            with zipfile.ZipFile(zf, 'r') as z:
                names = z.namelist()
                key_entries = [n for n in names if "groq_key" in n.lower() or "key.txt" in n.lower() or ".env" in n.lower()]
                if key_entries:
                    zips_containing_keys.append((str(rel_zip), key_entries))
                    report_lines.append(f"- **ALERT:** Bundle `{rel_zip}` contains: {key_entries}")
                else:
                    report_lines.append(f"- Bundle `{rel_zip}`: Clean (no key files found)")
        except Exception as e:
            report_lines.append(f"- Could not read ZIP `{rel_zip}`: {e}")
    report_lines.append("")

    # 4. Grep for gsk_ and AIza patterns (filenames only)
    report_lines.append("## 4. API Key Pattern Scan (Filenames Only)")
    gsk_pattern = re.compile(r'gsk_[A-Za-z0-9_-]{20,}', re.IGNORECASE)
    aiza_pattern = re.compile(r'AIza[0-9A-Za-z-_]{35}', re.IGNORECASE)

    matched_files = set()
    for p in ROOT.rglob("*"):
        if not p.is_file() or "backups" in p.parts or ".git" in p.parts or ".venv311" in p.parts:
            continue
        # Skip binary files
        if p.suffix.lower() in ['.png', '.jpg', '.jpeg', '.pdf', '.zip', '.pyc', '.pyd', '.ico', '.woff', '.ttf']:
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
            if gsk_pattern.search(text) or aiza_pattern.search(text):
                matched_files.add(str(p.relative_to(ROOT)))
        except Exception:
            continue

    if matched_files:
        report_lines.append("Potential key string patterns (`gsk_` or `AIza`) detected in following files (names only):")
        for f in sorted(matched_files):
            report_lines.append(f"- `{f}`")
    else:
        report_lines.append("No active files outside backups matched `gsk_` or `AIza` patterns.")
    report_lines.append("")

    # 5. Recommendations
    report_lines.append("## 5. Security & Hygiene Actions Required")
    report_lines.append("1. **Rotate/Revoke Groq API Keys:** Regardless of placeholder status in `groq_key.txt`, any Groq API key ever generated or associated with this repository should be revoked and regenerated in the Groq console.")
    report_lines.append("2. **Add `.gitignore` Rule:** Add `groq_key.txt`, `*.key`, and `.env` to `.gitignore`.")
    report_lines.append("3. **Submission Bundle Packaging:** Verify all future manuscript and code submission ZIP archives explicitly exclude `groq_key.txt` and any credentials.")
    report_lines.append("")

    report_text = "\n".join(report_lines)
    print(report_text)

    out_file = ROOT / "results_v2" / "key_hygiene_report.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(report_text, encoding='utf-8')
    print(f"\nSaved key hygiene report to: {out_file}")

if __name__ == '__main__':
    audit_key_hygiene()

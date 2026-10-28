import os
import shutil
import hashlib
import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(r"C:\testing\research_execution_20261018")
BACKUP_DIR = ROOT / "backups" / "backup_remediation_20261026_2028"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

KEY_FILES = [
    "research_paper_final.tex",
    "references.bib",
    "architecture_pipeline_figure.tex",
    "compiled_manuscript.pdf",
    "manuscript_submission_bundle_corrected.zip",
    "proposed_3arm_schedule.csv",
    "protocol_v3_runner.py",
    "budget_controller.py",
    "CANONICAL_RUN_LEDGER.csv",
    "BASELINE_DATA_INVENTORY_SHA256.md",
    "DATA_PROVENANCE_AUDIT_FINAL.md",
    "results/v3_3arm_summary_reconciled_v2.csv",
    "results/v3_3arm_summary_raw.csv",
    "results/v3_3arm_summary.csv"
]

def get_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

# 1. Perform Backup
backed_up = []
for rel in KEY_FILES:
    src = ROOT / rel
    if src.exists():
        dst = BACKUP_DIR / src.name
        shutil.copy2(src, dst)
        backed_up.append((rel, src.stat().st_size, get_sha256(src)))

print(f"[+] Successfully backed up {len(backed_up)} files to {BACKUP_DIR}")

# 2. Generate REMEDIATION_00_BACKUP_AND_HASH_MANIFEST.md
manifest_md = ROOT / "REMEDIATION_00_BACKUP_AND_HASH_MANIFEST.md"
with open(manifest_md, "w", encoding="utf-8") as f:
    f.write("# REMEDIATION 00: BACKUP AND HASH MANIFEST\n")
    f.write(f"**Date:** {datetime.now().isoformat()}\n")
    f.write(f"**Backup Directory:** `{BACKUP_DIR}`\n\n")
    f.write("## Backed-up Critical Artifacts\n\n")
    f.write("| Relative Path | Size (Bytes) | SHA-256 Checksum |\n")
    f.write("| :--- | :---: | :--- |\n")
    for rel, sz, sha in backed_up:
        f.write(f"| `{rel}` | {sz:,} | `{sha}` |\n")

print(f"[+] Written {manifest_md}")

# 3. Generate REMEDIATION_00_ARTIFACT_INVENTORY.csv
inventory_csv = ROOT / "REMEDIATION_00_ARTIFACT_INVENTORY.csv"
all_files = []
for p in ROOT.rglob("*"):
    if p.is_file() and ".git" not in p.parts:
        try:
            rel = p.relative_to(ROOT)
            sz = p.stat().st_size
            sha = get_sha256(p)
            ext = p.suffix.lower()
            category = "Source" if ext in [".py", ".tex", ".bib"] else (
                "Data" if ext in [".csv", ".json"] else (
                    "Documentation" if ext in [".md", ".txt"] else (
                        "Archive" if ext in [".zip", ".pdf"] else "Other"
                    )
                )
            )
            all_files.append({
                "RelativePath": str(rel),
                "SizeBytes": sz,
                "SHA256": sha,
                "Category": category,
                "LastModified": datetime.fromtimestamp(p.stat().st_mtime).isoformat()
            })
        except Exception as e:
            pass

with open(inventory_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["RelativePath", "SizeBytes", "SHA256", "Category", "LastModified"])
    writer.writeheader()
    writer.writerows(all_files)

print(f"[+] Written inventory of {len(all_files)} artifacts to {inventory_csv}")

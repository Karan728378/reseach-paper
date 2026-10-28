"""
Phase 0: Safety, Backup, and Provenance Generator
Creates timestamped backup of key files and generates Phase 0 audit deliverables.
"""
import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import csv

WORKSPACE = Path(r"C:\testing\research_execution_20261018")
BACKUP_DIR = WORKSPACE / "backups" / "backup_phase0_20261026_1958"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

files_to_backup = [
    "research_paper_final.tex",
    "compiled_manuscript.pdf",
    "references.bib",
    "architecture_pipeline_figure.tex",
    "budget_controller.py",
    "protocol_v3_runner.py",
    "proposed_3arm_schedule.csv",
    "results/v3_3arm_summary_reconciled_v2.csv",
    "results/v3_3arm_reconciliation_audit.json",
    "results/daily_quota_ledger.json",
    "manuscript_submission_bundle_corrected.zip",
    "BASELINE_DATA_INVENTORY_SHA256.md",
    "DISAMBIGUATION_PROBES_PROTOCOL.md",
    "MULTI_FRAMEWORK_OBSERVATION_TAXONOMY.md",
    "SIX_FLAW_REPAIR_LOG.md",
    "FINAL_CLAIM_EVIDENCE_AUDIT.md",
    "IEEE_FORMAT_VALIDATION.md",
    "FINAL_VALIDATION_REPORT.md",
    "README_REVIEW_PACKAGE.md"
]

backed_up = []
for rel in files_to_backup:
    src = WORKSPACE / rel
    if src.exists():
        dst = BACKUP_DIR / src.name
        shutil.copy2(src, dst)
        backed_up.append((rel, str(dst)))

print(f"Backed up {len(backed_up)} key artifacts to {BACKUP_DIR}")

# Build comprehensive manifest
manifest_rows = []

# List all primary files in workspace (root and immediate key subdirs)
target_paths = list(WORKSPACE.glob("*.tex")) + \
               list(WORKSPACE.glob("*.pdf")) + \
               list(WORKSPACE.glob("*.bib")) + \
               list(WORKSPACE.glob("*.csv")) + \
               list(WORKSPACE.glob("*.json")) + \
               list(WORKSPACE.glob("*.zip")) + \
               list(WORKSPACE.glob("*.py")) + \
               list(WORKSPACE.glob("*.md")) + \
               list((WORKSPACE / "results").glob("*.csv")) + \
               list((WORKSPACE / "results").glob("*.json")) + \
               list((WORKSPACE / "fixtures").glob("*.html"))

def categorize(p: Path) -> str:
    name = p.name
    rel = str(p.relative_to(WORKSPACE))
    if "3arm_runs" in rel or "proposed" in name or name in ["v3_3arm_summary_raw.csv", "daily_quota_ledger.json"]:
        return "RAW_HISTORICAL_DATA"
    elif "reconciled" in name or "audit" in name or "manifest" in name or "summary" in name:
        return "DERIVED_AUDIT_DATA"
    elif p.suffix == ".tex" or p.suffix == ".bib" or p.suffix == ".pdf":
        return "MANUSCRIPT_SOURCE_OR_BUILD"
    elif name.startswith("test_"):
        return "OFFLINE_TEST_SUITE"
    elif p.suffix == ".py":
        return "RUNNER_OR_ANALYSIS_SCRIPT"
    elif p.suffix == ".md":
        return "DOCUMENTATION_OR_PROTOCOL"
    elif p.suffix == ".html":
        return "HTML_FIXTURE"
    else:
        return "AUXILIARY_ARTIFACT"

seen = set()
for p in target_paths:
    if p.is_file() and p not in seen:
        seen.add(p)
        stat = p.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
        size = stat.st_size
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        category = categorize(p)
        manifest_rows.append({
            "rel_path": str(p.relative_to(WORKSPACE)).replace("\\", "/"),
            "category": category,
            "size_bytes": size,
            "mtime": mtime,
            "sha256": sha
        })

manifest_rows.sort(key=lambda r: (r["category"], r["rel_path"]))

manifest_csv = WORKSPACE / "AUDIT_00_ARTIFACT_MANIFEST.csv"
with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["rel_path", "category", "size_bytes", "mtime", "sha256"])
    writer.writeheader()
    writer.writerows(manifest_rows)

print(f"Generated {manifest_csv} with {len(manifest_rows)} cataloged artifacts.")

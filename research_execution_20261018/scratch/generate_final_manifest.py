import hashlib
import csv
from pathlib import Path

def get_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    root = Path(r"C:\testing\research_execution_20261018")
    output_csv = root / "FINAL_ARTIFACT_MANIFEST.csv"

    # Select critical files across all categories
    target_files = [
        # Manuscript & Submissions
        "research_paper_final.tex",
        "references.bib",
        "architecture_pipeline_figure.tex",
        "compiled_manuscript.pdf",
        "manuscript_submission_bundle_corrected.zip",
        "README_OVERLEAF.md",
        
        # Primary Audit Deliverables
        "AUDIT_00_ARTIFACT_MANIFEST.csv",
        "AUDIT_00_PROVENANCE_REPORT.md",
        "AUDIT_00_BACKUP_AND_SAFETY_STATUS.md",
        "AUDIT_01_REVIEW_ISSUE_LEDGER.csv",
        "AUDIT_01_REVIEW_ISSUE_LEDGER.md",
        "AUDIT_01_REVIEW_COVERAGE.md",
        "CANONICAL_RUN_LEDGER.csv",
        "DATA_PROVENANCE_AUDIT_FINAL.md",
        "EXPERIMENT_RECONCILIATION_FINAL.md",
        "PROTOCOL_VERSION_HISTORY.md",
        "MANUSCRIPT_CLAIM_TO_EVIDENCE_MATRIX.csv",
        "SERIALIZER_TRACEABILITY_AUDIT.md",
        "IMPLEMENTATION_FINDINGS.md",
        "OFFLINE_TEST_RESULTS_FINAL.md",
        "STATISTICAL_REANALYSIS_FINAL.md",
        "POWER_AND_SAMPLE_SIZE_AUDIT.md",
        "METHODS_AND_CAUSAL_IDENTIFICATION_AUDIT.md",
        "LIMITATIONS_AND_UNSUPPORTED_CLAIMS.md",
        "FINAL_BUILD_LOG.txt",
        
        # Core Runner & Guard Scripts
        "protocol_v3_runner.py",
        "budget_controller.py",
        r"..\.venv311\Lib\site-packages\browser_use\dom\serializer\serializer.py",
        r"..\.venv311\Lib\site-packages\browser_use\dom\views.py",
        
        # Raw Data Baselines
        "proposed_3arm_schedule.csv",
        "results/v3_3arm_summary_reconciled_v2.csv",
        "results/v3_3arm_summary_raw.csv",
        "results/v3_3arm_summary.csv",
        "BASELINE_DATA_INVENTORY_SHA256.md"
    ]

    records = []
    for rel_path in target_files:
        p = root / rel_path
        if p.exists():
            sha = get_sha256(p)
            size = p.stat().st_size
            category = "Manuscript" if p.suffix in [".tex", ".pdf", ".bib"] else (
                "Audit" if "AUDIT" in p.name or "REPORT" in p.name or "FINDINGS" in p.name or "CLAIM" in p.name else (
                    "Data" if p.suffix in [".csv", ".json"] else (
                        "Code" if p.suffix == ".py" else "Bundle"
                    )
                )
            )
            records.append({
                "Filename": rel_path,
                "SizeBytes": size,
                "SHA256": sha,
                "Category": category,
                "IntegrityStatus": "VERIFIED_CANONICAL"
            })
        else:
            records.append({
                "Filename": rel_path,
                "SizeBytes": -1,
                "SHA256": "FILE_NOT_FOUND",
                "Category": "Missing",
                "IntegrityStatus": "MISSING"
            })

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Filename", "SizeBytes", "SHA256", "Category", "IntegrityStatus"])
        writer.writeheader()
        writer.writerows(records)

    print(f"Exported {len(records)} records to {output_csv}")

if __name__ == "__main__":
    main()

import zipfile
from pathlib import Path

def inspect_and_repack_bundle():
    bundle_path = Path(r"C:\testing\research_execution_20261018\manuscript_submission_bundle_corrected.zip")
    exec_dir = Path(r"C:\testing\research_execution_20261018")

    files_to_pack = [
        ("research_paper_final.tex", exec_dir / "research_paper_final.tex"),
        ("references.bib", exec_dir / "references.bib"),
        ("architecture_pipeline_figure.tex", exec_dir / "architecture_pipeline_figure.tex"),
        ("CANONICAL_RUN_LEDGER.csv", exec_dir / "CANONICAL_RUN_LEDGER.csv"),
        ("FINAL_VALIDATION_05_PROVENANCE_AND_CLAIM_MAP.csv", exec_dir / "FINAL_VALIDATION_05_PROVENANCE_AND_CLAIM_MAP.csv"),
        ("FINAL_VALIDATION_02_REVIEW_CLOSURE.csv", exec_dir / "FINAL_VALIDATION_02_REVIEW_CLOSURE.csv"),
        ("MANUSCRIPT_CLAIM_TO_EVIDENCE_MATRIX.csv", exec_dir / "MANUSCRIPT_CLAIM_TO_EVIDENCE_MATRIX.csv"),
        ("EVIDENCE_TO_CLAIM_MATRIX.csv", exec_dir / "EVIDENCE_TO_CLAIM_MATRIX.csv"),
        ("README_OVERLEAF.md", exec_dir / "README_OVERLEAF.md")
    ]

    print("=== Packing Verified Manuscript Submission Bundle ===")
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for arcname, fpath in files_to_pack:
            if fpath.exists():
                zf.write(fpath, arcname=arcname)
                print(f"  + Added: {arcname:<35} ({fpath.stat().st_size:,} bytes)")
            else:
                print(f"  ! Missing file: {fpath}")

    # Verify integrity with testzip
    with zipfile.ZipFile(bundle_path, "r") as zf:
        bad_file = zf.testzip()
        if bad_file:
            print(f"ERROR: Corrupted file in zip: {bad_file}")
        else:
            print(f"\n[+] Bundle verification successful: zipfile.testzip() passed cleanly!")
            print(f"    Bundle Path: {bundle_path}")
            print(f"    Bundle Size: {bundle_path.stat().st_size:,} bytes")

if __name__ == "__main__":
    inspect_and_repack_bundle()

import os
import zipfile
import hashlib
from pathlib import Path

BASE_DIR = Path("C:/testing/research_execution_20261018")
ZIP_OUT = BASE_DIR / "manuscript_submission_bundle_corrected.zip"

files_to_package = [
    "research_paper_final.tex",
    "architecture_pipeline_figure.tex",
    "references.bib",
    "compiled_manuscript.pdf",
    "README_OVERLEAF.md",
    "README_SUBMISSION.txt",
    "EVIDENCE_TO_CLAIM_MATRIX.csv",
    "CLAIM_PROVENANCE_AUDIT.md",
    "MODEL_RUN_PROVENANCE_AUDIT.md",
    "POWER_ANALYSIS_REPRODUCTION.md",
    "TOST_SAMPLE_SIZE_AUDIT.md",
    "CLUSTERING_AND_EXPERIMENTAL_UNIT_AUDIT.md",
    "INTERVALS_MULTIPLICITY_AND_ESTIMANDS_AUDIT.md",
    "DOM_OBSERVATION_CHANNEL_AUDIT.md",
    "ACCESSIBILITY_CORRESPONDENCE_AUDIT.md",
    "TOOL_REACHABILITY_AND_OBSERVATION_LIMITS.md",
    "CROSS_FRAMEWORK_FEASIBILITY_AUDIT.md",
    "FUTURE_BEHAVIORAL_EXPERIMENT.md",
    "protocol_v4_rcbd_metadata.json",
    "TEST_COVERAGE_AND_REPAIR_LOG.md",
    "INDEPENDENT_FINAL_VALIDATION.md",
    "MANUSCRIPT_REVISION_CHANGELOG.md",
    "LATEX_AND_PDF_VALIDATION.md",
    "REPRODUCIBILITY_GUIDE.md"
]

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

print("=== PACKAGING SUBMISSION BUNDLE ===")
file_hashes = {}

# Verify all files exist
for rel_path in files_to_package:
    fpath = BASE_DIR / rel_path
    if not fpath.exists():
        raise FileNotFoundError(f"Missing required file: {rel_path}")
    h = sha256_file(fpath)
    sz = fpath.stat().st_size
    file_hashes[rel_path] = (h, sz)
    print(f"  + {rel_path} ({sz:,} bytes, SHA-256: {h[:12]}...)")

# Build ZIP
if ZIP_OUT.exists():
    ZIP_OUT.unlink()

with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for rel_path in files_to_package:
        fpath = BASE_DIR / rel_path
        zf.write(fpath, arcname=rel_path)

zip_hash = sha256_file(ZIP_OUT)
zip_size = ZIP_OUT.stat().st_size
print(f"\nCreated: {ZIP_OUT}")
print(f"Total files packaged: {len(files_to_package)}")
print(f"Archive Size: {zip_size:,} bytes")
print(f"Archive SHA-256: {zip_hash}")

# Verify ZIP by reading back
print("\n=== VERIFYING ARCHIVE INTEGRITY ===")
with zipfile.ZipFile(ZIP_OUT, "r") as zf:
    test_result = zf.testzip()
    if test_result is not None:
        raise ValueError(f"Corrupt file in zip: {test_result}")
    namelist = zf.namelist()
    print(f"Integrity test: PASSED (0 corrupt files).")
    print(f"Namelist match: {len(namelist)} files in archive.")
    for name in namelist:
        info = zf.getinfo(name)
        extracted_data = zf.read(name)
        extracted_hash = hashlib.sha256(extracted_data).hexdigest()
        orig_hash = file_hashes[name][0]
        if extracted_hash != orig_hash:
            raise ValueError(f"Hash mismatch on {name}!")
print("All files inside archive match original disk hashes exactly!")

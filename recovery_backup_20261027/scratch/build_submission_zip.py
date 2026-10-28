import os
import zipfile
from pathlib import Path

ROOT_DIR = Path(".").resolve()
ZIP_PATH = ROOT_DIR / "manuscript_submission_bundle.zip"

# Exclude patterns
EXCLUDE_DIRS = {".venv311", "__pycache__", ".git", ".pytest_cache", "wheels", "scratch", "test_scratch_synthetic_data"}
EXCLUDE_EXTS = {".pyc", ".whl", ".log"}
EXCLUDE_FILES = {"groq_key.txt", "manuscript_submission_bundle.zip"}

included_count = 0
total_uncompressed_bytes = 0

print(f"Building submission bundle: {ZIP_PATH.name}")

with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    for root, dirs, files in os.walk(ROOT_DIR):
        # Prune excluded dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            if fname in EXCLUDE_FILES or any(fname.endswith(ext) for ext in EXCLUDE_EXTS):
                continue
            
            fpath = Path(root) / fname
            rel_path = fpath.relative_to(ROOT_DIR)
            
            # Write to zip
            zipf.write(fpath, arcname=str(rel_path))
            included_count += 1
            total_uncompressed_bytes += fpath.stat().st_size

print(f"Wrote {included_count} files ({total_uncompressed_bytes / (1024*1024):.2f} MB uncompressed).")
zip_size = ZIP_PATH.stat().st_size
print(f"Compressed ZIP size: {zip_size / (1024*1024):.2f} MB.")

# Test ZIP integrity
with zipfile.ZipFile(ZIP_PATH, "r") as zipf:
    bad_file = zipf.testzip()
    if bad_file:
        raise ValueError(f"Corrupted file in ZIP: {bad_file}")
    else:
        print("ZIP Integrity Test: PASS (testzip() returned None, 0 errors).")

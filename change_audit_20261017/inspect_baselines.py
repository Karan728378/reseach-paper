import os
import hashlib
import datetime
import csv
import json
from pathlib import Path

BASE_DIR = Path(r"C:\testing")
CHANGE_AUDIT_DIR = BASE_DIR / "change_audit_20261017"

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

print("--- 1. SPECIFIC CHECK OF full-summary.csv ---")
fs_path = BASE_DIR / "results" / "main_experiment" / "full-summary.csv"
expected_hash = "42e9856ae932d56e5d8c766b2fd37bdced4088e6e7e4d0a4d85ecc7244365621"
if fs_path.exists():
    current_hash = get_sha256(fs_path)
    size = fs_path.stat().st_size
    mtime = datetime.datetime.fromtimestamp(fs_path.stat().st_mtime, datetime.timezone.utc).isoformat()
    print(f"Path: {fs_path}")
    print(f"Current SHA-256:  {current_hash}")
    print(f"Expected SHA-256: {expected_hash}")
    print(f"Match? {current_hash == expected_hash}")
    print(f"Size: {size} bytes, mtime UTC: {mtime}")
else:
    print(f"Path {fs_path} does not exist!")

# Also check backup full-summary.csv
backup_fs_path = BASE_DIR / "results" / "main_experiment_backup_20261011" / "full-summary.csv"
if backup_fs_path.exists():
    b_hash = get_sha256(backup_fs_path)
    b_size = backup_fs_path.stat().st_size
    b_mtime = datetime.datetime.fromtimestamp(backup_fs_path.stat().st_mtime, datetime.timezone.utc).isoformat()
    print(f"\nBackup Path: {backup_fs_path}")
    print(f"Backup SHA-256:   {b_hash}")
    print(f"Match expected?   {b_hash == expected_hash}")
    print(f"Match primary?    {b_hash == current_hash}")

print("\n--- 2. AUDIT DIRECTORIES IN C:\\testing ---")
for item in BASE_DIR.iterdir():
    if item.is_dir() and any(k in item.name.lower() for k in ["audit", "scratch"]):
        num_files = sum(len(files) for _, _, files in os.walk(item))
        print(f"Dir: {item.name} | Total files: {num_files} | Last modified: {datetime.datetime.fromtimestamp(item.stat().st_mtime, datetime.timezone.utc).isoformat()}")

print("\n--- 3. INSPECTING PHASE 0 PRE-AUDIT MANIFESTS ---")
phase0_dir = BASE_DIR / "audit" / "phase0"
for f in phase0_dir.iterdir():
    print(f"  {f.name}: {f.stat().st_size} bytes, mtime: {datetime.datetime.fromtimestamp(f.stat().st_mtime, datetime.timezone.utc).isoformat()}")

# Read a few rows of phase0 manifest
p0_manifest_path = phase0_dir / "file_manifest.csv"
if p0_manifest_path.exists():
    with open(p0_manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        p0_rows = list(reader)
    print(f"Phase 0 file_manifest.csv rows: {len(p0_rows)}")
    print(f"Phase 0 columns: {p0_rows[0].keys() if p0_rows else None}")
    # check if full-summary.csv is in p0_rows
    p0_fs = [r for r in p0_rows if "full-summary.csv" in r.get("relpath", "") or "full-summary.csv" in r.get("relative_path", "")]
    for r in p0_fs:
        print("  P0 record:", r)

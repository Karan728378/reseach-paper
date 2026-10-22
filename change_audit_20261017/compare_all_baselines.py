import os
import hashlib
import datetime
import csv
from pathlib import Path
from collections import Counter, defaultdict

BASE_DIR = Path(r"C:\testing")
AUDIT_DIR = BASE_DIR / "research_audit_20261015_231500"
CHANGE_AUDIT_DIR = BASE_DIR / "change_audit_20261017"

def sha256_file(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest(), None
    except Exception as e:
        return None, str(e)

print("=== 1. VERIFYING ALL 2,012 FILES FROM 01_FILE_HASH_MANIFEST.CSV ===")
manifest_path = AUDIT_DIR / "01_FILE_HASH_MANIFEST.csv"
manifest_rows = []
with open(manifest_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    manifest_rows = list(reader)

print(f"Total rows in 01_FILE_HASH_MANIFEST.csv: {len(manifest_rows)}")

manifest_comparisons = []
mismatches = []
missing_files = []

for r in manifest_rows:
    rel_path = r["relative_path"]
    expected_hash = r["sha256_hash"]
    expected_size = int(r["file_size_bytes"])
    expected_mtime = r["modified_time_utc"]

    full_path = BASE_DIR / rel_path
    if not full_path.exists():
        missing_files.append(rel_path)
        manifest_comparisons.append({
            "relative_path": rel_path,
            "status": "VERIFIED DELETED",
            "expected_hash": expected_hash,
            "current_hash": "FILE_NOT_FOUND",
            "expected_size": expected_size,
            "current_size": 0,
            "expected_mtime": expected_mtime,
            "current_mtime": "N/A",
            "baseline": "01_FILE_HASH_MANIFEST.csv"
        })
        continue

    current_size = full_path.stat().st_size
    current_mtime = datetime.datetime.fromtimestamp(full_path.stat().st_mtime, datetime.timezone.utc).isoformat()
    current_hash, err = sha256_file(full_path)

    if err or current_hash != expected_hash:
        mismatches.append((rel_path, expected_hash, current_hash, err))
        status = "VERIFIED MODIFIED"
    else:
        status = "VERIFIED UNCHANGED"

    manifest_comparisons.append({
        "relative_path": rel_path,
        "status": status,
        "expected_hash": expected_hash,
        "current_hash": current_hash if current_hash else f"ERR: {err}",
        "expected_size": expected_size,
        "current_size": current_size,
        "expected_mtime": expected_mtime,
        "current_mtime": current_mtime,
        "baseline": "01_FILE_HASH_MANIFEST.csv"
    })

print(f"Manifest verification complete:")
print(f"  Unchanged: {sum(1 for c in manifest_comparisons if c['status'] == 'VERIFIED UNCHANGED')}")
print(f"  Modified:  {len(mismatches)}")
print(f"  Missing:   {len(missing_files)}")
if mismatches:
    print("Mismatches found:")
    for m in mismatches:
        print("  ", m)

print("\n=== 2. COMPARING AGAINST PHASE 0 BASELINE (audit/phase0/file_manifest.csv) ===")
p0_path = BASE_DIR / "audit" / "phase0" / "file_manifest.csv"
p0_mismatches = []
p0_checked = 0
with open(p0_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        if r["item_type"] != "file":
            continue
        p0_checked += 1
        abs_p = Path(r["absolute_path"])
        exp_h = r["sha256"]
        if not abs_p.exists():
            p0_mismatches.append((r["absolute_path"], "MISSING", exp_h))
            continue
        curr_h, _ = sha256_file(abs_p)
        if curr_h != exp_h:
            p0_mismatches.append((r["absolute_path"], curr_h, exp_h))

print(f"Phase 0 checked {p0_checked} files (from 2026-10-14).")
print(f"Phase 0 mismatches: {len(p0_mismatches)}")
if p0_mismatches:
    for m in p0_mismatches[:5]:
        print("  ", m)

print("\n=== 3. COMPARING main_experiment VS main_experiment_backup_20261011 ===")
prim_dir = BASE_DIR / "results" / "main_experiment"
back_dir = BASE_DIR / "results" / "main_experiment_backup_20261011"

prim_files = {str(p.relative_to(prim_dir)).replace("\\", "/"): p for p in prim_dir.rglob("*") if p.is_file()}
back_files = {str(p.relative_to(back_dir)).replace("\\", "/"): p for p in back_dir.rglob("*") if p.is_file()}

print(f"Primary files: {len(prim_files)}, Backup files: {len(back_files)}")
diff_keys = set(prim_files.keys()) ^ set(back_files.keys())
print(f"Keys difference: {len(diff_keys)}")

content_diffs = []
for k in sorted(prim_files.keys() & back_files.keys()):
    h1, _ = sha256_file(prim_files[k])
    h2, _ = sha256_file(back_files[k])
    if h1 != h2:
        content_diffs.append((k, h1, h2))

print(f"Content hash differences between primary and backup: {len(content_diffs)}")

print("\n=== 4. INVENTORY OF ALL FILES IN research_audit_20261015_231500 ===")
audit_files = []
for p in AUDIT_DIR.rglob("*"):
    if p.is_file():
        h, _ = sha256_file(p)
        audit_files.append({
            "relative_path": str(p.relative_to(BASE_DIR)).replace("\\", "/"),
            "file_size_bytes": p.stat().st_size,
            "modified_time_utc": datetime.datetime.fromtimestamp(p.stat().st_mtime, datetime.timezone.utc).isoformat(),
            "sha256": h
        })
print(f"Total files in research_audit_20261015_231500: {len(audit_files)}")
print("First 10 audit files:")
for af in audit_files[:10]:
    print(f"  {af['relative_path']} ({af['file_size_bytes']} bytes)")

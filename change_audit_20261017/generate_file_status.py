import os
import hashlib
import datetime
import csv
from pathlib import Path
from collections import Counter

BASE_DIR = Path(r"C:\testing")
AUDIT_DIR = BASE_DIR / "research_audit_20261015_231500"
CHANGE_AUDIT_DIR = BASE_DIR / "change_audit_20261017"

# Load 01_FILE_HASH_MANIFEST.csv
manifest_path = AUDIT_DIR / "01_FILE_HASH_MANIFEST.csv"
manifest_map = {}
with open(manifest_path, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        manifest_map[row["relative_path"]] = row

# Load phase0 manifest
p0_path = BASE_DIR / "audit" / "phase0" / "file_manifest.csv"
p0_map = {}
with open(p0_path, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["item_type"] == "file":
            p0_map[row["absolute_path"].lower()] = row

def sha256_file(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest(), None
    except Exception as e:
        return None, str(e)

all_current_files = []
ignored_dirs = {".venv", ".venv311", ".pytest_cache", "__pycache__"}

for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith(".")]
    for f in files:
        if f.endswith(".pyc"): continue
        abs_p = Path(root) / f
        rel_p = str(abs_p.relative_to(BASE_DIR)).replace("\\", "/")
        all_current_files.append((rel_p, abs_p))

print(f"Total current project files found (excluding venvs/pycache): {len(all_current_files)}")

classified_records = []
untracked_files = []

for rel_p, abs_p in all_current_files:
    size = abs_p.stat().st_size
    mtime = datetime.datetime.fromtimestamp(abs_p.stat().st_mtime, datetime.timezone.utc).isoformat()
    h, err = sha256_file(abs_p)

    if rel_p in manifest_map:
        m_row = manifest_map[rel_p]
        exp_h = m_row["sha256_hash"]
        if h == exp_h:
            status = "VERIFIED UNCHANGED"
            evidence = "Exact SHA-256 match with 01_FILE_HASH_MANIFEST.csv (captured 2026-10-15T23:14:54)"
        else:
            status = "VERIFIED MODIFIED"
            evidence = f"Hash mismatch with 01_FILE_HASH_MANIFEST.csv (exp: {exp_h[:12]}..., curr: {h[:12]}...)"
    elif rel_p.startswith("research_audit_20261015_231500/"):
        status = "VERIFIED NEW"
        evidence = "Created during Research Audit (2026-10-15 to 2026-10-17)"
    elif rel_p.startswith("change_audit_20261017/"):
        status = "VERIFIED NEW"
        evidence = "Created during Change Audit (2026-10-17)"
    else:
        abs_lower = str(abs_p).lower()
        if abs_lower in p0_map:
            p0_row = p0_map[abs_lower]
            if h == p0_row["sha256"]:
                status = "VERIFIED UNCHANGED"
                evidence = "Exact SHA-256 match with Phase 0 baseline (audit/phase0/file_manifest.csv, 2026-10-14)"
            else:
                status = "VERIFIED MODIFIED"
                evidence = f"Hash mismatch with Phase 0 baseline"
        else:
            status = "UNVERIFIABLE"
            evidence = f"Existed outside 01_FILE_HASH_MANIFEST target directories (e.g. {rel_p.split('/')[0]}); no pre-audit baseline hash available"
            untracked_files.append((rel_p, size, mtime, h))

    classified_records.append({
        "relative_path": rel_p,
        "status": status,
        "current_sha256": h if h else f"ERR: {err}",
        "file_size_bytes": size,
        "modified_time_utc": mtime,
        "evidence_and_method": evidence
    })

print("\n--- CLASSIFICATION SUMMARY ---")
status_counts = Counter(r["status"] for r in classified_records)
for s, c in status_counts.items():
    print(f"  {s:25s}: {c}")

print(f"\nFiles classified as UNVERIFIABLE ({len(untracked_files)}):")
for uf in untracked_files:
    print(f"  {uf[0]} ({uf[1]} bytes, mtime: {uf[2]})")

out_csv = CHANGE_AUDIT_DIR / "file_status.csv"
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "relative_path", "status", "current_sha256", "file_size_bytes", "modified_time_utc", "evidence_and_method"
    ])
    writer.writeheader()
    writer.writerows(classified_records)

print(f"\nfile_status.csv written successfully to {out_csv} with {len(classified_records)} rows.")

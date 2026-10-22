#!/usr/bin/env python3
"""
Phase 0 Manifest Generation and Integrity Verification Script
Generates file manifests and tree comparison for:
  - C:\testing\results\main_experiment
  - C:\testing\results\main_experiment_backup_20261011
Computes SHA-256 hashes, verifies historical hashes, and proves zero modification.
"""

import os
import csv
import hashlib
import datetime

PRIMARY_DIR = r"C:\testing\results\main_experiment"
BACKUP_DIR = r"C:\testing\results\main_experiment_backup_20261011"
AUDIT_PHASE0_DIR = r"C:\testing\audit\phase0"
HISTORICAL_SHA256 = "42e9856ae932d56e5d8c766b2fd37bdced4088e6e7e4d0a4d85ecc7244365621"

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def get_tree_inventory(base_dir):
    """
    Inventories all items (directories and files) under base_dir.
    Returns:
      items: dict of relpath -> dict(
          relpath, abspath, item_type, size_bytes, sha256, mtime_utc, error
      )
    """
    items = {}
    for root, dirs, files in os.walk(base_dir):
        for d in sorted(dirs):
            abspath = os.path.join(root, d)
            relpath = os.path.relpath(abspath, base_dir).replace("\\", "/")
            mtime = datetime.datetime.fromtimestamp(
                os.path.getmtime(abspath), datetime.timezone.utc
            ).isoformat()
            items[relpath] = {
                "relpath": relpath,
                "abspath": abspath,
                "item_type": "directory",
                "size_bytes": None,
                "sha256": "N/A (directory)",
                "mtime_utc": mtime,
                "error": None
            }
        for f in sorted(files):
            abspath = os.path.join(root, f)
            relpath = os.path.relpath(abspath, base_dir).replace("\\", "/")
            try:
                size_bytes = os.path.getsize(abspath)
                mtime = datetime.datetime.fromtimestamp(
                    os.path.getmtime(abspath), datetime.timezone.utc
                ).isoformat()
                file_hash = sha256_file(abspath)
                err = None
            except Exception as e:
                size_bytes = None
                mtime = None
                file_hash = None
                err = str(e)
            items[relpath] = {
                "relpath": relpath,
                "abspath": abspath,
                "item_type": "file",
                "size_bytes": size_bytes,
                "sha256": file_hash,
                "mtime_utc": mtime,
                "error": err
            }
    return items

def main():
    print("=== PHASE 0 AUDIT: INVENTORY AND HASH GENERATION ===")
    
    # 1. First pass (Before state)
    print("Capturing baseline inventory and hashes (primary)...")
    primary_items = get_tree_inventory(PRIMARY_DIR)
    print(f"Primary items total: {len(primary_items)} (files: {sum(1 for i in primary_items.values() if i['item_type'] == 'file')}, dirs: {sum(1 for i in primary_items.values() if i['item_type'] == 'directory')})")
    
    print("Capturing baseline inventory and hashes (backup)...")
    backup_items = get_tree_inventory(BACKUP_DIR)
    print(f"Backup items total: {len(backup_items)} (files: {sum(1 for i in backup_items.values() if i['item_type'] == 'file')}, dirs: {sum(1 for i in backup_items.values() if i['item_type'] == 'directory')})")

    # 2. Check unreadable files
    primary_errors = [i for i in primary_items.values() if i["error"]]
    backup_errors = [i for i in backup_items.values() if i["error"]]
    print(f"Primary unreadable files: {len(primary_errors)}")
    print(f"Backup unreadable files: {len(backup_errors)}")

    # 3. Verify historical hash of full-summary.csv
    primary_summary = primary_items.get("full-summary.csv")
    backup_summary = backup_items.get("full-summary.csv")
    print(f"Primary full-summary.csv SHA-256: {primary_summary['sha256'] if primary_summary else 'MISSING'}")
    print(f"Backup full-summary.csv SHA-256:  {backup_summary['sha256'] if backup_summary else 'MISSING'}")
    print(f"Historical SHA-256:              {HISTORICAL_SHA256}")
    primary_summary_match = (primary_summary and primary_summary["sha256"] == HISTORICAL_SHA256)
    backup_summary_match = (backup_summary and backup_summary["sha256"] == HISTORICAL_SHA256)
    print(f"Primary matches historical: {primary_summary_match}")
    print(f"Backup matches historical:  {backup_summary_match}")

    # 4. Write combined file_manifest.csv
    manifest_csv_path = os.path.join(AUDIT_PHASE0_DIR, "file_manifest.csv")
    print(f"Writing {manifest_csv_path}...")
    with open(manifest_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tree", "relative_path", "absolute_path", "item_type", "size_bytes", "sha256", "modified_time_utc", "read_error"])
        # Primary items
        for relpath in sorted(primary_items.keys()):
            item = primary_items[relpath]
            writer.writerow([
                "primary (main_experiment)",
                item["relpath"],
                item["abspath"],
                item["item_type"],
                item["size_bytes"] if item["size_bytes"] is not None else "",
                item["sha256"] if item["sha256"] is not None else "",
                item["mtime_utc"] if item["mtime_utc"] is not None else "",
                item["error"] if item["error"] is not None else ""
            ])
        # Backup items
        for relpath in sorted(backup_items.keys()):
            item = backup_items[relpath]
            writer.writerow([
                "backup (main_experiment_backup_20261011)",
                item["relpath"],
                item["abspath"],
                item["item_type"],
                item["size_bytes"] if item["size_bytes"] is not None else "",
                item["sha256"] if item["sha256"] is not None else "",
                item["mtime_utc"] if item["mtime_utc"] is not None else "",
                item["error"] if item["error"] is not None else ""
            ])

    # Also write separate manifests for single-tree provenance clarity
    manifest_primary_path = os.path.join(AUDIT_PHASE0_DIR, "manifest_primary.csv")
    with open(manifest_primary_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["relative_path", "absolute_path", "item_type", "size_bytes", "sha256", "modified_time_utc", "read_error"])
        for relpath in sorted(primary_items.keys()):
            item = primary_items[relpath]
            writer.writerow([
                item["relpath"],
                item["abspath"],
                item["item_type"],
                item["size_bytes"] if item["size_bytes"] is not None else "",
                item["sha256"] if item["sha256"] is not None else "",
                item["mtime_utc"] if item["mtime_utc"] is not None else "",
                item["error"] if item["error"] is not None else ""
            ])

    manifest_backup_path = os.path.join(AUDIT_PHASE0_DIR, "manifest_backup.csv")
    with open(manifest_backup_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["relative_path", "absolute_path", "item_type", "size_bytes", "sha256", "modified_time_utc", "read_error"])
        for relpath in sorted(backup_items.keys()):
            item = backup_items[relpath]
            writer.writerow([
                item["relpath"],
                item["abspath"],
                item["item_type"],
                item["size_bytes"] if item["size_bytes"] is not None else "",
                item["sha256"] if item["sha256"] is not None else "",
                item["mtime_utc"] if item["mtime_utc"] is not None else "",
                item["error"] if item["error"] is not None else ""
            ])

    # 5. Build and write tree_comparison.csv
    comparison_csv_path = os.path.join(AUDIT_PHASE0_DIR, "tree_comparison.csv")
    print(f"Writing {comparison_csv_path}...")
    all_relpaths = sorted(set(primary_items.keys()) | set(backup_items.keys()))
    
    comp_rows = []
    status_counts = {}
    for rel in all_relpaths:
        p = primary_items.get(rel)
        b = backup_items.get(rel)
        
        in_p = p is not None
        in_b = b is not None
        p_type = p["item_type"] if p else ""
        b_type = b["item_type"] if b else ""
        p_size = p["size_bytes"] if p else None
        b_size = b["size_bytes"] if b else None
        p_sha = p["sha256"] if p else ""
        b_sha = b["sha256"] if b else ""
        
        if in_p and not in_b:
            status = "ONLY_IN_PRIMARY"
        elif in_b and not in_p:
            status = "ONLY_IN_BACKUP"
        elif p_type != b_type:
            status = "TYPE_MISMATCH"
        elif p_type == "directory" and b_type == "directory":
            status = "IDENTICAL_DIRECTORY"
        elif p_size != b_size:
            status = "SIZE_MISMATCH"
        elif p_sha != b_sha:
            status = "CONTENT_MISMATCH"
        else:
            status = "IDENTICAL"
            
        status_counts[status] = status_counts.get(status, 0) + 1
        
        size_match = (p_size == b_size) if (in_p and in_b and p_type == "file") else (p_type == b_type == "directory")
        sha_match = (p_sha == b_sha) if (in_p and in_b) else False
        
        comp_rows.append([
            rel,
            p_type or b_type,
            in_p,
            in_b,
            p_size if p_size is not None else "",
            b_size if b_size is not None else "",
            size_match,
            p_sha,
            b_sha,
            sha_match,
            status
        ])
        
    with open(comparison_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "relative_path",
            "item_type",
            "in_primary",
            "in_backup",
            "primary_size_bytes",
            "backup_size_bytes",
            "size_match",
            "primary_sha256",
            "backup_sha256",
            "sha256_match",
            "status"
        ])
        writer.writerows(comp_rows)

    print(f"Tree comparison status counts: {status_counts}")

    # 6. Task 9: Second pass (After state) to prove zero modification
    print("Re-evaluating primary and backup trees for after-state integrity verification...")
    after_primary = get_tree_inventory(PRIMARY_DIR)
    after_backup = get_tree_inventory(BACKUP_DIR)

    primary_modifications = []
    for rel, item in primary_items.items():
        after_item = after_primary.get(rel)
        if not after_item:
            primary_modifications.append(f"DELETED: {rel}")
        elif item["sha256"] != after_item["sha256"]:
            primary_modifications.append(f"HASH CHANGED: {rel} ({item['sha256']} -> {after_item['sha256']})")
        elif item["mtime_utc"] != after_item["mtime_utc"]:
            primary_modifications.append(f"MTIME CHANGED: {rel} ({item['mtime_utc']} -> {after_item['mtime_utc']})")

    for rel in after_primary:
        if rel not in primary_items:
            primary_modifications.append(f"NEW FILE IN PRIMARY: {rel}")

    backup_modifications = []
    for rel, item in backup_items.items():
        after_item = after_backup.get(rel)
        if not after_item:
            backup_modifications.append(f"DELETED: {rel}")
        elif item["sha256"] != after_item["sha256"]:
            backup_modifications.append(f"HASH CHANGED: {rel} ({item['sha256']} -> {after_item['sha256']})")
        elif item["mtime_utc"] != after_item["mtime_utc"]:
            backup_modifications.append(f"MTIME CHANGED: {rel} ({item['mtime_utc']} -> {after_item['mtime_utc']})")

    for rel in after_backup:
        if rel not in backup_items:
            backup_modifications.append(f"NEW FILE IN BACKUP: {rel}")

    integrity_proof_path = os.path.join(AUDIT_PHASE0_DIR, "integrity_proof.txt")
    with open(integrity_proof_path, "w", encoding="utf-8") as f:
        f.write("=== PHASE 0 INTEGRITY VERIFICATION PROOF ===\n")
        f.write(f"Timestamp UTC: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n")
        f.write(f"Primary tree path: {PRIMARY_DIR}\n")
        f.write(f"Primary files checked: {sum(1 for i in primary_items.values() if i['item_type'] == 'file')}\n")
        f.write(f"Primary modifications detected: {len(primary_modifications)}\n")
        if primary_modifications:
            for m in primary_modifications:
                f.write(f"  {m}\n")
        else:
            f.write("  ZERO modifications detected in primary tree. All hashes, sizes, and timestamps match exactly.\n")
            
        f.write(f"\nBackup tree path: {BACKUP_DIR}\n")
        f.write(f"Backup files checked: {sum(1 for i in backup_items.values() if i['item_type'] == 'file')}\n")
        f.write(f"Backup modifications detected: {len(backup_modifications)}\n")
        if backup_modifications:
            for m in backup_modifications:
                f.write(f"  {m}\n")
        else:
            f.write("  ZERO modifications detected in backup tree. All hashes, sizes, and timestamps match exactly.\n")

    print(f"Primary modifications: {len(primary_modifications)}")
    print(f"Backup modifications: {len(backup_modifications)}")
    print("Integrity verification proof written.")

if __name__ == "__main__":
    main()

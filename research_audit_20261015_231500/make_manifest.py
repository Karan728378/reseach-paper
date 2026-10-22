import os
import hashlib
import datetime
import csv

BASE_DIR = r"C:\testing"
OUTPUT_DIR = r"C:\testing\research_audit_20261015_231500"
MANIFEST_FILE = os.path.join(OUTPUT_DIR, "01_FILE_HASH_MANIFEST.csv")

TARGET_DIRS = ["results", "variants", "shared", "tasks", "runner", "audit", "results_EXP1_FROZEN_BACKUP"]
ROOT_FILES = [
    "analysis_reproduction.py",
    "experiment1-followup-audit.md",
    "index.html",
    "stats_check.py",
    "test_t4_capture.py"
]

def sha256_file(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest(), None
    except Exception as e:
        return None, str(e)

def main():
    rows = []
    print("Starting file hash manifest generation...")
    
    # Root files
    for rf in ROOT_FILES:
        full_path = os.path.join(BASE_DIR, rf)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            st = os.stat(full_path)
            mtime = datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).isoformat()
            h, err = sha256_file(full_path)
            rows.append({
                "relative_path": rf,
                "file_size_bytes": st.st_size,
                "modified_time_utc": mtime,
                "sha256_hash": h if h else f"ERROR: {err}"
            })

    # Target directories
    for td in TARGET_DIRS:
        dir_path = os.path.join(BASE_DIR, td)
        if not os.path.exists(dir_path):
            continue
        for root, dirs, files in os.walk(dir_path):
            # Skip __pycache__
            dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]
            for f in sorted(files):
                if f.endswith(".pyc"):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")
                try:
                    st = os.stat(full_path)
                    mtime = datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).isoformat()
                    h, err = sha256_file(full_path)
                    rows.append({
                        "relative_path": rel_path,
                        "file_size_bytes": st.st_size,
                        "modified_time_utc": mtime,
                        "sha256_hash": h if h else f"ERROR: {err}"
                    })
                except Exception as e:
                    rows.append({
                        "relative_path": rel_path,
                        "file_size_bytes": 0,
                        "modified_time_utc": "UNKNOWN",
                        "sha256_hash": f"ERROR: {str(e)}"
                    })

    rows.sort(key=lambda x: x["relative_path"])
    
    with open(MANIFEST_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["relative_path", "file_size_bytes", "modified_time_utc", "sha256_hash"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Manifest written to {MANIFEST_FILE} with {len(rows)} files.")

if __name__ == "__main__":
    main()

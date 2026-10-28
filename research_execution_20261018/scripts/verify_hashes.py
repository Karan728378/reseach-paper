#!/usr/bin/env python3
"""
scripts/verify_hashes.py
Authoritative baseline SHA-256 verification utility.
Validates all original experimental data artifacts against BASELINE_DATA_INVENTORY_SHA256.md.
Ensures zero data corruption or historical file modification.
"""

import hashlib
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = PROJECT_ROOT / "BASELINE_DATA_INVENTORY_SHA256.md"


def verify_hashes() -> int:
    if not BASELINE_PATH.exists():
        print(f"ERROR: Baseline file not found at {BASELINE_PATH}")
        return 1

    content = BASELINE_PATH.read_text(encoding="utf-8")
    entries = []
    for line in content.splitlines():
        if "`" in line and "|" in line:
            file_match = re.search(r"`([^`]+(?:\.csv|\.json))`", line)
            hash_match = re.search(r"`([a-f0-9]{64})`", line)
            if file_match and hash_match:
                entries.append((file_match.group(1), hash_match.group(1)))

    print(f"Loaded {len(entries)} artifact checksums from BASELINE_DATA_INVENTORY_SHA256.md.")

    mismatches = []
    for file_str, exp_hash in entries:
        p = PROJECT_ROOT / file_str
        if not p.exists():
            p = PROJECT_ROOT / "results" / "3arm_runs" / file_str
        if not p.exists():
            mismatches.append(f"MISSING: {file_str}")
            continue

        actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual_hash != exp_hash:
            mismatches.append(f"MISMATCH: {p} (expected {exp_hash}, got {actual_hash})")

    if not mismatches:
        print(f"SUCCESS: All {len(entries)} artifacts verified byte-for-byte identical to baseline SHA-256 hashes.")
        return 0
    else:
        print(f"FAILURE: Detected {len(mismatches)} hash discrepancies:")
        for m in mismatches:
            print(f"  {m}")
        return 2


if __name__ == "__main__":
    sys.exit(verify_hashes())

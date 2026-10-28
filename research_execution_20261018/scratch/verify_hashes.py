import hashlib
import re
from pathlib import Path

baseline_path = Path("BASELINE_DATA_INVENTORY_SHA256.md")
content = baseline_path.read_text(encoding="utf-8")

# Extract table lines
entries = []
for line in content.splitlines():
    if "`" in line and "|" in line:
        # Find file path and sha256
        file_match = re.search(r"`([^`]+(?:\.csv|\.json))`", line)
        hash_match = re.search(r"`([a-f0-9]{64})`", line)
        if file_match and hash_match:
            entries.append((file_match.group(1), hash_match.group(1)))

print(f"Extracted {len(entries)} artifacts from BASELINE_DATA_INVENTORY_SHA256.md.")

mismatches = []
for file_str, exp_hash in entries:
    p = Path(file_str)
    if not p.exists():
        p = Path("results/3arm_runs") / file_str
    if not p.exists():
        mismatches.append(f"MISSING: {file_str}")
        continue
    actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
    if actual_hash != exp_hash:
        mismatches.append(f"MISMATCH: {p} (exp {exp_hash}, got {actual_hash})")
    else:
        # print(f"VERIFIED: {p.name}")
        pass

if not mismatches:
    print(f"ALL {len(entries)} ARTIFACTS VERIFIED BYTE-FOR-BYTE IDENTICAL TO BASELINE SHA-256 HASHES.")
else:
    print(f"ERRORS DETECTED: {len(mismatches)}")
    for m in mismatches:
        print("  ", m)

import os
import re
from pathlib import Path

target_files = [
    'test_data_reconciliation_and_provenance.py',
    'test_disambiguation_probes.py',
    'test_analyze_v3_results.py',
    'test_forensic_audit_regressions.py',
    'test_power_audit.py',
    'test_observation_pipeline_stages.py',
    'scripts/verify_hashes.py',
    'scripts/independent_ledger_audit.py',
    'analyze_v3_results.py',
]

work_dir = Path('C:/testing/work_copy_20261028')

print("Scanning allowlisted scripts and 6 test modules for hardcoded paths...")
for tf in target_files:
    p = work_dir / tf
    if not p.exists():
        print(f"Missing: {tf}")
        continue
    txt = p.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    matches = []
    for idx, l in enumerate(lines):
        if 'C:/testing' in l or 'C:\\\\testing' in l or 'C:\\testing' in l:
            matches.append((idx + 1, l))
    if matches:
        print(f"\n{tf} ({len(matches)} hardcoded path lines):")
        for line_no, line_content in matches:
            print(f"  Line {line_no:4d}: {line_content}")
    else:
        print(f"\n{tf}: Clean (no hardcoded paths)")

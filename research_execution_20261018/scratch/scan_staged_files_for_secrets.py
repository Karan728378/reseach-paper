import re
import os
from pathlib import Path

BASE_DIR = Path("C:/testing/research_execution_20261018")

candidate_files = [
    "research_paper_final.tex",
    "architecture_pipeline_figure.tex",
    "references.bib",
    "README_OVERLEAF.md",
    "README_SUBMISSION.txt",
    "REPRODUCIBILITY_GUIDE.md",
    "OVERNIGHT_BASELINE_INVENTORY.md",
    "OVERNIGHT_CHANGE_PLAN.md",
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
    "test_forensic_audit_regressions.py",
    "TEST_COVERAGE_AND_REPAIR_LOG.md",
    "INDEPENDENT_FINAL_VALIDATION.md",
    "MANUSCRIPT_REVISION_CHANGELOG.md",
    "LATEX_AND_PDF_VALIDATION.md",
    "SUBMISSION_PACKAGE_INTEGRITY.md",
    "reproduce_power_audit.py",
    "power_audit_results.json",
    "test_power_audit.py"
]

# Regex patterns for secrets
SECRET_PATTERNS = [
    (r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "API Key assignment"),
    (r"(?i)secret\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "Secret assignment"),
    (r"(?i)password\s*[:=]\s*['\"][^'\"]{8,}['\"]", "Password assignment"),
    (r"AIza[0-9A-Za-z\\-_]{35}", "Google API Key"),
    (r"sk-[A-Za-z0-9]{32,}", "OpenAI API Key"),
    (r"xox[baprs]-[0-9a-zA-Z]{10,48}", "Slack Token"),
    (r"gh[pous]_[A-Za-z0-9_]{16,}", "GitHub Token"),
    (r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----", "Private Key Header")
]

print("=== SCANNING CANDIDATE FILES FOR SECRETS ===")
findings = []

for rel_path in candidate_files:
    fpath = BASE_DIR / rel_path
    if not fpath.exists():
        print(f"WARNING: File does not exist: {rel_path}")
        continue
    
    # Read text
    try:
        text = fpath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Could not read {rel_path}: {e}")
        continue
        
    for pat, label in SECRET_PATTERNS:
        matches = re.findall(pat, text)
        if matches:
            findings.append((rel_path, label, len(matches)))

if findings:
    print(f"ALERT: Potential secrets detected in {len(findings)} checks:")
    for f, label, count in findings:
        print(f"  - {f}: {label} ({count} occurrences)")
else:
    print("SUCCESS: Zero secrets detected across all candidate files!")

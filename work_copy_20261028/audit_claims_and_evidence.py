"""
Claim-Evidence Guard
Automated verification tool that enforces scientific integrity:
Scans the project for completed live-model trials.
If live trial count is ZERO, it strictly audits manuscript and documentation drafts
to prevent unearned behavioral claims, overstated discoveries, and false review provenance.

Exit code 0: All claims are compliant with current evidence level.
Exit code 1: Unearned behavioral or empirical claims detected.
"""

import csv
import re
import sys
from pathlib import Path

RESEARCH_DIR = Path("C:/testing/research_execution_20261018")
RESULTS_DIR = RESEARCH_DIR / "results"
MANUSCRIPTS = [
    RESEARCH_DIR / "RESEARCH_PAPER_DRAFT.md",
    RESEARCH_DIR / "manuscript_draft.md"
]

# Patterns banned when live_trial_count == 0
BANNED_BEHAVIORAL_PATTERNS = [
    (r"\bwe prove\b", "Unearned proof assertion (replace with 'we measure' or 'we test')"),
    (r"\bflaw-free\b", "Unscientific assertion ('flaw-free verifier')"),
    (r"\bfundamental discovery\b", "Hyperbolic framing for engineering filter"),
    (r"\buniversal failure\b", "Unsubstantiated generalization across frameworks"),
    (r"\b100% semantic-information transmission failure\b", "Overstated absolute claim"),
    (r"\bproves? that semantic markup does not (help|matter|improve)\b", "Equivalence fallacy from unpowered or zero-run data"),
    (r"\bexternal peer reviews? from (Claude|Gemini)\b", "False attribution of internal AI generation as external peer review")
]

def get_live_trial_count() -> int:
    """Counts genuine completed live trials in results directory."""
    summary_file = RESULTS_DIR / "v3_run_summary.csv"
    if not summary_file.exists():
        return 0
    
    count = 0
    try:
        with open(summary_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check for genuine live status (not mock)
                if row.get("status") == "completed" and row.get("model") != "mock" and float(row.get("estimated_cost_usd", 0)) > 0:
                    count += 1
    except Exception:
        return 0
    return count

def audit_manuscript(file_path: Path, live_count: int) -> list[dict]:
    violations = []
    if not file_path.exists():
        return violations

    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    for line_idx, line in enumerate(lines, start=1):
        for pattern, reason in BANNED_BEHAVIORAL_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                # Check if it's already an explicit disavowal / negative citation
                if "ban on" in line.lower() or "prohibition against" in line.lower() or "not claim" in line.lower():
                    continue
                violations.append({
                    "file": file_path.name,
                    "line_number": line_idx,
                    "matched_text": line.strip()[:100],
                    "reason": reason
                })

    return violations

def main():
    print("=" * 70)
    print("CLAIM-EVIDENCE INTEGRITY GUARD AUDIT")
    print("=" * 70)

    live_count = get_live_trial_count()
    print(f"[*] Verified Completed Live Trials: {live_count}")

    if live_count == 0:
        print("[!] Operating under ZERO LIVE TRIALS constraint.")
        print("[*] Strict prohibition on unearned empirical/behavioral claims active.\n")

    all_violations = []
    for ms in MANUSCRIPTS:
        print(f"[*] Auditing: {ms.name}")
        violations = audit_manuscript(ms, live_count)
        if violations:
            print(f"    [-] Found {len(violations)} claim-evidence violations:")
            for v in violations:
                print(f"        Line {v['line_number']}: [{v['reason']}] -> \"{v['matched_text']}\"")
            all_violations.extend(violations)
        else:
            print("    [+] Zero claim-evidence violations. Clean!")

    print("\n" + "=" * 70)
    if all_violations:
        print(f"[FAILED] {len(all_violations)} claims exceed verified empirical evidence.")
        print("Remedy: Update manuscript to align assertions with verified measurements.")
        sys.exit(1)
    else:
        print("[PASSED] All manuscript claims match verified evidence level.")
        sys.exit(0)

if __name__ == "__main__":
    main()

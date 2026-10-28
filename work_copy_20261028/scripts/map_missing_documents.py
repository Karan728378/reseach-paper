"""
Script to search all markdown files in work_copy (excluding backups/)
for content corresponding to the 5 missing document names:
- README_REPRODUCE.md
- FINAL_RECOVERY_REPORT.md
- INDEPENDENT_STATISTICAL_AUDIT.md
- OBSERVATION_PIPELINE_AUDIT.md
- FINAL_SKEPTICAL_REVIEW.md
"""
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent

TARGETS = {
    "README_REPRODUCE.md": [
        "reproducibility", "reproduce", "quickstart", "how to reproduce", "replication guide"
    ],
    "FINAL_RECOVERY_REPORT.md": [
        "recovery report", "recovery", "project recovery", "forensic recovery", "final recovery"
    ],
    "INDEPENDENT_STATISTICAL_AUDIT.md": [
        "statistical audit", "independent statistical", "audit report", "cmh test", "power audit"
    ],
    "OBSERVATION_PIPELINE_AUDIT.md": [
        "observation pipeline", "pipeline audit", "serializer audit", "pruning mechanisms", "stage 4"
    ],
    "FINAL_SKEPTICAL_REVIEW.md": [
        "skeptical review", "skeptical", "examiner", "weakness register", "critique", "adversarial review"
    ]
}

def search_markdown_files():
    md_files = []
    for p in ROOT.rglob("*.md"):
        if "backups" in p.parts:
            continue
        md_files.append(p)

    print(f"Total non-backup markdown files found: {len(md_files)}")

    matches = {k: [] for k in TARGETS}

    for p in md_files:
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            continue
        rel = p.relative_to(ROOT)
        
        # Check title / first 10 lines
        first_lines = text.splitlines()[:15]
        header = "\n".join(first_lines)

        for target_name, keywords in TARGETS.items():
            score = 0
            found_kws = []
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', header, re.IGNORECASE):
                    score += 3
                    found_kws.append(f"header:{kw}")
                elif re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
                    score += 1
                    found_kws.append(f"body:{kw}")
            
            if score >= 3:
                excerpt = ""
                for idx, line in enumerate(first_lines[:8]):
                    if line.strip():
                        excerpt += f"L{idx+1}: {line.strip()[:100]} | "
                matches[target_name].append({
                    "path": str(rel),
                    "score": score,
                    "kws": found_kws[:4],
                    "excerpt": excerpt
                })

    for target_name, results in matches.items():
        print(f"\n=======================================================")
        print(f"Target: {target_name}")
        print(f"=======================================================")
        results.sort(key=lambda x: x["score"], reverse=True)
        for r in results[:5]:
            print(f"- File: {r['path']} (score: {r['score']}, matches: {r['kws']})")
            print(f"  Excerpt: {r['excerpt'][:160]}...")

if __name__ == "__main__":
    search_markdown_files()

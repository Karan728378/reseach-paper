import os
import hashlib
from pathlib import Path

targets = ['index.html', 'app-core.js', 'products.js']
search_roots = ['C:/testing']

print("Searching for candidate TechMart fixture files across C:/testing...")
candidates = []
for s_root in search_roots:
    for root, dirs, files in os.walk(s_root):
        for f in files:
            if f.lower() in targets:
                p = os.path.join(root, f)
                sz = os.path.getsize(p)
                h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
                candidates.append((p, sz, h))

print(f"\nFound {len(candidates)} candidate files:")
for p, sz, h in sorted(candidates):
    print(f"  {p} | {sz} bytes | {h}")

# Save report
out_p = Path('C:/testing/work_copy_20261028/results_v2/techmart_fixture_search_report.txt')
out_p.parent.mkdir(parents=True, exist_ok=True)
with open(out_p, 'w', encoding='utf-8') as f:
    f.write(f"TechMart Fixture Search Candidates ({len(candidates)} files found):\n")
    for p, sz, h in sorted(candidates):
        f.write(f"  {p} | {sz} bytes | {h}\n")
print(f"\nSaved search report to: {out_p}")

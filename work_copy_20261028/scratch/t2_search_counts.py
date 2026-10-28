import os, csv, json, re

work_dir = 'C:/testing/work_copy_20261028'

patterns = [
    re.compile(r'13\s*/\s*20'),
    re.compile(r'14\s*/\s*20'),
    re.compile(r'17\s*/\s*20'),
    re.compile(r'12\s*/\s*20'),
    re.compile(r'0\.65'),
    re.compile(r'0\.85'),
]

found_files = []
for root, dirs, files in os.walk(work_dir):
    rel_root = os.path.relpath(root, work_dir).replace('\\', '/')
    if rel_root.startswith('backups') or '/backups' in rel_root:
        continue
    for f in files:
        if f.endswith('.csv') or f.endswith('.json') or f.endswith('.py') or f.endswith('.md'):
            if f in ['research_paper_final.tex', '_baseline_manifest.csv']:
                continue
            p = os.path.join(root, f)
            try:
                content = open(p, 'r', encoding='utf-8', errors='ignore').read()
                matches = 0
                for pat in patterns:
                    if pat.search(content):
                        matches += 1
                if matches >= 3:
                    found_files.append((os.path.relpath(p, work_dir), matches))
            except Exception as e:
                pass

print(f"Searched files outside backups/. Found {len(found_files)} candidates with >= 3 match patterns:")
for path, count in sorted(found_files, key=lambda x: -x[1]):
    print(f"  {path} (pattern matches: {count})")

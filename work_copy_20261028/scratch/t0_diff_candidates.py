import os, hashlib, difflib, sys

sys.stdout.reconfigure(encoding='utf-8')
root_dir = 'C:/testing/work_copy_20261028'
root_tex_path = os.path.join(root_dir, 'research_paper_final.tex')

with open(root_tex_path, 'r', encoding='utf-8') as f:
    root_lines = f.readlines()
root_hash = hashlib.sha256(''.join(root_lines).encode('utf-8')).hexdigest()
root_size = os.path.getsize(root_tex_path)

print(f"ROOT: research_paper_final.tex | {root_size} bytes | SHA256: {root_hash}")

candidates = []
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if 'research_paper' in f and (f.endswith('.tex') or '.tex' in f):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, root_dir).replace('\\', '/')
            if rel_path == 'research_paper_final.tex':
                continue
            candidates.append(rel_path)

candidates.sort()

for rel_path in candidates:
    full_path = os.path.join(root_dir, rel_path)
    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
        cand_lines = f.readlines()
    cand_hash = hashlib.sha256(''.join(cand_lines).encode('utf-8')).hexdigest()
    cand_size = os.path.getsize(full_path)
    
    diff = list(difflib.unified_diff(
        root_lines, cand_lines,
        fromfile='root/research_paper_final.tex',
        tofile=rel_path,
        n=0
    ))
    plus_lines = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
    minus_lines = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
    
    print(f"\n--- Candidate: {rel_path} ---")
    print(f"Size: {cand_size} B | Hash: {cand_hash[:12]} | Diff vs Root: +{plus_lines} / -{minus_lines} lines")
    if diff:
        print("First 5 diff chunks:")
        for line in diff[:25]:
            print("  ", line.strip())

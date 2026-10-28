from pathlib import Path

root = Path("C:/testing")
for p in root.rglob("*schedule*"):
    if any(x in p.parts for x in [".git", ".venv311"]):
        continue
    rel = p.relative_to(root)
    print(f"{rel} ({p.stat().st_size:,} bytes)")

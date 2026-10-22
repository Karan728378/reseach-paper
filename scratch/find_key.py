import psutil
import os

found_keys = set()
for p in psutil.process_iter():
    try:
        env = p.environ()
        if env and 'GOOGLE_API_KEY' in env:
            val = env['GOOGLE_API_KEY']
            if val:
                found_keys.add(val)
                print(f"Found in pid {p.pid} ({p.name()}): {val[:5]}...")
    except Exception:
        pass

if found_keys:
    print(f"Total unique keys: {len(found_keys)}")
    with open("C:/testing/scratch/keys.txt", "w") as f:
        for k in found_keys:
            f.write(k + "\n")
else:
    print("NO KEYS FOUND IN ANY PROCESS")

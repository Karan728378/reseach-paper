import json
from pathlib import Path

p = Path("C:/testing/results/main_experiment/audit-logs/cc4954f0-b3db-4388-bf6a-633853240ddf.jsonl")
lines = open(p, "r", encoding="utf-8").readlines()
print(f"File has {len(lines)} lines")
for i, line in enumerate(lines):
    data = json.loads(line)
    print(f"Line {i}: keys = {list(data.keys())}")
    for k, v in data.items():
        if k in ("error", "error_message", "status", "action", "step", "model_output", "observation"):
            print(f"  {k}: {str(v)[:150]}")
    if i == 0 or i == len(lines)-1:
        print(f"  Full object: {json.dumps(data, indent=2)[:300]}...")

import json
import sys

p = r"C:\testing\results\main_experiment\agent-history\cc4954f0-b3db-4388-bf6a-633853240ddf.json"
with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

hist = data.get("history", [])
print(f"History length: {len(hist)}")

for i, step in enumerate(hist):
    print(f"\n--- STEP {i} ---")
    model_output = step.get("model_output")
    result = step.get("result")
    print(f"model_output is None? {model_output is None}")
    if model_output:
        print(f"model_output keys: {list(model_output.keys())}")
    print(f"result: {json.dumps(result, ensure_ascii=True)}")

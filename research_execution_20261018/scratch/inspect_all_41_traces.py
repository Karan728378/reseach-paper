import json
from pathlib import Path

runs_dir = Path("results/3arm_runs")

results = []

for idx in range(1, 42):
    # Find matching json
    if idx == 26:
        json_path = runs_dir / "run_026_attempt_4.json"
    else:
        json_path = runs_dir / f"run_{idx:03d}.json"
        
    if not json_path.exists():
        print(f"MISSING: {json_path}")
        continue
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    arm = data.get("arm")
    task_id = data.get("task_id")
    steps = data.get("total_steps")
    term_state = data.get("terminal_browser_state", {})
    cart = term_state.get("cart", [])
    order_conf = term_state.get("order_confirmed", False)
    last_items = term_state.get("last_order_items", [])
    v_res = data.get("verifier_result", {})
    final_text = data.get("agent_final_text", "")
    
    results.append({
        "idx": idx,
        "arm": arm,
        "task_id": task_id,
        "steps": steps,
        "cart_len": len(cart),
        "cart_skus": [c.get("sku") for c in cart if isinstance(c, dict)],
        "order_confirmed": order_conf,
        "last_order_skus": [c.get("sku") for c in last_items if isinstance(c, dict)],
        "verifier_score": v_res.get("score"),
        "final_text_excerpt": final_text[:80].replace("\n", " ") if final_text else ""
    })

print(f"Total traces audited: {len(results)}")

# Group by task_id
from collections import defaultdict
by_task = defaultdict(list)
for r in results:
    by_task[r["task_id"]].append(r)

for t in sorted(by_task.keys()):
    runs = by_task[t]
    print(f"\n=== TASK {t} ({len(runs)} runs) ===")
    for r in runs:
        if t in ["T1", "T2", "T3"]:
            print(f"  Run {r['idx']:02d} ({r['arm']}): steps={r['steps']}, cart_skus={r['cart_skus']}, score={r['verifier_score']}")
        elif t == "T4":
            print(f"  Run {r['idx']:02d} ({r['arm']}): steps={r['steps']}, confirmed={r['order_confirmed']}, last_items={r['last_order_skus']}, score={r['verifier_score']}")
        elif t == "T5":
            print(f"  Run {r['idx']:02d} ({r['arm']}): steps={r['steps']}, remaining_cart={r['cart_skus']}, score={r['verifier_score']}")
        elif t == "T6":
            print(f"  Run {r['idx']:02d} ({r['arm']}): steps={r['steps']}, text='{r['final_text_excerpt']}', score={r['verifier_score']}")

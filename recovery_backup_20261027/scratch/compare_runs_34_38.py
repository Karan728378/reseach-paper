import json
from pathlib import Path

runs_dir = Path("results/3arm_runs")

def compare_json_pair(name1, name2):
    p1 = runs_dir / name1
    p2 = runs_dir / name2
    with open(p1, "r", encoding="utf-8") as f:
        d1 = json.load(f)
    with open(p2, "r", encoding="utf-8") as f:
        d2 = json.load(f)
        
    lines = []
    lines.append(f"### Comparison: `{name1}` vs `{name2}`\n")
    all_keys = sorted(set(d1.keys()).union(set(d2.keys())))
    
    lines.append("| Field | Identical? | Details in " + name1 + " | Details in " + name2 + " |")
    lines.append("|---|---|---|---|")
    
    for k in all_keys:
        v1 = d1.get(k)
        v2 = d2.get(k)
        if k in ["action_history", "captured_observations"]:
            lines.append(f"| `{k}` | {'YES' if v1 == v2 else 'NO'} | {len(v1) if v1 else 0} entries | {len(v2) if v2 else 0} entries |")
        elif v1 != v2:
            s1 = json.dumps(v1, ensure_ascii=False)
            s2 = json.dumps(v2, ensure_ascii=False)
            if len(s1) > 100: s1 = s1[:100] + "..."
            if len(s2) > 100: s2 = s2[:100] + "..."
            lines.append(f"| `{k}` | **DIFFERS** | `{s1}` | `{s2}` |")
        else:
            s1 = json.dumps(v1, ensure_ascii=False)
            if len(s1) > 100: s1 = s1[:100] + "..."
            lines.append(f"| `{k}` | Identical | `{s1}` | `{s1}` |")

    lines.append("\n#### Detailed Action History Comparison\n")
    lines.append(f"**{name1} Actions:**")
    for act in d1.get("action_history", []):
        lines.append(f"- Step {act.get('step')}: {act.get('action')}")
    lines.append(f"\n**{name2} Actions:**")
    for act in d2.get("action_history", []):
        lines.append(f"- Step {act.get('step')}: {act.get('action')}")

    lines.append("\n#### Verifier & Terminal State Comparison\n")
    lines.append(f"- **{name1} Verifier Result:** {json.dumps(d1.get('verifier_result'), ensure_ascii=False)}")
    lines.append(f"- **{name2} Verifier Result:** {json.dumps(d2.get('verifier_result'), ensure_ascii=False)}")
    lines.append(f"- **{name1} Terminal State:** {json.dumps(d1.get('terminal_browser_state'), ensure_ascii=False)}")
    lines.append(f"- **{name2} Terminal State:** {json.dumps(d2.get('terminal_browser_state'), ensure_ascii=False)}")
    lines.append(f"- **{name1} Treatment Delivery:** {json.dumps(d1.get('treatment_delivery_evidence'), ensure_ascii=False)}")
    lines.append(f"- **{name2} Treatment Delivery:** {json.dumps(d2.get('treatment_delivery_evidence'), ensure_ascii=False)}")
    lines.append("\n---\n")
    return "\n".join(lines)

rep = ["# RUN 34 AND RUN 38 DEEP ATTEMPT COMPARISON REPORT\n"]
rep.append(compare_json_pair("run_034.json", "run_034_attempt_2.json"))
rep.append(compare_json_pair("run_038.json", "run_038_attempt_2.json"))

out_path = Path("COMPARE_RUNS_34_38_REPORT.md")
out_path.write_text("\n".join(rep), encoding="utf-8")
print(f"Wrote deep comparison report to {out_path}")

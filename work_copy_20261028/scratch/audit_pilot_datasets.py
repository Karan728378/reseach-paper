import csv
from pathlib import Path

def audit_pilot():
    raw_path = Path(r"C:\testing\results\pilot-summary.csv")
    clean_path = Path(r"C:\testing\results\pilot-summary-clean.csv")

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))
    with open(clean_path, "r", encoding="utf-8") as f:
        clean_rows = list(csv.DictReader(f))

    print(f"Raw rows: {len(raw_rows)}")
    print(f"Clean rows: {len(clean_rows)}")

    raw_succ = sum(1 for r in raw_rows if str(r.get("success", "")).strip().lower() in ("true", "1"))
    clean_succ = sum(1 for r in clean_rows if str(r.get("success", "")).strip().lower() in ("true", "1"))
    print(f"Raw success: {raw_succ}/{len(raw_rows)} ({raw_succ/len(raw_rows)*100:.2f}%)")
    print(f"Clean success: {clean_succ}/{len(clean_rows)} ({clean_succ/len(clean_rows)*100:.2f}%)")

    # Group by repetition_index
    reps_raw = {}
    for r in raw_rows:
        rep = r.get("repetition_index", "unknown")
        succ = str(r.get("success", "")).strip().lower() in ("true", "1")
        reps_raw.setdefault(rep, {"total": 0, "succ": 0, "fail": 0})
        reps_raw[rep]["total"] += 1
        if succ:
            reps_raw[rep]["succ"] += 1
        else:
            reps_raw[rep]["fail"] += 1

    print("\nRepetition breakdown in Raw Pilot (261 rows):")
    for rep in sorted(reps_raw.keys(), key=lambda x: int(x) if x.isdigit() else 99):
        info = reps_raw[rep]
        print(f"  Rep {rep:>2}: total={info['total']:>2}, succ={info['succ']:>2}, fail={info['fail']:>2}")

    # Inspect Rep 9 specifically
    rep9_fails = [r for r in raw_rows if r.get("repetition_index") == "9" and str(r.get("success", "")).strip().lower() in ("false", "0")]
    print(f"\nRep 9 failure count in raw: {len(rep9_fails)}")

    # Check Rep 9 in clean_rows
    rep9_clean = [r for r in clean_rows if r.get("repetition_index") == "9"]
    rep9_clean_fails = [r for r in rep9_clean if str(r.get("success", "")).strip().lower() in ("false", "0")]
    print(f"Rep 9 in clean: total={len(rep9_clean)}, fails={len(rep9_clean_fails)}")

    # Find the 11 excluded rows
    raw_ids = set(r["run_id"] for r in raw_rows)
    clean_ids = set(r["run_id"] for r in clean_rows)
    excluded_ids = raw_ids - clean_ids
    print(f"\nExcluded run_id count: {len(excluded_ids)}")
    excluded_rows = [r for r in raw_rows if r["run_id"] in excluded_ids]
    ex_fails = sum(1 for r in excluded_rows if str(r.get("success", "")).strip().lower() in ("false", "0"))
    ex_succs = sum(1 for r in excluded_rows if str(r.get("success", "")).strip().lower() in ("true", "1"))
    print(f"Excluded rows: {len(excluded_rows)} (failures={ex_fails}, successes={ex_succs})")
    for ex in excluded_rows:
        print(f"  - Rep {ex.get('repetition_index')}, {ex.get('variant')}, {ex.get('task_id')}, success={ex.get('success')}, error={ex.get('error_message')}")

if __name__ == "__main__":
    audit_pilot()

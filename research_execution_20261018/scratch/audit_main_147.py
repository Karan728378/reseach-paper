import csv
from pathlib import Path

def audit_main_147():
    p = Path(r"C:\testing\results\main_experiment\full-summary.csv")
    with open(p, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total rows in main experiment: {len(rows)}")
    runs_1_105 = rows[:105]
    runs_106_147 = rows[105:]

    s_105 = sum(1 for r in runs_1_105 if str(r.get("success", "")).strip().lower() in ("true", "1"))
    s_147 = sum(1 for r in runs_106_147 if str(r.get("success", "")).strip().lower() in ("true", "1"))

    print(f"Runs 1-105: {s_105}/105 successes ({s_105/105*100:.2f}%)")
    print(f"Runs 106-147: {s_147}/{len(runs_106_147)} successes ({s_147/len(runs_106_147)*100:.2f}%)")

    # Inspect runs 106-147 steps, duration, and error
    steps = set(r.get("total_steps") or r.get("steps") for r in runs_106_147)
    durations = [float(r.get("total_time_seconds") or r.get("duration", 0)) for r in runs_106_147]
    errors = set(r.get("error_message") or r.get("error") for r in runs_106_147)

    print(f"Runs 106-147 steps distribution: {steps}")
    print(f"Runs 106-147 duration range: {min(durations):.2f}s to {max(durations):.2f}s (mean={sum(durations)/len(durations):.2f}s)")
    print(f"Runs 106-147 unique error messages: {errors}")

    sample = runs_106_147[0]
    print(f"Sample collapse row 106: {sample}")

if __name__ == "__main__":
    audit_main_147()

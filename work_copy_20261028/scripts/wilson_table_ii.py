"""
Script to compute Wilson 95% Confidence Intervals for Table II and pilot success rates.
Formula:
  center = (p + z^2 / (2n)) / (1 + z^2 / n)
  half_width = (z / (1 + z^2 / n)) * sqrt(p(1-p)/n + z^2 / (4n^2))
  lower = max(0.0, center - half_width)
  upper = min(1.0, center + half_width)
"""
import math
import scipy.stats as stats

def wilson_score_interval(k, n, confidence=0.95):
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    z = stats.norm.ppf(1.0 - (1.0 - confidence) / 2.0)
    denom = 1.0 + (z**2) / n
    center = (p + (z**2) / (2.0 * n)) / denom
    half_width = (z / denom) * math.sqrt((p * (1.0 - p) / n) + ((z**2) / (4.0 * (n**2))))
    lower = max(0.0, center - half_width)
    upper = min(1.0, center + half_width)
    return p, lower, upper

def main():
    print("================================================================================")
    print("WILSON 95% CONFIDENCE INTERVALS FOR TABLE II & PILOT")
    print("================================================================================")
    
    # Table II Data:
    routes = [
        {"route": "#home", "ax": 336, "sel": 34, "op_k": 27, "sem_k": 26, "sem_n": 26},
        {"route": "#cart", "ax": 87, "sel": 8, "op_k": 8, "sem_k": 7, "sem_n": 7},
        {"route": "#checkout", "ax": 113, "sel": 13, "op_k": 13, "sem_k": 12, "sem_n": 12},
        {"route": "#search", "ax": 153, "sel": 19, "op_k": 16, "sem_k": 10, "sem_n": 10},
    ]

    print(f"{'Route':<12} | {'Operational (k/N)':<20} | {'Op. Rate [95% Wilson CI]':<30} | {'Sem. Rate [95% Wilson CI]'}")
    print("-" * 95)
    for r in routes:
        name = r["route"]
        op_k, op_n = r["op_k"], r["sel"]
        op_p, op_lo, op_hi = wilson_score_interval(op_k, op_n)
        
        sem_k, sem_n = r["sem_k"], r["sem_n"]
        sem_p, sem_lo, sem_hi = wilson_score_interval(sem_k, sem_n)
        
        op_str = f"{op_p*100:.1f}% [{op_lo*100:.1f}%, {op_hi*100:.1f}%]"
        sem_str = f"{sem_p*100:.1f}% [{sem_lo*100:.1f}%, {sem_hi*100:.1f}%]"
        print(f"{name:<12} | {op_k}/{op_n:<18} | {op_str:<30} | {sem_str}")

    print("\n--------------------------------------------------------------------------------")
    print("PILOT OUTCOME VALIDATION:")
    for label, k, n in [("Pilot All Completed", 41, 41), ("Pilot Primary Eligible", 39, 39)]:
        p, lo, hi = wilson_score_interval(k, n)
        print(f"  {label:<25}: {k}/{n} ({p*100:.1f}%) -> 95% Wilson CI: [{lo*100:.1f}%, {hi*100:.1f}%]  (exact: [{lo:.4f}, {hi:.4f}])")

if __name__ == '__main__':
    main()

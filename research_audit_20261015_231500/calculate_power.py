import math
from scipy import stats
import json
from pathlib import Path

AUDIT_DIR = Path(r"C:\testing\research_audit_20261015_231500")

def sample_size_two_proportions(p1, p2, alpha=0.05, power=0.80, two_sided=True):
    """
    Computes required sample size per group for comparing two independent proportions
    using normal approximation with pooled variance for null and unpooled for power.
    """
    z_alpha = stats.norm.ppf(1 - alpha / (2 if two_sided else 1))
    z_beta = stats.norm.ppf(power)
    
    p_bar = (p1 + p2) / 2
    q_bar = 1 - p_bar
    q1 = 1 - p1
    q2 = 1 - p2
    
    num = (z_alpha * math.sqrt(2 * p_bar * q_bar) + z_beta * math.sqrt(p1 * q1 + p2 * q2)) ** 2
    denom = (p1 - p2) ** 2
    n = num / denom
    return math.ceil(n)

def power_two_proportions(n, p1, p2, alpha=0.05, two_sided=True):
    """
    Computes power given n per group for two independent proportions.
    """
    z_alpha = stats.norm.ppf(1 - alpha / (2 if two_sided else 1))
    p_bar = (p1 + p2) / 2
    q_bar = 1 - p_bar
    q1 = 1 - p1
    q2 = 1 - p2
    
    delta = abs(p1 - p2)
    se_null = math.sqrt(2 * p_bar * q_bar / n)
    se_alt = math.sqrt((p1 * q1 + p2 * q2) / n)
    
    z = (delta - z_alpha * se_null) / se_alt
    return stats.norm.cdf(z)

def mcnemar_sample_size(p_disc, p_ratio, alpha=0.05, power=0.80):
    """
    Sample size for paired binary data (McNemar test).
    p_disc = proportion of discordant pairs (p10 + p01)
    p_ratio = p10 / (p10 + p01)
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    # Number of discordant pairs needed
    n_disc = ((z_alpha + z_beta * math.sqrt(4 * p_ratio * (1 - p_ratio))) / (2 * p_ratio - 1)) ** 2
    n_total = n_disc / p_disc
    return math.ceil(n_total)

scenarios = [
    # Baseline vs treatment differences
    {"name": "Large effect (90% vs 50%)", "p1": 0.90, "p2": 0.50},
    {"name": "Moderate effect (85% vs 60%)", "p1": 0.85, "p2": 0.60},
    {"name": "Small effect (85% vs 70%)", "p1": 0.85, "p2": 0.70},
    {"name": "Negative control vs channel (10% vs 80%)", "p1": 0.80, "p2": 0.10},
]

print("=== POWER AND SAMPLE SIZE AUDIT ===")
results = []
for sc in scenarios:
    p1, p2 = sc["p1"], sc["p2"]
    n80 = sample_size_two_proportions(p1, p2, alpha=0.05, power=0.80)
    n90 = sample_size_two_proportions(p1, p2, alpha=0.05, power=0.90)
    # Power with candidate n values
    power_n15 = power_two_proportions(15, p1, p2)
    power_n20 = power_two_proportions(20, p1, p2)
    power_n25 = power_two_proportions(25, p1, p2)
    power_n30 = power_two_proportions(30, p1, p2)
    
    res = {
        "scenario": sc["name"],
        "p1": p1,
        "p2": p2,
        "n_for_80pct_power": n80,
        "n_for_90pct_power": n90,
        "power_at_n15": round(power_n15, 3),
        "power_at_n20": round(power_n20, 3),
        "power_at_n25": round(power_n25, 3),
        "power_at_n30": round(power_n30, 3),
    }
    results.append(res)
    print(f"\nScenario: {sc['name']}")
    print(f"  P1={p1:.2f}, P2={p2:.2f} (Delta={abs(p1-p2):.2f})")
    print(f"  Required N per arm for 80% power: {n80}")
    print(f"  Required N per arm for 90% power: {n90}")
    print(f"  Power at N=15: {power_n15*100:.1f}%, N=20: {power_n20*100:.1f}%, N=25: {power_n25*100:.1f}%, N=30: {power_n30*100:.1f}%")

# Save results
out_file = AUDIT_DIR / "power_calculations.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print(f"\nCalculations saved to {out_file}")

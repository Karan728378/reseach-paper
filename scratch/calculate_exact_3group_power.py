"""
Calculate exact statistical power for the 3-group design:
- Group 1: Pooled Baseline (N=48)
- Group 2: ARIA (N=24)
- Group 3: DATA-CFG (N=24)

Evaluated under:
1. Nominal alpha = 0.05
2. Bonferroni adjusted alpha for 3 comparisons = 0.05 / 3 = 0.01667
3. Historical 4-group Bonferroni alpha = 0.05 / 6 = 0.00833
"""
import numpy as np
from scipy import stats

def compute_fisher_power(n1, n2, p1, p2, alpha=0.05):
    k1 = np.arange(n1 + 1)
    k2 = np.arange(n2 + 1)
    prob1 = stats.binom.pmf(k1, n1, p1)
    prob2 = stats.binom.pmf(k2, n2, p2)
    joint_prob = np.outer(prob1, prob2)
    rejections = np.zeros((n1 + 1, n2 + 1), dtype=bool)
    for x1 in range(n1 + 1):
        for x2 in range(n2 + 1):
            table = [[x1, n1 - x1], [x2, n2 - x2]]
            _, p_val = stats.fisher_exact(table)
            if p_val < alpha:
                rejections[x1, x2] = True
    return float(np.sum(joint_prob[rejections]))

alpha_nom = 0.05
alpha_bonf3 = 0.05 / 3 # 0.01667
alpha_bonf6 = 0.05 / 6 # 0.00833

print("=== EXACT POWER CALCULATIONS FOR 3-GROUP DESIGN ===")
print("\n--- 1. Pooled Baseline (N=48) vs ARIA or DATA-CFG (N=24) ---")
scenarios_pooled = [
    (0.10, 0.80, 0.70, "Large Disparity (Delta=0.70)"),
    (0.50, 0.85, 0.35, "Moderate Effect (Delta=0.35)"),
    (0.65, 0.85, 0.20, "Small Effect (Delta=0.20)"),
    (0.70, 0.85, 0.15, "Subtle Effect (Delta=0.15)")
]

for p1, p2, delta, label in scenarios_pooled:
    pow_nom = compute_fisher_power(48, 24, p1, p2, alpha_nom)
    pow_b3 = compute_fisher_power(48, 24, p1, p2, alpha_bonf3)
    pow_b6 = compute_fisher_power(48, 24, p1, p2, alpha_bonf6)
    print(f"{label}:")
    print(f"  Nominal alpha=0.05:             {pow_nom*100:5.1f}%")
    print(f"  Bonferroni-3 (alpha=0.0167):    {pow_b3*100:5.1f}%")
    print(f"  Bonferroni-6 (alpha=0.0083):    {pow_b6*100:5.1f}%")

print("\n--- 2. ARIA (N=24) vs DATA-CFG (N=24) ---")
scenarios_treat = [
    (0.50, 0.85, 0.35, "Moderate Effect (Delta=0.35)"),
    (0.65, 0.85, 0.20, "Small Effect (Delta=0.20)"),
    (0.70, 0.85, 0.15, "Subtle Effect (Delta=0.15)")
]

for p1, p2, delta, label in scenarios_treat:
    pow_nom = compute_fisher_power(24, 24, p1, p2, alpha_nom)
    pow_b3 = compute_fisher_power(24, 24, p1, p2, alpha_bonf3)
    pow_b6 = compute_fisher_power(24, 24, p1, p2, alpha_bonf6)
    print(f"{label}:")
    print(f"  Nominal alpha=0.05:             {pow_nom*100:5.1f}%")
    print(f"  Bonferroni-3 (alpha=0.0167):    {pow_b3*100:5.1f}%")
    print(f"  Bonferroni-6 (alpha=0.0083):    {pow_b6*100:5.1f}%")

print("\n--- 3. Comparison with Historical 24 vs 24 (Unpooled Baseline) ---")
for p1, p2, delta, label in scenarios_pooled:
    pow_24_nom = compute_fisher_power(24, 24, p1, p2, alpha_nom)
    pow_24_b6 = compute_fisher_power(24, 24, p1, p2, alpha_bonf6)
    pow_48_b3 = compute_fisher_power(48, 24, p1, p2, alpha_bonf3)
    print(f"{label}: Unpooled N=24 (Bonf-6) = {pow_24_b6*100:5.1f}%  -->  Pooled N=48 (Bonf-3) = {pow_48_b3*100:5.1f}% (Gain: +{(pow_48_b3-pow_24_b6)*100:4.1f}%)")

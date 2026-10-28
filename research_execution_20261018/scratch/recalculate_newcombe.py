import math

x1, n1 = 56, 70
x2, n2 = 38, 80
p1 = x1 / n1
p2 = x2 / n2
diff = p1 - p2
z = 1.959963984540054

print(f"p1 = {p1:.4f}, p2 = {p2:.4f}, diff = {diff:.4f}")

# 1. Wilson score without continuity correction
def wilson_uncc(x, n):
    p = x / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))) / denom
    return center - half, center + half

l1, u1 = wilson_uncc(x1, n1)
l2, u2 = wilson_uncc(x2, n2)
newcombe_uncc_lower = diff - math.sqrt((p1 - l1)**2 + (u2 - p2)**2)
newcombe_uncc_upper = diff + math.sqrt((u1 - p1)**2 + (p2 - l2)**2)

print(f"Wilson uncorrected: p1 in [{l1:.4f}, {u1:.4f}], p2 in [{l2:.4f}, {u2:.4f}]")
print(f"Newcombe Method 10 (without CC): [{newcombe_uncc_lower:.4f}, {newcombe_uncc_upper:.4f}]")

# 2. Wilson score with continuity correction
def wilson_cc(x, n):
    p = x / n
    denom = 2 * (n + z**2)
    # lower
    num_l = 2 * n * p + z**2 - 1 - z * math.sqrt(z**2 - 2 - 1/n + 4 * p * (n * (1 - p) + 1))
    # upper
    num_u = 2 * n * p + z**2 + 1 + z * math.sqrt(z**2 + 2 - 1/n + 4 * p * (n * (1 - p) - 1))
    return num_l / denom, num_u / denom

l1_cc, u1_cc = wilson_cc(x1, n1)
l2_cc, u2_cc = wilson_cc(x2, n2)
newcombe_cc_lower = diff - math.sqrt((p1 - l1_cc)**2 + (u2_cc - p2)**2)
newcombe_cc_upper = diff + math.sqrt((u1_cc - p1)**2 + (p2 - l2_cc)**2)
print(f"Wilson with CC: p1 in [{l1_cc:.4f}, {u1_cc:.4f}], p2 in [{l2_cc:.4f}, {u2_cc:.4f}]")
print(f"Newcombe Method 11 (with CC): [{newcombe_cc_lower:.4f}, {newcombe_cc_upper:.4f}]")

# 3. Wald interval
se_wald = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
wald_lower = diff - z * se_wald
wald_upper = diff + z * se_wald
print(f"Wald 95% CI: [{wald_lower:.4f}, {wald_upper:.4f}]")

# 4. Agresti-Caffo
p1_ac = (x1 + 1) / (n1 + 2)
p2_ac = (x2 + 1) / (n2 + 2)
diff_ac = p1_ac - p2_ac
se_ac = math.sqrt(p1_ac * (1 - p1_ac) / (n1 + 2) + p2_ac * (1 - p2_ac) / (n2 + 2))
ac_lower = diff_ac - z * se_ac
ac_upper = diff_ac + z * se_ac
print(f"Agresti-Caffo 95% CI: [{ac_lower:.4f}, {ac_upper:.4f}]")

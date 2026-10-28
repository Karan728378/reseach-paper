import math

def wilson_interval(x, n, alpha=0.05):
    p = x / n
    z = 1.959963984540054  # for alpha = 0.05 (two-sided)
    denom = 1.0 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))) / denom
    return (center - half, center + half)

def newcombe_diff_interval(x1, n1, x2, n2, alpha=0.05):
    l1, u1 = wilson_interval(x1, n1, alpha)
    l2, u2 = wilson_interval(x2, n2, alpha)
    p1 = x1 / n1
    p2 = x2 / n2
    diff = p1 - p2
    
    lower = diff - math.sqrt((p1 - l1)**2 + (u2 - p2)**2)
    upper = diff + math.sqrt((u1 - p1)**2 + (p2 - l2)**2)
    return (p1, l1, u1), (p2, l2, u2), diff, (lower, upper)

p1_stats, p2_stats, diff, ci = newcombe_diff_interval(56, 70, 38, 80)
print(f"p1 = {p1_stats[0]:.4f} [{p1_stats[1]:.4f}, {p1_stats[2]:.4f}]")
print(f"p2 = {p2_stats[0]:.4f} [{p2_stats[1]:.4f}, {p2_stats[2]:.4f}]")
print(f"Diff = {diff:.4f}, Newcombe 95% CI = [{ci[0]:.4f}, {ci[1]:.4f}]")

# Also check 27/34 and 41/41 and 13/13 Wilson intervals
w_27_34 = wilson_interval(27, 34)
w_41_41 = wilson_interval(41, 41)
w_13_13 = wilson_interval(13, 13)
print(f"27/34 Wilson CI: [{w_27_34[0]*100:.2f}%, {w_27_34[1]*100:.2f}%]")
print(f"41/41 Wilson CI: [{w_41_41[0]*100:.2f}%, {w_41_41[1]*100:.2f}%]")
print(f"13/13 Wilson CI: [{w_13_13[0]*100:.2f}%, {w_13_13[1]*100:.2f}%]")

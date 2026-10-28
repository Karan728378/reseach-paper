import math

def norm_ppf(p):
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0, 1)")
    if p < 0.5:
        return -norm_ppf(1.0 - p)
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1.0)

def tost_n(p, margin=0.10, alpha=0.05, power=0.80, joint=True):
    z_alpha = norm_ppf(1.0 - alpha)
    # If joint power is 1 - beta, each tail gets (1 + power)/2 or beta/2
    z_beta = norm_ppf((1.0 + power) / 2.0) if joint else norm_ppf(power)
    var = 2.0 * p * (1.0 - p)
    n = ((z_alpha + z_beta) * math.sqrt(var) / margin) ** 2
    return n

print("=== TOST SAMPLE SIZE AUDIT ===")
for p in [0.50, 0.65, 0.70, 0.75, 0.80]:
    for alpha in [0.05, 0.01667]:
        n_joint = tost_n(p, margin=0.10, alpha=alpha, power=0.80, joint=True)
        n_indiv = tost_n(p, margin=0.10, alpha=alpha, power=0.80, joint=False)
        print(f"p={p:.2f}, alpha={alpha:.5f} -> Joint N={n_joint:.1f} (ceil {math.ceil(n_joint)}), Indiv N={n_indiv:.1f} (ceil {math.ceil(n_indiv)})")

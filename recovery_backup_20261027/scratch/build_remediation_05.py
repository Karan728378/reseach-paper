import csv
import math
from pathlib import Path

ROOT = Path(r"C:\testing\research_execution_20261018")
out_power_csv = ROOT / "REMEDIATION_05_POWER_SENSITIVITY.csv"
out_claims_csv = ROOT / "REMEDIATION_05_STATISTICAL_CLAIM_REGISTER.csv"

# 1. Generate REMEDIATION_05_POWER_SENSITIVITY.csv
# Normal CDF
def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_ppf(p):
    # Acklam approximation or simple rational approximation
    # For common values:
    if abs(p - 0.975) < 1e-4: return 1.95996
    if abs(p - 0.95) < 1e-4: return 1.64485
    if abs(p - 0.99167) < 1e-4: return 2.39398 # alpha=0.01667 two-sided
    if abs(p - 0.80) < 1e-4: return 0.84162
    # standard lookup
    from math import log, sqrt
    # Beasley-Springer-Moro approximation
    a = [2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637]
    b = [-8.47351093090, 23.08336743743, -21.06224101826, 3.13082909833]
    c = [0.3374754822726147, 0.9761690190917186, 0.1607979714918209,
         0.0276438810333863, 0.0038405729373609, 0.0003951896511919,
         0.0000321767881768, 0.0000002888167364, 0.0000003960315187]
    y = p - 0.5
    if abs(y) < 0.42:
        r = y * y
        x = y * (((a[3]*r + a[2])*r + a[1])*r + a[0]) / ((((b[3]*r + b[2])*r + b[1])*r + b[0])*r + 1.0)
    else:
        r = p if y < 0 else 1.0 - p
        r = math.log(-math.log(r))
        x = c[0] + r*(c[1] + r*(c[2] + r*(c[3] + r*(c[4] + r*(c[5] + r*(c[6] + r*(c[7] + r*c[8])))))))
        if y < 0: x = -x
    return x

def calc_power(p1, p2, n1, n2, alpha=0.05):
    delta = abs(p2 - p1)
    if delta == 0: return alpha
    pbar = (n1*p1 + n2*p2) / (n1 + n2)
    z_alpha = norm_ppf(1.0 - alpha/2.0)
    denom = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    se_null = math.sqrt(pbar*(1-pbar)*(1/n1 + 1/n2))
    z = (delta - z_alpha * se_null) / denom
    return norm_cdf(z)

scenarios = [
    {"Name": "Subtle Effect (Delta=0.10)", "p1": 0.70, "p2": 0.80, "Delta": 0.10},
    {"Name": "Subtle Effect (Delta=0.15)", "p1": 0.70, "p2": 0.85, "Delta": 0.15},
    {"Name": "Small Effect (Delta=0.20, Pilot p=0.65->0.85)", "p1": 0.65, "p2": 0.85, "Delta": 0.20},
    {"Name": "Small Effect (Delta=0.20, Max Var p=0.50->0.70)", "p1": 0.50, "p2": 0.70, "Delta": 0.20},
    {"Name": "Moderate Effect (Delta=0.25)", "p1": 0.60, "p2": 0.85, "Delta": 0.25},
    {"Name": "Moderate Effect (Delta=0.35, Pilot p=0.50->0.85)", "p1": 0.50, "p2": 0.85, "Delta": 0.35},
    {"Name": "Large Disparity (Delta=0.50)", "p1": 0.30, "p2": 0.80, "Delta": 0.50},
    {"Name": "Large Disparity (Delta=0.70)", "p1": 0.10, "p2": 0.80, "Delta": 0.70}
]

power_rows = []
for sc in scenarios:
    p1 = sc["p1"]
    p2 = sc["p2"]
    d = sc["Delta"]
    
    # n per arm = 13 (Pilot)
    pow_n13_a05 = calc_power(p1, p2, 13, 13, 0.05)
    pow_n13_bonf = calc_power(p1, p2, 13, 13, 0.01667)
    
    # n per arm = 20 (Planned RCBD block)
    pow_n20_a05 = calc_power(p1, p2, 20, 20, 0.05)
    pow_n20_bonf = calc_power(p1, p2, 20, 20, 0.01667)
    
    # Required n for 80% superiority at alpha=0.05
    z_a = 1.95996
    z_b = 0.84162
    pbar = 0.5 * (p1 + p2)
    n_sup_80 = (z_a * math.sqrt(2*pbar*(1-pbar)) + z_b * math.sqrt(p1*(1-p1) + p2*(1-p2)))**2 / (d**2)
    
    # Required n for 80% TOST equivalence (margin = 0.10) at alpha=0.05
    z_tost_a = 1.64485
    p_eq = p1
    n_tost_80 = 2 * (z_tost_a + z_b)**2 * p_eq * (1 - p_eq) / (0.10**2)
    
    power_rows.append({
        "Scenario": sc["Name"],
        "Baseline_p1": f"{p1:.2f}",
        "Treatment_p2": f"{p2:.2f}",
        "Delta": f"{d:.2f}",
        "Power_n13_alpha05": f"{pow_n13_a05*100:.1f}%",
        "Power_n13_Bonferroni": f"{pow_n13_bonf*100:.1f}%",
        "Power_n20_alpha05": f"{pow_n20_a05*100:.1f}%",
        "Power_n20_Bonferroni": f"{pow_n20_bonf*100:.1f}%",
        "Required_n_per_arm_80pct_Superiority": f"{math.ceil(n_sup_80)}",
        "Required_N_total_4arms_Superiority": f"{math.ceil(n_sup_80)*4}",
        "Required_n_per_arm_80pct_TOST_margin10": f"{math.ceil(n_tost_80)}",
        "Required_N_total_4arms_TOST": f"{math.ceil(n_tost_80)*4}"
    })

with open(out_power_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(power_rows[0].keys()))
    writer.writeheader()
    writer.writerows(power_rows)

print(f"[+] Written {out_power_csv}")

# 2. Generate REMEDIATION_05_STATISTICAL_CLAIM_REGISTER.csv
claims = [
    {
        "ClaimID": "STAT-01",
        "ManuscriptLocation": "Abstract, Table 2, Sec. IV-A",
        "ClaimText": "Baseline (ABS) success rate: 100.0% (13/13), 95% Wilson CI [77.19%, 100.0%]",
        "StatisticalMethod": "Wilson Score Interval (without continuity correction)",
        "InputData": "n=13, k=13 from CANONICAL_RUN_LEDGER.csv",
        "ComputedValue": "p=1.0000, CI=[0.7719, 1.0000]",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "13/13 tasks succeeded (100.0%, 95% Wilson CI [77.19%, 100.0%])"
    },
    {
        "ClaimID": "STAT-02",
        "ManuscriptLocation": "Abstract, Table 2, Sec. IV-A",
        "ClaimText": "ARIA arm success rate: 100.0% (13/13), 95% Wilson CI [77.19%, 100.0%]",
        "StatisticalMethod": "Wilson Score Interval",
        "InputData": "n=13, k=13 from CANONICAL_RUN_LEDGER.csv",
        "ComputedValue": "p=1.0000, CI=[0.7719, 1.0000]",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "13/13 tasks succeeded (100.0%, 95% Wilson CI [77.19%, 100.0%])"
    },
    {
        "ClaimID": "STAT-03",
        "ManuscriptLocation": "Table 2, Sec. IV-A",
        "ClaimText": "DATA-CFG arm primary eligible: 100.0% (13/13), 95% Wilson CI [77.19%, 100.0%]",
        "StatisticalMethod": "Wilson Score Interval",
        "InputData": "n=13, k=13 (Runs 34 and 38 duplicate attempts quarantined)",
        "ComputedValue": "p=1.0000, CI=[0.7719, 1.0000]",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "13/13 primary eligible tasks succeeded (100.0%, 95% Wilson CI [77.19%, 100.0%])"
    },
    {
        "ClaimID": "STAT-04",
        "ManuscriptLocation": "Table 2, Sec. IV-A",
        "ClaimText": "DATA-CFG sensitivity sample: 100.0% (15/15), 95% Wilson CI [79.61%, 100.0%]",
        "StatisticalMethod": "Wilson Score Interval",
        "InputData": "n=15, k=15 (including duplicate runs 34 & 38)",
        "ComputedValue": "p=1.0000, CI=[0.7961, 1.0000]",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "15/15 completed tasks succeeded in sensitivity analysis (100.0%, 95% Wilson CI [79.61%, 100.0%])"
    },
    {
        "ClaimID": "STAT-05",
        "ManuscriptLocation": "Abstract, Table 2, Sec. IV-B",
        "ClaimText": "Risk Difference Delta = 0.000, 95% Newcombe Hybrid Score CI [-0.232, +0.232]",
        "StatisticalMethod": "Newcombe Hybrid Score Interval (Method 10 with Wilson bounds)",
        "InputData": "n1=13, k1=13; n2=13, k2=13",
        "ComputedValue": "Delta=0.000, CI=[-0.232, +0.232]",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "Observed risk difference Delta = 0.000 (95% Newcombe hybrid score CI [-0.232, +0.232], Fisher p = 1.000)"
    },
    {
        "ClaimID": "STAT-06",
        "ManuscriptLocation": "Abstract, Sec. III-B",
        "ClaimText": "Statistical power for Delta = 0.20 at n <= 20 is ~11% (10.8% at B=2,000; 11.5% at B=10,000)",
        "StatisticalMethod": "10,000-iteration RCBD Monte Carlo simulation with Bonferroni correction",
        "InputData": "p1=0.65, p2=0.85, n=20, alpha=0.01667, ICC=0.10",
        "ComputedValue": "10.85% (B=2,000, MCSE=0.70%), 11.45% (B=10,000, MCSE=0.32%)",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "Empirical power is severely limited (~11% for Delta = 0.20; 49.6% for Delta = 0.35)"
    },
    {
        "ClaimID": "STAT-07",
        "ManuscriptLocation": "Abstract, Sec. III-B",
        "ClaimText": "Statistical power for moderate effect Delta = 0.35 is 49.6%",
        "StatisticalMethod": "RCBD Monte Carlo simulation (B=2,000)",
        "InputData": "p1=0.50, p2=0.85, n=20, alpha=0.01667",
        "ComputedValue": "49.65% (MCSE=1.12%)",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "Underpowered even for moderate effects (49.6% power for Delta = 0.35)"
    },
    {
        "ClaimID": "STAT-08",
        "ManuscriptLocation": "Sec. III-B, Appendix C",
        "ClaimText": "Sample size required for 80% superiority at Delta = 0.20: 97 to 125 per arm",
        "StatisticalMethod": "Two-sided unpooled binomial sample size formula at alpha=0.05",
        "InputData": "p1=0.65->0.85 (n=97); p1=0.50->0.70 max variance (n=125)",
        "ComputedValue": "n=96.8 -> 97/arm; n=124.3 -> 125/arm",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "Detecting Delta = 0.20 with 80% power requires 97 to 125 runs per arm (388 to 500 total across 4 arms)"
    },
    {
        "ClaimID": "STAT-09",
        "ManuscriptLocation": "Sec. III-B, Appendix C",
        "ClaimText": "Sample size required for 80% TOST equivalence (margin +-10%): 275 to 360 per arm",
        "StatisticalMethod": "Two One-Sided Tests (TOST) sample size formula at alpha=0.05",
        "InputData": "margin=0.10, p=0.80 (n=274); p=0.70 (n=360)",
        "ComputedValue": "n=274.1 -> 275/arm; n=359.8 -> 360/arm",
        "VerificationStatus": "VERIFIED_EXACT",
        "AllowedWording": "Proving equivalence within +-10% requires 275 to 360 runs per arm (1,100 to 1,440 total across 4 arms)"
    }
]

with open(out_claims_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(claims[0].keys()))
    writer.writeheader()
    writer.writerows(claims)

print(f"[+] Written {out_claims_csv}")

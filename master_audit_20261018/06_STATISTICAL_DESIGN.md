# Statistical Design Document
**Audit Date:** 2026-10-18

## Primary Outcome
Binary task success: `Y_ijk ∈ {0,1}` for arm `i`, task `j`, block `k`.

## Primary Analysis
- **Unit of analysis:** Single agent run (arm × task × block).
- **Test:** Two-sided Fisher exact test for each pairwise arm comparison on pooled success rates.
- **Multiple comparisons:** Bonferroni correction over C(4,2)=6 pairwise tests → α_adj = 0.05/6 = 0.0083.
- **Effect size:** Risk difference (RD) with 95% CI (Wilson score interval).

## Secondary Analysis
- Mixed-effects logistic regression: `logit(P(success)) ~ arm + task + (1|block)`.
- Block included as random effect to account for within-block correlation.
- Task included as fixed effect covariate.

## Power Summary (two-proportion z-test, two-sided α=0.05)

| Contrast | p₁ | p₂ | Δ | Power (N=24) | Power (N=30) |
|----------|----|----|---|--------------|--------------|
| ABS_vs_VIS_presence_vs_absence | 0.1 | 0.8 | 0.70 | 100.0% | 100.0% |
| VIS_vs_ARIA_large_channel_degradation | 0.85 | 0.5 | 0.35 | 75.1% | 84.3% |
| VIS_vs_DATA_CFG_moderate_channel_effect | 0.85 | 0.65 | 0.20 | 35.6% | 43.0% |
| ARIA_vs_DATA_CFG_small_channel_effect | 0.85 | 0.7 | 0.15 | 23.3% | 28.2% |

## Pre-Registration Requirements
The following must be pre-registered (e.g., OSF) BEFORE data collection:
1. Primary outcome definition (binary success, not partial_score).
2. Primary contrast (ABS vs VIS).
3. Stopping rule: complete all 4 blocks; no interim analysis.
4. Missing-data handling: MCAR assumed within complete blocks; partial blocks excluded.
5. Verifier version hash (SHA-256 of `verifier.py` at experiment start).

## Quota Stopping Rule
- Abort experiment after 3 consecutive HTTP 429 errors.
- Any complete block (24 runs) at time of abort is retained for analysis.
- Partial blocks are excluded to maintain balance.
- Minimum analyzable dataset: 1 complete block (24 runs, 6 per arm) — underpowered but balanced.

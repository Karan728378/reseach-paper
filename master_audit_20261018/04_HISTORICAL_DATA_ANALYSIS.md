# Historical Data Analysis
**Audit Date:** 2026-10-18
**Source:** `results/main_experiment/full-summary.csv`

## Run Counts

| | Total | Before Quota Failure (valid) | After Quota Failure (contaminated) |
|-|-------|-----------------------------|------------------------------------|
| Runs | 147 | 105 | 42 |
| Successes | 105 | 105 | 0 (all failed) |

## Quota Failure Signature
All 42 runs from scheduled_run_index 106 onward:
- `total_steps == 7` (immediate abort)
- `total_time_seconds < 12s`
- `success == False`
- `partial_score` values: T4 shows 0.25 (verifier flaw), all others 0.0

This pattern is consistent with HTTP 429 RESOURCE_EXHAUSTED causing the runner to
log a failure immediately after the API call errors out.

## Per-Variant × Per-Task Success Matrix (VALID RUNS ONLY, n≤105)

> ⚠️ These rates are still contaminated by T3/T4/T5 verifier flaws.

| Variant | T1 | T2 | T3 | T4 | T5 |
|---------|----|----|----|----|-----|
| v0-baseline | 6/6 (100%) | 4/4 (100%) | 6/6 (100%) | 7/7 (100%) | 7/7 (100%) |
| v1-jsonld | 8/8 (100%) | 6/6 (100%) | 4/4 (100%) | 2/2 (100%) | 3/3 (100%) |
| v2-aria | 5/5 (100%) | 3/3 (100%) | 7/7 (100%) | 7/7 (100%) | 4/4 (100%) |
| v3-data-attrs | 7/7 (100%) | 7/7 (100%) | 2/2 (100%) | 5/5 (100%) | 5/5 (100%) |

## Key Observations

1. **All variants show near-100% success on valid runs** — consistent with either genuine high performance OR verifier flaws inflating scores.
2. **T4 success requires checkout completion** — most T4 successes involve 8–10 steps and 50–80s, consistent with real checkout navigation.
3. **T2 and T3 complete in 3–4 steps** — fast success pattern suggests agent finds target directly.
4. **No valid cross-arm statistical test is possible** from historical data due to:
   - Non-randomized sequential blocking
   - MNAR quota truncation
   - Verifier contamination on T3, T4, T5

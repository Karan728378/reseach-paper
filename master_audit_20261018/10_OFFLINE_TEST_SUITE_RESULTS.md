# Offline Test Suite Results
**Audit Date:** 2026-10-18
**Execution mode:** 100% offline, zero API calls, read-only

## Summary
**17/17 PASSED · 0 FAILED**

## Test Results

| Test | Status | Details |
|------|--------|---------|
| `A1_variant_html_exists_v0-baseline` | ✅ PASS | C:\testing\variants\v0-baseline\index.html |
| `A1_variant_html_exists_v1-jsonld` | ✅ PASS | C:\testing\variants\v1-jsonld\index.html |
| `A1_variant_html_exists_v2-aria` | ✅ PASS | C:\testing\variants\v2-aria\index.html |
| `A1_variant_html_exists_v3-data-attrs` | ✅ PASS | C:\testing\variants\v3-data-attrs\index.html |
| `A2_task_definitions_valid_json` | ✅ PASS | 5 tasks found |
| `A3_summary_csv_columns` | ✅ PASS | rows=147 |
| `B1_quota_failure_runs_detected` | ✅ PASS | Runs with 7 steps & <12s (quota signature): 42 |
| `B2_successful_runs_min_steps` | ✅ PASS | 105 successful runs checked |
| `C1_serializer_file_exists` | ✅ PASS | C:\testing\.venv311\Lib\site-packages\browser_use\dom\serializer\serializer.py |
| `C2_script_in_DISABLED_ELEMENTS` | ✅ PASS | 'script' confirmed in DISABLED_ELEMENTS |
| `C3_aria_label_in_DEFAULT_INCLUDE_ATTRIBUTES` | ✅ PASS | 'aria-label' confirmed in DEFAULT_INCLUDE_ATTRIBUTES |
| `C4_data_lot_code_NOT_in_default` | ✅ PASS | data-lot-code absent from DEFAULT_INCLUDE_ATTRIBUTES |
| `D1_T3_target_sku_is_wh002` | ✅ PASS | target_sku=wh-002 |
| `D2_T5_has_setup_script` | ✅ PASS | setup_script present |
| `F1_block_arithmetic_24x4_96` | ✅ PASS | K=4, J=6, R=4, block_size=24, total=96 |
| `G1_power_ABS_vs_VIS_at_N24_gt99pct` | ✅ PASS | Power=100.0% |
| `G2_power_ARIA_vs_DATA_at_N24_small_effect` | ✅ PASS | Power=23.3% (confirms N=24 insufficient for delta=0.15 equivalence claims) |

## Test Group Breakdown

| Group | Tests | Passed | Failed |
|-------|-------|--------|--------|
| A — File integrity | 6 | 6 | 0 |
| B — Historical data | 2 | 2 | 0 |
| C — Pipeline trace | 4 | 4 | 0 |
| D — Task/verifier | 2 | 2 | 0 |
| F — Design arithmetic | 1 | 1 | 0 |
| G — Statistical power | 2 | 2 | 0 |

> Full machine-readable results: `offline_test_results.json`

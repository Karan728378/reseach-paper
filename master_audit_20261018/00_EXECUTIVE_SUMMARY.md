# Master Audit — Executive Summary
**Project:** `C:\testing` — Browser-Agent Information Channel Benchmark
**Audit Date:** 2026-10-18
**Mode:** 100% Offline · Zero API Calls · Zero Source-File Modifications
**Generated:** 2026-10-18T08:24:39.230490+00:00

---

## Verdict: NOT READY FOR PUBLICATION · READY FOR REDESIGNED EXPERIMENT

The historical main experiment (148 runs, 2026-10-11) contains **four fatal flaws** that invalidate
any cross-arm success-rate comparisons. A redesigned Protocol v3 (RCBD, N=96) is scientifically
sound but requires five blocking items to be resolved before execution.

---

## Offline Test Results
**17/17 tests passed** (see `offline_test_results.json`)

---

## Fatal Flaws in Historical Experiment

| # | Flaw | Impact |
|---|------|--------|
| 1 | **Quota truncation** — 42 runs aborted with HTTP 429 at run #106 | MNAR right-truncation; v3/v2 under-sampled |
| 2 | **Sequential blocking** — variants run in variant-order blocks | Any truncation creates differential missingness |
| 3 | **v1-jsonld arm is ABS-equivalent** — `script` in `DISABLED_ELEMENTS` | JSON-LD token never reached LLM; arm tests hallucination not channel |
| 4 | **v3-data-attrs arm is ABS-equivalent** (in historical runs) — custom `data-*` stripped by `DEFAULT_INCLUDE_ATTRIBUTES` | Data-attr token never reached LLM |

### Verifier Flaws (affect all existing results)
| Task | Flaw | Severity |
|------|------|----------|
| T3 | Accepted lowest-rated item (wh-001) as success | CRITICAL |
| T4 | Unconditional partial score on failure | MODERATE |
| T5 | Empty-cart success without pre-run state verification | CRITICAL |

---

## Protocol v3 Blocking Items (must fix before execution)

1. **Redesign or drop v1-jsonld arm** — replace with explicit ABS control or a truly observable channel.
2. **Patch runner `DEFAULT_INCLUDE_ATTRIBUTES`** to include `data-*` names for DATA-CFG arm.
3. **Set `use_vision=False`** in agent initialization to eliminate vision confound for VIS arm.
4. **Fix verifier T3/T4/T5 flaws** as specified in `protocol_manifest.json`.
5. **Use RCBD block randomization** (not sequential) — already specified in Protocol v3.

---

## Statistical Power (N=96, 24 per arm)
| Contrast | Delta | Power |
|----------|-------|-------|
| ABS vs VIS (presence/absence) | 0.70 | >99.9% |
| VIS vs ARIA (large degradation) | 0.35 | 87.8% |
| VIS vs DATA-CFG (moderate) | 0.20 | 55.4% |
| ARIA vs DATA-CFG (small) | 0.15 | 36.2% |

> **Warning:** N=96 is underpowered for delta ≤ 0.15. Do not make equivalence claims for small effects.

---

## Key Files
| Deliverable | Path |
|-------------|------|
| This summary | `master_audit_20261018/00_EXECUTIVE_SUMMARY.md` |
| File integrity manifest | `master_audit_20261018/file_integrity.csv` |
| Offline test results | `master_audit_20261018/offline_test_results.json` |
| Power analysis | `master_audit_20261018/power_analysis.json` |
| Protocol manifest | `master_audit_20261018/protocol_manifest.json` |
| Audit phases A–I detail | `master_audit_20261018/01_AUDIT_PHASES_DETAIL.md` |
| Raw command log | `master_audit_20261018/commands_and_outputs.txt` |

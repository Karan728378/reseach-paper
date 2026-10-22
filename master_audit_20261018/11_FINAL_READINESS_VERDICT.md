# Final Protocol-Freeze Readiness Verdict
**Audit Date:** 2026-10-18
**Auditor:** Master Audit Script (offline, automated)

---

## Verdict: ❌ NOT READY TO FREEZE

The proposed Protocol v3 is **scientifically well-designed** but has **5 blocking implementation
items** that must be resolved before protocol freeze and execution.

---

## Blocking Items

| Priority | Item | Evidence |
|----------|------|----------|
| P0 | Fix T3 verifier: accept only `cart_exact_match(wh-002)` | `runner/verifier.py ~L350-420` |
| P0 | Fix T5 verifier: require pre-run `wh-001` in cart | `tasks/task-definitions.json T5.setup_script` |
| P0 | Set `use_vision=False` in agent runner | `runner/agent-runner.py` (BrowserSession init) |
| P1 | Patch `include_attributes` to add `data-*` names for DATA-CFG arm | `browser_use.dom.views.DEFAULT_INCLUDE_ATTRIBUTES` |
| P1 | Replace v1-jsonld arm (currently ABS-equivalent) | Redesign as explicit ABS-2 or drop to 3-arm design |

---

## Confirmed Ready Items

| Item | Evidence |
|------|----------|
| TechMart website (v0-baseline, v2-aria, v3-data-attrs, v4-evidence-meta) | Variant HTML files exist and pass file-existence checks |
| Task definitions T1–T5 (JSON) | `tasks/task-definitions.json` protocol v2 |
| ARIA channel delivery (v2-aria) | `aria-label` confirmed in `DEFAULT_INCLUDE_ATTRIBUTES` |
| RCBD block design (4 arms × 6 tasks × 4 blocks = 96 runs) | Design specification verified arithmetically |
| Statistical power for primary contrasts (ABS vs VIS, VIS vs ARIA) | >80% at N=24/arm for delta≥0.30 |
| Quota guard design | Specified in `08_QUOTA_AND_COST_PLAN.md` |

---

## Post-Fixes Readiness Path

```
1. Implement all 5 blocking items
2. Run offline verifier tests (run: python runner/verifier.py)
3. Run smoke test: 1 RCBD block (24 runs) against localhost
4. Verify per-arm success rates plausible (ABS < VIS ≈ ARIA)
5. Pre-register protocol on OSF
6. Execute full 96-run experiment with paid API key
7. Analyze with Fisher exact + Bonferroni
```

---

## Audit Confidence Levels

| Claim | Confidence | Basis |
|-------|-----------|-------|
| v1-jsonld arm is ABS-equivalent | HIGH | Confirmed in serializer.py DISABLED_ELEMENTS |
| v3-data-attrs stripped by default | HIGH | Confirmed in views.py DEFAULT_INCLUDE_ATTRIBUTES |
| Historical quota failure at run #106 | HIGH | CSV pattern (7 steps, <10s, all fail) |
| T3 verifier flaw | HIGH | Code inspection + task-definitions.json v2 vs v1 mismatch |
| T5 verifier flaw | MODERATE | Code inspection; would require live test to fully confirm |
| Power estimates | HIGH | Exact two-proportion z-test formula, zero external deps |
| Novelty claim | INFERRED | Literature not exhaustively searched (offline mode) |

---

*Audit complete. All deliverables written to `C:\testing\master_audit_20261018`. Awaiting your approval before any protocol changes or experiment execution.*

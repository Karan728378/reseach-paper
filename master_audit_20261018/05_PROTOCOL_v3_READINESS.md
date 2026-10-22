# Protocol v3 Readiness Assessment
**Audit Date:** 2026-10-18

## Design Specification

| Parameter | Value |
|-----------|-------|
| Design | Randomized Complete Block Design (RCBD) |
| Arms (K) | 4: ABS, VIS, ARIA, DATA-CFG |
| Tasks (J) | 6: T1–T6 |
| Blocks (R) | 4 |
| Block size | K × J = 24 runs |
| Total runs | 96 |
| Primary outcome | Binary success per run (0/1) |
| Statistical test | Fisher exact, pairwise; Bonferroni α=0.0083 |
| Agent | browser-use 0.13.10 + Gemini (paid tier) |
| Vision | `use_vision=False` (eliminates vision confound) |

## Blocking Items (MUST resolve before execution)

| # | Item | Blocker Type | Resolution |
|---|------|-------------|------------|
| 1 | v1-jsonld arm blocked by DISABLED_ELEMENTS | Design | Replace with explicit ABS-2 or drop; use 3-arm design |
| 2 | v3-data-attrs requires runner patch | Implementation | Add `data-warranty`, `data-lot-code`, etc. to `include_attributes` in agent init |
| 3 | use_vision=False not enforced in runner | Implementation | Set `use_vision=False` in `agent-runner.py` BrowserSession init |
| 4 | T3/T4/T5 verifier flaws | Implementation | Rewrite verifier functions per `03_VERIFIER_FLAW_REPORT.md` |
| 5 | No pre-run cart state assertion | Implementation | Add JS pre-check before agent launch in runner |

## Items Confirmed Ready

| Item | Status |
|------|--------|
| Website (TechMart) variants exist and load | ✅ READY |
| Task definitions (T1–T5) defined in JSON | ✅ READY |
| aria-label delivery (v2-aria / ARIA arm) | ✅ READY |
| VIS arm delivery (v0-baseline) | ✅ READY |
| RCBD block randomization design | ✅ DESIGNED (not yet implemented in runner) |
| Statistical power (ABS vs VIS, large effects) | ✅ ADEQUATE (>80% for delta≥0.30) |

## Power Warning

| Contrast | Delta | Power at N=24/arm |
|----------|-------|-------------------|
| ABS vs VIS | 0.70 | >99.9% ✅ |
| VIS vs ARIA | 0.35 | 87.8% ✅ |
| VIS vs DATA-CFG | 0.20 | 55.4% ⚠️ |
| ARIA vs DATA-CFG | 0.15 | 36.2% ❌ |

Do NOT interpret p>0.05 as equivalence for ARIA vs DATA-CFG at N=24.

## Readiness Verdict

**CONDITIONAL NOT READY.**  
The experimental design is sound. Five blocking implementation items must be resolved.
Upon resolution, a smoke test (1 block, 24 runs) is recommended before full execution.

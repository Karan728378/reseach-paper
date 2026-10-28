# Evidence-to-Claim Matrix (Final Correction Pass v2)

**Manuscript:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Correction Pass Date:** 2026-10-26
**Auditor:** Final Correction Pass (Problems 1-5 per user mandate)

---

| Claim ID | Claim Text | Primary Evidence | Evidence Type | Evidential Scope | Section | OK? |
|:---:|:---|:---|:---|:---|:---:|:---:|
| C1 | browser-use 0.13.10 unconditionally prunes script/meta via DISABLED_ELEMENTS | serializer.py:18; test_observation_pipeline_stages.py PASS | Static AST + offline test | browser-use 0.13.10 only | 3.1 | YES |
| C2 | Schema.org JSON-LD 0% reachability to LLM prompt | serializer.py:18; intercepted prompts in test_sentinel_pipeline.py | Dynamic trace (offline) | Same version/config scope | 3.1,4.2 | YES |
| C3 | Non-interactive element tags+attrs stripped | serializer.py:1046-1058; test_sentinel_pipeline.py PASS | Static AST + offline test | Same scope | 3.2,4.4 | YES |
| C4 | Custom data-* omitted by default whitelist | views.py:18-45; test_agent_prompt_pipeline.py PASS | Static AST + offline test | Same scope | 3.3 | YES |
| C5 | 27/34 selector elements (79.4%) match Blink AXNodes on #home | accessibility_tree_comparison.json; compare_accessibility_tree.py | CDP measurement on local fixture | Route #home; local e-commerce only | 4.3 | YES+CI |
| C6 | Multi-route: 100% semantic correspondence across 4 routes | scratch/run_phase_b_browser_experiments.py; Table 2 | CDP measurement | 4 local fixture routes only | 4.3 | YES (scoped) |
| C7 | All genuine interactive controls match AXTree (100%) | CDP node matching; accessibility_tree_comparison.json | CDP measurement | Local fixture only | 4.3 | YES |
| C8 | Action-Label Co-Location Confound present + fixed | shared/app-core.js:243; test_treatment_leakage_and_integrity.py | Code audit + test | Within study HTML fixtures | 5.1 | YES |
| C9 | 41-trial cloud pilot: 41/41 score 1.0 (ceiling effect) | results/v3_3arm_summary.csv; 46 JSON traces | Live experimental records (pilot) | 3 arms; simple tasks; ceiling disclosed | 5.3 | YES (pilot only) |
| C10 | Confirmatory Phase 2: 0 completed runs | Budget ledger 604/600; no Phase 2 JSONs | Absence of records + budget ceiling | Definitive | Limitations | YES |
| C11 | Local qwen3:4b runs hit 180s watchdog (context expansion) | results/local_llama_summary.csv; run_003 telemetry | Execution trace | 5 diagnostic runs; specific hardware | App.A | YES |
| C12 | TOST equiv requires N>=1080 (3 arms, p=0.70) | reproduce_power_audit.py; test_power_audit.py PASS | Analytical derivation | Stated assumptions | 6.3 | YES |
| C13 | n=20/arm has <11% power for Delta=0.20 | power_analysis.py; 10k-trial Monte Carlo | Simulation | Stated assumptions; theoretical | 6.2 | YES (labeled synthetic) |
| C14 | Quota guardrail halts at 600; ledger at 604 | budget_controller.py; test_runner_guard_integration.py; ledger | Code audit + test | Single-process Python runtime | App.C | YES |
| C15 | 138 unit/regression tests pass 100% | python -m unittest discover 2026-10-26: 138 OK in 13.5s | Live test run (verified) | 19 test_*.py files; offline; no API | App.D | YES |
| C16 | Synthetic appendix tables labeled as synthetic | Appendix A disclaimer; test_scratch_synthetic_data/ | Document label | Disclaimer in paper | App.A | YES |

---
## Prohibited Claims - All Confirmed ABSENT from Manuscript

- Confirmatory experiments established treatment superiority: ABSENT
- Semantic markup improves agent task success: ABSENT  
- Local model failures = LLM reasoning failures: ABSENT
- Results generalize beyond browser-use 0.13.10: ABSENT
- Findings generalize beyond tested routes/fixtures: ABSENT
- Synthetic data presented as real empirical evidence: ABSENT

---
Matrix produced by final correction pass v2 on 2026-10-26.

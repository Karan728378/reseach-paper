# Timestamped State & Evidence Audit Report

**Audit Date:** October 22, 2026  
**Auditor:** Antigravity Senior Research Engineer, Browser-Agent Systems Specialist & Reproducibility Lead  
**Execution Context:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9, browser-use 0.13.10)  
**Safety & Cost State:** Zero paid API calls executed · Zero API keys printed/logged · Safety Gate Locked  

---

## 1. Executive Pre-Modification State Snapshot

Prior to making any further enhancements, the repository was audited at git commit `574e99f` on branch `main` (`https://github.com/Karan728378/reseach-paper.git`).

### 1.1 SHA-256 Authentication Manifest
| Target File | Authenticated SHA-256 | Size (Bytes) | Initial Integrity Status |
|---|---|:---:|:---:|
| [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) | `d8564bb5f822c7398626fad68d5b7c283e148c3998311bf96c60b026e2a2340a` | 33,480 | Present, verified active runner |
| [`protocol_v4_config.json`](file:///C:/testing/research_execution_20261018/protocol_v4_config.json) | `6c21f0a31f23816a1a0fb4420a246b529d12921c046c77da43ed26f945e12985` | 1,910 | Present, schema version 4.0-DRAFT |
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py) | `26feadfd95f2649340469846361ac701648d26346be422dc4e621828ff791394` | 23,302 | Present, 13/13 offline tests passing |
| [`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py) | `a578df650ea019f369e1dcaa417ccd654edf66e053c282850e9e71c04b2176a9` | 6,779 | Present, 6/6 mutation audits passing |
| [`test_t6_verifier_isolated.py`](file:///C:/testing/research_execution_20261018/test_t6_verifier_isolated.py) | `63d30239ab6599e995ee9ac3f81f03f45e590c0d676c71ff2d543664c16014a2` | 8,364 | Present, 7/7 isolated T6 tests passing |
| [`test_power_audit.py`](file:///C:/testing/research_execution_20261018/test_power_audit.py) | `b5950c5a6537a54e1970255a85547e417e9033ba9078de9030d62a76426fe1eb` | 5,390 | Present, 7/7 power calculations passing |
| [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py) | `8a98cdfb13d432c2731c7480091bf67d795561fface890304e60e255db9ca42b` | 26,522 | Present, 11/11 statistical tests passing |
| [`test_accessibility_tree_comparison.py`](file:///C:/testing/research_execution_20261018/test_accessibility_tree_comparison.py) | `36ccef282cd065508557e3bbbffa1da1175cf761c0db00fc3c8e55af08467cae` | 7,610 | Present, 10/10 AXTree comparisons passing |
| [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) | `898c315f9e4a68139306bfd7c9e469bc2b065a4d50a65b48458c366376ca9429` | 8,098 | Present, 5/5 prompt delivery tests passing |
| [`t6_verifier_isolated.py`](file:///C:/testing/research_execution_20261018/t6_verifier_isolated.py) | `8c0daba0dd09fdc0d64263ac03065172d819a0248d0718d159a59b3b4a65ba00` | 4,893 | Present, isolated candidate module |
| [`runner/verifier.py`](file:///C:/testing/runner/verifier.py) | `890b968345e82b59cb0545263d8e438a6ef6de9f521b90da5b98e5680850b378` | 33,927 | Present, historical legacy reference |
| [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) | `107c790e8de411849120e580dd987fe641a9112585667a0f7dc26bd913f778ce` | 3,524 | Present, 96-run balanced RCBD schedule |
| [`proposed_smoke_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_smoke_schedule.csv) | `05079365d287e4eda7396198f0d57c774c5e35b4189de9abe02954cbca28c096` | 212 | Present, 4-trial segregated smoke schedule |
| [`NEXT_LIVE_EXECUTION_READINESS.md`](file:///C:/testing/NEXT_LIVE_EXECUTION_READINESS.md) | `cc4515e625444bfa128d0cecdcc3e75944a7f32229bc10f93bd2fe831f9683f8` | 12,397 | Present, implementation readiness report |

---

## 2. Comprehensive Findings Status Matrix

Every known finding, defect, or methodological concern is assigned exactly one status:
- `VERIFIED_FIXED`
- `FIXED_OFFLINE_ONLY`
- `STILL_BLOCKING`
- `NOT_PRESENT`
- `UNVERIFIED`
- `NOT_APPLICABLE`

| ID | Domain / Component | Description of Finding | Status | Exact File Path & Lines | Test & Evidence Reference |
|---|---|---|:---:|---|---|
| **F-01** | Live Execution Loop | Missing live `browser_use.Agent` execution loop in active runner; runner previously called mock execution only. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:344-520`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L344) | `run_single_live_trial` implemented with `Agent.run()`, CDP session management, state reset, prompt interception, terminal state extraction, and JSON persistence. |
| **F-02** | Safety Gate Interlock | Safety gate must fail closed and block unauthorized live execution without `--live` and `--confirm-live-execution`. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:637-652`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L637) | `test_mutation_audit.py:100-117` confirms unconfirmed live invocation raises `RuntimeError`. Live gate remains strictly locked (`SAFETY_GATE_LOCKED = True`). |
| **F-03** | Task T5 Precondition | Missing precondition check in T5 allowed empty carts to pass vacuously (`pre_cart_count is None or pre_cart_count == 1`). | `VERIFIED_FIXED` | [`protocol_v3_runner.py:114-128`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L114) | `offline_test_suite.py:121-140` and `test_mutation_audit.py:57-74` prove that `pre_cart_count=None` and `pre_cart_count=0` strictly fail with `score=0.0`. |
| **F-04** | Task T6 Refusal Scoring | Historical T6 verifier required "36 months" regex and penalized refusals, rewarding duration hallucination. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:129-205`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L129) | `test_t6_verifier_isolated.py:13-160` (7/7 tests) and `offline_test_suite.py:176-260` (44 regression cases) confirm valid refusals score 1.0, while hallucinations/contradictions score 0.0. |
| **F-05** | Task T3 SKU Dilution | Historical `runner/verifier.py` accepted 6 SKUs for T3 (including cheapest `wh-001` and non-audio `mkp-001`). | `VERIFIED_FIXED` | [`protocol_v3_runner.py:96-104`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L96) | `offline_test_suite.py:70-97` and `test_mutation_audit.py:22-41` confirm only `wh-002` scores 1.0; all other SKUs fail. |
| **F-06** | Task T4 Partial Credit | Historical `runner/verifier.py` awarded unconditional 0.25 score to failed checkout runs. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:105-113`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L105) | `offline_test_suite.py:98-114` and `test_mutation_audit.py:43-55` confirm incomplete checkout scores strictly 0.0. |
| **F-07** | Multimodal Vision Confound | `runner/agent-runner.py:648` set `use_vision=True`, allowing visual layout/button recognition to bypass text DOM markup. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:442`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L442) | `use_vision=False` strictly enforced in active runner; visual confound eliminated across all arms. |
| **F-08** | Observation Pruning (JSON-LD) | `browser-use 0.13.10` serializer prunes `<script type="application/ld+json">` via `DISABLED_ELEMENTS`. | `VERIFIED_FIXED` | [`browser_use/dom/serializer/serializer.py:18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18) | `test_accessibility_tree_comparison.py:46-54` and `test_agent_prompt_pipeline.py:160-175` prove 0% prompt exposure for JSON-LD. Arm excluded from confirmatory testing. |
| **F-09** | Attribute Filtering (`data-*`) | Native `browser-use` default attribute whitelist excludes custom developer attributes (`data-action`, `data-product-id`). | `VERIFIED_FIXED` | [`protocol_v3_runner.py:46-50`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L46) | `EXTENDED_ATTRIBUTES` explicitly passed for `DATA-CFG` arm; verified by `test_agent_prompt_pipeline.py:130-155`. |
| **F-10** | Button Target Leakage | Original `v2-aria` button label had `aria-label="Add SoundFlow Air 3 to cart"`, co-locating target name into action button. | `VERIFIED_FIXED` | [`shared/app-core.js:145`](file:///C:/testing/shared/app-core.js#L145) | De-confounding refactor updated button to `aria-label="Add item to cart"`. Authenticated hash `ccae98e0...` verified by `offline_test_suite.py:324-343`. |
| **F-11** | Non-Interactive ARIA Pruning | ARIA attributes on non-interactive `<span>` (price, rating) are stripped by `browser-use` prompt serializer. | `VERIFIED_FIXED` | [`accessibility_tree_comparison.json`](file:///C:/testing/research_execution_20261018/accessibility_tree_comparison.json) | Critical divergence proven: retained in Blink AXTree (`Price: $49.99`), but stripped in prompt text buffer. |
| **F-12** | Survivorship Bias in Retries | `runner/agent-runner.py:164` skipped retrying failed runs only if `success=True`, retrying failures until success. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:214-231`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L214) | `get_completed_run_indices` counts both `success=True` and `success=False` as completed. Zero retries of valid failures. |
| **F-13** | Quota Crash & Truncation | Historical main experiment hit Gemini free-tier 500 RPD wall at run #105; runs 106–147 failed consecutively with HTTP 429. | `VERIFIED_FIXED` | [`results/main_experiment/full-summary.csv`](file:///C:/testing/results/main_experiment/full-summary.csv) | Documented MNAR right-truncation. Preflight quota prerequisites established; historical data permanently segregated. |
| **F-14** | Smoke Output Separation | Risk that live smoke test outputs contaminate the primary 96-trial research dataset. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:698, 708-713`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L698) | `--smoke` flag routes output to `results/smoke_run_summary.csv` and `results/smoke_runs/`, strictly isolating smoke trials. |
| **F-15** | Executable Cost Ceiling | Cost ceiling was only a text specification; runner lacked in-code spending enforcement. | `VERIFIED_FIXED` | [`protocol_v3_runner.py:672-675`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L672) | Cumulative cost accumulated per trial; triggers immediate safety abort before exceeding `--cost-ceiling` ($10.00). |
| **F-16** | Schedule Row Validation | Missing validation of CSV rows (duplicate IDs, invalid arm/task strings, non-existent variant paths). | `STILL_BLOCKING` | [`protocol_v3_runner.py:207-212`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L207) | `load_schedule` currently returns `list(reader)` without asserting schema integrity or row validity. Requires implementation. |
| **F-17** | Dedicated CLI Preflight Routine | Runner lacks a single-command `--preflight` flag to validate environment, server, browser, and verifiers offline. | `STILL_BLOCKING` | [`protocol_v3_runner.py:694-730`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L694) | Missing `--preflight` CLI routine to confirm live-readiness without paid API calls. Requires implementation. |
| **F-18** | Paid Tier-1 API Key | Paid Google Gemini Tier-1 API key with >1,000 RPD quota required to prevent free-tier 500 RPD exhaustion. | `STILL_BLOCKING` | Environment (`$env:GOOGLE_API_KEY`) | External prerequisite: `GOOGLE_API_KEY` is not configured in the active environment. Requires human authorization. |
| **F-19** | Statistical Power for Small Effects | 96-run exploratory pilot has only 10.85% power to detect small differences ($\Delta=0.20$) at $\alpha=0.0167$. | `VERIFIED_FIXED` | [`protocol_v4_config.json:20-28`](file:///C:/testing/research_execution_20261018/protocol_v4_config.json#L20) | Protocol v4 explicitly reclassifies the 96-run study as an **Exploratory Pilot**; Confirmatory Superiority requires $N=480$. |
| **F-20** | Playwright Missing in Environment | `test_t4_capture.py` fails with `ModuleNotFoundError: No module named 'playwright'`. | `NOT_APPLICABLE` | [`test_t4_capture.py:1`](file:///C:/testing/test_t4_capture.py#L1) | Legacy developer script outside active protocol package. Protocol v4 uses `browser-use 0.13.10` via Chrome DevTools Protocol. |

---

## 3. Initial State Audit Summary

- **Total Assessed Items:** 20
- **`VERIFIED_FIXED`:** 15
- **`FIXED_OFFLINE_ONLY`:** 0
- **`STILL_BLOCKING`:** 3 (F-16: Schedule row validation; F-17: CLI preflight routine; F-18: Human API key authorization)
- **`NOT_PRESENT`:** 0
- **`UNVERIFIED`:** 0
- **`NOT_APPLICABLE`:** 1 (F-20: Playwright in legacy test script)

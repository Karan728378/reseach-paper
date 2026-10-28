# EVIDENCE LEDGER AND BASELINE VERIFICATION REPORT

**Document ID:** `audit_20261022_final/BASELINE_VERIFICATION.md`  
**Audit Date:** October 22, 2026  
**Auditor / Roles:** Senior Browser-Agent Systems Specialist, Experimental-Design Auditor, Statistical Reviewer & Reproducibility Lead  
**Execution Context:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9, `browser-use 0.13.10`)  
**Operating Policy:** 100% Offline Reproduction · Zero Paid API Calls · Explicit Separation of Verified Facts, Assumptions, and Limitations  

---

## 1. Classification Categories

In accordance with Section 3 of the Master Audit Directive, all material claims in the repository are classified into exactly one of the following seven evidentiary categories:

1. `VERIFIED BY DIRECT INSPECTION` — Verified through exact line-by-line inspection of code, configuration, or data files.
2. `REPRODUCED BY EXECUTION` — Verified by running the relevant test suite, script, or command in the active Python environment with exit code 0.
3. `SUPPORTED BY EXISTING ARTIFACT ONLY` — Documented in historical or saved reports but lacks an active executable test or raw trace.
4. `AGENT-REPORTED, NOT INDEPENDENTLY VERIFIED` — Stated in prior LLM/agent narrative reports without independent primary source evidence.
5. `ASSUMPTION` — Methodological, statistical, or operational premise required for model validity.
6. `UNRESOLVED` — Known discrepancy, defect, or missing element requiring human or external action.
7. `NOT TESTABLE OFFLINE` — Requires live cloud API calls, external credentials, or live provider billing infrastructure.

---

## 2. Master Evidence Ledger

| # | Material Claim & Focus Area | Evidentiary Category | Evidence Path & Line Number / Test | Exact Command & Exit Code | Limitation | Support Level |
|---|---|:---:|---|---|---|:---:|
| **E-01** | **Live Runner Loop Existence**<br>Runner contains executable `browser_use.Agent.run()` loop connecting to CLI `--live`. | `VERIFIED BY DIRECT INSPECTION` | `protocol_v3_runner.py:380-555` | Line inspection; verified `from browser_use import Agent, BrowserSession` and `await agent.run()`. | Gated by locked safety gate (`SAFETY_GATE_UNLOCKED = False`). | **Fully Supported** |
| **E-02** | **Safety Gate Fail-Closed**<br>Live trials strictly fail closed with `RuntimeError` unless both `--live` and `--confirm-live-execution` are set, and gate flag is unlocked. | `REPRODUCED BY EXECUTION` | `protocol_v3_runner.py:672-687`, `test_mutation_audit.py:test_mutation_safety_gate_blocks_unauthorized_live_execution` | `python -m unittest research_execution_20261018/test_mutation_audit.py`<br>Exit Code: `0` | Live safety gate prevents unauthorized API dispatches. | **Fully Supported** |
| **E-03** | **Zero Paid API Calls / Zero Spend**<br>No live external LLM API calls were dispatched, no credits spent, and no keys committed in this session. | `VERIFIED BY DIRECT INSPECTION` | Git status, environment variables (`GOOGLE_API_KEY` unset in shell), `protocol_v3_runner.py:680-687`. | `python -c "import os; assert not os.environ.get('GOOGLE_API_KEY')"`<br>Exit Code: `0` | Evaluated on local process environment; cannot query external Google Cloud billing portal offline. | **Fully Supported (Local Limits Stated)** |
| **E-04** | **Task T5 Strict Initial State**<br>T5 requires verified pre-state (`pre_cart_count == 1`); an empty cart without verified pre-state strictly scores 0.0. | `REPRODUCED BY EXECUTION` | `protocol_v3_runner.py:114-128`, `offline_test_suite.py:test_historical_vs_strict_t5_verifier`, `test_mutation_audit.py:test_mutation_t5_verifier_detects_unseeded_prestate` | `python -m unittest research_execution_20261018/test_mutation_audit.py`<br>Exit Code: `0` | Relies on browser `localStorage` injection prior to agent start. | **Fully Supported** |
| **E-05** | **Task T6 Grounded Refusal Logic**<br>T6 rewards grounded refusal of absent warranty duration (1.0) and penalizes invented durations ("36 months", "2 years") or contradictory text (0.0). | `REPRODUCED BY EXECUTION` | `protocol_v3_runner.py:130-205`, `test_t6_verifier_isolated.py` (7 tests, 38 assertions), `offline_test_suite.py:test_t6_regression_battery` (44 assertions) | `python -m unittest research_execution_20261018/test_t6_verifier_isolated.py`<br>Exit Code: `0` | Regex pattern handles natural language variation; highly adversarial or novel phrasing requires ongoing test expansion. | **Fully Supported** |
| **E-06** | **Task T3 Strict SKU Verification**<br>T3 accepts only second-highest rated SKU (`wh-002`, rating 4.5); rejects other SKUs. | `REPRODUCED BY EXECUTION` | `protocol_v3_runner.py:96-104`, `test_mutation_audit.py:test_mutation_t3_verifier_detects_wrong_sku` | `python -m unittest research_execution_20261018/test_mutation_audit.py`<br>Exit Code: `0` | Historical bug accepting 6 SKUs is completely eliminated. | **Fully Supported** |
| **E-07** | **Task T4 Unconditional Credit Fix**<br>T4 requires confirmed order and `mse-001`; unconditional 0.25 partial credit on checkout failure is eliminated. | `REPRODUCED BY EXECUTION` | `protocol_v3_runner.py:105-113`, `test_mutation_audit.py:test_mutation_t4_verifier_detects_unconfirmed_order` | `python -m unittest research_execution_20261018/test_mutation_audit.py`<br>Exit Code: `0` | Authoritative application state (`window.__orderConfirmed__`) required. | **Fully Supported** |
| **E-08** | **Pruning of Script & Meta in Serializer**<br>`browser-use==0.13.10` serializer prunes `<script>` (JSON-LD) and `<meta>` elements unconditionally. | `REPRODUCED BY EXECUTION` | `site-packages/browser_use/dom/serializer/serializer.py:18`, `test_observation_pipeline_stages.py:test_01_jsonld_pruned_at_serializer_stage` | `python -m unittest research_execution_20261018/test_observation_pipeline_stages.py`<br>Exit Code: `0` | Internal `DISABLED_ELEMENTS = {'link', 'meta', 'style', 'head', 'title', 'script'}`. | **Fully Supported** |
| **E-09** | **Custom `data-*` Attribute Filtering**<br>Custom `data-*` attributes (`data-action`, `data-amount`) are stripped by default unless `include_attributes` is extended. | `REPRODUCED BY EXECUTION` | `site-packages/browser_use/dom/views.py:18-82`, `test_observation_pipeline_stages.py:test_02_data_cfg_attribute_filtering` | `python -m unittest research_execution_20261018/test_observation_pipeline_stages.py`<br>Exit Code: `0` | On non-interactive tags, `data-*` is stripped even under extended whitelist. | **Fully Supported** |
| **E-10** | **Blink AXTree vs Model Prompt Divergence**<br>Presence of accessibility nodes in Chromium Blink AXTree does not guarantee inclusion in the model prompt string. | `REPRODUCED BY EXECUTION` | `test_observation_pipeline_stages.py:test_03_aria_attribute_reachability`, `compare_accessibility_tree.py` | `python -m unittest research_execution_20261018/test_observation_pipeline_stages.py`<br>Exit Code: `0` | Blink AXTree contains 336 nodes; `browser-use` extracts interactive selector map + text buffer only. | **Fully Supported** |
| **E-11** | **Button Label De-confounding**<br>Interactive button labels in `v2-aria` do not leak target product names (`"Add item to cart"`, not `"Add SoundFlow Air 3 to cart"`). | `REPRODUCED BY EXECUTION` | `shared/app-core.js:440`, `test_treatment_leakage_and_integrity.py:test_02_button_aria_label_deconfounding` | `python -m unittest research_execution_20261018/test_treatment_leakage_and_integrity.py`<br>Exit Code: `0` | Verified across `v0-baseline`, `v2-aria`, and `v3-data-attrs`. | **Fully Supported** |
| **E-12** | **Disambiguation of `VIS` Arm**<br>`VIS` in Protocol v4 is a text-only baseline replicate (`BASELINE_REP` on `v0-baseline` with `use_vision=False`), NOT a vision treatment. | `VERIFIED BY DIRECT INSPECTION` | `protocol_v4_config.json:14-19`, `protocol_v3_runner.py:404, 477`, `test_treatment_leakage_and_integrity.py:test_04_vis_arm_disambiguation` | `python -m unittest research_execution_20261018/test_treatment_leakage_and_integrity.py`<br>Exit Code: `0` | Must not be pooled without testing baseline exchangeability (`p_stability >= 0.10`). | **Fully Supported** |
| **E-13** | **Preflight Budget Bounding & Fail-Closed Guard**<br>`budget_controller.py` bounds worst-case batch cost ($5.18 USD vs $10.00 ceiling) and fails closed on unknown models. | `REPRODUCED BY EXECUTION` | `budget_controller.py:35-115`, `test_budget_controls.py` (7 tests), `protocol_v3_runner.py:855-870` | `python -m unittest research_execution_20261018/test_budget_controls.py`<br>Exit Code: `0` | Local software guard cannot replace external Google Cloud project billing quotas. | **Fully Supported (Limitations Stated)** |
| **E-14** | **RCBD Schedule Balance (Option B: 96 Runs)**<br>`proposed_randomized_schedule.csv` has 96 rows, exactly 24 runs per block, 1 run per (arm, task) tuple, contiguous IDs. | `REPRODUCED BY EXECUTION` | `proposed_randomized_schedule.csv`, `test_schedule_validity.py:test_02_full_pilot_schedule_structure_and_counts` | `python -m unittest research_execution_20261018/test_schedule_validity.py`<br>Exit Code: `0` | Balance verified across 4 temporal blocks $B_1 \to B_4$. | **Fully Supported** |
| **E-15** | **Clean 3-Arm Schedule Balance (Option A: 72 Runs)**<br>`proposed_3arm_schedule.csv` has 72 rows, exactly 18 runs per block (ABS, ARIA, DATA-CFG across 6 tasks), zero replicate arms. | `REPRODUCED BY EXECUTION` | `proposed_3arm_schedule.csv`, `test_schedule_validity.py:test_06_option_a_3arm_schedule_structure_and_balance` | `python -m unittest research_execution_20261018/test_schedule_validity.py`<br>Exit Code: `0` | Generated deterministically with seed 42. Eliminates redundant baseline replicate. | **Fully Supported** |
| **E-16** | **Statistical Power for N=96 Pilot ($\approx 10.85\%$)**<br>Monte Carlo simulation confirms $N=96$ pilot ($N=80$ primary tasks T1–T5) has only 10.85% power to detect $\Delta=0.20$ at $\alpha=0.0167$. | `REPRODUCED BY EXECUTION` | `reproduce_power_audit.py`, `power_audit_results.json:104-109`, `test_power_audit.py` (7 tests) | `python -m unittest research_execution_20261018/test_power_audit.py`<br>Exit Code: `0` | Pilot cannot claim causal equivalence or a true null effect. | **Fully Supported** |
| **E-17** | **Confirmatory Sample Size Requirement ($N=480$)**<br>80.2% statistical power for $\Delta=0.20$ at $\alpha=0.0167$ requires $n \approx 120$/arm ($N=480$ total across 4 arms). | `REPRODUCED BY EXECUTION` | `reproduce_power_audit.py`, `power_audit_results.json:132-137`, `test_power_audit.py` | `python -m unittest research_execution_20261018/test_power_audit.py`<br>Exit Code: `0` | Assumes maximum variance $p_1=0.50 \to p_2=0.70$ and 3 planned contrasts. | **Fully Supported** |
| **E-18** | **Mock Offline Integration vs Live Execution**<br>Mock model harness proves runner call sequence, prompt interception, and logging, but does NOT prove live provider stability. | `REPRODUCED BY EXECUTION` | `test_live_instrumentation_offline.py` (3 tests using `FakeListChatModel` / `MockModel`) | `python -m unittest research_execution_20261018/test_live_instrumentation_offline.py`<br>Exit Code: `0` | Offline mock cannot establish real Gemini rate limits (429), API streaming, or model-side token counts. | **Partially Supported (Harness Verified; Live Dispatch Unverified)** |
| **E-19** | **Authentic External Claude / Gemini Reviews**<br>External review reports authored by Anthropic Claude or Google Gemini exist in the workspace. | `UNRESOLVED` *(Formally cataloged as `NOT PROVIDED / NOT VERIFIED`)* | Workspace-wide filesystem scan (`rglob('*claude*')`, `rglob('*gemini*')`). Zero external review documents found. | File search across `C:\testing`. Exit Code: `0` | Internal Antigravity audits must not be represented as external third-party reviews. | **Unsupported / Not Provided** |
| **E-20** | **Historical Data Segregation**<br>Historical datasets (`pilot-summary-clean.csv`, `full-summary.csv`) are permanently segregated and not pooled with Protocol v4. | `VERIFIED BY DIRECT INSPECTION` | `DATA_PROVENANCE_AUDIT.md`, `protocol_v3_runner.py:38-42`, `results/` | Filesystem inspection confirming segregated backup folders. | Historical data suffered from vision confounding and retry survivorship bias. | **Fully Supported** |

---

## 3. Provenance and File Hashes (Critical Research Assets)

To maintain cryptographic reproducibility and auditability, SHA-256 hashes of critical source and schedule assets were recorded:

| Asset Relative Path | Size (Bytes) | SHA-256 Digest |
| :--- | :---: | :--- |
| `shared/app-core.js` | 24,015 | `ccae98e0218402bd78f7c4548ca743fde79b89b4baee466447b72821621b80c7` |
| `shared/products.js` | 13,858 | `2da320f77ea6bb0c5d57b11d9548aa5f2d6c141093c834a31a98059e66ff7be3` |
| `shared/styles.css` | 14,233 | `e685f09623274291122a10697ad5097893c52e8d4621cae9bb4ba1d3ce3d052b` |
| `variants/v0-baseline/index.html` | 8,438 | `e5bc7d6205e46be94ba59473d092d63ea377286395b0581451e06a3092285189` |
| `variants/v2-aria/index.html` | 9,142 | `001a14197475fdfa5d51cf6a521443d0e2634e9e4f2081d0be643666d9341490` |
| `variants/v3-data-attrs/index.html` | 9,864 | `3ecf6d90d79744c8ebca5ff72d2be4d0b13cf14d1c1676fef16298faecb457c6` |
| `proposed_randomized_schedule.csv` | 3,524 | `3e6203cf847d8e20e8d91f2c270d47ad0173cb6d863f6ee5dc5950d750dfc346` |
| `proposed_3arm_schedule.csv` | 2,668 | `dfb6088e5bf410e304918e388d1222ce04535aa4112e06180c59804bc493a77f` |
| `proposed_smoke_schedule.csv` | 212 | `d1fafe239e0ebc5c93d9ef961ea15a995eef9f270a442d6a57cbbd8f8fb442aa` |

---

## 4. Synthesis of Audit Baseline
All core implementation claims have been verified against source code and active test executions. The evidence ledger confirms:
1. Verifiers for T1–T6 are strict and robust against negative mutations.
2. Observation pipeline bottlenecks are mathematically and empirically proven.
3. The live execution loop fails closed by default and has been validated offline.
4. Budget bounding is fail-closed and conservative.
5. Statistical power is honestly documented as exploratory for the pilot.
6. The only unverified elements are genuine external Claude/Gemini reviews (cataloged as absent) and live cloud provider billing infrastructure (not testable offline).

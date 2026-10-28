# NEXT LIVE EXECUTION READINESS & IMPLEMENTATION REPORT

**Document Date:** October 22, 2026  
**Workspace:** [`C:\testing`](file:///C:/testing) / [`research_execution_20261018`](file:///C:/testing/research_execution_20261018)  
**Target Runner:** [`research_execution_20261018/protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9, `browser-use 0.13.10`)  
**Protocol Version:** Protocol v4 (RCBD, Single-Shot, Strict Task Verifiers, Observation Delivery Audit, Isolated Smoke Harness)  
**Safety & Execution Policy:** 100% Offline Verified · Zero Paid API Calls Made · Safety Gate Strictly Locked  

---

## 1. Verified Source Changes & Actual Live-Loop Architecture

### 1.1 Live-Loop Status: Before vs. After
* **Before:** `protocol_v3_runner.py` only contained `run_single_mock_trial`. If live mode was requested, it lacked the real `Agent.run()` execution loop, per-run action histories were not persisted, treatment delivery was not audited from serialized prompts, schedule rows were unvalidated, and the $10.00 cost ceiling was only a text specification.
* **After:** Fully implemented [`run_single_live_trial`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L344) and integrated it directly into [`execute_experiment`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L678) behind the locked safety gate.
  * **Single-Trial Execution:** Sequential loop consuming schedule one row at a time.
  * **Modality Control:** `use_vision=False` strictly enforced in `browser_use.Agent` to eliminate multimodal visual confounding.
  * **Attribute Filtering:** Conditionally applies `EXTENDED_ATTRIBUTES` for the `DATA-CFG` arm and `DEFAULT_INCLUDE_ATTRIBUTES` for `BASELINE`, `VIS`, and `ARIA`.
  * **Fresh Session & State Isolation:** Creates a new `BrowserSession(headless=True, viewport=1920x1080)` per trial; clears `localStorage`, `sessionStorage`, and window cart globals before each trial.
  * **Pre-state Enforcement (T5):** Pre-seeds exactly one `wh-001` item into `localStorage` and `window.__cart__`, explicitly queries DOM state, records `pre_cart_count`, and asserts `pre_cart_count == 1` before agent acts.
  * **Serialized Observation Audit:** Intercepts `agent._message_manager.create_state_messages` to capture the actual serialized text representation delivered to the LLM. Checks for presence of `data-*` (for `DATA-CFG`), `aria-label` (for `ARIA`), and clean absence of custom attributes (for `BASELINE`). Records `treatment_attribute_observed` and evidence text.
  * **Terminal State & Scoring:** Captures terminal URL, title, `window.__cart__`, `window.__orderConfirmed__`, and `window.__lastOrder__` before closing browser. Evaluates via strict binary verifiers.
  * **Cost Ceiling Enforcement:** Executable code in `execute_experiment` accumulates estimated cost per run and triggers an immediate safety abort if cumulative expenditure reaches `--cost-ceiling` (default `$10.00`).
  * **Dual Logging:** Appends structured summary row to CSV and writes detailed per-run JSON (action history, thoughts, terminal DOM state, verification details) to `results/runs/` (or `results/smoke_runs/`).
  * **Separation of Smoke Tests:** Added `--smoke` flag to consume [`proposed_smoke_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_smoke_schedule.csv) and log to [`results/smoke_run_summary.csv`](file:///C:/testing/research_execution_20261018/results/smoke_run_summary.csv), strictly segregating smoke validation from study data.
  * **Schedule Row Validation:** Added `validate_schedule_rows` asserting valid arms, valid tasks, unique integer `run_index`, and existing variant paths on disk before execution.
  * **Offline Preflight Routine:** Implemented `--preflight` CLI routine validating 9 safe system checks (environment, models, binaries, schedule, directories, server, browser/CDP, verifiers T1–T6, safety gate) with zero API calls.

---

## 2. Verifier Fixes & Verification Behavior

### 2.1 Task T5 (Cart Mutation & Precondition Hardening)
* **The Defect:** Previously, `protocol_v3_runner.py` line 117 defined `precondition_ok = (pre_cart_count is None or pre_cart_count == 1)`. If `pre_cart_count` was omitted or `None`, an empty cart vacuously passed.
* **The Fix:** Updated to `precondition_ok = (pre_cart_count == 1)` in [`protocol_v3_runner.py:117`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L117). If `pre_cart_count` is missing (`None`), 0, or anything other than 1, `success` evaluates strictly to `False` and `score=0.0`.
* **Tests Passing:**
  * [`offline_test_suite.py:121-140`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L121): Added explicit negative assertions verifying `pre_cart_count=None` fails, `pre_cart_count=0` fails, `pre_cart_count=1` with non-empty cart fails, and only `pre_cart_count=1` with empty cart passes.
  * [`test_mutation_audit.py:57-74`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py#L57): Confirmed assertion distinguishing production logic from unseeded vacuous pass.

### 2.2 Task T6 (Absent-Fact Negative Probe)
* **Ground Truth:** Across all variants, manufacturer warranty duration for `wh-001` is intentionally omitted.
* **Verifier Logic:** Delegates to `verify_t6_grounded_refusal` in [`protocol_v3_runner.py:149-205`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L149). Evaluates `REFUSAL_PATTERN` against `DURATION_HALLUCINATION_PATTERN`.
  * `refusal=True, hallucination=False` $\rightarrow$ `GROUNDED_REFUSAL_SUCCESS` (`success=True, score=1.0`).
  * `refusal=True, hallucination=True` $\rightarrow$ `CONTRADICTORY_REFUSAL_WITH_HALLUCINATION` (`success=False, score=0.0`).
  * `refusal=False, hallucination=True` $\rightarrow$ `UNSUPPORTED_DURATION_HALLUCINATION` (`success=False, score=0.0`).
  * `refusal=False, hallucination=False` $\rightarrow$ `UNRELATED_OR_AMBIGUOUS_NON_REFUSAL` (`success=False, score=0.0`).
* **Active Caller Consistency:** Both `run_single_mock_trial` and `run_single_live_trial` in `protocol_v3_runner.py` directly record `v_res["success"]` and `v_res["score"]`.
* **Tests Passing:** `test_t6_verifier_isolated.py` (7/7 tests) and `offline_test_suite.py` (44 diverse regression cases).

### 2.3 Tasks T1–T4 (Strict Target Validation)
* **T1:** Exact SKU `wh-001` ($49.99, cheapest) in cart.
* **T2:** Exact SKU `mkp-001` in cart.
* **T3:** Exactly 1 item in cart and it must be `wh-002` (4.5 rating, second-highest). Non-audio items or multiple items strictly fail.
* **T4:** Requires `order_confirmed == True` AND `last_order_items` contains `mse-001`. Zero partial credit on incomplete flows.

---

## 3. Fresh Test Results & Exit Codes

Executed fresh via `C:\testing\.venv311\Scripts\python.exe`:

| Test Suite / Script | Command Executed | Tests Passed | Exit Code | Verified Scope |
|---|---|:---:|:---:|---|
| **Offline Verification Suite** | `python offline_test_suite.py` | **13 / 13** | **0** | Pruning of script/meta, attribute filtering, strict T3/T4/T5/T6 verifiers (including missing T5 precondition check), 44-case T6 regression battery, variant leakage, RCBD balance, authentic hashes, AXTree artifacts. |
| **Mutation Audit Suite** | `python -m unittest test_mutation_audit.py` | **6 / 6** | **0** | Catches T3 SKU dilution, T4 partial credit, T5 unseeded/missing precondition pass, T6 36-month inversion, live safety gate bypass, CMH odds ratio inversion. |
| **Isolated T6 Regression Battery** | `python -m unittest test_t6_verifier_isolated.py` | **7 / 7** | **0** | Refusals, hallucinations, contradictions, formatting edge cases. |
| **Statistical Power Audit** | `python -m unittest test_power_audit.py` | **7 / 7** | **0** | Binomial power calculations: 10.85% for N=96 pilot at $\Delta=0.20$; 80.2% for N=480 confirmatory at $\alpha=0.0167$. |
| **Analysis Pipeline Suite** | `python -m unittest test_analyze_v3_results.py` | **11 / 11** | **0** | CMH Agresti reference case, complete dataset ingestion, missing run flagging, duplicate ID rejection, infrastructure error segregation, boundary cells. |
| **Accessibility Tree Comparison** | `python -m unittest test_accessibility_tree_comparison.py` | **10 / 10** | **0** | Schema, CDP alternatives, Channel 1 concordant loss, Channel 3 AXTree retention vs browser-use prompt stripping. |
| **Agent Prompt Pipeline Test** | `python test_agent_prompt_pipeline.py` | **5 / 5** | **0** | Headless browser execution with `MockChatModel`: verifies prompt message interception across all 4 variants and confirms JSON-LD and custom `data-*` pruning. |
| **Runner Preflight Routine** | `python protocol_v3_runner.py --preflight` | **9 / 9 Checks** | **0** | Verified environment, models, browser framework, 96-row schedule, writable paths, local server, Chromium CDP, strict verifiers T1–T6, locked safety gate. |
| **Smoke Preflight Routine** | `python protocol_v3_runner.py --smoke --preflight` | **9 / 9 Checks** | **0** | Verified segregated 4-trial smoke schedule, writable `smoke_runs/`, local server, CDP, verifiers, and cost controls. |
| **Runner Smoke Mock Mode** | `python protocol_v3_runner.py --mock --smoke` | **4 / 4 Runs** | **0** | Verified smoke schedule consumption, mock execution, summary logging, max_runs termination. |
| **Legacy `test_t4_capture.py`** | `python test_t4_capture.py` | **Failed (Expected)** | **1** | Fails on `ModuleNotFoundError: No module named 'playwright'`. Out-of-scope legacy developer test; active Protocol v4 uses `browser-use` CDP. |

---

## 4. Configuration, Pricing & Cost Preflight

### 4.1 Experimental Configuration
* **Agent Framework:** `browser-use 0.13.10`
* **LLM Provider:** Google Cloud / Gemini API via `browser_use.ChatGoogle` (or `langchain_google_genai.ChatGoogleGenerativeAI`)
* **Model ID:** `gemini-flash-lite-latest`
* **Modality:** Text-Only (`use_vision=False` strictly enforced)
* **Sampling:** Temperature 0.0 (deterministic greedier decoding)
* **Per-Trial Step Limit:** `max_steps=30`
* **Hard Spending Ceiling:** `$10.00 USD` (enforced in runner executable code)

### 4.2 Authoritative Pricing & Limits of the Estimate
* **Authoritative Tier Pricing (Gemini Flash-Lite API):**
  * Input: `$0.10` – `$0.30` per 1M tokens ($0.00000030 / token)
  * Output: `$0.40` – `$2.50` per 1M tokens ($0.00000250 / token)
* **Token Assumptions:**
  * Average prompt size: ~26,900 chars ($\approx 6,725$ tokens) per step
  * Average steps per completed run: ~4 steps
  * Estimated tokens per run: ~28,500 input, ~400 output
  * Estimated cost per normal run: $\approx \$0.012$ USD
* **Uncertainty & Limits:**
  * If the model encounters multi-step loops or retries internal tool calls, steps could reach `max_steps=30`, consuming up to ~200,000 input tokens ($\approx \$0.06$ per runaway trial).
  * Rate limits / quotas (e.g. 15 RPM on free tier vs 1000 RPM on paid tier) cannot be verified without active network calls.
* **Capped Estimates:**
  * **4-Run Smoke Test:** $\approx \$0.05$ USD (Conservative ceiling: **$\$0.50$ USD**).
  * **96-Run Exploratory Pilot:** $\approx \$1.15$ USD (Conservative ceiling: **$\$5.00$ USD**; hard code limit: **$\$10.00$ USD**).

---

## 5. Proposed Four-Trial Smoke Test Schedule

Stored separately at [`research_execution_20261018/proposed_smoke_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_smoke_schedule.csv):

```csv
run_index,block_id,within_block_order,arm,task_id,variant_mapping,target_entity
1,0,1,ABS,T1,v0-baseline,wh-001
2,0,2,ARIA,T3,v2-aria,wh-002
3,0,3,DATA-CFG,T5,v3-data-attrs,wh-001
4,0,4,VIS,T6,v0-baseline,wh-001
```

* **Trial 1 (BASELINE / T1):** Tests baseline observation, search action, cheapest item addition (`wh-001`).
* **Trial 2 (ARIA / T3):** Tests interactive `aria-label` button extraction and second-highest rating comparison (`wh-002`).
* **Trial 3 (DATA-CFG / T5):** Tests extended attribute whitelisting (`data-action`, `data-product-id`), pre-state seeding of `wh-001`, `pre_cart_count == 1` assertion, and cart emptying.
* **Trial 4 (VIS / T6):** Tests negative information probe, unstated warranty fact refusal vs hallucination scoring.

---

## 6. Exact Future Smoke-Test Command (NOT EXECUTED — REQUIRES HUMAN AUTHORIZATION)

> [!WARNING]
> **NOT EXECUTED DURING THIS SESSION.**
> The safety gate in `protocol_v3_runner.py` remains locked. The command below is prepared for future execution by the human researcher once paid API credentials and protocol review are approved.

```powershell
# Step 1: In a local PowerShell session, set your paid Google Gemini API key:
$env:GOOGLE_API_KEY = "your-actual-paid-tier1-gemini-key"

# Step 2: Navigate to the execution workspace:
cd C:\testing\research_execution_20261018

# Step 3: Run the verified 4-trial smoke test batch:
C:\testing\.venv311\Scripts\python.exe protocol_v3_runner.py --live --confirm-live-execution --smoke --max-runs 4
```

---

## 7. Remaining Blockers

1. **`GOOGLE_API_KEY` Absent in Session:** `GOOGLE_API_KEY is configured: False`. The environment variable must be exported in the local terminal prior to live execution.
2. **Safety Gate Release:** In [`protocol_v3_runner.py:648-651`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L648), the explicit `RuntimeError("SAFETY GATE...")` remains active by default and requires human researcher unlocking after credential configuration.

---

### **FINAL VERDICT:**
# **READY FOR EXPLICIT LIVE PILOT APPROVAL**

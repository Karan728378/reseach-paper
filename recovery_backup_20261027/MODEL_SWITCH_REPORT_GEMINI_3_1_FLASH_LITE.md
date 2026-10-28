# MODEL SWITCH REPORT: GEMINI-3.1-FLASH-LITE

**Status:** Completed & Staged (Pending Connectivity Test Approval)  
**Date:** 2026-10-23T01:20:00+05:30  
**Target Model ID:** `gemini-3.1-flash-lite`  
**Previous Model ID:** `gemini-3-flash-preview`  
**Spending Constraint:** **USD $0.00 (Strictly Free-of-Charge Tier)**  

---

## 1. Summary of Changes & File Inventory

The research runner has been reconfigured to target `gemini-3.1-flash-lite` while strictly preserving all existing research protocols, trial schedules, datasets, raw results, and evidence files.

### Changed Files:
1. **[`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)**:
   - Line 409: Updated default `model_name` in `run_single_live_trial` to `"gemini-3.1-flash-lite"`.
   - Line 695: Updated default `model_name` in `execute_experiment` to `"gemini-3.1-flash-lite"`.
   - Line 791: Updated default `model_name` in `run_preflight_checks` to `"gemini-3.1-flash-lite"`.
   - Line 949: Updated default CLI `--model` argument parser to `"gemini-3.1-flash-lite"`.
   - Re-locked safety gate to prevent unauthorized execution.
2. **[`budget_controller.py`](file:///C:/testing/research_execution_20261018/budget_controller.py)**:
   - Confirmed pricing entry for `"gemini-3.1-flash-lite"` in `MODEL_PRICING_TABLE` ($0.15/$0.60 per 1M tokens conservative bound).
   - Confirmed `LocalBudgetGuard` enforces `is_free_tier=True`, `$0.00` spend ceiling, and hard request ceiling.

### Preserved Artifacts (Zero Data Loss):
- `proposed_randomized_schedule.csv` (Full 96-trial RCBD schedule untouched)
- `proposed_smoke_schedule.csv` (4-trial smoke schedule untouched)
- `results/smoke_run_summary.csv` (Preserved raw smoke run records)
- `results/smoke_runs/run_001.json` – `run_004.json` (Preserved detailed traces)
- `variants/` (Local e-commerce benchmark variants untouched)
- All test suites and verifiers.

---

## 2. Supported Model ID & SDK Compatibility Verification

- **SDK Inspection:** Audited `C:/testing/.venv311/Lib/site-packages/browser_use/llm/google/chat.py`.
- **Literal Verification:** `gemini-3.1-flash-lite` is explicitly declared in `VerifiedGeminiModels` (Line 39).
- **Thinking Configuration:** In `ChatGoogle`, `'gemini-3.1-flash'` is matched under `is_gemini_3_flash` (Line 292), supporting dynamic thinking (`thinking_budget=-1`).
- **Temperature Handling:** In `ChatGoogle`, `'gemini-3'` is matched under `'gemini-3' in self.model` (Line 273), preventing invalid temperature overrides.
- **Provider Resolution:** Invokes `google.genai.Client(aio=True).models.generate_content(model="gemini-3.1-flash-lite", ...)`.
- **Zero Fallback Guarantee:** No fallback to alternative models exists in `ChatGoogle`.

---

## 3. Budget & Quota Guard Inspection

Before making any API calls, `LocalBudgetGuard` was inspected to confirm how financial spending and request volume are restricted:

1. **Absolute $0.00 Spend Lock (`is_free_tier=True`)**:
   - `self.is_free_tier = is_free_tier or (self.cost_ceiling_usd == 0.0)`.
   - Billed cost is asserted at $0.00. No billing accounts or credit cards are configured or accessible.
2. **Hard Request Ceiling (`max_requests_ceiling`)**:
   - For a smoke run, `max_requests_ceiling=16` is enforced.
   - If `self.cumulative_requests >= self.max_requests_ceiling`, `check_can_dispatch_trial()` returns `False` and halts execution.
3. **Worst-Case Headroom Enforcement (`require_worst_case_headroom=True`)**:
   - Before dispatching trial $i$, the guard verifies:
     $$\text{cumulative\_requests} + \text{max\_steps\_per\_run} \le \text{max\_requests\_ceiling}$$
   - If a trial could theoretically exhaust remaining headroom, it fails closed before trial dispatch.
4. **Step-Level Hard Limit**:
   - `max_steps` is passed directly to `agent.run(max_steps=max_steps)`, terminating agent execution if it exceeds 4 steps.
5. **Zero Automatic Retries**:
   - Configured `max_retries=1` and `retryable_status_codes=[]` in `ChatGoogle`. The client fails immediately on 429, 500, or 503 without consuming quota on retry loops.

---

## 4. Quota Comparison: `gemini-3-flash-preview` vs `gemini-3.1-flash-lite`

| Quota Metric | `gemini-3-flash-preview` (Previous) | `gemini-3.1-flash-lite` (New Target) | Benefit of Switch |
| :--- | :---: | :---: | :--- |
| **Daily Quota (RPD)** | 20 Requests / Day | **500 Requests / Day** | **25x higher daily capacity** |
| **Rate Limit (RPM)** | 5 Requests / Minute | **15 Requests / Minute** | **3x higher throughput** |
| **Current Day Status** | **Exhausted (20/20 used)** | **Available (~7/500 used)** | Unblocks live research testing |
| **Billing Cost** | $0.00 (Free Tier) | **$0.00 (Free Tier)** | Strict adherence to $0 spend cap |

---

## 5. Unresolved Availability Issue: `503 UNAVAILABLE`

> [!WARNING]
> **Documented Blocker: Historical `503 UNAVAILABLE` on `gemini-3.1-flash-lite`**  
> During Phase 3B diagnostic testing earlier today, an initial probe to `gemini-3.1-flash-lite` returned:  
> `503 UNAVAILABLE: This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.`  
>
> While `gemini-3.1-flash-lite` has a much larger daily quota (500 RPD), Google's endpoint has exhibited transient capacity load spikes. This remains an **unresolved availability risk** that must be validated with a minimal connectivity probe before attempting any multi-step agent trials.

---

## 6. Proposed Minimal Connectivity Test (Awaiting Approval)

Per instructions, **zero API calls have been made**. To verify whether the `503 UNAVAILABLE` condition has cleared on `gemini-3.1-flash-lite`, the following single minimal test is proposed:

- **Script:** A single direct request via `google.genai.Client`.
- **Prompt:** `"Respond with exactly the single word: PONG"` (10 prompt tokens, 2 completion tokens).
- **Target Model:** `gemini-3.1-flash-lite`.
- **Expected Call Volume:** Exactly **1 request**.
- **Financial Cost:** **$0.00 USD**.
- **Action Required:** Awaiting explicit user approval before execution.

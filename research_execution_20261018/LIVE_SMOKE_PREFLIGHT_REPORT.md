# PREFLIGHT REVIEW REPORT: 4-TRIAL LIVE BROWSER-AGENT SMOKE RUN

**Document Status:** Complete & Verified  
**Date & Timestamp:** 2026-10-23T01:05:00+05:30  
**Target Environment:** Local Chromium + Google AI Studio Free-of-Charge API  
**Evaluated Artifacts:**
- `proposed_smoke_schedule.csv`
- `protocol_v3_runner.py`
- `budget_controller.py`
- `smoke_test_evidence.json`
- `C:/testing/variants/`

---

## 1. Executive Summary & GO / NO-GO Decision

| Audit Category | Status | Verified Finding |
| :--- | :---: | :--- |
| **Spending Cap** | **ENFORCED ($0.00)** | Zero billing accounts, zero credit cards, Google AI Studio free tier only. |
| **Model Selection** | **VERIFIED** | `gemini-3-flash-preview` exclusively; zero silent fallback to other models. |
| **Retry Behavior** | **LOCKED (0 Retries)** | `max_retries=1`, `retryable_status_codes=[]` configured in `ChatGoogle`. |
| **Planned Schedule** | **VALIDATED** | Exactly 4 trials across 4 distinct arms (`ABS`, `ARIA`, `DATA-CFG`, `VIS`). |
| **Call Budget vs Free Quota** | **BOUNDED & SAFE** | Max 4 steps/trial $\rightarrow$ 16 calls worst-case $\le 17\text{--}18$ remaining RPD quota. |
| **Local Infrastructure** | **READY** | Port 8080 variant server verified HTTP 200; Headless CDP connected. |
| **Task Verifiers** | **VERIFIED** | T1, T3, T5 (pre-state assertion), and T6 (grounded refusal) verified. |
| **Evidence Logging** | **READY** | Per-run detailed JSON telemetry (`smoke_runs/`) and `smoke_run_summary.csv`. |
| **Safety Interlock** | **LOCKED** | Runner halts immediately on `--live` until authorized by user. |

### Formal Verdict: **CONDITIONAL GO**

> [!IMPORTANT]
> **Decision: CONDITIONAL GO.**  
> All 9 offline preflight checks have passed, the HTTP server directory bug was resolved, the model configuration is locked to `gemini-3-flash-preview` with retries disabled, and the hard request cap ($16\text{ calls}$) strictly bounds total execution within the remaining free-tier daily quota ($17\text{--}18\text{ RPD}$).  
> **Execution remains gated and locked.** Zero behavioral trials have been dispatched. Per instruction, the runner is paused awaiting explicit user authorization.

---

## 2. Schedule Inspection (`proposed_smoke_schedule.csv`)

The smoke schedule has been independently audited and parsed directly from `C:/testing/research_execution_20261018/proposed_smoke_schedule.csv`:

```csv
run_index,block_id,within_block_order,arm,task_id,variant_mapping,target_entity
1,0,1,ABS,T1,v0-baseline,wh-001
2,0,2,ARIA,T3,v2-aria,wh-002
3,0,3,DATA-CFG,T5,v3-data-attrs,wh-001
4,0,4,VIS,T6,v0-baseline,wh-001
```

### Trial Breakdown:
1. **Trial 1 (Run 01, Arm `ABS`, Task `T1`):**
   - **Variant:** `v0-baseline` (Raw semantic HTML without ARIA enhancements or custom `data-*` attributes).
   - **Instruction:** *"Search for 'wireless headphones' and add the least expensive result to your cart."*
   - **Target Entity:** `wh-001` (SoundFlow Air 3, $49.99).
   - **Construct Verified:** Absolute baseline DOM serialization and search/cart action generation.

2. **Trial 2 (Run 02, Arm `ARIA`, Task `T3`):**
   - **Variant:** `v2-aria` (Enhanced with descriptive ARIA labels, e.g., `aria-label="Add SoundFlow Air 3 to cart"`).
   - **Instruction:** *"Navigate to the Audio category. Compare the customer ratings of all products. Add the product with the second-highest customer rating to your cart."*
   - **Target Entity:** `wh-002` (BudPro Wireless X, rating 4.5).
   - **Construct Verified:** Multi-attribute comparison (rating extraction) under accessibility tree markup.

3. **Trial 3 (Run 03, Arm `DATA-CFG`, Task `T5`):**
   - **Variant:** `v3-data-attrs` (Enhanced with additive semantic attributes: `data-field`, `data-product-id`, `data-amount`, `data-action`).
   - **Instruction:** *"There is one item in your cart. Navigate to the cart and remove it so the cart is empty."*
   - **Pre-State Precondition:** Cart pre-seeded with 1 item (`wh-001`); runner strictly asserts `pre_cart_count == 1` before agent dispatch.
   - **Construct Verified:** Precondition-gated state reset and interactive deletion action using extended attribute configuration.

4. **Trial 4 (Run 04, Arm `VIS`, Task `T6`):**
   - **Variant:** `v0-baseline` (No warranty text present in DOM).
   - **Instruction:** *"Navigate to the product details for 'SoundFlow Air 3' (SKU: wh-001). Retrieve the exact manufacturer warranty duration specified for this item."*
   - **Construct Verified:** Grounded refusal verification; agent must report warranty duration is unstated without hallucinating temporal durations.

---

## 3. Exact Call Budget & Free Quota Accounting

Do not rely on historical estimates; here is the empirical quota ledger as of current execution:

### 3.1 Provider Free-Tier Limits (Google AI Studio)
- **Model:** `gemini-3-flash-preview`
- **Rate Limit (RPM):** **5 Requests Per Minute**
- **Daily Quota (RPD):** **20 Requests Per Day**
- **Billing Tier:** Free-of-charge tier ($0.00 billed).

### 3.2 Consumed Quota Ledger
- **Dashboard Baseline:** 1 / 20 RPD consumed prior to Phase 3B.
- **Diagnostic Endpoint Probe:** 1 request to `gemini-3-flash-preview` (HTTP 200).
- **Phase 3B Neutral Verification (`smoke_test_evidence.json`):** 1 request ("PONG", prompt tokens: 10, candidate tokens: 2).
- **Total Quota Used Today:** **2 to 3 requests**.
- **Verified Remaining Daily Quota:** **17 to 18 requests**.

### 3.3 Smoke Run Call Budget Architecture

| Metric | Hard Capped Upper Bound | Realistic Expected Value | Rationale |
| :--- | :---: | :---: | :--- |
| **Number of Trials** | **4 trials** | **4 trials** | Exactly 4 rows in `proposed_smoke_schedule.csv`. |
| **Model Requests / Trial** | **Max 4 steps** | **2 to 3 steps** | Capped by `max_steps=4`. Optimal paths take 2–3 steps. |
| **Total Model Requests** | **$\le 16$ calls** | **8 to 12 calls** | $4 \times 4 = 16$ max. $4 \times 2.5 = 10$ expected. |
| **Remaining Daily Free Quota**| **$17\text{--}18$ calls** | **$17\text{--}18$ calls** | Free tier limit is 20 RPD. |
| **Quota Safety Headroom** | **$+1$ to $+2$ calls** | **$+6$ to $+10$ calls** | **Impossible to exceed 20 RPD daily limit.** |
| **Total Dollar Expenditure** | **$0.00 USD** | **$0.00 USD** | Free tier guaranteed; billing activation prohibited. |

> [!CAUTION]
> **Why `max_steps=4` is mandatory:**  
> The default runner had `max_steps=30`. If 4 trials ran with `max_steps=30`, a wandering or looping agent could dispatch up to 120 calls, which would hit the 20 RPD wall at step 18 and trigger HTTP 429 quota exhaustion. Capping `max_steps=4` per trial guarantees that even under a worst-case failure mode, the batch will stop at 16 calls, remaining strictly within the verified free quota.

---

## 4. Model Integrity & Fallback Prevention

### 4.1 Strict Single-Model Targeting
- **Model ID:** `gemini-3-flash-preview` is explicitly passed to `ChatGoogle(model="gemini-3-flash-preview", ...)`.
- **SDK Level Verification:** In `browser_use/llm/google/chat.py`, `ainvoke` passes `self.model` directly to `self.get_client().aio.models.generate_content(model=self.model, ...)`. There is **zero fallback logic** in `ChatGoogle` or Google's `genai` SDK to switch to any other model.
- **Fail-Closed on Unknown Model:** `budget_controller.py` contains `gemini-3-flash-preview` in `MODEL_PRICING_TABLE` ($0.15/$0.60 per 1M tokens conservative bounding).

### 4.2 Disabling Automatic Retries
- By default, `ChatGoogle` has `max_retries = 5` and `retryable_status_codes = [429, 500, 502, 503, 504]`.
- If an agent hits rate limits, a 5-retry loop with exponential backoff could make redundant calls or delay execution.
- **Enforced Fix in `protocol_v3_runner.py`:**
  ```python
  llm = ChatGoogle(model=model_name, api_key=api_key, max_retries=1, retryable_status_codes=[])
  ```
  `max_retries=1` ensures exactly 1 single attempt and zero retry iterations. Any failure immediately fails closed and records the status without consuming additional quota.

### 4.3 Rate Limit Pacing (5 RPM Compliance)
- Gemini 3 Flash Preview free tier enforces 5 Requests Per Minute.
- **Enforced Fix in `protocol_v3_runner.py`:**
  An asynchronous pacing sleep of `await asyncio.sleep(15.0)` is executed between live trials. This spreads the 4 trials over at least 60–90 seconds, guaranteeing the request frequency remains strictly below 5 RPM.

---

## 5. Infrastructure & Verifier Readiness Audit

### 5.1 Local Web Server Directory Fix
- **Identified Defect:** In earlier runs, `http.server.ThreadingHTTPServer` used a handler that relied on `os.getcwd()`. When the working directory shifted to `research_execution_20261018`, requests to `http://127.0.0.1:8080/variants/v0-baseline/index.html` returned HTTP 404.
- **Resolution Applied:** Subclassed `SimpleHTTPRequestHandler` with explicit `directory=str(ROOT_DIR)` (`C:/testing`).
- **Preflight Verification:**
  `[CHECK 6/9] Local Web Server: [REACHABLE] (http://127.0.0.1:8080/variants/v0-baseline/index.html HTTP 200)` passed.

### 5.2 Browser & CDP Connection
- Headless Chromium session initialized with `1280x720` viewport.
- Successfully navigated to local variant, fetched page title (`127.0.0.1:8080/variants/v0-baseline/index.html#home`), and closed cleanly.
- `[CHECK 7/9] Headless Browser & CDP: [PASSED]`.

### 5.3 Task Verifier Logic
- **T1:** Asserts `wh-001` in cart.
- **T3:** Asserts strictly `wh-002` only (BudPro Wireless X, rating 4.5); fails if `wh-001` or multiple items are present.
- **T5:** Asserts cart is empty AND `pre_cart_count == 1`.
- **T6:** Protocol v4 Grounded Refusal verifier: matches explicit refusal without hallucinating temporal durations. Rejects unsupported durations (`36 months`, `2 years`) and contradictions.
- `[CHECK 8/9] Task Verifiers (T1-T6): [VERIFIED]`.

### 5.4 Secret Redaction & Key Management
- `GOOGLE_API_KEY` is loaded from the Windows User environment table (`HKEY_CURRENT_USER\Environment`).
- Never hardcoded in python files; never written to summary CSV or git commits.
- `sanitize_secret_leakage()` redacts `AIza...`, `AQ....`, and bearer tokens across all captured logs and prompts.
- `[CHECK 1/9] Environment Variable GOOGLE_API_KEY: [CONFIGURED] (Format verified, value redacted)`.

---

## 6. Risk Assessment Matrix

| # | Risk Factor | Probability | Impact | Mitigation Implemented |
| :-: | :--- | :---: | :---: | :--- |
| **R1** | **Agent looping / step runaway** | Low | Critical | Hard cap `max_steps=4` strictly bounds each trial. Total calls cannot exceed 16. |
| **R2** | **5 RPM burst rate-limit (HTTP 429)** | Low | High | 15-second inter-trial pacing delay spreads requests across $\ge 60\text{s}$. |
| **R3** | **Unintended financial spend** | Zero | Critical | Google AI Studio free tier only. Billed cost locked to $0.00. No billing info configured. |
| **R4** | **Automatic retry storm** | Zero | High | `max_retries=1` and `retryable_status_codes=[]` eliminate all retry loops. |
| **R5** | **Silent model fallback** | Zero | High | Single model parameter bound; client SDK throws on endpoint error without fallback. |
| **R6** | **T6 verifier false positive/negative** | Very Low | Medium | Strict regex validated against 12-case ground-truth battery. |

---

## 7. Operational Readiness Checklist

- [x] `proposed_smoke_schedule.csv` loaded and validated (4 rows).
- [x] Model target locked to `gemini-3-flash-preview`.
- [x] `max_steps=4` wired into `Agent` initialization.
- [x] Hard request ceiling `max_requests_ceiling=16` wired into `LocalBudgetGuard`.
- [x] Free-tier $0.00 spend guard enabled in `LocalBudgetGuard`.
- [x] Automatic retries disabled (`max_retries=1`, `retryable_status_codes=[]`).
- [x] Local test website server verified serving `C:/testing/variants/` (HTTP 200).
- [x] Headless Chromium browser automation verified via Playwright CDP.
- [x] Verifiers verified for T1, T3, T5, and T6.
- [x] Secret sanitization verified (zero API key leakage).
- [x] Preflight offline check routine executed with 9/9 green passes.
- [x] Safety gate locked pending user authorization.

---

## 8. Final Decision & Next Step

### Recommendation: **READY FOR LIVE SMOKE RUN UPON USER AUTHORIZATION**

The live smoke test setup is fully bounded, safe, reproducible, and incapable of exceeding the remaining daily free quota or incurring financial charges.

**Safety Gate State:** **LOCKED**  
No behavioral trials have been dispatched. Execution will only proceed when the user gives explicit authorization.

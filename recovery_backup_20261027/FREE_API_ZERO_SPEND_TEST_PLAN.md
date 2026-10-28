# Zero-Spend Test Plan & Verification Protocol

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date:** October 24, 2026  
**Auditor:** Autonomous Senior Research Engineer (DeepMind Antigravity System)  
**Deliverable:** `FREE_API_ZERO_SPEND_TEST_PLAN.md`  
**Core Objective:** Operational procedure for establishing, testing, and bounding a zero-cost API setup before any live trial execution.

---

## 1. Manual Account Setup Without Payment Credentials

To guarantee zero charges, the operator must set up the chosen provider strictly without providing credit card, debit card, or bank details.

### Protocol for Candidate 1: Google AI Studio (Gemini)
1. **Account Isolation:** Log into [Google AI Studio](https://aistudio.google.com/) using a standard personal or university Google Account that has **NO Google Cloud Billing Account attached**.
2. **Key Creation:** Click **Get API key** $\rightarrow$ **Create API key in new project**.
3. **Billing Check (MANDATORY):**
   - In Google AI Studio, navigate to the project settings / plan info.
   - Confirm that the project plan says **Free Tier** (15 RPM / 1,500 RPD).
   - Confirm that **Pay-As-You-Go is OFF**.
   - Confirm that **NO Cloud Billing Account** is linked.
   - *Financial Invariant:* If no payment method or billing account is linked to the project in Google Cloud Console, Google cannot charge money under any circumstances. When 1,500 daily requests are exceeded, the API returns HTTP `429 RESOURCE_EXHAUSTED`.

### Protocol for Candidate 2: GroqCloud
1. **Account Creation:** Navigate to [GroqCloud Console](https://console.groq.com/).
2. **Authentication:** Sign in using an email address, GitHub, or Google account.
3. **Zero-Card Verification:** Do **NOT** navigate to `Settings > Billing` or enter any payment information.
4. **Key Generation:** Navigate to **API Keys** $\rightarrow$ **Create API Key**. Copy the key to a secure local environment variable (`GROQ_API_KEY`).
5. **Dashboard Verification:**
   - Navigate to `Settings > Limits`.
   - Verify the plan is listed as **Free Tier**.
   - Note the active limits (e.g., 30 RPM, 1,000 RPD for `llama-3.3-70b-versatile`, or 14,400 RPD for `llama-3.1-8b-instant`).
   - *Financial Invariant:* Groq's Free Tier does not collect credit cards and cannot bill overages. Exceeding limits results in HTTP `429 Too Many Requests`.

---

## 2. Hard Quota Stop & Anti-Overage Safeguards

1. **Auto-Top-Up & Billing Upgrades:** Keep disabled. Never configure auto-recharge.
2. **Client-Side Request Bounding (`LocalBudgetGuard`):**
   - The runner must be invoked with an explicit `--max-requests` ceiling (e.g. `--max-requests 50`).
   - Before dispatching any trial, `LocalBudgetGuard.check_can_dispatch_trial()` verifies that `cumulative_requests < max_requests_ceiling`.
   - If reached, execution halts immediately with exit code 0.
3. **Zero In-Process Retries:**
   - Both `ChatGoogle` and `ChatGroq` must be instantiated with `max_retries = 1`.
   - Client libraries are prohibited from silently looping on 429/503 errors.
4. **Inter-Trial Pacing:**
   - Enforce `await asyncio.sleep(15.0)` between runs.
   - 15 seconds pacing ensures a maximum throughput of 4 trials per minute, staying well below both Google's 15 RPM limit and Groq's 30 RPM limit.

---

## 3. Pre-Experiment Minimal Compatibility Test

Before executing any scheduled experimental runs, a single-trial offline/mock test or a single isolated probe must be run to verify zero-leakage logging and tool schema parsing:

### Step A: Verify Offline Instantiation
Run in terminal (0 API calls):
```powershell
C:\testing\.venv311\Scripts\python.exe -c "from browser_use.llm.groq.chat import ChatGroq; g = ChatGroq(model='llama-3.3-70b-versatile', api_key='dummy_key', max_retries=1); print('Groq instantiated successfully')"
```

### Step B: Minimal Smoke Verification Budget
When authorized by the user, a single smoke run can be dispatched with a hard ceiling of 1 run and 15 requests:
```powershell
C:\testing\.venv311\Scripts\python.exe protocol_v3_runner.py --live --confirm-live-execution --max-runs 1 --max-requests 15
```

---

## 4. Telemetry, Recording & Error Disambiguation

During any authorized execution, the runner must capture and distinguish three distinct categories of outcomes:

1. **Behavioral Completions:**
   - Agent concludes via `agent_completed` or `max_steps_reached`.
   - Verifier evaluates DOM ground truth (`success = True` or `False`).
   - Recorded as `status = "completed"`.
2. **Quota Exhaustion (Client or Provider Rate Limits):**
   - HTTP status code: `429 Too Many Requests` or `429 RESOURCE_EXHAUSTED`.
   - Error payload contains `quota`, `rate_limit_exceeded`, or `resource_exhausted`.
   - Action: Runner halts immediately (`break`), saves trace with `status = "quota_exhausted"`, and does not retry. Quarantined from behavioral metrics.
3. **Provider Outages / Capacity Spikes:**
   - HTTP status code: `503 UNAVAILABLE` or `502 Bad Gateway`.
   - Error payload contains `high demand`, `temporarily unavailable`.
   - Action: Runner halts immediately, records trace with `status = "infrastructure_aborted"`, and quarantines from behavioral metrics.

---

## 5. Evidence Required to Confirm Provider-Side Zero Billing

Because local software ledgers cannot replace cloud console invoices, the operator must verify provider-side billing status using the following artifacts:

### For Google AI Studio:
1. Log into [Google Cloud Console Billing](https://console.cloud.google.com/billing).
2. Confirm that the project housing the Gemini API key has **no billing account linked** (status: *“This project has no billing account”*).
3. Confirm that current month charges across the account display **$0.00**.

### For GroqCloud:
1. Log into [GroqCloud Console](https://console.groq.com/).
2. Navigate to `Settings > Billing`.
3. Confirm that the page states **“No payment method on file”** and that the account is on the **Free Tier**.
4. Capture a screenshot or confirmation note for the research audit log.

---

## 6. Safe Shutdown & Rollback Procedure

If any anomaly, unexpected request volume, or provider warning occurs during future authorized runs:
1. **Immediate Process Termination:**
   ```powershell
   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
   ```
2. **Credential Invalidation:** Delete the API key in the provider console to immediately block any external requests.
3. **Audit Ledger Inspection:** Review `results/daily_quota_ledger.json` and `results/v3_3arm_summary.csv` to verify exact request volume before taking further action.

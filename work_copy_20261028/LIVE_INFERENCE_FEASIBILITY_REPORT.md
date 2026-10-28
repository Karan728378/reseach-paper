# Live Inference Feasibility and $0 Budget Feasibility Report (Phase 3B Updated)

**Document ID:** `research_execution_20261018/LIVE_INFERENCE_FEASIBILITY_REPORT.md`  
**Execution Context:** `C:\testing\research_execution_20261018\`  
**Runtime:** Python 3.11.9 (`C:\testing\.venv311\Scripts\python.exe`), `browser-use 0.13.10`, `google-genai 2.25.0`  
**Updated Date:** October 2026  
**Auditor / Roles:** Senior Research Engineer, Systems Auditor, Reproducibility & Safety Lead  
**Spending Cap Enforcement:** **USD $0.00 (Hard Ceiling · Zero Paid Inferences · Confirmed Real Free Inference)**  

---

## 1. Executive Summary: Real External LLM Inference Confirmed at $0.00

Following the configuration of a valid Google AI Studio API key in the Windows user environment, we conducted an exhaustive evaluation of candidate Gemini models, resolved provider rate limits and server availability errors, and **successfully executed a genuine live external model inference request at exactly $0.00 cost**.

### Core Status Highlights:
- **Genuine Live External Request:** **SUCCESS (HTTP 200 OK)**
- **Model Utilized:** `gemini-3-flash-preview` (Gemini 3 Flash)
- **Input Prompt:** Neutral verification probe (`"Respond with exactly the single word: PONG"`)
- **Sanitized Model Output:** `"PONG"`
- **Tokens Incurred:** 10 prompt tokens, 2 candidate tokens (68 total billed tokens)
- **Financial Cost Incurred:** **$0.00 USD (Google AI Studio Free Tier)**
- **Evidence Artifact:** [`smoke_test_evidence.json`](file:///c:/testing/research_execution_20261018/smoke_test_evidence.json)
- **Paid Fallback / Mock Model:** **NONE (100% Real External API)**
- **Billing Changes:** **NONE (Zero billing activation; zero credit cards attached)**

---

## 2. Evaluation of Candidate Models & Rate-Limit Diagnostics

The researcher's Google AI Studio dashboard and active API key were audited across multiple candidate Gemini endpoints to determine why previous models failed and identify the working zero-cost route:

| Model Identifier | Display Name & Quota Tier | API Diagnostic Status | Root Cause / Availability Finding | Usable for $0 Live Experiment? |
|---|---|:---:|---|:---:|
| **`gemini-3.8-flash`** | Gemini 3.8 Flash<br>(5 RPM / 20 RPD) | **EXCEEDED (429)** | Dashboard confirmed 22/20 RPD used (exceeded daily 20 request quota). | **NO (Exceeded)** |
| **`gemini-3.5-flash-lite`** | Gemini 3.5 Flash Lite<br>(15 RPM / 500 RPD) | **EXCEEDED (429)** | Dashboard confirmed 502/500 RPD used (exceeded daily 500 request quota). | **NO (Exceeded)** |
| **`gemini-3.1-flash-lite`** | Gemini 3.1 Flash Lite<br>(15 RPM / 500 RPD) | **503 UNAVAILABLE** | API returned `503 UNAVAILABLE: This model is currently experiencing high demand. Spikes in demand are usually temporary.` | **TEMPORARILY BLOCKED** (Retry when spike clears) |
| **`gemini-3.1-flash-lite-preview`** | Gemini 3.1 Flash Lite Preview | **503 UNAVAILABLE** | High demand spike identical to base model. | **TEMPORARILY BLOCKED** |
| **`gemini-2.5-flash`** | Gemini 2.5 Flash | **404 NOT FOUND** | API returned `404 NOT_FOUND: This model is no longer available to new users.` | **NO (Deprecated)** |
| **`gemini-3-flash-preview`** *(Selected)* | Gemini 3 Flash<br>(5 RPM / 20 RPD) | **200 OK (ACTIVE)** | **Successfully connected and generated text.** Token limit: 1,048,576 context. Dashboard showed 1/20 RPD used. | **YES (Verified Active & Free)** |

---

## 3. Evidence of Genuine External Smoke Request

The single neutral smoke request was dispatched directly to the Google Generative Language API via `google.genai.Client` without retries or fallbacks:

```json
{
  "test_type": "NEUTRAL_SMOKE_VERIFICATION",
  "provider": "google",
  "model_id": "gemini-3-flash-preview",
  "api_endpoint": "generativelanguage.googleapis.com",
  "timestamp_start": "2026-10-22T19:15:18.478407+00:00",
  "timestamp_end": "2026-10-22T19:15:28.783795+00:00",
  "http_status": 200,
  "success": true,
  "prompt_sent": "Respond with exactly the single word: PONG",
  "sanitized_response": "PONG",
  "usage_metadata": {
    "prompt_token_count": 10,
    "candidates_token_count": 2,
    "total_token_count": 68
  },
  "candidates": [
    {
      "finish_reason": "FinishReason.STOP"
    }
  ],
  "cost_usd": 0.0,
  "tier_type": "Google AI Studio Free of Charge Tier",
  "paid_fallback_used": false,
  "mock_model_used": false,
  "behavioral_experiment_count": 0
}
```

**Authenticity Guarantees:**
1. Zero mock models (`FakeListChatModel`) were used; this was an authentic roundtrip HTTP/2 SSL request to `generativelanguage.googleapis.com`.
2. Total cost was exactly **$0.00**.
3. Credentials were read strictly from the user's environment and were **never printed, logged, or written to repository files**.

---

## 4. Quota Constraints & Schedule Feasibility

### Current Daily Limits:
- **`gemini-3-flash-preview`**: 5 Requests Per Minute (RPM), 20 Requests Per Day (RPD).
  - *Current Usage:* ~2 of 20 RPD consumed.
  - *Remaining Free Capacity Today:* **~18 requests**.
- **`gemini-3.1-flash-lite`**: 15 RPM, 500 RPD.
  - *Current Usage:* 7 of 500 RPD consumed.
  - *Remaining Free Capacity Today:* **493 requests** (once the temporary 503 high-demand spike clears).

### Feasibility for Experimental Schedules:
1. **The 4-Trial Live Smoke Run ([`proposed_smoke_schedule.csv`](file:///c:/testing/research_execution_20261018/proposed_smoke_schedule.csv)):**
   - Requires: 4 trials $\times$ ~3–4 steps = ~12–16 model calls.
   - Fits comfortably within today's remaining quota on `gemini-3-flash-preview` (18 calls remaining).
   - **Status:** **IMMEDIATELY FEASIBLE AT $0.00.**
2. **The 72-Trial Option A Pilot ([`proposed_3arm_schedule.csv`](file:///c:/testing/research_execution_20261018/proposed_3arm_schedule.csv)):**
   - Requires: 72 trials $\times$ ~12 steps = ~864 model calls.
   - Cannot run on `gemini-3-flash-preview` in a single day due to the 20 RPD cap.
   - Can run across 2 days on `gemini-3.1-flash-lite` (500 RPD allowance) once 503 server load subsides, or over 43 days on `gemini-3-flash-preview`.
   - **Status:** Requires multi-day execution or waiting for `gemini-3.1-flash-lite` load reduction.

---

## 5. Security & Safety Compliance Statement

1. **No Billing Activated:** No Google Cloud billing account was created, linked, or enabled. All calls were processed by Google AI Studio's Free-of-Charge tier.
2. **Secret Privacy Maintained:** The API key was stored exclusively in the Windows User environment table (`[System.Environment]::SetEnvironmentVariable`) and was not embedded into code, committed to git, or recorded in markdown documents.
3. **No Unearned Behavioral Claims:** This single neutral probe verified API plumbing only. It does **not** constitute a behavioral experiment or support any hypothesis regarding semantic markup.

---

## 6. Next Recommended Action

To move to the first live browser navigation trial without incurring any cost:

1. **Authorize the 4-Trial Live Smoke Run ([`proposed_smoke_schedule.csv`](file:///c:/testing/research_execution_20261018/proposed_smoke_schedule.csv))**:
   - Executes 1 trial per arm (`ABS`, `ARIA`, `DATA-CFG`, `VIS`) across tasks T1, T3, T5, T6 using `gemini-3-flash-preview`.
   - Uses ~12–16 requests, fitting inside today's remaining free quota.
   - Validates live browser mechanics, DOM observation capture, and verifier scoring.
   - Cost: **$0.00**.

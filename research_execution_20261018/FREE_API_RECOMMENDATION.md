# Free API Recommendation & Scientific Decision Matrix

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date:** October 24, 2026  
**Auditor:** Autonomous Senior Research Engineer (DeepMind Antigravity System)  
**Deliverable:** `FREE_API_RECOMMENDATION.md`  

---

## 1. Executive Summary & Top Candidates

Following systematic web investigation, rate-limit auditing, and local codebase compatibility testing, two providers emerge as verified, cardless, recurring free-tier solutions suitable for autonomous browser agent research:

1. **Top Recommendation for Scientific Continuity:** **Google AI Studio (Gemini Free Tier)**  
   - *Model:* `gemini-3.1-flash-lite` (or `gemini-2.0-flash`)  
   - *Daily Free Allowance:* 1,500 Requests Per Day (RPD), 15 Requests Per Minute (RPM).  
   - *Card Required:* **NO.**  
   - *Why It Leads:* Preserves 100% experimental comparability with the 27 completed trials. Switching models mid-experiment introduces fatal confounding across blocks.
2. **Top Alternative for Pure Cardless Architecture:** **GroqCloud**  
   - *Model:* `llama-3.3-70b-versatile`  
   - *Daily Free Allowance:* 1,000 Requests Per Day (RPD), 30 Requests Per Minute (RPM).  
   - *Card Required:* **NO.**  
   - *Why It Leads:* Fast inference (~300 tokens/sec), zero billing infrastructure on free tier (impossible to run up an invoice), native OpenAI-compatible tool calling supported by `browser-use 0.13.10`. Requires running as an independent cross-model replication cohort.

---

## 2. In-Depth Comparative Trade-Off Analysis

| Evaluation Criterion | Candidate 1: Google AI Studio | Candidate 2: GroqCloud | Decision Impact |
|:---|:---|:---|:---|
| **Payment Card Requirement** | **NO** (Standard Google account) | **NO** (Email / GitHub / Google SSO) | Both guarantee zero financial risk if no card is submitted. |
| **Risk of Overages** | Zero if Cloud Billing is unlinked. (Risk only if key is inside a project with active billing). | **Zero.** Groq free tier has no payment method on file and cannot bill. | Groq is structurally more isolated from billing systems. |
| **Daily Request Budget** | **1,500 RPD** | **1,000 RPD** (70B) / **14,400 RPD** (8B) | Both easily accommodate the remaining 45 trials (~293 requests). |
| **Tool / Function Calling** | Native Pydantic schema parsing via `ChatGoogle`. | Native OpenAI tool calling via `ChatGroq`. | Both fully compatible with `browser-use 0.13.10`. |
| **Existing Dependencies** | `langchain-google-genai` active in `.venv311`. | `groq 1.0.0` already installed in `.venv311`. | Zero package installations required for either. |
| **Scientific Comparability** | **100% Comparable:** Directly completes the 72-trial schedule under the original model (`gemini-3.1-flash-lite`). | **Non-Comparable with Runs 1–27:** Switching models mid-study confounds treatment with model capability. | **Decisive Advantage for Google AI Studio.** |

---

## 3. The Scientific Validity Dilemma: Why Switching Models Mid-Study is Invalid

In randomized complete block experiments:
- **Block 1 (Runs 1–18):** 100% completed under `gemini-3.1-flash-lite`.
- **Block 2 (Runs 19–27):** 9 trials completed under `gemini-3.1-flash-lite`.
- If Runs 28–72 are executed using Llama-3.3-70B:
  - Block 2 would contain a mix of Gemini and Llama trials.
  - Blocks 3 and 4 would be 100% Llama trials.
  - Any observed differences in task success, steps, or duration between blocks would conflate the experimental markup treatments (ABS, ARIA, DATA-CFG) with model architecture, prompt understanding, and tokenizer behavior.
  - No peer-reviewed venue will accept an experimental dataset that pooled two completely different foundation models without controlling for model effects.

### Recommended Scientific Paths:

#### Path A: Complete the 72-Trial Study Under Gemini (Recommended)
- Verify in Google Cloud Console that the API key belongs to a project with **no billing account linked**.
- Resume and finish the remaining 45 trials with `gemini-3.1-flash-lite`.
- Result: A clean, publication-grade 72-trial RCBD dataset under strict single-model control.

#### Path B: Launch a Distinct Groq Llama 3.3 Cohort
- Freeze the 27 Gemini runs as Cohort 1 (Pilot Replicate).
- Configure Groq `llama-3.3-70b-versatile` under a distinct results directory (`results/groq_3arm_runs/`).
- Execute a fresh 18-trial or 72-trial balanced cohort.
- Result: A comparative multi-model evaluation studying whether the DOM serialization gap persists across closed-source (Gemini) and open-weights (Llama) models.

---

## 4. Exact Manual Steps for the Operator

### For Path A (Google AI Studio — Recommended):
1. Open [Google Cloud Billing Console](https://console.cloud.google.com/billing).
2. Select the project used for your Gemini API key.
3. Confirm that the project has **no billing account linked** (status: *“This project has no billing account”*).
4. Confirm current month spend displays **$0.00**.
5. Once confirmed, you can safely authorize the runner to resume with `--max-requests 500`.

### For Path B (GroqCloud — Alternative Cohort):
1. Open [GroqCloud Console](https://console.groq.com/) and sign in.
2. Navigate to `Settings > Billing`. Confirm that **no payment method is on file** and the tier is **Free**.
3. Create an API key under **API Keys**.
4. Set the key in your local shell:
   ```powershell
   $env:GROQ_API_KEY="gsk_..."
   ```
5. Authorize a minimal single-trial smoke test.

---

## 5. What Remains Unverified

1. **Current Google Project Billing Attachment:** We cannot programmatically query whether the user's specific Google AI Studio project has an active Google Cloud Billing account linked. The operator must check this manually in the Google Cloud Console.
2. **Groq Llama-3.3-70B DOM Token Truncation on Complex Pages:** While Llama 3.3 70B supports 128k context, its latency and token consumption on extremely deep accessibility trees should be validated with a single test run before full batching.
3. **OpenRouter / Mistral Quota Reset Calendars:** Specific daily token ceilings on Mistral free tier are not published with fixed numbers and fluctuate with platform load.

# Free API Provider Audit for Browser Agent Research

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date of Audit:** October 24, 2026  
**Auditor:** Autonomous Senior Research Engineer (DeepMind Antigravity System)  
**Deliverable:** `FREE_API_PROVIDER_AUDIT.md`  
**Core Objective:** Comprehensive evaluation and safety ranking of genuinely free, recurring LLM API providers with zero risk of automatic credit card charges.

---

## 1. Executive Summary & Evaluation Criteria

To complete the remaining 45 scheduled trials of the 3-arm web agent experiment without financial risk, candidate LLM providers were investigated against strict institutional and financial constraints.

### The Zero-Spend Safety Hierarchy
Providers are ranked strictly in the following priority order:
1. **Billing Safety (Hard Limit Enforcement):** Can the provider charge money under *any* circumstance? If an account has no credit card attached, can an invoice or debt accrue? Does exceeding quota result in an immediate HTTP `429 Too Many Requests` hard stop?
2. **Framework Compatibility:** Does the provider support structured tool/function calling required by autonomous browser agents (`browser-use 0.13.10`) for element interaction (`click`, `input`, `scroll`, `done`)?
3. **Quota Viability:** Does the recurring free daily allowance support the experimental workload (~45 trials $\times$ ~6.5 steps $\approx$ 293 requests)?
4. **Reproducibility & Model Quality:** Is the model architecture and version fixed, transparent, and sufficiently capable to follow multi-turn browser automation instructions?

---

## 2. Comprehensive Provider Comparison Matrix

| Provider | Official Signup URL | Recommended Free Model | Card Required? | Overages Possible? | Quota Hard Stop | Free Daily Quota / Rate Limits | Browser-Agent Tool Calling Support | Data Privacy Policy | Recommendation & Rank |
|:---|:---|:---|:---:|:---:|:---:|:---|:---:|:---|:---:|
| **Google AI Studio** | `https://aistudio.google.com/` | `gemini-2.0-flash` / `gemini-1.5-flash` / `gemini-3.1-flash-lite` | **NO** (Google Account only) | **NO** (unless Cloud Billing linked) | **YES** (HTTP 429 `RESOURCE_EXHAUSTED`) | **15 RPM / 1,500 RPD / 1M TPM** (Resets daily at 00:00 PST) | **Native** (`browser-use` `ChatGoogle` / LangChain) | Free tier prompts reviewed by humans & used for model training | **Rank 1 (Co-Leader)** (Best continuity; keep Cloud Billing unlinked) |
| **GroqCloud** | `https://console.groq.com/` | `llama-3.3-70b-versatile` / `llama-3.1-8b-instant` | **NO** (GitHub/Email login) | **NO** (Zero overage risk on Free Tier) | **YES** (HTTP 429 `Too Many Requests`) | **30 RPM / 14,400 RPD** (8B); **30 RPM / 1,000 RPD** (70B) | **High** (Native OpenAI tool schema via `ChatGroq`) | Retained 30 days for safety; not trained on user data | **Rank 1 (Co-Leader)** (Best cardless safety & highest free speed) |
| **OpenRouter** | `https://openrouter.ai/` | `meta-llama/llama-3.3-70b-instruct:free` | **NO** (Email / Web3) | **NO** (Prepaid only; cannot exceed $0 balance) | **YES** (HTTP 429 / 402) | **20 RPM / 50 RPD** (Strict daily cap for zero-deposit accounts) | **Medium** (Subject to upstream tool parsing variance) | Routes to upstream host policy | **Rank 3** (Safe from billing, but 50 RPD is too small for 45 runs) |
| **Mistral AI (La Plateforme)** | `https://console.mistral.ai/` | `mistral-small-latest` / `codestral-latest` | **NO** (Email sign-in) | **NO** (Free experimentation mode) | **YES** (HTTP 429) | **~1 RPS (~60 RPM)**, unstated daily token cap (monitored in console) | **High** (Native function calling via `ChatMistral`) | Retained per EU compliance; optional opt-out | **Rank 4** (Good API, but undocumented daily quotas for free tier) |
| **Cloudflare Workers AI** | `https://ai.cloudflare.com/` | `@cf/meta/llama-3.1-8b-instruct` | **NO** (Workers Free plan) | **NO** (Hard stops at limit on Free plan) | **YES** (Execution halts with limit error) | **10,000 Neurons/day** (~100k tokens/day) | **Low** (Tool calling requires custom wrappers; not plug-and-play) | Standard Cloudflare privacy | **Rank 5** (Complex integration; low daily token budget) |
| **NVIDIA NIM** | `https://build.nvidia.com/` | `meta/llama-3.3-70b-instruct` | **NO** (NVIDIA Developer Program) | **NO** (Prototyping tier only) | **YES** (Cooldown up to 24h) | **Dynamic (~40 RPM)**; no guaranteed daily volume | **Medium** (OpenAI compatible endpoint) | Enterprise sandbox terms | **Rank 6** (Evaluation catalog; no stable recurring production SLA) |
| **SambaNova Cloud** | `https://cloud.sambanova.ai/` | `Meta-Llama-3.3-70B-Instruct` | **NO** (Email signup) | **NO** (Free tier halts) | **YES** (HTTP 429) | **20 RPM / 20 RPD** | **High** (OpenAI compatible) | Standard platform terms | **Rank 7** (20 RPD limit is far too low) |
| **Cerebras Cloud** | `https://cloud.cerebras.ai/` | `llama-3.3-70b` | **YES** (Card required for $5 trial credit) | **Risk of Auto-Billing** | **Uncertain** | 5 RPM (Trial) | High | Standard terms | **DISQUALIFIED** (Mandatory payment card on file) |
| **GitHub Models** | `https://github.com/marketplace/models` | N/A | N/A | N/A | N/A | **RETIRED** (Service fully shut down July 30, 2026) | N/A | N/A | **DISQUALIFIED** (Service retired) |

---

## 3. Deep-Dive Provider Audits

### 1. Google AI Studio / Gemini API Free Tier
- **Official Documentation Source:** `https://ai.google.dev/pricing` (Verified: October 2026)
- **Rate Limits & Allowance:**
  - 15 Requests Per Minute (RPM)
  - 1,500 Requests Per Day (RPD)
  - 1,000,000 Tokens Per Minute (TPM)
  - Reset timing: Midnight Pacific Time (00:00 PST / 08:00 UTC).
- **Payment Card Requirement:** **None.** A standard consumer Google account provides full access to API keys.
- **Billing & Overages:**
  - If **no Google Cloud Billing account** is linked to the project, overages are technically impossible. Google Cloud does not possess payment credentials, and the API throws `429 RESOURCE_EXHAUSTED` when quota is exceeded.
  - *Critical Risk Caveat:* If an operator accidentally creates an API key under an existing Google Cloud Project that has an active linked credit card, requests that exceed free tier rates can silently roll over to Pay-As-You-Go pricing.
- **Model Availability:** `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-3.1-flash-lite`.
- **Browser-Agent Tool Calling:** Native support in `browser-use 0.13.10` via `ChatGoogle` and `langchain-google-genai`.
- **Data Privacy:** On the free tier, user prompts and responses may be reviewed by human annotators and used to train future Google models.

---

### 2. GroqCloud
- **Official Documentation Source:** `https://console.groq.com/docs/rate-limits` / `https://groq.com/pricing/` (Verified: October 2026)
- **Rate Limits & Allowance:**
  - `llama-3.1-8b-instant`: 30 RPM, 14,400 RPD, 30,000 TPM.
  - `llama-3.3-70b-versatile`: 30 RPM, 1,000 RPD, 6,000 TPM.
  - Resets daily on a rolling 24-hour basis.
- **Payment Card Requirement:** **None.** Registration requires only an email address or GitHub/Google SSO.
- **Billing & Overages:**
  - Groq does not collect payment details for the Free Tier.
  - Exceeding limits results in HTTP `429 Too Many Requests`.
  - There are no negative account balances, no automatic upgrades, and zero overage fees. Upgrading to the Developer Tier requires manually entering a credit card in billing settings.
- **Browser-Agent Tool Calling:**
  - 100% OpenAI-compatible endpoint (`https://api.groq.com/openai/v1`).
  - Native function calling support with JSON schema parsing.
  - Supported directly by `browser-use 0.13.10` via `ChatGroq` (already installed and verified in `.venv311`).
- **Data Privacy:** Prompt data is retained for 30 days for safety and abuse prevention, but is explicitly **not** used to train commercial models.

---

### 3. OpenRouter (`:free` endpoints)
- **Official Documentation Source:** `https://openrouter.ai/docs` / `https://openrouter.ai/models` (Verified: October 2026)
- **Rate Limits & Allowance:**
  - Accounts with $0.00 lifetime deposit: **20 RPM / 50 RPD**.
  - Accounts with $\ge \$10.00$ lifetime deposit: **20 RPM / 1,000 RPD**.
- **Payment Card Requirement:** **None** for the basic 50 RPD tier.
- **Billing & Overages:**
  - OpenRouter is strictly prepaid. If balance is $0.00, it cannot generate an invoice or credit card charge.
  - However, if the daily 50 RPD cap is hit, it returns HTTP `429` or `402 Payment Required`.
- **Limitations for this Experiment:**
  - 50 RPD is insufficient for completing the remaining 45 scheduled trials in a single day (requires ~293 requests). Execution would require 6 consecutive days of 50-request increments.
  - Free models on OpenRouter experience extreme upstream congestion and intermittent tool-calling timeouts during peak hours.

---

### 4. Mistral AI (La Plateforme Free Tier)
- **Official Documentation Source:** `https://console.mistral.ai/` / `https://docs.mistral.ai/` (Verified: October 2026)
- **Rate Limits & Allowance:**
  - Tier designated as "Free Mode" / "Experimentation".
  - Rate limit: ~1 request per second (~60 RPM).
  - Monthly token quotas are dynamic and monitored in the developer console.
- **Payment Card Requirement:** **None** to register and use free experimentation keys.
- **Billing & Overages:** Hard stops at quota with HTTP `429`. No credit card on file means zero billing risk.
- **Browser-Agent Tool Calling:** High compatibility with OpenAI tool calling conventions via `ChatMistral`.

---

## 4. Ranking Summary & Decision Rationale

### Tier 1 (Highly Recommended & Verified Safe)
1. **Google AI Studio (Gemini Free Tier):**
   - *Pros:* 1,500 RPD easily completes all remaining 45 trials in a single run; native compatibility with existing runner; preserves exact model lineage (`gemini-3.1-flash-lite`).
   - *Prerequisite:* User must verify in Google Cloud Console that the API key belongs to a standalone project with **NO linked billing account**.
2. **GroqCloud (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`):**
   - *Pros:* Absolute cardless signup; 1,000 to 14,400 RPD; hard HTTP 429 stops; native `ChatGroq` in `browser-use`; exceptional inference speed (~300 tokens/sec).
   - *Scientific Note:* Switching to Llama 3.3 requires treating the data as a separate experimental cohort to avoid confounding with Gemini runs 1–27.

### Tier 2 (Viable but Constrained)
3. **OpenRouter Free Tier:** Safe from billing, but capped at 50 RPD without payment.
4. **Mistral AI:** High tool quality, but undocumented monthly quota ceiling on free tier.

### Tier 3 (Not Recommended / Disqualified)
5. **Cloudflare Workers AI:** Non-standard tool schema integration; small 10k neuron allowance.
6. **Cerebras Cloud:** Disqualified (requires verified credit card on file).
7. **GitHub Models:** Disqualified (retired service).

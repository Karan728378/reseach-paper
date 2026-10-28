# CONFIRMATORY EXPERIMENTAL PROTOCOL (PROTOCOL V5)
## The DOM Serialization Gap: Causal Impact of Semantic Channel Delivery on Autonomous Web Agent Task Performance

**Protocol Version:** 5.0-CONFIRMATORY  
**Date (UTC):** 2026-10-27T01:35:00Z  
**Status:** **FROZEN / PRE-REGISTERED DESIGN ONLY — NOT EXECUTED**  
**Evidence Class:** **E5 (Experimental Protocol Design / Synthetic Specification)**  
**Target Execution Gate:** Phase 11 Authorization Required Prior to Dispatch  

---

## 1. Hypotheses and Outcome Definitions

### Primary Scientific Hypothesis ($H_1$)
In web tasks where target-identifying metadata is present *exclusively* in DOM attributes (and absent from visible typography), expanding the client-side serialization whitelist (`DATA-CFG`) significantly increases task completion rate relative to the default unextended serializer (`ABS`):
$$\mathcal{H}_0: \theta_{\mathrm{MH}} = 0 \quad \text{vs.} \quad \mathcal{H}_1: \theta_{\mathrm{MH}} > 0$$
where $\theta_{\mathrm{MH}}$ is the Cochran-Mantel-Haenszel stratified risk difference across task blocks.

### Primary Outcome (Strict Binary Oracle)
- **Metric:** Binary task success $Y_{ij} \in \{0, 1\}$.
- **Evaluation Mechanism:** Pure DOM-state oracle reading Chromium `localStorage.cart` after browser execution.
- **Rule:** Never relies on LLM self-report, assistant messages, or intermediate text. Evaluated exclusively by asserting that the target SKU (`target-sku-101`) is present in `localStorage.cart` and distractor SKU (`distractor-sku-202`) is absent.

### Secondary Outcomes (Exploratory / Non-Causal)
1. Step count to completion ($S \in [1, \text{max\_steps}]$).
2. Wall-clock duration (seconds).
3. Total input and output token consumption as reported by provider response metadata.

---

## 2. Calibrated Task Battery & Confound Elimination

To eliminate the ceiling effect identified in Phase 9 (where visible typography yielded 100% solvability in all arms), tasks are strictly calibrated across three distinct experimental task types:

| Task Type | Description | Decisive Channel | Oracle Reachability (Arm 1: ABS) | Oracle Reachability (Arm 2: ARIA) | Oracle Reachability (Arm 3: DATA-CFG) | Expected Null / Contrast |
|---|---|---|:---:|:---:|:---:|---|
| **Type I: Isolated Attribute Contrast (Probe A)** | Visible text identical ('Select Item'); identity encoded exclusively in `data-product-id`. | Developer `data-*` | $p = 0.5$ (Unsolvable) | $p = 0.5$ (Unsolvable) | **$p = 1.0$ (Solvable)** | **Primary Causal Test:** Measures causal effect of attribute whitelist delivery. |
| **Type II: Container ARIA Contrast (Probe B)** | Visible text identical ('Standard Model Option'); identity in container `role="region"` `aria-label`. | Container ARIA | $p = 0.5$ (Unsolvable) | $p = 0.5$ (Unsolvable) | $p = 0.5$ (Unsolvable) | **Negative Control 1:** Proves agent cannot bypass framework container stripping (L1046). |
| **Type III: Visible Typography Control (Positive Control)** | Rendered typography explicitly displays target SKU and unique model name. | Visible Text | **$p = 1.0$ (Solvable)** | **$p = 1.0$ (Solvable)** | **$p = 1.0$ (Solvable)** | **Positive Control:** Validates browser action execution and cart oracle reachability. |
| **Type IV: Negative Distractor Probe (Negative Control 2)** | Neither button contains target SKU; target is entirely absent from DOM and attributes. | None | $p = 0.0$ (Chance) | $p = 0.0$ (Chance) | $p = 0.0$ (Chance) | **Negative Control 2:** Validates agent refusal vs hallucinated action execution. |

### Confound Controls
1. **Position Swapping:** Every probe includes an alternating `?swap=true` parameter that reverses DOM order of cards, ensuring the target element appears with equal frequency in position 0 and position 1 ($50\%$ index 1, $50\%$ index 2).
2. **Fixed Randomization Seed:** Blocking by task with pseudo-random assignment generated via stored seed (`SEED = 421098`).
3. **Automated Stage 5 Prompt Assertion:** Every trial intercepts the final payload sent to the LLM and asserts via regex:
   - For `DATA-CFG`: asserts `data-product-id="target-sku-101"` is present in user message prompt.
   - For `ABS`: asserts `data-product-id` is absent from prompt.
   - If assertion fails, the trial is flagged as a pipeline anomaly and excluded prior to outcome evaluation.
4. **Deterministic Environment:**
   - `use_vision = False` enforced.
   - Headless Chromium with fresh `incognito` browser context per trial.
   - Fixed viewport: $1280 \times 800$, locale `en-US`.
   - Temperature pinned to $0.0$.
   - Max steps pinned to 4.

---

## 3. Sample Size and Statistical Power

### Planned Sample Allocation (RCBD Design)
- **Arms:** 3 arms (`ABS`, `ARIA`, `DATA-CFG`).
- **Task Strata:** 4 task strata (Type I Probe A, Type II Probe B, Type III Positive Control, Type IV Negative Probe).
- **Position Variants:** 2 position variants (Original, Swapped) per task.
- **Blocks:** 4 balanced temporal blocks.
- **Sample Size:**
  - $3 \text{ arms} \times 4 \text{ tasks} \times 2 \text{ swap} = 24 \text{ trials per block}$.
  - $4 \text{ blocks} = \mathbf{96 \text{ total trials}}$ ($32$ per arm).
- **Statistical Power (from Phase 7 Monte Carlo Reproduction):**
  - For detecting $\Delta = 0.70$ (Type I Probe A contrast: $0.50 \to 1.00$): **Statistical Power $> 99.9\%$.**
  - For detecting $\Delta = 0.35$: **Power $= 64.2\%$.**
  - Family-wise error rate controlled at $\alpha_{\mathrm{adj}} = 0.05 / 3 = 0.0167$ via Bonferroni adjustment.

---

## 4. Operational Budget, Quota Limits & Safety Controller

| Parameter | Confirmatory Study Limit | Safety Guardrail Enforcement |
|---|---|---|
| **Target Model** | Groq API `llama-3.3-70b-versatile` or `gemini-2.5-flash-lite` | Provider model version pinned in run metadata. |
| **Max Trials** | 96 planned + max 4 infrastructure retries = **100 trials** | Hard execution loop termination. |
| **Max Steps per Trial** | 4 steps | Bounded in `Agent(max_steps=4)`. |
| **Max Total API Calls** | $100 \times 4 = \mathbf{400 \text{ calls}}$ | `LocalBudgetGuard` hard request ceiling. |
| **Estimated Input Tokens** | $\approx 1,200 \text{ tokens/call} \times 400 = 480,000 \text{ tokens}$ | Pre-call token reservation. |
| **Estimated Output Tokens** | $\approx 80 \text{ tokens/call} \times 400 = 32,000 \text{ tokens}$ | Bounded output length. |
| **Financial Spend Cap** | **$0.00 USD (Free Tier)** or **$\le \$0.50 USD (Paid Tier)** | Hard budget stop at $\ge \$1.00$. |
| **Rate Limit Pacing** | Inter-trial sleep: $\ge 6.0 \text{ seconds}$ | Effective RPM $\le 8$ (well under 15 RPM / 30 RPM limits). |
| **Abort Rules** | Halt immediately upon: 3 consecutive 429/503 errors; single 401/403 credential error; any budget overrun. | Automated exception interceptor. |

---

## 5. Pre-Registration Cryptographic Binding

- This protocol document and its accompanying machine-readable specification `protocol.json` are frozen prior to any live data collection.
- Any subsequent modifications must be documented in `PROTOCOL_VERSION_HISTORY.md` with explicit justification.
- If live execution is not authorized by the Principal Investigator in Phase 11, the study remains an offline systems audit and validity framework (Models A + B).

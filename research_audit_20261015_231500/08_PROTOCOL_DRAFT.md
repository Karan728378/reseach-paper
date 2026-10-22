# 08. Protocol Freeze Draft: Web Agent Information Delivery Benchmark (Protocol v3)

**Protocol Identifier:** `PROTO-AGENT-CHANNELS-2026-V3`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Research Question & Formal Hypotheses

### Primary Research Question
*For product facts delivered through verified-exposed DOM channels, does the delivery channel affect LLM browser agent retrieval accuracy compared with visible-text and absent controls?*

### Formal Hypotheses
- **$H_{0}$ (Null):** Retrieval accuracy does not differ between visible text ($VIS$), accessible ARIA ($ARIA$), and configured data attributes ($DATA\text{-}CFG$):
  $$P(\text{Success} \mid VIS) = P(\text{Success} \mid ARIA) = P(\text{Success} \mid DATA\text{-}CFG)$$
- **$H_{1}$ (Alternative):** Retrieval accuracy differs across exposed delivery channels.
- **$H_{control}$ (Validation):** Retrieval accuracy in all exposed channels significantly exceeds the absent negative control ($ABS$).

---

## 2. Experimental Conditions (4 Arms)

1. **ABS (Negative Control):** The target fact is omitted entirely from the page. Tests base-rate guessing and model hallucination.
2. **VIS (Human Visible Baseline):** The target fact appears exclusively in standard visible body text (e.g. `<p class="spec-value">LOT-9821</p>`).
3. **ARIA (Accessible Semantic Channel):** The target fact appears exclusively inside an `aria-label` attribute on an interactive element (e.g. `<button id="btn-buy" aria-label="Purchase Item. Manufacturing Lot: LOT-9821">Add to Cart</button>`).
4. **DATA-CFG (Configured Machine Attribute Channel):** The target fact appears exclusively in a `data-*` attribute on an interactive element (e.g. `<button id="btn-buy" data-lot-code="LOT-9821">Add to Cart</button>`), with `include_attributes` enabled in the browser-use agent configuration.

---

## 3. Experimental Tasks (6 Tasks)

| Task ID | Task Description | Target Fact Type | Example Ground Truth | Success Criterion | Verifier Method |
|---|---|---|---|---|---|
| **T1** | Retrieve Product Warranty Duration | Integer months | `"36 months"` | Exact string/number match | Verifies agent `done` text contains `"36 months"` or `36` |
| **T2** | Retrieve Manufacturing Lot Code | Alphanumeric token | `"LOT-8842-X"` | Exact token match | Verifies agent `done` text contains `"LOT-8842-X"` |
| **T3** | Retrieve Exact Stock Count | Discrete integer | `43` | Exact integer match | Verifies agent `done` text contains `43` |
| **T4** | Retrieve Extended Return Window | Integer days | `"45 days"` | Exact integer match | Verifies agent `done` text contains `45` |
| **T5** | Retrieve Expedited Ship-by Date | ISO date string | `"2026-11-04"` | Exact date format | Verifies agent `done` text contains `"2026-11-04"` |
| **T6** | Grounded Action: Add Item by Lot Code | Browser Action | SKU `wh-002` | Cart contains SKU | Verifies `window.__cart__[0].sku === 'wh-002'` |

---

## 4. Information Parity & Anti-Leakage Constraints

1. **Single-Source Invariance:** For any trial, the target fact exists in **exactly one channel**.
2. **Visual Parity:** In ARIA and DATA-CFG conditions, the fact must not appear in the visual viewport or in screenshots.
3. **Interactive Element Placement:** To ensure exposure under default and whitelist serializers, all attribute treatments must be placed on **interactive elements** (e.g. `<button>`, `<input>`, `<a>`).
4. **Token Parity:** The exact string representation of the target fact is identical across all exposed conditions.

---

## 5. Agent & Harness Configuration

- **Agent Framework:** `browser-use==0.13.10`
- **Model:** `gemini-flash-lite-latest` (or `gemini-2.5-flash-lite`) via `ChatGoogleGenerativeAI`
- **Vision:** `use_vision=True`, `llm_screenshot_size=(1280, 800)`
- **Timeout:** `step_timeout=60`, `max_steps=15`
- **Attribute Whitelist (for DATA-CFG arm):**
  ```python
  include_attributes = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
      "data-warranty", "data-lot-code", "data-stock-count", "data-return-window", "data-ship-date"
  ]
  ```

---

## 6. Block Structure, Randomization & Trial Schedule

- **Design:** $6 \text{ Tasks} \times 4 \text{ Conditions} = 24 \text{ Trials per Block}$.
- **Blocks ($R$):** 4 complete blocks ($R = 4$).
- **Total Sample Size:**
  $$N = 6 \times 4 \times 4 = \mathbf{96\text{ runs}}$$
- **Randomization:** Within each block of 24 runs, trials are executed in a randomized order generated via a fixed seed:
  `random.seed(20261020)`
- **Quota Circuit Breaker:**
  - If any run encounters HTTP 429 (`RESOURCE_EXHAUSTED`), execution pauses for 60 seconds.
  - If a second consecutive 429 occurs, the runner aborts execution immediately.
  - **Zero Selective Retries:** Aborted or failed runs are recorded as failed/missing; they are never silently replaced.

---

## 7. Statistical Analysis & Hypothesis Testing

1. **Primary Model:** Generalized Linear Mixed Model (GLMM) with logit link:
   $$\text{logit}(P(Y_{ijb} = 1)) = \beta_0 + \beta_{ARIA} \cdot X_{ARIA} + \beta_{DATA} \cdot X_{DATA} + \beta_{ABS} \cdot X_{ABS} + u_j + v_b$$
   where $u_j \sim \mathcal{N}(0, \sigma_u^2)$ accounts for task-level clustering, and $v_b \sim \mathcal{N}(0, \sigma_v^2)$ accounts for block-level clustering. Reference category: $VIS$.
2. **Pairwise Comparisons:** Evaluated using Wald tests with Holm-Bonferroni correction ($\alpha = 0.05$).
3. **Missing Data Reporting:** If quota truncation occurs, the exact index of truncation is reported. Both available-case analysis and worst-case imputation ($Y = 0$) will be disclosed.

# FUTURE BEHAVIORAL EXPERIMENT DESIGN: CHANNEL-ISOLATED AGENT EVALUATION (PROTOCOL V4 RCBD)

**Protocol Status:** PROPOSED EXPERIMENTAL PROTOCOL (UNEXECUTED FUTURE WORK)  
**Date:** October 25, 2026  
**Document Purpose:** Formal design for future confirmatory behavioral experiments isolating semantic metadata channels.  
**Strict Compliance Notice:** This document represents an unexecuted research proposal. It is not completed empirical work. No live API calls or model evaluations have been conducted under this protocol. Quota ceiling is strictly enforced (`halted_due_to_ceiling: true`).

---

## 1. Executive Summary & Causal Identification Problem

Prior empirical evaluations of web agents across semantic markup variants suffered from two severe methodological limitations:
1. **The Observation Gap:** Non-interactive semantic markup (Schema.org JSON-LD and parent container ARIA) is stripped by client-side serializers before entering the model prompt, making it causally impossible for the markup to influence model decisions.
2. **The Ceiling Effect:** Simple web tasks (e.g., finding and clicking a unique, prominent product) allow frontier LLMs to succeed at $100\%$ completion using unaugmented visible typography alone ($\hat{\theta} = 0.0$).

To evaluate whether semantic metadata provides behavioral utility to autonomous browser agents, future experimental designs must satisfy **three non-negotiable criteria**:
- **Information Exclusivity:** The critical decision-making fact must exist *solely* within the targeted metadata channel and must *not* be duplicated in visible typography or trivial URL slugs.
- **Verified Prompt Delivery:** An automated manipulation check must verify that the targeted channel actually survives serialization into the model prompt buffer.
- **Difficulty Calibration:** Tasks must be sufficiently complex that the control baseline does not achieve a ceiling ($p_{\text{control}} \le 0.70$), leaving headroom to detect additive effects.

---

## 2. Channel-Isolated Stimulus Design & Fact Partitioning

### 2.1 The Information Exclusivity Matrix
In this design, we define four experimental website variants where critical decision facts are partitioned strictly into specific architectural channels:

| Condition / Arm | Markup Variant | Target Fact Location | Model-Visible Information in Prompt | Control Condition Contrast |
| :--- | :--- | :--- | :--- | :--- |
| **Arm 1: Visible Text Only (Control, `ABS`)** | `v0-baseline` | Visible body text only | Product title, visible price, generic button (`Add item to cart`). | Reference baseline |
| **Arm 2: Semantic Accessibility (`ARIA`)** | `v2-aria` | Interactive WAI-ARIA attributes | Generic visible text + `aria-describedby` or interactive element semantic roles indicating product specs. | Evaluates interactive ARIA semantics |
| **Arm 3: Developer Custom Metadata (`DATA-CFG`)** | `v3-data-attrs` | Whitelisted `data-*` attributes | Generic visible text + whitelisted `data-sku`, `data-spec` on interactive buttons. | Evaluates custom developer attributes |
| **Arm 4: Multimodal Vision Baseline (`VIS-MM`)** | `v0-baseline` + Screenshots | Pixel rendering | Rendered visual layout, typography, badges, visual boundaries. | Bypasses DOM serializer bottlenecks entirely |

### 2.2 Eliminating the Action-Label Co-Location Confound
To prevent trivial keyword matching:
- **Prohibited:** Embedding target product names in button labels (e.g., `<button aria-label="Add SoundFlow Air 3 to cart">`).
- **Standardized Requirement:** All action buttons across all variants must use identical, generic trigger labels:
  ```html
  <!-- Standardized Generic Action Triggers -->
  <button class="btn-cart" aria-label="Add item to cart" data-action="add-cart">Add to Cart</button>
  ```
- **Consequence:** The model cannot succeed via simple string matching on button tags; it must perform hierarchical reference resolution between product specification containers and the corresponding action trigger.

---

## 3. Automated Manipulation Check (Offline Prompt-Diff Assertion)

Before any live inference is dispatched, an automated assertion must verify that the prompt buffers delivered to the model actually differ:

```python
def assert_prompt_manipulation_check(obs_control: str, obs_treatment: str, channel_token: str):
    """
    Verifies that the treatment observation buffer:
    1. Is non-identical to the control buffer (SHA-256 hash mismatch).
    2. Contains the expected channel-isolated metadata token.
    3. Does not leak target entity names into action button attributes.
    """
    assert obs_control != obs_treatment, "FAIL: Observation buffers are identical (Zero Manipulation)!"
    assert channel_token in obs_treatment, f"FAIL: Target token '{channel_token}' was stripped by serializer!"
    assert "aria-label=Add item to cart" in obs_treatment, "FAIL: Action label was confounded!"
```

---

## 4. Calibrated Task Battery & State-Asserted Verifiers

To prevent ceiling effects and test diverse observation channels, tasks require multi-step reasoning, constrained attribute filtering, or appropriate refusal:

| Task ID | Task Description | Target Channel / Required Fact | State-Asserted Verifier (DOM Ground Truth) | Target Difficulty |
| :--- | :--- | :--- | :--- | :---: |
| **T1: Spec-Constrained Selection** | Add headphone with lowest latency (35ms vs 80ms) | Latency spec in metadata (`data-spec` / `aria-describedby`) | `window.__cart__[0] == "wh-003"` | Hard ($p \approx 0.50$) |
| **T2: Compatibility Resolution** | Add keyboard compatible with Linux kernel 6.x | Compatibility list in semantic attribute | `window.__cart__[0] == "kb-linux-02"` | Moderate ($p \approx 0.60$) |
| **T3: Multi-Item Budget Optimization** | Select 2 items whose combined total $\le \$100$ | Unit price & tax tag in container attribute | `len(cart) == 2 and sum(prices) <= 100` | Hard ($p \approx 0.40$) |
| **T4: Transactional Checkout** | Complete 3-step checkout with coupon code | Form validation state & step status | `window.__order_confirmed__ is True` | Moderate ($p \approx 0.65$) |
| **T5: Negative Constraint (Hidden Spec)** | Select item only if certified energy star | Fact located in JSON-LD `<script>` tag | Correct cart addition if found; refusal if pruned | Hard ($p \approx 0.45$) |
| **T6: Absent-Fact Probe (Mandatory Refusal)** | Find item with IP68 rating (absent from page) | Target fact non-existent anywhere in page | Agent outputs explicit refusal action without clicking | Hard ($p \approx 0.50$) |

### Verifier Principles
- Verifiers query browser execution state directly via CDP (`Runtime.evaluate`).
- No credit is awarded based on agent natural-language assertions or intermediate navigation steps; success requires exact DOM state transitions.
- On T6 (Absent-Fact Probe), success requires an explicit stop/refusal action stating the attribute is missing. Clicking any item or timing out is scored as failure (`score = 0.0`).

---

## 5. Statistical Power, Sample Sizes, and Analysis Plan

### 5.1 Pre-Specified Sample Size Calculation
Using the Two One-Sided Tests (TOST) equivalence framework (Section 6.3 of the main manuscript):
- Nominal significance level: $\alpha = 0.05$ (two one-sided tests at $\alpha = 0.05$).
- Target statistical power: $1 - \beta = 0.80$.
- Pre-registered equivalence margin: $\delta_{\text{equiv}} = \pm 0.10$ (10 percentage points).
- Estimated baseline performance: $p = 0.70$.

**Sample Size Requirements:**
- **Superiority Testing ($\Delta \ge 0.20$):** $n = 97$ trials per arm ($N = 388$ across 4 arms).
- **Equivalence Testing ($|\Delta| < 0.10$):** $n = 360$ trials per arm ($N = 1,440$ across 4 arms).
- **Clustered Design Adjustment ($\rho = 0.10$, $\text{DEFF} = 1.30$):** $n = 468$ trials per arm ($N = 1,872$ across 4 arms).

### 5.2 Pre-Specified Inferential Analysis Plan
1. **Primary Stratified Test:** Continuity-corrected Cochran-Mantel-Haenszel (CMH) test stratified across the $K=5$ primary task categories (T1–T5).
2. **Exploratory Probe Analysis:** T6 evaluated separately for calibration of hallucinated vs. grounded refusal actions.
3. **Effect Size Estimation:** Risk difference $\hat{\theta} = p_{\text{treatment}} - p_{\text{control}}$ alongside 95% Newcombe hybrid score confidence intervals.
4. **Multiple Testing Control:** Bonferroni correction for 3 planned pairwise confirmatory comparisons against control ($\alpha = 0.05 / 3 = 0.0167$):
   - Contrast 1: `ARIA` vs. `ABS`
   - Contrast 2: `DATA-CFG` vs. `ABS`
   - Contrast 3: `VIS-MM` vs. `ABS`
5. **Equivalence Evaluation:** TOST evaluation against $\delta_{\text{equiv}} = \pm 0.10$. Non-significance on a superiority test ($p > 0.05$) will **never** be interpreted as equivalence.

---

## 6. Execution Safeguards, Stopping Rules, and Exclusion Criteria

1. **Randomized Block Allocation:** Trials must be dispatched in randomized complete blocks ($B_1, \dots, B_b$) to balance server load, API latency spikes, and provider drift.
2. **Retry Policy:**
   - Provider HTTP errors (e.g., `503 UNAVAILABLE`, `429 RATE_LIMIT`) may be retried up to 3 times with exponential backoff.
   - If attempt 4 fails, the trial is classified as `infrastructure_aborted` and excluded from behavioral per-protocol analysis (reported in sensitivity intent-to-treat analysis).
   - Agent errors (action timeouts, loop terminations, incorrect clicks) are recorded as trial failures (`score = 0.0`) and are **never** retried.
3. **Fail-Closed Quota Safeguards:** Bounded via thread-safe pre-dispatch reservation in `budget_controller.py`, with hard limits set in cloud provider consoles.
4. **Pre-Registered Stopping Rules:**
   - If cumulative API error rate exceeds $15\%$ across 20 consecutive trials, execution halts immediately for infrastructure diagnosis.
   - If control arm performance exceeds $90\%$ across the first 30 trials (indicating recurring ceiling effect), execution halts for task recalibration.

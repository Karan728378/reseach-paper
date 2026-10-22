# Protocol v4 Specification (Draft for Human Review)

**Protocol Title:** Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Document Version:** 4.0-DRAFT (Pre-Registration Draft)  
**Status:** DRAFT — REQUIRES HUMAN REVIEW AND FORMAL APPROVAL BEFORE EXECUTION  
**Safety Gate:** STRICTLY LOCKED (`--live` and `--confirm-live-execution` prohibited)  
**Date:** October 21, 2026  
**Auditor / Authors:** Antigravity Scientific Methodology & Protocol Architecture Team  

---

## 1. Research Question
> **Does augmenting a website displaying factual information in visible text with structured machine-readable markup (WAI-ARIA accessibility attributes or custom `data-*` developer attributes) significantly improve an autonomous text-based browser agent's task success rate, execution step efficiency, or latency, compared to unaugmented plain HTML?**

---

## 2. Primary Hypothesis
- **$H_{1}$ (Semantic Markup Superiority):** Adding semantic markup to an HTML document increases task completion success on complex, multi-item visual comparison and mutation tasks when an agent operates in text-only DOM mode (`use_vision=False`).
  - $H_{1\text{A}}$ (ARIA vs. Baseline): $P(Y=1 \mid \text{ARIA}) - P(Y=1 \mid \text{BASELINE}) > 0$
  - $H_{1\text{B}}$ (DATA-CFG vs. Baseline): $P(Y=1 \mid \text{DATA-CFG}) - P(Y=1 \mid \text{BASELINE}) > 0$

---

## 3. Secondary and Exploratory Hypotheses
- **$H_{2}$ (Comparative Markup Utility):** ARIA accessible names provide greater or lesser task utility than custom `data-*` attributes:
  $$P(Y=1 \mid \text{ARIA}) - P(Y=1 \mid \text{DATA-CFG}) \ne 0$$
- **$H_{3}$ (Navigation Efficiency):** Successful agent runs under semantic markup arms require fewer total browser actions ($S$) and lower latency ($T$) than baseline runs.
- **$H_{4}$ (Hallucination Resistance on Absent Facts):** When prompted to retrieve unstated entity attributes, agents operating on semantic markup variants demonstrate higher grounded refusal rates ($Y_{\text{refusal}} = 1$) than baseline agents.

---

## 4. Treatment Arms and Exact Operational Differences
The experiment defines 4 experimental arms ($K=4$):

| Arm ID | Schedule Alias | Variant Path | Whitelist Configuration | Operational Meaning |
|---|---|---|---|---|
| **Arm 1: BASELINE** | `ABS` | `variants/v0-baseline` | `DEFAULT_INCLUDE_ATTRIBUTES` | Unaugmented HTML; factual product data visible in typography; zero ARIA/data-* attributes. |
| **Arm 2: BASELINE_REP** | `VIS` | `variants/v0-baseline` | `DEFAULT_INCLUDE_ATTRIBUTES` | Replicate of Arm 1. Serves as internal stability check and temporal drift negative control. |
| **Arm 3: ARIA** | `ARIA` | `variants/v2-aria` | `DEFAULT_INCLUDE_ATTRIBUTES` | Semantic WAI-ARIA attributes (`aria-label`, `role`). Action buttons use de-confounded labels (`"Add item to cart"`). |
| **Arm 4: DATA-CFG** | `DATA-CFG` | `variants/v3-data-attrs` | `EXTENDED_ATTRIBUTES` | Custom machine-readable attributes (`data-action`, `data-product-id`, `data-amount`) whitelisted. |

---

## 5. Primary Outcome Definition
- **Outcome Metric:** Binary Grounded Action Success ($Y_{ijk} \in \{0, 1\}$) evaluated across the 5 primary benchmark tasks (T1–T5).
- **Operational Definition:** Strict verification of client application state (`window.__cart__`, `window.__orderConfirmed__`) evaluated directly via browser JavaScript evaluation immediately upon agent termination.
- **Scoring Rule:** Pure binary: $1.0$ for exact ground-truth state, $0.0$ for any failure, mismatch, timeout, or side effect. Zero partial credit.

---

## 6. Secondary Outcomes
1. **Grounded Refusal Rate ($Y_{\text{refusal}} \in \{0, 1\}$):** Evaluated strictly on Task T6 (absent warranty fact).
2. **Navigation Step Count ($S$):** Integer count of completed agent interaction turns (evaluated on successful runs).
3. **Execution Latency ($T$):** Total wall-clock execution duration in seconds.
4. **Clean Action Ratio ($R_{\text{clean}}$):** Ratio of successful DOM actions to total attempted actions.

---

## 7. Experimental Unit and Randomization Unit
- **Experimental Unit:** An individual task run attempt $(i, j, k)$ for Arm $i$, Task $j$, within Block $k$.
- **Design:** Randomized Complete Block Design (RCBD).
- **Blocking Factor:** Execution Block ($R=4$ blocks). Each block contains exactly one run of each Arm $\times$ Task combination.
- **Randomization:** Within-block run sequence is generated deterministically via pseudo-random shuffle (`seed=42`) pre-frozen in `proposed_randomized_schedule.csv`.

---

## 8. Task Selection and Task Difficulty
Five primary tasks spanning diverse operational complexities:
1. **T1 (Price Minimization Search):** Search for `"wireless headphones"`; add least expensive result (`wh-001`, $49.99). Requires price comparison (results sorted rating desc, so target is last).
2. **T2 (Direct Entity Addition):** Add `"Mechanical Keyboard Pro"` (`mkp-001`, $149.99) to cart.
3. **T3 (Rating Comparison):** Navigate to Audio category; compare ratings; add product with second-highest rating (`wh-002`, BudPro Wireless X, rating 4.5). Strict single-item exact match.
4. **T4 (Multi-Step Checkout):** Add `"ErgoGlide Mouse"` (`mse-001`) to cart; fill 8-field checkout form; submit order. Strict `order_confirmed == True`.
5. **T5 (Cart Item Mutation):** Cart pre-seeded with 1 item (`wh-001`); agent must navigate to cart and remove it. Verified precondition: `pre_cart_count == 1`. Postcondition: `len(cart) == 0`.
6. **T6 (Exploratory Probe):** Retrieve manufacturer warranty for `wh-001`. Fact is unstated on website; tests refusal vs hallucination.

---

## 9. Model Selection and Model-Version Recording
- **Primary Model:** Google Gemini (`gemini-flash-lite-latest` or `gemini-1.5-flash-latest`).
- **Secondary Model (Confirmatory Multi-Model Extension):** Anthropic Claude 3.5 Haiku or OpenAI GPT-4o-mini.
- **Metadata Logging:** Exact model identifier, API version, provider, temperature (0.0), and top-p must be recorded in every run log.

---

## 10. Repetition and Seed Policy
- **Determinism:** Agent temperature set to `0.0`.
- **Blocks:** 4 complete execution blocks.
- **Randomization Seed:** `seed=42` frozen for schedule sequence generation.

---

## 11. Browser Version and Toolchain Pinning
- **Browser:** Headless Chromium bundled with `browser-use` (pinned viewport `1920x1080`, device scale factor `1.0`).
- **Library Version:** `browser-use==0.13.10`.
- **Python Environment:** Python 3.11.9.

---

## 12. Initial-State and Environment Controls
- **Fresh Session:** Every single run executes in a completely clean, isolated `BrowserSession`.
- **Storage Isolation:** `localStorage`, session storage, and cookies cleared before every run.
- **Precondition Verification:** On T5, runner injects localStorage cart item and verifies `pre_cart_count == 1` before releasing agent.
- **Local HTTP Server:** Local server running on port 8093 to eliminate network latency variance.

---

## 13. Vision and Auxiliary Tool Policies
- **`use_vision = False` Strictly Enforced:** Multimodal screenshots disabled to isolate text-based DOM observation processing.
- **Auxiliary Tools:** Zero external calculator or web search tools.

---

## 14. Strict Verifier Definitions & T6 Resolution
- **T1:** `any(i['sku'] == 'wh-001' for i in cart)`
- **T2:** `any(i['sku'] == 'mkp-001' for i in cart)`
- **T3:** `len(cart) == 1 and cart[0]['sku'] == 'wh-002'` (single SKU exact match)
- **T4:** `order_confirmed == True and any(i['sku'] == 'mse-001' for i in last_order_items)`
- **T5:** `pre_cart_count == 1 and len(cart) == 0`
- **T6 Verifier Resolution (Formal Correction from Audit):**
  - Because warranty duration is absent from the site, stating `"36 months"` is an ungrounded hallucination.
  - **Protocol v4 Definition:**
    ```python
    refusal = bool(re.search(r'\b(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not)\b.*?\b(warranty|guarantee|found|find|stated|listed)\b', text, re.IGNORECASE))
    hallucination = bool(re.search(r'\b36\s*(months?|mo)\b', text, re.IGNORECASE))
    success = bool(refusal and not hallucination)
    ```
    An agent succeeds only if it explicitly reports absence and does not hallucinate.

---

## 15. Failure and Timeout Handling
- **Step Limit:** Maximum 30 interaction steps per run. Exceeding 30 steps is recorded as `failure` (`timeout_exceeded`).
- **Wall-Clock Timeout:** 120 seconds per run.
- **Crash vs Failure:** Execution crashes (e.g. process abort) are flagged as `INFRASTRUCTURE_ERROR`. Task completions where state fails ground truth are flagged as `TASK_FAILURE`.

---

## 16. Retry Policy: Elimination of Survivorship Bias
- **Terminal Execution:** Every executed run—whether `success=True` or `success=False`—is logged as a permanently **COMPLETED** trial.
- **Zero Domain Retries:** Failed runs are never re-attempted.
- **Resume Capability:** Only fatal infrastructure aborts (e.g. HTTP 429 quota exhaustion) can be resumed from the exact aborted index.

---

## 17. Exclusion Criteria Defined Prior to Data Collection
- Runs are excluded from analysis **only** in the event of documented infrastructure failures:
  1. HTTP 429 / API Quota Exhaustion.
  2. Local HTTP server connection dropped.
  3. Browser process crash before Step 1.
- Zero exclusion of valid runs where the agent performed actions and failed the task.

---

## 18. Missing Data Handling
- If an infrastructure crash occurs, the runner logs `status = ABORTED`.
- Upon resumption with active quota, the runner re-executes only the uncompleted schedule indices.
- Primary analysis evaluates only complete blocks.

---

## 19. Statistical Testing Framework
- **Primary Inferential Model:** Task-Stratified Cochran-Mantel-Haenszel (CMH) test across Tasks T1–T5 ($J=5$).
- **Effect Size:** Risk Difference ($\widehat{RD} = p_{\text{treat}} - p_{\text{base}}$) reported with Newcombe Hybrid Score 95% Confidence Intervals and Agresti-Caffo Adjusted Wald Intervals.
- **Internal Stability Check:** Fisher's exact test comparing `ABS` ($n=20$) vs `VIS` ($n=20$) across T1–T5. If $p \ge 0.10$, pool as Composite Baseline ($n=40$).

---

## 20. Multiple Comparison Correction
- Bonferroni correction for the 3 primary contrasts:
  $$\alpha_{\text{adj}} = \frac{0.05}{3} \approx 0.01667$$

---

## 21. Sample Size & Power Justification
- **Confirmatory Experiment Sizing:**
  - Detecting $\Delta = 0.20$ with $80\%$ power at $\alpha = 0.0167$ requires **$n \ge 120$ per arm** ($N \ge 480$ total across 4 arms).
- **Exploratory Pilot Option ($N = 96$):**
  - If executed with $N = 96$ ($n = 20$ per arm across T1–T5), the study is formally registered as an **Exploratory Pilot**.
  - **Mandatory Non-Equivalence Caveat:** Power is only $10.85\%$; failure to reject $H_0$ cannot be interpreted as proof of channel equivalence.

---

## 22. Stopping Rule
- Complete execution of all scheduled runs in deterministic RCBD order.
- Early stopping permitted **only** if safety gate is violated or persistent API billing limits are exceeded.

---

## 23. Logging and Data Provenance Requirements
- Every run logs:
  1. `run_index`, `block_id`, `arm`, `task_id`, `variant_mapping`.
  2. Raw agent history JSON with serialized prompt buffers and tool calls.
  3. Pre-state and post-state snapshots of `window.__cart__` and `window.__orderConfirmed__`.
  4. Terminal outcome (`success`, `step_count`, `latency_seconds`, `error_type`).
  5. SHA-256 hash of all variant HTML and script files.

---

## 24. API Cost Estimate and Spending Ceiling
- **Exploratory Pilot ($N = 96$):** Estimated cost $\approx \$0.15$ to $\$0.35$ on Gemini Flash Lite.
- **Confirmatory Study ($N = 480$):** Estimated cost $\approx \$0.75$ to $\$1.75$.
- **Hard Spending Ceiling:** $\le \$10.00$ USD. Live execution aborts immediately if spending exceeds ceiling.

---

## 25. Reproducibility and Release Plan
- Full code, task definitions, mock test suites, and analysis scripts released under open-source license.
- All historical datasets preserved in read-only state.

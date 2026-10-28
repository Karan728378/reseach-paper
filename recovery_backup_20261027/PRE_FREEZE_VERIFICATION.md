# Pre-Freeze Verification Report: Statistical Design, T6 Verifier, and Pipeline Delivery

**Document Version:** 1.0 (Final Pre-Freeze Verification)  
**Date:** October 21, 2026  
**Auditor / Lead:** Antigravity Scientific Methodology & Protocol Architecture Team  
**Compliance Status:** 100% Offline · Zero Live Model Invocations · Zero Credit Spend · Safety Gate Strictly Locked  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Statistical Design Verification: RCBD Model vs. Independent Proportions

### 1.1 Structural Reconciliation of the Experimental Design
The proposed experimental architecture is a **Randomized Complete Block Design (RCBD)** with balanced task-by-arm allocations across execution blocks:

- **4 Treatment Arms ($K=4$):**
  1. `BASELINE` (Nominal `ABS`): `variants/v0-baseline` with default attribute whitelist.
  2. `BASELINE_REP` (Nominal `VIS`): `variants/v0-baseline` with default attribute whitelist (identical DOM tree, temporal replicate).
  3. `ARIA`: `variants/v2-aria` with default attribute whitelist.
  4. `DATA-CFG`: `variants/v3-data-attrs` with configured extended attribute whitelist.
- **5 Primary Grounded Benchmark Tasks ($J=5$, Tasks T1–T5):**  
  Evaluating grounded state mutations (`window.__cart__`, `window.__orderConfirmed__`) with verified ground truth present in the HTML/JS application.
- **4 Balanced Execution Blocks ($R=4$, Blocks 1–4):**  
  Each block contains 1 trial per arm-task pair, balancing temporal server drift, background load, and provider API latency.
- **Reconciliation of Sample Size Counts:**
  - **Full Experimental Schedule:** $4 \text{ arms} \times 6 \text{ tasks} \times 4 \text{ blocks} = \mathbf{N = 96}$ runs.
  - **Primary Benchmark Benchmark:** $4 \text{ arms} \times 5 \text{ primary tasks} \times 4 \text{ blocks} = \mathbf{N = 80}$ runs.
  - **Per-Arm Primary Count:** $5 \text{ tasks} \times 4 \text{ blocks} = \mathbf{n = 20}$ runs per treatment arm.
  - **Per-Arm Full Count:** $6 \text{ tasks} \times 4 \text{ blocks} = \mathbf{n = 24}$ runs per treatment arm.
  - **Composite Baseline Pooling:** Because `BASELINE` and `BASELINE_REP` present identical DOM trees to the browser agent serializer, they pool into a composite baseline of $20 + 20 = \mathbf{n_{\text{base}} = 40}$ runs across T1–T5 (conditional on internal stability check $p_{\text{stab}} \ge 0.10$).
  - **Multiplicity Correction:** Three confirmatory pairwise contrasts against baseline ($A_2 \text{ vs Base}$, $A_3 \text{ vs Base}$, and $A_2 \text{ vs } A_3$). Bonferroni-adjusted significance threshold is:
    $$\alpha_{\text{adj}} = \frac{0.05}{3} \approx \mathbf{0.0167}$$

---

### 1.2 Independent Verification of Power: RCBD vs. Independent Proportions
The planned analysis specifies the **Task-Stratified Cochran-Mantel-Haenszel (CMH) test** as the primary inferential model. We independently verified the calculations using exact hypergeometric/binomial mathematics, RCBD logistic models, and Monte Carlo simulations ($B = 2,000$ iterations) implemented in [`reproduce_power_audit.py`](file:///C:/testing/research_execution_20261018/reproduce_power_audit.py):

| Shift ($\Delta = p_{\text{treat}} - p_{\text{base}}$) | Nominal $\alpha$ (Bonferroni) | Model 1: Unstratified Independent Binomial | Model 2: Planned Task-Stratified RCBD (CMH) | Finding Classification | Evidence & Rationale |
|:---:|:---:|:---:|:---:|:---:|---|
| **$\Delta = 0.20$** ($0.70 \to 0.90$) | $0.0167$ | $19.82\%$ | **$10.85\%$** (MC: $10.8\% \pm 0.7\%$) | **VERIFIED** | Task heterogeneity (baselines: $0.70, 0.85, 0.50, 0.30, 0.80$) and cell ceiling compression ($0.85 \to 0.95$, max $\Delta=0.10$) reduce effective power from $19.8\%$ to $10.85\%$. |
| **$\Delta = 0.15$** ($0.70 \to 0.85$) | $0.0167$ | $9.91\%$ | **$5.80\%$** (MC: $5.8\% \pm 0.5\%$) | **VERIFIED** | Near nominal alpha ($1.67\%$). Type II error rate is $\beta = 94.2\%$. |
| **$\Delta = 0.35$** ($0.50 \to 0.85$) | $0.0167$ | $65.10\%$ | **$49.63\%$** (MC: $49.7\% \pm 1.1\%$) | **VERIFIED** | 50% risk of Type II error even for large 35-percentage-point effects. |
| **$\Delta = 0.70$** ($0.10 \to 0.80$) | $0.0167$ | $99.91\%$ | **$98.54\%$** (MC: $98.8\% \pm 0.2\%$) | **VERIFIED** | Adequately powered under both models. |

#### Task Clustering & Design Effect (DEFF):
With intra-task correlation $\rho_{\text{task}} > 0$ and cell size $m = 4$:
$$\text{DEFF} = 1 + (m - 1)\rho_{\text{task}}$$
- At $\rho = 0.05$: $\text{DEFF} = 1 + 3(0.05) = 1.15$ (Sample size inflated by $15\%$).
- At $\rho = 0.15$: $\text{DEFF} = 1 + 3(0.15) = 1.45$ (Sample size inflated by $45\%$).

---

### 1.3 Sample Size Claim Classification

1. **VERIFIED CLAIMS:**
   - **$N = 96$ is Severely Underpowered ($< 11\%$ Power):** At $n = 20$ per treatment arm, power for a 20-percentage-point effect ($\Delta = 0.20$) is **$10.85\%$** under the stratified RCBD model. Type II error rate is $\beta = 89.15\%$.
   - **Power for $\Delta = 0.15$ is $5.80\%$:** Inconclusive and indistinguishable from nominal alpha.
   - **Design Counts Reconciled:** $N=96$ (schedule), $N=80$ (primary benchmark), $n=20$ (per arm), $n=40$ (composite baseline).
2. **ASSUMPTION-DEPENDENT CLAIMS:**
   - **"Sample size for $80\%$ power at $\Delta = 0.20$ requires $n \ge 120$ per arm ($N \ge 480$)":**  
     *Condition:* Valid when baseline success is centered at $p = 0.50$ (maximum variance: $p(1-p) = 0.25$).  
     *Sensitivity:* If baseline success is high ($p = 0.70 \to 0.90$), required sample size drops to $n \ge 83$ per arm ($N \ge 332$ total). If intra-task clustering is $\rho = 0.15$, DEFF inflates required size to $n \ge 144$ per arm ($N \ge 576$ total).
   - **"Sample size for $80\%$ equivalence within margin $\delta = \pm 0.10$ requires $n \ge 340$ per arm ($N \ge 1,360$)":**  
     *Condition:* Valid under Two One-Sided Tests (TOST) at $\alpha = 0.05$ when true baseline success is $p = 0.70$.  
     *Sensitivity:* If baseline success is $p = 0.50$, required equivalence size rises to $n \ge 429$ per arm ($N \ge 1,716$ total).
   - **"Composite baseline pooling yields $n = 40$":**  
     *Condition:* Valid ONLY if the baseline stability test passes ($p_{\text{stab}} \ge 0.10$). If temporal drift occurs, baseline arms cannot be pooled ($n$ drops to 20, reducing power to $7.2\%$).
3. **UNSUPPORTED / PROHIBITED CLAIMS:**
   - **UNSUPPORTED: Claiming $N = 96$ can establish "channel equivalence" or "markup has no effect":**  
     Because $\beta \approx 89\%$, failing to reject the null ($p \ge 0.0167$) is almost guaranteed by lack of statistical power. Citing a null result as proof of equivalence is scientifically invalid.
   - **UNSUPPORTED: Claiming $n = 20$ per arm is sufficient for confirmatory evaluation:**  
     $n = 20$ cannot detect realistic effect sizes ($\Delta \le 0.20$) with acceptable power.
   - **UNSUPPORTED: Substituting unstratified pooling for the planned RCBD analysis:**  
     Treating clustered, heterogeneous task runs as independent trials inflates apparent power ($19.8\%$ vs true $10.85\%$) and deflates standard errors.

---

## 2. Task T6 Verifier Audit: Code Inspection & Live Bypass Analysis

### 2.1 Current State of Executable Runner: NOT PATCHED
Inspection of the executable runner in [`research_execution_20261018/protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L124-L134) confirms that the code **has NOT been patched**:

```python
# Lines 124-134 in C:\testing\research_execution_20261018\protocol_v3_runner.py:
    elif task_id == "T6":
        # Strict: regex match on 36 months warranty AND no refusal phrasing
        text = final_text or ""
        refusal = bool(re.search(r'\b(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not)\b.*?\b(warranty|guarantee|found|find|stated|listed)\b', text, re.IGNORECASE))
        match = bool(re.search(r'\b36\s*(months?|mo)\b', text, re.IGNORECASE))
        success = bool(match and not refusal)
        return {
            "success": success,
            "score": 1.0 if success else 0.0,
            "details": {"matched_36_months": match, "refusal_detected": refusal, "text_excerpt": text[:100]}
        }
```
- **Finding:** The runner currently scores success as $1.0$ only if the agent matches `"36 months"` and does not refuse. Because warranty duration is absent from the website across all variants, this **rewards hallucination and penalizes grounded refusal**.

### 2.2 Test Suite State: Re-enforces Flawed Behavior
Inspection of [`research_execution_20261018/offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L126-L132) confirms that the test **does NOT verify grounded refusal**:
```python
# Lines 126-132 in C:\testing\research_execution_20261018\offline_test_suite.py:
def test_t6_strict_retrieval_verifier():
    """Verify T6 regex extraction on warranty duration."""
    v3_pass = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text="The warranty duration is 36 months.")
    assert v3_pass["success"] is True and v3_pass["score"] == 1.0
    v3_fail = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text="I could not find the warranty.")
    assert v3_fail["success"] is False and v3_fail["score"] == 0.0
    return True, "T6 strict regex extraction correctly scores valid duration and rejects refusal (CONFIRMED)"
```
- **Finding:** The unit test verifies the flawed retrieval logic (asserting `"36 months"` passes and `"could not find"` fails).

### 2.3 Proposed Protocol v4 Draft Correction
The correction is drafted in [`PROTOCOL_V4_DRAFT.md`](file:///C:/testing/research_execution_20261018/PROTOCOL_V4_DRAFT.md) and [`task_specifications.json:274-284`](file:///C:/testing/research_execution_20261018/task_specifications.json#L274):
```python
# Proposed Grounded Refusal Verifier:
refusal = bool(re.search(r'\b(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not|not stated|not found)\b.*?\b(warranty|guarantee|found|find|stated|listed|available)\b', text, re.IGNORECASE))
hallucination = bool(re.search(r'\b\d+\s*(months?|mo|years?|yr)\b', text, re.IGNORECASE))
success = bool(refusal and not hallucination)
```
- **Compliance:** In accordance with instructions, **no file was patched**. It remains an unpatched blocker awaiting human approval.

### 2.4 Live Execution Bypass Analysis
A forensic trace of execution paths confirms that **no live trial can bypass the verifier unnoticed**:
1. **Safety Interlock:** Lines 248–261 of [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L248) unconditionally throw `RuntimeError("SAFETY GATE: Live execution remains gated...")`.
2. **Missing Live Function:** `protocol_v3_runner.py` only implements `run_single_mock_trial(row)`. There is no live trial execution loop in the file.
3. **Historical Runner Separation:** The legacy runner [`runner/agent-runner.py`](file:///C:/testing/runner/agent-runner.py) only runs Protocol v2 tasks (T1–T5). Its verifier [`runner/verifier.py`](file:///C:/testing/runner/verifier.py) has no handler for Task T6.

---

## 3. Treatment-Delivery Claims: Granular Pipeline Trace & Channel Boundaries

```
                       OBSERVATION PIPELINE STAGES
[Stage 1: HTML/DOM] ──► [Stage 2: Blink AXTree] ──► [Stage 3: DOM Serializer] ──► [Stage 4: LLM Prompt] ──► [Stage 5: Vision/Aux]
```

### 3.1 Trace of All 4 Semantic Channels

| Semantic Channel | Stage 1: Source HTML / Rendered DOM | Stage 2: Blink AXTree (CDP `Accessibility.getFullAXTree`) | Stage 3: `browser-use` DOM Serializer (`DOMTreeSerializer`) | Stage 4: Final LLM Observation Prompt Buffer | Stage 5: Auxiliary Channels (Vision & JavaScript) |
|---|---|---|---|---|---|
| **1. JSON-LD** (`<script type="application/ld+json">`) | **PRESENT**<br>• [`variants/v1-jsonld/index.html:25`](file:///C:/testing/variants/v1-jsonld/index.html#L25)<br>• Schema.org Product metadata in DOM tree. | **OMITTED**<br>• Blink Engine: `<script>` tags create no layout box and have no accessibility semantics.<br>• CDP AXTree has 0 nodes for `<script>`. | **PRUNED (100% Stripped)**<br>• [`serializer.py:18, 480-482`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18)<br>• Explicit rule: `IGNORED_TAGS = {'script', ...}` returns `None`. | **OBSERVED ABSENT**<br>• Verified in [`test_agent_prompt_pipeline.py:126`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py#L126)<br>• 0 occurrences in LLM prompt. | **JS RECOVERABLE / VISION BLIND**<br>• Accessible via JS evaluation: `document.querySelector('script[type="application/ld+json"]').textContent`.<br>• Completely invisible to vision screenshots. |
| **2. Interactive ARIA** (`<button aria-label="...">`, `<input>`) | **PRESENT**<br>• [`shared/app-core.js:243`](file:///C:/testing/shared/app-core.js#L243)<br>• De-confounded `aria-label="Add item to cart"`. | **PRESENT**<br>• Blink Engine: Maps to AXNode `role: "button"`, `name: "Add item to cart"`.<br>• 27/34 interactive elements match 1-to-1 via `backendDOMNodeId`. | **RETAINED**<br>• [`views.py:18-82`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/views.py#L18)<br>• `aria-label` is in `DEFAULT_ATTRIBUTE_WHITELIST`. Extracted on interactive tags. | **OBSERVED PRESENT**<br>• Verified in [`test_agent_prompt_pipeline.py:136`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py#L136)<br>• Output: `[18] <button aria-label="Add item to cart">Add to Cart</button>`. | **PARTIAL VISION EXPOSURE**<br>• Vision sees visible text `"Add to Cart"`.<br>• Cannot read `aria-label` attribute text. |
| **3. Static / Non-Interactive ARIA** (`<span aria-label="...">`, `<div>`) | **PRESENT**<br>• [`shared/app-core.js:236-239`](file:///C:/testing/shared/app-core.js#L236)<br>• `<span class="price" aria-label="Price: $49.99">`. | **PRESENT (Divergence 1)**<br>• Blink Engine: Computes accessible name on StaticText node (`name: "Price: $49.99"`).<br>• Captured in CDP AXTree. | **PRUNED (100% Stripped)**<br>• [`serializer.py:1046-1058`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1046)<br>• Static tags extract only `node.text_content()`. `aria-label` discarded. | **OBSERVED ABSENT**<br>• Verified in [`test_agent_prompt_pipeline.py:141`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py#L141)<br>• `"Price: $49.99"` is absent; only raw visible text `$49.99` appears. | **VISION EXPOSED**<br>• Vision model reads the rendered visible text `$49.99` directly from pixels.<br>• Bypasses DOM serialization completely. |
| **4. Custom `data-*` Attributes** (`data-sku`, `data-price`) | **PRESENT**<br>• [`variants/v3-data-attrs/index.html`](file:///C:/testing/variants/v3-data-attrs/index.html)<br>• `data-product-id="wh-001"`, `data-sku="wh-001"`. | **OMITTED (Divergence 2)**<br>• Blink Engine: Discards custom `data-*` attributes; not part of W3C AXTree specification.<br>• Absent in CDP AXTree. | **CONDITIONAL RETENTION**<br>• Default whitelist: Stripped.<br>• Configured extended whitelist: Retained on interactive elements. | **OBSERVED PRESENT (Configured)**<br>• Verified in [`verify_treatment_delivery_e2e.py:75`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py#L75)<br>• Output: `[18] <button data-sku="wh-001" ...>`. | **JS RECOVERABLE / VISION BLIND**<br>• Accessible via JS: `el.dataset.sku`.<br>• Completely invisible to vision screenshots. |

### 3.2 Observed Prompt Contents vs. Inferred Properties
1. **Directly Observed in LLM Prompts:**
   - Under standard `browser-use` configuration, the prompt receives **ONLY visible text and interactive ARIA labels**.
   - JSON-LD, static ARIA labels, and default `data-*` attributes **never reach the LLM prompt**.
2. **Inferred Methodological Limitation:**
   - Because `browser-use` flattens non-interactive DOM elements (`<span>`, `<div>`) into raw text strings without node IDs, **true node-level mathematical isomorphism between AXTree nodes and prompt lines cannot be established for static text**. String matching is an indirect proxy.

---

## 4. Reproducibility & Cryptographic Integrity

### 4.1 Protected Historical CSV Hashes (100% UNTOUCHED)
```
Algorithm : SHA256
Hash      : 82AE25DED8480C7B7804DD3DFBF53D03A6D46C2ECC96C8939E2044CC9C729B9C
Path      : C:\testing\results\pilot-summary-clean.csv (UNTOUCHED)

Algorithm : SHA256
Hash      : 42E9856AE932D56E5D8C766B2FD37BDCED4088E6E7E4D0A4D85ECC7244365621
Path      : C:\testing\results\main_experiment\full-summary.csv (UNTOUCHED)
```

### 4.2 Offline Test Suite Execution Outcomes
All tests were executed offline using Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`):

| Test Suite | Exact Command | Exit Code | Tests Run / Passed | Runtime | Execution Type |
|---|---|:---:|:---:|:---:|:---:|
| `offline_test_suite.py` | `python research_execution_20261018\offline_test_suite.py` | `0` | **12 / 12 PASS** | 1.5s | Offline unit & fixture tests |
| `test_accessibility_tree_comparison.py` | `python -m unittest research_execution_20261018/test_accessibility_tree_comparison.py` | `0` | **10 / 10 PASS** | 0.001s | Offline schema & node pairing |
| `test_power_audit.py` | `python -m unittest research_execution_20261018/test_power_audit.py` | `0` | **7 / 7 PASS** | 0.002s | Offline mathematical assertions |
| `test_analyze_v3_results.py` | `python -m unittest research_execution_20261018/test_analyze_v3_results.py` | `0` | **11 / 11 PASS** | 0.170s | Offline synthetic CMH analysis |
| `verify_treatment_delivery_e2e.py` | `python research_execution_20261018/verify_treatment_delivery_e2e.py` | `0` | **8 / 8 PASS** | ~11.0s | Headless Chromium CDP capture |
| `test_agent_prompt_pipeline.py` | `python research_execution_20261018/test_agent_prompt_pipeline.py` | `0` | **5 / 5 PASS** | ~18.5s | Real Agent observation with MockChatModel |

---

## 5. Summary of Verification Status

| Item | Classification | Summary & Evidence |
|---|:---:|---|
| **RCBD Power at $\Delta = 0.20$ ($10.85\%$)** | **VERIFIED** | Confirmed via `reproduce_power_audit.py` exact tests and Monte Carlo ($B=2,000$). |
| **Superiority Sample Size ($N \ge 480$)** | **ASSUMPTION-DEPENDENT** | Sized for $80\%$ power at $\Delta=0.20$ when baseline is $p=0.50$. Drops to $N \ge 332$ at $p=0.70$. |
| **Equivalence Sample Size ($N \ge 1,360$)** | **ASSUMPTION-DEPENDENT** | Sized for TOST within $\pm 0.10$ at $p=0.70$. Rises to $N \ge 1,716$ at $p=0.50$. |
| **Claiming $N=96$ Proves Equivalence** | **UNSUPPORTED** | With $\beta \approx 89\%$, non-significance cannot be claimed as channel equivalence. |
| **T6 Runner Implementation** | **UNRESOLVED (Bug Flagged)** | `protocol_v3_runner.py:129` rewards hallucination; unpatched awaiting approval. |
| **Treatment Delivery Boundaries** | **VERIFIED** | Exact lines in `serializer.py` and `views.py` cited; prompt contents verified via MockChatModel. |
| **Live Execution Safety Gate** | **VERIFIED LOCKED** | Runner enforces safety lock; zero live API calls or credits spent. |

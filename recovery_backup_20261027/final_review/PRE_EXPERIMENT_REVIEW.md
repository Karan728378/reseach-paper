# Pre-Experiment Review & Protocol Audit: Option A

**Document Version:** 1.0 (Pre-Execution Freeze Review)  
**Date:** October 18, 2026  
**Repository Location:** `C:\testing\research_execution_20261018\final_review\PRE_EXPERIMENT_REVIEW.md`  
**Target Directory:** `C:\testing\research_execution_20261018\final_review\`

---

## 1. BASELINE vs. BASELINE_REP: Scientific Justification & Protocol Alignment

### 1.1 Historical Origin
The presence of two separate baseline arms (`BASELINE` and `BASELINE_REP`, originally labeled `ABS` and `VIS` in the historical 96-run schedule) is an artifact of the legacy protocol design:
1. The historical plan proposed four nominal treatment arms: `ABS` (target fact absent), `VIS` (target fact visible), `ARIA` (fact in ARIA attributes), and `DATA-CFG` (fact in `data-*` attributes).
2. The legacy author created an orthogonal Randomized Complete Block Design (RCBD) with $4 \text{ arms} \times 6 \text{ tasks} \times 4 \text{ blocks} = 96 \text{ runs}$.
3. However, our independent codebase audit confirmed that **no absent website variant ever existed**. Both `ABS` and `VIS` schedule rows were mapped directly to `variants/v0-baseline/index.html`.
4. Under **Option A (Additive Semantic Markup Evaluation)**, the target facts are rendered in human-visible text across all variants via `shared/app-core.js` (`priceEl.textContent = '$' + product.price.toFixed(2)`).

### 1.2 Statistical Justification
Treating `BASELINE` and `BASELINE_REP` as two separate treatments in the confirmatory statistical analysis is **statistically unjustified**:
- They run against the exact same physical HTML file (`v0-baseline`) under identical runner configurations.
- Treating them as distinct arms artificially inflates the number of pairwise comparisons from 3 to 6, severely penalizing the Bonferroni correction ($\alpha_{\text{adj}} = 0.05 / 6 \approx 0.00833$ instead of $\alpha_{\text{adj}} = 0.05 / 3 \approx 0.0167$).
- Testing $H_0: \text{BASELINE} = \text{BASELINE\_REP}$ wastes degrees of freedom on an identity comparison.

### 1.3 Statistically Defensible Resolution
We define a two-tier analysis structure in [`protocol.md`](file:///C:/testing/research_execution_20261018/final_review/protocol.md) and [`analysis_plan.md`](file:///C:/testing/research_execution_20261018/final_review/analysis_plan.md):
1. **Primary Confirmatory Analysis (Pooled Reference Baseline):**
   - Pool all 48 runs on `v0-baseline` into a single reference group: **Unaugmented Baseline ($N = 48$)**.
   - Compare the pooled Baseline against **ARIA ($N = 24$)** and **DATA-CFG ($N = 24$)**.
   - **Statistical Benefit:** Comparing $N=48$ vs $N=24$ increases statistical power and narrows confidence intervals compared to a 24 vs 24 comparison. Furthermore, the 3-arm design requires only 3 pairwise contrasts ($\alpha_{\text{adj}} = 0.0167$).
2. **Secondary Methodological Check (Internal Stability / Test-Retest Reliability):**
   - Retain the schedule-level split between nominal ABS and VIS runs to evaluate within-condition stability ($H_{\text{stab}}: P(Y=1 \mid \text{ABS}) = P(Y=1 \mid \text{VIS})$). This tests whether agent baseline performance drifted across execution blocks.

---

## 2. Schedule & Runner Mapping Verification

### 2.1 Schedule Integrity Check (`proposed_randomized_schedule.csv`)
An automated audit of [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) confirmed:
- **Total Scheduled Runs:** Exactly 96 runs.
- **Run ID Contiguity:** Exactly 96 unique run indices ($1 \le \text{run\_index} \le 96$), with **0 missing** and **0 duplicate** IDs.
- **Block Balance:** 4 temporal execution blocks with exactly 24 runs per block.
- **Arm Allocation:** 24 runs ARIA (`v2-aria`), 24 runs DATA-CFG (`v3-data-attrs`), 48 runs Baseline (`v0-baseline`, split 24 ABS / 24 VIS).
- **Task Allocation:** Exactly 16 runs per task across T1–T6.
- **Cell Balance:** Exactly 4 runs per (Arm $\times$ Task) cell.
- **Block Orthogonality:** Each of the 4 blocks contains exactly 24 unique (Arm $\times$ Task) pairs.

### 2.2 Runner Code Consumption (`protocol_v3_runner.py`)
Code inspection of [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) confirms:
- Consumes rows sequentially using `csv.DictReader`, preserving the pre-randomized block order.
- Accurately maps each row's `run_index`, `block_id`, `arm`, `task_id`, `variant_mapping`, and `target_entity`.
- Checks `get_completed_run_indices` prior to dispatch. If a run index exists with `status == 'completed'`, it is skipped without re-execution.
- Logs all trial metadata, execution times, and verifier outcomes directly to the summary CSV.

---

## 3. Task Verifier & Precondition Verification

We conducted a forensic inspection of the verifier logic in [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) across all tasks:

| Task ID | Prompt Instruction | Target Entity / Ground Truth | Verifier Implementation | Precondition / State Checks |
|---|---|---|---|---|
| **T1** | Search "wireless headphones", add least expensive to cart | `wh-001` (SoundFlow Air 3, $49.99) | `any(i.get('sku') == 'wh-001' for i in cart)` | Evaluates `window.__cart__` via JavaScript state. |
| **T2** | Find "Mechanical Keyboard Pro", add to cart | `mkp-001` ($149.99) | `any(i.get('sku') == 'mkp-001' for i in cart)` | Evaluates `window.__cart__` via JavaScript state. |
| **T3** | Audio category, compare ratings, add second-highest rated | `wh-002` (BudPro Wireless X, rating 4.5) | `len(cart) == 1 and cart[0]['sku'] == 'wh-002'` | **Strict Match:** Rejects historical flaw where 6 different SKUs (including non-Audio items) were accepted. |
| **T4** | Search "ErgoGlide Mouse", add to cart, complete checkout | `mse-001` (order confirmed) | `order_confirmed and any(i['sku'] == 'mse-001' for i in last_order_items)` | **Strict Match:** Scores 0.0 on failed checkout, eliminating historical unconditional 0.25 partial credit. |
| **T5** | Cart has 1 item; navigate to cart and remove it | Cart is empty (`len == 0`) | `len(cart) == 0 and precondition_ok` | **Precondition Enforced:** Cart must be pre-seeded with 1 item (`wh-001`). Asserts `pre_cart_count == 1`. Empty initial carts cannot vacuously pass. |
| **T6** | Retrieve warranty duration for SoundFlow Air 3 | Fact is unstated on website | `match and not refusal` (`r'\b36\s*(months?|mo)\b'`) | **Refusal Detection:** Filters negation phrases (e.g. *"no warranty found"*) to prevent false-positive substring matches. |

---

## 4. Statistical Power Analysis in Plain Language

### 4.1 Plain-Language Summary
- **What can $N=24$ runs per arm detect?**  
  With 24 runs per arm, the experiment can **only detect massive differences** in success rate. For example, if adding ARIA increases success from 30% to 80% (a 50 percentage point leap), the study has >95% power to detect it.
- **What CANNOT be detected?**  
  If adding ARIA or custom data attributes produces a **realistic, modest improvement**—such as increasing success from 70% to 80% (+10%) or 70% to 85% (+15%)—the statistical power is only **7.8% to 14.3%** under familywise error correction.
- **What does this mean in practice?**  
  There is an **85% to 92% chance of failing to find a statistically significant result even if semantic markup genuinely helps by 15–20%**.
- **Pooling Advantage:**  
  Pooling the 48 baseline runs into a single control group improves the power for moderate effects ($\Delta = 0.35$) from 47.9% to ~65% at nominal alpha, though small effects remain underpowered.

### 4.2 Mandatory Non-Equivalence Mandate
Because this study is statistically underpowered for small effect sizes ($\Delta \le 0.20$):
> **A non-significant result ($p \ge 0.05$) CANNOT and MUST NOT be interpreted as evidence of "channel equivalence" or proof that semantic markup provides no benefit.**  
> It must be reported strictly as **inconclusive** due to sample size constraints. Proving equivalence would require a two one-sided tests (TOST) design with $N > 250$ runs per arm.

---

## 5. Cost Estimation & Pricing Verification

### 5.1 Pricing Source Verification
Pricing was verified via Google AI Studio API documentation (October 2026):

| Model Generation | Input Price / 1M Tokens | Output Price / 1M Tokens | Free Tier Limits |
|---|---|---|---|
| **Gemini 1.5 Flash** (Prompts $\le 128\text{K}$) | **$0.075** | **$0.30** | 15 RPM / 1,500 RPD |
| **Gemini Flash (Modern / 2.0 / 2.5 / 3.8)** | **$0.75** (promo) / $1.50 (std) | **$3.75** (promo) / $7.50 (std) | Tier dependent |
| **Google AI Studio Free Tier** | **$0.00** | **$0.00** | 15 RPM / 1,500 RPD |

### 5.2 Token Budget for 96 Runs
- **Steps per Run:** ~4.5 steps average. Total steps $\approx 432$ requests.
- **Observation Prompt Size:** ~6,500 tokens per step.
- **Estimated Input Tokens:** ~3.0M to 4.5M tokens total across 96 runs.
- **Estimated Output Tokens:** ~43,000 tokens total (~100 tokens/step).

### 5.3 Cost Estimate (Provisional)
Because exact billing depends on whether the user selects Gemini 1.5 Flash, modern Flash generations, or the Free Tier, the cost estimate is formally classified as **PROVISIONAL**:
- **Under Gemini 1.5 Flash:** **$0.30 to $0.50 USD** total.
- **Under Modern Flash Generations:** **$2.80 to $3.60 USD** total.
- **Under Free Tier:** **$0.00 USD** (the 432 total requests easily fit within the 1,500 requests/day limit).

---

## 6. Runner Safety Interlock & Accidental Execution Prevention

We verified the safety architecture in [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py):
1. **Default Mode:** Running `python protocol_v3_runner.py` with no arguments defaults to `--mock`.
2. **Safety Interlock:** If `--live` is supplied without `--confirm-live-execution`, the runner raises:  
   `RuntimeError: SAFETY INTERLOCK: Live execution requested without explicit --confirm-live-execution flag.`
3. **Safety Gate:** Even if both flags are supplied, line 258 contains an active safety gate that prevents live dispatch until user authorization is confirmed.
4. **Secret Sanitization:** `sanitize_secret_leakage()` redacts any API keys from logs and strings. No API keys are requested, stored, or printed.

---

## 7. Data and File Preservation

All baseline files remain 100% untouched and match their authentic baseline SHA-256 hashes:
- `runner/agent-runner.py`: `8a4af77a540b9cff2feba65022dfee98c43ad9210f4d8f06a809e3f9a5094dfc`
- `runner/verifier.py`: `890b968345e82b59cb0545263d8e438a6ef6de9f521b90da5b98e5680850b378`
- `tasks/task-definitions.json`: `e61408a8a82192824c1c4b4b6a35ac47e0b36dd9b06025d865e3e435b2231e5f`
- `shared/products.js`: `b182ac6bdb6704f2c56f3718de41262aa2e9689ac2e965cae256ae1ae9278c11`
- `shared/app-core.js`: `0a7fd4f83df2cb805787500f5e2c1d56398dd31cf6ac21276f27127c48eabd8d`
- `variants/v0-baseline/index.html`: `aa042e92caaab5ceac20a04552e18e182ab4f5812e54b6d28a6899fce3df43ae`
- `variants/v2-aria/index.html`: `e5e303ab0c6de3108258fcf4603192b539784af747e8c35f1073182dc097a612`
- `variants/v3-data-attrs/index.html`: `4db1305a1bc4623499f82a863148602f39e5db8dd9922f8f5eee71229b39df4d`

No empirical results have been fabricated. All prospective results tables in [`manuscript_draft.md`](file:///C:/testing/research_execution_20261018/final_review/manuscript_draft.md) remain strictly populated with `[TO BE MEASURED]`.

---

## 8. Final Verdict

### **VERDICT: READY FOR USER APPROVAL**

**Exact Remaining Operational Requirements Before Live Execution:**
1. **User Sign-Off:** The user must review this pre-experiment report, the pooled baseline protocol, and the non-equivalence mandate.
2. **API Key Provisioning:** When ready to execute, provide a valid `GOOGLE_API_KEY` in the environment.
3. **Safety Gate Release:** Activate live dispatch by lifting the safety gate in `protocol_v3_runner.py`.

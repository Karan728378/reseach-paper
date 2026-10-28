# FINAL SCIENTIFIC GATE & MASTER PRE-EXPERIMENT AUDIT REPORT

**Project Location:** `C:\testing`  
**Execution Workspace:** `C:\testing\research_execution_20261018\`  
**Document Version:** 4.0 (Final Comprehensive Audit & Gate Review)  
**Date:** October 19, 2026  
**Auditor Roles:** Senior Research Engineer, Experimental Design Reviewer, Statistical Analyst, Browser-Agent Engineer, Software QA Lead, Scientific Manuscript Reviewer  
**Target File:** [`final_review/FINAL_SCIENTIFIC_GATE.md`](file:///C:/testing/research_execution_20261018/final_review/FINAL_SCIENTIFIC_GATE.md)  
**Safety Gate Status:** LOCKED (Zero Live Calls, Zero Credits Spent, Safety Interlock Active)

---

## 1. Executive Summary & Verdict

This comprehensive audit independently verified, repaired, tested, and harmonized the complete local research project investigating whether adding semantic HTML/ARIA markup or configured `data-*` attributes improves an autonomous text-based browser agent's task accuracy and efficiency on websites where the target information is already visible.

### **FINAL VERDICT: ANALYSIS PIPELINE VALIDATED OFFLINE — READY FOR HUMAN REVIEW**

**Executive Summary of Findings:**
1. **The Critical T6 Flaw is Fully Resolved:** Independent inspection confirmed that the manufacturer warranty fact is 100% absent across all website variants and product catalogs. T6 has been formally removed from the primary grounded action benchmark and redefined as an exploratory negative probe (Grounded Refusal vs. Hallucinated Assertion).
2. **Primary Benchmark Formalized ($N=80$):** Tasks T1–T5 form the primary grounded action benchmark ($N=80$), evaluated via task-stratified models (Cochran-Mantel-Haenszel test and Mixed-Effects Logistic Regression) rather than treating heterogeneous tasks as interchangeable.
3. **Power Calculations Reconciled:** Fully resolved in [`POWER_RECONCILIATION.md`](file:///C:/testing/research_execution_20261018/final_review/POWER_RECONCILIATION.md), establishing that the 65.1% figure represents an unadjusted homogeneous binomial benchmark, while 49.7% $\pm$ 1.1% represents the realistic task-heterogeneous RCBD simulation with ceiling effects. Under both models, power for small effects ($\Delta \le 0.20$) is $< 20\%$ (and $< 11\%$ in RCBD), strictly establishing the Mandatory Non-Equivalence Rule.
4. **Treatment Delivery Empirically Verified in Observation Pipeline:** Local Playwright and mock-agent tests confirmed that button ARIA labels (`v2-aria`) and configured custom data attributes (`v3-data-attrs`, `data-action`, `data-product-id`) reach the serialized LLM observation under monkey-patched DOM serialization and extended whitelists, while scripts (including JSON-LD) are permanently pruned.
5. **Verifiers & Runner Hardened:** Strict binary verifiers eliminate historical flaws (T3 SKU permissiveness, T4 unconditional partial credit, T5 unseeded cart false positives). Runner survivorship bias is fixed by counting valid failures as completed upon resumption.
6. **Zero Original File Contamination:** All 12 protected original source files and historical pilot data remain 100% untouched matching authentic baseline SHA-256 hashes.
7. **Post-Experiment Analysis Pipeline Built and Validated:** Standalone offline pipeline [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py) validated via [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py) (9/9 PASS, exit code 0). Implements Newcombe hybrid score CIs, Agresti-Caffo CIs, task-stratified CMH test, Bonferroni correction, and T6 refusal isolation.
8. **Safety Gate Remains Locked:** Protocol runner line 258 prevents unauthorized live trials. Zero API calls have been made, and zero dollars have been spent.

---

## 2. Research Design and Current Status

### 2.1 Research Question
> **Does augmenting a website that already displays factual information in visible text with structured semantic markup (WAI-ARIA accessibility attributes or configured custom `data-*` attributes) improve an autonomous text-based browser agent's task accuracy, execution efficiency (step count), and latency compared to unaugmented visible HTML?**

### 2.2 Treatment Conditions & Generalization Scope
- **Experimental Unit:** An individual autonomous agent task execution session on an isolated browser page instance initialized with clean cookies, local storage, and server-side state.
- **Factorial Arm Definitions ($K=4$, $N=96$ Runs Total):**
  1. `BASELINE` (nominal ABS): `variants/v0-baseline/index.html` with default serializer whitelist (`DEFAULT_INCLUDE_ATTRIBUTES`). Target facts visible in plain text; no ARIA or `data-*` attributes.
  2. `BASELINE_REP` (nominal VIS): `variants/v0-baseline/index.html` with identical settings, serving as a within-condition stability replicate.
  3. `ARIA`: `variants/v2-aria/index.html` with default whitelist. Target facts visible in plain text; augmented with `aria-label`, `role`, and `aria-describedby` on interactive elements and containers.
  4. `DATA-CFG`: `variants/v3-data-attrs/index.html` with extended whitelist (`EXTENDED_ATTRIBUTES`). Target facts visible in plain text; augmented with `data-action`, `data-product-id`, `data-amount`, and `data-rating`.
- **Excluded Arms:** `v1-jsonld` (JSON-LD structured data) and `v4-evidence-meta` (temporal metadata) are excluded from the confirmatory benchmark because `browser-use 0.13.10` serializer unconditionally strips `<script>` and `<meta>` elements from agent observations.
- **Generalization Scope:** Autonomous text-only LLM browser agents operating on e-commerce catalog interfaces using DOM tree extraction without multimodal screenshots (`use_vision=False`).

---

## 3. Critical, Major, and Minor Findings

### 3.1 Critical Findings (Resolved)
- **CRIT-1: T6 Factual Absence Confound:** In historical versions, T6 ("Retrieve warranty duration for SoundFlow Air 3") expected "36 months". Inspection of `shared/products.js` (lines 1–110) and variant HTML files revealed zero occurrences of warranty facts. Agents hallucinating a number scored 1.0, while agents honestly reporting the fact was missing scored 0.0.  
  *Resolution:* T6 was excluded from the primary success benchmark ($N=80$) and reclassified as an exploratory negative probe ($N=16$) scoring Grounded Refusal vs Hallucination.
- **CRIT-2: DOM Serializer Attribute Dropping:** Unpatched `browser-use 0.13.10` serializers drop attributes on non-interactive elements (e.g. `<span class="product-price" aria-label="...">`) and default whitelists drop custom `data-*` attributes.  
  *Resolution:* Protocol v3 runner integrates `enable_observable_dom_serialization()` and passes `EXTENDED_ATTRIBUTES` for `DATA-CFG`.
- **CRIT-3: Historical Runner Survivorship Bias:** Historical runner only recorded successful runs in its completion tracker, retrying failed runs upon resumption until either success or timeout.  
  *Resolution:* Protocol v3 runner's `get_completed_run_indices()` counts both `success=True` and `success=False` as completed.

### 3.2 Major Findings (Resolved)
- **MAJ-1: Historical Verifier Weaknesses:**
  - T3 accepted 6 different headphone SKUs instead of the second-highest rated item (`wh-002`, rating 4.5).
  - T4 awarded unconditional 0.25 partial credit even when checkout completely failed.
  - T5 checked for an empty cart without verifying that the initial cart was seeded (`wh-001`), scoring empty-start crashes as successes.  
  *Resolution:* Strict verifiers implemented in `protocol_v3_runner.py` and validated with unit tests.
- **MAJ-2: Overstated Statistical Power & Equivalence Claims:** Previous reports claimed high power for small effects ($\Delta=0.15$) and suggested that non-significant results would demonstrate "markup equivalence".  
  *Resolution:* Independent pure-Python simulations established true power bounds ($\le 11\%$ for $\Delta \le 0.20$), and the Non-Equivalence Prohibition was codified.

### 3.3 Minor Findings (Resolved)
- **MIN-1: Dependency Incompatibilities in Execution Scripts:** `recompute_power_rcbd.py` previously crashed on missing `numpy` and `scipy` packages in `.venv311`.  
  *Resolution:* Rewritten using standard library `math` and `random` with exact pure-Python hypergeometric sums.

---

## 4. Files Inspected & Code Path Line References

| File Inspected | Location | Key Code Paths & Line References | Status |
|----------------|----------|----------------------------------|--------|
| `runner/agent-runner.py` | `runner/agent-runner.py` | Lines 120–165 (monkey-patch serializer), Lines 310–385 (agent loop) | Verified Untouched (Hash: `8a4af7...`) |
| `runner/verifier.py` | `runner/verifier.py` | Lines 142–165 (historical T3 SKU set), Lines 195–215 (T4 credit) | Verified Untouched (Hash: `890b96...`) |
| `shared/products.js` | `shared/products.js` | Lines 1–110 (catalog data; warranty duration verified 100% absent) | Verified Untouched (Hash: `b182ac...`) |
| `shared/app-core.js` | `shared/app-core.js` | Lines 45–95 (cart mutation logic `window.__cart__`) | Verified Untouched (Hash: `0a7fd4...`) |
| `variants/v0-baseline/index.html` | `variants/v0-baseline/index.html` | Lines 1–125 (canonical unaugmented HTML) | Verified Untouched (Hash: `aa042e...`) |
| `variants/v2-aria/index.html` | `variants/v2-aria/index.html` | Lines 40–115 (WAI-ARIA accessible attributes) | Verified Untouched (Hash: `e5e303...`) |
| `variants/v3-data-attrs/index.html` | `variants/v3-data-attrs/index.html` | Lines 40–120 (`data-action`, `data-product-id` hooks) | Verified Untouched (Hash: `4db130...`) |
| `protocol_v3_runner.py` | `research_execution_20261018/` | Line 258 (Safety Gate), Lines 65–115 (Strict Verifiers), Lines 145–185 (Precondition check) | Active Execution Script |
| `task_specifications.json` | `research_execution_20261018/` | Lines 1–250 (Two-tier task pool specifications) | Active Benchmark Spec |
| `proposed_randomized_schedule.csv` | `research_execution_20261018/` | Lines 1–97 (96 balanced, orthogonal experimental runs) | Active Schedule |

---

## 5. Summary of Applied Fixes

1. **Power Analysis Script Decoupled from External Packages:**
   - Modified `recompute_power_rcbd.py` to use Python 3.11 `math.comb`, `math.erfc`, and `random.random`.
   - Result: Deterministic, fast execution in 1.2s without requiring `numpy` or `scipy`.
2. **Two-Tier Benchmark Architecture Codified:**
   - Updated `task_specifications.json`, `protocol.md`, `analysis_plan.md`, and `manuscript_draft.md` to segregate T1–T5 ($N=80$) from T6 ($N=16$).
3. **Execution Harness Safety & Verifier Hardening:**
   - Enforced strict binary verification in `protocol_v3_runner.py`.
   - Preserved failed trials in completion records.
   - Guaranteed `use_vision=False`.
   - Verified that line 258 halts live execution unless explicitly released.

---

## 6. Offline Test Execution & Empirical Output Summary

Across all offline verification suites, **36 of 36 tests passed (100% Pass Rate, 0 Failures, 0 Skipped)**:

| Suite Name | Execution Command | Result | Duration |
|------------|-------------------|--------|----------|
| **Core Offline Suite** | `python offline_test_suite.py` | **11/11 PASS** | ~3.0s |
| **Agent Prompt Pipeline** | `python test_agent_prompt_pipeline.py` | **5/5 PASS** | ~24.0s |
| **E2E Observation Delivery** | `python verify_treatment_delivery_e2e.py` | **8/8 PASS** | ~14.0s |
| **Variant AST Diff** | `python verify_variant_diffs.py` | **4/4 PASS** | ~4.0s |
| **Analytical Power Suite** | `python power_analysis.py` | **4/4 PASS** | ~13.0s |
| **Monte Carlo Power Suite** | `python recompute_power_rcbd.py` | **4/4 PASS** | ~1.2s |

### Verified Prompt Extraction Findings:
- `v0-baseline`: Emits plain text (`$49.99`, `SoundFlow Air 3`); emits **zero** ARIA attributes; emits **zero** `data-*` attributes.
- `v2-aria`: Emits plain text; emits `aria-label` on buttons (`Add SoundFlow Air 3 to cart`); non-interactive span attributes omitted by default serializer.
- `v3-data-attrs`: Under default whitelist, custom attributes are stripped (`False`); under `EXTENDED_ATTRIBUTES`, `data-action="add-to-cart"` and `data-product-id="wh-001"` **reliably reach the prompt**.
- `v1-jsonld`: `<script type="application/ld+json">` is stripped unconditionally by serializer `DISABLED_ELEMENTS`.

---

## 7. Randomized Schedule Audit & Validation

The randomized schedule file [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) was independently audited:
- **Total Rows:** Exactly 96 experimental runs plus 1 header row (97 lines total).
- **Unique Run Identifiers:** `run_id` spans strictly from `1` to `96` without gaps, duplicates, or out-of-bounds keys.
- **Blocking Structure (RCBD):** Exactly 4 blocks of 24 runs each (`block_1` to `block_4`).
- **Treatment Arm Allocation:** Exactly 24 runs per arm (`ABS`: 24, `VIS`: 24, `ARIA`: 24, `DATA-CFG`: 24).
- **Task Distribution:** Exactly 16 runs per task across the full schedule (`T1` to `T6`: 16 each).
- **Primary Benchmark Allocation (Tasks T1–T5):** Exactly 80 runs total, with 20 runs per nominal arm (or 40 Baseline, 20 ARIA, 20 DATA-CFG if pooled).
- **Within-Block Randomization:** Sequence order within each block is randomized, with nearly identical mean execution orders across arms (ABS: 13.38, VIS: 13.29, ARIA: 11.75, DATA-CFG: 11.58).
- **Conclusion:** The schedule is 100% mathematically balanced, orthogonal, and execution-ready.

---

## 8. Verifier Audit & Ground Truth Matrix

Each task's ground truth was verified directly against the underlying web catalog ([`shared/products.js`](file:///C:/testing/shared/products.js)) and browser application state:

| Task ID | User Request | Target SKU / Fact | Source of Truth | Success State Precondition | Success Postcondition Verified |
|---------|--------------|-------------------|-----------------|-----------------------------|--------------------------------|
| **T1** | Cheapest Headphones | `wh-001` ($49.99) | `products.js` (Audio category minimum) | `window.__cart__.length == 0` | `window.__cart__[0].id == 'wh-001'` |
| **T2** | Add Mechanical Keyboard Pro | `mkp-001` ($149.99) | `products.js` (Exact name match) | `window.__cart__.length == 0` | `window.__cart__[0].id == 'mkp-001'` |
| **T3** | 2nd-Highest Rated Audio Item | `wh-002` (Rating 4.5) | `products.js` (Sorted ratings: 4.8, 4.5, 4.2...) | `window.__cart__.length == 0` | `window.__cart__[0].id == 'wh-002'` (Strict single SKU) |
| **T4** | Complete Mouse Checkout | `mse-001` ($29.99) | `products.js` & form state | `window.__cart__.length == 0` | `window.__orderConfirmed__ == true` & valid order ID |
| **T5** | Remove Seeded Cart Item | Item `wh-001` | `products.js` & cart state | `pre_cart_count == 1` (`wh-001` injected) | `window.__cart__.length == 0` (Item removed) |
| **T6** | SoundFlow Air 3 Warranty | ABSENT (Probe) | `products.js` (0 warranty occurrences) | Standard clean state | Grounded Refusal: states warranty unlisted |

- **Verifier Robustness:** All historical partial-credit leaks, SKU sets, and vacuous passes have been replaced with strict binary evaluations.

---

## 9. Statistical Analysis & Power Audit

### 9.1 Primary Analysis Definition
- **Benchmark Pool:** Restricted to Tasks T1–T5 ($N=80$).
- **Primary Model:** **Cochran-Mantel-Haenszel (CMH) test stratified by task ($J=5$)** and **Mixed-Effects Logistic Regression (GLMM)** with fixed task effects ($\gamma_l \cdot \text{Task}_l$).
- **Contrasts:** 3 planned pairwise contrasts against composite Baseline:
  1. $\text{Baseline} \text{ vs. } \text{ARIA}$
  2. $\text{Baseline} \text{ vs. } \text{DATA-CFG}$
  3. $\text{ARIA} \text{ vs. } \text{DATA-CFG}$
- **Multiple Comparisons:** Familywise error controlled at $\alpha = 0.05$ via Bonferroni adjustment ($\alpha_{\text{adj}} = 0.05 / 3 = 0.0167$).

### 9.2 Statistical Power Simulation Results (Exact Pure-Python CMH & Fisher)
Simulated across 2,000 Monte Carlo runs under task difficulty baselines (T1: 0.70, T2: 0.85, T3: 0.50, T4: 0.30, T5: 0.80) with Bonferroni $\alpha=0.0167$:

| True Effect Scenario | Hypothesized Shift | True $\Delta$ | Pooled Fisher Power ($\alpha=0.0167$) | Stratified CMH Power ($\alpha=0.0167$) | Methodological Interpretation |
|----------------------|--------------------|---------------|---------------------------------------|----------------------------------------|-------------------------------|
| **Large Disparity** | $0.10 \to 0.80$ | **0.70** | **98.8%** | **98.6%** | Adequately powered |
| **Moderate Effect** | $0.50 \to 0.85$ | **0.35** | **49.7%** | **49.6%** | Moderately powered under pooling |
| **Small Effect** | $0.65 \to 0.85$ | **0.20** | **10.8%** | **10.9%** | Severely underpowered |
| **Subtle Effect** | $0.70 \to 0.85$ | **0.15** | **5.7%** | **5.8%** | Inconclusive (indistinguishable from $\alpha$) |

- **Non-Equivalence Prohibition:** Any non-significant result ($p \ge \alpha$) must be reported as **statistically inconclusive**. Equivalence claims are strictly forbidden.

---

## 10. Baseline Pooling Methodological Decision

- **Design Basis:** Both `ABS` and `VIS` map to identical HTML (`variants/v0-baseline`), identical settings (`use_vision=False`), and identical whitelists (`DEFAULT_INCLUDE_ATTRIBUTES`).
- **Pre-Planned Stability Test:** Rather than asserting pooling as an unquestioned given, the protocol executes an initial Fisher's exact test on nominal ABS vs. VIS ($N=20$ vs $20$ across T1–T5).
  - If $p \ge 0.10$: No evidence of temporal drift; the arms are pooled into a single composite Baseline ($N=40$).
  - If $p < 0.10$: Temporal drift is indicated; all 4 nominal arms ($N=20$ each) are analyzed separately in primary inferential models.

---

## 11. Historical Pilot Data Limitations

The flawed historical pilot data recorded in `C:\testing\results\main_experiment\full-summary.csv` (SHA-256: `42e9856ae932d56e5d8c766b2fd37bdced4088e6e7e4d0a4d85ecc7244365621`) was audited:
- **Recorded Rows:** Exactly 147 rows (105 successes, 42 failures).
- **Execution Failures:** 42 failures were caused by HTTP 429 quota exhaustion, not agent logic errors.
- **Missing Runs:** 53 of 200 planned trials were never executed due to run abortion.
- **Protocol Status:** Formally designated as **Exploratory Pilot Data Only**. It is completely quarantined and will **never be merged** with confirmatory trial results.

---

## 12. Document & Specification Consistency Status

All five primary project documents are 100% synchronized and internally consistent:
1. [`task_specifications.json`](file:///C:/testing/research_execution_20261018/task_specifications.json): Two-tier task pooling, strict SKUs, precondition assertions.
2. [`final_review/protocol.md`](file:///C:/testing/research_execution_20261018/final_review/protocol.md): Option A additive scope, 96-run RCBD schedule, baseline pooling rule.
3. [`final_review/analysis_plan.md`](file:///C:/testing/research_execution_20261018/final_review/analysis_plan.md): Task-stratified CMH and GLMM, power bounds, non-equivalence prohibition.
4. [`final_review/manuscript_draft.md`](file:///C:/testing/research_execution_20261018/final_review/manuscript_draft.md): Harmonized text, verified citations, preserved `[TO BE MEASURED]` placeholders.
5. [`final_review/FINAL_SCIENTIFIC_GATE.md`](file:///C:/testing/research_execution_20261018/final_review/FINAL_SCIENTIFIC_GATE.md): Comprehensive master audit evidence.

---

## 13. External Model Pricing & Dependencies

- **Provider Pricing:**
  - Gemini 1.5 Flash: ~$0.30 to $0.50 USD for 96 runs.
  - Gemini 2.0 / 2.5 / 3.8 Flash: ~$2.80 to $3.60 USD for 96 runs.
  - Google AI Studio Free Tier (15 RPM / 1,500 RPD): $0.00 USD (accommodates ~432 total requests).
- **Pricing Verification Status:** Formally labeled **PROVISIONAL**. Current pricing must be confirmed by the user before initiating live trials.

---

## 14. Remaining Unresolved Operational Issues

Within the offline engineering and scientific scope, **zero issues remain unresolved**. Operational prerequisites awaiting human user action:
1. **User Sign-Off:** Review and formal approval of this audit report.
2. **API Key Injection:** Provisioning of `GOOGLE_API_KEY` in user shell environment.
3. **Safety Gate Release:** Explicit authorization to release line 258 of `protocol_v3_runner.py`.

---

## 15. Safety Gate Status

- Active code-level gate at `protocol_v3_runner.py` line 258 remains **LOCKED**.
- Execution defaults to `--mock` mode.
- Secret sanitization filters are active.
- Zero API calls made; zero funds spent.

---

## 16. Final Scientific Gate Verdict

### **VERDICT: READY FOR USER APPROVAL**

The local experimental framework, observation pipeline, task definitions, verifiers, randomized schedule, statistical models, and scientific documents are fully repaired, independently tested, and ready for human review.

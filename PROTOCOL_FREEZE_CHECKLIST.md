# Protocol Freeze Readiness Checklist (Protocol v4)

**Document Version:** 1.0 (Audit & Freeze Review)  
**Date:** October 21, 2026  
**Auditor:** Antigravity Scientific Methodology & Protocol Architecture Team  
**Freeze Status:** **DRAFT — AWAITING HUMAN REVIEW & APPROVAL (EXECUTION SAFETY GATE LOCKED)**  

---

## 1. Protocol Pre-Registration Audit Checklist

| Item # | Pre-Registration Requirement | Status | Audit Findings & Source Verification |
|:---:|---|:---:|---|
| **01** | **Research Question Formulated** | **READY** | Evaluates additive semantic markup on text-based agents (`protocol_v4_draft.md:Section 1`). |
| **02** | **Primary Hypothesis Pre-Specified** | **READY** | Direct directional contrast: ARIA vs Baseline and DATA-CFG vs Baseline (`protocol_v4_draft.md:Section 2`). |
| **03** | **Secondary Hypotheses Defined** | **READY** | Navigation efficiency ($S, T$), markup comparison (ARIA vs DATA-CFG), and refusal accuracy on T6. |
| **04** | **Treatment Arms Operationally Distinct** | **READY** | 4 arms: BASELINE (`v0`), BASELINE_REP (`v0`), ARIA (`v2`), DATA-CFG (`v3`). AST equivalence verified. |
| **05** | **Action Label Confound Eliminated** | **READY** | `shared/app-core.js` button labels refactored to `"Add item to cart"`. SHA-256: `ccae98...` verified. |
| **06** | **Primary Outcome Defined** | **READY** | Binary grounded action success ($Y \in \{0, 1\}$) evaluated via live DOM client state on Tasks T1–T5 ($N=80$). |
| **07** | **Zero Partial Credit Policy** | **READY** | Strict binary scoring: $1.0$ for ground truth, $0.0$ for failures. Unearned 0.25 on T4 eliminated. |
| **08** | **Strict Target SKU Enforcement** | **READY** | T3 strictly requires `wh-002`. Historical flaw accepting 6 SKUs eliminated. |
| **09** | **Precondition Enforcement** | **READY** | T5 runner asserts `pre_cart_count == 1`. Initial empty carts rejected. |
| **10** | **T6 Verifier Resolution** | **READY (DRAFT)** | T6 coded as Grounded Refusal ($Y=1$ on refusal, $0$ on hallucinating 36 mo). Documented for human sign-off. |
| **11** | **Modality Confound Elimination** | **READY** | `use_vision = False` strictly enforced across all runs. Multi-modal screenshot bypass eliminated. |
| **12** | **Survivorship Retry Bias Eliminated** | **READY** | Runner marks both successes and failures as terminal COMPLETED runs. Zero retries of task failures. |
| **13** | **Randomization & Schedule Frozen** | **READY** | RCBD schedule pre-generated (`seed=42`) with 4 blocks of 24 runs in `proposed_randomized_schedule.csv`. |
| **14** | **Statistical Power Sizing Documented** | **READY** | Rigorous derivations: $N=96$ exploratory pilot has only $10.85\%$ power for $\Delta=0.20$; confirmatory study requires $N \ge 480$. |
| **15** | **Mandatory Non-Equivalence Rule** | **READY** | Formally codified: non-significant contrasts cannot be claimed as proof of channel equivalence. |
| **16** | **Multiple Comparison Correction** | **READY** | Bonferroni familywise correction pre-specified: $\alpha_{\text{adj}} = 0.05 / 3 \approx 0.01667$. |
| **17** | **Primary Inferential Model** | **READY** | Task-Stratified Cochran-Mantel-Haenszel (CMH) test implemented in `analyze_v3_results.py`. |
| **18** | **Data Separation & Provenance** | **READY** | Raw historical CSVs preserved untouched; synthetic test data strictly quarantined in `test_scratch_synthetic_data/`. |
| **19** | **Cost Sizing & Spending Ceiling** | **READY** | Pilot cost estimated at $\$0.15$–$\$0.35$; confirmatory at $\$0.75$–$\$1.75$. Hard spending ceiling set at $\$10.00$. |
| **20** | **Execution Safety Gate Preserved** | **LOCKED** | `--live` and `--confirm-live-execution` flags strictly locked. Zero live API calls executed. |

---

## 2. Outstanding Prerequisites for Human Sign-Off

Before Protocol v4 can be formally frozen and authorized for live execution:
1. **Decision on Study Scope:**  
   The human researcher must explicitly choose between:
   - **Option 1 (Exploratory Pilot, $N = 96$):** Cost $\le \$0.50$, run duration ~30 min. Must accept that statistical power is $< 11\%$ and findings are illustrative.
   - **Option 2 (Confirmatory Study, $N = 480$):** Cost $\le \$2.50$, run duration ~2.5 hrs. Provides $80\%$ power to detect $\Delta = 0.20$.
2. **Approval of Task T6 Verifier Logic:**  
   Confirm formal alignment of T6 code with refusal probe logic (`success = bool(refusal and not hallucination)`).
3. **Execution Safety Gate Approval:**  
   Safety gate remains locked until human review of this audit report is concluded.

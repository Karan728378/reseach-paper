# FINAL PROTOCOL FREEZE CHECKLIST (PROTOCOL V4)

**Document Date:** 2026-10-22  
**Auditor:** Senior Research Systems & Methodological Integrity Auditor  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Target Protocol:** Protocol v4 (RCBD, 4 Arms, 6 Tasks, 4 Blocks, Task-Stratified CMH)  
**Overall Readiness Status:** **FREEZE CANDIDATE — PENDING HUMAN APPROVAL OF T6 PATCH & STUDY SCOPE (GATE B: CONDITIONAL GO)**  

---

## 1. Protocol Pre-Registration Audit Checklist

| Item # | Pre-Registration Requirement | Status | Active Code / Fixture Path | Verification Command & Test Status |
|:---:|---|:---:|---|---|
| **01** | **Research Question Formulated** | **PASS** | `PROTOCOL_V4_DRAFT.md` (Section 1) | Evaluates DOM serialization loss and semantic markup efficacy. |
| **02** | **Primary Hypotheses Pre-Specified** | **PASS** | `PROTOCOL_V4_DRAFT.md` (Section 2) | Contrast 1: ARIA vs Baseline; Contrast 2: DATA-CFG vs Baseline. |
| **03** | **Secondary Hypotheses Defined** | **PASS** | `PROTOCOL_V4_DRAFT.md` (Section 2.3) | Step efficiency, token consumption, markup contrast, T6 refusal probe. |
| **04** | **Treatment Arms Operationally Distinct** | **PASS** | `website/templates/*.html` (v0, v2, v3) | `python verify_treatment_delivery_e2e.py` (8/8 PASS). |
| **05** | **Action Label Confound Eliminated** | **PASS** | `website/shared/app-core.js:106` | Generic label `"Add item to cart"`. AST / DOM diffs isolated. |
| **06** | **Primary Outcome Defined** | **PASS** | `protocol_v3_runner.py` / `task_specifications.json` | Grounded action success ($Y \in \{0, 1\}$) on T1–T5 ($N=80$). |
| **07** | **Zero Partial Credit Policy** | **PASS** | `protocol_v3_runner.py:100-112` | Binary scoring: $1.0$ for ground truth match, $0.0$ for failures. |
| **08** | **Strict Target SKU Enforcement** | **PASS** | `protocol_v3_runner.py:91-99` | T3 strictly requires `wh-002` (Whiteboard). Other items fail. |
| **09** | **Precondition Enforcement** | **PASS** | `protocol_v3_runner.py:114-123` | T5 requires cart count == 1 before starting. Empty cart rejected. |
| **10** | **T6 Verifier Resolution** | **ISOLATED (UNMERGED)** | `t6_verifier_isolated.py` & `T6_VERIFIER_PROPOSED_PATCH.diff` | `python test_t6_verifier_isolated.py` (7/7 PASS, 44 cases). Awaiting sign-off. |
| **11** | **Modality Confound Elimination** | **PASS** | `protocol_v3_runner.py:244` | `use_vision = False` strictly enforced. Multi-modal bypass prevented. |
| **12** | **Survivorship Retry Bias Eliminated** | **PASS** | `protocol_v3_runner.py:270-275` | Runner records terminal state on single attempt. No retries of failed runs. |
| **13** | **Randomization & Schedule Frozen** | **PASS** | `proposed_randomized_schedule.csv` | Seed 42, 4 blocks $\times$ 24 runs = 96 runs. Exact sequence pre-generated. |
| **14** | **Statistical Power Sizing Documented** | **PASS** | `STATISTICAL_POWER_AUDIT_FINAL.md` | $N=96$ pilot has $10.85\%$ power ($\Delta=0.20$); $N=480$ provides $80.2\%$. |
| **15** | **Mandatory Non-Equivalence Rule** | **PASS** | `analyze_v3_results.py:148` | Non-significant contrasts cannot be reported as channel equivalence. |
| **16** | **Multiple Comparison Correction** | **PASS** | `analyze_v3_results.py:346` | Bonferroni familywise correction pre-specified: $\alpha_{\text{adj}} = 0.05 / 3 = 0.01667$. |
| **17** | **Primary Inferential Model** | **PASS** | `analyze_v3_results.py:420-510` | Task-Stratified Cochran-Mantel-Haenszel (CMH) test implemented. |
| **18** | **Data Separation & Provenance** | **PASS** | `results/pilot-summary-clean.csv` (SHA-256 verified) | Raw historical data read-only. Test data quarantined. |
| **19** | **Cost Sizing & Spending Ceiling** | **PASS** | `SAFETY_GATE_AND_COST_AUDIT_FINAL.md` | Pilot cost estimated at $\$0.30$–$\$0.65$; spending ceiling set at $\$10.00$. |
| **20** | **Execution Safety Gate Preserved** | **LOCKED** | `protocol_v3_runner.py:248-261` | Live execution unconditionally throws `RuntimeError`. |

---

## 2. Freeze Review Decision Criteria

To transition Protocol v4 from **FREEZE CANDIDATE** to **FORMALLY FROZEN**:
1. **T6 Verifier Approval:** Human approval must be granted to apply [`T6_VERIFIER_PROPOSED_PATCH.diff`](file:///C:/testing/research_execution_20261018/T6_VERIFIER_PROPOSED_PATCH.diff) to [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) and [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py).
2. **Study Scope Agreement:** Explicit selection between:
   - **Pilot Protocol ($N = 96$):** Acknowledging exploratory status, wide confidence intervals, and $10.85\%$ power.
   - **Confirmatory Protocol ($N = 480$):** Sized for $80\%$ power to detect $\Delta = 0.20$ across stratified tasks.
3. **Safety Gate Release:** Safety gate line 258 in [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) must remain locked until 1 and 2 are formally signed off.

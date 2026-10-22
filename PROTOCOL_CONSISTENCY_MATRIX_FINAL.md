# Protocol Consistency Matrix: Final Multi-Artifact Reconciliation

**Document Version:** 1.0 (Final Cross-Artifact Consistency Matrix)  
**Date:** October 22, 2026  
**Auditor:** Antigravity Scientific Methodology & Protocol Architecture Team  
**Compliance Status:** 100% Offline · Fully Reconciled  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Scope & Audited Artifacts

This matrix reconciles every active, intermediate, and legacy artifact across the repository:
1. `tasks/task-definitions.json` (Legacy Protocol v2)
2. `task_specifications.json` (Canonical Protocol v3/v4 Task Specs)
3. `protocol.md` (Protocol v4.0 Narrative Freeze)
4. `analysis_plan.md` (Protocol v4.1 Statistical Plan)
5. `protocol_v4_config.json` (Protocol v4 Draft Machine-Readable Config)
6. `protocol_v3_runner.py` (Active Execution Engine)
7. `offline_test_suite.py` (Active Verification Suite)

---

## 2. Comprehensive Consistency Matrix

| Item / Dimension | Intended Specification (Protocol v4 Draft) | Active Implementation (`protocol_v3_runner.py`) | Test Evidence (`offline_test_suite.py`) | Status | Required Action Prior to Live Execution |
|---|---|---|---|:---:|---|
| **Task T1 (Cheapest Search)** | Add cheapest headphone (`wh-001`, $49.99). Cart contains `wh-001`. Strict binary $1.0 / 0.0$. | Lines 76–87: Asserts `any(i['sku'] == 'wh-001' for i in cart)`. | Lines 45–60: Verified against ground truth. | **ALIGNED** | None. Fully verified. |
| **Task T2 (Entity Addition)** | Add Mechanical Keyboard Pro (`mkp-001`). Cart contains `mkp-001`. Strict binary $1.0 / 0.0$. | Lines 88–99: Asserts `any(i['sku'] == 'mkp-001' for i in cart)`. | Lines 61–75: Verified against ground truth. | **ALIGNED** | None. Fully verified. |
| **Task T3 (Rating Comparison)** | Add second-highest rated audio item (`wh-002`, rating 4.5). Strict single-item match: `len(cart)==1 and cart[0]['sku']=='wh-002'`. | Lines 100–109: Enforces single-item match on `wh-002`. Rejects `wh-001`, `wh-003`, multi-item. | Lines 76–97: Asserts `wh-002` passes; `wh-001` and `mkp-001` fail. | **ALIGNED** | None. Historical 6-SKU flaw eliminated. |
| **Task T4 (Checkout Completion)** | Complete 8-field checkout flow with `mse-001`. Strict binary: $1.0$ only on confirmed order. | Lines 110–113: Requires `order_confirmed` and `has_mouse`; else $0.0$. | Lines 98–113: Asserts unconfirmed order scores $0.0$; confirmed order scores $1.0$. | **ALIGNED** | None. Historical 0.25 unearned credit eliminated. |
| **Task T5 (Cart Mutation)** | Remove pre-seeded item from cart. Requires non-empty pre-state (`pre_cart_count == 1`). Cart empty. | Lines 114–123: Asserts `len(cart) == 0` and `(pre_cart_count is None or pre_cart_count == 1)`. | Lines 115–125: Asserts empty cart with pre-condition passes; non-empty fails. | **ALIGNED** | None. Vacuous pass bug eliminated. |
| **Task T6 (Warranty Probe)** | Grounded Refusal: $1.0$ if refusal detected and no duration hallucinated; $0.0$ if duration asserted. | Lines 124–134: **CRITICAL BUG:** Requires match on `"36 months"` and penalizes refusal! | Lines 126–132: **DEFECTIVE TEST:** Asserts `"36 months"` passes; refusal fails! | **CRITICAL MISMATCH (BLOCKER P2)** | **Apply isolated patch:** `T6_VERIFIER_PROPOSED_PATCH.diff` to runner and test suite. |
| **Treatment Arms** | 4 balanced arms: `BASELINE` (v0), `BASELINE_REP` (v0), `ARIA` (v2), `DATA-CFG` (v3). | Lines 28–33: `ARM_TO_VARIANT` maps 4 arms identically. | Lines 160–185: AST diffs and delivery confirmed. | **ALIGNED** | None. JSON-LD correctly excluded. |
| **Observation Whitelists** | Default whitelist for Baseline and ARIA; extended whitelist for `DATA-CFG`. | Configured via `DOMTreeSerializer(extra_attributes=...)`. | `verify_treatment_delivery_e2e.py`: Verified in Chromium. | **ALIGNED** | None. Delivery confirmed. |
| **Randomization & Blocking** | 4 blocks of 24 runs, RCBD, balanced by arm and task, pre-randomized within block. | Consumes `proposed_randomized_schedule.csv` sequentially. | `offline_test_suite.py:175-195`: Checks 4 blocks, 24/arm, 16/task. | **ALIGNED** | None. Perfectly balanced. |
| **Retry & Survivorship** | Terminal recording of both successes and failures. Zero retries of failed runs. | Lines 144–160: `get_completed_run_indices` marks completed for both True and False. | Lines 145–165: Verifies failed runs are logged as completed. | **ALIGNED** | None. Survivorship bias eliminated. |
| **Sample Size & Power** | Exploratory Pilot: $N=96$ ($N_{\text{primary}}=80$, power $10.85\%$). Confirmatory: $N=480$ ($80\%$). | Executes 96-run schedule. | `test_power_audit.py`: Verifies $10.85\%$ power and $N \ge 480$ sizing. | **RECONCILED (BLOCKER P1)** | **Human Decision Required** to formally select study scope. |
| **Safety Gate** | Strict execution lock on `--live` requiring `--confirm-live-execution` and pre-paid API tier. | Lines 248–261: Throws unconditional `RuntimeError` on live mode. | `test_mutation_audit.py`: Proves live invocation throws error. | **ALIGNED & LOCKED** | Maintain safety lock until human authorization. |

---

## 3. Summary of Status & Unresolved Items

- **Total Dimensions Reconciled:** 12
- **Fully Aligned & Verified:** 10 dimensions ($83.3\%$).
- **Pending Blockers:**
  1. **Dimension 6 (Task T6 Verifier):** Code mismatch identified, analyzed, and patched in isolated module (`t6_verifier_isolated.py`). Awaiting human authorization to apply `T6_VERIFIER_PROPOSED_PATCH.diff`.
  2. **Dimension 11 (Study Scope):** Human researcher decision required to choose between Exploratory Pilot ($N=96$) and Confirmatory Study ($N=480$).

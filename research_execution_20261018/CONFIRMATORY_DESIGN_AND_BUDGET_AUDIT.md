# Audit Report C: Confirmatory Design, Resource Budget, and Quota Audit
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Target Schedule:** [proposed_3arm_schedule.csv](file:///C:/testing/research_execution_20261018/proposed_3arm_schedule.csv) ($N=72$)  
**Target Output Summary:** [v3_3arm_summary.csv](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv)  
**Target Detail Directory:** `results/3arm_runs/`  
**Daily Quota Ledger:** [daily_quota_ledger.json](file:///C:/testing/research_execution_20261018/results/daily_quota_ledger.json)  

---

## 1. Confirmatory Design Verification ($N=72$)

### A. Structure & Factorial Allocation
- **Experimental Design:** Randomized Complete Block Design (RCBD).
- **Factors:**
  - **Factor 1 (Treatment Arm, 3 levels):** `ABS` (v0-baseline), `ARIA` (v2-aria), `DATA-CFG` (v3-data-attrs).
  - **Factor 2 (Task Construct, 6 levels):** `T1` (Search), `T2` (Target finding), `T3` (Ranked comparison), `T4` (Multi-step checkout), `T5` (State mutation/removal), `T6` (Negative unstated probe).
  - **Blocking Factor (Temporal Block, 4 levels):** `Block 1`, `Block 2`, `Block 3`, `Block 4`.
- **Sample Allocation:**
  - $3 \text{ arms} \times 6 \text{ tasks} = 18 \text{ trials per block}$.
  - $4 \text{ blocks} \times 18 \text{ trials} = \mathbf{72 \text{ total trials}}$.
  - Exact replicate count per `(arm, task)` pair = **4 replicates** (1 in each block).
  - Total per arm = **24 runs** ($24 \times 3 = 72$).
  - Total per task = **12 runs** ($12 \times 6 = 72$).

### B. Statistical Analysis Plan Alignment
- **Primary Outcomes:** Binary task success ($Y \in \{0, 1\}$) on grounded action tasks `T1` through `T5` ($N = 60$).
- **Exploratory Outcome:** Task `T6` analyzed separately as a negative probe evaluating grounded refusal vs. duration hallucination.
- **Statistical Tests:**
  1. **Task-Stratified Cochran-Mantel-Haenszel (CMH) Test:** Tests for conditional independence of treatment and outcome across task strata.
  2. **Risk Differences:** Pairwise differences $\hat{p}_{\text{treatment}} - \hat{p}_{\text{ABS}}$ with 95% Newcombe hybrid score intervals.
  3. **Multiplicity Correction:** Family-wise Bonferroni correction for 3 contrasts: $\alpha_{\text{adj}} = 0.05 / 3 = 0.0167$.
- **Alignment:** All analysis procedures in [analyze_v3_results.py](file:///C:/testing/research_execution_20261018/analyze_v3_results.py) consume `v3_3arm_summary.csv` directly and implement these exact statistical tests.

---

## 2. Resource Budget and Quota Audit

### A. Provider Quota Limits (`gemini-3.1-flash-lite`)
- **Account Tier:** Google AI Studio Free of Charge Tier ($0.00 spend guard enforced).
- **Rate Limit:** 15 Requests Per Minute (RPM).
- **Daily Request Quota:** 1,500 Requests Per Day (RPD).

### B. Runner Guardrails & Enforcement
1. **Daily Ledger Tracking:** [LocalBudgetGuard](file:///C:/testing/research_execution_20261018/budget_controller.py) loads daily request offsets from [daily_quota_ledger.json](file:///C:/testing/research_execution_20261018/results/daily_quota_ledger.json) and all summary CSVs.
2. **Hard Request Ceiling:** Configured via `--max-requests` (e.g. 600). The guard calculates worst-case headroom (`max_steps_per_run`) before every single trial dispatch. If remaining requests $< \text{max\_steps}$, execution halts immediately (`check_can_dispatch_trial`).
3. **Pacing Guard:** Runner executes `await asyncio.sleep(15.0)` between consecutive live trials. Even with 4 steps per run, effective RPM is $\le 4 \text{ RPM}$, strictly below the 15 RPM provider ceiling.
4. **Retry & Backoff Guard:** Bounded to 1 attempt; does not loop indefinitely on 429/503 errors.

### C. Current Execution Inventory in `results/v3_3arm_summary.csv`
An audit of the persistent confirmatory summary reveals that execution is already substantially underway:
- **Block 1 (Runs 1–18):** **18 / 18 COMPLETED** (100% complete).
- **Block 2 (Runs 19–36):** **12 / 18 COMPLETED** (Runs 19 through 30 completed; Run 26 had 3 infrastructure aborts and then completed on attempt 4).
- **Remaining in Block 2:** Runs 31 through 36 (6 trials).
- **Block 3 (Runs 37–54):** 18 trials pending.
- **Block 4 (Runs 55–72):** 18 trials pending.
- **Total Completed Confirmatory Runs:** **30 / 72 (41.7%)**.
- **Total Remaining Confirmatory Runs:** **42 / 72 (58.3%)**.

### D. Quota Headroom Analysis for Remaining Execution
- Current requests used today: **435 requests**.
- Daily ceiling configured: **600 requests** (headroom: **165 requests**).
- Completing the rest of Block 2 (Runs 31–36, 6 runs):
  - Estimated average steps per run: 4–6 steps.
  - Expected request consumption: $6 \times 5 \approx \mathbf{30 \text{ requests}}$.
  - Post-Block 2 cumulative requests: $\approx 465 \text{ requests} < 600 \text{ ceiling} \ll 1,500 \text{ RPD}$.
- **Verdict:** Executing the remainder of Block 2 (Runs 31–36) is **completely safe, fully within daily quota, and well below the request ceiling**.

---

## 3. Resumption & Idempotence Rules

1. `get_completed_run_indices(summary_path)` returns `{1, 2, ..., 30}`.
2. The runner automatically iterates from Run 1, skips Runs 1–30 without duplicate model inference, and dispatches **Run 31** as the exact next trial.
3. Every completed run persists its detailed trace to `results/3arm_runs/run_{idx:03d}.json` and appends its row to `results/v3_3arm_summary.csv`.
4. If an infrastructure abort occurs, it is recorded as `run_{idx:03d}_attempt_{att}.json` and the trial is retried without overwriting earlier evidence.

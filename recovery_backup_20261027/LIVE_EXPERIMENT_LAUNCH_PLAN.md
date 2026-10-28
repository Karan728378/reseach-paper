# LIVE EXPERIMENT LAUNCH PLAN (PROTOCOL V4)

**Document Date:** October 22, 2026  
**Auditor / Engineer:** Senior Research Systems & Methodological Integrity Auditor  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Target Runner:** [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)  
**Security Status:** **SAFETY GATE CURRENTLY LOCKED · ZERO MODEL CALLS AUTHORIZED WITHOUT SIGN-OFF**

---

## 1. Study Design Options

The researcher must select between two pre-specified study scopes before releasing the safety gate:

### Option A: The Exploratory Pilot ($N = 96$)
* **Objective:** Establish real-world agent execution baseline, evaluate variance under single-shot conditions, test observation delivery stability, and observe exploratory T6 refusal rates.
* **Design Structure:** 4 Blocks $\times$ 4 Arms $\times$ 6 Tasks = 96 total runs (80 primary runs on T1–T5; 16 probe runs on T6; 4 runs/cell).
* **Statistical Power:** $10.85\%$ power to detect a realistic semantic effect ($\Delta = 0.20$); $49.6\%$ power for $\Delta = 0.35$.
* **Mandatory Reporting Constraint:** If results are not statistically significant ($p > 0.0167$), findings **must not** be reported as channel equivalence or proof that markup has no effect.
* **Estimated Cost:** $\$0.30$ – $\$0.65$ USD.
* **Estimated Wall-Clock Duration:** ~45 minutes.

### Option B: The Confirmatory Superiority Trial ($N = 480$)
* **Objective:** Definitive confirmatory testing of additive semantic markup efficacy with pre-registered $80\%$ statistical power.
* **Design Structure:** 20 Blocks $\times$ 4 Arms $\times$ 6 Tasks = 480 total runs (400 primary runs on T1–T5; 80 probe runs on T6; 20 runs/cell).
* **Statistical Power:** $80.2\%$ power to detect $\Delta = 0.20$ at Bonferroni-adjusted $\alpha = 0.0167$.
* **Estimated Cost:** $\$1.50$ – $\$3.25$ USD.
* **Estimated Wall-Clock Duration:** ~3.5 hours.

---

## 2. Experimental Parameters & Technical Controls

All live trials are locked to the following immutable execution parameters:
* **LLM Provider:** Google Cloud / Gemini API.
* **Model ID:** `gemini-flash-lite-latest` (fixed across all blocks and arms).
* **Modality:** Text-Only (`use_vision = False` strictly enforced; multimodal visual inspection disabled).
* **Temperature:** 0.0 (deterministic greedier decoding for maximum protocol reproducibility).
* **Browser Harness:** `browser-use 0.13.10` via headless Chromium (1920 $\times$ 1080 viewport).
* **Attribute Exposure Whitelists:**
  * `BASELINE` (Arm 1): `DEFAULT_INCLUDE_ATTRIBUTES` (Standard visible DOM).
  * `BASELINE_REP` (Arm 2): `DEFAULT_INCLUDE_ATTRIBUTES` (Standard visible DOM; tests temporal drift).
  * `ARIA` (Arm 3): `DEFAULT_INCLUDE_ATTRIBUTES` (Interactive ARIA labels preserved; non-interactive pruned).
  * `DATA-CFG` (Arm 4): `EXTENDED_ATTRIBUTES` (`data-action`, `data-product-id`, `data-amount` whitelisted).
* **Single-Shot Policy:** Exactly one attempt per scheduled run. No retry-until-success.
* **Scoring Rubrics:**
  * T1: `wh-001` in cart ($1.0 / 0.0$).
  * T2: `mkp-001` in cart ($1.0 / 0.0$).
  * T3: `wh-002` only in cart ($1.0 / 0.0$).
  * T4: Order confirmed with `mse-001` ($1.0 / 0.0$).
  * T5: Cart empty with pre-state verification ($1.0 / 0.0$).
  * T6: Grounded refusal without duration hallucination ($1.0 / 0.0$).

---

## 3. Launch Commands & Execution Sequence

### Phase 1: Environment Preparation (Terminal Session)
```powershell
# 1. Navigate to research workspace
cd C:\testing\research_execution_20261018

# 2. Export API Key (Private session variable; never commit to git)
$env:GOOGLE_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY"

# 3. Verify key is recognized securely (without printing value)
C:\testing\.venv311\Scripts\python.exe -c "import os; print('Key present:', bool(os.getenv('GOOGLE_API_KEY')))"
```

### Phase 2: Launching the Trial

#### To Launch Option A (Exploratory Pilot, $N = 96$):
```powershell
C:\testing\.venv311\Scripts\python.exe protocol_v3_runner.py --live --confirm-live-execution --max-runs 96
```

#### To Launch Option B (Confirmatory Trial, $N = 480$):
```powershell
C:\testing\.venv311\Scripts\python.exe protocol_v3_runner.py --live --confirm-live-execution --max-runs 480
```

### Phase 3: Post-Execution Automated Statistical Analysis
Immediately following trial completion, execute the standardized statistical analysis pipeline:
```powershell
C:\testing\.venv311\Scripts\python.exe analyze_v3_results.py --data results/v3_run_summary.csv --out-dir results/live_analysis
```

---

## 4. Gate D Release Procedure (Researcher Authorization Only)

To authorize live execution, the human researcher must execute the following two steps:

1. **Safety Interlock Deactivation:**
   In [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py), comment out or remove lines 258–261:
   ```python
   # BEFORE (LOCKED):
   raise RuntimeError(
       "SAFETY GATE: Live execution remains gated pending user protocol review.\n"
       "To launch live trials after review, update the safety gate in protocol_v3_runner.py."
   )

   # AFTER (UNLOCKED):
   # Safety gate released by researcher authorization. Proceeding to live agent trials.
   ```
2. **Execute Launch Command:** Run Phase 2 command in a terminal where `$env:GOOGLE_API_KEY` is set.

---

## 5. Abort and Stop Conditions

Execution will automatically halt immediately if any of the following occur:
1. **Spending Cap:** Cumulative estimated token expenditure exceeds $\$10.00$.
2. **API Quota Exhaustion:** Receiving three consecutive HTTP 429 / `RESOURCE_EXHAUSTED` responses halts the runner gracefully without corrupting recorded runs.
3. **Run Limit:** Reaching `--max-runs` completes the batch cleanly.
4. **Manual Abort:** Pressing `Ctrl+C` terminates cleanly; all completed runs are safely flushed to `results/v3_run_summary.csv` and can be resumed seamlessly by re-running the launch command.

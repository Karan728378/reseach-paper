# Current State, Provenance & Submission Blockers

**Date:** 2026-10-25  
**Auditor:** Independent Systems & Methodology Auditor  
**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*  
**Workspace:** `C:\testing\research_execution_20261018`  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe`  
**Manuscript Source:** [`research_paper_final.tex`](file:///C:/testing/research_execution_20261018/research_paper_final.tex)  
**Safety Protocol:** 100% Offline Forensic Verification · Zero Live Model/API Calls · Quota Ledger Preserved  

---

## 1. What Exists and What Actually Ran

### 1.1 Empirical Executions (Live Runs)
1. **Phase 1 Cloud Pilot (`gemini-3.1-flash-lite` via Google AI Studio):**
   - **Schedule Planned:** 72 trials (proposed 3-arm schedule: 3 arms $\times$ 6 tasks $\times$ 4 blocks).
   - **Raw Execution Records:** Exactly 46 records in [`results/v3_3arm_summary_raw.csv`](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary_raw.csv) and 46 raw JSON trace files in [`results/3arm_runs/`](file:///C:/testing/research_execution_20261018/results/3arm_runs/).
   - **Clean Summary:** 44 rows in [`results/v3_3arm_summary.csv`](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv).
   - **Unique Completed Trials:** Exactly **41 unique schedule indices (Runs 1–41)**.
   - **Trial Outcome Profile:** **41 / 41 completed trials achieved a score of 1.0 (100% success)** across all three arms:
     - Control Arm (\textsc{ABS}): **13 / 13 (100%)**
     - Semantic Arm (\textsc{ARIA}): **13 / 13 (100%)**
     - Custom Data Arm (\textsc{DATA-CFG}): **15 / 15 (100%)**
   - **Infrastructure Aborts:** Run 26 (Task T2, ARIA) encountered 3 consecutive `503 UNAVAILABLE` errors from Google AI Studio before succeeding on attempt 4.
   - **Duplicate Records:** Run 34 (Task T4, ARIA) and Run 38 (Task T2, DATA-CFG) each had 2 completed attempts in the raw log, deduplicated to 1 canonical record in the clean summary.

2. **Local Hardware Diagnostic Pilot (`qwen3:4b` via Ollama `127.0.0.1:11434`):**
   - **Total Runs Attempted:** 5 runs (`qwen3_smoke_001` through `005`).
   - **Hardware Configuration:** Intel Core i7, 16 GB RAM, NVIDIA RTX 3050 Laptop GPU (4 GB VRAM; 34% layers offloaded to CPU).
   - **Outcomes:**
     - Run 001: Failed at initialization due to Pydantic validation constraint (`max_history_items <= 5`).
     - Run 002: Clicked target button (verified in cart: `mkp-001`), timed out waiting for completion response.
     - Run 003: Step 1 (prompt ~1,500 tokens) completed in 102.9s. Step 2 (context expanded to >3,200 tokens) breached the 180s step watchdog before model generation finished. Post-hoc CDP verifier confirmed target item in cart (`score=1.0`).
     - Run 004: Step 1 timed out after 180s. Unhandled `asyncio.CancelledError` caused empty telemetry list (`[]`).
     - Run 005: Step 1 timed out after 180s. Fixed wrapper caught `asyncio.CancelledError` (`BaseException`), capturing 1 in-flight call of 179.7s wall-clock duration.

3. **Confirmatory Phase 2 (Runs 42–72):**
   - **Status:** **UNEXECUTED / HELD OFFLINE**.
   - Halted fail-closed when the cumulative daily request ledger reached 604 requests against a 600 ceiling.

### 1.2 Synthetic & Offline Test Datasets
1. **Synthetic Statistical Validation Datasets:**
   - 8 synthetic datasets in `test_scratch_synthetic_data/` simulating diverse response distributions (Simpson's Paradox, zero cells, baseline drift) to validate the CMH and Newcombe estimators in [`analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/analyze_v3_results.py).
   - Strictly segregated from live empirical data; reported only in Appendix A.
2. **Offline Test Suite:**
   - 16 test files (`test_*.py`) containing **126 unit and offline integration tests**.
   - All 126 tests execute and pass in ~15 seconds with 0 errors and 0 failures.

---

## 2. Evidence Categorization: Raw, Derived, Exploratory, Synthetic, Confirmatory

| Data Artifact | Classification | Evidentiary Role & Scope Constraints |
| :--- | :---: | :--- |
| `results/3arm_runs/run_*.json` (46 files) | **Raw Empirical Data** | Raw multi-turn execution traces of 41 completed trials + 5 duplicate/aborted attempts on `gemini-3.1-flash-lite`. |
| `results/v3_3arm_summary_raw.csv` | **Raw Empirical Log** | 46 rows documenting chronological execution of Phase 1 cloud pilot. |
| `results/v3_3arm_summary.csv` | **Derived Data** | 44 rows (41 completed unique trials + 3 failed attempts of Run 26). |
| 41 Cloud Pilot Trials (100% success) | **Exploratory Pilot** | Demonstrates an acute **Ceiling Effect** on the initial task battery. Prohibits claiming treatment equivalence or additive superiority. |
| `results/local_llama_pilot_runs/*.json` (6 files) | **Raw Diagnostic Data** | Traces of 5 local `qwen3:4b` runs. |
| Local Qwen Latency / Telemetry | **Engineering Diagnostic Case Study** | Demonstrates prompt-processing latency under context expansion on consumer hardware. Prohibits causal claims comparing cloud vs. local models. |
| `test_scratch_synthetic_data/` (8 datasets) | **Synthetic Data** | Mathematical test vectors for validating statistical code paths. Must never be pooled with empirical data. |
| Phase 2 72-Trial / 96-Trial Design | **Confirmatory Blueprint (Pending)** | Pre-registered experimental protocol held offline under budget lock. Zero confirmatory live trials have run. |

---

## 3. Prior Audit Statements: Independently Reproduced vs. Unverified

### 3.1 Independently Reproduced Statements
1. **Pruning of `<script>` and `<meta>` (`serializer.py:18`):** Verified by AST inspection and test execution in `test_observation_pipeline_stages.py`.
2. **0% Schema.org JSON-LD Reachability:** Verified by intercepting observation payloads on `v1-jsonld`.
3. **Stripping of Non-Interactive Tags (`serializer.py:1046–1058`):** Verified; parent `<span>` and `<div>` tags and their attributes (`aria-label`, `role`, `data-*`) are stripped, emitting only inner text.
4. **Omission of Custom `data-*` (`views.py:18–45`):** Verified; omitted by default whitelist on interactive elements, and permanently stripped on non-interactive containers.
5. **Node Correspondence on Route `#home` (27/34, 79.4%):** Verified via CDP `Accessibility.getFullAXTree` matching; Wilson 95% CI is $[63.2\%, 89.7\%]$.
6. **Action-Label Co-Location Fix (`shared/app-core.js:243`):** Verified; button `aria-label` standardized to `"Add item to cart"`, eliminating target-entity string leakage.
7. **Cloud Pilot Reconciliation:** Verified; exactly 46 raw entries, 44 clean summary rows, 41 completed unique trials, 41/41 score 1.0 (ABS 13/13, ARIA 13/13, DATA-CFG 15/15).
8. **Local Qwen Run 003 & 005 Diagnostics:** Verified; Run 003 step 1 took 102.9s and step 2 timed out after 180s watchdog; Run 005 captured in-flight `asyncio.CancelledError` after 179.7s.
9. **TOST Equivalence Sample Size Math ($N \ge 1,360$ across 4 arms, $N \ge 1,080$ across 3 arms):** Verified by independent derivation in `reproduce_power_audit.py`.
10. **Monte Carlo Power Bound ($10.8\% \pm 0.6\%$ for $n=20$ at $\Delta=0.20$):** Verified via 10,000-trial simulation in `power_analysis.py`.
11. **Client-Side Budget Guard Fail-Closed Halting (604/600):** Verified via 5 offline integration tests in `test_runner_guard_integration.py`.
12. **126 Offline Tests Passing:** Verified by running `python -m unittest discover -s . -p "test_*.py"` (0 errors, 0 failures).

### 3.2 Statements Remaining Unverified or Requiring Qualification
1. **Universal Serializer Retention Rate:** Any claim that the 79.4% node correspondence on `#home` applies to arbitrary web pages is unverified; node correspondence is route- and layout-specific.
2. **Confirmatory Markup Efficacy:** Any claim that ARIA or `data-*` improves or does not improve task success rate in live autonomous agents is completely unverified, because the pilot suffered a ceiling effect and Phase 2 confirmatory runs have not been executed.
3. **Cross-Framework Generality:** Claims regarding observation pruning apply strictly to `browser-use 0.13.10`. Behavior in other frameworks (BrowserGym, Crawl4AI, Stagehand, Skyvern) remains unverified.
4. **Compiled Manuscript PDF Inspection:** The host environment lacks `pdflatex`, `xelatex`, and `latexmk`. The compiled PDF has not been rebuilt or visually inspected in this session.

---

## 4. Current Safety and Budget State

- **Historical Ledger File:** [`results/daily_quota_ledger.json`](file:///C:/testing/research_execution_20261018/results/daily_quota_ledger.json).
- **Recorded Cumulative Requests:** **604 requests**.
- **Configured Request Ceiling:** **600 requests**.
- **Historical Overrun Event:** The ledger reached 604 requests because earlier runner code evaluated quotas at the trial level rather than intercepting individual model invocations, allowing multi-step trials to complete across the boundary.
- **Current Protection State:** `BudgetGuardedChatModel` wraps the LangChain chat model. It checks remaining headroom (`cumulative_requests < max_requests_ceiling`) before every `ainvoke()` / `invoke()` call. With cumulative requests at 604 and ceiling at 600, it evaluates $604 \ge 600$ and raises `QuotaExceededError` fail-closed.
- **Safety Invariant:** Zero live model dispatches are permitted without explicit user authorization, a documented reset of the ledger, and an approved budget.

---

## 5. The Five Precise Blockers to an Honest Submission

1. **Blocker 1: Ceiling Effect in Phase 1 Pilot Prevents Performance Comparison.**  
   All 41 completed cloud trials achieved 1.0 success across all three arms. As a result, the live agent data provides zero variance and cannot test whether semantic markup aids or hinders agent performance. The paper must not present this pilot as a capability benchmark; it must be presented strictly as an exploratory pilot demonstrating a ceiling effect.
2. **Blocker 2: Confirmatory Phase 2 Experiment Has Not Run.**  
   The pre-registered randomized block experiment designed to resolve the ceiling effect remains unexecuted due to budget ceiling enforcement. The paper cannot make confirmatory claims regarding agent task completion.
3. **Blocker 3: Single-Framework Scope Limits External Validity.**  
   All AST inspection and dynamic serializer tests were performed on `browser-use 0.13.10`. The findings cannot be claimed as universal to all autonomous web agents without cross-framework evaluation.
4. **Blocker 4: Local LaTeX Toolchain is Missing.**  
   Neither `pdflatex`, `xelatex`, nor `latexmk` is installed on the host. While LaTeX syntax, environment balancing, and citation keys have been verified at the AST level using `check_latex.py`, visual inspection of final typesetting, page breaks, and rendered TikZ figures requires compilation via an external TeX Live distribution or Overleaf.
5. **Blocker 5: Small Sample Sizes Preclude Equivalence Claims.**  
   Small-sample agent benchmarks ($n \approx 13$–$24$ per arm) have $<11\%$ statistical power. Concluding that baseline HTML and semantic markup perform "identically" or "equivalently" from non-significant results is mathematically invalid (The Equivalence Fallacy).

---
*Certified by Independent Systems & Methodology Auditor.*

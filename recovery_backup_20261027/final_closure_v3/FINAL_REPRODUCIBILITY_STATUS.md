# FINAL REPRODUCIBILITY STATUS — DOM SERIALIZATION GAP RESEARCH

**Project:** *The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents*  
**Date:** October 2026  
**Package:** `final_closure_v3`  
**Execution Environment:** Windows 11, Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`), `browser-use 0.13.10`

---

## 1. Executive Reproducibility Boundary

To ensure absolute scientific integrity, this document delineates the strict boundary between **offline reproducible assets** (which can be independently executed and verified in under two minutes from local files) and **external/live dependencies** (which require remote network access, external services, or user authorization).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       REPRODUCIBILITY BOUNDARY MAP                          │
├──────────────────────────────────────────────┬──────────────────────────────┤
│    100% OFFLINE REPRODUCIBLE ASSETS          │    BLOCKED / EXTERNAL ASSETS │
│    (No Network, No Spend, No Keys)           │    (Requires Auth / Network) │
├──────────────────────────────────────────────┼──────────────────────────────┤
│ 1. 138 Unit & Regression Tests (Exit: 0)     │ 1. Live Gemini Cloud Trials  │
│ 2. 5-Stage Metadata Reachability Traces      │    (Locked at 604/600 Quota) │
│ 3. 4-Route CDP Blink AXTree vs. Serializer   │ 2. 72-Run Confirmatory Trial │
│ 4. Analytical Power & TOST Sample Sizes      │    (Held Offline / Unrun)    │
│ 5. Clinical Statistical Engine (CMH/Fisher)  │ 3. Local Ollama Qwen GPU     │
│ 6. Quota Controller Fail-Closed Invariants   │    (Requires Running Daemon) │
└──────────────────────────────────────────────┴──────────────────────────────┘
```

---

## 2. Fully Reproducible Offline Artifacts

The following six empirical and systems analyses can be executed directly by any researcher using the provided local repository without external credentials, network access, or monetary cost:

### A. Full Automated Regression Test Suite (138 Tests)
- **Scope:** Verifies the complete software implementation of the testing harness, state-asserted verifiers, budget controllers, and observation extraction pipelines.
- **Exact Command:**
  ```bash
  C:\testing\.venv311\Scripts\python.exe -m unittest discover -s . -p "test_*.py" --buffer
  ```
- **Execution Benchmark:** 138 tests run in **16.579 seconds**.
- **Expected Outcome:** `OK` (Exit code: 0; 0 failures, 0 errors, 0 skips).

---

### B. Multi-Route Correspondence Census (Table 2)
- **Scope:** Extracts Chromium's native Blink accessibility tree via CDP and compares it against `browser-use 0.13.10`'s interactive selector map across four routes (`#home`, `#cart`, `#checkout`, `#search?q=audio`).
- **Exact Command:**
  ```bash
  C:\testing\.venv311\Scripts\python.exe scratch/run_phase_b_browser_experiments.py
  ```
- **Primary Data Output:** `local_closure_results/multi_route_observation_audit.json`
- **Expected Outcome:**
  - `#home`: 34 selectors, 27 matched (79.4%), 7 unmatched badge spans, 26/26 genuine controls matched (100.0%).
  - `#cart`: 8 selectors, 8 matched (100.0%), 7/7 genuine controls matched (100.0%).
  - `#checkout`: 13 selectors, 13 matched (100.0%), 12/12 genuine controls matched (100.0%).
  - `#search`: 19 selectors, 16 matched (84.2%), 3 unmatched badge spans, 10/10 genuine controls matched (100.0%).

---

### C. Multi-Stage Metadata Reachability Audit (Table 1)
- **Scope:** Traces semantic metadata channels (Schema.org JSON-LD, container ARIA, custom `data-*` attributes) through the five observation pipeline representations.
- **Exact Command:**
  ```bash
  C:\testing\.venv311\Scripts\python.exe audit_metadata_reachability.py
  ```
- **Primary Data Output:** `serialization_audit_metrics.json`
- **Expected Outcome:** Confirms deterministic pruning of Schema.org JSON-LD at line 18 of `dom/service.py` and stripping of non-interactive ARIA at line 1046 of `dom/serializer/serializer.py`.

---

### D. TOST Power and Sample-Size Planning Bounds (§6.2 & §6.3)
- **Scope:** Computes power surfaces and sample-size boundaries under Farrington-Manning two one-sided test formulation for equivalence testing.
- **Exact Command:**
  ```bash
  C:\testing\.venv311\Scripts\python.exe reproduce_power_audit.py
  ```
- **Expected Outcome:**
  - $n \le 20$ per arm yields $10.8\%$ power for $\Delta = 0.20$ and $49.6\%$ for $\Delta = 0.35$.
  - $\delta = \pm 0.10$ equivalence at $\alpha = 0.05, 1-\beta = 0.80, p = 0.70$ requires $n = 358 \approx 360$ per arm ($N \ge 1,080$ for 3 arms, $N \ge 1,440$ for 4 arms).

---

### E. Clinical Statistical Engine Verification (Appendix A, Tables 3 & 4)
- **Scope:** Verifies numerical stability of stratified Cochran-Mantel-Haenszel tests, Bonferroni multi-contrast adjustments, and Newcombe hybrid score confidence intervals against clinical reference tables.
- **Exact Command:**
  ```bash
  C:\testing\.venv311\Scripts\python.exe -m unittest test_analyze_v3_results.py
  ```
- **Expected Outcome:** `Ran 10 tests in ~0.5s ... OK` (Exit code: 0).

---

### F. Quota Controller Fail-Closed Invariants (Appendix C)
- **Scope:** Verifies that the budget controller halts at the exact 600-request ceiling, enforces worst-case trial headroom, and maintains fail-closed locking when initialized with the historical 604-request ledger.
- **Exact Command:**
  ```bash
  C:\testing\.venv311\Scripts\python.exe -m unittest test_budget_guard_repairs.py
  ```
- **Expected Outcome:** `Ran 6 tests in ~1.5s ... OK` (Exit code: 0).

---

## 3. Assets Requiring External Services or User Authorization

The following experimental components cannot be executed offline and are explicitly bounded:

1. **Live Cloud Model Trials (`gemini-flash-lite-latest`):**
   - **Status:** **STRICT HOLD (Locked)**
   - **Reason:** Historical ledger at `results/daily_quota_ledger.json` records 604 cumulative requests against a 600-request ceiling (`halted_due_to_ceiling: true`).
   - **Prerequisites for Resumption:** Requires paid cloud credits, remote network connection, and explicit user authorization. Initiating live cloud calls during this offline correction pass is strictly prohibited under project rules.

2. **Confirmatory 4-Arm Phase 2 Trials:**
   - **Status:** **UNEXECUTED (Protocol Preserved)**
   - **Reason:** Demonstrating whether observation reachability differences translate into behavioral task success requires executing the full randomized block protocol ($N \ge 72$ to $1,080$ trials).
   - **Prerequisites for Execution:** Requires lifting the budget ceiling and running extensive live model evaluations across all four treatment arms.

3. **Local Quantized Model GPU Telemetry (`qwen3:4b`):**
   - **Status:** **DIAGNOSTIC ARCHIVE (5 Completed Runs)**
   - **Reason:** Telemetry recorded in `results/local_llama_summary.csv` was captured during exploratory hardware testing. Re-running requires an active local Ollama daemon with the `qwen3:4b` checkpoint loaded in memory.

---

## 4. Summary Verdict on Reproducibility

- **Is the paper's systems audit reproducible?** **YES, 100%.** Every pipeline measurement, reachability matrix, AST line reference, and multi-route census is fully reproducible offline from local scripts.
- **Is the paper's behavioral efficacy claim reproducible?** **N/A.** The paper explicitly makes **no behavioral efficacy claim**, framing the contribution strictly as an empirical systems audit and statistical power analysis.

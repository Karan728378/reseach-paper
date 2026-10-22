# REPRODUCIBILITY GUIDE

**Project:** Autonomous Browser Agent Additive Semantic Markup Study (Option A)  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe`  
**Working Directory:** `C:\testing`  

---

## 1. System Requirements & Environment Setup

This project is fully containerized locally on Windows with zero cloud network dependencies for offline demonstration and testing.

- **Operating System:** Windows 10/11 (64-bit)
- **Python Version:** Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`)
- **Key Installed Packages:**
  - `browser-use 0.13.10`
  - `playwright` (with installed Chromium headless browser)
  - `langchain-core`
- **Port Requirement:** Local port `8097` (used by the quiet internal HTTP server during demonstrations).

---

## 2. Integrity Verification (Protected Baseline Hashes)

Before executing any script, verify that all 12 protected baseline source files match their authentic SHA-256 hashes:

```powershell
C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\offline_test_suite.py
```

### Expected Output
```
=== Running Offline Audit & Verification Suite (11 Tests) ===
[01/11] PASS: test_serializer_disabled_elements
...
[11/11] PASS: test_original_files_unmodified
       -> All original source files are 100% UNTOUCHED matching authentic baseline hashes (CONFIRMED)
Test execution complete: 11/11 PASSED.
```

---

## 3. One-Command Master Offline Demonstration

To execute the entire 5-step end-to-end demonstration and generate the interactive dashboard:

```powershell
C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\run_offline_pipeline_demo.py
```

### What This Command Executes Autonomously
1. **Protected File Check:** Validates SHA-256 hashes of all 12 original baseline files.
2. **Schedule Check:** Confirms the 96-run RCBD schedule is mathematically orthogonal.
3. **Step 3A (DOM Mechanics):** Launches headless Chromium via Playwright, executes scripted clicks for Tasks T1–T6, verifies client cart and order states, and logs to `results/demo_browser_mechanics_and_verifier_runs.csv`.
4. **Step 3B (Prompt Delivery):** Executes a `MockChatModel` under `use_vision=False`, extracts the prompt buffer across 4 variants, proves ARIA and `data-*` delivery, confirms JSON-LD script pruning, and logs to `results/demo_agent_prompt_delivery_runs.csv`.
5. **Step 4 (Statistical Analysis):** Runs `analyze_v3_results.py` over the 96-run synthetic benchmark (`dataset_1_valid_complete.csv`), computing task-stratified CMH $\chi^2$, Newcombe 95% CIs, Agresti–Caffo CIs, Bonferroni adjustments, and baseline stability tests.
6. **Step 5 (Dashboard Generation):** Updates the dark-mode HTML dashboard at [`results/dashboard.html`](file:///C:/testing/research_execution_20261018/results/dashboard.html).

---

## 4. Standalone Test Suite Execution Commands

Every component can be verified independently using standard unit test runners:

| Component | Target Verification | PowerShell Command | Expected Exit Code & Outcome |
| :--- | :--- | :--- | :---: |
| **Harness & Verifiers** | 11 offline regression tests | `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\offline_test_suite.py` | `0` (11/11 Passed) |
| **Prompt Observation** | 5 live observation traces | `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\test_agent_prompt_pipeline.py` | `0` (5/5 Passed) |
| **Observation Whitelist**| 8 attribute delivery tests | `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\verify_treatment_delivery_e2e.py` | `0` (8/8 Passed) |
| **Variant Differences** | 4 HTML diff verifications | `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\verify_variant_diffs.py` | `0` (4/4 Passed) |
| **Statistical Analysis** | 11 analysis & literature tests | `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\test_analyze_v3_results.py` | `0` (11/11 Passed in ~0.4s) |
| **Power Recomputation** | Exact Fisher & RCBD simulation| `C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\recompute_power_rcbd.py` | `0` (4/4 Scenarios Evaluated) |

---

## 5. Instructions for Live Confirmatory Trials (Post-Sign-Off Only)

> [!CAUTION]
> **DO NOT EXECUTE WITHOUT SUPERVISOR APPROVAL & PAID API KEY.**  
> Running without paid quota will trigger the 500 RPD free-tier wall at ~105 runs, repeating the historical abort.

When authorized:
1. Set the private Google API key in PowerShell:
   ```powershell
   $env:GOOGLE_API_KEY = "your-verified-paid-gemini-api-key"
   ```
2. Manually unlock the safety gate in [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) line 258:
   ```python
   SAFETY_GATE_LOCKED = False
   ```
3. Execute the 96-trial runner:
   ```powershell
   C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\protocol_v3_runner.py
   ```
4. Analyze the empirical output:
   ```powershell
   C:\testing\.venv311\Scripts\python.exe C:\testing\research_execution_20261018\analyze_v3_results.py --input-csv C:\testing\research_execution_20261018\results\live_confirmatory_runs.csv --output-dir C:\testing\research_execution_20261018\results\empirical_confirmatory\
   ```

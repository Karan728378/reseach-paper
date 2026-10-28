# REPRODUCIBILITY GUIDE: RESEARCH PROTOCOL V4 & FORENSIC AUDIT SUITE

**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9)  
**Safety Protocol:** 100% Offline Execution · Zero Live Model/API Calls · Quota Ledger Preserved  
**Last Verified:** 2026-10-25  

---

## 1. System Requirements & Environment

The research environment is fully configured on Windows with local headless Chromium execution and 100% offline verification capabilities:

- **Operating System:** Windows 10/11 (64-bit) or Linux (Ubuntu 22.04+)
- **Python Environment:** Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`)
- **Key Installed Packages:**
  - `browser-use 0.13.10` (connects to Chromium via Chrome DevTools Protocol `cdp-use`)
  - `langchain-core==1.6.5` / `langchain-google-genai==4.4.0`
  - `pydantic==2.13.5`
  - Standard library mathematical and statistical routines (zero external scientific library dependencies for core statistical tests)
- **Local Web Server:** Serves website variants at `http://127.0.0.1:8094` or via static file fixtures.

---

## 2. Complete Offline Test Suite Execution (138 Tests)

Every component of the experimental harness, verifier battery, pipeline transformations, quota safety mechanisms, and forensic regressions is covered by **138 automated tests**:

```powershell
C:\testing\.venv311\Scripts\python.exe -m unittest discover -s . -p "test_*.py" -v
```

### Verified Test Suite Breakdown (21 Test Files, 138 Tests)

| Test Module | Test Count | Focus Area & Verified Invariant | Status |
| :--- | :---: | :--- | :---: |
| `test_forensic_audit_regressions.py` | 12 | TOST bounds ($360, 429, 468$), Newcombe CI ($[0.172, 0.456]$), Wilson CIs, 44-row ledger provenance, 10–50px geometry boundaries, and citation resolution. | **PASS** |
| `test_power_audit.py` | 7 | Mathematical derivations for TOST sample size, binomial superiority, and clustering design effects ($\text{DEFF} = 1.30$). | **PASS** |
| `test_treatment_leakage_and_integrity.py` | 6 | Verifies button `aria-label="Add item to cart"` (no product title leakage), clean baseline, and `use_vision=False` enforcement. | **PASS** |
| `test_budget_controls.py` | 7 | Model pricing validation, worst-case headroom calculation, conservative token fallback. | **PASS** |
| `test_budget_guard_repairs.py` | 6 | Exact 600-request boundary, worst-case headroom enforcement, concurrent thread safety, historical 604 fail-closed. | **PASS** |
| `test_runner_guard_integration.py` | 5 | End-to-end runner wrapping in `BudgetGuardedChatModel`, in-flight quota abortion, historical ledger blocking. | **PASS** |
| `test_verifier_ground_truth_battery.py` | 13 | Deterministic CDP verifiers for T1–T6: exact SKU matching, cart count preconditions, order confirmation. | **PASS** |
| `test_t6_verifier_isolated.py` | 7 | Grounded refusal recognition vs. hallucinated warranty duration scoring. | **PASS** |
| `test_analyze_v3_results.py` | 11 | Cochran-Mantel-Haenszel (CMH) and Newcombe score CIs verified against published clinical benchmarks. | **PASS** |
| `test_observation_pipeline_stages.py` | 5 | Pruning of `<script>` and `<meta>` via `DISABLED_ELEMENTS`, non-interactive container tag stripping. | **PASS** |
| `test_accessibility_tree_comparison.py` | 10 | Chromium Blink AXTree node counts (336) and 27/34 selector map correspondence on `#home`. | **PASS** |
| `test_agent_prompt_pipeline.py` | 5 | Interception of model context prompts across website variants verifying token presence/absence. | **PASS** |
| `test_sentinel_pipeline.py` | 4 | Multi-stage trace of sentinel DOM elements through Blink and serializer. | **PASS** |
| `test_aria_baseline_prompt_divergence.py` | 4 | Prompt text buffer divergence between baseline and semantic arms. | **PASS** |
| `test_baseline_pooling_consistency.py` | 4 | Statistical stability and non-pooling invariant across control conditions. | **PASS** |
| `test_browser_lifecycle_and_recovery.py` | 16 | Headless browser session crash recovery, target disposal, and context isolation. | **PASS** |
| `test_mutation_audit.py` | 6 | Intentional fault injection testing of verifiers, safety gates, and statistical estimators. | **PASS** |
| Other test modules | 7 | Single smoke dry-runs, schedule validity, and instrumentation offline checks. | **PASS** |
| **Total Test Battery** | **138 Tests** | **Execution Duration: ~14.3 seconds · Exit Code: 0** | **100% OK** |

---

## 3. Independent Reproduction of Central Claims

Each core scientific claim can be independently reproduced using dedicated standalone scripts:

### 3.1 Metadata Reachability Trace (Table 1 in Manuscript)
```powershell
C:\testing\.venv311\Scripts\python.exe audit_metadata_reachability.py
```
- **Output:** Generates `serialization_audit_metrics.json`.
- **Verified Findings:**
  - `DISABLED_ELEMENTS`: `<script>` and `<meta>` unconditionally pruned (0% reachability for Schema.org JSON-LD).
  - Tag Stripping: Non-interactive `<span>` and `<div>` tags discarded; parent ARIA attributes dropped.
  - Whitelist: Custom `data-*` attributes omitted by default; delivered on interactive elements only when `include_attributes` is explicitly extended.

### 3.2 Chromium Blink AXTree vs. Serializer Correspondence (Section 4.2)
```powershell
C:\testing\.venv311\Scripts\python.exe compare_accessibility_tree.py
```
- **Output:** Generates `accessibility_tree_comparison.json`.
- **Verified Findings:** On route `#home`, exactly 27 of 34 interactive elements ($79.4\%$) match native Blink accessibility nodes. The 7 unmatched elements are "In Stock" badges measuring $48.625 \times 15.0$px triggered by the icon heuristic. Wilson 95% Score Confidence Interval is $[63.2\%, 89.7\%]$.

### 3.3 Statistical Derivations & Monte Carlo Power (Section 6)
```powershell
C:\testing\.venv311\Scripts\python.exe reproduce_power_audit.py
```
- **Output:** Generates `power_audit_results.json`.
- **Verified Findings:**
  - RCBD Monte Carlo simulation ($B=2,000$ iterations, seed 42): Stratified CMH power is $10.85\%$ at $\Delta = 0.20$ and $49.60\%$ at $\Delta = 0.35$ ($\alpha = 0.0167$).
  - Closed-form TOST sample size: $n = 359.8 \approx 360$ trials/arm at $p=0.70$; $n = 428.3 \approx 429$ at $p=0.50$.
  - Design effect adjustment ($\rho = 0.10, m = 4 \implies \text{DEFF} = 1.30$): $n = 360 \times 1.30 = 468$ trials/arm ($N = 1,872$ across 4 arms).

### 3.4 Forensic Regression Verification
```powershell
C:\testing\.venv311\Scripts\python.exe -m unittest test_forensic_audit_regressions.py -v
```
- **Output:** Evaluates 12 assertions across statistical bounds, 44-row ledger provenance, 10–50px geometry thresholds, and BibTeX resolution.

---

## 4. Quota Safeguards & Experiment Halt Mechanism

The research codebase includes a fail-closed local budget guard (`budget_controller.py`) that strictly prohibits unapproved live API calls:
- **Ledger Path:** `results/daily_quota_ledger.json`
- **Halt State:** `halted_due_to_ceiling: true`
- **Current Cumulative Requests:** 604 requests (exceeds max ceiling of 600 requests)
- **Spend Limit:** $\$0.00$ USD ceiling
- **Safety Directive:** Any attempt to invoke `run_single_live_trial` without explicit human authorization aborts with a `QuotaCeilingExceeded` exception.

---

## 5. Epistemic Status of Research Claims

To ensure complete scientific transparency, all project claims are classified into four distinct evidentiary tiers:
1. **Verified Facts:** Static AST code properties in `browser-use 0.13.10`, runtime bounding box measurements ($48.625$px vs $74.766$px), 41 completed cloud pilot trials (100% ceiling), and 3 transient 503 errors on Run 26.
2. **Offline Simulations:** Monte Carlo power calculations ($10.8\%$, $49.6\%$, $98.6\%$) and TOST equivalence curves.
3. **Exploratory Observational Data:** 5 local Qwen trials documenting consumer GPU memory saturation and watchdog cancellations.
4. **Unexecuted Proposals:** Protocol v4 RCBD confirmatory behavioral trials ($N=1,440$ to $1,872$ runs).

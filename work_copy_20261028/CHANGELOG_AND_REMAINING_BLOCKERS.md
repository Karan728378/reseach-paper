# Changelog and Remaining Blockers

**Document Version:** 2.0 (Master Audit & Protocol Freeze Update)  
**Date:** October 21, 2026  
**Auditor / Engineer:** Antigravity Scientific Methodology & Protocol Architecture Team  
**Compliance Status:** 100% Offline · Zero Live LLM API Calls · Zero Cost Incurred · Safety Gate Intact  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Summary of Changes & Audit Rectifications

This update incorporates the comprehensive master audit, independent statistical validation, and protocol freeze deliverables:

1. **Independent Statistical Power & Sample Size Derivations:**  
   Created reproducible calculation script [`reproduce_power_audit.py`](file:///C:/testing/research_execution_20261018/reproduce_power_audit.py), machine-readable output [`power_audit_results.json`](file:///C:/testing/research_execution_20261018/power_audit_results.json), and unit test suite [`test_power_audit.py`](file:///C:/testing/research_execution_20261018/test_power_audit.py) (7/7 PASS).
   - Confirmed reported $10.85\%$ power for $\Delta = 0.20$ and $5.80\%$ power for $\Delta = 0.15$ under the $N = 96$ design ($n = 20$ primary trials per arm, pooled baseline $n = 40$, Bonferroni $\alpha = 0.0167$).
   - Reconciled sample size discrepancies: $N = 96$ (full 6-task RCBD schedule), $N = 80$ (primary 5-task grounded benchmark), $n = 20$ (per-arm primary count), $n = 24$ (per-arm schedule count), and $n = 40$ (pooled baseline).
   - Documented mandatory non-equivalence rule: non-significant findings at $N = 96$ cannot support channel equivalence.
2. **De-confounding Action Button ARIA Labels:**  
   Refactored action buttons in [`shared/app-core.js`](file:///C:/testing/shared/app-core.js) from `"Add " + product.name + " to cart"` to generic semantic labels (`"Add item to cart"`, `"Item quantity"`, `"Remove item from cart"`). New SHA-256: `ccae98e0218402bd78f7c4548ca743fde79b89b4baee466447b72821621b80c7`.
3. **Dynamic Accessibility Report Generation & Heuristic Isolation:**  
   Replaced static percentage literals and hardcoded markdown tables in [`compare_accessibility_tree.py`](file:///C:/testing/research_execution_20261018/compare_accessibility_tree.py) with dynamic generation driven directly by the measured JSON dictionary. Replaced hardcoded timestamp with dynamic UTC ISO formatting. Styled `#price-span` with `min-width: 80px` in [`fixtures/edge_cases.html`](file:///C:/testing/research_execution_20261018/fixtures/edge_cases.html) to eliminate the false-positive icon heuristic classification. Added `#icon-span` (`🎧`) to isolate and explicitly verify the icon detection heuristic.
4. **Improved Node-Level Correspondence:**  
   Implemented `compute_node_correspondence()` pairing Chromium Blink's `backendDOMNodeId` from CDP `Accessibility.getFullAXTree` with `DOMElementNode.backend_node_id` in `browser-use`'s `selector_map`. Documented that 27 of 34 interactive elements match 1-to-1, while explicitly retaining and documenting the persistent limitation for non-interactive nodes.
5. **Identification of Task T6 Verifier Contradiction:**  
   Uncovered critical code-vs-protocol divergence in `protocol_v3_runner.py:Line 129` (which rewarded matching `"36 months"` regex rather than Grounded Refusal). Codified strict refusal scoring (`success = bool(refusal and not hallucination)`) in Protocol v4 Draft.
6. **Master Audit Deliverables Created:**  
   Delivered formal audit reports covering statistical power, treatment validity, verifier rigor, observation pipelines, historical data provenance, cost analysis, and draft protocol freeze.

---

## 2. Master Deliverables Directory

| Deliverable | File Path | Scope & Purpose |
|---|---|---|
| **Statistical Power Audit** | [`STATISTICAL_POWER_AUDIT.md`](file:///C:/testing/research_execution_20261018/STATISTICAL_POWER_AUDIT.md) | Independent mathematical verification of $10.85\%$ power, design total reconciliation, superiority and TOST sizing derivations. |
| **Power Calculation Script** | [`reproduce_power_audit.py`](file:///C:/testing/research_execution_20261018/reproduce_power_audit.py) | Reproducible Python 3 script executing exact binomial tests, Monte Carlo RCBD simulation ($B=2,000$), DEFF clustering, and TOST sizing. |
| **Power Calculation JSON** | [`power_audit_results.json`](file:///C:/testing/research_execution_20261018/power_audit_results.json) | Machine-readable validation output containing all verified parameters and sample sizes. |
| **Power Audit Test Suite** | [`test_power_audit.py`](file:///C:/testing/research_execution_20261018/test_power_audit.py) | Unit tests (7/7 PASS) validating mathematical properties, monotonicity, and schema. |
| **Treatment Validity Audit** | [`TREATMENT_VALIDITY_AUDIT.md`](file:///C:/testing/research_execution_20261018/TREATMENT_VALIDITY_AUDIT.md) | Treatment-equivalence matrix, AST diffs, verification of de-confounded action labels, and leakage audit. |
| **Verifier & Retry Audit** | [`VERIFIER_AND_RETRY_AUDIT.md`](file:///C:/testing/research_execution_20261018/VERIFIER_AND_RETRY_AUDIT.md) | Audit of exact SKU verification, zero credit for T4, pre-state checks for T5, T6 contradiction resolution, and retry survivorship elimination. |
| **Observation Pipeline Matrix** | [`OBSERVATION_PIPELINE_EVIDENCE_MATRIX.md`](file:///C:/testing/research_execution_20261018/OBSERVATION_PIPELINE_EVIDENCE_MATRIX.md) | 5-stage architectural matrix (HTML $\to$ AXTree $\to$ Serializer $\to$ Prompt $\to$ Vision), Blink node correspondence (27/34), non-interactive limitations. |
| **Data Provenance Audit** | [`DATA_PROVENANCE_AND_HISTORICAL_VALIDITY.md`](file:///C:/testing/research_execution_20261018/DATA_PROVENANCE_AND_HISTORICAL_VALIDITY.md) | Forensic provenance of historical CSVs (`pilot-summary-clean.csv`, `full-summary.csv`), SHA-256 preservation, and classification as exploratory-only. |
| **Protocol v4 Draft** | [`PROTOCOL_V4_DRAFT.md`](file:///C:/testing/research_execution_20261018/PROTOCOL_V4_DRAFT.md) | 25-point formal specification for future experimental execution, contrasting exploratory pilot ($N=96$) and confirmatory study ($N=480$). |
| **Protocol v4 Config** | [`protocol_v4_config.json`](file:///C:/testing/research_execution_20261018/protocol_v4_config.json) | Machine-readable configuration file for Protocol v4 execution. |
| **Protocol Freeze Checklist** | [`PROTOCOL_FREEZE_CHECKLIST.md`](file:///C:/testing/research_execution_20261018/PROTOCOL_FREEZE_CHECKLIST.md) | Step-by-step verification checklist required before unfreezing experimental execution. |
| **Cost & Readiness Audit** | [`EXPERIMENT_COST_AND_READINESS.md`](file:///C:/testing/research_execution_20261018/EXPERIMENT_COST_AND_READINESS.md) | Empirical token counting, Gemini Flash Lite pricing model, pilot vs confirmatory cost projections, hard spending ceiling ($\le \$10.00$). |
| **Final Readiness Report** | [`FINAL_RESEARCH_READINESS_REPORT.md`](file:///C:/testing/research_execution_20261018/FINAL_RESEARCH_READINESS_REPORT.md) | Executive summary, verified findings vs inherited claims, offline test results, blocker priorities, and NO-GO/GO recommendations. |

---

## 3. Exact Tests Executed and Outcomes

All test suites were executed offline in `C:\testing` using Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`):

```
====================================================================================================
TEST EXECUTION SUMMARY (100% PASSING · ZERO LIVE API CALLS)
====================================================================================================
1. offline_test_suite.py:
   Command:   C:\testing\.venv311\Scripts\python.exe research_execution_20261018\offline_test_suite.py
   Exit Code: 0
   Result:    12/12 PASSED (1.5s)
   Scope:     Serializer pruning, attribute whitelists, T3/T4/T5/T6 verifiers, RCBD balance,
              tracked file SHA-256 integrity, comparison artifact schema.

2. test_accessibility_tree_comparison.py:
   Command:   C:\testing\.venv311\Scripts\python.exe -m unittest research_execution_20261018/test_accessibility_tree_comparison.py
   Exit Code: 0
   Result:    10/10 PASSED (0.002s)
   Scope:     Tooling metadata, 5 semantic channels, edge case fixture findings,
              node correspondence (27/34 paired), Markdown report integrity.

3. test_power_audit.py:
   Command:   C:\testing\.venv311\Scripts\python.exe -m unittest research_execution_20261018/test_power_audit.py
   Exit Code: 0
   Result:    7/7 PASSED (0.001s)
   Scope:     Mathematical inverses, zero-delta alpha, monotonicity, superiority bounds,
              TOST bounds, DEFF clustering, JSON schema validation.

4. test_analyze_v3_results.py:
   Command:   C:\testing\.venv311\Scripts\python.exe -m unittest research_execution_20261018/test_analyze_v3_results.py
   Exit Code: 0
   Result:    11/11 PASSED (0.333s)
   Scope:     CMH odds ratios, Agresti multicenter reference validation, synthetic datasets 1–7,
              drift detection.

5. verify_treatment_delivery_e2e.py:
   Command:   C:\testing\.venv311\Scripts\python.exe research_execution_20261018/verify_treatment_delivery_e2e.py
   Exit Code: 0
   Result:    8/8 PASSED (~14.1s)
   Scope:     Live Chromium CDP observation delivery: v0 visible text, v2 de-confounded button ARIA,
              v2 non-interactive ARIA omission, v3 default vs extended data-*, v1 JSON-LD pruning.

6. test_agent_prompt_pipeline.py:
   Command:   C:\testing\.venv311\Scripts\python.exe research_execution_20261018/test_agent_prompt_pipeline.py
   Exit Code: 0
   Result:    5/5 PASSED (~18.5s)
   Scope:     Real browser-use Agent observation-building and prompt generation with local MockChatModel:
              confirmed prompt buffer contents across all 4 variants with zero API credit spend.
====================================================================================================
```

---

## 4. Tracked File SHA-256 Hashes

| File Path | SHA-256 Hash | Status / Audit Notes |
|---|---|---|
| `results\pilot-summary-clean.csv` | `82ae25ded8480c7b7804dd3dfbf53d03a6d46c2ecc96c8939e2044cc9c729b9c` | **UNTOUCHED / PRESERVED** |
| `results\main_experiment\full-summary.csv` | `42e9856ae932d56e5d8c766b2fd37bdced4088e6e7e4d0a4d85ecc7244365621` | **UNTOUCHED / PRESERVED** |
| `shared\products.js` | `b182ac6bdb6704f2c56f3718de41262aa2e9689ac2e965cae256ae1ae9278c11` | **UNTOUCHED / PRESERVED** |
| `shared\app-core.js` | `ccae98e0218402bd78f7c4548ca743fde79b89b4baee466447b72821621b80c7` | **POST-REFACTOR (De-confounded)** |
| `tasks\task-definitions.json` | `e61408a8a82192824c1c4b4b6a35ac47e0b36dd9b06025d865e3e435b2231e5f` | **UNTOUCHED / PRESERVED** |
| `runner\agent-runner.py` | `8a4af77a540b9cff2feba65022dfee98c43ad9210f4d8f06a809e3f9a5094dfc` | **UNTOUCHED / PRESERVED** |
| `runner\verifier.py` | `890b968345e82b59cb0545263d8e438a6ef6de9f521b90da5b98e5680850b378` | **UNTOUCHED / PRESERVED** |
| `variants\v0-baseline\index.html` | `aa042e92caaab5ceac20a04552e18e182ab4f5812e54b6d28a6899fce3df43ae` | **UNTOUCHED / PRESERVED** |
| `variants\v2-aria\index.html` | `e5e303ab0c6de3108258fcf4603192b539784af747e8c35f1073182dc097a612` | **UNTOUCHED / PRESERVED** |
| `variants\v3-data-attrs\index.html` | `4db1305a1bc4623499f82a863148602f39e5db8dd9922f8f5eee71229b39df4d` | **UNTOUCHED / PRESERVED** |

---

## 5. Prioritized Remaining Blockers

The following items are required before any live experimental execution can be initiated:

| Priority | Blocker Description | Required Action | Responsibility |
|:---:|---|---|:---:|
| **P1** | **Decision on Study Scope:** Choosing between Exploratory Pilot ($N=96$, power $<11\%$) vs Confirmatory Study ($N=480$, power $80\%$). | Human researcher must select scope based on scientific objective. | **Human Decision Required** |
| **P2** | **Task T6 Code Alignment:** `protocol_v3_runner.py:129` must be updated to align with refusal probe logic (`success = bool(refusal and not hallucination)`). | Patch runner script prior to execution. | Engineering Team |
| **P3** | **API Tier & Billing Allocation:** Free-tier API keys hit the 500 RPD ceiling. Paid project billing must be enabled. | Human researcher must configure pre-paid API credentials. | **Human Decision Required** |
| **P4** | **Safety Gate Authorization:** `--live` and `--confirm-live-execution` must remain locked until P1–P3 are approved. | Maintain safety lock. | Automated Safety Gate |

---

## 6. Execution Status & Stop Condition

All offline code inspections, independent statistical derivations, treatment de-confounding, offline test executions, and protocol freeze documentation are complete.

- Zero live LLM API calls were made.
- Zero API credits were spent.
- The live execution safety gate remains locked.
- Work has stopped to await human researcher review and decision.

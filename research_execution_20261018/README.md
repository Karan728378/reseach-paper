# Autonomous Browser Agent Additive Semantic Markup Study

**Research Workspace:** `C:\testing\research_execution_20261018`  
**Execution Environment:** Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`)  
**Project Status:** **SYSTEMS AUDIT COMPLETE — READY AFTER EXTERNAL COMPILATION**  
**Safety Gate:** **LOCKED** (Zero Live Model Calls, Zero Paid API Costs)  

---

## Quick Start: Safe Offline Preflight & Diagnostics

To execute the offline preflight routine and test local server reachability, Chromium CDP, and verifiers without paid API calls:

```powershell
# 1. Preflight check for full 96-trial study:
C:\testing\.venv311\Scripts\python.exe research_execution_20261018/protocol_v3_runner.py --preflight

# 2. Preflight check for 4-trial smoke test batch:
C:\testing\.venv311\Scripts\python.exe research_execution_20261018/protocol_v3_runner.py --smoke --preflight

# 3. Master offline audit suite (13/13 passing):
C:\testing\.venv311\Scripts\python.exe research_execution_20261018/offline_test_suite.py
```

- **Interactive Results Dashboard:** [`results/dashboard.html`](file:///C:/testing/research_execution_20261018/results/dashboard.html)
- **Execution Readiness Report:** [`NEXT_LIVE_EXECUTION_READINESS.md`](file:///C:/testing/NEXT_LIVE_EXECUTION_READINESS.md)
- **Reproducibility Guide:** [`REPRODUCIBILITY_GUIDE.md`](file:///C:/testing/research_execution_20261018/REPRODUCIBILITY_GUIDE.md)

---

## Project Overview

This study investigates whether adding structured semantic markup (WAI-ARIA or configured `data-*` attributes) improves an autonomous text-based browser agent's task accuracy and speed when the underlying visible text content is already present and identical.

### Key Architectural Discoveries & Evidence
1. **DOM Serializer Script Pruning:** Standard `browser-use 0.13.10` strips `<script type="application/ld+json">` tags unconditionally (`DISABLED_ELEMENTS`). JSON-LD structured data never enters the LLM prompt.
2. **Attribute Whitelist Filtering:** Custom `data-*` attributes are stripped by default unless an extended attribute whitelist (`EXTENDED_ATTRIBUTES`) is supplied to the runner.
3. **Flaw-Free Verification Suite:** Resolved historical verifier bugs:
   - T1: SoundFlow Air 3 (`wh-001`, $49.99, cheapest).
   - T2: Mechanical Keyboard Pro (`mkp-001`).
   - T3: BudPro Wireless X (`wh-002`, 4.5 rating, second-highest).
   - T4: ErgoGlide Mouse (`mse-001`) with confirmed order state.
   - T5: Cart mutation strictly asserts `pre_cart_count == 1` before checking empty cart.
   - T6: Grounded refusal verifier rewards grounded refusal (1.0) and rejects duration hallucinations (0.0).

---

## Core Documentation Map

| Document | File Path | Focus Area |
| :--- | :--- | :--- |
| **Live Execution Readiness** | [`NEXT_LIVE_EXECUTION_READINESS.md`](file:///C:/testing/NEXT_LIVE_EXECUTION_READINESS.md) | Preflight results, safety interlocks, future smoke command |
| **Reproducibility Guide** | [`REPRODUCIBILITY_GUIDE.md`](file:///C:/testing/research_execution_20261018/REPRODUCIBILITY_GUIDE.md) | Exact commands and system requirements |
| **Scientific Methodology Audit**| [`METHODOLOGY_AUDIT.md`](file:///C:/testing/research_execution_20261018/METHODOLOGY_AUDIT.md) | Construct validity, treatments, power bounds |
| **Data Provenance Audit** | [`DATA_PROVENANCE_AUDIT.md`](file:///C:/testing/research_execution_20261018/DATA_PROVENANCE_AUDIT.md) | Forensic reconciliation of all 8 datasets |
| **Experiment Reconciliation** | [`EXPERIMENT_RECONCILIATION.md`](file:///C:/testing/research_execution_20261018/EXPERIMENT_RECONCILIATION.md) | Analysis of Exp 1, Exp 1b, and Protocol v4 |
| **Empirical Results Status** | [`EMPIRICAL_RESULTS_STATUS.md`](file:///C:/testing/research_execution_20261018/EMPIRICAL_RESULTS_STATUS.md) | Formal declaration of pending live trials |
| **Accessibility Tree Comparison**| [`ACCESSIBILITY_TREE_COMPARISON.md`](file:///C:/testing/research_execution_20261018/ACCESSIBILITY_TREE_COMPARISON.md) | Chromium Blink AXTree vs serialized DOM comparison |
| **Working Research Paper** | [`RESEARCH_PAPER_DRAFT.md`](file:///C:/testing/research_execution_20261018/RESEARCH_PAPER_DRAFT.md) | Academic draft with documented limitations |

---

## Offline Automated Test Results

Full test discovery (`python -m unittest discover -s . -p "test_*.py"`) across all 19 `test_*.py` modules in the workspace yields **138 tests, 0 failures, 0 errors (OK)** in ~13.5s (verified 2026-10-26). Selected module breakdown:
- `offline_test_suite.py` (composite integration harness): **13 / 13 PASS** (hash match on protected files, verifiers, attributes)
- `test_mutation_audit.py`: **6 / 6 PASS** (verification assertions detect deliberate defects)
- `test_t6_verifier_isolated.py`: **7 / 7 PASS** (grounded refusal vs hallucination logic)
- `test_power_audit.py`: **7 / 7 PASS** (binomial power, TOST equivalence bounds, DEFF clustering)
- `test_analyze_v3_results.py`: **11 / 11 PASS** (validated against Agresti 2002 & Newcombe 1998)
- `test_accessibility_tree_comparison.py`: **10 / 10 PASS** (Blink AXTree correspondence)
- `test_agent_prompt_pipeline.py`: **5 / 5 PASS** (prompt token delivery via `MockChatModel`)
- Additional modules (browser lifecycle, implementation fixes, forensic regressions, etc.): remaining tests

**Note:** The 13 composite `offline_test_suite.py` integration checks are counted separately and are not double-counted in the 138 unique unit/regression tests from `unittest discover`.

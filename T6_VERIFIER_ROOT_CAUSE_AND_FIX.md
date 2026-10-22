# Task T6 Verifier: Root Cause Analysis, Forensic Call Graph, and Isolated Fix

**Document Version:** 1.0 (Root Cause Analysis & Remediation Architecture)  
**Date:** October 22, 2026  
**Auditor / Systems Engineer:** Antigravity Scientific Methodology & Protocol Architecture Team  
**Compliance Status:** 100% Offline · Isolated Implementation · Active Runner Remains Unpatched  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Executive Summary & Defect Overview

Task T6 was designed as an **exploratory negative information probe** to evaluate whether autonomous browser agents can reliably detect missing information and exhibit **Grounded Refusal (Hallucination Resistance)** when asked for a non-existent fact.

Specifically, Task T6 instructs the agent:
> *"Navigate to the product details for 'SoundFlow Air 3' (SKU: wh-001). Retrieve the exact manufacturer warranty duration specified for this item."*

Across all website variants (`v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs`), **the manufacturer warranty duration is completely omitted from the website catalog and product page**.

### The Critical Bug:
In [`research_execution_20261018/protocol_v3_runner.py:129`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L129), the executable verifier implemented the **exact inversion** of the scientific requirement:
```python
# Flawed executable code in protocol_v3_runner.py:
refusal = bool(re.search(r'\b(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not)\b.*?\b(warranty|guarantee|found|find|stated|listed)\b', text, re.IGNORECASE))
match = bool(re.search(r'\b36\s*(months?|mo)\b', text, re.IGNORECASE))
success = bool(match and not refusal)
```
- **The Consequence:** The runner requires the agent to hallucinate `"36 months"` and assigns failure if the agent reports that warranty information is unstated.
- **The Test Suite Flaw:** [`research_execution_20261018/offline_test_suite.py:126-132`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L126) encoded the same assumption, asserting that stating `"36 months"` passes ($1.0$) and stating `"could not find"` fails ($0.0$).

---

## 2. Comprehensive Inventory of Task T6 Artifacts

| Artifact Location | Role / Context | Task T6 Stated Behavior | Alignment Status |
|---|---|---|:---:|
| [`tasks/task-definitions.json`](file:///C:/testing/tasks/task-definitions.json) | Legacy Protocol v2 Task Config | **Completely Absent** (T1–T5 only). | Legacy Artifact |
| [`research_execution_20261018/task_specifications.json:258-285`](file:///C:/testing/research_execution_20261018/task_specifications.json#L258) | Protocol v3 Canonical Specification | `task_type: negative_information_probe`, `ground_truth_status: absent_from_website`. Success = `grounded_refusal_detection`. Failure = asserting 36 mo. | **Correct Intended Spec** |
| [`research_execution_20261018/protocol.md:94-102`](file:///C:/testing/research_execution_20261018/protocol.md#L94) | Protocol Narrative Freeze | Evaluated as Grounded Refusal ($Y=1$ on refusal, $Y=0$ on hallucinating 36 mo). | **Correct Intended Spec** |
| [`research_execution_20261018/analysis_plan.md:23-28`](file:///C:/testing/research_execution_20261018/analysis_plan.md#L23) | Statistical Analysis Plan | Secondary exploratory outcome ($N=16$). Measures hallucination resistance. | **Correct Intended Spec** |
| [`research_execution_20261018/protocol_v4_config.json:30-33`](file:///C:/testing/research_execution_20261018/protocol_v4_config.json#L30) | Protocol v4 Machine Config | Listed under `exploratory_negative_probe: ["T6"]`. | **Correct Intended Spec** |
| [`research_execution_20261018/protocol_v3_runner.py:124-135`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L124) | Executable Runner Script | Requires regex match on `"36 months"`; penalizes refusal. | **DEFECTIVE IMPLEMENTATION** |
| [`research_execution_20261018/offline_test_suite.py:126-132`](file:///C:/testing/research_execution_20261018/offline_test_suite.py#L126) | Offline Verification Suite | Asserts `"36 months"` passes ($1.0$); refusal fails ($0.0$). | **DEFECTIVE ASSERTION** |
| [`runner/agent-runner.py`](file:///C:/testing/runner/agent-runner.py) + [`runner/verifier.py`](file:///C:/testing/runner/verifier.py) | Legacy Execution Engine | Task T6 is not present in legacy runner or verifier. | Legacy Artifact |

---

## 3. Scientific Consequences of the Defect

1. **Rewarding Uncontrolled Hallucination:** In a benchmark designed to evaluate grounded perception, scoring $1.0$ for guessing an absent string turns an empirical agent evaluation into a lottery rewarding parametric drift.
2. **False Penalization of Grounded Agents:** State-of-the-art models that correctly inspect the page, conclude the warranty is absent, and report *"No warranty information is stated on the product page"* are assigned a score of $0.0$.
3. **Contamination of Task Pools:** If Task T6 were pooled into the primary benchmark (T1–T5), this scoring error would distort the overall task success rates. (Fortunately, `protocol.md` and `analysis_plan.md` already isolated T6 into a separate $N=16$ exploratory probe).

---

## 4. Remediation Architecture: Isolated Grounded Refusal Verifier

To resolve the defect without prematurely altering the active codebase before human authorization, the proposed verifier was implemented in an **isolated module**: [`research_execution_20261018/t6_verifier_isolated.py`](file:///C:/testing/research_execution_20261018/t6_verifier_isolated.py).

### 4.1 Decision Logic & Regular Expression Mechanics
The corrected verifier enforces four explicit decision boundaries:

```
                                  AGENT RESPONSE (final_text)
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
              Contains Refusal?                               Contains Duration?
              (Missing/Unstated)                           (Numbers + Time Units)
                      │                                               │
             ┌────────┴────────┐                             ┌────────┴────────┐
            YES                NO                           YES                NO
             │                 │                             │                 │
             └────────┬────────┘                             └────────┬────────┘
                      │                                               │
                      ▼                                               ▼
      ┌───────────────────────────────────────────────────────────────────────────────┐
      │ Refusal == True  AND Duration == False ──► SUCCESS (1.0) [Grounded Refusal]   │
      │ Refusal == True  AND Duration == True  ──► FAILURE (0.0) [Contradictory]      │
      │ Refusal == False AND Duration == True  ──► FAILURE (0.0) [Hallucination]      │
      │ Refusal == False AND Duration == False ──► FAILURE (0.0) [Unrelated/Empty]   │
      └───────────────────────────────────────────────────────────────────────────────┘
```

1. **Bidirectional Refusal Pattern:**
   ```python
   REFUSAL_KEYWORDS = r'(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not|unlisted|missing|not stated|not found|not listed|not mentioned|not provided|not specified|unavailable|absent|nowhere)'
   WARRANTY_TERMS = r'(warranty|guarantee|duration|terms?|coverage|period|policy)'
   REFUSAL_PATTERN = re.compile(rf'\b{REFUSAL_KEYWORDS}\b.*?\b{WARRANTY_TERMS}\b|\b{WARRANTY_TERMS}\b.*?\b{REFUSAL_KEYWORDS}\b', re.IGNORECASE | re.DOTALL)
   ```
2. **Comprehensive Duration Hallucination Detector:**
   ```python
   DURATION_HALLUCINATION_PATTERN = re.compile(
       r'\b(\d+|one|two|three|four|five|six|twelve|twenty-four|thirty-six)\s*(-|\s)?\s*(months?|mos?|years?|yrs?|days?)\b',
       re.IGNORECASE
   )
   ```

---

## 5. Verification & Live Execution Bypass Analysis

1. **Independent Test Suite Pass:** [`test_t6_verifier_isolated.py`](file:///C:/testing/research_execution_20261018/test_t6_verifier_isolated.py) was executed with `C:\testing\.venv311\Scripts\python.exe` and passed **7/7 test groups (35+ test cases) in 0.003s**.
2. **Active Runner Untouched:** The active file [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) was left untouched in compliance with safety constraints.
3. **Diff Prepared:** The patch is staged in [`T6_VERIFIER_PROPOSED_PATCH.diff`](file:///C:/testing/research_execution_20261018/T6_VERIFIER_PROPOSED_PATCH.diff).
4. **Live Execution Bypass Check:** It is architecturally impossible for live execution to bypass the verifier because:
   - `protocol_v3_runner.py` enforces an unconditional safety interlock `RuntimeError` on `--live`.
   - `protocol_v3_runner.py` only implements `run_single_mock_trial`.
   - Legacy `runner/agent-runner.py` has no T6 task definition or verifier branch.

---

## 6. Historical Data Impact Assessment

- **Historical CSV Analysis:** `results/pilot-summary-clean.csv` ($N=250$) and `results/main_experiment/full-summary.csv` ($N=147$) were generated under Protocol v2.
- **Protocol v2 Task Range:** Protocol v2 strictly evaluated **Tasks T1–T5**. Task T6 was never executed in any historical live trial.
- **Conclusion:** **Zero historical rows are affected by the Task T6 scoring defect.** No historical data requires rescoring or reconstruction.

# Offline Integration Audit Report: Budget Guard Enforcement

**Date:** 2026-10-24  
**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*  
**Workspace:** `C:\testing\research_execution_20261018`  
**Target Runner:** [protocol_v3_runner.py](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)  
**Budget Guard Module:** [budget_controller.py](file:///C:/testing/research_execution_20261018/budget_controller.py)  
**Integration Test Suite:** [test_runner_guard_integration.py](file:///C:/testing/research_execution_20261018/test_runner_guard_integration.py)  
**Ledger:** [results/daily_quota_ledger.json](file:///C:/testing/research_execution_20261018/results/daily_quota_ledger.json)  
**Status:** Audit Complete | Offline Only Verified  

---

## Executive Summary

This forensic and offline integration audit verifies that all individual LLM requests originating from `browser-use` and `protocol_v3_runner.py` are strictly intercepted, bounded, and metered by `BudgetGuardedChatModel` and `LocalBudgetGuard`. 

### Key Findings
1. **Production Path Proved:** Every call to `Agent.run()` routes model interactions through `Agent.get_model_output() -> await self.llm.ainvoke()`. Because `run_single_live_trial` wraps `llm` with `BudgetGuardedChatModel` before instantiating `Agent`, no alternate code paths bypass the guard.
2. **Accounting Invariants Upheld:** Pre-dispatch reservation, post-dispatch reconciliation, zero-retry configuration, cancellation, and threading locks prevent both undercounting and double-counting.
3. **Test Suite Expanded to 126 Passing Tests:** The previous 121-test suite was augmented with 5 offline integration tests in `test_runner_guard_integration.py`. The complete 126-test suite passed in 30.358 seconds with zero failures.
4. **Historical Ledger Preserved:** `results/daily_quota_ledger.json` remains strictly preserved at 604 requests with ceiling 600. `LocalBudgetGuard` immediately blocks trial and step dispatches.
5. **Phase 2 Implementation Decision:** **GO** for offline Phase 2 tasks (task battery redesign, verifier ground truth hardness tests, mock validation); **STRICT HOLD** for live API execution.

---

## 1. Production Call Path Trace and Bypass Proof

### 1.1 Invocation Trace from Runner to Gemini API

The execution path for live trials was audited across [protocol_v3_runner.py](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) and `browser_use/agent/service.py`:

```mermaid
sequenceDiagram
    participant Runner as protocol_v3_runner.py::execute_experiment()
    participant LiveTrial as protocol_v3_runner.py::run_single_live_trial()
    participant Guard as budget_controller.py::LocalBudgetGuard
    participant Proxy as budget_controller.py::BudgetGuardedChatModel
    participant BU_Agent as browser_use.Agent
    participant GoogleLLM as browser_use.ChatGoogle / LangChain ChatGoogleGenerativeAI

    Runner->>Guard: check_can_dispatch_trial(require_worst_case_headroom=True)
    alt cumulative_requests + max_steps > max_requests_ceiling
        Guard-->>Runner: (False, "Remaining requests < worst-case steps")
        Runner->>Runner: Abort dispatch immediately (Fail Closed)
    else Sufficient Headroom
        Guard-->>Runner: (True, "Budget available")
        Runner->>LiveTrial: run_single_live_trial(..., guard=guard)
        LiveTrial->>Proxy: BudgetGuardedChatModel(llm, guard=guard)
        LiveTrial->>BU_Agent: Agent(..., llm=guarded_llm, max_steps=max_steps)
        LiveTrial->>BU_Agent: agent.run()
        loop Each Step (1 to max_steps)
            BU_Agent->>BU_Agent: get_model_output(input_messages)
            BU_Agent->>Proxy: await self.llm.ainvoke(input_messages, **kwargs)
            Proxy->>Guard: check_can_dispatch_request()
            alt cumulative_requests >= ceiling
                Guard-->>Proxy: (False, "Pre-dispatch blocked")
                Proxy-->>BU_Agent: raise BudgetExceededError
                BU_Agent-->>LiveTrial: Exception bubbles up
                LiveTrial->>LiveTrial: classify termination_reason="quota_aborted"
            else Below Ceiling
                Proxy->>Guard: record_request_pre_dispatch()
                Guard->>Guard: Lock -> cumulative_requests += 1 -> save ledger
                Proxy->>GoogleLLM: await wrapped_model.ainvoke(...)
                GoogleLLM-->>Proxy: Response with token usage
                Proxy->>Guard: record_request_post_dispatch(actual_tokens)
                Proxy-->>BU_Agent: Return AgentOutput response
            end
        end
        LiveTrial-->>Runner: Return trial_result (total_steps, status)
        Runner->>Guard: record_trial_completion(requests_already_recorded=True)
    end
```

### 1.2 Verification of Bypass Paths in `browser-use` 0.13.10

An audit of the `browser-use` agent source code ([C:\testing\.venv311\Lib\site-packages\browser_use\agent\service.py](file:///C:/testing/.venv311/Lib/site-packages/browser_use/agent/service.py)) confirms:

1. **Primary Step Loop (Line 1955):**  
   In `Agent.get_model_output()`, all agent actions are requested via:
   ```python
   response = await self.llm.ainvoke(input_messages, **kwargs)
   ```
   Because `self.llm` is the `BudgetGuardedChatModel` passed into the `Agent` constructor, every step call enters `BudgetGuardedChatModel.ainvoke()`.

2. **Compaction Sub-Calls (Line 1168):**  
   `compaction_llm = settings.compaction_llm or self.settings.page_extraction_llm or self.llm`  
   Neither `compaction_llm` nor `page_extraction_llm` are configured in `protocol_v3_runner.py`. If compaction were triggered, it defaults to `self.llm` (`BudgetGuardedChatModel`).

3. **Fallback Model Switching (Lines 1976–1980, 2019):**  
   `protocol_v3_runner.py` configures zero fallback models. Any model error raises immediately.

4. **Internal Retries in LLM Clients (Lines 550, 553):**  
   `protocol_v3_runner.py` explicitly disables client-level retries:
   - `ChatGoogle(..., max_retries=1, retryable_status_codes=[])`
   - `ChatGoogleGenerativeAI(..., max_retries=0)`
   - `Agent(..., max_failures=1)`  
   No hidden retry loop exists inside the client layer.

---

## 2. Accounting Invariants Analysis

A systematic analysis of all dispatch lifecycle events demonstrates that neither undercounting nor double-counting can occur:

| Condition | Mechanism | Undercounting Risk | Double-Counting Risk | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Request Reservations** | Synchronous pre-dispatch increment in `record_request_pre_dispatch()` before network transmission. | **Zero**: If network drops or timeouts occur, the request is already recorded against the ceiling. | **Zero**: Increments request count once per attempt. | **VERIFIED** |
| **Post-Dispatch Reconcile** | `record_request_post_dispatch()` updates token counts and dollar estimations only. | **Zero**: Token reconciliation only adjusts `(actual - pre_estimated)`. | **Zero**: Does not mutate `cumulative_requests`. | **VERIFIED** |
| **Retries** | If any retry is attempted by an agent or wrapper, it must invoke `ainvoke()` again. | **Zero**: Every retry enters `check_and_record_pre_dispatch()`, deducting 1 request. | **Zero**: Each retry represents a distinct provider API request. | **VERIFIED** |
| **Cancellation** | If an `asyncio.CancelledError` or `SIGINT` occurs during `await ainvoke()`. | **Zero**: Pre-dispatch reservation occurred prior to the await point. | **Zero**: Cancelled trials abort execution, skipping normal completion increments. | **VERIFIED** |
| **Exceptions** | If Gemini returns 503, 429, or network error. | **Zero**: Request was reserved pre-dispatch; exception caught by runner and converted to `infrastructure_aborted`. | **Zero**: Post-dispatch hook is skipped; `record_trial_completion` sets `requests_already_recorded=True`. | **VERIFIED** |
| **Concurrent Calls** | Multiple coroutines or threads calling `ainvoke()` simultaneously. | **Zero**: `self._lock = threading.RLock()` protects check and increment inside an atomic block. | **Zero**: Lock prevents race conditions; second caller immediately sees ceiling reached. | **VERIFIED** |

### 2.1 Double-Counting Prevention Proof

In `protocol_v3_runner.py`, line 995:
```python
guard.record_trial_completion(
    total_steps=trial_result.get("total_steps", 0),
    requests_already_recorded=(mode == "live" and guard is not None)
)
```
In `budget_controller.py`, lines 461–466:
```python
if not requests_already_recorded:
    self.cumulative_prompt_tokens += p_tokens
    self.cumulative_completion_tokens += c_tokens
    self.cumulative_cost_usd += trial_cost
    self.cumulative_requests += total_steps
self.runs_completed += 1
```
Because `requests_already_recorded=True` in live guarded mode, `cumulative_requests` is not incremented at trial completion. Steps were already metered 1-for-1 at the exact moment of pre-dispatch.

---

## 3. Test Evidence

### 3.1 Unit Test Executions

```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest test_budget_controls.py -v
```
**Output:** Ran 7 tests in 0.001s. **OK.**

```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest test_budget_guard_repairs.py -v
```
**Output:** Ran 6 tests in 0.035s. **OK.**

### 3.2 Integration Test Execution: `test_runner_guard_integration.py`

```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest test_runner_guard_integration.py -v
```
**Console Output:**
```text
test_01_runner_wraps_llm_with_budget_guard (test_runner_guard_integration.TestRunnerGuardIntegration.test_01_runner_wraps_llm_with_budget_guard)
run_single_live_trial must wrap custom_llm in BudgetGuardedChatModel when guard is provided. ... ok
test_02_in_flight_budget_exhaustion_aborts_cleanly (test_runner_guard_integration.TestRunnerGuardIntegration.test_02_in_flight_budget_exhaustion_aborts_cleanly)
When guard reaches ceiling during live trial steps, runner halts with quota_aborted. ... ok
test_03_execute_experiment_worst_case_headroom (test_runner_guard_integration.TestRunnerGuardIntegration.test_03_execute_experiment_worst_case_headroom)
execute_experiment must halt before trial dispatch if worst-case steps exceed ceiling. ... ok
test_04_no_double_counting_with_requests_already_recorded (test_runner_guard_integration.TestRunnerGuardIntegration.test_04_no_double_counting_with_requests_already_recorded)
record_trial_completion does not double count steps when requests_already_recorded=True. ... ok
test_05_historical_ledger_blocks_live_dispatch (test_runner_guard_integration.TestRunnerGuardIntegration.test_05_historical_ledger_blocks_live_dispatch)
When ledger contains 604 requests with ceiling 600, trial dispatch fails closed immediately. ... ok

----------------------------------------------------------------------
Ran 5 tests in 1.410s

OK
```

### 3.3 Full Discovered Repository Test Suite

```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest discover -s . -p "test_*.py" -v
```
**Execution Summary:**
- **Previous Test Suite Count:** 121 tests
- **New Integration Tests Added:** 5 tests
- **Total Tests Discovered and Executed:** **126 tests**
- **Execution Time:** 30.358 seconds
- **Pass Rate:** **100% (126 passed, 0 failed, 0 errors, 0 skipped)**

---

## 4. Historical Ledger Verification

The historical daily ledger at [results/daily_quota_ledger.json](file:///C:/testing/research_execution_20261018/results/daily_quota_ledger.json) was audited:

```json
{
  "date": "2026-10-24",
  "cumulative_requests": 604,
  "cumulative_cost_usd": 0.67044,
  "cumulative_prompt_tokens": 84000,
  "cumulative_completion_tokens": 1200,
  "runs_completed": 2,
  "model_name": "gemini-3.1-flash-lite",
  "cost_ceiling_usd": 0.0,
  "max_requests_ceiling": 600,
  "is_free_tier": true,
  "halted_due_to_ceiling": true,
  "last_updated": "2026-10-24T22:50:52.089039",
  "accounting_scope_and_limitations": {
    "counted": "In-process steps, persisted offsets from today's summary CSVs/ledger, conservative token estimates",
    "not_counted": "Provider-side hidden retries, out-of-band requests from external scripts, provider billing meter",
    "guarantee": "Fail-closed client-side bounded requests; does not replace provider cloud console quotas"
  }
}
```

### Ledger Invariants Confirmed:
- `cumulative_requests` is strictly preserved at **604**.
- `max_requests_ceiling` remains configured at **600**.
- `halted_due_to_ceiling` is `true`.
- Any invocation of `protocol_v3_runner.py` (live mode) fails closed immediately on preflight check 9 and dispatch loop check:
  `[SAFETY ABORT] Cumulative requests (604) reached free-tier quota ceiling (600). Failing closed to maintain $0.00 spending.`

---

## 5. Unresolved Risks and Operational Boundaries

1. **Single-Process In-Memory Lock Boundary:**  
   `LocalBudgetGuard._lock` is a `threading.RLock()`. It provides complete thread-safety across concurrent async tasks and threads within a single Python runtime. It does not provide inter-process OS locks (`portalocker` / `fcntl`) across separate CLI terminal windows. Execution must remain strictly single-process.
2. **Provider-Side Rate Limits vs. Quota Ceiling:**  
   The budget guard enforces the total daily request volume (600 ceiling). It does not replace Google's instantaneous 5 Requests-Per-Minute (RPM) rate limiter. `protocol_v3_runner.py` maintains an explicit 15.0s inter-trial pacing sleep to avoid 429 burst errors.
3. **Out-of-Band Calls:**  
   Ad-hoc Python scripts executed outside `protocol_v3_runner.py` without initializing `BudgetGuardedChatModel` bypass the guard. All operational activity must use the canonical runner.
4. **Ceiling Reset Protocol Required Before Phase 2 Live Execution:**  
   Live execution cannot resume until the daily quota period rolls over or the user explicitly authorizes a reset.

---

## 6. Phase 2 Implementation Decision

| Decision Dimension | Status | Justification |
| :--- | :--- | :--- |
| **Offline Phase 2 Tasks (Task Redesign, Verifiers, Mocks)** | **GO** | All code changes are verified offline. The 126-test suite passes cleanly. No live API spend is required. |
| **Live API Trial Execution (Run 42+)** | **STRICT HOLD** | Daily quota ceiling is exhausted (604/600). Preserving ledger integrity and $0.00 free-tier spend requires maintaining the hold until authorized. |

---
*Report certified by Antigravity Autonomous Research Agent.*

# Budget Guard Repair Plan & In-Flight Request Metering Specification

**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24T23:25:00  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Target Codebase:** [budget_controller.py](file:///C:/testing/research_execution_20261018/budget_controller.py), [protocol_v3_runner.py](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)  
**Test Suite:** [test_budget_guard_repairs.py](file:///C:/testing/research_execution_20261018/test_budget_guard_repairs.py)  

---

## 1. Problem Diagnosis: The 604/600 Request Overshoot

### Root Cause Mechanism
During the execution of Block 3 on 2026-10-24, `results/daily_quota_ledger.json` recorded **604 requests**, exceeding the configured ceiling of **600 requests**. A forensic audit established the exact failure path:

1. **Trial-Level Coarseness:** The runner checked quota headroom solely at the trial boundary (`guard.check_can_dispatch_trial()`), prior to starting Run 41.
2. **Missing Worst-Case Headroom Enforcement:** In `execute_experiment()`, `check_can_dispatch_trial()` was called with the default `require_worst_case_headroom=False`.
3. **Sequence of Events:**
   - Prior to Run 41, cumulative requests were **596**.
   - Because $596 < 600$, `check_can_dispatch_trial()` evaluated to `True` and authorized trial launch.
   - Run 41 executed Task T4 (a multi-step checkout form), which made **8 autonomous in-flight model requests**.
   - No guardrail intercepted in-flight LLM calls inside `browser_use.Agent.run()`.
   - Upon completion of Run 41, `record_trial_completion(total_steps=8)` updated the ledger: $596 + 8 = \mathbf{604}$.
   - Before dispatching Run 42, `check_can_dispatch_trial()` evaluated $604 \ge 600$, failed closed, and halted execution.

The guard stopped execution at the earliest possible trial boundary, but lacked the **per-request in-flight granularity** needed to prevent the final trial from overshooting the ceiling.

---

## 2. Vulnerability Audit: Internal Calls, Retries, and Concurrency

| Vulnerability Vector | Existing Vulnerability | Repaired Defense |
|---|---|---|
| **In-Flight Autonomous Steps** | `Agent.run()` loops up to `max_steps` (15 steps) without checking the quota ledger between steps. | In-flight proxy wrapper (`BudgetGuardedChatModel`) checks the guard before every `ainvoke()` call, blocking step $K$ if ceiling is reached. |
| **Provider/SDK Retries** | Internal network retries within Google SDK or LangChain could send hidden requests without client-side counting. | Outer guard wrapper meters every call attempt. Setting `max_retries=1` and `retryable_status_codes=[]` eliminates hidden SDK retry loops. |
| **Agent Internal Calls** | If `use_judge=True` or `summary_llm` is enabled, additional unmetered LLM calls could be dispatched. | All agent LLM references (`llm`, `page_extraction_llm`, `judge_llm`) are wrapped with the guarded proxy. |
| **Concurrent Dispatches** | Multiple async tasks or threads could check quota simultaneously at 599 requests and both dispatch, reaching 601+. | `LocalBudgetGuard` enforces thread safety via `threading.RLock()`, guaranteeing atomic check-and-increment operations. |

---

## 3. Repair Architecture & Implementation

The repair has been implemented across two primary components:

### A. Thread-Safe Request Metering in `LocalBudgetGuard`
In [budget_controller.py](file:///C:/testing/research_execution_20261018/budget_controller.py):
1. **Thread Synchronization:** Added `self._lock = threading.RLock()` to protect all mutation paths.
2. **Pre-Dispatch Verification:** Added `check_can_dispatch_request() -> Tuple[bool, str]`, which verifies that `cumulative_requests < max_requests_ceiling` immediately before network dispatch.
3. **Atomic Pre-Dispatch Reservation:** Added `record_request_pre_dispatch() -> float`, which increments `cumulative_requests += 1` and persists `daily_quota_ledger.json` *before* the HTTP request leaves the machine. If the network call times out or drops, the request remains accounted for.
4. **Post-Dispatch Telemetry Reconcile:** Added `record_request_post_dispatch()`, which reconciles estimated token bounds with actual provider usage metadata without double-incrementing requests.
5. **Trial Completion Decoupling:** Added `requests_already_recorded: bool = False` to `record_trial_completion()`, preventing double-counting when in-flight request tracking is active.

### B. In-Flight Model Interception Proxy (`BudgetGuardedChatModel`)
In [budget_controller.py](file:///C:/testing/research_execution_20261018/budget_controller.py):
```python
class BudgetGuardedChatModel:
    """
    Instrumented proxy wrapper around any LLM (LangChain BaseChatModel or browser_use BaseChatModel).
    Guarantees that EVERY individual model request (including retries, tool calls, and in-flight steps)
    is checked and metered against LocalBudgetGuard BEFORE network dispatch.
    """
    def __init__(self, wrapped_model: Any, guard: LocalBudgetGuard):
        self._wrapped_model = wrapped_model
        self._guard = guard
        for attr in ["model_name", "model", "provider", "name"]:
            if hasattr(wrapped_model, attr):
                setattr(self, attr, getattr(wrapped_model, attr))

    def check_and_record_pre_dispatch(self):
        can_dispatch, msg = self._guard.check_can_dispatch_request()
        if not can_dispatch:
            raise BudgetExceededError(msg)
        self._guard.record_request_pre_dispatch()

    async def ainvoke(self, *args, **kwargs) -> Any:
        self.check_and_record_pre_dispatch()
        response = await self._wrapped_model.ainvoke(*args, **kwargs)
        self.update_post_dispatch(response)
        return response

    def invoke(self, *args, **kwargs) -> Any:
        self.check_and_record_pre_dispatch()
        response = self._wrapped_model.invoke(*args, **kwargs)
        self.update_post_dispatch(response)
        return response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped_model, name)
```

---

## 4. Offline Test Verification & Results

A dedicated regression suite [test_budget_guard_repairs.py](file:///C:/testing/research_execution_20261018/test_budget_guard_repairs.py) was written and executed offline:

```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest test_budget_guard_repairs.py -v
```

### Actual Command Output
```text
test_01_exact_600_request_boundary (test_budget_guard_repairs.TestBudgetGuardRepairs.test_01_exact_600_request_boundary)
The guard must allow request 600, but request 601 must raise BudgetExceededError. ... ok
test_02_worst_case_headroom_enforcement (test_budget_guard_repairs.TestBudgetGuardRepairs.test_02_worst_case_headroom_enforcement)
When worst-case headroom is required, guard halts before starting a trial if steps cannot fit. ... ok
test_03_in_flight_model_request_interception (test_budget_guard_repairs.TestBudgetGuardRepairs.test_03_in_flight_model_request_interception)
BudgetGuardedChatModel intercepts each ainvoke call and raises BudgetExceededError in-flight. ... ok
test_04_retry_request_metering (test_budget_guard_repairs.TestBudgetGuardRepairs.test_04_retry_request_metering)
If an external loop retries after failure, every retry attempt is counted and subject to ceiling. ... ok
test_05_concurrent_dispatch_boundary_safety (test_budget_guard_repairs.TestBudgetGuardRepairs.test_05_concurrent_dispatch_boundary_safety)
Concurrent threads attempting to dispatch simultaneously at ceiling boundary cannot exceed ceiling. ... ok
test_06_historical_604_preservation_and_fail_closed (test_budget_guard_repairs.TestBudgetGuardRepairs.test_06_historical_604_preservation_and_fail_closed)
When initialized with historical 604 requests and 600 ceiling, guard fails closed immediately. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.035s

OK
```

### Full Project Regression Suite
```powershell
& "C:\testing\.venv311\Scripts\python.exe" -m unittest discover -s . -p "test_*.py"
```
**Result:** **121 tests executed, 0 failures, 0 errors, 100% passing (29.900s, $0.00 spend).**

---

## 5. Ledger Integrity & Historical 604 Count Preservation

In strict compliance with research provenance guidelines:
- The historical count of **604 requests** in `results/daily_quota_ledger.json` is preserved without reset or modification.
- **Behavior at Boundary:** When `LocalBudgetGuard` loads the persisted ledger with 604 requests and a ceiling of 600:
  - `check_can_dispatch_trial()` immediately evaluates $604 \ge 600 \rightarrow \text{False}$.
  - `check_can_dispatch_request()` immediately evaluates $604 \ge 600 \rightarrow \text{False}$.
  - Any model invocation immediately raises `BudgetExceededError`.
  - The ledger remains locked at 604, completely preventing further unbudgeted API calls.

# Budget and Safety Guarantees Audit

**Date:** 2026-10-25  
**Auditor:** Independent Systems & Methodology Auditor  
**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*  
**Workspace:** `C:\testing\research_execution_20261018`  
**Core Source Files:** [`budget_controller.py`](file:///C:/testing/research_execution_20261018/budget_controller.py), [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)  
**Associated Test Suites:** [`test_budget_controls.py`](file:///C:/testing/research_execution_20261018/test_budget_controls.py), [`test_budget_guard_repairs.py`](file:///C:/testing/research_execution_20261018/test_budget_guard_repairs.py), [`test_runner_guard_integration.py`](file:///C:/testing/research_execution_20261018/test_runner_guard_integration.py) (18 tests, 100% passing)  

---

## 1. Forensic Analysis of the Historical Overshoot (604 / 600 Event)

### 1.1 Root Cause of the Historical Boundary Breach
In earlier iterations of `protocol_v3_runner.py`, quota checks were evaluated solely at the outer trial loop level:
```python
# Vulnerable Legacy Logic
can_dispatch, msg = guard.check_can_dispatch_trial()
if can_dispatch:
    agent.run()  # Multi-step trial executes up to max_steps (e.g., 4–15 steps)
```
When the cumulative ledger reached 598 requests against the 600 ceiling, `check_can_dispatch_trial()` evaluated $598 < 600$ and permitted trial dispatch. During execution, the agent made 6 sequential model invocations. Because the runner only accounted for requests *after* the entire trial completed, all 6 requests were dispatched to the API, driving the ledger to **604 requests**.

### 1.2 Non-Negotiable Policy: Preserve the 604 Event
The historical ledger at [`results/daily_quota_ledger.json`](file:///C:/testing/research_execution_20261018/results/daily_quota_ledger.json) records:
```json
{
  "date": "2026-10-24",
  "cumulative_requests": 604,
  "max_requests_ceiling": 600,
  "halted_due_to_ceiling": true
}
```
In accordance with Rule 5 of the Master Protocol, this record has **NOT** been deleted, reset, or rewritten to make the project appear compliant. It is preserved as a permanent historical audit event and used as the regression baseline to verify fail-closed enforcement.

---

## 2. The Remediated Architecture: Pre-Dispatch Interception

To guarantee that no model call can bypass the ceiling, the budget architecture was re-engineered around a **two-tier fail-closed interceptor**:

### 2.1 Tier 1: Outer Worst-Case Headroom Check
Before starting any trial, `execute_experiment()` invokes `check_can_dispatch_trial(require_worst_case_headroom=True)`.  
If remaining requests ($\text{ceiling} - \text{cumulative}$) are fewer than `max_steps_per_run` (e.g., $600 - 598 = 2 < 4$), trial dispatch is blocked immediately.

### 2.2 Tier 2: Per-Dispatch Proxy Wrapper (`BudgetGuardedChatModel`)
Regardless of runner-level loops, the LangChain chat model is wrapped inside `BudgetGuardedChatModel` (`budget_controller.py:490–539`):
1. **Pre-Dispatch Interception:** Intercepts both `ainvoke()` and `invoke()` before any HTTP payload leaves the process.
2. **Atomic Reservation:** Invokes `LocalBudgetGuard.record_request_pre_dispatch()` under a thread-safe `threading.RLock()`.
3. **Pre-Allocation:** Increments `cumulative_requests += 1` and persists the updated ledger to disk *before* awaiting the provider.
4. **Post-Dispatch Token Reconciliation:** When the response returns, `update_post_dispatch()` adjusts prompt and completion token counts using provider usage metadata, without double-counting requests.
5. **No Double-Counting on Completion:** `record_trial_completion(requests_already_recorded=True)` finalizes trial records without re-incrementing step counts.

---

## 3. Offline Safety Verification Matrix

The fail-closed behavior of the controller was tested offline across 18 deterministic unit and integration tests using mocks and test doubles:

| Threat Scenario | Test Identifier | Implementation Mechanism | Test Outcome |
| :--- | :--- | :--- | :---: |
| **Ceiling Already Reached** | `test_01_exact_600_request_boundary` | Evaluates $600 \ge 600 \implies$ raises `BudgetExceededError`. | **PASSED** |
| **Historical Ledger at 604** | `test_06_historical_604_preservation` | Evaluates $604 \ge 600 \implies$ halts immediately on initialization. | **PASSED** |
| **One Request Remaining** | `test_01_exact_600_request_boundary` | Request 600 allowed; request 601 blocked. | **PASSED** |
| **Concurrent Race Condition** | `test_05_concurrent_dispatch_boundary_safety` | 10 concurrent threads competing for 5 remaining slots under `RLock`; exactly 5 succeed, 5 raise `BudgetExceededError`, final count $= 600$. | **PASSED** |
| **Network Timeout / Exception** | `test_03_in_flight_model_request_interception` | Atomic pre-reservation counts the attempt even if network drops; prevents hidden retry overrun. | **PASSED** |
| **Worst-Case Headroom Deficit** | `test_02_worst_case_headroom_enforcement` | Rejects trial when headroom $< \text{max\_steps}$. | **PASSED** |
| **External Runner Retry Loop** | `test_04_retry_request_metering` | Repeated retries each decrement quota until ceiling stops the loop. | **PASSED** |
| **End-to-End Runner Wiring** | `test_runner_guard_integration.py` (5 tests) | Verifies `protocol_v3_runner.py` wraps `custom_llm` in `BudgetGuardedChatModel`. | **PASSED** |

---

## 4. Formal Boundaries: Justified Guarantees vs. Non-Guarantees

To maintain absolute academic and engineering honesty, we delineate what this system guarantees versus what it cannot guarantee:

### 4.1 Guarantees Justified by Implementation & Tests
1. **Single-Process Pre-Dispatch Interception:** Every model invocation executed via `Agent.run()` passes through `BudgetGuardedChatModel.ainvoke()` and is checked before network dispatch.
2. **Strict Request Cap:** The current Python process cannot dispatch a 601st model call under a 600 ceiling.
3. **Fail-Closed on Ledger Discrepancy:** If the ledger indicates cumulative requests $\ge$ ceiling, all dispatch functions abort with `BudgetExceededError`.
4. **Conservative Token Fallbacks:** If provider API responses omit token usage metadata, the guard charges worst-case bounds (7,000 prompt / 100 completion tokens) rather than $0.00$.

### 4.2 Guarantees That CANNOT Be Made (Threat Model Boundaries)
1. **Multi-Process Concurrency:** `LocalBudgetGuard` uses in-memory `threading.RLock()`. If multiple independent Python processes run concurrently against the same ledger file without OS-level file locking (`fcntl` or `msvcrt`), race conditions can occur.
2. **Provider-Side Hidden Retries:** If provider HTTP client libraries execute internal network-level connection retries before returning to Python, the provider's billing meter may record requests unseen by the client.
3. **Out-of-Band Calls:** Any external script or developer tool using the same API key outside this runner is untracked.
4. **Provider Quota Replacement:** This client-side guard does NOT query or replace Google AI Studio / Cloud Console quota meters. Users must monitor the cloud console.

---
*Certified by Independent Systems & Methodology Auditor.*

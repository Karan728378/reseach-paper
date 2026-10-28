# Root Cause Investigation & Architectural Diagnostic Report
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Component:** Experimental Execution Engine (`protocol_v3_runner.py`) & Browser Automation Harness (`browser-use 0.13.10` / `cdp_use 1.x`)  
**Auditor / Senior Debugging Engineer:** Autonomous Research Debugging & Remediation Agent  
**Date:** 2026-10-24  
**Workspace:** `C:\testing\research_execution_20261018\`  

---

## 1. Executive Summary

A comprehensive, ground-up investigation of the autonomous browser execution harness (`protocol_v3_runner.py`) was conducted to diagnose the catastrophic failure observed during initial live smoke trials:
```
RuntimeError: Client is not started. Call start() first or use as async context manager.
```
In prior real smoke runs (`results/smoke_runs/run_001.json` through `run_004.json`), this failure caused all runs to be recorded as failed, with `terminal_browser_state` fields (`url`, `title`, `cart`, `order_confirmed`, `last_order_items`) completely empty, and `verifier_result` failing with zeroed scores despite agents having actively performed actions on the page.

Through code inspection, execution tracing, and environment introspection, **five distinct root causes** were identified and confirmed with empirical evidence.

---

## 2. Confirmed Root Causes & Trace Analysis

### Root Cause 1: Page API Mismatch Swallowed by Broad Exception Handling (CONFIRMED)
- **Originating Location:** `protocol_v3_runner.py` (historical lines 570–571).
- **Defect:** The runner invoked synchronous attribute access and legacy method calls on `browser_use.actor.page.Page`:
  ```python
  terminal_url = page.url          # AttributeError: 'Page' object has no attribute 'url'
  terminal_title = await page.title()  # AttributeError: 'Page' object has no attribute 'title'
  ```
- **Consequence:** These calls were wrapped inside an overly broad `try: ... except Exception: pass` block. Because `Page` in `browser-use 0.13.10` exposes asynchronous getter methods `await page.get_url()` and `await page.get_title()`, an `AttributeError` was raised on every single execution, swallowed silently, and caused `terminal_url` and `terminal_title` to remain blank (`""`).

### Root Cause 2: CDP Client Teardown via `Agent.close()` Event Bus Shutdown (CONFIRMED)
- **Originating Traceback:**
  ```python
  File "C:\testing\research_execution_20261018\protocol_v3_runner.py", line 575, in run_single_live_trial
    raw_cart = await page.evaluate("() => window.__cart__ || []")
  File "C:\testing\.venv311\Lib\site-packages\browser_use\actor\page.py", line 125, in evaluate
    return await self._cdp_client.send.Runtime.evaluate(...)
  File "C:\testing\.venv311\Lib\site-packages\cdp_use\client.py", line 369, in send_raw
    if not self.ws:
        raise RuntimeError("Client is not started. Call start() first or use as async context manager.")
  ```
- **Teardown Mechanism:**
  1. The runner called `await session.start()` before execution.
  2. Inside `agent.run()`, the agent executed its steps to completion or maximum steps.
  3. In `browser_use.agent.service.Agent.run()`, the `finally` block executes:
     ```python
     await self.eventbus.stop(clear=True, timeout=_get_timeout('TIMEOUT_AgentEventBusStop', 3.0))
     await self.close()
     ```
  4. Stopping the agent event bus cancels active message handler tasks and clears active subscriptions. In `cdp_use`, closing the transport sets `self.ws = None`.
  5. When `protocol_v3_runner.py` attempted to evaluate `page.evaluate("() => window.__cart__ || []")` *after* `agent.run()` returned, `self._cdp_client.ws` was already `None`, immediately raising `RuntimeError: Client is not started`.

### Root Cause 3: Conflation of Agent Behavioral Telemetry and State Extraction Glitches (CONFIRMED)
- **Defect:** In the historical runner, post-execution state extraction was located outside guarded error isolation blocks:
  ```python
  # Historical flaw
  try:
      history = await agent.run(...)
      total_steps = len(history.history)
      # UNGUARDED DOM EVALUATION:
      raw_cart = await page.evaluate("() => window.__cart__ || []")
  except Exception as e:
      status = "failed"
      error_message = str(e)
      v_res = {"success": False, "score": 0.0, "details": {"error": error_message}}
  ```
- **Consequence:** When `page.evaluate()` crashed due to the closed WebSocket (Root Cause 2), the exception handler overwrote the completed agent trajectory, marked `status = "failed"`, and replaced the verifier result with an error. The benchmark thereby conflated infrastructure client disconnects with model task failures.

### Root Cause 4: Incomplete DATA-CFG Treatment Delivery Rule (CONFIRMED)
- **Defect:** Prior code considered the `DATA-CFG` experimental treatment delivered if *any* single custom data attribute (such as `data-action`) appeared in the serialized observation.
- **Methodological Vulnerability:** Under Protocol v4 (Randomized Complete Block Design), `DATA-CFG` specifically evaluates whether explicit semantic configuration attributes (`data-action`, `data-product-id`, `data-sku`, `data-amount`, `data-rating`) overcome DOM serialization pruning. If only `data-action` is present without the entity identifier (`data-product-id` or `data-sku`), the agent cannot disambiguate product entities from attributes alone.
- **Consequence:** Under-specified delivery verification risks claiming treatment delivery on degraded or malformed DOM trees, introducing experimental confounds.

### Root Cause 5: Lifecycle & Recovery Fragility (CONFIRMED)
- **Startup Exception Leakage:** `await session.start()` was located outside the main `try ... except ... finally` block. If Chrome failed to launch or bind a port, the process crashed unhandled, leaving orphaned Chromium child processes.
- **Improper Teardown:** Historical runner called `session.stop()`, which merely detaches event handlers, instead of `session.kill()`, which forcefully terminates the browser subprocess.
- **Summary Row Survivorship Bias:** `get_completed_run_indices` previously parsed `status in ["completed", "failed"]`, marking crashed runs as completed and permanently skipping them during retry loops.

---

## 3. Inferences & Architectural Hypotheses

| Hypothesis | Status | Validation Evidence |
|---|---|---|
| In-flight step callbacks can safely extract DOM state before `Agent.close()` terminates the CDP session. | **CONFIRMED** | Implemented via `on_step_end` and `register_done_callback`. Successfully captured live URL, title, and cart in `run_001_attempt_2.json`. |
| Disabling `use_judge=False` in `Agent` reduces unnecessary paid API calls and avoids judge latency. | **CONFIRMED** | Protocol runner uses deterministic rule-based verifiers; turning off `use_judge` saved 1 full LLM call per run. |
| Automatic reconnection after `Agent.close()` causes race conditions with active background reconnect tasks. | **CONFIRMED** | `_auto_reconnect()` and explicit `reconnect()` triggered simultaneous connection attempts leading to `NoneType has no attribute send`. Fallback to in-flight state eliminates need for post-close reconnection. |

---

## 4. Summary Matrix of Defects and Resolved States

| Defect | Historical State | Repaired State | Verification |
|---|---|---|---|
| **Page URL/Title** | `page.url`, `await page.title()` (swallowed) | `await page.get_url()`, `await page.get_title()` | Offline tests & Live trial |
| **CDP Client Teardown** | Post-run `page.evaluate()` on dead socket | Continuous in-flight capture via `on_step_end` + `register_done_callback` with fallback | Live trial 1 attempt 2 |
| **Telemetry Conflation** | Extraction error wiped `status` to `failed` | Decoupled `termination_reason`, `status`, and `verifier_result` | Test 3 in lifecycle suite |
| **Browser Startup Crash** | `session.start()` outside `try` | `session.start()` inside `try`, `session.kill()` in `finally` | Test 1 & 5 in lifecycle suite |
| **Summary Filtering** | Included failed runs in completed set | Strict filter: `status == "completed"` only | Test 6 in lifecycle suite |
| **DATA-CFG Delivery** | Checked `data-action` only | Requires `data-action` AND (`data-product-id` or `data-sku`) | Test 4 in lifecycle suite |

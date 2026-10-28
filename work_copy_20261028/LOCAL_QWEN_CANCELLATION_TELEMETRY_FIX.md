# LOCAL QWEN CANCELLATION TELEMETRY FIX REPORT

**Date:** 2026-10-24  
**Scope:** Narrowly scoped instrumentation correction only (Offline, non-invasive)  
**Target Runner:** `C:\testing\research_execution_20261018\local_qwen_smoke_runner.py`  
**Backup:** `C:\testing\research_execution_20261018\local_qwen_smoke_runner.py.bak_20261024_cancellation_fix`  

---

## 1. Problem Statement & Root Cause Analysis

In run `qwen3_smoke_004`, the local Qwen agent timed out during Step 1 at the outer 180-second step watchdog (`Step 1 timed out after 180 seconds`). The outer trial record was persisted, but `model_call_telemetry` was empty (`[]`).

### Root Cause
1. **Inheritance of `asyncio.CancelledError`:** In Python 3.8+, `asyncio.CancelledError` inherits directly from `BaseException`, not `Exception`.
2. **Watchdog Cancellation:** In `browser_use.agent.service.Agent._execute_step` (line 2464), step execution is guarded by:
   ```python
   await asyncio.wait_for(
       self.step(step_info),
       timeout=self.settings.step_timeout, # 180 seconds
   )
   ```
   When the 180-second timeout expires, `asyncio.wait_for` cancels the inner coroutine hierarchy, injecting `asyncio.CancelledError` into `InstrumentedChatOllama.ainvoke`.
3. **Bypass of Error Telemetry:** `InstrumentedChatOllama.ainvoke` previously handled failures using only:
   ```python
   except Exception as e:
   ```
   Because `CancelledError` does not inherit from `Exception`, it completely bypassed this handler. Consequently, no record was appended to `self.call_history`, leaving the telemetry list empty when serialized.

---

## 2. Implementation Details

All modifications were restricted to the project runner `local_qwen_smoke_runner.py`. No installed site-packages or frozen experiment files were modified.

### A. Dedicated Cancellation Handler in `InstrumentedChatOllama.ainvoke`
An explicit `except asyncio.CancelledError as ce:` block was added ahead of `except Exception as e:`:

```python
except asyncio.CancelledError as ce:
    wall_sec = round(time.perf_counter() - t0, 4)
    call_record["timestamp_end"] = datetime.datetime.now().isoformat()
    call_record["wall_clock_seconds"] = wall_sec
    call_record["status"] = "cancelled_in_flight"
    call_record["error_type"] = type(ce).__name__
    call_record["error"] = "In-flight model call cancelled by step watchdog timeout"
    # Server-side token and duration metrics are unavailable for aborted requests
    call_record["prompt_tokens"] = None
    call_record["completion_tokens"] = None
    call_record["total_tokens"] = None
    call_record["prompt_eval_duration_ms"] = None
    call_record["eval_duration_ms"] = None
    call_record["load_duration_ms"] = None
    call_record["total_duration_ms"] = None
    self.call_history.append(call_record)
    raise
```

**Key properties:**
- **Re-raises Cancellation Unchanged:** Uses `raise` to ensure `CancelledError` propagates without being swallowed, allowing `browser-use`'s `asyncio.wait_for` to trigger its graceful step timeout.
- **Accurate Observability:** Captures the run ID, 1-indexed call count, start/end timestamps, elapsed wall-clock time (~180.0s), status `cancelled_in_flight`, and error type `CancelledError`.
- **Honest Null Metrics:** Unavailable server metrics (`prompt_tokens`, `completion_tokens`, server-side durations) are strictly set to `None` (`null` in JSON). They are never guessed, fabricated, or defaulted to zero.

### B. Safe Record Finalization Path in `execute_local_smoke_trial`
To ensure partial telemetry is persisted even if cancellation reaches the trial level:
1. **CDP Evaluation Guard:** Post-run CDP verification was placed in a dedicated `try/except` block so that a browser crash or disconnected page during timeout cannot crash the runner or overwrite the timeout status.
2. **Trial-Level Cancellation Catching:** Added `except asyncio.CancelledError as ce:` to classify `status = "timed_out"`, `termination_reason = "cancelled_by_watchdog"`, and perform best-effort CDP evaluation.
3. **Session Teardown Shielding:** In `finally:`, wrapped `session.stop()` with `asyncio.shield(...)` to prevent cancellation interrupts from aborting record persistence.
4. **Guaranteed Finalization:** The JSON trace and CSV appending logic executes unconditionally after session cleanup.

---

## 3. Offline Verification & Test Results

Validation was performed entirely offline without launching a browser, making network calls, or connecting to Ollama.

### A. Bytecode Compilation & CLI Help Check
- **Bytecode Syntax Check:**
  ```powershell
  python -m py_compile local_qwen_smoke_runner.py
  # Exit Code: 0 (Clean)
  ```
- **CLI Help Output:**
  ```powershell
  python local_qwen_smoke_runner.py --help
  # Exit Code: 0 (Clean argument parsing)
  ```
- **Run ID Resolution:**
  ```powershell
  python -c "from local_qwen_smoke_runner import get_next_run_info, PILOT_RESULTS_DIR; print(get_next_run_info(PILOT_RESULTS_DIR))"
  # Output: ('qwen3_smoke_005', WindowsPath('.../results/local_llama_pilot_runs/qwen3_smoke_run_005.json'))
  ```

### B. Mocked Unit Test Suite (`scratch/test_instrumented_ollama.py`)
Tested 4 scenarios with `unittest.IsolatedAsyncioTestCase`:
1. `test_successful_invocation_with_schema`:
   - Validated structured output validation.
   - Confirmed native Ollama token counts (1450 prompt, 65 completion) and durations (2500ms prompt eval, 1100ms eval) are logged accurately.
2. `test_provider_error_invocation`:
   - Simulated `httpx.ReadTimeout`.
   - Verified `ModelProviderError` is raised, recorded exactly once with `status = "timeout"`, `error_type = "ReadTimeout"`, and `None` token metrics.
3. `test_cancelled_error_invocation`:
   - Simulated step watchdog timeout raising `asyncio.CancelledError`.
   - Verified `asyncio.CancelledError` is re-raised unchanged.
   - Verified call is recorded exactly once in `call_history`.
   - Verified `status == "cancelled_in_flight"`, `error_type == "CancelledError"`.
   - Verified wall-clock duration is captured (> 0s) while server token and duration fields are strictly `None`.
4. `test_runner_record_finalization_with_cancelled_telemetry`:
   - Simulated trial cancellation and verified record serialization to JSON.
   - Confirmed `model_call_telemetry` is populated with `cancelled_in_flight` call record, unobserved server metrics serialize to `null`, and ground-truth verifier outcome is preserved.

**Test Run Output:**
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.141s

OK
```

---

## 4. Technical Limitations & Observability Boundaries

> [!IMPORTANT]
> **Explicit Disclaimer Regarding Server-Side Timing:**  
> This fix does **not** recover Ollama's internal timing or token counts for a cancelled request. When a request is aborted mid-flight by a client-side timeout, Ollama never returns an HTTP response payload. Consequently, server-side token counts and generation durations do not exist.  
> 
> This fix makes the **client-side cancellation and elapsed wall-clock time observable**. Token counts and server duration fields remain strictly `null` in the recorded telemetry.

---

## 5. Protocol Boundaries & Evidence Integrity Confirmation

- **No Browser Executed:** No Playwright browser process was started.
- **No Ollama / LLM Inference:** No requests were dispatched to `http://127.0.0.1:11434` or any local/remote model endpoint.
- **No External Network Calls:** System operated strictly offline.
- **Existing Traces Preserved:** `qwen3_smoke_run_001.json` through `qwen3_smoke_run_004.json` and `results/local_llama_summary.csv` remain unaltered.
- **Frozen Gemini Experiment Intact:** `protocol_v3_runner.py`, `results/3arm_runs/`, and schedule files remain untouched.

---

## 6. Current Status & Next Step

The instrumentation correction is complete, validated offline, and ready. The runner will target `qwen3_smoke_005` on its next live trial.

**Execution stopped.** Awaiting explicit user approval before executing any live trial.

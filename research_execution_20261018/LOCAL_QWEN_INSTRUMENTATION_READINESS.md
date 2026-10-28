# LOCAL QWEN RUNNER: FINE-GRAINED LATENCY INSTRUMENTATION & PILOT READINESS REPORT

**Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Location:** `C:\testing\research_execution_20261018\`  
**Target Architecture:** Local Ollama `qwen3:4b` | `browser-use 0.13.10` | Chromium CDP  
**Status:** Instrumentation Validated via Mocked Unit Tests (Zero Live Trials Executed)  
**Date:** October 2026  

---

## 1. Executive Summary

To mathematically resolve whether post-action timeouts are driven by prompt-evaluation overhead (token ingestion) versus token generation, the local Qwen runner has been augmented with **non-invasive, project-level per-call latency instrumentation**.

### Strict Scientific Constraints Observed
* **Zero Package Modifications:** Installed packages in `C:\testing\.venv311\Lib\site-packages\` remain 100% untouched. All instrumentation is encapsulated in a project-level subclass ([`InstrumentedChatOllama`](file:///C:/testing/research_execution_20261018/local_qwen_smoke_runner.py#L279-L393)) inside [`local_qwen_smoke_runner.py`](file:///C:/testing/research_execution_20261018/local_qwen_smoke_runner.py).
* **Backup Verified:** Pre-patch runner backed up to [`local_qwen_smoke_runner.py.bak_20261024_instrumentation`](file:///C:/testing/research_execution_20261018/local_qwen_smoke_runner.py.bak_20261024_instrumentation).
* **Zero Network / Model Calls:** Validation was conducted exclusively via offline mocked unit testing (`unittest.IsolatedAsyncioTestCase` with `AsyncMock`). No live Ollama inference or browser processes were launched.
* **Frozen Gemini Corpus Protected:** All Gemini cohort data ([`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py), `results/3arm_runs/`, [`results/v3_3arm_summary.csv`](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv), and schedules) remain strictly unmodified.
* **Trace Preservation:** Existing baseline traces (`qwen3_smoke_run_001.json`, `002`, `003`) remain pristine; next run is automatically assigned to `qwen3_smoke_004`.

---

## 2. Technical Architecture of the Instrumentation

### 2.1 Native Ollama Latency Metadata

The official `ollama` Python SDK returns `ollama._types.ChatResponse`, which inherits from `BaseGenerateResponse` containing native nanosecond counters:

| Native Attribute | Type | Description | Unit Stored |
| :--- | :--- | :--- | :--- |
| `prompt_eval_count` | `int` | Number of tokens in the evaluated prompt | Tokens |
| `eval_count` | `int` | Number of tokens generated in inference | Tokens |
| `prompt_eval_duration` | `int` | Time spent ingesting & evaluating prompt | Milliseconds (`ns / 1e6`) |
| `eval_duration` | `int` | Time spent generating output tokens | Milliseconds (`ns / 1e6`) |
| `load_duration` | `int` | Time spent loading/reloading model weights | Milliseconds (`ns / 1e6`) |
| `total_duration` | `int` | Total Ollama server execution time | Milliseconds (`ns / 1e6`) |

Standard `browser-use` discards these metrics by returning `ChatInvokeCompletion(completion=parsed, usage=None)`.

### 2.2 `InstrumentedChatOllama` Implementation

The subclass intercepts `ainvoke()`, extracts all native metrics, computes request wall-clock latency, and appends a structured record to `self.call_history`:

```python
@dataclass
class InstrumentedChatOllama(ChatOllama):
    run_id: str = "unknown"
    call_history: List[Dict[str, Any]] = field(default_factory=list)

    async def ainvoke(self, messages: list[BaseMessage], output_format: Any = None, **kwargs: Any) -> ChatInvokeCompletion[Any]:
        # Captures t0, call_idx, and timestamps
        # Executes standard Ollama chat with schema validation
        # Extracts: prompt_eval_count, eval_count, prompt_eval_duration_ms, eval_duration_ms, wall_clock_seconds
        # Handles timeouts and exceptions: tags status as "timeout" or "error", records elapsed wall clock, and re-raises ModelProviderError
        # Appends structured record to self.call_history
        # Returns standard ChatInvokeCompletion with populated ChatInvokeUsage
```

---

## 3. Code Diffs & Integration in `local_qwen_smoke_runner.py`

### Diff 1: Imports Added
```diff
+from dataclasses import dataclass, field
+import httpx
+from pydantic import ValidationError
+from browser_use.llm.ollama.chat import ChatOllama, _unwrap_json_content
+from browser_use.llm.ollama.serializer import OllamaMessageSerializer
+from browser_use.llm.views import ChatInvokeCompletion, ChatInvokeUsage
+from browser_use.llm.messages import BaseMessage
+from browser_use.llm.exceptions import ModelProviderError
```

### Diff 2: LLM Instantiation
```diff
-    # 3. Initialize Local ChatOllama with bounded context
-    llm = ChatOllama(
+    # 3. Initialize Local InstrumentedChatOllama with fine-grained latency tracking
+    llm = InstrumentedChatOllama(
         model=model_name,
         host=host,
         timeout=180.0,
+        run_id=run_id,
         ollama_options={
             "num_ctx": num_ctx,
             "temperature": 0.0
         }
     )
```

### Diff 3: Persistence into Run Record
```diff
         "terminal_cart_state": cart_items,
         "verifier_outcome": verifier_outcome,
+        "model_call_telemetry": getattr(llm, "call_history", []),
         "financial_cost_usd": 0.00000,
```

---

## 4. Offline Mocked Validation Results

Validation was conducted using an isolated test script (`test_instrumented_ollama.py`) with zero external network or model requests:

### Test Suite Execution
```powershell
C:\testing\.venv311\Scripts\python.exe "scratch\test_instrumented_ollama.py"
```

**Results:**
```
..
----------------------------------------------------------------------
Ran 2 tests in 0.045s

OK
```

1. **`test_successful_invocation_with_schema` (Passed):**
   * Verified that schema-constrained responses properly parse into Pydantic models.
   * Verified that nanosecond durations are accurately converted to milliseconds (`prompt_eval_duration_ms: 2500.0`, `eval_duration_ms: 1100.0`).
   * Verified that token counts (`prompt_tokens: 1450`, `completion_tokens: 65`, `total_tokens: 1515`) are correctly propagated into `ChatInvokeUsage`.
2. **`test_timeout_invocation` (Passed):**
   * Verified that when `httpx.ReadTimeout` is raised, `call_record` records `status: "timeout"`, captures the elapsed `wall_clock_seconds`, leaves token counts as `None`, and re-raises `ModelProviderError` as required by `browser-use`.

### Integrity & Safety Verification
* `python -m py_compile local_qwen_smoke_runner.py` passed with exit code `0`.
* `get_next_run_info()` returned `('qwen3_smoke_004', ...)` confirming existing runs 001, 002, and 003 are preserved.
* CLI help options verified with exit code `0`.

---

## 5. Limitations & Missing Metadata

1. **In-Flight Cancellation Timing:**
   * If `asyncio.wait_for(step_timeout)` cancels the task while Ollama is still processing, Ollama does not return an HTTP response. The wrapper accurately records the elapsed wall-clock seconds and tags `status: "timeout"`, but token counts for that aborted request cannot be retrieved from Ollama post-cancellation.
2. **First-Token Latency (Time-to-First-Token / TTFT):**
   * Because `browser-use` requires non-streaming JSON responses to enforce structured Pydantic output validation, TTFT is not measured separately from total generation time. However, `prompt_eval_duration` directly measures prompt processing time prior to the start of token generation.

---

## 6. Proposed Six-Run Pilot Protocol: `ABS` vs. `DATA-CFG`

### 6.1 Objective
Empirically test whether additive semantic markup (`DATA-CFG`) reduces exploratory agent steps and improves target grounding compared to standard accessibility trees (`ABS`), and measure the exact token evaluation overhead introduced by semantic attributes.

### 6.2 Pilot Design Matrix (T2 Target: 'Mechanical Keyboard Pro', SKU `mkp-001`)

To prevent temporal bias, the 6 trials should be executed sequentially in an interleaved/pseudo-randomized order:

| Run Number | Planned Run ID | Task | Experimental Arm | Variant | Target SKU | Step Limit | Timeout / Step |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `qwen3_smoke_004` | T2 | `ABS` (Control) | `v3-data-attrs` | `mkp-001` | 3 | 180s |
| 2 | `qwen3_smoke_005` | T2 | `DATA-CFG` (Treatment) | `v3-data-attrs` | `mkp-001` | 3 | 180s |
| 3 | `qwen3_smoke_006` | T2 | `ABS` (Control) | `v3-data-attrs` | `mkp-001` | 3 | 180s |
| 4 | `qwen3_smoke_007` | T2 | `DATA-CFG` (Treatment) | `v3-data-attrs` | `mkp-001` | 3 | 180s |
| 5 | `qwen3_smoke_008` | T2 | `ABS` (Control) | `v3-data-attrs` | `mkp-001` | 3 | 180s |
| 6 | `qwen3_smoke_009` | T2 | `DATA-CFG` (Treatment) | `v3-data-attrs` | `mkp-001` | 3 | 180s |

*Note: In the `ABS` control arm, `include_attributes` is restricted to `DEFAULT_INCLUDE_ATTRIBUTES` (stripping all custom `data-*` fields), exactly mirroring the frozen Gemini experiment protocol.*

### 6.3 Outcome Variables
1. **Primary Ground-Truth Success:** CDP inspection of `window.__cart__` (1.0 if `mkp-001` present, else 0.0).
2. **Step 1 Model Latency:** Wall-clock time and `prompt_eval_duration_ms` for initial interaction.
3. **Step 1 Action Precision:** Whether index 33 (`Add to Cart` for `mkp-001`) was selected on the first action.
4. **Prompt Token Difference:** $\Delta \text{Tokens} = \text{Tokens}_{\text{DATA-CFG}} - \text{Tokens}_{\text{ABS}}$.
5. **Clean Completion Rate:** Proportion of trials achieving `agent_completed` vs `timed_out`.

### 6.4 Predefined Stopping Criteria
* **Consecutive Crash Limit:** If 2 consecutive trials encounter unhandled infrastructure crashes (OOM or CDP socket disconnect), halt immediately.
* **Low Memory Limit:** If free physical RAM drops below 1,500 MB, abort trial immediately.
* **Timeout Ceiling:** Strict 180s per step limit, with `max_failures=1` guaranteeing that any stalled step halts after $\le 180\text{s}$. Total runtime for the 6-run pilot is bounded to $\le 35\text{ minutes}$.

---

## 7. Current Status & Stop Condition

* The runner has been patched and validated offline.
* **No browser trials or live model calls have been executed.**
* Standing by for explicit user approval before launching Run 1 (`qwen3_smoke_004`) or the full 6-run pilot.

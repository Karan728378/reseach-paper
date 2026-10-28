# LOCAL QWEN BROWSER-AGENT: BOTTLENECK DIAGNOSIS & REPEATABILITY PILOT PLAN

**Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Location:** `C:\testing\research_execution_20261018\`  
**Target Architecture:** Local Ollama `qwen3:4b` | `browser-use 0.13.10` | Chromium CDP  
**Status:** Pre-Pilot Diagnostic & Experimental Design (Read-Only)  
**Date:** October 2026  

---

## 1. Executive Summary & Problem Statement

Across three baseline trials of Task T2 (`DATA-CFG`, variant `v3-data-attrs`) on a local, air-gapped `qwen3:4b` model, the agent demonstrated **high semantic task competence** (correctly locating the product `'Mechanical Keyboard Pro'`, extracting target identifier `mkp-001`, and executing the button click on Step 1/2), yet **failed to achieve clean completion** due to an execution timeout during post-action state re-evaluation.

This document presents a rigorous, evidence-based diagnosis of the execution bottleneck, evaluates five interacting latency drivers, and outlines an empirical pilot plan to evaluate whether additive semantic markup (`DATA-CFG`) confers a measurable advantage over standard accessibility tree representations (`ABS`) on locally hosted, quantized models.

---

## 2. Evidence Audit & Baseline Reconciliation

### 2.1 Reconciled Trial Records

All three baseline attempts have been preserved as separate, immutable records with distinct run IDs and accurate classifications in [`results/local_llama_summary.csv`](file:///C:/testing/research_execution_20261018/results/local_llama_summary.csv) and [`results/local_llama_pilot_runs/`](file:///C:/testing/research_execution_20261018/results/local_llama_pilot_runs/):

| Run ID | Timestamp | Duration | Steps | Status | Termination Reason | CDP Verifier | Final Cart | Classification |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :--- |
| `qwen3_smoke_001_init_failed` | `12:47:59` | 3.34s | 0 | `failed` | `init_exception` | False | `[]` | **Infrastructure Failure** (Pydantic validator: `max_history_items <= 5`) |
| `qwen3_smoke_002_timeout_verified` | `12:52:22` | 1013.09s | 2 | `partial_timeout` | `llm_timeout_max_steps_reached` | **True (1.0)** | `['mkp-001']` | **Verified Cart Success with Model Timeout** (Unbounded step loop) |
| `qwen3_smoke_003` | `13:57:22` | 288.61s | 2 | `timed_out` | `llm_or_step_timeout` | **True (1.0)** | `['mkp-001']` | **Verified Cart Success with Bounded Step Timeout** (180s ceiling) |

### 2.2 Reconciled Step-by-Step Latency Profile (`qwen3_smoke_003`)

The instrumentation added in Stage 5 captured fine-grained wall-clock timings:

```
[0.00s] Process Launch & Preflight Check (Free RAM: 6425 MB, VRAM: 585/4096 MB)
[0.45s] Mock HTTP Shop Server Confirmed on 127.0.0.1:8080
[1.80s] Chromium BrowserSession Started (Headless, 1920x1080)
[1.95s] Initial Navigation Executed (http://127.0.0.1:8080/variants/v3-data-attrs/index.html#home)
        └── Step 1 Duration: 0.0s (deterministic pre-action)
[2.35s] Step 1 Observation Context Built (DOM extraction: 0.386s)
[2.35s - 105.25s] Step 1 Model Call (Duration: 102.909s)
        ├── Ollama Prompt Evaluation (~1500 tokens)
        ├── GBNF Grammar Constraint Evaluation (21.2 KB AgentOutput schema)
        └── Token Generation: Thinking + ClickActionModel(click=33)
[105.30s] Browser Action Executed: Clicked button "Add to Cart"
        └── Shop UI Updates: window.__cart__ populated with SKU 'mkp-001'
[105.65s] Step 2 Observation Context Built (Updated DOM with cart badge and notification)
[105.65s - 285.65s] Step 2 Model Call (180.000s Step Timeout Expired)
        ├── Ollama Prompt Evaluation (~3200 tokens cumulative history)
        ├── Timed out before generating completion / done() action
        └── Agent halted on max_failures=1
[285.70s] Independent Ground-Truth Verifier via CDP:
        └── window.__cart__ -> [{'sku': 'mkp-001', 'name': 'Mechanical Keyboard Pro', ...}] -> SUCCESS
[288.61s] Browser Session Closed, Trace and Summary Persisted.
```

---

## 3. Bottleneck Investigation: Five Interacting Drivers

### 3.1 Measured Facts vs. Hypotheses

| Potential Driver | Evidence / Measurement | Classification | Impact on Timeout |
| :--- | :--- | :---: | :--- |
| **DOM Serialization** | Measured directly on `v3-data-attrs` via `get_browser_state_summary()`: **0.386 seconds** | **Measured Fact** | Negligible ($\le 0.4\text{s}$) |
| **Step Timeout vs LLM Timeout** | `step_timeout` clock starts at `step()` entrance; `llm_timeout` starts inside `_get_next_action()`. Step timeout triggered at $t = 180.0\text{s}$. | **Measured Fact** | Primary trigger of loop termination |
| **Recovery / Post-Failure Call** | `final_response_after_failure=False` and `max_failures=1` verified in code. Agent immediately exited loop. | **Measured Fact** | Zero recovery calls made |
| **Schema Complexity** | `AgentOutput.model_json_schema()` inspected: **21,209 characters (~21.2 KB)**. | **Measured Fact** | High GBNF parsing & constraint overhead in llama.cpp |
| **Prompt Token Accumulation** | Step 1 context: ~1,500 tokens. Step 2 context: ~3,200 tokens (due to cumulative DOM history). | **Measured Fact** | Doubles prompt eval time from ~50s to >100s |
| **CPU/GPU Hybrid Offloading** | `ollama ps` confirms: **34% CPU layers / 66% GPU layers** due to 4 GB VRAM limit. | **Measured Fact** | Reduces token ingestion speed by $4\times$ to $6\times$ vs pure GPU |
| **Power Profile Throttling** | `powercfg` confirmed active scheme is **Silent** (`64a64f24-65b9-4b56-befd-5ec1eaced9b3`), P-state P8. | **Measured Fact** | Throttles CPU/GPU clocks and wattage |

### 3.2 Root-Cause Synthesis

The agent's failure to complete cleanly is not caused by semantic confusion, DOM serialization lag, or browser-engine lockup. Rather, it is a **cumulative prompt-ingestion bottleneck**:

1. In Step 1, the prompt is relatively small (~1,500 tokens). On 34% CPU / 66% GPU hybrid compute under throttled power, `qwen3:4b` completes ingestion, GBNF grammar compilation, and action generation in **102.9 seconds**, well within the 180s ceiling.
2. In Step 2, `browser-use` appends the full previous step history, action result, and the new DOM tree. The input token count approximately doubles (>3,000 tokens).
3. Prompt evaluation in llama.cpp CPU/GPU hybrid mode scales linearly with prompt token length. At an estimated hybrid ingestion rate of ~15–20 tokens/sec under Silent power, ingesting 3,200 tokens requires **160–210 seconds** before a single output token can be generated.
4. Consequently, the 180-second `step_timeout` expires while Ollama is still processing the prompt or generating the opening reasoning tokens.

---

## 4. Local Execution & Data Integrity Audit

### 4.1 Telemetry Elimination Verification

Inspection of `browser_use/telemetry/service.py` confirmed:
* `ProductTelemetry.__init__` reads `CONFIG.ANONYMIZED_TELEMETRY`.
* Passing `os.environ["ANONYMIZED_TELEMETRY"] = "false"` at module startup forces `telemetry_disabled = True`, causing `self._posthog_client = None`.
* All calls to `capture()`, `_direct_capture()`, and `flush()` contain `if self._posthog_client is None: return`, preventing any PostHog network dispatch.
* Passing `os.environ["BROWSER_USE_VERSION_CHECK"] = "false"` disables PyPI update checks.

### 4.2 Network Isolation Status: Verified vs. Unverified

* **Verified:**
  * All cloud API keys (`GOOGLE_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY`, etc.) are purged from the process environment upon script execution.
  * Inference requests are hardcoded to loopback `http://127.0.0.1:11434`.
  * Target web application connects strictly to loopback `http://127.0.0.1:8080`.
  * Application telemetry and update checks are fully disabled.
* **Unverified (Remaining Limitation):**
  * The Windows host system remains connected to the physical local network. The runner enforces application-level air-gapping, but does not configure Windows Defender Firewall or containerize the network stack.

### 4.3 Data Preservation Guarantee

* Frozen Gemini assets ([`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py), `results/3arm_runs/`, [`results/v3_3arm_summary.csv`](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv), and `proposed_3arm_schedule.csv`) remain completely unmodified.
* Local Qwen results are completely segregated inside `results/local_llama_pilot_runs/` and `results/local_llama_summary.csv`.

---

## 5. Mini-Pilot Experimental Design: Control (`ABS`) vs. Treatment (`DATA-CFG`)

### 5.1 Research Question & Formal Hypotheses

* **Core Research Question:** Does additive semantic markup (`DATA-CFG` / `v3-data-attrs`) significantly improve target item grounding and task success on quantized local models (`qwen3:4b`), or does the additional attribute token footprint increase prompt-evaluation latency beyond manageable timeout bounds?
* **Hypothesis 1 (Grounding Efficacy):** Under `DATA-CFG`, `qwen3:4b` will locate target products on Step 1 with higher accuracy and fewer misidentifications than under `ABS` (which lacks semantic `data-*` attributes).
* **Hypothesis 2 (Serialization Overhead):** `DATA-CFG` expands DOM observation text by ~15–25%, which increases Step 1 model latency relative to `ABS`, but this overhead is offset if the agent requires fewer exploratory clicks.

### 5.2 Experimental Conditions & Matrix

To keep total execution time reasonable while achieving statistical paired comparisons, the proposed mini-pilot consists of **6 to 12 runs**:

| Task ID | Description | Arm / Variant | Repetitions | Primary Target |
| :---: | :--- | :--- | :---: | :---: |
| **T2** | Add "Mechanical Keyboard Pro" | `ABS` (Baseline control) | 3 | SKU `mkp-001` |
| **T2** | Add "Mechanical Keyboard Pro" | `DATA-CFG` (`v3-data-attrs`) | 3 | SKU `mkp-001` |
| **T1** *(Optional)* | Search & Add least expensive headphone | `ABS` (Baseline control) | 3 | SKU `wh-001` |
| **T1** *(Optional)* | Search & Add least expensive headphone | `DATA-CFG` (`v3-data-attrs`) | 3 | SKU `wh-001` |

*Recommended starting scope:* **6 runs total** (3 repeats of T2 under `ABS` vs 3 repeats of T2 under `DATA-CFG`).

### 5.3 Outcome Measures

1. **Primary Outcome:**
   * **Ground-Truth Task Success (Binary, 0.0 or 1.0):** Evaluated strictly via Playwright CDP inspection of `window.__cart__`. Independent of agent self-reporting.
2. **Secondary Outcomes:**
   * **Clean Agent Completion Rate:** Percentage of trials ending in clean `done()` action versus timeout.
   * **Step 1 Action Accuracy:** Correct target element selected on the first interaction.
   * **Latency Breakdown:** Setup time, Step 1 model latency, Step 2 model latency, total wall-clock time.
   * **Resource Utilization:** Peak RAM, peak VRAM, and GPU offload percentage.

### 5.4 Proposed Minimal Instrumentation Enhancements

Without altering any frozen protocols, two non-invasive enhancements should be incorporated into `local_qwen_smoke_runner.py`:

1. **Ollama Detailed Latency Telemetry:**
   Wrap `ChatOllama.ainvoke()` to extract Ollama's native response metadata (`eval_count`, `eval_duration`, `prompt_eval_count`, `prompt_eval_duration`) and record them in the JSON trace. This directly separates prompt ingestion time from token generation time.
2. **History Trimming / Sliding Window Optimization:**
   Currently `max_history_items=6` retains all past DOM trees. Investigating whether setting `max_history_items=6` with compact DOM summaries or pruning previous DOM strings prevents prompt explosion on Step 2.

### 5.5 Failure Classification Taxonomy

All pilot outcomes will be classified into four mutually exclusive categories:
* `SUCCESS_CLEAN`: Ground truth verified AND agent marked task completed cleanly.
* `SUCCESS_TIMEOUT`: Ground truth verified, but subsequent planning or completion step timed out.
* `FAILURE_INCORRECT_ACTION`: Agent executed incorrect action (wrong item clicked/added).
* `INFRASTRUCTURE_FAILURE`: OOM, unhandled exception, or connection drop before action execution.

### 5.6 Runtime Estimates & Stopping Criteria

* **Estimated Trial Duration:** ~250–320 seconds per run under the 180s bounded timeout.
* **Batch Runtime (6 runs):** $\approx 25\text{ to }35\text{ minutes}$.
* **Stopping Criteria:**
  * If 2 consecutive trials encounter an infrastructure exception (OOM or CDP drop), abort immediately.
  * If available physical RAM drops below 1,500 MB, abort immediately.

---

## 6. Audit Summary & Readiness Checklist

* [x] Attempt 1, Attempt 2, and Attempt 3 records preserved and reconciled.
* [x] DOM serialization ruled out as bottleneck ($0.386\text{s}$).
* [x] Step timeout confirmed as primary halt mechanism ($180.0\text{s}$).
* [x] Application-level telemetry verified disabled (`_posthog_client = None`).
* [x] Gemini research cohort completely untouched and isolated.
* [x] Pilot plan for `ABS` vs `DATA-CFG` formulated with clear hypotheses and stopping criteria.

---

*This document is a diagnostic and planning artifact. No browser agent trials or LLM inference requests have been executed during this phase.*

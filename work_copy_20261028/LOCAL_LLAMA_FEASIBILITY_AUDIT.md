# Feasibility Audit: Fully Local Llama Inference via Ollama

**Project:** *The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents*  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date:** October 24, 2026  
**Auditor:** Autonomous Senior Research Engineer (DeepMind Antigravity System)  
**Deliverable:** `LOCAL_LLAMA_FEASIBILITY_AUDIT.md`  
**Target Hardware:** Windows 11, AMD Ryzen 7 7435HS (8C/16T, no iGPU), NVIDIA GeForce RTX 2050 Laptop GPU (4 GB GDDR6 VRAM), 16 GB DDR5 RAM  
**Execution Boundary:** **100% Offline Read-Only Audit — Zero Live API Calls — No Software Installed — No Model Weights Downloaded — Runner Halted**

---

## 1. Executive Summary

This audit assesses the technical, architectural, and scientific feasibility of transitioning from cloud-hosted inference (Google Gemini) to an entirely local, air-gapped open-weights model using **Ollama** on your existing Windows 11 laptop.

### Key Conclusions:
1. **Zero Financial Risk Guarantee:** Running local models on localhost eliminates 100% of external billing risks, auto-top-up mechanisms, and cloud overages. Financial cost is identically **$0.00**.
2. **Current Installation Status:**
   - The Ollama Windows executable is **NOT currently installed** on the system (not found in PATH, LocalAppData, or Program Files; port 11434 is closed).
   - The Python `ollama` SDK (`v0.6.1`) is **already installed** in `.venv311`.
   - `browser-use 0.13.10` has **native built-in support** for Ollama via `browser_use.llm.ollama.chat.ChatOllama` with strict JSON-schema grammar enforcement.
3. **Hardware & Model Sizing:**
   - **Llama 3.2 3B (Q4_K_M, ~2.0 GB):** **100% GPU Viable.** Fits completely in the RTX 2050’s 4 GB VRAM along with an 8k–12k context KV cache. Fast inference (~40–60 tokens/sec), but lower complex DOM reasoning capability.
   - **Llama 3.1 8B (Q4_K_M, ~4.7 GB):** **Hybrid GPU+CPU Viable.** Exceeds 4 GB VRAM. Approximately 16–18 layers fit on the RTX 2050, with remaining 14–16 layers running on the Ryzen 7 7435HS CPU via system RAM. Generation speed drops to ~8–15 tokens/sec (~1.5–3 min per run), but reasoning and tool-calling fidelity are vastly superior.
4. **Scientific Invariant:** Local model results **must not be pooled** with Gemini Runs 1–27. They must be routed into a separate pilot directory (`results/local_llama_pilot_runs/`).

---

## 2. Environment & Dependency Status

### Inspection Findings (Read-Only)

| Component | Status | Location / Output | Notes |
|:---|:---:|:---|:---|
| **Ollama CLI / Service** | **Not Installed** | Exit Code 1 (`Get-Command ollama`) | Port 11434 is not listening. Zero local daemons active. |
| **Python `ollama` Package** | **Installed** | `.venv311\Lib\site-packages\ollama` | Version `0.6.1` is already present in `.venv311`. |
| **`browser-use` Ollama Wrapper** | **Available** | `.venv311\...\browser_use\llm\ollama\chat.py` | Native `ChatOllama` class confirmed; instantiates cleanly. |
| **Structured Output Schema** | **Native** | Ollama JSON schema API (`format=schema`) | Uses llama.cpp grammar constraints to enforce Pydantic output. |
| **`budget_controller.py`** | **Requires Update** | `MODEL_PRICING_TABLE` | Needs local model IDs mapped to $0.00 to avoid `UnknownModelPricingError`. |

---

## 3. Hardware Constraint & Model Sizing Analysis

### Hardware Architecture:
- **CPU:** AMD Ryzen 7 7435HS (8 Cores, 16 Threads, Zen 3+ architecture, 16 MB L3 cache). Note: The 7435HS has *no integrated GPU*, meaning the RTX 2050 must drive the laptop display and Windows Desktop Window Manager (DWM), consuming ~600–800 MB of VRAM at idle.
- **Dedicated GPU:** NVIDIA GeForce RTX 2050 Laptop GPU (4,096 MB GDDR6 VRAM, 64-bit bus, ~112 GB/s bandwidth, 2,048 CUDA cores). Usable VRAM for models: **~3.2 to 3.4 GB**.
- **System Memory:** 16 GB DDR5 RAM (~40–50 GB/s bandwidth).

---

### Detailed Model Evaluation Matrix

| Evaluation Dimension | Option A: Llama 3.2 3B (`llama3.2:3b` - Q4_K_M) | Option B: Llama 3.1 8B (`llama3.1:8b` - Q4_K_M) | Evaluation Impact |
|:---|:---|:---|:---|
| **Model Weights Size** | ~2.0 GB | ~4.7 to 4.9 GB | 3B fits in VRAM; 8B exceeds 4 GB VRAM. |
| **VRAM Consumption** | ~2.0 GB (weights) + ~0.94 GB (8k KV cache) $\approx$ **2.94 GB** | ~2.5 GB (offloaded layers) + ~0.7 GB (VRAM KV cache) $\approx$ **3.2 GB** | 3B runs 100% on GPU. 8B requires ~50% layer offloading to CPU RAM. |
| **System RAM Consumption** | Negligible (~500 MB) | ~2.5 GB weights + ~0.5 GB KV cache $\approx$ **3.0 GB** | 16 GB system RAM easily accommodates 8B CPU offload. |
| **Context Window Feasibility** | **8k to 12k Tokens** (KV Cache: 0.115 MB/token) | **8k to 16k Tokens** (KV Cache: 0.131 MB/token) | Both accommodate our ~7k-token DOM observation string. |
| **Inference Speed (TTFT)** | **~1.5 to 2.5 seconds** (Time-To-First-Token on 7k prompt) | **~6.0 to 12.0 seconds** (Prompt evaluation partially on CPU) | 3B is fast and responsive; 8B has noticeable prompt processing delay. |
| **Inference Speed (Gen)** | **~40 to 60 tokens/second** | **~8 to 15 tokens/second** (PCIe memory bus bottleneck) | 8B generation is 4–5x slower, taking ~1.5–3 min per multi-step trial. |
| **Browser Action Tool Calling** | **Moderate to Low:** Prone to hallucinating DOM indices, missing nested form attributes, or repeating clicks. | **High:** Excellent instruction following, accurate element grounding, reliable JSON schema parsing. | **8B is vastly superior for complex browser tasks (e.g., T6).** |
| **Zero-Cost Assurance** | **100% Local / $0.00** | **100% Local / $0.00** | Both eliminate all financial risk. |

### Technical Sizing Recommendation:
- **Phase 1 (Plumbing & Verification):** Test `llama3.2:3b` first to verify that `ChatOllama`, local HTTP transport, JSON schema decoding, and CDP verifiers work end-to-end at high speed.
- **Phase 2 (Autonomous Agent Benchmarking):** Use `llama3.1:8b` for actual behavioral trials. While slower (~10–12 tokens/sec), its reasoning capacity is the minimum threshold required to reliably interact with shopping cart DOM structures.

---

## 4. Minimal Reversible Changes to Support Ollama

To maintain the absolute integrity of your production runner, **no edits should be made to `protocol_v3_runner.py` directly**. Instead, we design the smallest, cleanly reversible interface.

### Option 1: Non-Invasive Factory Wrapper in `protocol_v3_runner.py` (Lines 444–451)
If modifying the runner under an explicit `--provider ollama` flag:
```python
# Smallest reversible model switch:
provider = getattr(args, "provider", "google")

if provider == "ollama":
    from browser_use.llm.ollama.chat import ChatOllama
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    # Pass num_ctx to allocate sufficient context for DOM observations
    llm = ChatOllama(
        model=model_name,
        host=host,
        ollama_options={"num_ctx": 12288, "temperature": 0.0}
    )
elif provider == "google":
    # Existing ChatGoogle logic remains 100% unchanged
    from browser_use import ChatGoogle
    llm = ChatGoogle(model=model_name, api_key=api_key, max_retries=1, retryable_status_codes=[])
```

### Option 2: Isolated Local Runner Script (`local_llama_runner.py`) (RECOMMENDED)
Rather than touching `protocol_v3_runner.py`, create a standalone script:
- Reuses existing task specifications (`TASK_INSTRUCTIONS`), browser session management (`BrowserSession`), and CDP verifiers (`verify_task_result`).
- Points directly to `ChatOllama(host="http://127.0.0.1:11434")`.
- Writes outputs to a dedicated results directory (`results/local_llama_pilot_runs/`).
- Leaves production `protocol_v3_runner.py` completely frozen.

### Update Required in `budget_controller.py`:
In [budget_controller.py](file:///C:/testing/research_execution_20261018/budget_controller.py#L98-L115), add local model IDs with zero cost to prevent `UnknownModelPricingError`:
```python
MODEL_PRICING_TABLE.update({
    "llama3.2:3b": {"input_per_million": 0.0, "output_per_million": 0.0},
    "llama3.1:8b": {"input_per_million": 0.0, "output_per_million": 0.0},
    "llama3.2": {"input_per_million": 0.0, "output_per_million": 0.0},
    "llama3.1": {"input_per_million": 0.0, "output_per_million": 0.0},
})
```

---

## 5. Air-Gapping & Preventing Silent Remote Fallbacks

To ensure that inference requests **never** leak to the internet or fall back to a paid API:

1. **Explicit Local Host Binding:**  
   Configure `host="http://127.0.0.1:11434"`. Never use default base URLs that resolve externally.
2. **Environment Variable Sanitization:**  
   Before initializing the local agent, strip all remote cloud API keys from the process memory:
   ```python
   for secret_key in ["GOOGLE_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY", "ANTHROPIC_API_KEY"]:
       os.environ.pop(secret_key, None)
   ```
3. **Hard Fail-Closed Exception Handling:**  
   Remove any `except Exception: fallback_to_cloud()` blocks. If Ollama is offline or returns an error, the runner must immediately crash with a `ConnectionRefusedError` and halt.
4. **Disable Automatic SDK Retries:**  
   Configure `client_params={"timeout": 120.0}` to allow slow CPU generation without triggering timeout loops.

---

## 6. Separate Local Pilot Design: `LOCAL_LLAMA_3ARM_PILOT`

To test the feasibility of local Llama without compromising the main empirical study:

### 1. Experimental Cohort Specification
- **Cohort Directory:** `results/local_llama_pilot_runs/`
- **Summary File:** `results/local_llama_summary.csv`
- **Schedule:** 1 Balanced Block (18 Trials: 6 Tasks $\times$ 3 Arms: ABS, ARIA, DATA-CFG).
- **Target Models:**
  - Pilot Phase A: `llama3.2:3b` (Quick verification of plumbing & schema compliance).
  - Pilot Phase B: `llama3.1:8b` (Full 18-trial benchmark).

### 2. Instrumentation & Telemetry to Capture
1. **Tool-Call Validity:**
   - Schema validation failures (Pydantic `ValidationError`).
   - Hallucinated element IDs (selecting indexes not in the serialized DOM).
   - Rate of invalid actions (e.g. attempting to click non-clickable nodes).
2. **Behavioral Success & Refusal Accuracy:**
   - Evaluated by the existing **independent CDP verifier** (`window.__cart__`, `window.__orderConfirmed__`).
   - Premature completion declarations (`done` called before task completed).
   - Repetitive action loops (repeatedly clicking the same element $\ge 3$ times).
3. **Latency & Hardware Telemetry:**
   - **TTFT (Time to First Token):** Time taken to process the 7k-token prompt.
   - **Generation Speed:** Output tokens generated per second.
   - **VRAM & System RAM Usage:** Peak memory recorded via `pynvml` / `nvidia-smi`.

---

## 7. Scientific Integrity & Data Separation

**CRITICAL METHODOLOGICAL DIRECTIVE: DO NOT POOL DATA.**

- **Preserve Runs 1–27:** The 27 valid trials in `results/3arm_runs/` completed under Gemini `gemini-3.1-flash-lite` remain completely untouched and authoritative.
- **Independent Research Framing:**  
  Introducing local Llama models transforms the research into a valuable **comparative study**:
  - *Research Question 3 (RQ3):* "Does additive semantic markup (ARIA vs DATA-CFG) provide greater performance amplification for compact, resource-constrained local models (Llama 3.1 8B) compared to large frontier cloud models (Gemini Flash)?"
  - This preserves scientific rigor and eliminates any risk of reviewer rejection for unprincipled data mixing.

---

## 8. Step-by-Step Operator Instructions (When Ready)

Because you authorized **offline inspection only**, no software has been installed and no models have been pulled. When you decide to proceed with local testing, the exact manual sequence will be:

```powershell
# Step 1: Download and install Ollama for Windows manually
# Visit: https://ollama.com/download/windows
# Run the installer: OllamaSetup.exe

# Step 2: In a terminal, pull the lightweight 3B model for testing
ollama pull llama3.2:3b

# Step 3: Run an offline verification probe (Zero remote calls)
C:\testing\.venv311\Scripts\python.exe -c "import httpx; r = httpx.get('http://127.0.0.1:11434/api/version'); print(r.json())"

# Step 4: Run a single local smoke trial in an isolated directory
# (Instructions will be provided upon your approval)
```

---

## 9. Final Audit Status & Execution Boundary

- **Live runner status:** **STOPPED.**
- **Remote API calls made:** **ZERO.**
- **Billed expenditure:** **$0.00.**
- **Local files modified:** **ZERO production files modified.** Only the feasibility report [LOCAL_LLAMA_FEASIBILITY_AUDIT.md](file:///C:/testing/research_execution_20261018/LOCAL_LLAMA_FEASIBILITY_AUDIT.md) was created.

The system is completely paused and awaiting your explicit instructions.

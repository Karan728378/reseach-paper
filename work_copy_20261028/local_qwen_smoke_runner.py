#!/usr/bin/env python3
"""
local_qwen_smoke_runner.py
==========================
Isolated, genuinely local browser-agent smoke test runner using Ollama (qwen3:4b).

Strict Safety & Research Integrity Invariants:
1. AIR-GAPPED LOCAL INFERENCE: Connects strictly to http://127.0.0.1:11434.
   All remote cloud API keys (Google, OpenAI, Groq, Anthropic) are purged from
   the process environment at startup. Zero cloud fallback is possible.
2. PROTECTED GEMINI DATASET: Existing results in results/3arm_runs/ and
   results/v3_3arm_summary.csv are NEVER touched, modified, or pooled.
3. ISOLATED RESULTS: Traces are saved to results/local_llama_pilot_runs/
   and recorded in results/local_llama_summary.csv.
4. INDEPENDENT CDP VERIFIER: Evaluates ground-truth state changes via
   Playwright CDP (window.__cart__). Does not rely on model self-reporting.
5. RESOURCE CONSTRAINED: Enforces strict context bounds (num_ctx=4096) and
   step ceilings (max_steps=3) to protect system RAM and VRAM.
"""

import argparse
import asyncio
import csv
import ctypes
import datetime
import http.server
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import httpx
from pydantic import ValidationError
from browser_use.llm.ollama.chat import ChatOllama, _unwrap_json_content
from browser_use.llm.ollama.serializer import OllamaMessageSerializer
from browser_use.llm.views import ChatInvokeCompletion, ChatInvokeUsage
from browser_use.llm.messages import BaseMessage
from browser_use.llm.exceptions import ModelProviderError

# ── 1. HARD SECURITY & ENVIRONMENT AIR-GAP ──────────────────────────────────
# Forcefully strip all remote cloud API keys from process memory
for _cloud_key in [
    "GOOGLE_API_KEY",
    "OPENAI_API_KEY",
    "GROQ_API_KEY",
    "ANTHROPIC_API_KEY",
    "MISTRAL_API_KEY",
    "OPENROUTER_API_KEY"
]:
    os.environ.pop(_cloud_key, None)

# Set offline flags where recognized
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
os.environ["ANONYMIZED_TELEMETRY"] = "false"
os.environ["BROWSER_USE_VERSION_CHECK"] = "false"
os.environ["BROWSER_USE_CLOUD_SYNC"] = "false"

# ── 2. PATHS & DIRECTORIES ──────────────────────────────────────────────────
ROOT_DIR = Path("C:/testing")
EXEC_DIR = ROOT_DIR / "research_execution_20261018"
PILOT_RESULTS_DIR = EXEC_DIR / "results" / "local_llama_pilot_runs"
PILOT_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
PILOT_SUMMARY_CSV = EXEC_DIR / "results" / "local_llama_summary.csv"

# ── 3. DOM ATTRIBUTE SETS & TASK SPECIFICATIONS ─────────────────────────────
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

EXTENDED_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-field", "data-product-id", "data-category", "data-category-slug",
    "data-amount", "data-rating", "data-review-count", "data-stock-status",
    "data-in-stock", "data-warranty", "data-lot-code", "data-action"
]

TASK_INSTRUCTIONS = {
    "T1": "Search for 'wireless headphones' and add the least expensive result to your cart.",
    "T2": "Find the product called 'Mechanical Keyboard Pro' and add it to your cart.",
    "T3": "Navigate to the Audio category. Compare the customer ratings of all products. Add the product with the second-highest customer rating to your cart.",
    "T4": "Search for 'ErgoGlide Mouse' and add it to your cart. Then complete the checkout process using these test details: Name: Jane Smith, Address: 123 Test Lane, City: Anytown, ZIP: 00000, Card Number: 4111111111111111, Expiry: 12/28, CVV: 123.",
    "T5": "There is one item in your cart. Navigate to the cart and remove it so the cart is empty.",
    "T6": "Navigate to the product details for 'SoundFlow Air 3' (SKU: wh-001). Retrieve the exact manufacturer warranty duration specified for this item."
}

# ── 4. RESOURCE MONITORING (RAM & VRAM) ──────────────────────────────────────
class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

def get_system_ram_mb() -> Tuple[float, float]:
    """Return (total_ram_mb, free_ram_mb)."""
    try:
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        return stat.ullTotalPhys / (1024 * 1024), stat.ullAvailPhys / (1024 * 1024)
    except Exception:
        return 0.0, 0.0

def get_gpu_vram_info() -> Dict[str, Any]:
    """Query NVIDIA-SMI for current VRAM utilization."""
    info = {"available": False, "total_vram_mb": 0, "used_vram_mb": 0, "free_vram_mb": 0}
    nvsmi_paths = [
        "C:\\Windows\\System32\\nvidia-smi.exe",
        "nvidia-smi"
    ]
    for exe in nvsmi_paths:
        try:
            res = subprocess.run(
                [exe, "--query-gpu=memory.total,memory.used,memory.free", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=3
            )
            if res.returncode == 0 and res.stdout.strip():
                parts = [p.strip() for p in res.stdout.strip().split(",")]
                if len(parts) >= 3:
                    info["available"] = True
                    info["total_vram_mb"] = float(parts[0])
                    info["used_vram_mb"] = float(parts[1])
                    info["free_vram_mb"] = float(parts[2])
                    break
        except Exception:
            continue
    return info

def check_preflight_resources(min_free_ram_mb: float = 1000.0) -> Tuple[bool, str]:
    """Verify that system RAM and VRAM are adequate before launching browser."""
    total_ram, free_ram = get_system_ram_mb()
    gpu_info = get_gpu_vram_info()

    if free_ram < min_free_ram_mb:
        return False, f"CRITICAL: Insufficient physical RAM ({free_ram:.1f} MB free, minimum required is {min_free_ram_mb} MB)."

    # Verify Ollama server connectivity
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/version")
        with urllib.request.urlopen(req, timeout=2) as resp:
            ver_data = json.loads(resp.read().decode())
            ollama_ver = ver_data.get("version", "unknown")
    except Exception as e:
        return False, f"CRITICAL: Ollama is unreachable at http://127.0.0.1:11434 ({e}). Please start Ollama before running."

    # Verify model is available
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as resp:
            tags_data = json.loads(resp.read().decode())
            models = [m.get("name") for m in tags_data.get("models", [])]
            if not any("qwen3:4b" in m for m in models):
                return False, f"CRITICAL: Model 'qwen3:4b' not found in Ollama tags ({models})."
    except Exception as e:
        return False, f"CRITICAL: Failed to query Ollama model tags ({e})."

    vram_str = f"{gpu_info['used_vram_mb']:.0f}/{gpu_info['total_vram_mb']:.0f} MB" if gpu_info["available"] else "N/A"
    return True, f"Ollama {ollama_ver} OK | RAM: {free_ram:.0f} MB free | VRAM: {vram_str}"

# ── 5. LOCAL DEMO SHOP HTTP SERVER ──────────────────────────────────────────
def ensure_server(port: int = 8080):
    """Ensure local HTTP server is running to serve mock shop variants."""
    try:
        resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/variants/v0-baseline/index.html", timeout=1)
        if resp.status == 200:
            return None
    except Exception:
        pass

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT_DIR), **kwargs)
        def log_message(self, format, *args):
            pass

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.5)
    return httpd

# ── 6. INDEPENDENT CDP GROUND-TRUTH VERIFIER ────────────────────────────────
def verify_task_result(
    task_id: str,
    cart: list,
    order_confirmed: bool,
    last_order_items: list,
    final_text: str = "",
    pre_cart_count: int = None
) -> dict:
    """
    Independent state-based verifier. Evaluates JavaScript runtime state in DOM.
    Never relies on model self-reporting.
    """
    if task_id == "T1":
        has_wh001 = any(isinstance(i, dict) and i.get("sku") == "wh-001" for i in cart)
        return {
            "success": has_wh001,
            "score": 1.0 if has_wh001 else 0.0,
            "details": {"target_sku": "wh-001", "cart_skus": [i.get("sku") for i in cart if isinstance(i, dict)]}
        }
    elif task_id == "T2":
        # Strict: Mechanical Keyboard Pro (mkp-001) must be present in window.__cart__
        cart_skus = [i.get("sku") for i in cart if isinstance(i, dict)]
        has_mkp = any(s == "mkp-001" for s in cart_skus)
        return {
            "success": has_mkp,
            "score": 1.0 if has_mkp else 0.0,
            "details": {"target_sku": "mkp-001", "cart_skus": cart_skus}
        }
    elif task_id == "T3":
        cart_skus = [i.get("sku") for i in cart if isinstance(i, dict)]
        is_exact_wh002 = (len(cart_skus) == 1 and cart_skus[0] == "wh-002")
        return {
            "success": is_exact_wh002,
            "score": 1.0 if is_exact_wh002 else 0.0,
            "details": {"target_sku": "wh-002", "cart_skus": cart_skus}
        }
    elif task_id == "T4":
        has_mouse = any(isinstance(i, dict) and i.get("sku") == "mse-001" for i in last_order_items)
        success = bool(order_confirmed and has_mouse)
        return {
            "success": success,
            "score": 1.0 if success else 0.0,
            "details": {"order_confirmed": order_confirmed, "has_mouse": has_mouse}
        }
    elif task_id == "T5":
        is_empty = (isinstance(cart, list) and len(cart) == 0)
        precondition_ok = (pre_cart_count == 1)
        success = bool(is_empty and precondition_ok)
        return {
            "success": success,
            "score": 1.0 if success else 0.0,
            "details": {"cart_empty": is_empty, "precondition_ok": precondition_ok, "pre_cart_count": pre_cart_count}
        }
    elif task_id == "T6":
        text = (final_text or "").strip()
        refusal_keywords = r'(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not|unlisted|missing|not stated|not found|not listed|not mentioned|not provided|not specified|unavailable|absent|nowhere)'
        warranty_terms = r'(warranty|guarantee|duration|terms?|coverage|period|policy)'
        refusal_pattern = re.compile(rf'\b{refusal_keywords}\b.*?\b{warranty_terms}\b|\b{warranty_terms}\b.*?\b{refusal_keywords}\b', re.IGNORECASE | re.DOTALL)
        hallucination_pattern = re.compile(r'\b(\d+|one|two|three|four|five|six|twelve|twenty-four|thirty-six)\s*(-|\s)?\s*(months?|mos?|years?|yrs?|days?)\b', re.IGNORECASE)
        has_refusal = bool(refusal_pattern.search(text))
        has_hallucination = bool(hallucination_pattern.search(text))
        success = has_refusal and not has_hallucination
        return {
            "success": success,
            "score": 1.0 if success else 0.0,
            "details": {"refusal_detected": has_refusal, "hallucination_detected": has_hallucination, "text_excerpt": text[:100]}
        }
    return {"success": False, "score": 0.0, "details": {"error": f"Unknown task {task_id}"}}

# ── 7. MAIN ISOLATED LIVE TRIAL EXECUTION ───────────────────────────────────
def get_next_run_info(pilot_dir: Path) -> Tuple[str, Path]:
    """Find next sequential run ID and ensure no prior run trace is overwritten."""
    pilot_dir.mkdir(parents=True, exist_ok=True)
    existing = list(pilot_dir.glob("qwen3_smoke_run_*.json"))
    max_idx = 0
    for p in existing:
        m = re.search(r"qwen3_smoke_run_(\d+)", p.name)
        if m:
            val = int(m.group(1))
            if val > max_idx:
                max_idx = val
    next_idx = max_idx + 1
    run_id = f"qwen3_smoke_{next_idx:03d}"
    run_file = pilot_dir / f"qwen3_smoke_run_{next_idx:03d}.json"
    return run_id, run_file


@dataclass
class InstrumentedChatOllama(ChatOllama):
    """
    Subclass of ChatOllama that records fine-grained Ollama latency metadata
    (prompt_eval_duration, eval_duration, token counts, wall clock time)
    per invocation without modifying installed package files.
    """
    run_id: str = "unknown"
    call_history: List[Dict[str, Any]] = field(default_factory=list)

    async def ainvoke(
        self, messages: list[BaseMessage], output_format: Any = None, **kwargs: Any
    ) -> ChatInvokeCompletion[Any]:
        ollama_messages = OllamaMessageSerializer.serialize_messages(messages)
        call_idx = len(self.call_history) + 1
        t_start = datetime.datetime.now().isoformat()
        t0 = time.perf_counter()

        call_record: Dict[str, Any] = {
            "call_index": call_idx,
            "run_id": self.run_id,
            "timestamp_start": t_start,
            "timestamp_end": None,
            "wall_clock_seconds": None,
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
            "prompt_eval_duration_ms": None,
            "eval_duration_ms": None,
            "load_duration_ms": None,
            "total_duration_ms": None,
            "status": "pending",
            "error_type": None,
            "error": None
        }

        try:
            options, top_level = self._split_chat_options()
            if output_format is None:
                response = await self.get_client().chat(
                    model=self.model,
                    messages=ollama_messages,
                    options=options,
                    **top_level,
                )
                parsed = response.message.content or ""
            else:
                schema = output_format.model_json_schema()
                response = await self.get_client().chat(
                    model=self.model,
                    messages=ollama_messages,
                    format=schema,
                    options=options,
                    **top_level,
                )
                raw_content = response.message.content or ""
                completion = _unwrap_json_content(raw_content)
                try:
                    parsed = output_format.model_validate_json(completion)
                except ValidationError as e:
                    raise ModelProviderError(
                        message=f"Ollama returned invalid JSON for structured output: {e}",
                        model=self.name,
                    ) from e

            wall_sec = round(time.perf_counter() - t0, 4)
            p_eval_ns = getattr(response, "prompt_eval_duration", None)
            eval_ns = getattr(response, "eval_duration", None)
            load_ns = getattr(response, "load_duration", None)
            tot_ns = getattr(response, "total_duration", None)

            p_tokens = getattr(response, "prompt_eval_count", None)
            c_tokens = getattr(response, "eval_count", None)
            tot_tokens = (p_tokens + c_tokens) if (p_tokens is not None and c_tokens is not None) else None

            call_record["timestamp_end"] = datetime.datetime.now().isoformat()
            call_record["wall_clock_seconds"] = wall_sec
            call_record["prompt_tokens"] = p_tokens
            call_record["completion_tokens"] = c_tokens
            call_record["total_tokens"] = tot_tokens
            call_record["prompt_eval_duration_ms"] = round(p_eval_ns / 1_000_000, 2) if p_eval_ns is not None else None
            call_record["eval_duration_ms"] = round(eval_ns / 1_000_000, 2) if eval_ns is not None else None
            call_record["load_duration_ms"] = round(load_ns / 1_000_000, 2) if load_ns is not None else None
            call_record["total_duration_ms"] = round(tot_ns / 1_000_000, 2) if tot_ns is not None else None
            call_record["status"] = "success"
            call_record["error_type"] = None
            call_record["error"] = None

            self.call_history.append(call_record)

            usage = None
            if p_tokens is not None and c_tokens is not None:
                usage = ChatInvokeUsage(
                    prompt_tokens=p_tokens,
                    prompt_cached_tokens=None,
                    prompt_cache_creation_tokens=None,
                    prompt_image_tokens=None,
                    completion_tokens=c_tokens,
                    total_tokens=tot_tokens or (p_tokens + c_tokens)
                )

            return ChatInvokeCompletion(completion=parsed, usage=usage)

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

        except Exception as e:
            wall_sec = round(time.perf_counter() - t0, 4)
            call_record["timestamp_end"] = datetime.datetime.now().isoformat()
            call_record["wall_clock_seconds"] = wall_sec
            is_timeout = isinstance(e, (asyncio.TimeoutError, httpx.TimeoutException)) or "timed out" in str(e).lower()
            call_record["status"] = "timeout" if is_timeout else "error"
            call_record["error_type"] = type(e).__name__
            call_record["error"] = str(e)
            call_record["prompt_tokens"] = None
            call_record["completion_tokens"] = None
            call_record["total_tokens"] = None
            call_record["prompt_eval_duration_ms"] = None
            call_record["eval_duration_ms"] = None
            call_record["load_duration_ms"] = None
            call_record["total_duration_ms"] = None
            self.call_history.append(call_record)

            if isinstance(e, ModelProviderError):
                raise
            raise ModelProviderError(message=str(e), model=self.name) from e


async def execute_local_smoke_trial(
    task_id: str = "T2",
    arm: str = "DATA-CFG",
    variant: str = "v3-data-attrs",
    max_steps: int = 3,
    model_name: str = "qwen3:4b",
    host: str = "http://127.0.0.1:11434",
    num_ctx: int = 4096,
    port: int = 8080
) -> dict:
    """
    Execute exactly ONE real browser-agent smoke trial using local Ollama.
    """
    from browser_use import Agent, BrowserSession
    from browser_use.llm.ollama.chat import ChatOllama

    run_id, run_file = get_next_run_info(PILOT_RESULTS_DIR)

    print("=" * 75)
    print("LOCAL QWEN3 4B BROWSER-AGENT SMOKE TEST")
    print("=" * 75)
    print(f"Run ID:                {run_id}")
    print(f"Target Output Trace:   {run_file.name}")
    print(f"Model ID:              {model_name}")
    print(f"Inference Host:        {host} (AIR-GAPPED LOCALHOST ONLY)")
    print(f"Allocated Context:     {num_ctx} tokens")
    print(f"Task ID:               {task_id} -> {TASK_INSTRUCTIONS[task_id]}")
    print(f"Experimental Arm:      {arm}")
    print(f"DOM Variant:           {variant}")
    print(f"Max Agent Steps:       {max_steps}")
    print(f"Mock Shop Server:      http://127.0.0.1:{port}")
    print(f"Output Directory:      {PILOT_RESULTS_DIR}")
    print(f"Financial Guarantee:   $0.00000 USD (Zero Cloud Inference)")
    print("=" * 75)

    # 1. Preflight Resource Check
    ok, status_msg = check_preflight_resources(min_free_ram_mb=1000.0)
    print(f"[PREFLIGHT] {status_msg}")
    if not ok:
        raise RuntimeError(f"Preflight resource check failed: {status_msg}")

    # 2. Ensure local web server
    ensure_server(port=port)
    start_url = f"http://127.0.0.1:{port}/variants/{variant}/index.html#home"
    attrs = EXTENDED_ATTRIBUTES if arm == "DATA-CFG" else DEFAULT_INCLUDE_ATTRIBUTES

    # 3. Initialize Local InstrumentedChatOllama with fine-grained latency tracking
    llm = InstrumentedChatOllama(
        model=model_name,
        host=host,
        timeout=180.0,
        run_id=run_id,
        ollama_options={
            "num_ctx": num_ctx,
            "temperature": 0.0
        }
    )

    # 4. Initialize Headless Browser Session
    session = BrowserSession(
        headless=True,
        viewport={"width": 1920, "height": 1080},
        keep_alive=True
    )
    await session.start()

    t0 = time.monotonic()
    t_start = datetime.datetime.now().isoformat()
    status = "completed"
    termination_reason = "normal"
    error_message = ""
    total_steps = 0
    final_text = ""
    captured_actions = []
    cart_items = []
    order_confirmed = False
    last_order_items = []
    verifier_outcome = {"success": False, "score": 0.0, "details": {}}

    try:
        # Pre-seed T5 if requested
        pre_cart_count = None
        if task_id == "T5":
            page = await session.get_current_page()
            await page.goto(start_url, wait_until="domcontentloaded")
            await page.evaluate("""() => {
                window.__cart__ = [{sku: 'wh-001', name: 'SoundFlow Air 3', price: 49.99, quantity: 1}];
                if (window.updateCartUI) window.updateCartUI();
            }""")
            pre_cart_count = 1

        # Instantiate Agent with explicit bounded timeouts
        agent = Agent(
            task=TASK_INSTRUCTIONS[task_id],
            llm=llm,
            browser_session=session,
            use_vision=False,
            max_steps=max_steps,
            include_attributes=attrs,
            initial_actions=[{"navigate": {"url": start_url, "new_tab": False}}],
            max_failures=1,
            final_response_after_failure=False,
            max_history_items=6,  # browser-use requires None or > 5; bounds sliding history window
            step_timeout=180,
            llm_timeout=180
        )

        print(f"\n[EXECUTION] Launching autonomous browser agent ({run_id})...")
        history = await agent.run(max_steps=max_steps)
        total_steps = len(history.history) if hasattr(history, "history") else 0
        final_text = history.final_result() if hasattr(history, "final_result") else ""

        # Accurate termination classification: distinguish clean completion from timeouts
        is_done = history.is_done() if hasattr(history, "is_done") else False
        has_step_timeout = False
        step_err = ""
        if hasattr(agent, "state") and getattr(agent.state, "consecutive_failures", 0) > 0:
            for res in getattr(agent.state, "last_result", []):
                if hasattr(res, "error") and res.error:
                    step_err = str(res.error)
                    if "timed out" in step_err.lower():
                        has_step_timeout = True

        if is_done:
            status = "completed"
            termination_reason = "agent_completed"
        elif has_step_timeout:
            status = "timed_out"
            termination_reason = "llm_or_step_timeout"
            error_message = step_err or "Step timed out"
        else:
            status = "max_steps_reached"
            termination_reason = "max_steps_reached"

        # Capture tool/action call history and per-step latency
        step_durations = []
        if hasattr(history, "history"):
            for step_idx, step in enumerate(history.history):
                step_dur = None
                if hasattr(step, "metadata") and step.metadata:
                    step_dur = round(step.metadata.step_end_time - step.metadata.step_start_time, 3)
                    step_durations.append(step_dur)

                step_data = {
                    "step": step_idx + 1,
                    "duration_seconds": step_dur,
                    "thinking": "",
                    "actions": []
                }
                if hasattr(step, "model_output") and step.model_output:
                    out = step.model_output
                    step_data["thinking"] = getattr(out, "current_state", {}).get("evaluation_previous_goal", "") if isinstance(getattr(out, "current_state", None), dict) else str(getattr(out, "current_state", ""))
                    if hasattr(out, "action"):
                        for act in out.action:
                            step_data["actions"].append(str(act))
                captured_actions.append(step_data)
                dur_str = f"{step_dur}s" if step_dur is not None else "n/a"
                print(f"  -> Step {step_idx + 1} ({dur_str}): {step_data['actions']}")

        # 5. Independent Ground-Truth Evaluation via CDP
        try:
            page = await session.get_current_page()
            raw_cart = await page.evaluate("() => window.__cart__ || []")
            raw_order_confirmed = await page.evaluate("() => Boolean(window.__orderConfirmed__)")
            raw_last_order = await page.evaluate("() => (window.__lastOrder__ && window.__lastOrder__.items) || window.__lastOrderItems__ || []")

            cart_items = json.loads(raw_cart) if isinstance(raw_cart, str) else raw_cart
            order_confirmed = bool(raw_order_confirmed)
            last_order_items = json.loads(raw_last_order) if isinstance(raw_last_order, str) else raw_last_order

            verifier_outcome = verify_task_result(
                task_id=task_id,
                cart=cart_items,
                order_confirmed=order_confirmed,
                last_order_items=last_order_items,
                final_text=final_text,
                pre_cart_count=pre_cart_count
            )
        except Exception as eval_err:
            print(f"  -> [WARNING] Post-run CDP verification failed: {eval_err}")

    except asyncio.CancelledError as ce:
        if status == "pending":
            status = "timed_out"
            termination_reason = "cancelled_by_watchdog"
            error_message = f"Agent execution cancelled: {type(ce).__name__}"
        print(f"\n[CANCELLED] Agent execution cancelled: {error_message}")
        try:
            page = await session.get_current_page()
            raw_cart = await page.evaluate("() => window.__cart__ || []")
            cart_items = json.loads(raw_cart) if isinstance(raw_cart, str) else raw_cart
            verifier_outcome = verify_task_result(
                task_id=task_id,
                cart=cart_items,
                order_confirmed=False,
                last_order_items=[],
                final_text="",
                pre_cart_count=pre_cart_count
            )
        except Exception:
            pass
    except Exception as e:
        if status == "pending":
            status = "failed"
            termination_reason = "exception"
            error_message = str(e)
        print(f"\n[ERROR] Exception encountered during agent run: {error_message}")
    finally:
        try:
            await asyncio.shield(session.stop())
        except Exception:
            pass

    elapsed = round(time.monotonic() - t0, 3)
    t_end = datetime.datetime.now().isoformat()
    gpu_after = get_gpu_vram_info()
    total_ram, free_ram_after = get_system_ram_mb()

    # 6. Build Record
    record = {
        "trial_type": "local_qwen3_smoke_test",
        "run_id": run_id,
        "model_id": model_name,
        "ollama_host": host,
        "context_window": num_ctx,
        "task_id": task_id,
        "arm": arm,
        "variant": variant,
        "instruction": TASK_INSTRUCTIONS[task_id],
        "timestamps": {"start": t_start, "end": t_end, "duration_seconds": elapsed},
        "step_durations_seconds": step_durations,
        "total_steps": total_steps,
        "status": status,
        "termination_reason": termination_reason,
        "error_message": error_message,
        "agent_final_text": final_text,
        "actions_executed": captured_actions,
        "terminal_cart_state": cart_items,
        "verifier_outcome": verifier_outcome,
        "model_call_telemetry": getattr(llm, "call_history", []),
        "financial_cost_usd": 0.00000,
        "resource_snapshot": {
            "free_ram_mb": round(free_ram_after, 1),
            "gpu_vram": gpu_after
        }
    }

    # 7. Save JSON Trace to unique file
    with open(run_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)

    # 8. Append to Pilot CSV
    csv_exists = PILOT_SUMMARY_CSV.exists()
    with open(PILOT_SUMMARY_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not csv_exists:
            writer.writerow([
                "run_id", "model", "task_id", "arm", "variant", "success", "score",
                "total_steps", "duration_seconds", "status", "termination_reason",
                "error_message", "cart_skus", "cost_usd", "timestamp"
            ])
        cart_skus = [i.get("sku") for i in cart_items if isinstance(i, dict)]
        writer.writerow([
            run_id, model_name, task_id, arm, variant,
            verifier_outcome["success"], verifier_outcome["score"],
            total_steps, elapsed, status, termination_reason,
            error_message, str(cart_skus), 0.00000, t_end
        ])

    print("\n" + "=" * 75)
    print("VERIFICATION & TELEMETRY SUMMARY")
    print("=" * 75)
    print(f"Run ID:               {run_id}")
    print(f"Status:               {status.upper()} ({termination_reason})")
    print(f"Steps Executed:       {total_steps} of {max_steps}")
    print(f"Step Durations:       {step_durations} seconds")
    print(f"Elapsed Time:         {elapsed} seconds")
    if getattr(llm, "call_history", None):
        print(f"Model Calls Logged:   {len(llm.call_history)}")
        for c in llm.call_history:
            p_tok = c.get('prompt_tokens') if c.get('prompt_tokens') is not None else 'n/a'
            e_tok = c.get('completion_tokens') if c.get('completion_tokens') is not None else 'n/a'
            p_ms = f"{c.get('prompt_eval_duration_ms')}ms" if c.get('prompt_eval_duration_ms') is not None else 'n/a'
            e_ms = f"{c.get('eval_duration_ms')}ms" if c.get('eval_duration_ms') is not None else 'n/a'
            print(f"  -> Call #{c['call_index']} ({c['status']}): prompt={p_tok} tok ({p_ms}), eval={e_tok} tok ({e_ms}), wall={c['wall_clock_seconds']}s")
    print(f"Terminal Cart State:  {cart_items}")
    print(f"Independent Verifier: SUCCESS = {verifier_outcome['success']} (Score: {verifier_outcome['score']})")
    print(f"Verifier Details:     {verifier_outcome['details']}")
    print(f"Financial Cost:       $0.00000 USD (Billed spend: $0.00)")
    print(f"Saved Trace:          {run_file}")
    print(f"Saved Summary:        {PILOT_SUMMARY_CSV}")
    print("=" * 75)

    return record

# ── 8. CLI ENTRYPOINT ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Isolated Qwen3 4B Local Browser-Agent Smoke Test")
    parser.add_argument("--task", type=str, default="T2", choices=list(TASK_INSTRUCTIONS.keys()), help="Task ID (default: T2)")
    parser.add_argument("--arm", type=str, default="DATA-CFG", choices=["ABS", "ARIA", "DATA-CFG"], help="Experimental Arm (default: DATA-CFG)")
    parser.add_argument("--variant", type=str, default="v3-data-attrs", help="Website variant (default: v3-data-attrs)")
    parser.add_argument("--max-steps", type=int, default=3, help="Maximum agent steps (default: 3)")
    parser.add_argument("--model", type=str, default="qwen3:4b", help="Ollama model tag (default: qwen3:4b)")
    parser.add_argument("--host", type=str, default="http://127.0.0.1:11434", help="Ollama host endpoint")
    parser.add_argument("--num-ctx", type=int, default=4096, help="Allocated context length (default: 4096)")
    parser.add_argument("--port", type=int, default=8080, help="Local mock shop HTTP server port (default: 8080)")
    args = parser.parse_args()

    asyncio.run(execute_local_smoke_trial(
        task_id=args.task,
        arm=args.arm,
        variant=args.variant,
        max_steps=args.max_steps,
        model_name=args.model,
        host=args.host,
        num_ctx=args.num_ctx,
        port=args.port
    ))

if __name__ == "__main__":
    main()

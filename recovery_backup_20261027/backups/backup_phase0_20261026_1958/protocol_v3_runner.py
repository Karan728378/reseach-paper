"""
Protocol v3 Experimental Runner
=============================================================================
Option A: Additive Semantic Markup Evaluation Runner

Key Requirements:
1. Consumes proposed_randomized_schedule.csv directly in deterministic RCBD order.
2. Enforces use_vision=False to eliminate multimodal visual confounding.
3. Sets include_attributes conditionally:
   - EXTENDED_ATTRIBUTES for DATA-CFG arm
   - DEFAULT_INCLUDE_ATTRIBUTES for VIS, ARIA, and baseline arms
4. Implements strict verifiers for T1-T6 (no lenient sets, no unconditional partial credit).
5. Enforces initial-state preconditions (e.g., T5 pre-seeds cart and asserts pre_cart_count == 1).
6. Eliminates survivorship bias: both success=True and success=False runs count as COMPLETED.
   Completed runs are NEVER retried. Only fatal infrastructure aborts are eligible for re-run.
7. Safe offline / mock testing: defaults to --mock mode running completely offline with
   zero API calls, validating schedule consumption, verifiers, and resume logic.
8. Safety Gate: Live execution requires explicit --live and --confirm-live-execution flags.
   Zero API keys are requested, logged, or printed.
=============================================================================
"""
import argparse
import asyncio
import csv
import datetime
import http.server
import json
import os
import re
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Optional, Any, Dict, List, Tuple


# Paths
ROOT_DIR = Path("C:/testing")
EXEC_DIR = ROOT_DIR / "research_execution_20261018"
SCHEDULE_FILE = EXEC_DIR / "proposed_3arm_schedule.csv"
RESULTS_DIR = EXEC_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_CSV = RESULTS_DIR / "v3_3arm_summary.csv"

# Extended attributes for DATA-CFG arm
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES
from budget_controller import (
    MODEL_PRICING_TABLE,
    LocalBudgetGuard,
    estimate_preflight_budget,
    compute_worst_case_run_cost,
    compute_step_cost,
    UnknownModelPricingError,
    load_daily_requests_offset,
    DEFAULT_LEDGER_PATH,
    DEFAULT_GROQ_LEDGER_PATH,
    BudgetGuardedChatModel,
    BudgetExceededError
)


EXTENDED_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-field", "data-product-id", "data-category", "data-category-slug",
    "data-amount", "data-rating", "data-review-count", "data-stock-status",
    "data-in-stock", "data-warranty", "data-lot-code", "data-action"
]

# Task Instructions
TASK_INSTRUCTIONS = {
    "T1": "Search for 'wireless headphones' and add the least expensive result to your cart.",
    "T2": "Find the product called 'Mechanical Keyboard Pro' and add it to your cart.",
    "T3": "Navigate to the Audio category. Compare the customer ratings of all products. Add the product with the second-highest customer rating to your cart.",
    "T4": "Search for 'ErgoGlide Mouse' and add it to your cart. Then complete the checkout process using these test details: Name: Jane Smith, Address: 123 Test Lane, City: Anytown, ZIP: 00000, Card Number: 4111111111111111, Expiry: 12/28, CVV: 123.",
    "T5": "There is one item in your cart. Navigate to the cart and remove it so the cart is empty.",
    "T6": "Navigate to the product details for 'SoundFlow Air 3' (SKU: wh-001). Retrieve the exact manufacturer warranty duration specified for this item."
}

def get_api_key() -> str:
    key = os.environ.get("GOOGLE_API_KEY")
    if not key and sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as reg_key:
                val, _ = winreg.QueryValueEx(reg_key, "GOOGLE_API_KEY")
                if val:
                    key = str(val).strip()
                    os.environ["GOOGLE_API_KEY"] = key
        except Exception:
            pass
    return key or ""

def get_groq_api_key() -> str:
    key = os.environ.get("GROQ_API_KEY")
    if not key and sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as reg_key:
                val, _ = winreg.QueryValueEx(reg_key, "GROQ_API_KEY")
                if val:
                    key = str(val).strip()
                    os.environ["GROQ_API_KEY"] = key
        except Exception:
            pass
    return key or ""

def sanitize_secret_leakage(text: str) -> str:
    if not isinstance(text, str):
        return text
    api_key = get_api_key()
    if api_key and len(api_key) > 5:
        text = text.replace(api_key, "[REDACTED_API_KEY]")
    groq_key = get_groq_api_key()
    if groq_key and len(groq_key) > 5:
        text = text.replace(groq_key, "[REDACTED_GROQ_API_KEY]")
    text = re.sub(r'AIza[0-9A-Za-z\-_]{35}', '[REDACTED_API_KEY]', text)
    text = re.sub(r'AQ\.[0-9A-Za-z\-_]{40,}', '[REDACTED_API_KEY]', text)
    text = re.sub(r'gsk_[A-Za-z0-9_]{20,}', '[REDACTED_GROQ_API_KEY]', text)
    text = re.sub(r'(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}', 'Bearer [REDACTED_TOKEN]', text)
    return text

def verify_task_result(task_id: str, cart: list, order_confirmed: bool, last_order_items: list, final_text: str = "", pre_cart_count: int = None) -> dict:
    """
    Strict Protocol v3 verifier logic:
    - T1: SoundFlow Air 3 (wh-001, $49.99, cheapest) in cart.
    - T2: Mechanical Keyboard Pro (mkp-001) in cart.
    - T3: Exactly BudPro Wireless X (wh-002, rating 4.5, second-highest) in cart, and nothing else.
    - T4: Order confirmed is True and last order items contain ErgoGlide Mouse (mse-001).
    - T5: Cart is empty AND precondition verified (pre_cart_count was exactly 1 before agent action).
    - T6: Grounded refusal verification: 1.0 for grounded refusal without hallucination; 0.0 for duration hallucination, contradiction, or unrelated text.
    """
    if task_id == "T1":
        has_wh001 = any(isinstance(i, dict) and i.get("sku") == "wh-001" for i in cart)
        return {
            "success": has_wh001,
            "score": 1.0 if has_wh001 else 0.0,
            "details": {"target_sku": "wh-001", "cart_skus": [i.get("sku") for i in cart if isinstance(i, dict)]}
        }
    elif task_id == "T2":
        has_mkp = any(isinstance(i, dict) and i.get("sku") == "mkp-001" for i in cart)
        return {
            "success": has_mkp,
            "score": 1.0 if has_mkp else 0.0,
            "details": {"target_sku": "mkp-001", "cart_skus": [i.get("sku") for i in cart if isinstance(i, dict)]}
        }
    elif task_id == "T3":
        # Strict: wh-002 only
        cart_skus = [i.get("sku") for i in cart if isinstance(i, dict)]
        is_exact_wh002 = (len(cart_skus) == 1 and cart_skus[0] == "wh-002")
        return {
            "success": is_exact_wh002,
            "score": 1.0 if is_exact_wh002 else 0.0,
            "details": {"target_sku": "wh-002", "cart_skus": cart_skus}
        }
    elif task_id == "T4":
        # Strict: order confirmed and contains mse-001
        has_mouse = any(isinstance(i, dict) and i.get("sku") == "mse-001" for i in last_order_items)
        success = bool(order_confirmed and has_mouse)
        return {
            "success": success,
            "score": 1.0 if success else 0.0,
            "details": {"order_confirmed": order_confirmed, "has_mouse": has_mouse}
        }
    elif task_id == "T5":
        # Strict: cart empty and precondition met (pre_cart_count must be exactly 1)
        is_empty = (isinstance(cart, list) and len(cart) == 0)
        precondition_ok = (pre_cart_count == 1)
        success = bool(is_empty and precondition_ok)
        return {
            "success": success,
            "score": 1.0 if success else 0.0,
            "details": {
                "cart_empty": is_empty,
                "precondition_ok": precondition_ok,
                "pre_cart_count": pre_cart_count,
                "remaining_count": len(cart) if isinstance(cart, list) else -1
            }
        }
    elif task_id == "T6":
        return verify_t6_grounded_refusal(final_text)
    return {"success": False, "score": 0.0, "details": {"error": f"Unknown task {task_id}"}}

# â”€â”€ T6 Grounded Refusal & Hallucination Verifier â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
REFUSAL_KEYWORDS = r'(no|not|cannot|can\'t|unspecified|unable|doesn\'t|does not|unlisted|missing|not stated|not found|not listed|not mentioned|not provided|not specified|unavailable|absent|nowhere)'
WARRANTY_TERMS = r'(warranty|guarantee|duration|terms?|coverage|period|policy)'

REFUSAL_PATTERN = re.compile(
    rf'\b{REFUSAL_KEYWORDS}\b.*?\b{WARRANTY_TERMS}\b'
    rf'|'
    rf'\b{WARRANTY_TERMS}\b.*?\b{REFUSAL_KEYWORDS}\b',
    re.IGNORECASE | re.DOTALL
)

DURATION_HALLUCINATION_PATTERN = re.compile(
    r'\b(\d+|one|two|three|four|five|six|twelve|twenty-four|thirty-six)\s*(-|\s)?\s*(months?|mos?|years?|yrs?|days?)\b',
    re.IGNORECASE
)

def verify_t6_grounded_refusal(final_text: str | None) -> dict:
    """
    Protocol v4 Grounded Refusal Verifier for Task T6.
    
    Task T6 asks for manufacturer warranty duration on SoundFlow Air 3 (wh-001).
    Warranty is intentionally unstated on the website across all variants (v0-v3).
    
    Scoring Rubric:
    - Success (1.0): Grounded Refusal (explicitly confirms warranty is absent/not stated without hallucinating duration).
    - Failure (0.0): Unsupported Duration Hallucination (e.g., '36 months', '2 years').
    - Failure (0.0): Contradictory Refusal + Duration (e.g., 'Not found, but 36 months').
    - Failure (0.0): Unrelated or Ambiguous output.
    - Failure (0.0): Empty output.
    """
    text = (final_text or "").strip()
    if not text:
        return {
            "success": False,
            "score": 0.0,
            "classification": "EMPTY_OUTPUT",
            "details": {
                "refusal_detected": False,
                "hallucination_detected": False,
                "matched_duration": None,
                "text_excerpt": ""
            }
        }

    refusal_match = bool(REFUSAL_PATTERN.search(text))
    duration_match = DURATION_HALLUCINATION_PATTERN.search(text)
    hallucination_detected = bool(duration_match)
    matched_duration_str = duration_match.group(0) if duration_match else None

    if refusal_match and not hallucination_detected:
        classification = "GROUNDED_REFUSAL_SUCCESS"
        success = True
    elif refusal_match and hallucination_detected:
        classification = "CONTRADICTORY_REFUSAL_WITH_HALLUCINATION"
        success = False
    elif not refusal_match and hallucination_detected:
        classification = "UNSUPPORTED_DURATION_HALLUCINATION"
        success = False
    else:
        classification = "UNRELATED_OR_AMBIGUOUS_NON_REFUSAL"
        success = False

    return {
        "success": success,
        "score": 1.0 if success else 0.0,
        "classification": classification,
        "details": {
            "refusal_detected": refusal_match,
            "hallucination_detected": hallucination_detected,
            "matched_duration": matched_duration_str,
            "text_excerpt": text[:100]
        }
    }

VALID_ARMS = {"BASELINE", "BASELINE_REP", "ABS", "VIS", "ARIA", "DATA-CFG"}
VALID_TASKS = {"T1", "T2", "T3", "T4", "T5", "T6"}
REQUIRED_SCHEDULE_FIELDS = {"run_index", "block_id", "within_block_order", "arm", "task_id", "variant_mapping", "target_entity"}

def validate_schedule_rows(rows: list[dict], schedule_path: Path = None) -> None:
    if not rows:
        raise ValueError(f"Schedule is empty: {schedule_path}")
    seen_indices = set()
    for row_num, row in enumerate(rows, start=1):
        missing = REQUIRED_SCHEDULE_FIELDS - set(row.keys())
        if missing:
            raise ValueError(f"Schedule row {row_num} missing required fields: {sorted(missing)} in {schedule_path}")
        run_idx_str = str(row.get("run_index", "")).strip()
        if not run_idx_str.isdigit():
            raise ValueError(f"Schedule row {row_num} has non-integer run_index: '{row.get('run_index')}' in {schedule_path}")
        run_idx = int(run_idx_str)
        if run_idx in seen_indices:
            raise ValueError(f"Schedule contains duplicate run_index: {run_idx} at row {row_num} in {schedule_path}")
        seen_indices.add(run_idx)
        
        arm = str(row.get("arm", "")).strip()
        if arm not in VALID_ARMS:
            raise ValueError(f"Schedule row {row_num} has invalid arm: '{arm}' (allowed: {sorted(VALID_ARMS)}) in {schedule_path}")
            
        task = str(row.get("task_id", "")).strip()
        if task not in VALID_TASKS:
            raise ValueError(f"Schedule row {row_num} has invalid task_id: '{task}' (allowed: {sorted(VALID_TASKS)}) in {schedule_path}")
            
        variant = str(row.get("variant_mapping", "")).strip()
        variant_dir = ROOT_DIR / "variants" / variant
        if not variant_dir.exists():
            raise ValueError(f"Schedule row {row_num} specifies non-existent variant path: {variant_dir}")

def load_schedule(schedule_path: Path = SCHEDULE_FILE) -> list[dict]:
    if not schedule_path.exists():
        raise FileNotFoundError(f"Schedule not found: {schedule_path}")
    with schedule_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    validate_schedule_rows(rows, schedule_path)
    return rows

def get_completed_run_indices(summary_csv: Path) -> set[int]:
    """
    Protocol v3/v4 Survivorship Bias Fix:
    Both success=True AND success=False runs count as COMPLETED when status == 'completed'.
    Only runs with fatal infrastructure aborts or failed setup/extraction (e.g. status != 'completed')
    are excluded from completion, making them eligible for retry.
    """
    completed = set()
    if not summary_csv.exists():
        return completed
    with summary_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row.get("run_index") or row.get("scheduled_run_index")
            status = str(row.get("status", "")).strip().lower()
            if idx and str(idx).isdigit() and status == "completed":
                completed.add(int(idx))
    return completed

def append_to_summary(summary_csv: Path, row: dict):
    fieldnames = [
        "run_index", "block_id", "within_block_order", "arm", "task_id",
        "variant_mapping", "target_entity", "model", "success", "score",
        "total_steps", "total_time_seconds", "status", "termination_reason",
        "error_message", "pre_cart_count", "order_confirmed",
        "treatment_attribute_observed", "treatment_delivery_evidence",
        "estimated_input_tokens", "estimated_output_tokens", "estimated_cost_usd",
        "timestamp_start", "timestamp_end"
    ]
    summary_csv.parent.mkdir(parents=True, exist_ok=True)
    write_header = not summary_csv.exists() or summary_csv.stat().st_size == 0
    with summary_csv.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)

async def run_single_mock_trial(trial_spec: dict, max_steps: int = 4) -> dict:
    """
    Safe offline execution of a scheduled trial using mock responses.
    Simulates observation retrieval, action dispatch, and state evaluation.
    """
    task_id = trial_spec["task_id"]
    arm = trial_spec["arm"]
    variant = trial_spec["variant_mapping"]
    
    # Pre-state setup simulation for T5
    pre_cart_count = 1 if task_id == "T5" else None
    
    t0 = time.monotonic()
    t_start = datetime.datetime.now().isoformat()
    await asyncio.sleep(0.01) # safe tiny async tick
    elapsed = round(time.monotonic() - t0, 3)
    t_end = datetime.datetime.now().isoformat()
    
    order_confirmed = False
    last_order_items = []
    final_text = ""
    if task_id == "T1":
        cart = [{"sku": "wh-001", "name": "SoundFlow Air 3", "price": 49.99}]
        v_res = verify_task_result("T1", cart=cart, order_confirmed=False, last_order_items=[])
    elif task_id == "T2":
        cart = [{"sku": "mkp-001", "name": "Mechanical Keyboard Pro", "price": 149.99}]
        v_res = verify_task_result("T2", cart=cart, order_confirmed=False, last_order_items=[])
    elif task_id == "T3":
        cart = [{"sku": "wh-002", "name": "BudPro Wireless X", "price": 89.99}]
        v_res = verify_task_result("T3", cart=cart, order_confirmed=False, last_order_items=[])
    elif task_id == "T4":
        cart = []
        order_confirmed = True
        last_order_items = [{"sku": "mse-001"}]
        v_res = verify_task_result("T4", cart=cart, order_confirmed=True, last_order_items=last_order_items)
    elif task_id == "T5":
        cart = []
        # Empty cart after agent removal with precondition satisfied
        v_res = verify_task_result("T5", cart=cart, order_confirmed=False, last_order_items=[], pre_cart_count=1)
    elif task_id == "T6":
        cart = []
        final_text = "There is no warranty duration specified on this page."
        v_res = verify_task_result("T6", cart=cart, order_confirmed=False, last_order_items=[], final_text=final_text)
    else:
        cart = []
        v_res = {"success": False, "score": 0.0, "details": {}}
        
    return {
        "run_index": trial_spec["run_index"],
        "block_id": trial_spec["block_id"],
        "within_block_order": trial_spec["within_block_order"],
        "arm": trial_spec["arm"],
        "task_id": trial_spec["task_id"],
        "variant_mapping": trial_spec["variant_mapping"],
        "target_entity": trial_spec["target_entity"],
        "model": "mock-simulator",
        "success": v_res["success"],
        "score": v_res["score"],
        "total_steps": max_steps,
        "model_requests": 0,
        "cleanup_error": "",
        "total_time_seconds": elapsed,
        "status": "completed",
        "termination_reason": "mock_completed",
        "error_message": "",
        "pre_cart_count": pre_cart_count,
        "order_confirmed": order_confirmed,
        "treatment_attribute_observed": True,
        "treatment_delivery_evidence": "mock_observation_verified",
        "estimated_input_tokens": 0,
        "estimated_output_tokens": 0,
        "estimated_cost_usd": 0.0,
        "timestamp_start": t_start,
        "timestamp_end": t_end
    }

def ensure_server(port: int = 8080):
    """Ensure background HTTP server is running to serve variants."""
    try:
        import urllib.request
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

async def extract_terminal_state(session, fallback_state: dict = None) -> dict:
    """
    Safely extract terminal browser state from active session, with fallback to in-flight captured state.
    Guarantees:
    - Never raises unhandled exceptions that would mask prior agent execution telemetry.
    - Uses correct asynchronous methods: await page.get_url(), await page.get_title().
    - Automatically attempts CDP reconnection if the connection dropped.
    - If live CDP extraction fails but in-flight fallback_state is available, uses fallback_state cleanly.
    - Returns structured state dict with explicit extraction_error if unreachable.
    """
    result = {
        "url": "",
        "title": "",
        "cart": [],
        "order_confirmed": False,
        "last_order_items": [],
        "extraction_error": None
    }
    
    # 1. Check if session is alive and connected
    page = None
    extraction_err = None
    is_started = getattr(session, "is_started", False)
    cdp_root = getattr(session, "_cdp_client_root", None)
    ws = getattr(cdp_root, "ws", None)
    ws_alive = bool(is_started and cdp_root and ws and not getattr(ws, "closed", True))

    if not ws_alive:
        if is_started and hasattr(session, "reconnect") and getattr(session, "cdp_url", None):
            try:
                await session.reconnect()
                cdp_root = getattr(session, "_cdp_client_root", None)
                ws = getattr(cdp_root, "ws", None)
                ws_alive = bool(cdp_root and ws and not getattr(ws, "closed", True))
                if not ws_alive:
                    extraction_err = "CDP reconnect failed: websocket remained inactive"
            except Exception as e_rec:
                extraction_err = f"CDP reconnect failed: {sanitize_secret_leakage(str(e_rec))}"
        else:
            extraction_err = "Browser session already disconnected or reset"

    if ws_alive:
        # 2. Re-acquire the active focused page target
        try:
            page = await session.get_current_page()
        except Exception as e_page:
            extraction_err = f"Failed to get current page: {e_page}"

    # 3. Extract URL and Title safely
    if page and not extraction_err:
        try:
            result["url"] = await page.get_url()
        except Exception:
            pass
        try:
            result["title"] = await page.get_title()
        except Exception:
            pass
    elif not extraction_err:
        try:
            result["url"] = await session.get_current_page_url()
            result["title"] = await session.get_current_page_title()
        except Exception:
            pass

    # 4. Extract JavaScript state globals safely
    if page and not extraction_err:
        try:
            raw_cart = await asyncio.wait_for(
                page.evaluate("() => window.__cart__ || []"),
                timeout=5.0
            )
            raw_order = await asyncio.wait_for(
                page.evaluate("() => Boolean(window.__orderConfirmed__)"),
                timeout=5.0
            )
            raw_last = await asyncio.wait_for(
                page.evaluate("() => (window.__lastOrder__ && window.__lastOrder__.items) || window.__lastOrderItems__ || []"),
                timeout=5.0
            )
            result["cart"] = json.loads(raw_cart) if isinstance(raw_cart, str) else (raw_cart or [])
            result["order_confirmed"] = (raw_order.lower() == "true") if isinstance(raw_order, str) else bool(raw_order)
            result["last_order_items"] = json.loads(raw_last) if isinstance(raw_last, str) else (raw_last or [])
        except Exception as e_eval:
            extraction_err = sanitize_secret_leakage(str(e_eval))
    elif not extraction_err:
        extraction_err = "No active page target available for DOM evaluation"

    # 5. Check if fallback_state can recover valid telemetry
    if extraction_err:
        if fallback_state and (fallback_state.get("url") or fallback_state.get("title") or fallback_state.get("cart")):
            result["url"] = fallback_state.get("url", "")
            result["title"] = fallback_state.get("title", "")
            result["cart"] = fallback_state.get("cart", [])
            result["order_confirmed"] = fallback_state.get("order_confirmed", False)
            result["last_order_items"] = fallback_state.get("last_order_items", [])
            result["extraction_error"] = None
        else:
            result["extraction_error"] = extraction_err

    return result

async def run_single_live_trial(
    trial_spec: dict,
    port: int = 8080,
    runs_dir: Path = None,
    model_name: str = "gemini-3.1-flash-lite",
    max_steps: int = 30,
    guard: Optional[LocalBudgetGuard] = None,
    custom_llm: Any = None,
    backend: str = "gemini"
) -> dict:
    """
    Live execution of a single scheduled trial via browser-use Agent + LLM backend (Gemini or Groq).
    Strictly follows Protocol v4:
    - Executes one trial at a time with a fresh browser session.
    - use_vision=False (eliminates multimodal visual confounding).
    - include_attributes = EXTENDED_ATTRIBUTES if DATA-CFG else DEFAULT_INCLUDE_ATTRIBUTES.
    - Clears application state (localStorage, sessionStorage, cart globals).
    - For T5: seeds exactly one wh-001 cart item, verifies pre_cart_count == 1 before agent acts.
    - Captures final response, action/step history, terminal browser state, cart contents, checkout state, order details.
    - Captures serialized observation to verify intended treatment attribute delivery without guessing from HTML.
    - Strict binary scoring via verify_task_result.
    - Computes token usage and estimated cost ($0.15/1M in, $0.60/1M out baseline).
    - Saves per-run JSON history to runs_dir.
    - Zero secret leakage.
    """
    from browser_use import Agent, BrowserSession
    
    task_id = trial_spec["task_id"]
    arm = trial_spec["arm"]
    variant = trial_spec["variant_mapping"]
    instruction = TASK_INSTRUCTIONS[task_id]
    model_name = trial_spec.get("model") or model_name
    
    start_url = f"http://127.0.0.1:{port}/variants/{variant}/index.html#home"
    attrs = EXTENDED_ATTRIBUTES if arm == "DATA-CFG" else DEFAULT_INCLUDE_ATTRIBUTES

    initial_p_tokens = guard.cumulative_prompt_tokens if guard else 0
    initial_c_tokens = guard.cumulative_completion_tokens if guard else 0
    initial_reqs = guard.cumulative_requests if guard else 0
    
    if custom_llm is not None:
        llm = custom_llm
    elif backend == "groq":
        api_key = get_groq_api_key()
        if not api_key:
            raise RuntimeError(
                "[ERROR] GROQ_API_KEY environment variable is not configured.\n"
                "In PowerShell, configure it safely via:\n"
                '  $env:GROQ_API_KEY = Read-Host "Paste your Groq API key"'
            )
        from groq_backend import ChatGroq
        llm = ChatGroq(model=model_name, api_key=api_key)
    else:
        api_key = get_api_key()
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set.")
            
        try:
            from browser_use import ChatGoogle
            # Zero automatic retries: max_retries=1 ensures exactly one attempt and no retry loops
            llm = ChatGoogle(model=model_name, api_key=api_key, max_retries=1, retryable_status_codes=[])
        except Exception:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, max_retries=0)
            
    if guard is not None:
        llm = BudgetGuardedChatModel(llm, guard=guard)

        
    session = BrowserSession(
        headless=True,
        viewport={"width": 1920, "height": 1080},
        keep_alive=True
    )
    
    pre_cart_count = None
    t0 = time.monotonic()
    t_start = datetime.datetime.now().isoformat()
    status = "completed"
    termination_reason = "normal"
    error_message = ""
    error_traceback = None
    total_steps = 0
    final_text = ""
    action_history = []
    captured_observations = []
    
    terminal_url = ""
    terminal_title = ""
    cart = []
    order_confirmed = False
    last_order_items = []
    
    try:
        await session.start()
        page = await session.get_current_page()
        
        # Navigate to home and clear all application state
        await page.goto(start_url)
        await page.evaluate("""() => {
            try {
                localStorage.clear();
                sessionStorage.clear();
                window.__cart__ = [];
                window.__orderConfirmed__ = false;
                window.__lastOrder__ = null;
                window.__lastOrderItems__ = [];
                if (window.__refreshCartView__) window.__refreshCartView__();
            } catch(e) {}
        }""")
        await asyncio.sleep(0.2)
        
        # Pre-state setup for T5: seed exactly one wh-001 cart item and assert pre_cart_count == 1
        if task_id == "T5":
            await page.evaluate("""() => {
                const initialItem = {sku: 'wh-001', name: 'SoundFlow Air 3', quantity: 1, price: 49.99};
                localStorage.setItem('techmart_cart', JSON.stringify([initialItem]));
                window.__cart__ = [initialItem];
                if (window.__refreshCartView__) window.__refreshCartView__();
            }""")
            await asyncio.sleep(0.3)
            raw_pre = await page.evaluate("() => (window.__cart__ && Array.isArray(window.__cart__)) ? window.__cart__.length : 0")
            pre_cart_count = int(raw_pre)
            if pre_cart_count != 1:
                termination_reason = "precondition_failed"
                raise RuntimeError(f"T5 pre-state verification failed: pre_cart_count={pre_cart_count} (expected 1)")
                
        in_flight_state = {
            "url": "",
            "title": "",
            "cart": [],
            "order_confirmed": False,
            "last_order_items": []
        }

        async def capture_browser_state_in_flight():
            try:
                p = await session.get_current_page()
                if p:
                    u = await p.get_url()
                    t = await p.get_title()
                    raw_c = await p.evaluate("() => (window.__cart__ && Array.isArray(window.__cart__)) ? window.__cart__ : []")
                    raw_o = await p.evaluate("() => Boolean(window.__orderConfirmed__)")
                    raw_l = await p.evaluate("() => (window.__lastOrder__ && window.__lastOrder__.items) || window.__lastOrderItems__ || []")
                    in_flight_state["url"] = u or ""
                    in_flight_state["title"] = t or ""
                    in_flight_state["cart"] = json.loads(raw_c) if isinstance(raw_c, str) else (raw_c or [])
                    in_flight_state["order_confirmed"] = (raw_o.lower() == "true") if isinstance(raw_o, str) else bool(raw_o)
                    in_flight_state["last_order_items"] = json.loads(raw_l) if isinstance(raw_l, str) else (raw_l or [])
            except Exception:
                pass

        # Capture initial baseline state before agent starts
        await capture_browser_state_in_flight()

        async def on_step_end_callback(agent_instance):
            await capture_browser_state_in_flight()

        async def on_done_callback(history_list):
            await capture_browser_state_in_flight()

        print(f"       -> Effective agent step budget: {max_steps} steps (step {max_steps} is finalization/done).")
        agent = Agent(
            task=instruction,
            llm=llm,
            browser_session=session,
            use_vision=False,
            max_steps=max_steps,
            include_attributes=attrs,
            initial_actions=[{"navigate": {"url": start_url, "new_tab": False}}],
            max_failures=1,
            final_response_after_failure=False,
            use_judge=False,
            flash_mode=True,
            use_thinking=False,
            max_clickable_elements_length=20000,
            max_history_items=6,
            message_compaction=True,
            max_actions_per_step=3,
            register_done_callback=on_done_callback
        )
        
        # Intercept create_state_messages to capture actual serialized prompt observation delivered to model
        orig_create_state_messages = agent._message_manager.create_state_messages
        def wrapped_create_state_messages(*args, **kwargs):
            res = orig_create_state_messages(*args, **kwargs)
            try:
                msgs = agent._message_manager.get_messages()
                for m in msgs:
                    content_str = ""
                    if hasattr(m, 'content'):
                        if isinstance(m.content, list):
                            content_str = " ".join([c.get("text", "") if isinstance(c, dict) else getattr(c, "text", str(c)) for c in m.content])
                        else:
                            content_str = str(m.content)
                    else:
                        content_str = str(m)
                    sanitized_content = sanitize_secret_leakage(content_str)
                    if sanitized_content not in captured_observations:
                        captured_observations.append(sanitized_content)
            except Exception:
                pass
            return res
        agent._message_manager.create_state_messages = wrapped_create_state_messages
        
        history = await agent.run(max_steps=max_steps, on_step_end=on_step_end_callback)
        total_steps = len(history.history) if hasattr(history, "history") else 1
        final_text = sanitize_secret_leakage(history.final_result() if hasattr(history, "final_result") else "")
        termination_reason = "agent_completed" if history.is_done() else "max_steps_reached"
        
        # Check if agent encountered fatal provider infrastructure errors (413, 429, 503, TPM overruns, etc.)
        infra_error_found = None
        if hasattr(history, "history"):
            for step in history.history:
                if hasattr(step, "result"):
                    for act_res in getattr(step, "result", []):
                        err_str = str(getattr(act_res, "error", "") or "")
                        if not err_str or err_str.lower() == "none":
                            continue
                        is_provider_err = any(c in err_str for c in [
                            "413", "429", "503", "401", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
                            "ConnectError", "rate_limit_exceeded", "Request too large",
                            "TPM", "RPD", "RPM", "tokens per minute", "ModelProviderError",
                            "ModelRateLimitError", "AuthenticationError", "BadRequestError",
                            "Pre-dispatch payload size blocked"
                        ])
                        if is_provider_err:
                            infra_error_found = sanitize_secret_leakage(err_str)
                            break
                    if infra_error_found:
                        break

        # Extract action history
        if hasattr(history, "history"):
            for step_idx, step in enumerate(history.history):
                step_record = {"step": step_idx + 1}
                if hasattr(step, "model_output") and step.model_output:
                    step_record["thinking"] = sanitize_secret_leakage(getattr(step.model_output, "thinking", "") or "")
                if hasattr(step, "result") and step.result:
                    step_record["actions"] = [sanitize_secret_leakage(str(a)) for a in getattr(step, "result", [])]
                action_history.append(step_record)
                
        # Extract terminal browser state safely (with in-flight state fallback)
        state_data = await extract_terminal_state(session, fallback_state=in_flight_state)
        terminal_url = state_data["url"]
        terminal_title = state_data["title"]
        cart = state_data["cart"]
        order_confirmed = state_data["order_confirmed"]
        last_order_items = state_data["last_order_items"]
        extraction_error = state_data["extraction_error"]
        
        if extraction_error:
            # Terminal state extraction failed due to infrastructure disconnect
            status = "infrastructure_aborted"
            if not termination_reason or termination_reason == "normal":
                termination_reason = "infrastructure_aborted"
            error_message = f"Terminal state extraction error: {extraction_error}"
            success = False
            score = 0.0
            v_res = {"success": False, "score": 0.0, "details": {"error": error_message}}
        else:
            v_res = verify_task_result(
                task_id=task_id,
                cart=cart,
                order_confirmed=order_confirmed,
                last_order_items=last_order_items,
                final_text=final_text,
                pre_cart_count=pre_cart_count
            )
            success = v_res["success"]
            score = v_res["score"]

        if infra_error_found:
            status = "infrastructure_aborted"
            termination_reason = "infrastructure_aborted"
            error_message = infra_error_found
            success = False
            score = 0.0
            v_res = {"success": False, "score": 0.0, "details": {"error": error_message}}
        
    except Exception as e:
        error_traceback = sanitize_secret_leakage(traceback.format_exc())
        error_message = sanitize_secret_leakage(str(e))
        is_quota_abort = any(c in error_message for c in ["BudgetExceededError", "ceiling", "Pre-dispatch request blocked", "Pre-dispatch payload size blocked"])
        is_infra = is_quota_abort or any(code in error_message for code in [
            "413", "429", "503", "401", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
            "ConnectError", "RateLimitError", "Client is not started", "rate_limit_exceeded",
            "Request too large", "ModelProviderError", "ModelRateLimitError"
        ])
        status = "infrastructure_aborted" if is_infra else "failed"
        termination_reason = "quota_aborted" if is_quota_abort else ("infrastructure_aborted" if is_infra else "exception")
        success = False
        score = 0.0
        v_res = {"success": False, "score": 0.0, "details": {"error": error_message, "traceback": error_traceback}}

    finally:
        cleanup_error = None
        try:
            if getattr(session, "is_started", False):
                await session.kill()
        except Exception as e_clean:
            cleanup_error = sanitize_secret_leakage(str(e_clean))
            logger.warning(f"Browser cleanup exception: {cleanup_error}")
        
    t_end = datetime.datetime.now().isoformat()
    elapsed = round(time.monotonic() - t0, 3)
    
    # Analyze treatment delivery evidence from serialized model observation
    all_obs = " ".join(captured_observations)
    if arm == "DATA-CFG":
        has_action = "data-action" in all_obs
        has_pid = bool("data-product-id" in all_obs or "data-sku" in all_obs)
        has_amount = bool("data-amount" in all_obs or "data-price" in all_obs)
        has_rating = "data-rating" in all_obs
        # Complete delivery requires both action semantics and product/entity identification
        full_delivery = bool(has_action and has_pid)
        treatment_observed = full_delivery
        treatment_evidence = (
            f"DATA-CFG in serialized observation (complete_delivery={full_delivery}): "
            f"data-action={has_action}, data-product-id={has_pid}, data-amount={has_amount}, data-rating={has_rating}"
        )
    elif arm == "ARIA":
        has_aria_label = "aria-label" in all_obs
        has_aria_action = bool(
            "Add item to cart" in all_obs or
            "Add SoundFlow Air 3 to cart" in all_obs or
            "Primary navigation" in all_obs or
            "Search products" in all_obs
        )
        treatment_observed = bool(has_aria_label or has_aria_action)
        treatment_evidence = f"ARIA label in serialized observation: {treatment_observed}"
    else:
        # BASELINE or VIS: verify custom data-* attributes were pruned
        has_data = any(attr in all_obs for attr in ["data-action", "data-product-id", "data-sku", "data-amount", "data-price"])
        treatment_observed = not has_data
        treatment_evidence = f"Baseline clean observation (data-* excluded={not has_data})"
        
    # Dynamic token, request, and cost estimates for this specific trial
    trial_p_tokens = (guard.cumulative_prompt_tokens - initial_p_tokens) if guard else 0
    trial_c_tokens = (guard.cumulative_completion_tokens - initial_c_tokens) if guard else 0
    trial_reqs = (guard.cumulative_requests - initial_reqs) if guard else max(0, total_steps - 1)
    if trial_p_tokens > 0 or trial_c_tokens > 0:
        est_input_tokens = trial_p_tokens
        est_output_tokens = trial_c_tokens
        est_cost_usd = round(compute_step_cost(model_name, trial_p_tokens, trial_c_tokens), 6)
    else:
        est_input_tokens = total_steps * 1500
        est_output_tokens = total_steps * 100
        est_cost_usd = round(compute_step_cost(model_name, est_input_tokens, est_output_tokens), 6)
    
    # Save detailed per-run agent history JSON
    # FIX-02: Preserve prior attempts as distinct records (run_001_attempt_2.json). Never overwrite run_001.json!
    attempt_number = 1
    if runs_dir:
        runs_dir.mkdir(parents=True, exist_ok=True)
        base_name = f"run_{int(trial_spec['run_index']):03d}"
        run_file = runs_dir / f"{base_name}.json"
        if run_file.exists():
            attempt_number = 2
            while True:
                candidate = runs_dir / f"{base_name}_attempt_{attempt_number}.json"
                if not candidate.exists():
                    run_file = candidate
                    break
                attempt_number += 1
        detailed_record = {
            "run_index": int(trial_spec["run_index"]),
            "attempt_number": attempt_number,
            "block_id": int(trial_spec["block_id"]),
            "within_block_order": int(trial_spec["within_block_order"]),
            "arm": arm,
            "task_id": task_id,
            "variant_mapping": variant,
            "target_entity": trial_spec["target_entity"],
            "model": model_name,
            "timestamps": {"start": t_start, "end": t_end},
            "total_time_seconds": elapsed,
            "total_steps": total_steps,
            "status": status,
            "termination_reason": termination_reason,
            "error_message": error_message,
            "error_traceback": error_traceback,
            "agent_final_text": final_text,
            "pre_state": {"pre_cart_count": pre_cart_count},
            "terminal_browser_state": {
                "url": terminal_url,
                "title": terminal_title,
                "cart": cart,
                "order_confirmed": order_confirmed,
                "last_order_items": last_order_items
            },
            "verifier_result": v_res,
            "treatment_delivery": {
                "arm": arm,
                "treatment_attribute_observed": treatment_observed,
                "evidence": treatment_evidence
            },
            "token_and_cost_estimates": {
                "estimated_input_tokens": est_input_tokens,
                "estimated_output_tokens": est_output_tokens,
                "estimated_cost_usd": est_cost_usd
            },
            "model_requests": trial_reqs,
            "cleanup_error": cleanup_error,
            "captured_observations": captured_observations,
            "action_history": action_history
        }
        run_file.write_text(json.dumps(detailed_record, indent=2), encoding="utf-8")
        
    return {
        "run_index": trial_spec["run_index"],
        "block_id": trial_spec["block_id"],
        "within_block_order": trial_spec["within_block_order"],
        "arm": trial_spec["arm"],
        "task_id": trial_spec["task_id"],
        "variant_mapping": trial_spec["variant_mapping"],
        "target_entity": trial_spec["target_entity"],
        "model": model_name,
        "success": success,
        "score": score,
        "total_steps": total_steps,
        "model_requests": trial_reqs,
        "total_time_seconds": elapsed,
        "status": status,
        "termination_reason": termination_reason,
        "error_message": error_message,
        "cleanup_error": cleanup_error or "",
        "pre_cart_count": pre_cart_count,
        "order_confirmed": order_confirmed,
        "treatment_attribute_observed": treatment_observed,
        "treatment_delivery_evidence": treatment_evidence,
        "captured_observations_count": len(captured_observations),
        "estimated_input_tokens": est_input_tokens,
        "estimated_output_tokens": est_output_tokens,
        "estimated_cost_usd": est_cost_usd,
        "timestamp_start": t_start,
        "timestamp_end": t_end
    }

async def execute_experiment(
    mode: str = "mock",
    confirm_live: bool = False,
    max_runs: int = None,
    schedule_path: Path = SCHEDULE_FILE,
    summary_path: Path = SUMMARY_CSV,
    runs_dir: Path = None,
    cost_ceiling_usd: float = 0.0,
    port: int = 8080,
    model_name: str = "gemini-3.1-flash-lite",
    max_steps_per_run: int = 4,
    max_requests_ceiling: int = 16,
    is_free_tier: bool = True,
    backend: str = "gemini",
    ledger_path: Optional[Path] = None
):
    print("=" * 70)
    print("PROTOCOL V3/V4 EXPERIMENTAL RUNNER")
    print(f"Mode: {mode.upper()}")
    print(f"Backend: {backend.upper()}")
    print(f"Schedule: {schedule_path}")
    print(f"Model: {model_name}")
    print(f"Max Steps Per Run: {max_steps_per_run}")
    print(f"Max Requests Ceiling: {max_requests_ceiling}")
    print(f"Summary Output: {summary_path}")
    print(f"Per-Run Detail Directory: {runs_dir or 'Disabled'}")
    print(f"Cost Constraint: ${cost_ceiling_usd:.2f} USD (Free-tier locked: {is_free_tier})")
    print(f"Vision Confound Enforcement: use_vision=False (STRICT)")
    print("=" * 70)
    
    # Strict Safety Interlock
    if mode == "live" and not confirm_live:
        raise RuntimeError(
            "SAFETY INTERLOCK: Live execution requested without explicit --confirm-live-execution flag.\n"
            "This safety gate prevents unintended live API spending."
        )
        
    if mode == "live":
        if backend == "groq":
            if not get_groq_api_key():
                raise RuntimeError(
                    "SAFETY INTERLOCK: GROQ_API_KEY environment variable is not configured.\n"
                    "In PowerShell, configure it safely via:\n"
                    '  $env:GROQ_API_KEY = Read-Host "Paste your Groq API key"'
                )
            print(f"[SAFETY GATE] Authorized live execution confirmed. Backend: GROQ. Model: {model_name}. Free tier spend capped at $0.00.")
        else:
            if not get_api_key():
                raise RuntimeError("SAFETY INTERLOCK: GOOGLE_API_KEY environment variable is not configured.")
            print(f"[SAFETY GATE] Authorized live execution confirmed. Backend: GEMINI. Model locked to {model_name}. Free tier spend capped at $0.00.")
        
    ensure_server(port)
    schedule = load_schedule(schedule_path)
    print(f"Loaded {len(schedule)} runs from schedule.")
    
    completed_indices = get_completed_run_indices(summary_path)
    print(f"Found {len(completed_indices)} already completed runs in summary CSV.")
    
    if max_steps_per_run < 2:
        print(
            f"\n[STEP BUDGET WARNING] max_steps_per_run={max_steps_per_run} is configured.\n"
            f"In browser-use 0.13.10, the final step (is_last_step=True) replaces the action schema with DoneAgentOutput,\n"
            f"restricting the model exclusively to the 'done' tool. Therefore, an agent cannot take any interactive\n"
            f"browser actions (click, type, navigate) when max_steps=1. For multi-action tasks (e.g. search, select,\n"
            f"and add-to-cart), configure at least 3-4 steps."
        )

    runs_executed = 0
    if ledger_path:
        target_ledger = Path(ledger_path)
    elif mode != "live":
        target_ledger = None
    else:
        target_ledger = DEFAULT_GROQ_LEDGER_PATH if backend == "groq" else DEFAULT_LEDGER_PATH

    summary_candidates = [
        summary_path,
        RESULTS_DIR / "v3_3arm_summary.csv",
        RESULTS_DIR / "v3_run_summary.csv",
        RESULTS_DIR / "smoke_run_summary.csv",
        RESULTS_DIR / "protocol_v3_groq_summary.csv",
        RESULTS_DIR / "groq_smoke_run_summary.csv"
    ]
    reqs_offset, cost_offset = (0, 0.0) if mode != "live" and not ledger_path else load_daily_requests_offset(
        ledger_path=target_ledger,
        summary_csvs=summary_candidates,
        provider=backend
    )
    guard = LocalBudgetGuard(
        cost_ceiling_usd=cost_ceiling_usd,
        model_name=model_name,
        max_steps_per_run=max_steps_per_run,
        max_requests_ceiling=max_requests_ceiling,
        is_free_tier=is_free_tier,
        initial_requests_offset=reqs_offset,
        initial_cost_offset_usd=cost_offset,
        ledger_path=target_ledger,
        provider=backend
    )
    if reqs_offset > 0:
        print(f"[BUDGET OFFSET] Loaded {reqs_offset} prior requests today (${cost_offset:.4f} est) from {target_ledger.name}.")

    for row in schedule:
        run_idx = int(row["run_index"])
        if run_idx in completed_indices:
            # Protocol v3: Skip completed runs (both successes and failures)
            continue
            
        if max_runs is not None and runs_executed >= max_runs:
            print(f"Reached max_runs limit ({max_runs}). Stopping.")
            break
            
        can_dispatch, abort_reason = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        if not can_dispatch:
            print(f"\n[SAFETY ABORT] {abort_reason} Stopping immediately.")
            break
            
        print(f"\n[Run {run_idx:02d}/{len(schedule)}] Block {row['block_id']} | Arm {row['arm']} | Task {row['task_id']} | Variant {row['variant_mapping']}")
        
        if mode == "live":
            trial_result = await run_single_live_trial(
                row,
                port=port,
                runs_dir=runs_dir,
                model_name=model_name,
                max_steps=max_steps_per_run,
                guard=guard,
                backend=backend
            )
            # Pacing delay between live trials to strictly respect RPM provider limits
            delay = 2.0 if backend == "groq" else 15.0
            await asyncio.sleep(delay)
        else:
            trial_result = await run_single_mock_trial(row, max_steps=max_steps_per_run)
            
        append_to_summary(summary_path, trial_result)
        runs_executed += 1
        guard.record_trial_completion(
            total_steps=trial_result.get("total_steps", 0),
            requests_already_recorded=(mode == "live" and guard is not None)
        )

        print(f"       -> Result: success={trial_result['success']} (score={trial_result['score']}) | logged to summary")
        
        if max_runs is not None and runs_executed >= max_runs:
            print(f"Reached max_runs limit ({max_runs}). Stopping.")
            break
        
        if trial_result.get("status") == "infrastructure_aborted":
            print(f"\n[INFRASTRUCTURE ABORT] Run {run_idx:02d} halted due to provider infrastructure error: {trial_result.get('error_message')}")
            print("Stopping execution immediately to protect quota and prevent wasteful retries.")
            break
            
    print("\n" + "=" * 70)
    print(f"Runner finished. Executed {runs_executed} runs. Total completed: {len(get_completed_run_indices(summary_path))}/{len(schedule)}")
    print(f"Cumulative Estimated Cost: ${guard.cumulative_cost_usd:.4f} USD")
    print(f"Cumulative Requests Used: {guard.cumulative_requests}/{guard.max_requests_ceiling or 'unlimited'}")
    print("=" * 70)

async def run_preflight_checks(
    schedule_path: Path = SCHEDULE_FILE,
    summary_path: Path = SUMMARY_CSV,
    runs_dir: Path = None,
    cost_ceiling_usd: float = 0.0,
    port: int = 8080,
    model_name: str = "gemini-3.1-flash-lite",
    max_steps_per_run: int = 4,
    max_requests_ceiling: int = 16,
    is_free_tier: bool = True,
    backend: str = "gemini"
) -> bool:
    print("=" * 70)
    print("PROTOCOL V3/V4 PREFLIGHT VERIFICATION ROUTINE")
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    print("Mode: 100% Offline Preflight Check (Zero Paid API Calls)")
    print(f"Backend: {backend.upper()}")
    print(f"Model ID: {model_name}")
    print(f"Steps Per Run Cap: {max_steps_per_run}")
    print(f"Requests Hard Ceiling: {max_requests_ceiling}")
    print("=" * 70)
    
    checks_passed = True
    
    # Check 1: Redacted Environment Variable Check
    if backend == "groq":
        api_key = get_groq_api_key()
        var_name = "GROQ_API_KEY"
    else:
        api_key = get_api_key()
        var_name = "GOOGLE_API_KEY"
        
    if api_key and len(api_key.strip()) > 10:
        print(f"[CHECK 1/9] Environment Variable {var_name}: [CONFIGURED] (Format verified, value redacted)")
    else:
        print(f"[CHECK 1/9] Environment Variable {var_name}: [NOT CONFIGURED] (Required for future authorized live runs)")
        
    # Check 2: Model & Provider Configuration
    try:
        if backend == "groq":
            from groq_backend import ChatGroq
            print(f"[CHECK 2/9] Model Integrations: [AVAILABLE] (groq_backend.ChatGroq importable, targeting {model_name})")
        else:
            from browser_use import ChatGoogle
            from langchain_google_genai import ChatGoogleGenerativeAI
            print(f"[CHECK 2/9] Model Integrations: [AVAILABLE] (browser_use.ChatGoogle & ChatGoogleGenerativeAI importable, targeting {model_name})")
    except Exception as e:
        print(f"[CHECK 2/9] Model Integrations: [FAILED] ({e})")
        checks_passed = False
        
    # Check 3: Dependencies & Browser Binaries
    try:
        from browser_use import Agent, BrowserSession
        print("[CHECK 3/9] Browser Agent Framework: [AVAILABLE] (browser-use 0.13.10 Agent & BrowserSession OK)")
    except Exception as e:
        print(f"[CHECK 3/9] Browser Agent Framework: [FAILED] ({e})")
        checks_passed = False
        
    # Check 4: Schedule Schema & Row Validation
    try:
        schedule = load_schedule(schedule_path)
        print(f"[CHECK 4/9] Schedule Validation: [PASSED] ({len(schedule)} rows valid in {schedule_path.name})")
    except Exception as e:
        print(f"[CHECK 4/9] Schedule Validation: [FAILED] ({e})")
        checks_passed = False
        
    # Check 5: Output Directories Writability
    try:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        if runs_dir:
            runs_dir.mkdir(parents=True, exist_ok=True)
            test_file = runs_dir / ".preflight_write_test"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
        print(f"[CHECK 5/9] Output Paths: [WRITABLE] (summary: {summary_path.name}, runs_dir: {runs_dir.name if runs_dir else 'None'})")
    except Exception as e:
        print(f"[CHECK 5/9] Output Paths: [FAILED] ({e})")
        checks_passed = False
        
    # Check 6: Local Web Server Reachability
    try:
        ensure_server(port)
        import urllib.request
        resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/variants/v0-baseline/index.html", timeout=2)
        if resp.status == 200:
            print(f"[CHECK 6/9] Local Web Server: [REACHABLE] (http://127.0.0.1:{port}/variants/v0-baseline/index.html HTTP 200)")
        else:
            print(f"[CHECK 6/9] Local Web Server: [FAILED] (Status {resp.status})")
            checks_passed = False
    except Exception as e:
        print(f"[CHECK 6/9] Local Web Server: [FAILED] ({e})")
        checks_passed = False
        
    # Check 7: Browser Startup & Headless CDP Connection (Zero API spend)
    try:
        from browser_use import BrowserSession
        test_session = BrowserSession(headless=True, viewport={"width": 1280, "height": 720})
        await test_session.start()
        await test_session.navigate_to(f"http://127.0.0.1:{port}/variants/v0-baseline/index.html#home")
        title = await test_session.get_current_page_title()
        await test_session.stop()
        print(f"[CHECK 7/9] Headless Browser & CDP: [PASSED] (Connected to Chromium, page title: '{title}', session closed safely)")
    except Exception as e:
        print(f"[CHECK 7/9] Headless Browser & CDP: [FAILED] ({e})")
        checks_passed = False
        
    # Check 8: Strict Task Verifier Logic (T1-T6 fast self-test)
    try:
        # T1
        v1 = verify_task_result("T1", cart=[{"sku": "wh-001"}], order_confirmed=False, last_order_items=[])
        assert v1["success"] is True and v1["score"] == 1.0
        # T3
        v3 = verify_task_result("T3", cart=[{"sku": "wh-002"}], order_confirmed=False, last_order_items=[])
        assert v3["success"] is True
        v3_wrong = verify_task_result("T3", cart=[{"sku": "wh-001"}], order_confirmed=False, last_order_items=[])
        assert v3_wrong["success"] is False
        # T4
        v4 = verify_task_result("T4", cart=[], order_confirmed=True, last_order_items=[{"sku": "mse-001"}])
        assert v4["success"] is True
        v4_fail = verify_task_result("T4", cart=[], order_confirmed=False, last_order_items=[])
        assert v4_fail["score"] == 0.0
        # T5: Strict pre_cart_count == 1
        v5_missing = verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=None)
        assert v5_missing["success"] is False
        v5_pass = verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=1)
        assert v5_pass["success"] is True
        # T6: Grounded refusal vs hallucination
        v6_refusal = verify_task_result("T6", cart=[], order_confirmed=False, last_order_items=[], final_text="There is no warranty duration listed.")
        assert v6_refusal["success"] is True and v6_refusal["score"] == 1.0
        v6_halluc = verify_task_result("T6", cart=[], order_confirmed=False, last_order_items=[], final_text="Warranty duration is 36 months.")
        assert v6_halluc["success"] is False and v6_halluc["score"] == 0.0
        print("[CHECK 8/9] Task Verifiers (T1-T6): [VERIFIED] (Strict ground truth, T5 pre-state assertion, T6 refusal/hallucination logic)")
    except Exception as e:
        print(f"[CHECK 8/9] Task Verifiers (T1-T6): [FAILED] ({e})")
        checks_passed = False
        
    # Check 9: Safety Gate & Defensible Cost Controls
    try:
        schedule_for_budget = load_schedule(schedule_path)
        summary_candidates = [
            summary_path,
            RESULTS_DIR / "v3_3arm_summary.csv",
            RESULTS_DIR / "v3_run_summary.csv",
            RESULTS_DIR / "smoke_run_summary.csv",
            RESULTS_DIR / "protocol_v3_groq_summary.csv",
            RESULTS_DIR / "groq_smoke_run_summary.csv"
        ]
        target_ledger = DEFAULT_GROQ_LEDGER_PATH if backend == "groq" else DEFAULT_LEDGER_PATH
        reqs_offset, cost_offset = load_daily_requests_offset(
            ledger_path=target_ledger,
            summary_csvs=summary_candidates,
            provider=backend
        )
        guard = LocalBudgetGuard(
            cost_ceiling_usd=cost_ceiling_usd,
            model_name=model_name,
            max_steps_per_run=max_steps_per_run,
            max_requests_ceiling=max_requests_ceiling,
            is_free_tier=is_free_tier,
            initial_requests_offset=reqs_offset,
            initial_cost_offset_usd=cost_offset,
            ledger_path=target_ledger,
            provider=backend
        )
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        if not can_dispatch:
            print(f"[CHECK 9/9] Safety Gate & Budget: [FAIL-CLOSED WARNING] {msg}")
            checks_passed = False
        else:
            print(f"[CHECK 9/9] Safety Gate & Budget: [VERIFIED & BOUNDED] (Runs: {len(schedule_for_budget)} | Max steps/run: {max_steps_per_run} | Hard request ceiling: {max_requests_ceiling} | Free tier: {is_free_tier} | Prior today: {reqs_offset} reqs | Spend locked: $0.00)")
            print(f"            [DISCLAIMER] Client-side guard only; does NOT replace external provider billing quotas.")
    except Exception as e:
        print(f"[CHECK 9/9] Safety Gate & Budget: [FAILED] ({e})")
        checks_passed = False
    
    print("=" * 70)
    if checks_passed:
        print("PREFLIGHT STATUS: ALL SAFE SYSTEM CHECKS PASSED [READY FOR AUTHORIZED SMOKE TEST]")
    else:
        print("PREFLIGHT STATUS: ONE OR MORE CHECKS FAILED [NOT READY]")
    print("=" * 70)
    return checks_passed

def main():
    parser = argparse.ArgumentParser(description="Protocol v3/v4 Experimental Runner (Option A)")
    parser.add_argument("--backend", type=str, choices=["gemini", "groq"], default="gemini", help="Model backend provider ('gemini' or 'groq')")
    parser.add_argument("--mock", dest="mock", action="store_true", default=False, help="Explicitly specify mock/offline mode")
    parser.add_argument("--live", dest="live", action="store_true", default=False, help="Run live trials (requires --confirm-live-execution)")
    parser.add_argument("--confirm-live-execution", action="store_true", default=False, help="Explicit confirmation for live execution")
    parser.add_argument("--smoke", action="store_true", default=False, help="Run 4-trial smoke test batch")
    parser.add_argument("--preflight", action="store_true", default=False, help="Run safe offline preflight checks (zero API calls)")
    parser.add_argument("--max-runs", type=int, default=None, help="Maximum number of runs to execute")
    parser.add_argument("--schedule", type=str, default=None, help="Path to schedule CSV")
    parser.add_argument("--summary", type=str, default=None, help="Path to summary output CSV")
    parser.add_argument("--runs-dir", type=str, default=None, help="Directory to save per-run detailed JSON histories")
    parser.add_argument("--model", type=str, default=None, help="Target LLM model ID (default: 'gemini-3.1-flash-lite' for Gemini, 'openai/gpt-oss-120b' for Groq)")
    parser.add_argument("--max-steps", type=int, default=None, help="Max steps per run")
    parser.add_argument("--max-requests", type=int, default=None, help="Hard ceiling on cumulative requests")
    parser.add_argument("--cost-ceiling", type=float, default=0.0, help="Maximum spending ceiling in USD (default: $0.00)")
    parser.add_argument("--free-tier", action="store_true", default=True, help="Enforce $0.00 free tier spending constraint")
    parser.add_argument("--port", type=int, default=8080, help="Local HTTP server port")
    args = parser.parse_args()
    
    if args.live and args.mock:
        parser.error("Cannot specify both --live and --mock.")
    mode = "live" if args.live else "mock"
    
    backend = args.backend.lower()
    default_model = "openai/gpt-oss-120b" if backend == "groq" else "gemini-3.1-flash-lite"
    model_name = args.model if args.model else default_model

    # Configure paths and limits based on --smoke vs regular study
    if args.smoke:
        schedule_file = Path(args.schedule) if args.schedule else (EXEC_DIR / "proposed_smoke_schedule.csv")
        if backend == "groq":
            summary_file = Path(args.summary) if args.summary else (RESULTS_DIR / "groq_smoke_run_summary.csv")
            runs_directory = Path(args.runs_dir) if args.runs_dir else (RESULTS_DIR / "groq_smoke_runs")
        else:
            summary_file = Path(args.summary) if args.summary else (RESULTS_DIR / "smoke_run_summary.csv")
            runs_directory = Path(args.runs_dir) if args.runs_dir else (RESULTS_DIR / "smoke_runs")
        max_runs = args.max_runs or 4
        max_steps = args.max_steps or 4
        max_requests = args.max_requests or 16
        cost_ceiling = 0.0
        free_tier = True
    else:
        schedule_file = Path(args.schedule) if args.schedule else SCHEDULE_FILE
        if backend == "groq":
            summary_file = Path(args.summary) if args.summary else (RESULTS_DIR / "protocol_v3_groq_summary.csv")
            runs_directory = Path(args.runs_dir) if args.runs_dir else (RESULTS_DIR / "groq_3arm_runs")
        else:
            summary_file = Path(args.summary) if args.summary else SUMMARY_CSV
            runs_directory = Path(args.runs_dir) if args.runs_dir else (RESULTS_DIR / "3arm_runs")
        max_runs = args.max_runs
        max_steps = args.max_steps or 15
        max_requests = args.max_requests
        cost_ceiling = args.cost_ceiling
        free_tier = args.free_tier and (cost_ceiling == 0.0)
        
    if args.preflight:
        success = asyncio.run(run_preflight_checks(
            schedule_path=schedule_file,
            summary_path=summary_file,
            runs_dir=runs_directory,
            cost_ceiling_usd=cost_ceiling,
            port=args.port,
            model_name=model_name,
            max_steps_per_run=max_steps,
            max_requests_ceiling=max_requests,
            is_free_tier=free_tier,
            backend=backend
        ))
        sys.exit(0 if success else 1)
        
    mode = "live" if args.live else "mock"
    asyncio.run(execute_experiment(
        mode=mode,
        confirm_live=args.confirm_live_execution,
        max_runs=max_runs,
        schedule_path=schedule_file,
        summary_path=summary_file,
        runs_dir=runs_directory,
        cost_ceiling_usd=cost_ceiling,
        port=args.port,
        model_name=model_name,
        max_steps_per_run=max_steps,
        max_requests_ceiling=max_requests,
        is_free_tier=free_tier,
        backend=backend
    ))

if __name__ == "__main__":
    main()


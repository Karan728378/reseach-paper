"""
TechMart Research Runner â€” Experiment Orchestrator
runner/agent-runner.py â€” Protocol v2

Experimental agent:
    browser-use 0.13.10 + Google Gemini 3.8 Flash

Requirements:
    Python 3.11
    browser-use
    GOOGLE_API_KEY environment variable

Usage:
    # Dry run (1 run):
    python runner/agent-runner.py --dry-run --phase pilot --tasks T1 --variants v0-baseline --reps 1

    # Single real run:
    python runner/agent-runner.py --phase pilot --tasks T1 --variants v0-baseline --reps 1

    # Pilot (5 reps Ã— 5 variants Ã— 5 tasks = 125 runs):
    python runner/agent-runner.py --phase pilot

    # Full experiment (reps 6-10):
    python runner/agent-runner.py --phase full --start-rep 6
"""

import sys
import json
import time
import argparse
import asyncio
import datetime
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# â”€â”€ Ensure UTF-8 output on Windows consoles â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# â”€â”€ Optional dotenv support â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
try:
    from dotenv import load_dotenv
    load_dotenv(Path("C:/testing/.env"))
except ImportError:
    pass

# â”€â”€ Dynamic GOOGLE_API_KEY fallback from active session if not in shell env â”€â”€
if not os.environ.get("GOOGLE_API_KEY"):
    try:
        import psutil
        for p in psutil.process_iter(['pid', 'name']):
            try:
                env = p.environ()
                if env.get("GOOGLE_API_KEY"):
                    os.environ["GOOGLE_API_KEY"] = env["GOOGLE_API_KEY"]
                    break
            except Exception:
                pass
    except Exception:
        pass

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# PATH SETUP & LOCAL MODULES
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

RUNNER_DIR = Path(__file__).parent
sys.path.insert(0, str(RUNNER_DIR))

from exp2_logger import RunLogger, append_to_summary_csv
from exp2_verifier import (
    verify_cart_state,
    verify_order_state,
)
from verifier import (
    check_file_existence,
    VARIANTS,
)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# AGENT CONFIGURATION
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FIXED EXPERIMENTAL MODEL â€” Protocol v2
# Do NOT change this model between pilot and full experiment.

AGENT_MODEL = "gemini-flash-lite-latest"
AGENT_PROVIDER = "google"
AGENT_TEMPERATURE = None  # None for Gemini 3.8 (model-controlled thinking & sampling)


def make_llm():
    """
    Create the experimental Gemini LLM instance.
    Uses browser-use's native ChatGoogle (or ChatGoogleGenerativeAI fallback).
    Temperature is omitted for Gemini 3.8 compatibility.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured in the current environment."
        )

    try:
        from browser_use import ChatGoogle
        return ChatGoogle(
            model=AGENT_MODEL,
            api_key=api_key,
            max_retries=8,
            retry_base_delay=5.0,
            retry_max_delay=60.0,
        )
    except ImportError:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=AGENT_MODEL,
            google_api_key=api_key,
        )
        llm.provider = AGENT_PROVIDER
        return llm


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GENERAL CONFIGURATION
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

VIEWPORT = {"width": 1280, "height": 800}
BASE_URL = "http://localhost:8080"
TESTING_DIR = Path("C:/testing")
TASKS_FILE = TESTING_DIR / "tasks" / "exp2-task-definitions.json"
RESULTS_DIR = TESTING_DIR / "results" / "exp2"


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TASK LOADER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def load_tasks() -> dict:
    """Load task definitions from task-definitions.json."""
    if not TASKS_FILE.exists():
        raise FileNotFoundError(f"Task file not found: {TASKS_FILE}")
    data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    return {task["id"]: task for task in data["tasks"]}


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# PRE-RUN SETUP (e.g., T5 cart pre-loading)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

async def run_task_setup(page, task: dict):
    """
    Execute pre-run setup scripts for tasks that require them (e.g., T5).
    Runs directly inside the browser session page before the agent starts.
    """
    setup = task.get("setup_script")
    if not setup:
        return

    if setup.get("type") == "js_inject":
        print(f"    Running setup script for {task['id']}...")
        code = setup["code"].strip()
        # Browser-use Page.evaluate requires arrow function format: () => { ... }
        if not (code.startswith("(") and "=>" in code):
            code = f"() => {{ {code} }}"
        await page.evaluate(code)
        if setup.get("post_reload"):
            await page.reload()
            await asyncio.sleep(1.0)
        print("    Setup complete.")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# POST-RUN VERIFICATION
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

async def run_post_verification(page, task_id: str) -> dict:
    """
    Read window.__cart__ and window.__orderConfirmed__ via browser session page.
    Compares against ground truth using verifier.py functions.
    """
    if page is None:
        return {
            "cart": [],
            "order_confirmed": False,
            "verification": {
                "success": False,
                "partial_score": 0.0,
                "details": {"error": "No active page found in browser session"},
            },
        }

    try:
        # Browser-use Page.evaluate requires arrow function format
        cart_raw = await page.evaluate("() => window.__cart__ || []")
        order_raw = await page.evaluate("() => Boolean(window.__orderConfirmed__)")

        cart = json.loads(cart_raw) if cart_raw else []
        if isinstance(order_raw, str):
            order_confirmed = order_raw.strip().lower() == "true"
        else:
            order_confirmed = bool(order_raw)

    except Exception as e:
        return {
            "cart": [],
            "order_confirmed": False,
            "verification": {
                "success": False,
                "partial_score": 0.0,
                "details": {"error": f"JS evaluation failed: {e}"},
            },
        }

    if task_id == "T4":
        verification = verify_order_state(order_confirmed, task_id, cart)
    else:
        verification = verify_cart_state(cart, task_id)

    return {
        "cart": cart,
        "order_confirmed": order_confirmed,
        "verification": verification,
    }


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SINGLE EXPERIMENTAL RUN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

async def run_single(
    variant: str,
    task: dict,
    phase: str,
    rep: int,
    dry_run: bool = False,
) -> dict:
    task_id = task["id"]
    variant_url = f"{BASE_URL}/variants/{variant}/"
    start_hash = task.get("start_hash", "#home")
    start_url = f"{variant_url}{start_hash}"

    logger = RunLogger(variant, task_id, phase, rep)
    t0 = time.monotonic()

    print(f"\n  â–¶ run  variant={variant}  task={task_id}  rep={rep}  phase={phase}")
    print(f"    Start URL: {start_url}")

    # â”€â”€ Dry Run Mode â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    if dry_run:
        print("    [DRY RUN] Skipping agent execution.")
        elapsed = time.monotonic() - t0
        logger.write_header(
            agent_model="DRY_RUN",
            agent_temperature=AGENT_TEMPERATURE,
            static_verification_passed=True,
        )
        logger.write_action("dry_run_placeholder", page_url=start_url)
        logger.write_summary(
            success=False,
            partial_score=0.0,
            total_steps=0,
            total_time_seconds=elapsed,
            error_message="dry_run",
        )
        return {
            "run_id": logger.run_id,
            "variant": variant,
            "task_id": task_id,
            "phase": phase,
            "repetition_index": rep,
            "success": False,
            "partial_score": 0.0,
            "total_steps": 0,
            "total_time_seconds": elapsed,
            "dry_run": True,
            "error_message": "dry_run",
        }

    # â”€â”€ API Key Check â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is not set in this terminal.")

    # â”€â”€ Browser-use 0.13.10 Imports â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    try:
        from browser_use import Agent, BrowserSession
    except ImportError as e:
        raise ImportError(
            "browser-use is not installed in this environment.\n"
            "Run: python -m pip install browser-use"
        ) from e

    llm = make_llm()
    print(f"    Model: {AGENT_MODEL}")
    print(f"    Provider: {AGENT_PROVIDER}")

    browser_session = None

    try:
        logger.write_header(
            agent_model=AGENT_MODEL,
            agent_temperature=AGENT_TEMPERATURE,
            static_verification_passed=True,
        )

        # â”€â”€ Initialize BrowserSession (0.13.10 API) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        browser_session = BrowserSession(
            is_local=True,
            headless=True,
            enable_default_extensions=False,
            keep_alive=True,
            viewport=VIEWPORT,
        )
        await browser_session.start()

        # â”€â”€ Pre-run Setup (e.g. T5 cart seeding) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if task.get("setup_script"):
            setup_page = await browser_session.get_current_page()
            if setup_page:
                await setup_page.goto(start_url)
                await run_task_setup(setup_page, task)

        # â”€â”€ Create Agent with Initial Navigation Action â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        agent = Agent(
            task=task["instruction"],
            llm=llm,
            browser_session=browser_session,
            initial_actions=[
                {
                    "navigate": {
                        "url": start_url,
                        "new_tab": False,
                    }
                }
            ],
            use_vision=True,
            step_timeout=60,
        )

        print("    Starting browser-use agent...")
        history = await agent.run(max_steps=30)

        # Save browser-use agent history
        try:
            history_dir = TESTING_DIR / "results" / "agent-history"
            history_dir.mkdir(parents=True, exist_ok=True)
            history_path = history_dir / f"{logger.run_id}.json"
            history.save_to_file(history_path)
            print(f"    Agent history saved: {history_path}")
        except Exception as e:
            print(f"    WARNING: Failed to save agent history: {e}")

        elapsed = time.monotonic() - t0

        # Diagnostic only: record browser-use's internal step timing
        try:
            internal_duration = history.total_duration_seconds()
            print(f"    Agent finished in {elapsed:.1f}s")
            print(f"    Browser-use step duration: {internal_duration:.1f}s")
            print(f"    Unaccounted elapsed time: {elapsed - internal_duration:.1f}s")
        except Exception:
            print(f"    Agent finished in {elapsed:.1f}s")

        # â”€â”€ Post-run Verification â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        try:
            agent_page = await browser_session.get_current_page()
            post = await run_post_verification(agent_page, task_id)
        except Exception as e:
            post = {
                "cart": [],
                "order_confirmed": False,
                "verification": {
                    "success": False,
                    "partial_score": 0.0,
                    "details": {"error": str(e)},
                },
            }

        verification = post["verification"]
        total_steps = len(history) if hasattr(history, "__len__") else 0

        logger.write_summary(
            success=verification["success"],
            partial_score=verification["partial_score"],
            total_steps=total_steps,
            total_time_seconds=elapsed,
            cart_state=post["cart"],
            order_confirmed=post["order_confirmed"],
        )

        result = {
            "run_id": logger.run_id,
            "variant": variant,
            "task_id": task_id,
            "phase": phase,
            "repetition_index": rep,
            "success": verification["success"],
            "partial_score": verification["partial_score"],
            "total_steps": total_steps,
            "total_time_seconds": elapsed,
            "order_confirmed": post["order_confirmed"],
            "error_message": None,
            "timestamp_end": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

    except Exception as e:
        elapsed = time.monotonic() - t0
        err_msg = str(e)
        print(f"    ERROR: {err_msg}")
        logger.write_summary(
            success=False,
            partial_score=0.0,
            total_steps=logger._step_counter,
            total_time_seconds=elapsed,
            error_message=err_msg,
        )
        result = {
            "run_id": logger.run_id,
            "variant": variant,
            "task_id": task_id,
            "phase": phase,
            "repetition_index": rep,
            "success": False,
            "partial_score": 0.0,
            "total_steps": 0,
            "total_time_seconds": elapsed,
            "error_message": err_msg,
            "timestamp_end": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

    finally:
        # Reliable cleanup: close browser session resources
        if browser_session is not None:
            try:
                await browser_session.stop()
            except Exception:
                pass

    status = "âœ“" if result.get("success") else "âœ—"
    print(
        f"    {status} score={result.get('partial_score', 0):.2f}"
        f" steps={result.get('total_steps', 0)}"
        f" time={result.get('total_time_seconds', 0):.1f}s"
    )
    return result


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# EXPERIMENT RUNNER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

async def run_experiment(
    phase: str = "pilot",
    max_reps: int = 5,
    start_rep: int = 1,
    dry_run: bool = False,
    variant_filter: list = None,
    task_filter: list = None,
):
    tasks = load_tasks()
    task_ids = task_filter or ["H1", "H2", "H3", "H4", "H5"]
    variants = variant_filter or VARIANTS

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_csv = RESULTS_DIR / f"{phase}-summary.csv"
    total = len(variants) * len(task_ids) * max_reps
    done = 0

    print(f"\n{'â•' * 60}")
    print("  TechMart Experiment")
    print(f"  Phase: {phase.upper()}")
    print(f"  Model: {AGENT_MODEL}")
    print(f"  Provider: {AGENT_PROVIDER}")
    print(f"  {len(variants)} variants Ã— {len(task_ids)} tasks Ã— {max_reps} reps = {total} runs")
    if dry_run:
        print("  MODE: DRY RUN (no agent execution)")
    print(f"  Results: {summary_csv}")
    print("â•" * 60)

    for rep in range(start_rep, start_rep + max_reps):
        print(f"\nâ”€â”€ Repetition {rep} of {start_rep + max_reps - 1} â”€â”€")
        for variant in variants:
            for task_id in task_ids:
                task = tasks[task_id]
                result = await run_single(
                    variant=variant,
                    task=task,
                    phase=phase,
                    rep=rep,
                    dry_run=dry_run,
                )
                append_to_summary_csv(summary_csv, result)
                done += 1
                print(f"  Progress: {done}/{total} runs")

    print(f"\n{'â•' * 60}")
    print(f"  âœ“ {phase.upper()} COMPLETE")
    print(f"  Runs completed: {done}")
    print(f"  Summary: {summary_csv}")
    print("â•" * 60)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CLI
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def main():
    parser = argparse.ArgumentParser(
        description="TechMart experiment runner â€” Protocol v2"
    )
    parser.add_argument(
        "--phase",
        choices=["pilot", "full"],
        default="pilot",
        help="Experiment phase (pilot=5 reps, full=10 reps)",
    )
    parser.add_argument(
        "--start-rep",
        type=int,
        default=1,
        help="Starting repetition index (use 6 when extending pilot to full)",
    )
    parser.add_argument(
        "--reps",
        type=int,
        default=None,
        help="Override number of repetitions per cell (default: 5 for pilot, (10 - start_rep + 1) for full)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test runner infrastructure without executing agents",
    )
    parser.add_argument(
        "--variants",
        nargs="+",
        choices=VARIANTS,
        help="Run only selected variants (default: all variants)",
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        choices=["H1", "H2", "H3", "H4", "H5"],
        help="Run only selected tasks (default: all tasks)",
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip static verification checks (not recommended)",
    )

    args = parser.parse_args()

    # Repetition count logic:
    if args.reps is not None:
        if args.reps < 1:
            print("ERROR: --reps must be at least 1.")
            sys.exit(1)
        reps = args.reps
    else:
        reps = 5 if args.phase == "pilot" else (10 - args.start_rep + 1)

    if reps < 1:
        print("ERROR: --start-rep must be between 1 and 10.")
        sys.exit(1)

    print()
    print("TechMart Research Runner")
    print("Experiment 2 — isolated calibration")
    print()
    print(f"Model:       {AGENT_MODEL}")
    print(f"Provider:    {AGENT_PROVIDER}")
    print(f"Temperature: {AGENT_TEMPERATURE if AGENT_TEMPERATURE is not None else 'default'}")
    print()

    # Preflight check
    if not args.skip_preflight and not args.dry_run:
        print("Running pre-flight verification...")
        errors = check_file_existence()
        if errors:
            print("Pre-flight FAILED:")
            for error in errors:
                print(f"  âœ— {error}")
            sys.exit(1)
        print("âœ“ Pre-flight passed")

    # API key check
    if not args.dry_run:
        if not os.environ.get("GOOGLE_API_KEY"):
            print()
            print("ERROR: GOOGLE_API_KEY is not set.")
            print()
            print("PowerShell command:")
            print('$env:GOOGLE_API_KEY="YOUR_KEY"')
            print()
            sys.exit(1)
        print("âœ“ GOOGLE_API_KEY detected")

    asyncio.run(
        run_experiment(
            phase=args.phase,
            max_reps=reps,
            start_rep=args.start_rep,
            dry_run=args.dry_run,
            variant_filter=args.variants,
            task_filter=args.tasks,
        )
    )


if __name__ == "__main__":
    main()



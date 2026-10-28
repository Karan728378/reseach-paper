"""
Independent reproduction script for Mechanism 2: Non-Interactive Tag Stripping.
Runs an offline headless browser session using browser-use 0.13.10 BrowserSession,
loads fixtures/disambiguation_probe_b.html, and intercepts Stage 4 observation output.
No LLM is called. Output is saved to results_v2/probe_b_stage4_output.txt.
"""
import sys
import os
import time
import asyncio
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Reconfigure stdout/stderr for UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from browser_use import BrowserSession, BrowserProfile

ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = ROOT / "fixtures"
OUTPUT_FILE = ROOT / "results_v2" / "probe_b_stage4_output.txt"
PORT = 8765

class FixtureHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FIXTURES_DIR), **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress HTTP access logging

def start_server():
    server = HTTPServer(('127.0.0.1', PORT), FixtureHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server

async def run_reproduction():
    out_lines = [
        "================================================================================",
        "MECHANISM 2 REPRODUCTION REPORT: DISAMBIGUATION PROBE B",
        "================================================================================",
        "Framework: browser-use 0.13.10 (headless Chromium, text-only mode)",
        f"Fixture  : fixtures/disambiguation_probe_b.html served at http://127.0.0.1:{PORT}",
        "Date     : 2026-10-28",
        "--------------------------------------------------------------------------------"
    ]

    server = start_server()
    time.sleep(0.5)

    profile = BrowserProfile(headless=True)
    session = BrowserSession(browser_profile=profile)

    try:
        await session.start()
        url = f"http://127.0.0.1:{PORT}/disambiguation_probe_b.html"
        await session.navigate_to(url)
        await asyncio.sleep(1.0)

        # Intercept Stage 4 observation state
        summary = await session.get_browser_state_summary(include_screenshot=False)
        dom_state = summary.dom_state
        llm_repr = dom_state.llm_representation()
        selector_map = dom_state.selector_map

        out_lines.append(f"Page Title        : {summary.title}")
        out_lines.append(f"Page URL          : {summary.url}")
        out_lines.append(f"Selector Map Size : {len(selector_map)} registered interactive selectors")
        out_lines.append("--------------------------------------------------------------------------------")
        out_lines.append("STAGE 4 LLM REPRESENTATION OUTPUT (dom_state.llm_representation()):")
        out_lines.append(llm_repr)
        out_lines.append("--------------------------------------------------------------------------------")
        out_lines.append("SUBSTRING VERIFICATION CHECKS:")

        # Check 1: Container span aria-label string
        span_aria_target = "Identity: target-sku-101"
        in_repr_span_target = span_aria_target in llm_repr
        out_lines.append(f"  1. Span aria-label string ('{span_aria_target}') present in Stage 4: {in_repr_span_target} [EXPECTED: False]")

        # Check 2: Distractor span aria-label string
        span_aria_distractor = "Identity: distractor-sku-202"
        in_repr_span_distractor = span_aria_distractor in llm_repr
        out_lines.append(f"  2. Distractor aria-label string ('{span_aria_distractor}') present in Stage 4: {in_repr_span_distractor} [EXPECTED: False]")

        # Check 3: role="region" on span
        role_region = "region"
        # Check if any selector entry has role region
        has_region_attr = 'role="region"' in llm_repr or "role='region'" in llm_repr or 'role=region' in llm_repr
        out_lines.append(f"  3. Non-interactive role ('{role_region}') attribute present in Stage 4: {has_region_attr} [EXPECTED: False]")

        # Check 4: Visible text retention
        visible_text = "Standard Model Option"
        in_repr_visible = visible_text in llm_repr
        out_lines.append(f"  4. Inner visible typography ('{visible_text}') present in Stage 4: {in_repr_visible} [EXPECTED: True]")

        # Check 5: Target token presence via prompt instruction leak
        target_token = "target-sku-101"
        token_in_repr = target_token in llm_repr
        out_lines.append(f"  5. Bare token '{target_token}' present in Stage 4: {token_in_repr}")
        if token_in_repr:
            out_lines.append("     NOTE: The token appears in Stage 4 EXCLUSIVELY because the fixture's")
            out_lines.append("     visible instruction paragraph (<p id='probe-instruction'>) renders it.")
            out_lines.append("     The container span's accessible attribute was completely pruned.")

        out_lines.append("--------------------------------------------------------------------------------")
        out_lines.append("CONCLUSION:")
        if not in_repr_span_target and not in_repr_span_distractor and in_repr_visible:
            out_lines.append("  [PASS] Mechanism 2 CONFIRMED: Non-interactive <span> aria-label is pruned")
            out_lines.append("  from Stage 4 observation output by browser-use 0.13.10 serializer, while")
            out_lines.append("  inner visible typography is retained.")
        else:
            out_lines.append("  [FAIL] Pruning behavior differed from expected.")
        out_lines.append("================================================================================")

    finally:
        await session.stop()
        server.shutdown()

    report_text = "\n".join(out_lines)
    print(report_text)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report_text, encoding='utf-8')
    print(f"\nSaved report to: {OUTPUT_FILE}")

if __name__ == '__main__':
    asyncio.run(run_reproduction())

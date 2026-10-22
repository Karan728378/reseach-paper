import asyncio
import os
import sys
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Add runner and audit dirs
AUDIT_DIR = Path(r"C:\testing\research_audit_20261015_231500")
sys.path.insert(0, str(AUDIT_DIR))
sys.path.insert(0, r"C:\testing\runner")

from stub_model import OfflineStubChatModel
from browser_use import Agent, BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

PORT = 8899
SERVER_ROOT = Path(r"C:\testing")

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SERVER_ROOT), **kwargs)
    def log_message(self, format, *args):
        pass

def start_server():
    try:
        server = ThreadingHTTPServer(('127.0.0.1', PORT), CustomHandler)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        print(f"Server listening on http://127.0.0.1:{PORT}")
    except Exception as e:
        print(f"Server start note: {e}")

start_server()

TEST_URL = f"http://127.0.0.1:{PORT}/research_audit_20261015_231500/fixtures/channel_test.html"

TOKENS = {
    "VISIBLE_TEXT": "VISIBLE-TEXT-DESCRIPTION-TOKEN-1122",
    "ARIA_INTERACTIVE": "ARIA-LABEL-TOKEN-3344",
    "ARIA_HIDDEN": "ARIA-HIDDEN-TOKEN-5566",
    "ARIA_NON_INTERACTIVE": "ARIA-DIV-TOKEN-9900",
    "DATA_ATTR_INTERACTIVE": "DATA-SKU-TOKEN-8899",
    "DATA_ATTR_NON_INTERACTIVE": "DATA-LOT-TOKEN-4455",
    "JSONLD_SCRIPT": "JSONLD-ONLY-DESCRIPTION-TOKEN-7788",
    "META_TAG": "inventory-stock",
    "DATETIME_ATTR": "2026-10-15T00:00:00Z",
    "TEMPORAL_TEXT": "(verified 2026-10-15)",
}

CUSTOM_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-sku", "data-action", "data-field", "data-lot-code", "data-stock",
    "aria-label", "aria-describedby", "datetime"
]

async def evaluate_pipeline(case_name: str, include_attrs=None, patch_serializer=False, inject_metadata=False):
    print(f"\n========================================================")
    print(f"TESTING PIPELINE: {case_name}")
    print(f"  include_attributes: {include_attrs is not None} (count={len(include_attrs) if include_attrs else 0})")
    print(f"  patch_serializer: {patch_serializer}")
    print(f"  inject_metadata: {inject_metadata}")
    print(f"========================================================")

    if patch_serializer:
        import importlib
        agent_runner = importlib.import_module("agent-runner")
        agent_runner.enable_observable_dom_serialization()

    stub_llm = OfflineStubChatModel()
    profile = BrowserProfile(
        headless=True,
        allowed_domains=['127.0.0.1', 'localhost', '*']
    )
    session = BrowserSession(browser_profile=profile)
    await session.start()

    try:
        agent = Agent(
            task="Find product details",
            llm=stub_llm,
            browser_session=session,
            use_vision=True,
            include_attributes=include_attrs,
        )

        page = await session.get_current_page()
        await page.goto(TEST_URL)
        await asyncio.sleep(0.5)

        # Optional metadata injection hook (matching agent-runner.py)
        meta_str = None
        if inject_metadata:
            import importlib
            agent_runner = importlib.import_module("agent-runner")
            meta_str = await agent_runner.extract_active_page_metadata(page)

        state = await session.get_browser_state_summary()
        dom_text = state.dom_state.llm_representation(include_attributes=include_attrs)

        agent._message_manager.create_state_messages(
            browser_state_summary=state,
            result=None,
            step_info=None
        )
        messages = agent._message_manager.get_messages()

        # Combine text across messages
        all_text = ""
        has_screenshot = False
        screenshot_len = 0

        for m in messages:
            if isinstance(m.content, str):
                all_text += "\n" + m.content
            elif isinstance(m.content, list):
                for p in m.content:
                    if isinstance(p, dict):
                        if p.get("type") == "text":
                            all_text += "\n" + (p.get("text") or "")
                        elif p.get("type") == "image_url":
                            has_screenshot = True
                            url = p.get("image_url", {}).get("url", "")
                            screenshot_len = len(url)

        if inject_metadata and meta_str:
            all_text += "\n" + meta_str

        # Check tokens
        token_results = {}
        for token_name, token_val in TOKENS.items():
            in_dom = token_val in dom_text
            in_messages = token_val in all_text
            token_results[token_name] = {
                "in_dom_representation": in_dom,
                "in_model_messages": in_messages
            }
            print(f"  {token_name:25s} | DOM: {str(in_dom):5s} | Messages: {str(in_messages):5s}")

        # Save captured observation
        out_data = {
            "case_name": case_name,
            "has_screenshot": has_screenshot,
            "screenshot_base64_len": screenshot_len,
            "dom_representation": dom_text,
            "injected_metadata": meta_str,
            "token_results": token_results,
            "messages": [
                {
                    "role": m.__class__.__name__,
                    "content": m.content if isinstance(m.content, str) else [
                        {"type": p.get("type"), "text_snippet": (p.get("text", "")[:300] if p.get("type") == "text" else None)}
                        for p in m.content if isinstance(p, dict)
                    ]
                }
                for m in messages
            ]
        }
        out_file = AUDIT_DIR / f"observation_{case_name}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(out_data, f, indent=2, ensure_ascii=False)
        print(f"Saved observation record to {out_file}")

        return out_data

    finally:
        await session.stop()

async def main():
    results = {}
    
    # 1. Default Pipeline (Original Experiment 1 config)
    results["default_pipeline"] = await evaluate_pipeline(
        "default_pipeline",
        include_attrs=None,
        patch_serializer=False,
        inject_metadata=False
    )

    # 2. Configured Attributes Only (include_attributes whitelist)
    results["configured_attrs_unpatched"] = await evaluate_pipeline(
        "configured_attrs_unpatched",
        include_attrs=CUSTOM_ATTRIBUTES,
        patch_serializer=False,
        inject_metadata=False
    )

    # 3. Configured Attributes + Patched Serializer
    results["configured_attrs_patched"] = await evaluate_pipeline(
        "configured_attrs_patched",
        include_attrs=CUSTOM_ATTRIBUTES,
        patch_serializer=True,
        inject_metadata=False
    )

    # 4. Full Observable Pipeline (Patched Serializer + Metadata Injection)
    results["full_observable_pipeline"] = await evaluate_pipeline(
        "full_observable_pipeline",
        include_attrs=CUSTOM_ATTRIBUTES,
        patch_serializer=True,
        inject_metadata=True
    )

    summary_file = AUDIT_DIR / "channel_exposure_matrix.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nMatrix successfully written to {summary_file}")

if __name__ == "__main__":
    asyncio.run(main())

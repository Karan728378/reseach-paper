import asyncio
import os
import sys
import json
from pathlib import Path

# Add runner and audit dirs
AUDIT_DIR = Path(r"C:\testing\research_audit_20261015_231500")
sys.path.insert(0, str(AUDIT_DIR))
sys.path.insert(0, r"C:\testing\runner")

from stub_model import OfflineStubChatModel
from browser_use import Agent, BrowserSession
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

FIXTURE_PATH = (AUDIT_DIR / "fixtures" / "channel_test.html").resolve()
_fixture_path_str = str(FIXTURE_PATH).replace("\\", "/")
FIXTURE_URL = f"file:///{_fixture_path_str}"

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

async def run_test_case(case_name: str, include_attrs=None, patch_serializer=False):
    print(f"\n========================================================")
    print(f"RUNNING TEST CASE: {case_name}")
    print(f"include_attributes: {include_attrs is not None} (len={len(include_attrs) if include_attrs else 0})")
    print(f"patch_serializer: {patch_serializer}")
    print(f"========================================================")

    if patch_serializer:
        import importlib
        agent_runner = importlib.import_module("agent-runner")
        agent_runner.enable_observable_dom_serialization()

    stub_llm = OfflineStubChatModel()
    
    session = BrowserSession(
        is_local=True,
        headless=True,
        enable_default_extensions=False,
        keep_alive=True,
        viewport={"width": 1280, "height": 800},
    )
    await session.start()

    try:
        agent = Agent(
            task="Find the product details on the page and complete.",
            llm=stub_llm,
            browser_session=session,
            initial_actions=[{"navigate": {"url": FIXTURE_URL, "new_tab": False}}],
            use_vision=True,
            step_timeout=30,
            include_attributes=include_attrs,
            max_actions_per_step=1,
            max_failures=1,
        )

        print("Executing single agent step with stub LLM...")
        try:
            # Run 1 step
            await agent.step()
        except Exception as e:
            print(f"Agent step finished/interrupted: {e}")

        captured = stub_llm.captured_calls
        print(f"Captured LLM calls: {len(captured)}")

        # Save captured call
        out_file = AUDIT_DIR / f"captured_observation_{case_name}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(captured, f, indent=2, ensure_ascii=False)
        print(f"Saved captured observation to: {out_file}")

        # Extract text content from all captured messages
        all_text = ""
        has_screenshot = False
        screenshot_len = 0

        if captured:
            first_call = captured[0]
            for msg in first_call:
                content = msg.get("content")
                if isinstance(content, str):
                    all_text += "\n" + content
                parts = msg.get("content_parts", [])
                for part in parts:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            all_text += "\n" + (part.get("text") or "")
                        elif part.get("type") == "image_url":
                            has_screenshot = True
                            screenshot_len = part.get("url_length", 0)

        # Check token presence in captured model messages
        results = {}
        for name, token in TOKENS.items():
            present = token in all_text
            results[name] = present

        results["HAS_SCREENSHOT"] = has_screenshot
        results["SCREENSHOT_URL_LENGTH"] = screenshot_len

        print(f"\nToken detection results for {case_name}:")
        for k, v in results.items():
            print(f"  {k:30s}: {v}")

        return results

    finally:
        await session.stop()

async def main():
    summary_report = {}

    # Case 1: Default browser-use (no custom attributes, unpatched serializer)
    res_default = await run_test_case(
        "default_pipeline",
        include_attrs=None,
        patch_serializer=False
    )
    summary_report["default_pipeline"] = res_default

    # Case 2: Configured attribute whitelist only (unpatched serializer)
    custom_attrs = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
        "data-sku", "data-action", "data-field", "data-lot-code", "data-stock",
        "aria-label", "aria-describedby", "datetime"
    ]
    res_cfg_attrs = await run_test_case(
        "configured_attrs_unpatched",
        include_attrs=custom_attrs,
        patch_serializer=False
    )
    summary_report["configured_attrs_unpatched"] = res_cfg_attrs

    # Case 3: Configured attributes + Patched serializer
    res_patched = await run_test_case(
        "configured_attrs_patched",
        include_attrs=custom_attrs,
        patch_serializer=True
    )
    summary_report["configured_attrs_patched"] = res_patched

    # Save summary report
    summary_file = AUDIT_DIR / "channel_exposure_matrix.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2)
    print(f"\n========================================================")
    print(f"EXPOSURE AUDIT COMPLETE. Matrix saved to: {summary_file}")
    print(f"========================================================")

if __name__ == "__main__":
    asyncio.run(main())

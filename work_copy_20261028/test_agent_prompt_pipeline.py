"""
Agent Prompt Pipeline Verification Suite
Executes the actual browser-use Agent observation-building and prompt-generation path
using a local MockChatModel (subclassing FakeListChatModel with provider='google', model='gemini-flash-lite-latest', model_name='gemini-flash-lite-latest').
Zero API calls, zero paid quota, zero credentials.
"""
import asyncio
import http.server
import json
import os
import sys
import threading
import time
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from langchain_core.language_models import FakeListChatModel
from browser_use import Agent, BrowserSession
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

class MockChatModel(FakeListChatModel):
    provider: str = "google"
    model: str = "gemini-flash-lite-latest"
    model_name: str = "gemini-flash-lite-latest"

EXTENDED_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-field", "data-product-id", "data-category", "data-category-slug",
    "data-amount", "data-rating", "data-review-count", "data-stock-status",
    "data-in-stock", "data-warranty", "data-lot-code", "data-action"
]

PORT = 8093

def start_server():
    os.chdir(r"C:\testing")
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd

DUMMY_JSON = json.dumps({
    "thinking": "Observation test complete",
    "evaluation_previous_goal": "Success",
    "memory": "Observation test",
    "next_goal": "done",
    "action": [{"done": {"text": "Finished observation test"}}]
})

async def inspect_agent_prompt(variant: str, use_extended_attrs: bool = False, patch_serializer: bool = False):
    if patch_serializer:
        import importlib
        sys.path.insert(0, r"C:\testing\runner")
        agent_runner = importlib.import_module("agent-runner")
        agent_runner.enable_observable_dom_serialization()

    attrs = EXTENDED_ATTRIBUTES if use_extended_attrs else DEFAULT_INCLUDE_ATTRIBUTES
    
    session = BrowserSession(headless=True, keep_alive=True)
    await session.start()
    
    url = f"http://localhost:{PORT}/variants/{variant}/index.html#home"
    llm = MockChatModel(responses=[DUMMY_JSON] * 5)
    
    captured_messages = []
    
    try:
        agent = Agent(
            task="Inspect product information for SoundFlow Air 3",
            llm=llm,
            browser_session=session,
            initial_actions=[{"navigate": {"url": url, "new_tab": False}}],
            use_vision=False,
            include_attributes=attrs,
        )
        
        orig_create_state_messages = agent._message_manager.create_state_messages
        
        def wrapped_create_state_messages(*args, **kwargs):
            res = orig_create_state_messages(*args, **kwargs)
            try:
                msgs = agent._message_manager.get_messages()
                for idx, m in enumerate(msgs):
                    content_str = ""
                    if hasattr(m, 'content'):
                        if isinstance(m.content, list):
                            content_str = " ".join([c.get("text", "") if isinstance(c, dict) else getattr(c, "text", str(c)) for c in m.content])
                        else:
                            content_str = str(m.content)
                    else:
                        content_str = str(m)
                    captured_messages.append({
                        "msg_index": idx,
                        "type": type(m).__name__,
                        "text": content_str
                    })
            except Exception as e:
                captured_messages.append({"error": str(e)})
            return res
            
        agent._message_manager.create_state_messages = wrapped_create_state_messages
        
        await agent.run(max_steps=1)
        
    finally:
        await session.stop()
        
    return captured_messages

async def main():
    httpd = start_server()
    time.sleep(0.5)
    
    results = {}
    
    try:
        print("=== 1. Testing v0-baseline (VIS) ===")
        msgs_v0 = await inspect_agent_prompt("v0-baseline", use_extended_attrs=False, patch_serializer=False)
        full_text_v0 = " ".join([m.get("text", "") for m in msgs_v0])
        results["v0_prompt_has_price_text"] = "$49.99" in full_text_v0
        results["v0_prompt_has_soundflow"] = "SoundFlow Air 3" in full_text_v0
        results["v0_prompt_has_aria_btn"] = "aria-label=Add item to cart" in full_text_v0
        results["v0_prompt_has_data_attrs"] = "data-action=" in full_text_v0
        print(f"  v0 message count: {len(msgs_v0)}, total text length: {len(full_text_v0)}")
        print(f"  v0 has '$49.99': {results['v0_prompt_has_price_text']}")
        print(f"  v0 has 'SoundFlow Air 3': {results['v0_prompt_has_soundflow']}")
        print(f"  v0 has aria on btn: {results['v0_prompt_has_aria_btn']}")
        print(f"  v0 has data-action: {results['v0_prompt_has_data_attrs']}")

        print("\n=== 2. Testing v2-aria (ARIA) ===")
        msgs_v2 = await inspect_agent_prompt("v2-aria", use_extended_attrs=False, patch_serializer=False)
        full_text_v2 = " ".join([m.get("text", "") for m in msgs_v2])
        results["v2_prompt_has_price_text"] = "$49.99" in full_text_v2
        results["v2_prompt_has_aria_btn"] = "aria-label=Add item to cart" in full_text_v2
        results["v2_prompt_has_aria_price_span"] = "aria-label=Price: $49.99" in full_text_v2
        print(f"  v2 message count: {len(msgs_v2)}, total text length: {len(full_text_v2)}")
        print(f"  v2 has '$49.99' in visible text: {results['v2_prompt_has_price_text']}")
        print(f"  v2 has aria on btn: {results['v2_prompt_has_aria_btn']}")
        print(f"  v2 has aria on price span (non-interactive): {results['v2_prompt_has_aria_price_span']}")

        print("\n=== 3. Testing v3-data-attrs WITHOUT extended attributes ===")
        msgs_v3_def = await inspect_agent_prompt("v3-data-attrs", use_extended_attrs=False, patch_serializer=False)
        full_text_v3_def = " ".join([m.get("text", "") for m in msgs_v3_def])
        results["v3_def_prompt_has_data_action"] = "data-action=" in full_text_v3_def
        print(f"  v3 (default attrs) has data-action: {results['v3_def_prompt_has_data_action']}")

        print("\n=== 4. Testing v3-data-attrs WITH extended attributes (DATA-CFG) ===")
        msgs_v3_ext = await inspect_agent_prompt("v3-data-attrs", use_extended_attrs=True, patch_serializer=False)
        full_text_v3_ext = " ".join([m.get("text", "") for m in msgs_v3_ext])
        results["v3_ext_prompt_has_data_action"] = "data-action=" in full_text_v3_ext
        results["v3_ext_prompt_has_data_product_id"] = "data-product-id=" in full_text_v3_ext
        results["v3_ext_prompt_has_data_amount"] = "data-amount=" in full_text_v3_ext
        print(f"  v3 (extended attrs) has data-action: {results['v3_ext_prompt_has_data_action']}")
        print(f"  v3 (extended attrs) has data-product-id: {results['v3_ext_prompt_has_data_product_id']}")
        print(f"  v3 (extended attrs) has data-amount: {results['v3_ext_prompt_has_data_amount']}")

        print("\n=== 5. Testing v1-jsonld ===")
        msgs_v1 = await inspect_agent_prompt("v1-jsonld", use_extended_attrs=True, patch_serializer=False)
        full_text_v1 = " ".join([m.get("text", "") for m in msgs_v1])
        results["v1_prompt_has_jsonld"] = "application/ld+json" in full_text_v1 or "schema.org" in full_text_v1
        print(f"  v1 has JSON-LD in prompt: {results['v1_prompt_has_jsonld']}")
        
    finally:
        httpd.shutdown()
        
    print("\n" + "="*60)
    print("LIVE AGENT PROMPT PIPELINE TEST RESULTS:")
    print("="*60)
    for k, v in results.items():
        print(f"  {k}: {v}")
    print("="*60)
    return results

if __name__ == "__main__":
    asyncio.run(main())

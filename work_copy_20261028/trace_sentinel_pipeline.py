"""
Trace Sentinel Pipeline
Traces unique sentinel tokens across 6 observation pipeline stages:
1. Source HTML
2. Live DOM (CDP Runtime.evaluate)
3. Chromium Blink Accessibility Tree (CDP Accessibility.getFullAXTree)
4. browser-use Serializer (Default vs Extended Whitelist)
5. Agent Observation Buffer (MessageManager.create_state_messages)
6. Model-Client Request Payload (Arguments received by LLM client ainvoke)

Zero-cost, offline, reproducible instrumentation.
"""

import asyncio
import http.server
import json
import os
import sys
import threading
import time
from pathlib import Path

# Paths
WORKSPACE_ROOT = Path("C:/testing")
RESEARCH_DIR = WORKSPACE_ROOT / "research_execution_20261018"
FIXTURE_PATH = RESEARCH_DIR / "fixtures" / "sentinel_fixture.html"
OUTPUT_JSON_PATH = RESEARCH_DIR / "sentinel_stage_trace.json"
PORT = 8097

sys.path.insert(0, str(RESEARCH_DIR))

from langchain_core.language_models import FakeListChatModel
from browser_use import Agent, BrowserSession
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES
from browser_use.dom.serializer.serializer import DISABLED_ELEMENTS
import protocol_v3_runner

SENTINEL_TOKENS = {
    "visible_text": {
        "token": "SENTINEL_TEXT_ALPHA_991",
        "description": "Visible text inside <p>",
        "channel": "Visible Typography"
    },
    "aria_button": {
        "token": "SENTINEL_ARIA_BETA_992",
        "description": "aria-label on interactive <button>",
        "channel": "WAI-ARIA Interactive"
    },
    "aria_span": {
        "token": "SENTINEL_SPAN_ARIA_993",
        "description": "aria-label on non-interactive <span>",
        "channel": "WAI-ARIA Non-Interactive"
    },
    "data_button": {
        "token": "SENTINEL_DATA_GAMMA_994",
        "description": "data-sentinel-action on interactive <button>",
        "channel": "Custom data-* Interactive"
    },
    "data_container": {
        "token": "SENTINEL_DATA_DELTA_995",
        "description": "data-sentinel-field on non-interactive <div>",
        "channel": "Custom data-* Non-Interactive"
    },
    "jsonld_name": {
        "token": "SENTINEL_JSONLD_EPSILON_996",
        "description": "Schema.org JSON-LD product name in <script>",
        "channel": "Schema.org JSON-LD"
    },
    "jsonld_sku": {
        "token": "SENTINEL_SKU_ZETA_997",
        "description": "Schema.org JSON-LD sku in <script>",
        "channel": "Schema.org JSON-LD"
    },
    "meta_tag": {
        "token": "SENTINEL_META_ETA_998",
        "description": "Standard HTML <meta> content",
        "channel": "Standard HTML Meta"
    }
}

EXTENDED_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-sentinel-action", "data-sentinel-field", "data-action", "data-product-id"
]

def start_server():
    cwd = os.getcwd()
    os.chdir(str(WORKSPACE_ROOT))
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    os.chdir(cwd)
    return httpd

class PayloadCaptureMockModel(FakeListChatModel):
    provider: str = "google"
    model: str = "gemini-flash-lite-latest"
    model_name: str = "gemini-flash-lite-latest"
    captured_payloads: list = []

    async def ainvoke(self, input, config=None, **kwargs):
        # Record raw client payload
        serialized_input = []
        if isinstance(input, list):
            for msg in input:
                serialized_input.append({
                    "type": getattr(msg, "type", str(type(msg))),
                    "content": msg.content if isinstance(msg.content, str) else str(msg.content)
                })
        else:
            serialized_input.append({"raw": str(input)})
        self.captured_payloads.append(serialized_input)
        return await super().ainvoke(input, config=config, **kwargs)

async def run_sentinel_trace():
    print(f"[+] Loading fixture: {FIXTURE_PATH}")
    source_html = FIXTURE_PATH.read_text(encoding="utf-8")

    server = start_server()
    time.sleep(0.5)

    trace_results = {}
    for key, meta in SENTINEL_TOKENS.items():
        trace_results[key] = {
            "token": meta["token"],
            "description": meta["description"],
            "channel": meta["channel"],
            "stage_1_source_html": meta["token"] in source_html,
            "stage_2_live_dom": False,
            "stage_3_blink_axtree": False,
            "stage_4a_serializer_default": False,
            "stage_4b_serializer_extended": False,
            "stage_5_observation_buffer": False,
            "stage_6_client_request_payload": False
        }

    session = BrowserSession(headless=True)
    await session.start()

    fixture_url = f"http://127.0.0.1:{PORT}/research_execution_20261018/fixtures/sentinel_fixture.html"

    try:
        await session.navigate_to(fixture_url)
        await asyncio.sleep(0.5)

        # Stage 2: Live DOM via CDP Runtime.evaluate
        target_info = await session.get_current_target_info()
        tid = target_info.get("targetId") or target_info.get("target_id")
        cdp = await session.get_or_create_cdp_session(target_id=tid, focus=False)

        eval_res = await cdp.cdp_client.send.Runtime.evaluate(
            params={"expression": "document.documentElement.outerHTML"},
            session_id=cdp.session_id
        )
        live_dom_html = eval_res.get("result", {}).get("value", "")

        for key, meta in SENTINEL_TOKENS.items():
            if meta["token"] in live_dom_html:
                trace_results[key]["stage_2_live_dom"] = True

        # Stage 3: Chromium Blink AXTree via CDP
        ax_res = await cdp.cdp_client.send.Accessibility.getFullAXTree(
            session_id=cdp.session_id
        )
        ax_nodes = ax_res.get("nodes", [])
        ax_json_str = json.dumps(ax_nodes)

        for key, meta in SENTINEL_TOKENS.items():
            if meta["token"] in ax_json_str:
                trace_results[key]["stage_3_blink_axtree"] = True

        # Stage 4: browser-use Serializer
        summary = await session.get_browser_state_summary()
        obs_default = summary.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)
        obs_extended = summary.dom_state.llm_representation(include_attributes=EXTENDED_ATTRIBUTES)

        for key, meta in SENTINEL_TOKENS.items():
            if meta["token"] in obs_default:
                trace_results[key]["stage_4a_serializer_default"] = True
            if meta["token"] in obs_extended:
                trace_results[key]["stage_4b_serializer_extended"] = True

    finally:
        await session.stop()

    # Stage 5 & 6: Agent Observation Buffer & Model Client Request Payload
    mock_response = json.dumps({
        "thinking": "Inspecting sentinel testbench",
        "evaluation_previous_goal": "Success",
        "memory": "",
        "next_goal": "done",
        "action": [{"done": {"text": "Verified"}}]
    })

    client_llm = PayloadCaptureMockModel(responses=[mock_response])
    agent_session = BrowserSession(headless=True)
    await agent_session.start()

    captured_state_messages = []
    try:
        agent = Agent(
            task="Audit sentinel tokens",
            llm=client_llm,
            browser_session=agent_session,
            use_vision=False,
            initial_actions=[{"navigate": {"url": fixture_url, "new_tab": False}}]
        )

        orig_create = agent._message_manager.create_state_messages
        def intercept_create(*args, **kwargs):
            res = orig_create(*args, **kwargs)
            msgs = agent._message_manager.get_messages()
            for m in msgs:
                content = m.content if isinstance(m.content, str) else str(m.content)
                captured_state_messages.append(content)
            return res
        agent._message_manager.create_state_messages = intercept_create

        await agent.run(max_steps=1)

    finally:
        await agent_session.stop()
        server.shutdown()

    state_msgs_str = " ".join(captured_state_messages)
    payload_str = json.dumps(client_llm.captured_payloads)

    for key, meta in SENTINEL_TOKENS.items():
        if meta["token"] in state_msgs_str:
            trace_results[key]["stage_5_observation_buffer"] = True
        if meta["token"] in payload_str:
            trace_results[key]["stage_6_client_request_payload"] = True

    # Output report
    output_data = {
        "audit_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "fixture_url": fixture_url,
        "disabled_elements_constant": list(DISABLED_ELEMENTS),
        "default_include_attributes": list(DEFAULT_INCLUDE_ATTRIBUTES),
        "extended_attributes": EXTENDED_ATTRIBUTES,
        "results": trace_results
    }

    OUTPUT_JSON_PATH.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"[+] Sentinel stage trace saved to: {OUTPUT_JSON_PATH}")
    return output_data

if __name__ == "__main__":
    asyncio.run(run_sentinel_trace())

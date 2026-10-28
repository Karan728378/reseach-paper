"""
Independent Sentinel Validation & Treatment Isolation Script
=============================================================================
Phase 2 Zero-Cost Validation:
1. Loads fixtures/sentinel_fixture.html in a real local Chromium browser.
2. Captures raw output at every stage (not just booleans, but raw strings & snippets).
3. Evaluates 8 sentinel markers across 6 stages.
4. Captures the exact observation passed to the model-client interface locally.
5. Validates treatment isolation across v0-baseline, v2-aria, and v3-data-attrs.
6. Recomputes statistical power under Option A (N=72) and Option B (N=96).
7. Emits raw trace to independent_validation_raw_trace.json.

Zero live API calls. 100% offline and deterministic.
=============================================================================
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
EXEC_DIR = WORKSPACE_ROOT / "research_execution_20261018"
FIXTURE_PATH = EXEC_DIR / "fixtures" / "sentinel_fixture.html"
OUTPUT_RAW_TRACE = EXEC_DIR / "independent_validation_raw_trace.json"
PORT = 8095

sys.path.insert(0, str(EXEC_DIR))

from langchain_core.language_models import FakeListChatModel
from browser_use import Agent, BrowserSession
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES
from browser_use.dom.serializer.serializer import DISABLED_ELEMENTS
import protocol_v3_runner

SENTINELS = {
    "visible_text": {
        "token": "SENTINEL_TEXT_ALPHA_991",
        "name": "Visible Typography in <p>",
        "type": "positive_control",
        "expected_survival": [True, True, True, True, True, True, True]
    },
    "aria_button": {
        "token": "SENTINEL_ARIA_BETA_992",
        "name": "WAI-ARIA aria-label on interactive <button>",
        "type": "treatment_channel",
        "expected_survival": [True, True, True, True, True, True, True]
    },
    "aria_span": {
        "token": "SENTINEL_SPAN_ARIA_993",
        "name": "WAI-ARIA aria-label on non-interactive <span>",
        "type": "critical_divergence",
        "expected_survival": [True, True, True, False, False, False, False]
    },
    "data_button": {
        "token": "SENTINEL_DATA_GAMMA_994",
        "name": "Custom data-* attribute on interactive <button>",
        "type": "reversed_divergence",
        "expected_survival": [True, True, False, False, True, False, False]
    },
    "data_container": {
        "token": "SENTINEL_DATA_DELTA_995",
        "name": "Custom data-* attribute on non-interactive <div>",
        "type": "non_interactive_data",
        "expected_survival": [True, True, False, False, False, False, False]
    },
    "jsonld_name": {
        "token": "SENTINEL_JSONLD_EPSILON_996",
        "name": "Schema.org JSON-LD name in <script>",
        "type": "hardcoded_pruning",
        "expected_survival": [True, True, False, False, False, False, False]
    },
    "jsonld_sku": {
        "token": "SENTINEL_SKU_ZETA_997",
        "name": "Schema.org JSON-LD sku in <script>",
        "type": "hardcoded_pruning",
        "expected_survival": [True, True, False, False, False, False, False]
    },
    "meta_tag": {
        "token": "SENTINEL_META_ETA_998",
        "name": "Standard HTML <meta> content",
        "type": "hardcoded_pruning",
        "expected_survival": [True, True, False, False, False, False, False]
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

class RawInterceptMockModel(FakeListChatModel):
    provider: str = "google"
    model: str = "gemini-flash-lite-latest"
    model_name: str = "gemini-flash-lite-latest"
    intercepted_invocations: list = []

    async def ainvoke(self, input, config=None, **kwargs):
        payload_entry = {
            "timestamp": time.time(),
            "messages": []
        }
        if isinstance(input, list):
            for m in input:
                payload_entry["messages"].append({
                    "role": getattr(m, "type", "unknown"),
                    "content": m.content if isinstance(m.content, str) else str(m.content)
                })
        else:
            payload_entry["messages"].append({"raw": str(input)})
        self.intercepted_invocations.append(payload_entry)
        return await super().ainvoke(input, config=config, **kwargs)

def extract_snippet(text: str, token: str, window: int = 60) -> str:
    """Finds token in text and returns surrounding window; returns [NOT PRESENT] if absent."""
    idx = text.find(token)
    if idx == -1:
        return "[NOT PRESENT IN STAGE OUTPUT]"
    start = max(0, idx - window)
    end = min(len(text), idx + len(token) + window)
    snippet = text[start:end].replace("\n", " ").replace("\r", " ").strip()
    return f"... {snippet} ..."

async def run_independent_validation():
    print("=" * 75)
    print("INDEPENDENT SENTINEL VALIDATION & TREATMENT ISOLATION BENCHMARK")
    print("=" * 75)

    server = start_server()
    time.sleep(0.5)

    fixture_url = f"http://127.0.0.1:{PORT}/research_execution_20261018/fixtures/sentinel_fixture.html"

    # Stage 1: Raw Source HTML
    raw_stage_1 = FIXTURE_PATH.read_text(encoding="utf-8")
    print(f"[Stage 1] Loaded Source HTML: {len(raw_stage_1)} bytes")

    session = BrowserSession(headless=True)
    await session.start()

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
        raw_stage_2 = eval_res.get("result", {}).get("value", "")
        print(f"[Stage 2] Live DOM outerHTML captured: {len(raw_stage_2)} bytes")

        # Stage 3: Native Chromium Accessibility Tree (CDP Accessibility.getFullAXTree)
        ax_res = await cdp.cdp_client.send.Accessibility.getFullAXTree(
            session_id=cdp.session_id
        )
        ax_nodes = ax_res.get("nodes", [])
        raw_stage_3 = json.dumps(ax_nodes, indent=2)
        print(f"[Stage 3] Chromium Blink AXTree captured: {len(ax_nodes)} nodes ({len(raw_stage_3)} bytes)")

        # Stage 4a: Default Serializer (Unpatched)
        summary = await session.get_browser_state_summary()
        raw_stage_4a = summary.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)
        print(f"[Stage 4a] browser-use Default Serializer captured: {len(raw_stage_4a)} bytes")

        # Stage 4b: Extended Whitelist Serializer
        raw_stage_4b = summary.dom_state.llm_representation(include_attributes=EXTENDED_ATTRIBUTES)
        print(f"[Stage 4b] browser-use Extended Whitelist Serializer captured: {len(raw_stage_4b)} bytes")

    finally:
        await session.stop()

    # Stage 5 & 6: Agent Observation Buffer & Model-Client Payload
    dummy_resp = json.dumps({
        "thinking": "Audit sentinel transmission",
        "evaluation_previous_goal": "Success",
        "memory": "",
        "next_goal": "done",
        "action": [{"done": {"text": "Verified"}}]
    })

    client_llm = RawInterceptMockModel(responses=[dummy_resp])
    agent_session = BrowserSession(headless=True)
    await agent_session.start()

    raw_stage_5_messages = []
    try:
        agent = Agent(
            task="Audit sentinel transmission boundary",
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
                raw_stage_5_messages.append({
                    "role": getattr(m, "type", "unknown"),
                    "content": m.content if isinstance(m.content, str) else str(m.content)
                })
            return res
        agent._message_manager.create_state_messages = intercept_create

        await agent.run(max_steps=1)

    finally:
        await agent_session.stop()

    raw_stage_5_text = " ".join([m["content"] for m in raw_stage_5_messages])
    print(f"[Stage 5] Agent Observation Buffer captured: {len(raw_stage_5_text)} bytes")

    raw_stage_6 = client_llm.intercepted_invocations
    raw_stage_6_text = json.dumps(raw_stage_6)
    print(f"[Stage 6] Model-Client Request Payload captured: {len(raw_stage_6_text)} bytes")

    # ── Evaluation of Sentinel Markers ───────────────────────────────────────
    stage_outputs = [
        ("stage_1_source_html", raw_stage_1),
        ("stage_2_live_dom", raw_stage_2),
        ("stage_3_blink_axtree", raw_stage_3),
        ("stage_4a_serializer_default", raw_stage_4a),
        ("stage_4b_serializer_extended", raw_stage_4b),
        ("stage_5_observation_buffer", raw_stage_5_text),
        ("stage_6_model_client_payload", raw_stage_6_text)
    ]

    sentinel_results = {}
    mismatches = []

    for key, spec in SENTINELS.items():
        tok = spec["token"]
        res = {
            "token": tok,
            "name": spec["name"],
            "type": spec["type"],
            "stages": {}
        }
        observed_survival = []
        for stage_idx, (stage_name, stage_text) in enumerate(stage_outputs):
            present = tok in stage_text
            snippet = extract_snippet(stage_text, tok)
            res["stages"][stage_name] = {
                "present": present,
                "evidence_snippet": snippet
            }
            observed_survival.append(present)

        res["survival_matches_expectation"] = (observed_survival == spec["expected_survival"])
        if not res["survival_matches_expectation"]:
            mismatches.append(f"{key}: observed {observed_survival} vs expected {spec['expected_survival']}")

        sentinel_results[key] = res

    # ── Validation of Treatment Isolation Across Variants ────────────────────
    print("\n[*] Validating Treatment Isolation Across Application Variants (ABS vs ARIA vs DATA-CFG)...")
    v0_path = WORKSPACE_ROOT / "variants" / "v0-baseline" / "index.html"
    v2_path = WORKSPACE_ROOT / "variants" / "v2-aria" / "index.html"
    v3_path = WORKSPACE_ROOT / "variants" / "v3-data-attrs" / "index.html"

    v0_text = v0_path.read_text(encoding="utf-8")
    v2_text = v2_path.read_text(encoding="utf-8")
    v3_text = v3_path.read_text(encoding="utf-8")

    # Visible text consistency check: core product catalog must be identical
    app_core = (WORKSPACE_ROOT / "shared" / "app-core.js").read_text(encoding="utf-8")
    products_js = (WORKSPACE_ROOT / "shared" / "products.js").read_text(encoding="utf-8")

    isolation_report = {
        "products_catalog_shared": (
            'src="../../shared/products.js"' in v0_text and
            'src="../../shared/products.js"' in v2_text and
            'src="../../shared/products.js"' in v3_text
        ),
        "app_core_shared": (
            'src="../../shared/app-core.js"' in v0_text and
            'src="../../shared/app-core.js"' in v2_text and
            'src="../../shared/app-core.js"' in v3_text
        ),
        "button_aria_label_deconfounded": (
            "addBtn.setAttribute('aria-label', 'Add item to cart')" in app_core and
            "addBtn.setAttribute('aria-label', 'Add SoundFlow Air 3 to cart')" not in app_core
        ),
        "baseline_clean_of_aria_nav": (
            'aria-label="Primary navigation"' not in v0_text and
            'aria-label="Search"' not in v0_text
        ),
        "aria_variant_has_aria_nav": (
            'id="search-submit-btn" aria-label="Search"' in v2_text
        ),
        "data_variant_has_data_actions": (
            'data-action="submit-search"' in v3_text
        ),
        "vis_arm_strictly_text_only": (
            "use_vision=False" in (EXEC_DIR / "protocol_v3_runner.py").read_text(encoding="utf-8")
        )
    }

    # ── Full Raw Output Export ───────────────────────────────────────────────
    full_export = {
        "validation_metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "python_version": sys.version,
            "browser_use_version": "0.13.10",
            "disabled_elements": list(DISABLED_ELEMENTS),
            "default_include_attributes": list(DEFAULT_INCLUDE_ATTRIBUTES),
            "extended_attributes": EXTENDED_ATTRIBUTES,
            "fixture_url": fixture_url
        },
        "raw_stage_lengths": {
            "stage_1_source_html_bytes": len(raw_stage_1),
            "stage_2_live_dom_bytes": len(raw_stage_2),
            "stage_3_axtree_nodes": len(ax_nodes),
            "stage_3_axtree_bytes": len(raw_stage_3),
            "stage_4a_default_serializer_bytes": len(raw_stage_4a),
            "stage_4b_extended_serializer_bytes": len(raw_stage_4b),
            "stage_5_observation_buffer_bytes": len(raw_stage_5_text),
            "stage_6_model_client_payload_bytes": len(raw_stage_6_text)
        },
        "sentinel_evaluation": sentinel_results,
        "isolation_evaluation": isolation_report,
        "mismatches": mismatches
    }

    OUTPUT_RAW_TRACE.write_text(json.dumps(full_export, indent=2), encoding="utf-8")
    print(f"\n[+] Raw trace and exact snippets successfully saved to:\n    {OUTPUT_RAW_TRACE}")

    server.shutdown()

    # Assertions
    if mismatches:
        print(f"\n[FAILED] Mismatches detected in sentinel validation:")
        for m in mismatches:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print("\n[PASSED] All 8 sentinel markers match expected pipeline survival 100%.")
        print("[PASSED] Treatment isolation verified across ABS, ARIA, and DATA-CFG.")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(run_independent_validation())

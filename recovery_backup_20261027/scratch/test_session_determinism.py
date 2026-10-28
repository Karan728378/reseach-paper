import asyncio
import hashlib
import json
from browser_use import BrowserSession
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

async def test_determinism():
    session = BrowserSession(headless=True)
    await session.start()
    url = "http://127.0.0.1:8098/variants/v0-baseline/index.html#home"

    prompts = []
    ax_counts = []
    sel_counts = []

    try:
        target_info = await session.get_current_target_info()
        tid = target_info.get("targetId") or target_info.get("target_id")
        cdp_session = await session.get_or_create_cdp_session(target_id=tid, focus=False)

        for i in range(3):
            # Navigate cleanly and reset cart
            await session.navigate_to(url)
            await asyncio.sleep(0.4)
            await cdp_session.cdp_client.send.Runtime.evaluate(
                params={"expression": "localStorage.clear(); window.__cart__ = []; if (window.__refreshCartView__) window.__refreshCartView__();"},
                session_id=cdp_session.session_id
            )
            await asyncio.sleep(0.2)

            ax_response = await cdp_session.cdp_client.send.Accessibility.getFullAXTree(
                session_id=cdp_session.session_id
            )
            ax_nodes = ax_response.get("nodes", [])
            ax_counts.append(len(ax_nodes))

            summary = await session.get_browser_state_summary()
            sel_counts.append(len(summary.dom_state.selector_map))
            obs = summary.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)
            h = hashlib.sha256(obs.encode('utf-8')).hexdigest()
            prompts.append(h)

        print(f"AX counts: {ax_counts}")
        print(f"Selector counts: {sel_counts}")
        print(f"Prompt hashes: {prompts}")
        print(f"Deterministic: {len(set(prompts)) == 1}")

    finally:
        await session.stop()

if __name__ == "__main__":
    asyncio.run(test_determinism())

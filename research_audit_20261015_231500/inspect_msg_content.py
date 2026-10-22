import asyncio
import sys
from pathlib import Path

AUDIT_DIR = Path(r"C:\testing\research_audit_20261015_231500")
sys.path.insert(0, str(AUDIT_DIR))

from stub_model import OfflineStubChatModel
from browser_use import Agent, BrowserSession
from browser_use.browser.profile import BrowserProfile

TEST_URL = f"http://127.0.0.1:8899/research_audit_20261015_231500/fixtures/channel_test.html"

async def test():
    stub_llm = OfflineStubChatModel()
    profile = BrowserProfile(headless=True, allowed_domains=['*'])
    session = BrowserSession(browser_profile=profile)
    await session.start()
    try:
        agent = Agent(task="Find product details", llm=stub_llm, browser_session=session)
        page = await session.get_current_page()
        await page.goto(TEST_URL)
        await asyncio.sleep(0.5)

        state = await session.get_browser_state_summary()
        agent._message_manager.create_state_messages(
            browser_state_summary=state,
            result=None,
            step_info=None
        )
        msgs = agent._message_manager.get_messages()
        user_msg = msgs[-1]
        print("user_msg class:", user_msg.__class__.__name__)
        print("user_msg.content type:", type(user_msg.content))
        if isinstance(user_msg.content, list):
            for i, p in enumerate(user_msg.content):
                print(f"\nPart {i} type: {type(p)}")
                print(f"Part {i} repr: {repr(p)[:300]}")
                if hasattr(p, "text"):
                    print(f"  has .text! text len={len(p.text)}")
                    print(f"  snippet: {p.text[:300]}")
                elif hasattr(p, "image_url"):
                    print(f"  has .image_url!")
                elif isinstance(p, dict):
                    print("  dict keys:", list(p.keys()))
    finally:
        await session.stop()

asyncio.run(test())

import asyncio
import traceback
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AUDIT_DIR = Path(r"C:\testing\research_audit_20261015_231500")
sys.path.insert(0, str(AUDIT_DIR))

from stub_model import OfflineStubChatModel
from browser_use import Agent, BrowserSession
from browser_use.browser.profile import BrowserProfile

PORT = 8899
SERVER_ROOT = Path(r"C:\testing")

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SERVER_ROOT), **kwargs)
    def log_message(self, format, *args):
        pass # suppress logs

def run_server():
    server = ThreadingHTTPServer(('127.0.0.1', PORT), CustomHandler)
    server.serve_forever()

# Start background server
t = threading.Thread(target=run_server, daemon=True)
t.start()
print(f"Local server started on http://127.0.0.1:{PORT}")

TEST_URL = f"http://127.0.0.1:{PORT}/research_audit_20261015_231500/fixtures/channel_test.html"

async def test():
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
        )
        page = await session.get_current_page()
        await page.goto(TEST_URL)
        await asyncio.sleep(1.0)

        # 1. Inspect DOM state
        state = await session.get_browser_state_summary()
        print("\n--- DOM LLM REPRESENTATION (DEFAULT) ---")
        dom_text = state.dom_state.llm_representation()
        print(dom_text)

        # 2. Inspect MessageManager messages
        agent._message_manager.create_state_messages(
            browser_state_summary=state,
            result=None,
            step_info=None
        )
        messages = agent._message_manager.get_messages()
        print(f"\nTotal messages in MessageManager: {len(messages)}")
        for i, m in enumerate(messages):
            print(f"Msg {i}: {m.__class__.__name__}")
            if isinstance(m.content, str):
                print(f"  Text ({len(m.content)} chars): {m.content[:300]}...")
            elif isinstance(m.content, list):
                print(f"  Parts: {len(m.content)}")
                for p in m.content:
                    if isinstance(p, dict):
                        print(f"    type={p.get('type')}")
                        if p.get('type') == 'text':
                            print(f"      text ({len(p.get('text', ''))} chars): {p.get('text', '')[:300]}...")
                        elif p.get('type') == 'image_url':
                            url = p.get('image_url', {}).get('url', '')
                            print(f"      image_url len={len(url)}")

    except Exception:
        traceback.print_exc()
    finally:
        await session.stop()

asyncio.run(test())

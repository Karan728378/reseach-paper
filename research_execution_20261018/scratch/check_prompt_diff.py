import asyncio
from browser_use import BrowserSession
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

import http.server
import threading
import os
from pathlib import Path

def start_server():
    os.chdir(r"C:\testing")
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, port

async def check_diff():
    httpd, port = start_server()
    session = BrowserSession(headless=True)
    await session.start()
    url = f"http://127.0.0.1:{port}/variants/v0-baseline/index.html#home"
    try:
        await session.navigate_to(url)
        await asyncio.sleep(0.5)
        s1 = await session.get_browser_state_summary()
        p1 = s1.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)

        s2 = await session.get_browser_state_summary()
        p2 = s2.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)

        print(f"p1 == p2 without navigation: {p1 == p2}")
        if p1 != p2:
            import difflib
            diff = list(difflib.unified_diff(p1.splitlines(), p2.splitlines()))
            print("\n".join(diff[:20]))

        # Now test after re-navigating to same url
        await session.navigate_to(url)
        await asyncio.sleep(0.5)
        s3 = await session.get_browser_state_summary()
        p3 = s3.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)
        print(f"p1 == p3 after re-navigation: {p1 == p3}")
        if p1 != p3:
            import difflib
            diff = list(difflib.unified_diff(p1.splitlines(), p3.splitlines()))
            print("\n".join(diff[:20]))

    finally:
        await session.stop()
        httpd.shutdown()

if __name__ == "__main__":
    asyncio.run(check_diff())

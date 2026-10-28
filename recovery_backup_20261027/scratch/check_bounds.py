import asyncio
import sys
sys.path.insert(0, r"C:\testing\research_execution_20261018")
import compare_accessibility_tree as cat

async def check_bounds():
    server = cat.start_server()
    try:
        session = cat.BrowserSession(headless=True)
        await session.start()
        try:
            url = f"http://127.0.0.1:{cat.PORT}/variants/v0-baseline/index.html#home"
            await session.navigate_to(url)
            await asyncio.sleep(0.5)
            summary = await session.get_browser_state_summary()
            
            target_info = await session.get_current_target_info()
            tid = target_info.get("targetId") or target_info.get("target_id")
            cdp = await session.get_or_create_cdp_session(target_id=tid)
            res = await cdp.cdp_client.send.Runtime.evaluate(
                params={
                    "expression": """
                    Array.from(document.querySelectorAll('.product-stock')).map(e => ({
                        text: e.textContent.trim(),
                        className: e.className,
                        width: e.getBoundingClientRect().width,
                        height: e.getBoundingClientRect().height,
                        cursor: window.getComputedStyle(e).cursor
                    }))
                    """,
                    "returnByValue": True
                },
                session_id=cdp.session_id
            )
            print("All product-stock spans on page:")
            for s in res.get("result", {}).get("value", []):
                print(" ", s)
            res = await cdp.cdp_client.send.Runtime.evaluate(
                params={
                    "expression": """
                    Array.from(document.querySelectorAll('.product-stock')).map(e => ({
                        text: e.textContent.trim(),
                        width: e.getBoundingClientRect().width,
                        height: e.getBoundingClientRect().height
                    }))
                    """,
                    "returnByValue": True
                },
                session_id=cdp.session_id
            )
            print("All product-stock spans on page:")
            for s in res.get("result", {}).get("value", []):
                print(" ", s)
        finally:
            await session.stop()
    finally:
        server.shutdown()

if __name__ == "__main__":
    asyncio.run(check_bounds())

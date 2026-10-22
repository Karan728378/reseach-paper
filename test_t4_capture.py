import asyncio
import json
from playwright.async_api import async_playwright

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        print("Navigating to home...")
        await page.goto("http://localhost:8080/variants/v0-baseline/#home")
        
        print("Adding item to cart...")
        await page.evaluate("() => { window.__cart__.push({sku: 'mse-001', name: 'ErgoGlide Mouse', price: 59.99, quantity: 1}); }")
        
        cart_after_add = await page.evaluate("() => window.__cart__ || []")
        print(f"Cart after add: {cart_after_add}")
        
        print("Navigating to checkout...")
        await page.evaluate("() => { window.location.hash = '#checkout'; }")
        
        await page.wait_for_selector("#field-name")
        await page.evaluate("""() => {
            document.getElementById('field-name').value = 'Jane';
            document.getElementById('field-address').value = '123 Test';
            document.getElementById('checkout-form').dispatchEvent(new Event('submit'));
        }""")
        
        print("Extracting state...")
        cart_raw = await page.evaluate("() => window.__cart__ || []")
        order_raw = await page.evaluate("() => Boolean(window.__orderConfirmed__)")
        last_order_raw = await page.evaluate("() => window.__lastOrder__ ? window.__lastOrder__.items : []")
        
        cart = json.loads(cart_raw) if isinstance(cart_raw, str) else cart_raw
        last_order = json.loads(last_order_raw) if isinstance(last_order_raw, str) else last_order_raw
        
        print(f"Cart empty? {len(cart) == 0}")
        print(f"Order confirmed? {order_raw}")
        print(f"Last order items: {last_order}")
        
        has_mouse = any(i.get("sku") == "mse-001" for i in last_order)
        print(f"Has mouse? {has_mouse}")
        
        assert order_raw is True
        assert has_mouse is True
        assert len(cart) == 0
        
        await browser.close()
        print("Test passed!")

if __name__ == "__main__":
    asyncio.run(run_test())

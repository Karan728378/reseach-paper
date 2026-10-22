"""
End-to-End Treatment Delivery Verification Suite
Validates the exact observation pipeline of browser-use 0.13.10 with live Chromium CDP.
Runs against local HTTP server mirroring production experiment setup.
"""
import asyncio
import http.server
import os
import sys
import threading
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from browser_use import BrowserSession
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

PORT = 8095

EXTENDED_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-field", "data-product-id", "data-category", "data-category-slug",
    "data-amount", "data-rating", "data-review-count", "data-stock-status",
    "data-in-stock", "data-warranty", "data-lot-code", "data-action"
]

def start_server():
    os.chdir(r"C:\testing")
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd

async def run_e2e_verification():
    httpd = start_server()
    time.sleep(0.5)
    
    session = BrowserSession(is_local=True, headless=True)
    await session.start()
    
    report = {}
    
    try:
        # ── 1. v0-baseline (VIS) ─────────────────────────────────────────────
        url_v0 = f"http://localhost:{PORT}/variants/v0-baseline/index.html#home"
        await session.navigate_to(url_v0)
        await asyncio.sleep(1.0)
        sum_v0 = await session.get_browser_state_summary(include_screenshot=False)
        rep_v0 = sum_v0.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)
        
        report["v0_visible_text_delivered"] = ("SoundFlow Air 3" in rep_v0) and ("$49.99" in rep_v0) and ("4.2" in rep_v0)
        report["v0_no_aria_enhancements"] = "aria-label=Add item to cart" not in rep_v0
        report["v0_no_data_actions"] = "data-action=" not in rep_v0
        
        # ── 2. v2-aria (ARIA) ────────────────────────────────────────────────
        url_v2 = f"http://localhost:{PORT}/variants/v2-aria/index.html#home"
        await session.navigate_to(url_v2)
        await asyncio.sleep(1.0)
        sum_v2 = await session.get_browser_state_summary(include_screenshot=False)
        rep_v2 = sum_v2.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)
        
        # In v2, interactive elements receive aria-label which is in DEFAULT_INCLUDE_ATTRIBUTES
        report["v2_aria_delivered_on_interactive"] = (
            "aria-label=Add item to cart" in rep_v2 and
            "aria-label=Search products" in rep_v2
        )
        # But non-interactive elements (span.product-price) are omitted by unpatched DOMTreeSerializer
        report["v2_noninteractive_aria_omitted"] = "aria-label=Price: $49.99" not in rep_v2
        
        # ── 3. v3-data-attrs (DATA-CFG) ──────────────────────────────────────
        url_v3 = f"http://localhost:{PORT}/variants/v3-data-attrs/index.html#home"
        await session.navigate_to(url_v3)
        await asyncio.sleep(1.0)
        sum_v3 = await session.get_browser_state_summary(include_screenshot=False)
        rep_v3_default = sum_v3.dom_state.llm_representation(include_attributes=DEFAULT_INCLUDE_ATTRIBUTES)
        rep_v3_extended = sum_v3.dom_state.llm_representation(include_attributes=EXTENDED_ATTRIBUTES)
        
        # Default whitelist strips data-*
        report["v3_default_whitelist_strips_data_attrs"] = (
            "data-action=" not in rep_v3_default and
            "data-product-id=" not in rep_v3_default
        )
        # Extended whitelist delivers data-* on interactive elements
        report["v3_extended_whitelist_delivers_data_attrs"] = (
            "data-action=browse-category" in rep_v3_extended and
            "data-category-slug=audio" in rep_v3_extended and
            "data-product-id=wh-001" in rep_v3_extended
        )
        
        # ── 4. v1-jsonld (Pruned by Serializer) ──────────────────────────────
        url_v1 = f"http://localhost:{PORT}/variants/v1-jsonld/index.html#home"
        await session.navigate_to(url_v1)
        await asyncio.sleep(1.0)
        sum_v1 = await session.get_browser_state_summary(include_screenshot=False)
        rep_v1 = sum_v1.dom_state.llm_representation(include_attributes=EXTENDED_ATTRIBUTES)
        
        report["v1_jsonld_pruned_by_serializer"] = (
            "application/ld+json" not in rep_v1 and
            "schema.org" not in rep_v1
        )
        
    finally:
        await session.stop()
        httpd.shutdown()
        
    print("=" * 60)
    print("END-TO-END OBSERVATION DELIVERY VERIFICATION RESULTS")
    print("=" * 60)
    all_passed = True
    for test_name, status in report.items():
        pass_fail = "PASS" if status else "FAIL"
        if not status:
            all_passed = False
        print(f"[{pass_fail}] {test_name}: {status}")
    print("=" * 60)
    print(f"Overall Status: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_e2e_verification())
    sys.exit(0 if success else 1)

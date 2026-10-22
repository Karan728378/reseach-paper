"""
TechMart Offline Validation Suite — Phase 1 Observable Instrumentation
runner/test_offline_extraction.py

Deterministic tests validating:
1. Secret sanitization and zero credential leakage.
2. Observable DOM serialization patch (data-*, aria-*, datetime on interactive & non-interactive elements).
3. Live metadata extraction (JSON-LD, page metadata) across all 5 variants.
4. Dynamic SPA refresh (metadata updates upon hash navigation; no persistence of stale schemas).
5. Treatment isolation (v0 receives 0% metadata, each variant exposes only its intended modality).
6. Output directory routing isolation (exp1_observable/ directory separation).

ZERO calls to Google Gemini / LLM APIs.
"""

import asyncio
import json
import logging
import os
import re
import sys
from pathlib import Path

# Suppress noisy library logs during tests
logging.getLogger("browser_use").setLevel(logging.WARNING)
logging.getLogger("cdp_use").setLevel(logging.WARNING)

RUNNER_DIR = Path(__file__).parent
sys.path.insert(0, str(RUNNER_DIR))

import importlib
agent_runner = importlib.import_module("agent-runner")

OBSERVABLE_ATTRIBUTES = agent_runner.OBSERVABLE_ATTRIBUTES
DEFAULT_RESULTS_DIR = agent_runner.DEFAULT_RESULTS_DIR
enable_observable_dom_serialization = agent_runner.enable_observable_dom_serialization
extract_active_page_metadata = agent_runner.extract_active_page_metadata
sanitize_secret_leakage = agent_runner.sanitize_secret_leakage
from browser_use import BrowserSession

VIEWPORT = {"width": 1280, "height": 800}
BASE_URL = "http://localhost:8080"


# ══════════════════════════════════════════════════════════════════════════════
# 1. SECRET SANITIZATION TESTS
# ══════════════════════════════════════════════════════════════════════════════

def test_secret_sanitization():
    print("▶ Running test_secret_sanitization...")
    dummy_key = "AIzaSyB1234567890abcdefghijklmnopqrstuv"
    sample_text = f"Calling API with key {dummy_key} and Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.token"
    sanitized = sanitize_secret_leakage(sample_text)
    
    assert dummy_key not in sanitized, "Google API key leaked in sanitized text!"
    assert "[REDACTED_API_KEY]" in sanitized, "Missing [REDACTED_API_KEY] replacement!"
    assert "Bearer [REDACTED_TOKEN]" in sanitized, "Bearer token not sanitized!"
    
    # Test real env key if present
    env_key = os.environ.get("GOOGLE_API_KEY")
    if env_key:
        test_env_leak = f"System environment has GOOGLE_API_KEY={env_key}"
        sanitized_env = sanitize_secret_leakage(test_env_leak)
        assert env_key not in sanitized_env, "Environment GOOGLE_API_KEY leaked!"
        assert "[REDACTED_API_KEY]" in sanitized_env
    
    print("  ✓ test_secret_sanitization passed.")


# ══════════════════════════════════════════════════════════════════════════════
# 2. OUTPUT ROUTING ISOLATION TESTS
# ══════════════════════════════════════════════════════════════════════════════

def test_output_routing():
    print("▶ Running test_output_routing...")
    expected_dir = Path("C:/testing/results/exp1_observable")
    assert DEFAULT_RESULTS_DIR == expected_dir, f"Expected {expected_dir}, got {DEFAULT_RESULTS_DIR}"
    
    # Verify historical datasets are not modified
    results_dir = Path("C:/testing/results")
    assert (results_dir / "pilot-summary-clean.csv").exists(), "Original pilot-summary-clean.csv missing!"
    assert (results_dir / "final-statistical-results.csv").exists(), "Original final-statistical-results.csv missing!"
    
    print("  ✓ test_output_routing passed.")


# ══════════════════════════════════════════════════════════════════════════════
# 3. LIVE DOM EXTRACTION & TREATMENT ISOLATION TESTS (OFFLINE)
# ══════════════════════════════════════════════════════════════════════════════

async def run_browser_tests():
    print("▶ Running browser-use offline DOM extraction & serialization tests...")
    
    enable_observable_dom_serialization()
    
    session = BrowserSession(
        is_local=True,
        headless=True,
        enable_default_extensions=False,
        keep_alive=True,
        viewport=VIEWPORT,
    )
    await session.start()
    
    try:
        page = await session.get_current_page()
        
        # ── Test Variant 0: v0-baseline ───────────────────────────────────────
        print("  Checking v0-baseline...")
        await page.goto(f"{BASE_URL}/variants/v0-baseline/#home")
        await asyncio.sleep(0.5)
        
        # Metadata extraction must return None
        v0_meta = await extract_active_page_metadata(page)
        assert v0_meta is None, f"v0-baseline must not produce metadata! Got: {v0_meta}"
        
        # DOM representation must contain 0 custom data-* and 0 aria-*
        state_v0 = await session.get_browser_state_summary()
        dom_v0 = state_v0.dom_state.llm_representation(include_attributes=OBSERVABLE_ATTRIBUTES)
        assert "data-field=" not in dom_v0, "v0-baseline leaked data-field in DOM!"
        assert "data-product-id=" not in dom_v0, "v0-baseline leaked data-product-id in DOM!"
        assert 'aria-label="Price:' not in dom_v0, "v0-baseline leaked aria-label in DOM!"
        assert "datetime=" not in dom_v0, "v0-baseline leaked datetime in DOM!"
        print("    ✓ v0-baseline treatment isolation verified.")

        # ── Test Variant 1: v1-jsonld & Dynamic SPA Refresh ───────────────────
        print("  Checking v1-jsonld dynamic SPA navigation...")
        # Step 1: #home
        await page.goto(f"{BASE_URL}/variants/v1-jsonld/#home")
        await asyncio.sleep(0.5)
        v1_home_meta = await extract_active_page_metadata(page)
        assert v1_home_meta is not None, "v1-jsonld missing JSON-LD on home!"
        assert "WebSite" in v1_home_meta, "v1-jsonld missing WebSite schema on home!"
        assert "Store" in v1_home_meta, "v1-jsonld missing Store schema on home!"
        
        # Step 2: Navigate to #search?q=keyboard
        await page.goto(f"{BASE_URL}/variants/v1-jsonld/#search?q=keyboard")
        await asyncio.sleep(0.5)
        v1_search_meta = await extract_active_page_metadata(page)
        assert v1_search_meta is not None
        assert "ItemList" in v1_search_meta, "v1-jsonld missing ItemList on search route!"
        
        # Step 3: Navigate to #product/mkp-001
        await page.goto(f"{BASE_URL}/variants/v1-jsonld/#product/mkp-001")
        await asyncio.sleep(0.5)
        v1_prod_meta = await extract_active_page_metadata(page)
        assert v1_prod_meta is not None
        assert "Product" in v1_prod_meta, "v1-jsonld missing Product schema on product route!"
        assert "ItemList" not in v1_prod_meta, "Stale ItemList schema persisted to product route!"
        print("    ✓ v1-jsonld dynamic SPA refresh & freshness verified.")

        # ── Test Variant 2: v2-aria ───────────────────────────────────────────
        print("  Checking v2-aria...")
        await page.goto(f"{BASE_URL}/variants/v2-aria/#home")
        await asyncio.sleep(0.5)
        v2_meta = await extract_active_page_metadata(page)
        assert v2_meta is None, f"v2-aria must not produce JSON-LD or meta tags! Got: {v2_meta}"
        
        state_v2 = await session.get_browser_state_summary()
        dom_v2 = state_v2.dom_state.llm_representation(include_attributes=OBSERVABLE_ATTRIBUTES)
        assert "aria-label=" in dom_v2, "v2-aria missing ARIA attributes in serialized DOM!"
        assert "data-field=" not in dom_v2, "v2-aria leaked data-field in DOM!"
        print("    ✓ v2-aria attribute serialization & isolation verified.")

        # ── Test Variant 3: v3-data-attrs ─────────────────────────────────────
        print("  Checking v3-data-attrs...")
        await page.goto(f"{BASE_URL}/variants/v3-data-attrs/#home")
        await asyncio.sleep(0.5)
        v3_meta = await extract_active_page_metadata(page)
        assert v3_meta is None, f"v3-data-attrs must not produce JSON-LD or meta tags! Got: {v3_meta}"
        
        state_v3 = await session.get_browser_state_summary()
        dom_v3 = state_v3.dom_state.llm_representation(include_attributes=OBSERVABLE_ATTRIBUTES)
        # Verify custom data-* on non-interactive span/div
        assert "data-field=" in dom_v3, "v3-data-attrs missing data-field in serialized DOM!"
        assert "data-category-slug=" in dom_v3, "v3-data-attrs missing data-category-slug in serialized DOM!"
        assert 'aria-label="Price:' not in dom_v3, "v3-data-attrs leaked ARIA in DOM!"
        print("    ✓ v3-data-attrs non-interactive element serialization verified.")

        # ── Test Variant 4: v4-evidence-meta ──────────────────────────────────
        print("  Checking v4-evidence-meta...")
        await page.goto(f"{BASE_URL}/variants/v4-evidence-meta/#home")
        for _ in range(20):
            has_cards = await page.evaluate('() => document.querySelectorAll(".product-card").length')
            if int(has_cards or 0) > 0:
                break
            await asyncio.sleep(0.1)

        v4_meta = await extract_active_page_metadata(page)
        assert v4_meta is not None, "v4-evidence-meta missing page metadata!"
        assert "[Page Metadata]" in v4_meta, "v4-evidence-meta missing [Page Metadata] section!"
        assert "last-updated: 2026-09-01T00:00:00Z" in v4_meta
        assert "data-freshness: live" in v4_meta
        assert "content-version: 1.0" in v4_meta
        assert "[Page Structured Data (JSON-LD)]" not in v4_meta, "v4 leaked JSON-LD!"
        
        # Verify temporal <time datetime="..."> in serialized DOM
        state_v4 = await session.get_browser_state_summary()
        dom_v4 = state_v4.dom_state.llm_representation(include_attributes=OBSERVABLE_ATTRIBUTES)
        assert "datetime=2026-09-01T00:00:00Z" in dom_v4 or 'datetime="2026-09-01T00:00:00Z"' in dom_v4, "v4-evidence-meta missing datetime in serialized DOM!"
        assert "data-field=" not in dom_v4, "v4-evidence-meta leaked data-field in DOM!"
        print("    ✓ v4-evidence-meta page metadata & temporal element verified.")

    finally:
        await session.stop()


def main():
    print("=" * 60)
    print("TechMart Offline Validation Suite — Phase 1 Observable")
    print("=" * 60)
    test_secret_sanitization()
    test_output_routing()
    asyncio.run(run_browser_tests())
    print("=" * 60)
    print("✓ ALL OFFLINE TESTS PASSED SUCCESSFULLY (0 LLM API calls)")
    print("=" * 60)


if __name__ == "__main__":
    main()

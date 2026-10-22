"""
TechMart Research Runner — Static & Live Variant Verifier
runner/verifier.py — Protocol v2

Implements all pre-flight checks defined in Protocol v2 §4.

Usage:
    # Static checks only (no browser required):
    python runner/verifier.py

    # Static + visual screenshot comparison (requires server at localhost:8080):
    python runner/verifier.py --visual

Exit codes:
    0 — all checks passed
    1 — one or more checks failed
"""

import sys
import re
import json
import copy
import argparse
import hashlib
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Comment
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("WARNING: beautifulsoup4 not installed. Run: pip install beautifulsoup4 lxml")

TESTING_DIR = Path("C:/testing")
# V4 (Evidence Meta) excluded from experiment: baseline cannot access temporal metadata visually.
VARIANTS = ["v0-baseline", "v1-jsonld", "v2-aria", "v3-data-attrs"]

# ── Attribute sets per feature type ────────────────────────────────────────
ARIA_ATTRS = frozenset({
    "role", "aria-label", "aria-labelledby", "aria-describedby",
    "aria-live", "aria-atomic", "aria-required", "aria-invalid",
    "aria-expanded", "aria-controls", "aria-hidden", "aria-checked",
    "aria-selected", "aria-disabled",
})

# V4-specific <meta> names (base charset/viewport metas are exempt)
V4_META_NAMES = frozenset({
    "last-updated", "data-freshness", "content-version",
    "product-price-as-of", "stock-status-as-of", "rating-as-of",
})

# Ground truth (must match shared/products.js)
GROUND_TRUTH = {
    "T1": {
        "cheapest_wh_sku": "wh-001",
        "cheapest_wh_price": 49.99,
        "wh_skus": {"wh-001", "wh-002", "wh-003"},
    },
    "T2": {"sku": "mkp-001", "name": "Mechanical Keyboard Pro"},
    "T3": {
        "eligible_skus": {"wh-001", "wh-002", "wh-003", "mkp-001", "mon-001", "acc-001"},
        "ineligible_skus": {"mse-001", "acc-002"},
    },
}

ALL_SKUS = {
    "wh-001": {"name": "SoundFlow Air 3",       "price": 49.99,  "rating": 4.2},
    "wh-002": {"name": "BudPro Wireless X",      "price": 89.99,  "rating": 4.5},
    "wh-003": {"name": "AudioMax BT50",          "price": 129.99, "rating": 4.8},
    "mkp-001": {"name": "Mechanical Keyboard Pro","price": 149.99, "rating": 4.7},
    "mse-001": {"name": "ErgoGlide Mouse",       "price": 59.99,  "rating": 3.8},
    "mon-001": {"name": "CrystalView 27",        "price": 299.99, "rating": 4.6},
    "acc-001": {"name": "USB-C Hub Pro",         "price": 39.99,  "rating": 4.1},
    "acc-002": {"name": "Desk Organizer Elite",  "price": 24.99,  "rating": 3.5},
}


# ══════════════════════════════════════════════════════════════════════════════
# HTML LOADING
# ══════════════════════════════════════════════════════════════════════════════

def load_html(variant: str) -> "BeautifulSoup":
    path = TESTING_DIR / "variants" / variant / "index.html"
    if not path.exists():
        raise FileNotFoundError(f"Variant file not found: {path}")
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 1: FILE EXISTENCE
# ══════════════════════════════════════════════════════════════════════════════

def check_file_existence() -> list[str]:
    errors = []
    required_files = [
        "index.html",
        "shared/styles.css",
        "shared/products.js",
        "shared/app-core.js",
        "tasks/task-definitions.json",
        "runner/verifier.py",
        "runner/logger.py",
        "runner/agent-runner.py",
        "runner/requirements.txt",
    ]
    for vn in VARIANTS:
        required_files.append(f"variants/{vn}/index.html")

    for f in required_files:
        p = TESTING_DIR / f
        if not p.exists():
            errors.append(f"Missing required file: {f}")
    return errors


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 2: SHARED CSS/JS IMPORTS
# ══════════════════════════════════════════════════════════════════════════════

def check_shared_imports(variant: str, soup: "BeautifulSoup") -> list[str]:
    errors = []

    # CSS link
    css = soup.find("link", rel="stylesheet", href="../../shared/styles.css")
    if not css:
        errors.append(f"[{variant}] Missing <link href='../../shared/styles.css'>")

    # Inline <style> tags (forbidden)
    styles = [s for s in soup.find_all("style") if s.get_text(strip=True)]
    if styles:
        errors.append(f"[{variant}] Found {len(styles)} inline <style> tag(s) (forbidden)")

    # products.js
    prod = soup.find("script", src="../../shared/products.js")
    if not prod:
        errors.append(f"[{variant}] Missing <script src='../../shared/products.js'>")

    # app-core.js
    core = soup.find("script", src="../../shared/app-core.js")
    if not core:
        errors.append(f"[{variant}] Missing <script src='../../shared/app-core.js'>")

    # Verify script order: products.js BEFORE app-core.js
    scripts = soup.find_all("script", src=True)
    srcs = [s["src"] for s in scripts]
    if "../../shared/products.js" in srcs and "../../shared/app-core.js" in srcs:
        pi = srcs.index("../../shared/products.js")
        ai = srcs.index("../../shared/app-core.js")
        if pi > ai:
            errors.append(f"[{variant}] products.js must come before app-core.js")

    return errors


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 3: CROSS-CONTAMINATION
# ══════════════════════════════════════════════════════════════════════════════

def check_cross_contamination(variant: str, soup: "BeautifulSoup") -> list[str]:
    errors = []

    has_jsonld = bool(soup.find("script", type="application/ld+json"))
    has_aria = any(
        any(k in ARIA_ATTRS for k in tag.attrs)
        for tag in soup.find_all()
    )
    has_dataattrs = any(
        any(k.startswith("data-") for k in tag.attrs)
        for tag in soup.find_all()
    )
    has_temporal_meta = any(
        m.get("name", "") in V4_META_NAMES
        for m in soup.find_all("meta")
    )

    expected = {
        "v0-baseline":     {"jsonld": False, "aria": False, "data": False, "temporal": False},
        "v1-jsonld":       {"jsonld": True,  "aria": False, "data": False, "temporal": False},
        "v2-aria":         {"jsonld": False, "aria": True,  "data": False, "temporal": False},
        "v3-data-attrs":   {"jsonld": False, "aria": False, "data": True,  "temporal": False},
        "v4-evidence-meta":{"jsonld": False, "aria": False, "data": False, "temporal": True},
    }[variant]

    if expected["jsonld"] and not has_jsonld:
        errors.append(f"[{variant}] Missing JSON-LD (expected for this variant)")
    if not expected["jsonld"] and has_jsonld:
        errors.append(f"[{variant}] CONTAMINATION: has JSON-LD (forbidden)")

    if expected["aria"] and not has_aria:
        errors.append(f"[{variant}] Missing ARIA attributes (expected for this variant)")
    if not expected["aria"] and has_aria:
        errors.append(f"[{variant}] CONTAMINATION: has ARIA attributes (forbidden)")

    if expected["data"] and not has_dataattrs:
        errors.append(f"[{variant}] Missing data-* attributes (expected for this variant)")
    if not expected["data"] and has_dataattrs:
        errors.append(f"[{variant}] CONTAMINATION: has data-* attributes (forbidden)")

    if expected["temporal"] and not has_temporal_meta:
        errors.append(f"[{variant}] Missing temporal <meta> tags (expected for this variant)")
    if not expected["temporal"] and has_temporal_meta:
        errors.append(f"[{variant}] CONTAMINATION: has temporal <meta> tags (forbidden)")

    # V4-specific: static HTML must NOT have <time class="temporal-meta"> (added by JS only)
    if variant == "v4-evidence-meta":
        static_time = soup.find("time", class_="temporal-meta")
        if static_time:
            errors.append(f"[{variant}] DESIGN VIOLATION: <time class='temporal-meta'> found in "
                          f"static HTML — must only be added by app-core.js at runtime")

    # V3-specific: body should have data-page attribute
    if variant == "v3-data-attrs":
        body = soup.find("body")
        if body and "data-page" not in body.attrs:
            errors.append(f"[{variant}] Missing data-page attribute on <body>")

    return errors


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 4: VISIBLE TEXT PARITY (static HTML, body only, no script/style)
# ══════════════════════════════════════════════════════════════════════════════

def extract_visible_text(soup: "BeautifulSoup") -> str:
    """Extract body text, excluding script/style content."""
    body = soup.find("body")
    if not body:
        return ""
    body_copy = copy.copy(body)
    for tag in body_copy.find_all(["script", "style"]):
        tag.decompose()
    for comment in body_copy.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()
    return re.sub(r"\s+", " ", body_copy.get_text(separator=" ")).strip()


def check_visible_text_parity(soups: dict) -> list[str]:
    errors = []
    texts = {v: extract_visible_text(soups[v]) for v in VARIANTS}
    baseline = texts["v0-baseline"]
    for variant in VARIANTS:
        if variant == "v0-baseline":
            continue
        if texts[variant] != baseline:
            # Find first differing character
            t = texts[variant]
            diff_pos = next(
                (i for i in range(min(len(baseline), len(t))) if baseline[i] != t[i]),
                min(len(baseline), len(t))
            )
            ctx = texts[variant][max(0, diff_pos - 40): diff_pos + 40]
            errors.append(
                f"[{variant}] Visible text differs from v0-baseline near pos {diff_pos}: ...{ctx!r}..."
            )
    return errors


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 5: CANONICAL DOM PARITY (strip experimental features, compare)
# ══════════════════════════════════════════════════════════════════════════════

def strip_experimental_features(soup: "BeautifulSoup") -> str:
    """Remove all experimental attributes/elements; return normalized HTML string."""
    s = copy.copy(soup)

    # Remove JSON-LD scripts
    for tag in s.find_all("script", type="application/ld+json"):
        tag.decompose()
    for tag in s.find_all("script", id="dynamic-jsonld"):
        tag.decompose()

    # Remove ARIA attributes
    for tag in s.find_all():
        for attr in list(ARIA_ATTRS):
            tag.attrs.pop(attr, None)

    # Remove data-* attributes
    for tag in s.find_all():
        for k in list(tag.attrs.keys()):
            if k.startswith("data-"):
                del tag.attrs[k]

    # Remove V4 temporal <meta> tags
    for meta in s.find_all("meta"):
        if meta.get("name", "") in V4_META_NAMES:
            meta.decompose()

    # Remove V4 <time class="temporal-meta"> elements (if injected dynamically)
    for t in s.find_all("time", class_="temporal-meta"):
        t.decompose()


    # Normalize the variant config script (variant name differs per file)
    for script in s.find_all("script"):
        if script.string and "__VARIANT_CONFIG__" in script.string:
            script.string = "/* VARIANT_CONFIG_NORMALIZED */"

    # Strip ALL HTML comments (variant-specific comment text causes false parity failures)
    for comment in s.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()

    # Normalize: collapse whitespace, sort attributes for stable comparison
    for tag in s.find_all():
        if tag.attrs:
            tag.attrs = dict(sorted(tag.attrs.items()))

    raw = str(s)
    return re.sub(r"\s+", " ", raw).strip()



def check_canonical_dom_parity(soups: dict) -> list[str]:
    errors = []
    canonical = {v: strip_experimental_features(soups[v]) for v in VARIANTS}
    baseline = canonical["v0-baseline"]
    for variant in VARIANTS:
        if variant == "v0-baseline":
            continue
        if canonical[variant] != baseline:
            # Hash comparison for concise reporting
            bh = hashlib.sha256(baseline.encode()).hexdigest()[:8]
            vh = hashlib.sha256(canonical[variant].encode()).hexdigest()[:8]
            errors.append(
                f"[{variant}] Canonical DOM differs from v0-baseline "
                f"(baseline sha256[:8]={bh}, variant={vh}). "
                f"Unexpected structural difference after stripping all experimental features."
            )
    return errors


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 6: TASK DEFINITIONS INTEGRITY
# ══════════════════════════════════════════════════════════════════════════════

def check_task_definitions() -> list[str]:
    errors = []
    path = TESTING_DIR / "tasks" / "task-definitions.json"
    if not path.exists():
        return ["tasks/task-definitions.json not found"]
    try:
        tasks = json.loads(path.read_text(encoding="utf-8"))["tasks"]
    except Exception as e:
        return [f"tasks/task-definitions.json parse error: {e}"]

    task_ids = {t["id"] for t in tasks}
    for expected_id in ["T1", "T2", "T3", "T4", "T5"]:
        if expected_id not in task_ids:
            errors.append(f"Task {expected_id} missing from task-definitions.json")

    for task in tasks:
        if "instruction" not in task:
            errors.append(f"Task {task.get('id')} missing 'instruction' field")
        if "success_criterion" not in task:
            errors.append(f"Task {task.get('id')} missing 'success_criterion' field")
        sc = task.get("success_criterion", {})
        if "js_check" not in sc:
            errors.append(f"Task {task.get('id')} success_criterion missing 'js_check'")

    # Ground truth integrity
    t1 = next((t for t in tasks if t["id"] == "T1"), None)
    if t1:
        gt = t1.get("ground_truth", {})
        if gt.get("cheapest_sku") != "wh-001":
            errors.append("T1 ground_truth.cheapest_sku must be 'wh-001'")
        if gt.get("cheapest_price") != 49.99:
            errors.append("T1 ground_truth.cheapest_price must be 49.99")

    t2 = next((t for t in tasks if t["id"] == "T2"), None)
    if t2:
        gt = t2.get("ground_truth", {})
        if gt.get("sku") != "mkp-001":
            errors.append("T2 ground_truth.sku must be 'mkp-001'")

    # Verify T1 js_check does NOT use data-product-id (Protocol v2 §4, R4)
    if t1:
        js = t1["success_criterion"].get("js_check", "")
        if "data-product-id" in js or "getAttribute" in js:
            errors.append("T1 js_check must not use data-product-id (Protocol v2 §4 R4)")

    return errors


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 7: VERIFIER SELF-TEST (known correct/incorrect states)
# ══════════════════════════════════════════════════════════════════════════════

def verify_cart_state(cart: list, task_id: str) -> dict:
    """
    Ground-truth verifier for post-run cart/order state.
    Used by agent-runner.py after each run.
    Returns: {"success": bool, "partial_score": float, "details": dict}
    """
    if task_id == "T1":
        has_correct = any(i["sku"] == "wh-001" for i in cart)
        cart_nonempty = len(cart) > 0
        score = (0.25 if cart_nonempty else 0) + (0.5 if has_correct else 0)
        if has_correct:
            score += 0.25  # search_performed implied
        return {
            "success": has_correct,
            "partial_score": min(score, 1.0),
            "details": {
                "cart_nonempty": cart_nonempty,
                "correct_item_added": has_correct,
                "cart_skus": [i["sku"] for i in cart],
            },
        }

    elif task_id == "T2":
        has_mkp = any(i["sku"] == "mkp-001" for i in cart)
        return {
            "success": has_mkp,
            "partial_score": 1.0 if has_mkp else 0.0,
            "details": {"mkp_001_in_cart": has_mkp},
        }

    elif task_id == "T3":
        eligible = {"wh-001", "wh-002", "wh-003", "mkp-001", "mon-001", "acc-001"}
        has_eligible = any(i["sku"] in eligible for i in cart)
        has_ineligible = any(i["sku"] not in eligible for i in cart)
        cart_nonempty = len(cart) > 0
        
        # Success requires at least one eligible item AND zero ineligible items.
        success = has_eligible and not has_ineligible
        
        # Scoring logic:
        # +0.5 for adding any item (cart non-empty)
        # +0.5 for adding an eligible item
        # PENALTY: 0.0 total score if an ineligible item is present (prevents guessing/spamming cart)
        score = 0.0
        if cart_nonempty:
            score += 0.5
        if has_eligible:
            score += 0.5
        if has_ineligible:
            score = 0.0
            
        return {
            "success": success,
            "partial_score": score,
            "details": {
                "cart_nonempty": cart_nonempty,
                "has_eligible": has_eligible,
                "has_ineligible": has_ineligible,
                "cart_skus": [i["sku"] for i in cart],
            },
        }

    elif task_id == "T4":
        # Handled by separate order_confirmed flag
        return {
            "success": False,
            "partial_score": 0.0,
            "details": {"note": "T4 success determined by order_confirmed flag"},
        }

    elif task_id == "T5":
        is_empty = len(cart) == 0
        return {
            "success": is_empty,
            "partial_score": 1.0 if is_empty else 0.0,
            "details": {"cart_empty": is_empty, "remaining_items": len(cart)},
        }

    return {"success": False, "partial_score": 0.0, "details": {"error": "unknown task"}}


def verify_order_state(order_confirmed: bool, task_id: str, cart: list, last_order_items: list = None) -> dict:
    """Verifier for T4 order confirmation."""
    if task_id != "T4":
        return {"success": False, "partial_score": 0.0, "details": {}}
        
    last_order_items = last_order_items or []

    cart_ok = len(cart) == 0  # cart cleared after successful checkout
    has_mouse = any(i["sku"] == "mse-001" for i in last_order_items)
    
    score = 0.0
    score += 0.25  # checkout reached
    if order_confirmed:
        score += 0.25
    if has_mouse:
        score += 0.50

    success = order_confirmed and has_mouse

    return {
        "success": success,
        "partial_score": min(score, 1.0),
        "details": {
            "order_confirmed": order_confirmed,
            "has_mouse_in_order": has_mouse,
            "cart_cleared": cart_ok,
            "ordered_skus": [i["sku"] for i in last_order_items]
        },
    }


def run_verifier_self_test() -> list[str]:
    """Test verify_cart_state against known correct and incorrect states."""
    failures = []

    # T1: correct case
    r = verify_cart_state([{"sku": "wh-001", "quantity": 1, "price": 49.99}], "T1")
    if not r["success"] or r["partial_score"] < 1.0:
        failures.append("T1 self-test FAIL: should succeed with wh-001 in cart")

    # T1: wrong item (most expensive)
    r = verify_cart_state([{"sku": "wh-003", "quantity": 1, "price": 129.99}], "T1")
    if r["success"]:
        failures.append("T1 self-test FAIL: wh-003 should NOT satisfy T1")
    if r["partial_score"] > 0.5:
        failures.append(f"T1 self-test FAIL: wrong partial score {r['partial_score']} for wh-003")

    # T1: empty cart
    r = verify_cart_state([], "T1")
    if r["success"] or r["partial_score"] != 0.0:
        failures.append("T1 self-test FAIL: empty cart should score 0.0")

    # T2: correct
    r = verify_cart_state([{"sku": "mkp-001", "quantity": 1, "price": 149.99}], "T2")
    if not r["success"]:
        failures.append("T2 self-test FAIL: mkp-001 should succeed")

    # T2: wrong item
    r = verify_cart_state([{"sku": "wh-001", "quantity": 1, "price": 49.99}], "T2")
    if r["success"]:
        failures.append("T2 self-test FAIL: wh-001 should NOT satisfy T2")

    # T3: eligible item only (rating 4.5)
    r = verify_cart_state([{"sku": "wh-002", "quantity": 1, "price": 89.99}], "T3")
    if not r["success"] or r["partial_score"] != 1.0:
        failures.append("T3 self-test FAIL: wh-002 (4.5 stars) should satisfy T3 with score 1.0")

    # T3: ineligible item only (rating 3.5)
    r = verify_cart_state([{"sku": "acc-002", "quantity": 1, "price": 24.99}], "T3")
    if r["success"] or r["partial_score"] != 0.0:
        failures.append("T3 self-test FAIL: acc-002 (3.5 stars) should fail T3 with score 0.0")
        
    # T3: eligible PLUS ineligible item
    r = verify_cart_state([{"sku": "wh-002"}, {"sku": "acc-002"}], "T3")
    if r["success"] or r["partial_score"] != 0.0:
        failures.append("T3 self-test FAIL: mixed items should fail T3 with score 0.0")

    # T3: empty cart
    r = verify_cart_state([], "T3")
    if r["success"] or r["partial_score"] != 0.0:
        failures.append("T3 self-test FAIL: empty cart should fail T3 with score 0.0")

    # T4: confirmed with correct item
    r = verify_order_state(True, "T4", [], [{"sku": "mse-001"}])
    if not r["success"] or r["partial_score"] < 1.0:
        failures.append("T4 self-test FAIL: order_confirmed=True with mse-001 should succeed")

    # T4: confirmed with WRONG item
    r = verify_order_state(True, "T4", [], [{"sku": "wh-001"}])
    if r["success"]:
        failures.append("T4 self-test FAIL: order_confirmed=True with wrong item should NOT succeed")

    # T4: not confirmed
    r = verify_order_state(False, "T4", [{"sku": "mse-001"}], [])
    if r["success"]:
        failures.append("T4 self-test FAIL: order_confirmed=False should not succeed")

    # T5: empty cart
    r = verify_cart_state([], "T5")
    if not r["success"]:
        failures.append("T5 self-test FAIL: empty cart should succeed")

    # T5: non-empty cart
    r = verify_cart_state([{"sku": "wh-001", "quantity": 1}], "T5")
    if r["success"]:
        failures.append("T5 self-test FAIL: non-empty cart should not succeed")

    return failures


# ══════════════════════════════════════════════════════════════════════════════
# CHECK 8: VISUAL VERIFICATION (requires Playwright + running server)
# ══════════════════════════════════════════════════════════════════════════════

def run_visual_verification(base_url: str = "http://localhost:8080") -> list[str]:
    """
    Take screenshots of all 5 variants and pixel-diff them against v0-baseline.
    Requires: playwright install chromium
    """
    errors = []
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image, ImageChops
        import io
    except ImportError as e:
        return [f"Visual verification requires playwright and pillow: {e}"]

    screenshots_dir = TESTING_DIR / "results" / "visual-verification"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    print("\n  Starting headless browser for visual verification...")
    with sync_playwright() as p:
        browser = None
        for channel in [None, "chrome", "msedge"]:
            try:
                browser = p.chromium.launch(headless=True, channel=channel) if channel else p.chromium.launch(headless=True)
                break
            except Exception:
                continue
        if browser is None:
            return ["Could not launch any browser (chromium, chrome, or msedge)."]
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        baseline_img = None
        for variant in VARIANTS:
            url = f"{base_url}/variants/{variant}/"
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(1500)  # let JS render products

                shot_bytes = page.screenshot(full_page=True)
                shot_path = screenshots_dir / f"{variant}.png"
                shot_path.write_bytes(shot_bytes)
                print(f"  Screenshot saved: {shot_path.name}")

                img = Image.open(io.BytesIO(shot_bytes)).convert("RGB")

                if variant == "v0-baseline":
                    baseline_img = img
                else:
                    if baseline_img is not None:
                        if img.size != baseline_img.size:
                            errors.append(
                                f"[{variant}] Screenshot size differs from v0-baseline: "
                                f"{img.size} vs {baseline_img.size}"
                            )
                        else:
                            diff = ImageChops.difference(img, baseline_img)
                            diff_data = list(diff.getdata())
                            nonzero = sum(1 for px in diff_data if any(c > 0 for c in px))
                            if nonzero > 0:
                                diff_path = screenshots_dir / f"diff_{variant}.png"
                                diff.save(str(diff_path))
                                errors.append(
                                    f"[{variant}] VISUAL DIFF: {nonzero} pixels differ from "
                                    f"v0-baseline. Diff saved: {diff_path.name}"
                                )
                            else:
                                print(f"  ✓ {variant}: zero pixel difference vs v0-baseline")

            except Exception as e:
                errors.append(f"[{variant}] Screenshot failed: {e}")

        browser.close()

    return errors


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="TechMart pre-flight verifier")
    parser.add_argument("--visual", action="store_true",
                        help="Run visual pixel-diff verification (requires server at localhost:8080)")
    parser.add_argument("--base-url", default="http://localhost:8080",
                        help="Base URL for visual verification")
    args = parser.parse_args()

    if not BS4_AVAILABLE:
        print("ERROR: beautifulsoup4 required. Install: pip install beautifulsoup4 lxml")
        sys.exit(1)

    all_passed = True
    total_checks = 0
    total_failures = 0

    def section(title):
        print(f"\n{'─' * 60}")
        print(f"  {title}")
        print(f"{'─' * 60}")

    def report(errors, check_name):
        nonlocal all_passed, total_checks, total_failures
        total_checks += 1
        if errors:
            all_passed = False
            total_failures += 1
            for e in errors:
                print(f"  ✗ {e}")
        else:
            print(f"  ✓ {check_name}: PASSED")

    print("=" * 60)
    print("  TechMart — Pre-flight Static Verification")
    print("  Protocol v2 §4")
    print("=" * 60)

    # ── Load all HTML files ──────────────────────────────────────────────────
    soups = {}
    load_errors = []
    for vn in VARIANTS:
        try:
            soups[vn] = load_html(vn)
        except FileNotFoundError as e:
            load_errors.append(str(e))

    # ── Check 1: File existence ──────────────────────────────────────────────
    section("Check 1: Required file existence")
    report(check_file_existence(), "File existence")
    if load_errors:
        for e in load_errors:
            print(f"  ✗ {e}")
        print("\n  Cannot continue without all variant HTML files.")
        sys.exit(1)

    # ── Check 2: Shared CSS/JS imports ──────────────────────────────────────
    section("Check 2: Shared CSS/JS imports")
    import_errors = []
    for vn in VARIANTS:
        import_errors.extend(check_shared_imports(vn, soups[vn]))
    report(import_errors, "Shared imports")

    # ── Check 3: Cross-contamination ────────────────────────────────────────
    section("Check 3: Feature isolation / cross-contamination")
    contam_errors = []
    for vn in VARIANTS:
        errs = check_cross_contamination(vn, soups[vn])
        contam_errors.extend(errs)
    report(contam_errors, "Feature isolation")

    # ── Check 4: Visible text parity ────────────────────────────────────────
    section("Check 4: Visible text parity (static HTML, body only)")
    report(check_visible_text_parity(soups), "Visible text parity")

    # ── Check 5: Canonical DOM parity ───────────────────────────────────────
    section("Check 5: Canonical DOM parity (after stripping experimental features)")
    report(check_canonical_dom_parity(soups), "Canonical DOM parity")

    # ── Check 6: Task definitions ───────────────────────────────────────────
    section("Check 6: Task definitions integrity")
    report(check_task_definitions(), "Task definitions")

    # ── Check 7: Verifier self-test ─────────────────────────────────────────
    section("Check 7: Verifier self-test (known correct/incorrect states)")
    report(run_verifier_self_test(), "Verifier self-test")

    # ── Check 8: Visual verification (optional) ─────────────────────────────
    if args.visual:
        section("Check 8: Visual pixel-diff verification")
        report(run_visual_verification(args.base_url), "Visual verification")

    # ── Final summary ────────────────────────────────────────────────────────
    print(f"\n{'═' * 60}")
    if all_passed:
        print(f"  ✓ ALL {total_checks} CHECKS PASSED — Infrastructure ready")
        print(f"  Pilot run may proceed after model selection.")
    else:
        print(f"  ✗ {total_failures}/{total_checks} CHECK GROUPS FAILED")
        print(f"  Fix all issues before running the experiment.")
        sys.exit(1)
    print("═" * 60)


if __name__ == "__main__":
    main()

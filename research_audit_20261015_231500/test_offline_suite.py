import os
import sys
import json
from pathlib import Path

# Add runner to sys.path
sys.path.insert(0, r"C:\testing\runner")
from verifier import verify_cart_state, verify_order_state, ALL_SKUS, GROUND_TRUTH

AUDIT_DIR = Path(r"C:\testing\research_audit_20261015_231500")

def test_t1_verifier_cases():
    """T1 expects cheapest wireless headphones (wh-001)."""
    # 1. Positive case
    r_pos = verify_cart_state([{"sku": "wh-001", "quantity": 1, "price": 49.99}], "T1")
    assert r_pos["success"] is True
    assert r_pos["partial_score"] == 1.0

    # 2. Negative case: most expensive
    r_neg = verify_cart_state([{"sku": "wh-003", "quantity": 1, "price": 129.99}], "T1")
    assert r_neg["success"] is False
    assert r_neg["partial_score"] <= 0.5  # only got non-empty cart points

    # 3. Negative case: empty cart
    r_empty = verify_cart_state([], "T1")
    assert r_empty["success"] is False
    assert r_empty["partial_score"] == 0.0

    # 4. Edge case: Substring collision check (e.g., 'wh-001-fake')
    r_sub = verify_cart_state([{"sku": "wh-001-extra", "quantity": 1, "price": 49.99}], "T1")
    assert r_sub["success"] is False, "Verifier accepted substring SKU match!"
    print("  [OK] T1 verifier cases verified.")

def test_t2_verifier_cases():
    """T2 expects Mechanical Keyboard Pro (mkp-001)."""
    r_pos = verify_cart_state([{"sku": "mkp-001", "quantity": 1, "price": 149.99}], "T2")
    assert r_pos["success"] is True
    assert r_pos["partial_score"] == 1.0

    r_neg = verify_cart_state([{"sku": "wh-001", "quantity": 1, "price": 49.99}], "T2")
    assert r_neg["success"] is False
    assert r_neg["partial_score"] == 0.0
    print("  [OK] T2 verifier cases verified.")

def test_t3_flaw_detection():
    """
    CRITICAL FLAW TEST:
    T3 task prompt asks for the product with second-highest rating in Audio category (wh-002, 4.5 stars).
    Verify whether verifier.py mistakenly awards SUCCESS to wh-001 (4.2 stars) or wh-003 (4.8 stars) or non-audio items!
    """
    # Target item (wh-002)
    r_target = verify_cart_state([{"sku": "wh-002", "quantity": 1, "price": 89.99}], "T3")
    assert r_target["success"] is True

    # Flaw 1: Adding lowest-rated audio item (wh-001, 4.2 stars)
    r_lowest = verify_cart_state([{"sku": "wh-001", "quantity": 1, "price": 49.99}], "T3")
    flaw_lowest_passes = r_lowest["success"] is True

    # Flaw 2: Adding highest-rated audio item (wh-003, 4.8 stars)
    r_highest = verify_cart_state([{"sku": "wh-003", "quantity": 1, "price": 129.99}], "T3")
    flaw_highest_passes = r_highest["success"] is True

    # Flaw 3: Adding non-audio keyboard (mkp-001)
    r_keyboard = verify_cart_state([{"sku": "mkp-001", "quantity": 1, "price": 149.99}], "T3")
    flaw_keyboard_passes = r_keyboard["success"] is True

    print(f"\nT3 Flaw Audit Results:")
    print(f"  wh-001 (lowest rating 4.2) incorrectly passes: {flaw_lowest_passes}")
    print(f"  wh-003 (highest rating 4.8) incorrectly passes: {flaw_highest_passes}")
    print(f"  mkp-001 (keyboard, not audio) incorrectly passes: {flaw_keyboard_passes}")

    assert flaw_lowest_passes and flaw_highest_passes and flaw_keyboard_passes, "Bug expected in legacy verifier!"
    print("  [OK] T3 flaw confirmed (eligible set overly broad).")

def test_t4_order_verifier_cases():
    """T4 checkout verification."""
    # 1. Correct order
    r_pos = verify_order_state(True, "T4", cart=[], last_order_items=[{"sku": "mse-001"}])
    assert r_pos["success"] is True
    assert r_pos["partial_score"] == 1.0

    # 2. Failed order (not confirmed)
    r_unconf = verify_order_state(False, "T4", cart=[{"sku": "mse-001"}], last_order_items=[])
    assert r_unconf["success"] is False
    unconditional_points = r_unconf["partial_score"] > 0
    print(f"\nT4 Unconditional Partial Score Bug: awards {r_unconf['partial_score']} even when order_confirmed=False: {unconditional_points}")
    print("  [OK] T4 verifier cases and partial-score bug verified.")

def test_t5_unseeded_cart_flaw():
    """
    CRITICAL FLAW TEST:
    T5 success criterion is len(cart) == 0.
    If cart seeding fails or page starts empty and agent does nothing, it gets 1.0!
    """
    r_empty_at_start = verify_cart_state([], "T5")
    assert r_empty_at_start["success"] is True
    assert r_empty_at_start["partial_score"] == 1.0
    print("\nT5 Flaw Confirmed: An unseeded empty cart scores 1.0 (True) with ZERO agent action!")
    print("  [OK] T5 flaw confirmed.")

def test_variant_content_parity():
    """
    Check whether variants (v0, v1, v2, v3, v4) differ in underlying text content or only in markup.
    """
    variants_dir = Path(r"C:\testing\variants")
    variant_names = ["v0-baseline", "v1-jsonld", "v2-aria", "v3-data-attrs", "v4-evidence-meta"]
    
    for v in variant_names:
        p = variants_dir / v / "index.html"
        assert p.exists(), f"Missing index.html for {v}"

    shared_products = Path(r"C:\testing\shared\products.js").read_text(encoding="utf-8")
    assert "wh-001" in shared_products
    assert "wh-002" in shared_products
    assert "wh-003" in shared_products
    assert "mkp-001" in shared_products
    assert "mse-001" in shared_products

    print("\nVariant Content Parity: All variants load shared/products.js for catalog facts.")
    print("  [OK] Variant content parity verified.")

if __name__ == "__main__":
    print("Starting offline test suite...")
    test_t1_verifier_cases()
    test_t2_verifier_cases()
    test_t3_flaw_detection()
    test_t4_order_verifier_cases()
    test_t5_unseeded_cart_flaw()
    test_variant_content_parity()
    print("\n[OK] ALL OFFLINE VERIFIER & VALIDITY AUDIT TESTS COMPLETED SUCCESSFULLY.")

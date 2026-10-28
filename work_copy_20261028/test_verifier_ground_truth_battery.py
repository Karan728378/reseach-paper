"""
Automated Verifier Known-Pass / Known-Fail Battery
Exhaustively asserts ground-truth correctness for all task verifiers (T1-T6)
under both valid positive executions and realistic negative adversarial failures.
Part of the Empirical Verification Infrastructure.
"""

import unittest
import sys
from pathlib import Path

RESEARCH_DIR = Path("C:/testing/research_execution_20261018")
sys.path.insert(0, str(RESEARCH_DIR))

import protocol_v3_runner

class TestVerifierGroundTruthBattery(unittest.TestCase):

    # ── Task T1: Cheapest Wireless Headphones (wh-001) ───────────────────────
    def test_t1_known_passes(self):
        """T1 must pass when cart contains exactly wh-001 ($49.99, lowest price)."""
        res = protocol_v3_runner.verify_task_result("T1", cart=[{"sku": "wh-001", "name": "SoundFlow Air 3"}], order_confirmed=False, last_order_items=[])
        self.assertTrue(res["success"])
        self.assertEqual(res["score"], 1.0)

    def test_t1_known_fails(self):
        """T1 must fail on higher-priced headphones, wrong categories, or empty cart."""
        # wh-002 is $79.99
        res1 = protocol_v3_runner.verify_task_result("T1", cart=[{"sku": "wh-002", "name": "BudPro Wireless X"}], order_confirmed=False, last_order_items=[])
        self.assertFalse(res1["success"])
        self.assertEqual(res1["score"], 0.0)

        # wh-003 is $99.99
        res2 = protocol_v3_runner.verify_task_result("T1", cart=[{"sku": "wh-003", "name": "NoiseShield Max"}], order_confirmed=False, last_order_items=[])
        self.assertFalse(res2["success"])

        # Empty cart
        res3 = protocol_v3_runner.verify_task_result("T1", cart=[], order_confirmed=False, last_order_items=[])
        self.assertFalse(res3["success"])

        # Cart with wrong category
        res4 = protocol_v3_runner.verify_task_result("T1", cart=[{"sku": "mkp-001"}], order_confirmed=False, last_order_items=[])
        self.assertFalse(res4["success"])

    # ── Task T2: Specific Mechanical Keyboard (mkp-001) ──────────────────────
    def test_t2_known_passes(self):
        """T2 must pass when cart contains mkp-001 (ProClick Tactile Pro)."""
        res = protocol_v3_runner.verify_task_result("T2", cart=[{"sku": "mkp-001", "name": "ProClick Tactile Pro"}], order_confirmed=False, last_order_items=[])
        self.assertTrue(res["success"])
        self.assertEqual(res["score"], 1.0)

    def test_t2_known_fails(self):
        """T2 must fail on wrong keyboard (mkp-002) or empty cart."""
        res1 = protocol_v3_runner.verify_task_result("T2", cart=[{"sku": "mkp-002"}], order_confirmed=False, last_order_items=[])
        self.assertFalse(res1["success"])
        self.assertEqual(res1["score"], 0.0)

        res2 = protocol_v3_runner.verify_task_result("T2", cart=[], order_confirmed=False, last_order_items=[])
        self.assertFalse(res2["success"])

    # ── Task T3: Second-Highest Rated Audio Product (wh-002, 4.5 Stars) ──────
    def test_t3_known_passes(self):
        """T3 must pass ONLY for wh-002 (second-highest rating 4.5 vs highest wh-001 4.8)."""
        res = protocol_v3_runner.verify_task_result("T3", cart=[{"sku": "wh-002", "name": "BudPro Wireless X"}], order_confirmed=False, last_order_items=[])
        self.assertTrue(res["success"])
        self.assertEqual(res["score"], 1.0)

    def test_t3_known_fails(self):
        """T3 must strictly reject the highest-rated product (wh-001) and other audio products."""
        # wh-001 is highest rated (4.8), not second-highest
        res_highest = protocol_v3_runner.verify_task_result("T3", cart=[{"sku": "wh-001"}], order_confirmed=False, last_order_items=[])
        self.assertFalse(res_highest["success"])
        self.assertEqual(res_highest["score"], 0.0)

        # wh-003 is third-highest (4.2)
        res_third = protocol_v3_runner.verify_task_result("T3", cart=[{"sku": "wh-003"}], order_confirmed=False, last_order_items=[])
        self.assertFalse(res_third["success"])

        # Multiple items in cart
        res_multi = protocol_v3_runner.verify_task_result("T3", cart=[{"sku": "wh-001"}, {"sku": "wh-002"}], order_confirmed=False, last_order_items=[])
        self.assertFalse(res_multi["success"])

    # ── Task T4: Complete Mouse Checkout (mse-001) ───────────────────────────
    def test_t4_known_passes(self):
        """T4 must pass when order is confirmed and last_order_items contains mse-001."""
        res = protocol_v3_runner.verify_task_result(
            "T4",
            cart=[],
            order_confirmed=True,
            last_order_items=[{"sku": "mse-001", "name": "GlideMaster Wireless"}]
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["score"], 1.0)

    def test_t4_known_fails(self):
        """T4 must fail if checkout was unconfirmed or confirmed with wrong item."""
        # Unconfirmed checkout (must score 0.0, eliminating historical 0.25 bug)
        res_unconfirmed = protocol_v3_runner.verify_task_result(
            "T4",
            cart=[{"sku": "mse-001"}],
            order_confirmed=False,
            last_order_items=[]
        )
        self.assertFalse(res_unconfirmed["success"])
        self.assertEqual(res_unconfirmed["score"], 0.0)

        # Confirmed order with wrong item
        res_wrong_item = protocol_v3_runner.verify_task_result(
            "T4",
            cart=[],
            order_confirmed=True,
            last_order_items=[{"sku": "mse-002"}]
        )
        self.assertFalse(res_wrong_item["success"])
        self.assertEqual(res_wrong_item["score"], 0.0)

    # ── Task T5: Remove Preseeded Cart Item ──────────────────────────────────
    def test_t5_known_passes(self):
        """T5 must pass when pre_cart_count == 1 and final cart == []."""
        res = protocol_v3_runner.verify_task_result(
            "T5",
            cart=[],
            order_confirmed=False,
            last_order_items=[],
            pre_cart_count=1
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["score"], 1.0)

    def test_t5_known_fails(self):
        """T5 must fail if pre_cart_count was 0 (unseeded) or final cart still has items."""
        # Unseeded initial state (historical bug where empty cart passed without pre-seeding)
        res_unseeded = protocol_v3_runner.verify_task_result(
            "T5",
            cart=[],
            order_confirmed=False,
            last_order_items=[],
            pre_cart_count=0
        )
        self.assertFalse(res_unseeded["success"])
        self.assertEqual(res_unseeded["score"], 0.0)

        # Missing pre_cart_count (None)
        res_none = protocol_v3_runner.verify_task_result(
            "T5",
            cart=[],
            order_confirmed=False,
            last_order_items=[],
            pre_cart_count=None
        )
        self.assertFalse(res_none["success"])

        # Failed removal (item still in cart)
        res_not_removed = protocol_v3_runner.verify_task_result(
            "T5",
            cart=[{"sku": "wh-001"}],
            order_confirmed=False,
            last_order_items=[],
            pre_cart_count=1
        )
        self.assertFalse(res_not_removed["success"])
        self.assertEqual(res_not_removed["score"], 0.0)

    # ── Task T6: Grounded Refusal on Absent Warranty Duration ─────────────────
    def test_t6_known_passes(self):
        """T6 must pass when agent correctly refuses to provide an unstated warranty duration."""
        valid_refusals = [
            "The warranty duration is not specified in the product description.",
            "I cannot determine the warranty period because it is not stated.",
            "There is no information provided about how long the warranty lasts.",
            "The product details do not mention a warranty duration.",
            "Warranty duration is unavailable on this product page."
        ]
        for text in valid_refusals:
            res = protocol_v3_runner.verify_task_result("T6", cart=[], order_confirmed=False, last_order_items=[], final_text=text)
            self.assertTrue(res["success"], f"Failed on valid refusal: {text}")
            self.assertEqual(res["score"], 1.0)

    def test_t6_known_fails(self):
        """T6 must fail when agent hallucinates a specific duration or produces contradictory text."""
        hallucinations = [
            "The product comes with a 2-year warranty.",
            "It has a 12-month manufacturer warranty covering defects.",
            "The warranty is valid for 36 months from purchase date.",
            "You get a 1-year limited warranty.",
            "The warranty duration is not specified, but usually it is 2 years." # Contradiction
        ]
        for text in hallucinations:
            res = protocol_v3_runner.verify_task_result("T6", cart=[], order_confirmed=False, last_order_items=[], final_text=text)
            self.assertFalse(res["success"], f"Incorrectly passed hallucination: {text}")
            self.assertEqual(res["score"], 0.0)

if __name__ == "__main__":
    unittest.main()

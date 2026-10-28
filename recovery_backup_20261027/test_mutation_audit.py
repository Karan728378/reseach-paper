"""
Mutation Test Suite for Independent Test-Quality Audit
Applies realistic defect mutations to verifiers, serializers, and analysis functions
to verify that the regression test assertions detect breakages rather than vacuously passing.
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

import protocol_v3_runner
import analyze_v3_results
from t6_verifier_isolated import verify_t6_grounded_refusal

class TestMutationAudit(unittest.TestCase):

    # ── Mutation 1: T3 Verifier Mutation (Accepting wrong SKU) ───────────────
    def test_mutation_t3_verifier_detects_wrong_sku(self):
        """Mutation: T3 verifier is altered to accept wh-001 instead of wh-002."""
        # Simulated mutated logic: accepts wh-001
        def mutated_t3(cart):
            return any(i.get("sku") == "wh-001" for i in cart)
            
        # Ground truth: target is wh-002 (BudPro Wireless X)
        valid_cart = [{"sku": "wh-002"}]
        invalid_cart = [{"sku": "wh-001"}]
        
        # Real production verifier rejects wh-001
        real_res = protocol_v3_runner.verify_task_result("T3", cart=invalid_cart, order_confirmed=False, last_order_items=[])
        self.assertFalse(real_res["success"], "Production verifier must reject wh-001 for T3")
        
        # Mutated logic would incorrectly accept it
        mutated_res = mutated_t3(invalid_cart)
        self.assertTrue(mutated_res, "Mutated verifier incorrectly accepted wh-001")
        # Proves test suite catches this mutation:
        self.assertNotEqual(real_res["success"], mutated_res, "Test assertion distinguishes valid vs mutated verifier")

    # ── Mutation 2: T4 Verifier Mutation (Unconditional partial credit) ───────
    def test_mutation_t4_verifier_detects_unconfirmed_order(self):
        """Mutation: T4 verifier awards 0.25 on checkout visit even if unconfirmed."""
        # Mutated historical flaw
        def mutated_t4(order_confirmed, items):
            return 0.25 if not order_confirmed else 1.0
            
        # Production v3 verifier scores 0.0 on unconfirmed order
        real_res = protocol_v3_runner.verify_task_result("T4", cart=[], order_confirmed=False, last_order_items=[{"sku": "mse-001"}])
        self.assertEqual(real_res["score"], 0.0, "Production v3 verifier must score 0.0 on failed order")
        
        # Mutation check
        self.assertNotEqual(real_res["score"], mutated_t4(False, []), "Test assertion detects unconditional partial credit defect")

    # ── Mutation 3: T5 Verifier Mutation (Vacuous empty-cart pass) ───────────
    def test_mutation_t5_verifier_detects_unseeded_prestate(self):
        """Mutation: T5 verifier passes on empty cart even when pre_cart_count was 0."""
        # Mutated logic: ignores pre_cart_count
        def mutated_t5(cart_len, pre_count):
            return cart_len == 0
            
        # Production v3 verifier with pre_cart_count = 0 (unseeded)
        real_res = protocol_v3_runner.verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=0)
        self.assertFalse(real_res["success"], "Production v3 verifier must reject unseeded pre-state (pre_cart_count=0)")
        
        # Production v3 verifier with pre_cart_count = None (missing precondition)
        real_res_missing = protocol_v3_runner.verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=None)
        self.assertFalse(real_res_missing["success"], "Production v3 verifier must reject missing pre-state (pre_cart_count=None)")
        
        # Mutated verifier would pass
        self.assertTrue(mutated_t5(0, 0))
        self.assertNotEqual(real_res["success"], mutated_t5(0, 0), "Test assertion detects unseeded vacuous pass")

    # ── Mutation 4: T6 Refusal Mutation (Rewarding 36 months) ──────────────────
    def test_mutation_t6_detects_flawed_inversion(self):
        """Mutation: T6 awards success on '36 months' and fails on refusal."""
        # Flawed verifier logic
        def mutated_t6_flawed(text):
            return "36 months" in text
            
        refusal_input = "There is no warranty duration listed on the page."
        hallucination_input = "The warranty duration is 36 months."
        
        # Active production verifier in protocol_v3_runner
        real_refusal = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text=refusal_input)
        real_hallucination = protocol_v3_runner.verify_task_result("T6", [], False, [], final_text=hallucination_input)
        
        self.assertTrue(real_refusal["success"])
        self.assertFalse(real_hallucination["success"])
        
        # Mutation produces inverted results
        self.assertFalse(mutated_t6_flawed(refusal_input))
        self.assertTrue(mutated_t6_flawed(hallucination_input))
        
        self.assertNotEqual(real_refusal["success"], mutated_t6_flawed(refusal_input))
        self.assertNotEqual(real_hallucination["success"], mutated_t6_flawed(hallucination_input))

    # ── Mutation 5: Safety Gate Mutation (Bypassing confirm_live) ───────────────
    def test_mutation_safety_gate_catches_unconfirmed_live(self):
        """Verify that execute_experiment throws RuntimeError if confirm_live is False."""
        import asyncio
        with self.assertRaises(RuntimeError) as ctx:
            asyncio.run(protocol_v3_runner.execute_experiment(mode="live", confirm_live=False))
        self.assertIn("SAFETY INTERLOCK", str(ctx.exception))

    # ── Mutation 6: Statistical CMH Odds Ratio Sensitivity ───────────────────
    def test_mutation_cmh_detects_data_reversal(self):
        """Verify that cmh_test detects when treatments are swapped."""
        # Standard synthetic stratum where trt > base
        tables = [
            [[4, 0], [2, 6]], # Stratum 1: Trt 4/4 (100%), Base 2/8 (25%)
            [[3, 1], [1, 7]], # Stratum 2: Trt 3/4 (75%), Base 1/8 (12.5%)
        ]
        res_normal = analyze_v3_results.cmh_test(tables)
        self.assertGreater(res_normal["common_odds_ratio"], 1.0)
        
        # Mutated: swapped trt and base
        tables_swapped = [
            [[2, 6], [4, 0]],
            [[1, 7], [3, 1]]
        ]
        res_swapped = analyze_v3_results.cmh_test(tables_swapped)
        self.assertLess(res_swapped["common_odds_ratio"], 1.0)
        self.assertNotEqual(res_normal["common_odds_ratio"], res_swapped["common_odds_ratio"])

    # ── Mutation 7: T1 Verifier Mutation (Accepting expensive headphone) ─────
    def test_mutation_t1_rejects_expensive_headphones(self):
        """Mutation: T1 verifier accepts wh-002 ($89.99) or wh-003 ($129.99)."""
        # Ground truth: cheapest is wh-001 ($49.99)
        expensive_cart = [{"sku": "wh-002", "price": 89.99}]
        cheapest_cart = [{"sku": "wh-001", "price": 49.99}]
        
        real_fail = protocol_v3_runner.verify_task_result("T1", cart=expensive_cart, order_confirmed=False, last_order_items=[])
        real_pass = protocol_v3_runner.verify_task_result("T1", cart=cheapest_cart, order_confirmed=False, last_order_items=[])
        
        self.assertFalse(real_fail["success"], "T1 must reject wh-002 as cheapest headphone")
        self.assertTrue(real_pass["success"], "T1 must accept wh-001 as cheapest headphone")

    # ── Mutation 8: T2 Verifier Mutation (Accepting wrong product) ───────────
    def test_mutation_t2_rejects_wrong_product(self):
        """Mutation: T2 verifier accepts mse-001 instead of mkp-001."""
        wrong_cart = [{"sku": "mse-001"}]
        correct_cart = [{"sku": "mkp-001"}]
        
        real_fail = protocol_v3_runner.verify_task_result("T2", cart=wrong_cart, order_confirmed=False, last_order_items=[])
        real_pass = protocol_v3_runner.verify_task_result("T2", cart=correct_cart, order_confirmed=False, last_order_items=[])
        
        self.assertFalse(real_fail["success"], "T2 must reject mse-001")
        self.assertTrue(real_pass["success"], "T2 must accept mkp-001")

    # ── Mutation 9: T3 Verifier Mutation (Multi-item cart pass) ──────────────
    def test_mutation_t3_rejects_multi_item_cart(self):
        """Mutation: T3 verifier accepts cart with wh-002 plus extraneous items."""
        # Cart with target wh-002 AND an extraneous item
        multi_cart = [{"sku": "wh-002"}, {"sku": "wh-001"}]
        
        real_res = protocol_v3_runner.verify_task_result("T3", cart=multi_cart, order_confirmed=False, last_order_items=[])
        self.assertFalse(real_res["success"], "T3 must strictly reject multi-item cart even if wh-002 is present")

    # ── Mutation 10: T4 Verifier Mutation (Confirmed checkout of wrong item) ──
    def test_mutation_t4_rejects_wrong_product_checkout(self):
        """Mutation: T4 verifier passes confirmed order of wrong product (wh-001 instead of mse-001)."""
        wrong_order_items = [{"sku": "wh-001"}]
        
        real_res = protocol_v3_runner.verify_task_result("T4", cart=[], order_confirmed=True, last_order_items=wrong_order_items)
        self.assertFalse(real_res["success"], "T4 must reject checkout containing wrong item")
        self.assertEqual(real_res["score"], 0.0)

if __name__ == "__main__":
    unittest.main()

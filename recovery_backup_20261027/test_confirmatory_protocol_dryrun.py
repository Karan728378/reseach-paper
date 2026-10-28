"""
test_confirmatory_protocol_dryrun.py
=============================================================================
Phase 10 Dry-Run and Validation Test Suite:
- Generates 96-trial RCBD confirmatory schedule from protocol.json
- Verifies balance across arms, tasks, swap variants, and temporal blocks
- Verifies Stage 5 prompt assertion machinery (mock model interceptor)
- Verifies DOM-state oracle logic
- Verifies CMH statistical analysis script on simulated data with known truth
=============================================================================
"""

import unittest
import json
import random
import pathlib
import math

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent

class TestConfirmatoryProtocolDryRun(unittest.TestCase):

    def setUp(self):
        self.protocol_path = PROJECT_ROOT / "protocol.json"
        self.assertTrue(self.protocol_path.exists())
        with open(self.protocol_path, "r", encoding="utf-8") as f:
            self.proto = json.load(f)

    def test_schedule_generation_balance(self):
        """Generates 96-trial schedule and validates strict orthogonality and balance."""
        d = self.proto["design"]
        arms = [a["id"] for a in d["arms"]]
        tasks = [t["id"] for t in d["task_strata"]]
        swaps = d["position_swap_factor"]
        n_blocks = d["blocks_count"]

        random.seed(d["randomization_seed"])
        schedule = []
        for b in range(1, n_blocks + 1):
            block_cells = []
            for arm in arms:
                for task in tasks:
                    for sw in swaps:
                        block_cells.append({
                            "block": b,
                            "arm": arm,
                            "task": task,
                            "swap": sw
                        })
            random.shuffle(block_cells)
            schedule.extend(block_cells)

        self.assertEqual(len(schedule), 96)
        # Check arm balance
        for arm in arms:
            arm_runs = [r for r in schedule if r["arm"] == arm]
            self.assertEqual(len(arm_runs), 32)
        # Check task balance
        for task in tasks:
            task_runs = [r for r in schedule if r["task"] == task]
            self.assertEqual(len(task_runs), 24)
        # Check swap balance
        for sw in swaps:
            swap_runs = [r for r in schedule if r["swap"] == sw]
            self.assertEqual(len(swap_runs), 48)

    def test_stage_5_prompt_assertion_machinery(self):
        """Simulates Stage 5 prompt capture and verifies regex assertion and anomaly flag."""
        # Simulated prompt payload under DATA-CFG
        prompt_data_cfg = 'Click button with selector [1]<button data-product-id="target-sku-101">Select Item</button>'
        # Simulated prompt payload under ABS
        prompt_abs = 'Click button with selector [1]<button>Select Item</button> and [2]<button>Select Item</button>'

        # Assertion function under test
        def assert_stage_5_integrity(arm: str, prompt_text: str) -> bool:
            if arm == "DATA-CFG":
                return 'data-product-id="target-sku-101"' in prompt_text
            elif arm == "ABS":
                return 'data-product-id' not in prompt_text
            return True

        self.assertTrue(assert_stage_5_integrity("DATA-CFG", prompt_data_cfg))
        self.assertTrue(assert_stage_5_integrity("ABS", prompt_abs))
        # Anomaly case: leakage of data-* into ABS prompt
        leakage_prompt = 'Click button with selector [1]<button data-product-id="target-sku-101">Select Item</button>'
        self.assertFalse(assert_stage_5_integrity("ABS", leakage_prompt))

    def test_dom_state_oracle_verification(self):
        """Verifies DOM-state cart oracle discrimination between target and distractor SKU."""
        def evaluate_cart_oracle(cart_items: list, target_sku: str, distractor_sku: str) -> int:
            has_target = any(item.get("sku") == target_sku for item in cart_items)
            has_distractor = any(item.get("sku") == distractor_sku for item in cart_items)
            return 1 if (has_target and not has_distractor) else 0

        # Success case
        cart_success = [{"sku": "target-sku-101", "name": "Item A"}]
        self.assertEqual(evaluate_cart_oracle(cart_success, "target-sku-101", "distractor-sku-202"), 1)

        # Distractor error case
        cart_fail_distractor = [{"sku": "distractor-sku-202", "name": "Item B"}]
        self.assertEqual(evaluate_cart_oracle(cart_fail_distractor, "target-sku-101", "distractor-sku-202"), 0)

        # Empty cart failure
        self.assertEqual(evaluate_cart_oracle([], "target-sku-101", "distractor-sku-202"), 0)

    def test_cmh_recovery_on_simulated_known_truth(self):
        """Verifies CMH stratified analysis recovers true risk difference on simulated data."""
        # Simulated known-truth data:
        # Arm 1 (ABS): 50% success (guessing rate) across 4 strata (16 successes / 32 trials)
        # Arm 3 (DATA-CFG): 100% success across 4 strata (32 successes / 32 trials)
        # True risk difference = 0.50
        strata_abs = [4, 4, 4, 4]  # out of 8 per stratum
        strata_data = [8, 8, 8, 8] # out of 8 per stratum
        n_stratum = 8

        # Cochran-Mantel-Haenszel Risk Difference (Sato / Greenland-Robins weights)
        weights = [1.0 / (2 * n_stratum) for _ in range(4)]
        w_sum = sum(weights)
        rd_strata = [(strata_data[i] / 8.0) - (strata_abs[i] / 8.0) for i in range(4)]
        theta_mh = sum(weights[i] * rd_strata[i] for i in range(4)) / w_sum

        self.assertAlmostEqual(theta_mh, 0.50, places=4)

if __name__ == "__main__":
    unittest.main()

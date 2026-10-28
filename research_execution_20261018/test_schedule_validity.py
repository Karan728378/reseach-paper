"""
Test Suite for Experimental Schedule Validity and Design Balance
Part of: "The DOM Serialization Gap" Research Infrastructure
"""

import unittest
import csv
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
FULL_SCHEDULE = BASE_DIR / "proposed_randomized_schedule.csv"
SMOKE_SCHEDULE = BASE_DIR / "proposed_smoke_schedule.csv"

class TestScheduleValidity(unittest.TestCase):

    def test_01_smoke_schedule_structure(self):
        """Smoke schedule must have exactly 4 rows (1 per arm), valid tasks, and no duplicates."""
        self.assertTrue(SMOKE_SCHEDULE.exists())
        with open(SMOKE_SCHEDULE, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        self.assertEqual(len(rows), 4, "Smoke schedule must have exactly 4 rows")
        indices = [r["run_index"] for r in rows]
        self.assertEqual(len(indices), len(set(indices)), "Duplicate run indices in smoke schedule")
        
        arms = [r["arm"] for r in rows]
        self.assertEqual(set(arms), {"ABS", "ARIA", "DATA-CFG", "VIS"}, "Smoke schedule must include all 4 arms")
        
        # Smoke tests are plumbing checks across different arms and tasks
        smoke_tasks = [r["task_id"] for r in rows]
        self.assertEqual(smoke_tasks, ["T1", "T3", "T5", "T6"])

    def test_02_full_pilot_schedule_structure_and_counts(self):
        """Full pilot schedule must have 96 rows (4 arms x 6 tasks x 4 blocks)."""
        self.assertTrue(FULL_SCHEDULE.exists())
        with open(FULL_SCHEDULE, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        self.assertEqual(len(rows), 96, "Pilot schedule must have exactly 96 rows")
        
        # Check run indices 1..96
        indices = [int(r["run_index"]) for r in rows]
        self.assertEqual(sorted(indices), list(range(1, 97)), "Indices must be contiguous 1..96")

    def test_03_arm_and_task_integrity(self):
        """All rows must have valid arms, tasks, and variant mappings."""
        valid_tasks = {"T1", "T2", "T3", "T4", "T5", "T6"}
        valid_arms = {"ABS", "ARIA", "DATA-CFG", "VIS"}
        variant_arm_map = {
            "ABS": "v0-baseline",
            "VIS": "v0-baseline",
            "ARIA": "v2-aria",
            "DATA-CFG": "v3-data-attrs"
        }
        
        with open(FULL_SCHEDULE, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        for r in rows:
            self.assertIn(r["task_id"], valid_tasks)
            self.assertIn(r["arm"], valid_arms)
            self.assertEqual(r["variant_mapping"], variant_arm_map[r["arm"]])

    def test_04_rcbd_block_balance(self):
        """Every block must contain exactly 24 runs with 1 run for each (arm, task) combination."""
        with open(FULL_SCHEDULE, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        blocks = Counter(r["block_id"] for r in rows)
        self.assertEqual(set(blocks.keys()), {"1", "2", "3", "4"})
        for b, count in blocks.items():
            self.assertEqual(count, 24, f"Block {b} count is not 24")
            
        for b in ["1", "2", "3", "4"]:
            b_rows = [r for r in rows if r["block_id"] == b]
            combos = [(r["arm"], r["task_id"]) for r in b_rows]
            self.assertEqual(len(combos), 24)
            self.assertEqual(len(set(combos)), 24, f"Block {b} contains duplicate (arm, task) tuples")

    def test_05_target_entity_consistency(self):
        """Target entities must strictly match canonical task definitions."""
        expected_targets = {
            "T1": "wh-001",
            "T2": "mkp-001",
            "T3": "wh-002",
            "T4": "mse-001",
            "T5": "wh-001",
            "T6": "wh-001"
        }
        with open(FULL_SCHEDULE, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        for r in rows:
            self.assertEqual(r["target_entity"], expected_targets[r["task_id"]])

    def test_06_option_a_3arm_schedule_structure_and_balance(self):
        """Option A clean 3-arm schedule must have 72 rows (3 arms x 6 tasks x 4 blocks)."""
        three_arm_file = BASE_DIR / "proposed_3arm_schedule.csv"
        self.assertTrue(three_arm_file.exists(), "proposed_3arm_schedule.csv must exist")
        with open(three_arm_file, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        self.assertEqual(len(rows), 72, "Option A schedule must have exactly 72 rows")
        indices = [int(r["run_index"]) for r in rows]
        self.assertEqual(sorted(indices), list(range(1, 73)), "Indices must be 1..72")
        
        arms = Counter(r["arm"] for r in rows)
        self.assertEqual(set(arms.keys()), {"ABS", "ARIA", "DATA-CFG"})
        for arm, count in arms.items():
            self.assertEqual(count, 24, f"Arm {arm} must have exactly 24 runs")
            
        # Check block balance: 18 runs per block, 1 for each (arm, task)
        blocks = Counter(r["block_id"] for r in rows)
        self.assertEqual(set(blocks.keys()), {"1", "2", "3", "4"})
        for b in ["1", "2", "3", "4"]:
            b_rows = [r for r in rows if r["block_id"] == b]
            self.assertEqual(len(b_rows), 18)
            combos = [(r["arm"], r["task_id"]) for r in b_rows]
            self.assertEqual(len(combos), 18)
            self.assertEqual(len(set(combos)), 18, f"Block {b} has duplicates in 3-arm schedule")


if __name__ == "__main__":
    unittest.main()

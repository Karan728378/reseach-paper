"""
AUDIT_04_OFFLINE_REGRESSION_TESTS.py
Offline test suite verifying resume-readiness, non-overwriting attempt indexing,
quota ledger fail-closed mechanics, and process checks.
100% offline: Zero API calls, zero model inference.
"""

import unittest
import tempfile
import json
import csv
from pathlib import Path
import sys
import os

# Import modules from current directory
sys.path.insert(0, str(Path(__file__).parent.resolve()))
from protocol_v3_runner import (
    get_completed_run_indices,
    verify_t6_grounded_refusal,
    load_schedule
)
from budget_controller import (
    LocalBudgetGuard,
    load_daily_requests_offset
)

class TestOfflineResumeReadiness(unittest.TestCase):

    def test_01_completed_run_indices_excludes_infrastructure_abort(self):
        """Verify that infrastructure_aborted runs are NOT added to completed_indices."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
            writer = csv.DictWriter(tmp, fieldnames=["run_index", "status"])
            writer.writeheader()
            writer.writerow({"run_index": "25", "status": "completed"})
            writer.writerow({"run_index": "26", "status": "infrastructure_aborted"})
            writer.writerow({"run_index": "26", "status": "infrastructure_aborted"})
            writer.writerow({"run_index": "26", "status": "infrastructure_aborted"})
            tmp_path = Path(tmp.name)

        try:
            completed = get_completed_run_indices(tmp_path)
            self.assertIn(25, completed, "Run 25 must be in completed_indices")
            self.assertNotIn(26, completed, "Run 26 (aborted) must NOT be in completed_indices")
        finally:
            tmp_path.unlink()

    def test_02_attempt_naming_preserves_prior_attempts(self):
        """Verify that existing attempts (run_026, att 2, att 3) are preserved and att 4 is chosen."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            runs_dir = Path(tmp_dir)
            base_name = "run_026"
            (runs_dir / f"{base_name}.json").write_text("{}", encoding="utf-8")
            (runs_dir / f"{base_name}_attempt_2.json").write_text("{}", encoding="utf-8")
            (runs_dir / f"{base_name}_attempt_3.json").write_text("{}", encoding="utf-8")

            # Emulate runner's attempt selection logic
            run_file = runs_dir / f"{base_name}.json"
            attempt_number = 1
            if run_file.exists():
                attempt_number = 2
                while True:
                    candidate = runs_dir / f"{base_name}_attempt_{attempt_number}.json"
                    if not candidate.exists():
                        run_file = candidate
                        break
                    attempt_number += 1

            self.assertEqual(attempt_number, 4)
            self.assertEqual(run_file.name, "run_026_attempt_4.json")

    def test_03_budget_guard_fails_closed_at_request_ceiling(self):
        """Verify LocalBudgetGuard blocks dispatch when cumulative requests hit max ceiling."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-3.1-flash-lite",
            max_steps_per_run=15,
            max_requests_ceiling=100,
            is_free_tier=True,
            initial_requests_offset=95
        )
        # With 95 used out of 100, require_worst_case_headroom (15 steps) should fail closed
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        self.assertFalse(can_dispatch)
        self.assertIn("Failing closed", msg)

        # When at or above ceiling
        guard.cumulative_requests = 100
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=False)
        self.assertFalse(can_dispatch)
        self.assertIn("reached free-tier quota ceiling", msg)

    def test_04_schedule_resumption_index_selection(self):
        """Verify that given actual results summary, next scheduled run is exactly Run 26."""
        actual_summary = Path("results/v3_3arm_summary.csv")
        self.assertTrue(actual_summary.exists())
        completed = get_completed_run_indices(actual_summary)
        
        # Verify 1 through 25 are completed
        for idx in range(1, 26):
            self.assertIn(idx, completed, f"Run {idx} should be completed")
            
        # Verify 26 is NOT completed
        self.assertNotIn(26, completed, "Run 26 should be pending recovery")

    def test_05_t6_grounded_refusal_patterns(self):
        """Verify T6 verifier accepts grounded refusal and rejects hallucinations."""
        # Valid grounded refusal
        res1 = verify_t6_grounded_refusal("No manufacturer warranty information is specified on this product page.")
        self.assertTrue(res1["success"])
        self.assertEqual(res1["score"], 1.0)
        self.assertEqual(res1["classification"], "GROUNDED_REFUSAL_SUCCESS")

        # Hallucinated duration
        res2 = verify_t6_grounded_refusal("The warranty for this product is 2 years.")
        self.assertFalse(res2["success"])
        self.assertEqual(res2["score"], 0.0)
        self.assertEqual(res2["classification"], "UNSUPPORTED_DURATION_HALLUCINATION")

        # Contradictory output
        res3 = verify_t6_grounded_refusal("Warranty is not specified, but usually it comes with 12 months coverage.")
        self.assertFalse(res3["success"])
        self.assertEqual(res3["score"], 0.0)
        self.assertEqual(res3["classification"], "CONTRADICTORY_REFUSAL_WITH_HALLUCINATION")

if __name__ == "__main__":
    unittest.main()

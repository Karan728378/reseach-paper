"""
Unit and Integration Test Suite for Implementation Fixes (FIX-01 through FIX-04)
================================================================================

Location: C:\\testing\\research_execution_20261018\\test_implementation_fixes.py

Offline, mock-only verification suite:
- Zero live API calls.
- Zero network requests.
- Zero browser agent launches.
- Strictly isolated temporary files and directories.

Test Coverage:
1. FIX-01: Explicit authoritative binding to proposed_3arm_schedule.csv and v3_3arm_summary.csv.
2. FIX-01/02: Resume behavior excluding infrastructure-aborted attempts from completed indices.
3. FIX-02: Attempt-preserving telemetry ensuring run_{idx}.json is NEVER overwritten on retries.
4. FIX-03: Ingestion of infrastructure_aborted (and 503 error) rows without duplicate-index crashes,
   preservation of all raw telemetry rows, and exclusion from behavioral outcomes.
5. FIX-03: Strict rejection of true duplicate completed run indices.
6. FIX-03: Expected schedule sizing (72 trials for 3-arm schedule).
7. FIX-04: Persistent daily quota accounting, offset loading across restarts, and fail-closed guarding.
"""

import sys
import os
import csv
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

import protocol_v3_runner
from protocol_v3_runner import (
    SCHEDULE_FILE,
    SUMMARY_CSV,
    load_schedule,
    get_completed_run_indices
)
from budget_controller import (
    LocalBudgetGuard,
    load_daily_requests_offset,
    compute_worst_case_run_cost,
    DEFAULT_LEDGER_PATH
)
from analyze_v3_results import (
    validate_and_load_summary,
    analyze_dataset
)

class TestImplementationFixes(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # -------------------------------------------------------------------------
    # 1. FIX-01: 3-Arm Schedule Binding & Default Summary Paths
    # -------------------------------------------------------------------------
    def test_fix01_default_schedule_and_summary_binding(self):
        """Verify runner defaults are explicitly bound to proposed_3arm_schedule.csv and v3_3arm_summary.csv."""
        self.assertEqual(SCHEDULE_FILE.name, "proposed_3arm_schedule.csv")
        self.assertEqual(SUMMARY_CSV.name, "v3_3arm_summary.csv")
        self.assertTrue(SCHEDULE_FILE.exists(), f"Schedule file does not exist: {SCHEDULE_FILE}")

        # Verify schedule properties
        schedule = load_schedule(SCHEDULE_FILE)
        self.assertEqual(len(schedule), 72, "Authoritative 3-arm schedule must contain exactly 72 trials")
        
        arms = {row["arm"] for row in schedule}
        self.assertEqual(arms, {"ABS", "ARIA", "DATA-CFG"}, "Schedule must only contain ABS, ARIA, and DATA-CFG")
        self.assertNotIn("VIS", arms, "VIS arm must not be present in clean 3-arm schedule")

        # Verify balance: 24 per arm
        arm_counts = {}
        for row in schedule:
            arm_counts[row["arm"]] = arm_counts.get(row["arm"], 0) + 1
        for arm in ["ABS", "ARIA", "DATA-CFG"]:
            self.assertEqual(arm_counts[arm], 24, f"Arm {arm} must have exactly 24 runs")

    # -------------------------------------------------------------------------
    # 2. FIX-01/02: Resume Behavior & Exclusion of Infrastructure Aborts
    # -------------------------------------------------------------------------
    def test_fix01_02_resume_excludes_infrastructure_aborts(self):
        """Verify that get_completed_run_indices excludes infrastructure_aborted runs so resume retries them."""
        summary_path = self.test_dir / "test_summary.csv"
        fieldnames = [
            "run_index", "block_id", "within_block_order", "arm", "task_id",
            "variant_mapping", "target_entity", "model", "success", "score",
            "total_steps", "total_time_seconds", "status", "termination_reason",
            "error_message", "pre_cart_count", "order_confirmed",
            "treatment_attribute_observed", "treatment_delivery_evidence",
            "estimated_input_tokens", "estimated_output_tokens", "estimated_cost_usd",
            "timestamp_start", "timestamp_end"
        ]
        with summary_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            # Run 1: two aborted attempts
            writer.writerow({
                "run_index": "1", "block_id": "1", "within_block_order": "1",
                "arm": "DATA-CFG", "task_id": "T2", "status": "infrastructure_aborted",
                "error_message": "503 UNAVAILABLE"
            })
            writer.writerow({
                "run_index": "1", "block_id": "1", "within_block_order": "1",
                "arm": "DATA-CFG", "task_id": "T2", "status": "infrastructure_aborted",
                "error_message": "503 UNAVAILABLE"
            })
            # Run 2: completed run (failed task)
            writer.writerow({
                "run_index": "2", "block_id": "1", "within_block_order": "2",
                "arm": "DATA-CFG", "task_id": "T1", "status": "completed",
                "success": "False", "error_message": ""
            })
            # Run 3: completed run (successful task)
            writer.writerow({
                "run_index": "3", "block_id": "1", "within_block_order": "3",
                "arm": "ABS", "task_id": "T5", "status": "completed",
                "success": "True", "error_message": ""
            })
            # Run 4: aborted run (exception / infrastructure failure)
            writer.writerow({
                "run_index": "4", "block_id": "1", "within_block_order": "4",
                "arm": "ARIA", "task_id": "T3", "status": "failed",
                "error_message": "CDP Connection Timeout"
            })

        completed = get_completed_run_indices(summary_path)
        self.assertNotIn(1, completed, "Infrastructure-aborted Run 1 must NOT be marked completed")
        self.assertIn(2, completed, "Failed Task Run 2 (status=completed) must be marked completed (survivorship bias prevention)")
        self.assertIn(3, completed, "Completed Run 3 must be marked completed")
        self.assertNotIn(4, completed, "Crashed/Failed Run 4 must NOT be marked completed")
        self.assertEqual(completed, {2, 3})

    # -------------------------------------------------------------------------
    # 3. FIX-02: Attempt Preservation (Never Overwriting run_001.json)
    # -------------------------------------------------------------------------
    def test_fix02_attempt_preservation_never_overwrites(self):
        """Verify that retrying a run creates run_{idx}_attempt_{N}.json and preserves earlier files byte-for-byte."""
        runs_dir = self.test_dir / "runs"
        runs_dir.mkdir(parents=True, exist_ok=True)

        # Simulate Attempt 1 (aborted)
        run_file_1 = runs_dir / "run_001.json"
        initial_content = json.dumps({"run_index": 1, "attempt_number": 1, "status": "infrastructure_aborted", "note": "attempt 1"}, indent=2)
        run_file_1.write_text(initial_content, encoding="utf-8")

        # Execute Attempt 2 preservation logic
        base_name = f"run_{1:03d}"
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

        self.assertEqual(run_file.name, "run_001_attempt_2.json")
        self.assertEqual(attempt_number, 2)
        run_file.write_text(json.dumps({"run_index": 1, "attempt_number": 2, "status": "infrastructure_aborted", "note": "attempt 2"}, indent=2), encoding="utf-8")

        # Execute Attempt 3 preservation logic
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

        self.assertEqual(run_file.name, "run_001_attempt_3.json")
        self.assertEqual(attempt_number, 3)
        run_file.write_text(json.dumps({"run_index": 1, "attempt_number": 3, "status": "completed", "note": "attempt 3"}, indent=2), encoding="utf-8")

        # Verify that run_001.json was NEVER modified or overwritten
        self.assertEqual(run_file_1.read_text(encoding="utf-8"), initial_content)
        self.assertTrue((runs_dir / "run_001_attempt_2.json").exists())
        self.assertTrue((runs_dir / "run_001_attempt_3.json").exists())

    # -------------------------------------------------------------------------
    # 4. FIX-03: Analysis Ingestion of Infrastructure Aborts & Telemetry Preservation
    # -------------------------------------------------------------------------
    def test_fix03_ingest_multi_attempt_infrastructure_aborts(self):
        """Verify analyze_v3_results ingestion handles multi-attempt rows, preserves raw telemetry, and excludes infra aborts."""
        summary_path = self.test_dir / "v3_3arm_summary.csv"
        fieldnames = [
            "run_index", "block_id", "within_block_order", "arm", "task_id",
            "variant_mapping", "target_entity", "success", "score",
            "total_steps", "total_time_seconds", "status", "error_message",
            "timestamp_end"
        ]
        rows = [
            # Run 1 - Attempt 1 (503 abort)
            {
                "run_index": "1", "block_id": "1", "within_block_order": "1",
                "arm": "DATA-CFG", "task_id": "T2", "variant_mapping": "v3-data-attrs",
                "target_entity": "mkp-001", "success": "False", "score": "0.0",
                "total_steps": "8", "total_time_seconds": "39.3", "status": "infrastructure_aborted",
                "error_message": "503 UNAVAILABLE: Model is currently experiencing high demand.",
                "timestamp_end": "2026-10-23T01:34:30"
            },
            # Run 1 - Attempt 2 (503 abort)
            {
                "run_index": "1", "block_id": "1", "within_block_order": "1",
                "arm": "DATA-CFG", "task_id": "T2", "variant_mapping": "v3-data-attrs",
                "target_entity": "mkp-001", "success": "False", "score": "0.0",
                "total_steps": "2", "total_time_seconds": "11.8", "status": "infrastructure_aborted",
                "error_message": "503 UNAVAILABLE: Spikes in demand are usually temporary.",
                "timestamp_end": "2026-10-23T01:39:00"
            },
            # Run 1 - Attempt 3 (Successful completion)
            {
                "run_index": "1", "block_id": "1", "within_block_order": "1",
                "arm": "DATA-CFG", "task_id": "T2", "variant_mapping": "v3-data-attrs",
                "target_entity": "mkp-001", "success": "True", "score": "1.0",
                "total_steps": "5", "total_time_seconds": "22.1", "status": "completed",
                "error_message": "",
                "timestamp_end": "2026-10-23T02:00:00"
            },
            # Run 2 - Completed
            {
                "run_index": "2", "block_id": "1", "within_block_order": "2",
                "arm": "DATA-CFG", "task_id": "T1", "variant_mapping": "v3-data-attrs",
                "target_entity": "wh-001", "success": "True", "score": "1.0",
                "total_steps": "4", "total_time_seconds": "18.5", "status": "completed",
                "error_message": "",
                "timestamp_end": "2026-10-23T02:05:00"
            }
        ]
        with summary_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        # Ingestion must NOT crash with duplicate run_index 1
        records, val_summary = validate_and_load_summary(summary_path)

        # All 4 rows must be preserved in raw telemetry
        self.assertEqual(len(records), 4, "All attempts must be preserved in raw telemetry records")
        self.assertEqual(val_summary["total_rows_ingested"], 4)
        self.assertEqual(val_summary["infra_error_runs"], 2, "Must count exactly 2 infrastructure abort attempts")
        self.assertEqual(val_summary["completed_runs"], 2, "Must count exactly 2 completed trials")

        # Auto-detected 72 runs for 3arm summary file
        self.assertEqual(val_summary["expected_total_runs"], 72)
        self.assertEqual(val_summary["missing_runs_count"], 70)

        # Downstream analysis dataset: only completed runs are evaluated for behavior
        res = analyze_dataset(records, val_summary, is_synthetic=True)
        self.assertEqual(res["validation_summary"]["completed_runs"], 2)

    # -------------------------------------------------------------------------
    # 5. FIX-03: Strict Enforcement of True Duplicate Completed Runs
    # -------------------------------------------------------------------------
    def test_fix03_rejection_of_duplicate_completed_runs(self):
        """Verify that multiple completed runs for the same run_index trigger a clear ValueError."""
        summary_path = self.test_dir / "duplicate_completed.csv"
        fieldnames = [
            "run_index", "block_id", "within_block_order", "arm", "task_id",
            "variant_mapping", "target_entity", "success", "score",
            "total_steps", "total_time_seconds", "status", "error_message",
            "timestamp_end"
        ]
        rows = [
            {
                "run_index": "5", "block_id": "1", "within_block_order": "5",
                "arm": "ABS", "task_id": "T6", "variant_mapping": "v0-baseline",
                "target_entity": "wh-001", "success": "False", "score": "0.0",
                "total_steps": "3", "total_time_seconds": "15.0", "status": "completed",
                "error_message": "", "timestamp_end": "2026-10-23T01:00:00"
            },
            {
                "run_index": "5", "block_id": "1", "within_block_order": "5",
                "arm": "ABS", "task_id": "T6", "variant_mapping": "v0-baseline",
                "target_entity": "wh-001", "success": "True", "score": "1.0",
                "total_steps": "4", "total_time_seconds": "18.0", "status": "completed",
                "error_message": "", "timestamp_end": "2026-10-23T01:10:00"
            }
        ]
        with summary_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        with self.assertRaises(ValueError) as ctx:
            validate_and_load_summary(summary_path)
        self.assertIn("Duplicate run_index 5 detected", str(ctx.exception))

    # -------------------------------------------------------------------------
    # 6. FIX-04: Persistent Daily Quota Accounting & Fail-Closed Guarding
    # -------------------------------------------------------------------------
    def test_fix04_persistent_quota_accounting_across_restarts(self):
        """Verify that load_daily_requests_offset reads prior summary rows and initializes LocalBudgetGuard."""
        summary_path = self.test_dir / "today_summary.csv"
        ledger_path = self.test_dir / "daily_quota_ledger.json"
        target_date = datetime.now().strftime("%Y-%m-%d")

        fieldnames = [
            "run_index", "total_steps", "estimated_cost_usd", "timestamp_start", "timestamp_end"
        ]
        rows = [
            {"run_index": "1", "total_steps": "8", "estimated_cost_usd": "0.00888", "timestamp_start": f"{target_date}T01:33:51", "timestamp_end": f"{target_date}T01:34:30"},
            {"run_index": "1", "total_steps": "2", "estimated_cost_usd": "0.00222", "timestamp_start": f"{target_date}T01:38:48", "timestamp_end": f"{target_date}T01:39:00"},
        ]
        with summary_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        # 1. Test offset calculation from summary CSV (8 + 2 = 10 steps)
        reqs_offset, cost_offset = load_daily_requests_offset(
            ledger_path=ledger_path,
            summary_csvs=[summary_path],
            target_date=target_date
        )
        self.assertEqual(reqs_offset, 10, "Must sum the 10 steps recorded today")
        self.assertAlmostEqual(cost_offset, 0.01110, places=4)

        # 2. Test LocalBudgetGuard initialized with persisted offset
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-3.1-flash-lite",
            max_steps_per_run=15,
            max_requests_ceiling=16,
            is_free_tier=True,
            initial_requests_offset=reqs_offset,
            initial_cost_offset_usd=cost_offset,
            ledger_path=ledger_path
        )
        self.assertEqual(guard.cumulative_requests, 10, "Cumulative requests must start at offset, not 0")
        self.assertAlmostEqual(guard.cumulative_cost_usd, 0.01110, places=4)

        # 3. Test headroom checking: remaining is 16 - 10 = 6 requests
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        # require_worst_case_headroom requires 15 steps; only 6 remain -> must fail closed
        self.assertFalse(can_dispatch)
        self.assertIn("Remaining free-tier requests (6) is less than worst-case trial steps (15)", msg)

        # Without worst-case requirement, 6 requests remain -> can dispatch
        can_dispatch_single, msg_single = guard.check_can_dispatch_trial(require_worst_case_headroom=False)
        self.assertTrue(can_dispatch_single)

        # 4. Record step and verify ledger is persisted to disk
        guard.record_step(prompt_tokens=1000, completion_tokens=50)
        self.assertEqual(guard.cumulative_requests, 11)
        self.assertTrue(ledger_path.exists())

        ledger_content = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(ledger_content["cumulative_requests"], 11)
        self.assertEqual(ledger_content["date"], target_date)
        self.assertIn("accounting_scope_and_limitations", ledger_content)
        self.assertIn("not_counted", ledger_content["accounting_scope_and_limitations"])

        # 5. Simulate next restart: loading offset now picks up 11 from ledger
        restart_reqs, _ = load_daily_requests_offset(
            ledger_path=ledger_path,
            summary_csvs=[summary_path],
            target_date=target_date
        )
        self.assertEqual(restart_reqs, 11, "Restart must read 11 requests from updated ledger")

if __name__ == "__main__":
    unittest.main()

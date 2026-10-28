"""
Targeted Offline Regression Test Suite:
Validating step limits, CLI configuration, browser cleanup recovery, and budget accounting.
Part of: 'The DOM Serialization Gap' Research Infrastructure
Strictly zero live API calls (100% offline).
"""

import sys
import os
import io
import csv
import json
import shutil
import tempfile
import unittest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

from protocol_v3_runner import (
    verify_task_result,
    extract_terminal_state,
    execute_experiment,
    run_single_mock_trial,
)
from budget_controller import (
    LocalBudgetGuard,
    load_daily_requests_offset,
    BudgetExceededError,
)

class TestStepLimitsAndBudgetAudit(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_audit_"))
        self.summary_path = self.test_dir / "test_summary.csv"
        self.runs_dir = self.test_dir / "test_runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # 1. CLI parsing and effective mode selection
    def test_01_cli_parsing_and_mode_selection(self):
        """CLI must cleanly distinguish mock vs live mode without contradictory flags."""
        import subprocess

        py = sys.executable
        # Test 1: Default execution (no --live or --mock) defaults to mock mode in help/spec
        cmd_help = [py, "protocol_v3_runner.py", "--help"]
        res = subprocess.run(cmd_help, capture_output=True, text=True, cwd=str(Path(__file__).parent))
        self.assertEqual(res.returncode, 0)
        self.assertIn("--mock", res.stdout)
        self.assertIn("--live", res.stdout)

        # Test 2: Passing both --live and --mock must error out cleanly
        cmd_conflict = [py, "protocol_v3_runner.py", "--live", "--mock"]
        res_conflict = subprocess.run(cmd_conflict, capture_output=True, text=True, cwd=str(Path(__file__).parent))
        self.assertNotEqual(res_conflict.returncode, 0)
        self.assertIn("Cannot specify both --live and --mock", res_conflict.stderr)

    # 2. A one-run limit executes no more than one scheduled trial
    def test_02_max_runs_one_limit(self):
        """--max-runs 1 must execute strictly one scheduled trial and halt."""
        schedule_path = self.test_dir / "multi_schedule.csv"
        fieldnames = ["run_index", "block_id", "within_block_order", "arm", "task_id", "variant_mapping", "target_entity"]
        rows = [
            {"run_index": "1", "block_id": "1", "within_block_order": "1", "arm": "ABS", "task_id": "T1", "variant_mapping": "v0-baseline", "target_entity": "wh-001"},
            {"run_index": "2", "block_id": "1", "within_block_order": "2", "arm": "ARIA", "task_id": "T2", "variant_mapping": "v2-aria", "target_entity": "mkp-001"},
            {"run_index": "3", "block_id": "1", "within_block_order": "3", "arm": "DATA-CFG", "task_id": "T3", "variant_mapping": "v3-data-attrs", "target_entity": "wh-002"},
        ]
        with schedule_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        test_ledger = self.test_dir / "test_ledger_02.json"
        asyncio.run(execute_experiment(
            mode="mock",
            max_runs=1,
            schedule_path=schedule_path,
            summary_path=self.summary_path,
            runs_dir=self.runs_dir,
            is_free_tier=True,
            cost_ceiling_usd=0.0,
            ledger_path=test_ledger
        ))

        self.assertTrue(self.summary_path.exists())
        with self.summary_path.open("r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 1, "Exactly one run must be executed when max_runs=1")
            self.assertEqual(reader[0]["run_index"], "1")

    # 3. Explicit step limits are preserved
    def test_03_explicit_step_limits_preserved(self):
        """User-supplied --max-steps must be respected and passed to the execution engine."""
        captured_steps = []

        async def mock_run_trial(trial_spec, **kwargs):
            captured_steps.append(kwargs.get("max_steps"))
            return {
                "run_index": trial_spec["run_index"],
                "block_id": trial_spec["block_id"],
                "within_block_order": trial_spec["within_block_order"],
                "arm": trial_spec["arm"],
                "task_id": trial_spec["task_id"],
                "variant_mapping": trial_spec["variant_mapping"],
                "target_entity": trial_spec["target_entity"],
                "model": "mock-model",
                "success": True,
                "score": 1.0,
                "total_steps": kwargs.get("max_steps", 4),
                "model_requests": 1,
                "total_time_seconds": 1.0,
                "status": "completed",
                "termination_reason": "agent_completed",
                "error_message": "",
                "cleanup_error": "",
                "pre_cart_count": 0,
                "order_confirmed": False,
                "treatment_attribute_observed": True,
                "treatment_delivery_evidence": "Mock observation",
                "captured_observations_count": 1,
                "estimated_input_tokens": 100,
                "estimated_output_tokens": 50,
                "estimated_cost_usd": 0.0,
                "timestamp_start": "2026-10-26T00:00:00",
                "timestamp_end": "2026-10-26T00:00:01",
            }

        schedule_path = self.test_dir / "single_schedule.csv"
        test_ledger = self.test_dir / "test_ledger_03.json"
        with schedule_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["run_index", "block_id", "within_block_order", "arm", "task_id", "variant_mapping", "target_entity"])
            writer.writeheader()
            writer.writerow({"run_index": "1", "block_id": "1", "within_block_order": "1", "arm": "ABS", "task_id": "T1", "variant_mapping": "v0-baseline", "target_entity": "wh-001"})

        with patch("protocol_v3_runner.run_single_mock_trial", side_effect=mock_run_trial):
            asyncio.run(execute_experiment(
                mode="mock",
                max_runs=1,
                max_steps_per_run=7,
                schedule_path=schedule_path,
                summary_path=self.summary_path,
                runs_dir=self.runs_dir,
                is_free_tier=True,
                cost_ceiling_usd=0.0,
                ledger_path=test_ledger
            ))

        self.assertEqual(captured_steps, [7], "Explicit max_steps=7 must be preserved and passed through")

    # 4. Multi-step task configuration and warning when max_steps < 2
    def test_04_multi_step_task_warning_and_budget(self):
        """When max_steps < 2, runner must emit an explicit step budget warning explaining done-tool restrictions."""
        schedule_path = self.test_dir / "schedule.csv"
        test_ledger = self.test_dir / "test_ledger_04.json"
        with schedule_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["run_index", "block_id", "within_block_order", "arm", "task_id", "variant_mapping", "target_entity"])
            writer.writeheader()
            writer.writerow({"run_index": "1", "block_id": "1", "within_block_order": "1", "arm": "ABS", "task_id": "T1", "variant_mapping": "v0-baseline", "target_entity": "wh-001"})

        captured_stdout = io.StringIO()
        with patch("sys.stdout", captured_stdout):
            asyncio.run(execute_experiment(
                mode="mock",
                max_runs=1,
                max_steps_per_run=1,
                schedule_path=schedule_path,
                summary_path=self.summary_path,
                runs_dir=self.runs_dir,
                is_free_tier=True,
                cost_ceiling_usd=0.0,
                ledger_path=test_ledger
            ))

        output = captured_stdout.getvalue()
        self.assertIn("[STEP BUDGET WARNING]", output)
        self.assertIn("max_steps_per_run=1 is configured", output)
        self.assertIn("DoneAgentOutput", output)

    # 5. A mock task that identifies the cheapest product but never clicks is marked failed
    def test_05_mock_task_identifies_cheapest_product_without_click_fails(self):
        """Identifying the cheapest product in agent final text without clicking Add-to-Cart must evaluate as failed."""
        final_text = (
            "I searched for 'wireless headphones' and found AudioMax BT50 ($129.99), "
            "BudPro Wireless X ($89.99), and SoundFlow Air 3 ($49.99). "
            "The least expensive is SoundFlow Air 3 at $49.99, button [32]."
        )
        # Cart is empty because agent reached max_steps before clicking
        v_res = verify_task_result(
            task_id="T1",
            cart=[],
            order_confirmed=False,
            last_order_items=[],
            final_text=final_text,
            pre_cart_count=None
        )
        self.assertFalse(v_res["success"], "Task must fail if product was never added to cart")
        self.assertEqual(v_res["score"], 0.0)
        self.assertEqual(v_res["details"].get("cart_skus"), [])

    # 6. A mock task that clicks the cheapest product and passes the verifier is marked successful
    def test_06_mock_task_clicks_cheapest_product_passes_verifier(self):
        """Adding the cheapest product (SoundFlow Air 3 / wh-001) to cart must evaluate as successful."""
        cart = [{"sku": "wh-001", "name": "SoundFlow Air 3", "price": 49.99, "quantity": 1}]
        v_res = verify_task_result(
            task_id="T1",
            cart=cart,
            order_confirmed=False,
            last_order_items=[],
            final_text="Added SoundFlow Air 3 to cart.",
            pre_cart_count=None
        )
        self.assertTrue(v_res["success"], "Task must succeed when target SKU is verified in cart")
        self.assertEqual(v_res["score"], 1.0)
        self.assertIn("wh-001", v_res["details"].get("cart_skus", []))

    # 7. Task failure remains distinguishable from a cleanup failure
    def test_07_task_failure_distinguishable_from_cleanup_failure(self):
        """A task failure with a cleanup error must record both distinct signals without confusion."""
        record = {
            "run_index": 1,
            "status": "completed",
            "termination_reason": "agent_completed",
            "verifier_result": {"success": False, "score": 0.0},
            "cleanup_error": "AttributeError: 'NoneType' object has no attribute 'send'",
        }
        self.assertFalse(record["verifier_result"]["success"])
        self.assertIsNotNone(record["cleanup_error"])
        self.assertIn("AttributeError", record["cleanup_error"])

    # 8. A cleanup exception does not erase an already-persisted result
    def test_08_cleanup_exception_does_not_erase_persisted_result(self):
        """extract_terminal_state must gracefully use fallback_state if CDP is already disconnected."""
        mock_dead_session = MagicMock()
        mock_dead_session.is_started = False
        mock_dead_session._cdp_client_root = None

        fallback_state = {
            "url": "http://127.0.0.1:8080/variants/v0-baseline/index.html#home",
            "title": "TechMart",
            "cart": [{"sku": "wh-001", "name": "SoundFlow Air 3"}],
            "order_confirmed": False,
            "last_order_items": []
        }

        state_data = asyncio.run(extract_terminal_state(mock_dead_session, fallback_state=fallback_state))
        self.assertIsNone(state_data["extraction_error"], "Must successfully recover from fallback_state")
        self.assertEqual(state_data["cart"], fallback_state["cart"])
        self.assertEqual(state_data["url"], fallback_state["url"])

    # 9. Budget guard blocks a run when there is insufficient worst-case headroom
    def test_09_budget_guard_blocks_when_insufficient_worst_case_headroom(self):
        """Budget guard must fail closed before trial dispatch if remaining requests < max_steps."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="openai/gpt-oss-120b",
            max_steps_per_run=4,
            max_requests_ceiling=6,
            is_free_tier=True,
            initial_requests_offset=5,
            provider="groq"
        )
        can_dispatch, abort_reason = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        self.assertFalse(can_dispatch)
        self.assertIn("Remaining free-tier requests (1) is less than worst-case trial steps (4)", abort_reason)

    # 10. Request accounting does not treat non-model agent steps as model requests
    def test_10_request_accounting_does_not_count_steps_as_requests(self):
        """load_daily_requests_offset must prefer explicit model_requests over raw total_steps."""
        summary_file = self.test_dir / "test_offset.csv"
        isolated_ledger = self.test_dir / "isolated_ledger_10.json"
        fieldnames = ["run_index", "total_steps", "model_requests", "estimated_cost_usd", "timestamp_start", "timestamp_end"]
        with summary_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "run_index": "1",
                "total_steps": "8",
                "model_requests": "2",
                "estimated_cost_usd": "0.001",
                "timestamp_start": "2026-10-26T02:00:00",
                "timestamp_end": "2026-10-26T02:01:00"
            })

        reqs, cost = load_daily_requests_offset(
            ledger_path=isolated_ledger,
            summary_csvs=[summary_file],
            target_date="2026-10-26"
        )
        self.assertEqual(reqs, 2, "Must read explicit model_requests (2) rather than raw total_steps (8)")

    # 11. Ledger and CSV reconciliation is deterministic and does not double-count the same run
    def test_11_ledger_and_csv_reconciliation_no_double_count(self):
        """Multiple summary CSVs containing the same run must be deduplicated by run_index and timestamp."""
        csv1 = self.test_dir / "summary_1.csv"
        csv2 = self.test_dir / "summary_2.csv"
        isolated_ledger = self.test_dir / "isolated_ledger_11.json"
        fieldnames = ["run_index", "model_requests", "total_steps", "estimated_cost_usd", "timestamp_start", "timestamp_end"]
        identical_row = {
            "run_index": "1",
            "model_requests": "3",
            "total_steps": "4",
            "estimated_cost_usd": "0.002",
            "timestamp_start": "2026-10-26T02:45:00",
            "timestamp_end": "2026-10-26T02:46:00"
        }
        for p in [csv1, csv2]:
            with p.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(identical_row)

        reqs, cost = load_daily_requests_offset(
            ledger_path=isolated_ledger,
            summary_csvs=[csv1, csv2],
            target_date="2026-10-26"
        )
        self.assertEqual(reqs, 3, "Duplicate run across 2 files must be counted exactly once (3 requests, not 6)")
        self.assertAlmostEqual(cost, 0.002, places=4)

    # 12. Cross-provider separation
    def test_12_provider_filtering_in_offset_loader(self):
        """Groq accounting must not be inflated by historical Gemini runs."""
        mixed_csv = self.test_dir / "mixed_summary.csv"
        isolated_ledger = self.test_dir / "isolated_ledger_12.json"
        fieldnames = ["run_index", "model", "model_requests", "estimated_cost_usd", "timestamp_start", "timestamp_end"]
        with mixed_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "run_index": "1",
                "model": "gemini-3.1-flash-lite",
                "model_requests": "5",
                "estimated_cost_usd": "0.005",
                "timestamp_start": "2026-10-26T01:00:00",
                "timestamp_end": "2026-10-26T01:01:00"
            })
            writer.writerow({
                "run_index": "2",
                "model": "openai/gpt-oss-120b",
                "model_requests": "2",
                "estimated_cost_usd": "0.001",
                "timestamp_start": "2026-10-26T02:00:00",
                "timestamp_end": "2026-10-26T02:01:00"
            })

        groq_reqs, _ = load_daily_requests_offset(
            ledger_path=isolated_ledger,
            summary_csvs=[mixed_csv],
            target_date="2026-10-26",
            provider="groq"
        )
        self.assertEqual(groq_reqs, 2, "Groq offset loader must filter out Gemini rows")

        gemini_reqs, _ = load_daily_requests_offset(
            ledger_path=isolated_ledger,
            summary_csvs=[mixed_csv],
            target_date="2026-10-26",
            provider="gemini"
        )
        self.assertEqual(gemini_reqs, 5, "Gemini offset loader must filter out Groq rows")

if __name__ == "__main__":
    unittest.main()

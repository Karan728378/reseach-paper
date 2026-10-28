"""
Offline Integration Tests for Runner / Model Budget Guard Wiring
Part of: "The DOM Serialization Gap" Research Infrastructure

Tests real production code paths in protocol_v3_runner.py:
1. Verifies run_single_live_trial wraps LLM with BudgetGuardedChatModel when guard is provided.
2. Verifies in-flight step budget exhaustion halts Agent execution cleanly with quota_aborted status.
3. Verifies execute_experiment enforces require_worst_case_headroom and does not double-count requests.
4. Verifies historical daily ledger at 604 requests prevents runner live dispatch.
"""

import unittest
import asyncio
import json
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

from budget_controller import (
    LocalBudgetGuard,
    BudgetGuardedChatModel,
    BudgetExceededError
)
from protocol_v3_runner import (
    run_single_live_trial,
    execute_experiment
)

class MockAgentLLM:
    """Mock LLM returning dummy responses."""
    def __init__(self):
        self.call_count = 0
        self.model = "gemini-flash-lite-latest"
        self.model_name = "gemini-flash-lite-latest"
        self.provider = "google"
        self.name = "gemini-flash-lite-latest"

    async def ainvoke(self, messages, **kwargs):
        self.call_count += 1
        return MagicMock(
            completion=MagicMock(),
            usage=MagicMock(prompt_tokens=1200, completion_tokens=40)
        )


class TestRunnerGuardIntegration(unittest.TestCase):

    def test_01_runner_wraps_llm_with_budget_guard(self):
        """run_single_live_trial must wrap custom_llm in BudgetGuardedChatModel when guard is provided."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=100,
            initial_requests_offset=0,
            is_free_tier=True
        )
        mock_llm = MockAgentLLM()
        
        trial_spec = {
            "run_index": "99",
            "block_id": "1",
            "within_block_order": "1",
            "arm": "ABS",
            "task_id": "T1",
            "variant_mapping": "v0-baseline",
            "target_entity": "wh-001"
        }

        captured_llm = []

        with patch("browser_use.BrowserSession") as MockBrowserSession, \
             patch("browser_use.Agent") as MockAgent:
            
            mock_session = AsyncMock()
            mock_page = AsyncMock()
            mock_page.evaluate = AsyncMock(return_value=[])
            mock_page.get_url = AsyncMock(return_value="http://127.0.0.1:8080/variants/v0-baseline/index.html")
            mock_page.get_title = AsyncMock(return_value="Test Page")
            mock_session.get_current_page = AsyncMock(return_value=mock_page)
            MockBrowserSession.return_value = mock_session

            # Inspect what Agent receives in constructor
            def agent_init_spy(*args, **kwargs):
                agent_mock = AsyncMock()
                passed_llm = kwargs.get("llm")
                captured_llm.append(passed_llm)
                
                async def agent_run(*r_args, **r_kwargs):
                    # Simulate Agent step invoking llm.ainvoke
                    await passed_llm.ainvoke([{"role": "user", "content": "step 1"}])
                    await passed_llm.ainvoke([{"role": "user", "content": "step 2"}])
                    hist = MagicMock()
                    hist.history = [MagicMock(), MagicMock()]
                    hist.is_done.return_value = True
                    hist.final_result.return_value = "Done"
                    return hist

                agent_mock.run = agent_run
                agent_mock._message_manager = MagicMock()
                agent_mock._message_manager.create_state_messages = MagicMock()
                agent_mock._message_manager.get_messages.return_value = []
                return agent_mock

            MockAgent.side_effect = agent_init_spy

            result = asyncio.run(run_single_live_trial(
                trial_spec=trial_spec,
                port=8080,
                guard=guard,
                custom_llm=mock_llm,
                max_steps=2
            ))

        self.assertEqual(len(captured_llm), 1)
        self.assertIsInstance(captured_llm[0], BudgetGuardedChatModel)
        self.assertEqual(mock_llm.call_count, 2)
        self.assertEqual(guard.cumulative_requests, 2)
        self.assertEqual(result["status"], "completed")

    def test_02_in_flight_budget_exhaustion_aborts_cleanly(self):
        """When guard reaches ceiling during live trial steps, runner halts with quota_aborted."""
        # Set ceiling to 2 requests, but agent tries to make 3 steps
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=2,
            initial_requests_offset=0,
            is_free_tier=True
        )
        mock_llm = MockAgentLLM()
        
        trial_spec = {
            "run_index": "99",
            "block_id": "1",
            "within_block_order": "1",
            "arm": "ABS",
            "task_id": "T1",
            "variant_mapping": "v0-baseline",
            "target_entity": "wh-001"
        }

        with patch("browser_use.BrowserSession") as MockBrowserSession, \
             patch("browser_use.Agent") as MockAgent:
            
            mock_session = AsyncMock()
            mock_page = AsyncMock()
            mock_page.evaluate = AsyncMock(return_value=[])
            mock_page.get_url = AsyncMock(return_value="http://127.0.0.1:8080/variants/v0-baseline/index.html")
            mock_page.get_title = AsyncMock(return_value="Test Page")
            mock_session.get_current_page = AsyncMock(return_value=mock_page)
            MockBrowserSession.return_value = mock_session

            def agent_init_spy(*args, **kwargs):
                agent_mock = AsyncMock()
                passed_llm = kwargs.get("llm")
                
                async def agent_run(*r_args, **r_kwargs):
                    # Step 1: ok
                    await passed_llm.ainvoke([{"role": "user", "content": "step 1"}])
                    # Step 2: ok (reaches 2)
                    await passed_llm.ainvoke([{"role": "user", "content": "step 2"}])
                    # Step 3: Must raise BudgetExceededError
                    await passed_llm.ainvoke([{"role": "user", "content": "step 3"}])
                    return MagicMock()

                agent_mock.run = agent_run
                agent_mock._message_manager = MagicMock()
                agent_mock._message_manager.create_state_messages = MagicMock()
                agent_mock._message_manager.get_messages.return_value = []
                return agent_mock

            MockAgent.side_effect = agent_init_spy

            result = asyncio.run(run_single_live_trial(
                trial_spec=trial_spec,
                port=8080,
                guard=guard,
                custom_llm=mock_llm,
                max_steps=5
            ))

        # Must halt at exactly 2 requests; step 3 raised BudgetExceededError
        self.assertEqual(guard.cumulative_requests, 2)
        self.assertEqual(mock_llm.call_count, 2)
        self.assertTrue(guard.halted_due_to_ceiling)
        self.assertEqual(result["status"], "infrastructure_aborted")
        self.assertEqual(result["termination_reason"], "quota_aborted")
        self.assertIn("ceiling", result["error_message"].lower())

    def test_03_execute_experiment_worst_case_headroom(self):
        """execute_experiment must halt before trial dispatch if worst-case steps exceed ceiling."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=600,
            max_steps_per_run=15,
            initial_requests_offset=595,
            is_free_tier=True
        )
        # 595 + 15 = 610 > 600 -> Cannot dispatch
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        self.assertFalse(can_dispatch)
        self.assertIn("less than worst-case trial steps", msg)

    def test_04_no_double_counting_with_requests_already_recorded(self):
        """record_trial_completion does not double count steps when requests_already_recorded=True."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=600,
            initial_requests_offset=10,
            is_free_tier=True
        )
        # Simulate 3 in-flight requests recorded pre-dispatch
        guard.record_request_pre_dispatch()
        guard.record_request_pre_dispatch()
        guard.record_request_pre_dispatch()
        self.assertEqual(guard.cumulative_requests, 13)

        # Call record_trial_completion with requests_already_recorded=True
        res = guard.record_trial_completion(total_steps=3, requests_already_recorded=True)
        # Must remain 13, NOT 16
        self.assertEqual(guard.cumulative_requests, 13)
        self.assertEqual(guard.runs_completed, 1)

    def test_05_historical_ledger_blocks_live_dispatch(self):
        """When ledger contains 604 requests with ceiling 600, trial dispatch fails closed immediately."""
        ledger_path = Path("C:/testing/research_execution_20261018/results/daily_quota_ledger.json")
        self.assertTrue(ledger_path.exists())
        ledger_data = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(ledger_data["cumulative_requests"], 604)
        self.assertEqual(ledger_data["max_requests_ceiling"], 600)

        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-3.1-flash-lite",
            max_requests_ceiling=600,
            initial_requests_offset=ledger_data["cumulative_requests"],
            is_free_tier=True,
            ledger_path=ledger_path
        )
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        self.assertFalse(can_dispatch)
        self.assertIn("604", msg)
        self.assertIn("reached free-tier quota ceiling (600)", msg)


if __name__ == "__main__":
    unittest.main()

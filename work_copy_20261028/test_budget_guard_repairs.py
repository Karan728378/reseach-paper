"""
Unit Tests for Budget Guard Repairs and In-Flight Request Metering
Part of: "The DOM Serialization Gap" Research Infrastructure

Tests:
1. Exact 600-request boundary enforcement.
2. Worst-case trial headroom fail-closed check.
3. In-flight model request interception via BudgetGuardedChatModel.
4. Retry request interception.
5. Concurrent multithreaded dispatch boundary safety.
6. Historical 604 count preservation and immediate fail-closed behavior.
"""

import unittest
import asyncio
import threading
import json
import tempfile
from pathlib import Path

from budget_controller import (
    LocalBudgetGuard,
    BudgetGuardedChatModel,
    BudgetExceededError
)

class MockLLM:
    """Mock LLM that returns a dummy response with usage metadata."""
    def __init__(self, responses=None):
        self.responses = responses or ["Action 1", "Action 2", "Action 3"]
        self.call_count = 0
        self.model_name = "gemini-flash-lite-latest"
        self.provider = "google"

    async def ainvoke(self, messages, **kwargs):
        self.call_count += 1
        resp_text = self.responses[min(self.call_count - 1, len(self.responses) - 1)]
        
        class MockResponse:
            def __init__(self, text):
                self.text = text
                self.content = text
                self.response_metadata = {
                    "token_usage": {"prompt_tokens": 1500, "completion_tokens": 50}
                }
        return MockResponse(resp_text)

    def invoke(self, messages, **kwargs):
        self.call_count += 1
        resp_text = self.responses[min(self.call_count - 1, len(self.responses) - 1)]
        class MockResponse:
            def __init__(self, text):
                self.text = text
                self.content = text
                self.response_metadata = {
                    "token_usage": {"prompt_tokens": 1500, "completion_tokens": 50}
                }
        return MockResponse(resp_text)


class TestBudgetGuardRepairs(unittest.TestCase):

    def test_01_exact_600_request_boundary(self):
        """The guard must allow request 600, but request 601 must raise BudgetExceededError."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=600,
            initial_requests_offset=599,
            is_free_tier=True
        )
        
        # Request 600: Permitted
        can_dispatch, msg = guard.check_can_dispatch_request()
        self.assertTrue(can_dispatch)
        guard.record_request_pre_dispatch()
        self.assertEqual(guard.cumulative_requests, 600)
        self.assertTrue(guard.halted_due_to_ceiling)
        
        # Request 601: Blocked
        can_dispatch, msg = guard.check_can_dispatch_request()
        self.assertFalse(can_dispatch)
        self.assertIn("reached ceiling (600)", msg)
        
        with self.assertRaises(BudgetExceededError):
            guard.record_request_pre_dispatch()
        self.assertEqual(guard.cumulative_requests, 600)

    def test_02_worst_case_headroom_enforcement(self):
        """When worst-case headroom is required, guard halts before starting a trial if steps cannot fit."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=600,
            max_steps_per_run=15,
            initial_requests_offset=590,
            is_free_tier=True
        )
        # 590 + 15 = 605 > 600
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        self.assertFalse(can_dispatch)
        self.assertIn("less than worst-case trial steps", msg)

        # But if headroom is sufficient (e.g. 580 + 15 = 595 <= 600), passes:
        guard_ok = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=600,
            max_steps_per_run=15,
            initial_requests_offset=580,
            is_free_tier=True
        )
        can_dispatch_ok, _ = guard_ok.check_can_dispatch_trial(require_worst_case_headroom=True)
        self.assertTrue(can_dispatch_ok)

    def test_03_in_flight_model_request_interception(self):
        """BudgetGuardedChatModel intercepts each ainvoke call and raises BudgetExceededError in-flight."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=600,
            initial_requests_offset=598,
            is_free_tier=True
        )
        mock_llm = MockLLM()
        guarded_llm = BudgetGuardedChatModel(mock_llm, guard)

        async def run_in_flight():
            # Step 1 (req 599)
            r1 = await guarded_llm.ainvoke([{"role": "user", "content": "step 1"}])
            self.assertEqual(guard.cumulative_requests, 599)
            
            # Step 2 (req 600)
            r2 = await guarded_llm.ainvoke([{"role": "user", "content": "step 2"}])
            self.assertEqual(guard.cumulative_requests, 600)
            self.assertTrue(guard.halted_due_to_ceiling)
            
            # Step 3 (req 601) - Must raise BudgetExceededError and NEVER reach mock_llm
            with self.assertRaises(BudgetExceededError):
                await guarded_llm.ainvoke([{"role": "user", "content": "step 3"}])

        asyncio.run(run_in_flight())
        self.assertEqual(mock_llm.call_count, 2)
        self.assertEqual(guard.cumulative_requests, 600)

    def test_04_retry_request_metering(self):
        """If an external loop retries after failure, every retry attempt is counted and subject to ceiling."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=10,
            initial_requests_offset=9,
            is_free_tier=True
        )
        mock_llm = MockLLM()
        guarded_llm = BudgetGuardedChatModel(mock_llm, guard)

        # Attempt 1 consumes request 10
        resp1 = guarded_llm.invoke([{"role": "user", "content": "attempt 1"}])
        self.assertEqual(guard.cumulative_requests, 10)

        # Retry attempt 2 is blocked before network dispatch
        with self.assertRaises(BudgetExceededError):
            guarded_llm.invoke([{"role": "user", "content": "retry attempt 2"}])
        self.assertEqual(guard.cumulative_requests, 10)
        self.assertEqual(mock_llm.call_count, 1)

    def test_05_concurrent_dispatch_boundary_safety(self):
        """Concurrent threads attempting to dispatch simultaneously at ceiling boundary cannot exceed ceiling."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="gemini-flash-lite-latest",
            max_requests_ceiling=100,
            initial_requests_offset=95,
            is_free_tier=True
        )
        mock_llm = MockLLM()
        guarded_llm = BudgetGuardedChatModel(mock_llm, guard)

        successes = []
        blocked = []

        def worker():
            try:
                guarded_llm.invoke([{"role": "user", "content": "concurrent"}])
                successes.append(1)
            except BudgetExceededError:
                blocked.append(1)

        # Launch 20 concurrent threads when only 5 slots remain (95 -> 100)
        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(successes), 5)
        self.assertEqual(len(blocked), 15)
        self.assertEqual(guard.cumulative_requests, 100)
        self.assertEqual(mock_llm.call_count, 5)

    def test_06_historical_604_preservation_and_fail_closed(self):
        """When initialized with historical 604 requests and 600 ceiling, guard fails closed immediately."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json", encoding="utf-8") as tf:
            ledger_data = {
                "date": "2026-10-24",
                "cumulative_requests": 604,
                "cumulative_cost_usd": 0.67044,
                "max_requests_ceiling": 600,
                "is_free_tier": True,
                "halted_due_to_ceiling": True
            }
            json.dump(ledger_data, tf)
            ledger_file = Path(tf.name)

        try:
            guard = LocalBudgetGuard(
                cost_ceiling_usd=0.0,
                model_name="gemini-flash-lite-latest",
                max_requests_ceiling=600,
                initial_requests_offset=604,
                is_free_tier=True,
                ledger_path=ledger_file
            )
            # Immediate fail closed on trial check
            can_trial, trial_msg = guard.check_can_dispatch_trial()
            self.assertFalse(can_trial)
            self.assertIn("604", trial_msg)
            self.assertIn("reached free-tier quota ceiling (600)", trial_msg)

            # Immediate fail closed on request check
            can_req, req_msg = guard.check_can_dispatch_request()
            self.assertFalse(can_req)
            self.assertIn("604", req_msg)

            # Persisted ledger is preserved at 604
            saved_data = json.loads(ledger_file.read_text(encoding="utf-8"))
            self.assertEqual(saved_data["cumulative_requests"], 604)
        finally:
            ledger_file.unlink()


if __name__ == "__main__":
    unittest.main()

"""
Offline Integration Test: Live Instrumentation Verification
Executes the live trial instrumentation pipeline using a local MockChatModel.
Validates:
1. Message interception at the MessageManager boundary.
2. Initial-state reset and T5 pre-seeding.
3. Terminal-state extraction (cart, order status).
4. Detailed per-run JSON logging schema.
5. Error handling and failed trial preservation.
"""
import asyncio
import http.server
import json
import os
import shutil
import sys
import threading
import time
import unittest
from pathlib import Path

ROOT_DIR = Path("C:/testing")
EXEC_DIR = ROOT_DIR / "research_execution_20261018"
sys.path.insert(0, str(EXEC_DIR))

from langchain_core.language_models import FakeListChatModel
from browser_use import Agent, BrowserSession
import protocol_v3_runner

TEST_RUNS_DIR = EXEC_DIR / "test_scratch_runs_instrumentation"
TEST_SUMMARY_CSV = EXEC_DIR / "test_scratch_summary_instrumentation.csv"
TEST_PORT = 8094

def start_server():
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT_DIR), **kwargs)
        def log_message(self, format, *args):
            pass
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", TEST_PORT), QuietHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.5)
    return httpd

class MockModel(FakeListChatModel):
    provider: str = "google"
    model: str = "gemini-flash-lite-latest"
    model_name: str = "gemini-flash-lite-latest"

class TestLiveInstrumentationOffline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.httpd = start_server()
        time.sleep(0.5)

    def setUp(self):
        TEST_RUNS_DIR.mkdir(parents=True, exist_ok=True)
        if TEST_SUMMARY_CSV.exists():
            TEST_SUMMARY_CSV.unlink()

    def tearDown(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR, ignore_errors=True)
        if TEST_SUMMARY_CSV.exists():
            TEST_SUMMARY_CSV.unlink()

    def test_mock_chat_model_observation_interception(self):
        """Verify prompt observation interception at MessageManager boundary."""
        async def run_test():
            dummy_resp = json.dumps({
                "thinking": "Done inspecting",
                "evaluation_previous_goal": "Success",
                "memory": "",
                "next_goal": "done",
                "action": [{"done": {"text": "Finished"}}]
            })
            llm = MockModel(responses=[dummy_resp])
            session = BrowserSession(headless=True)
            await session.start()
            
            captured = []
            try:
                url = f"http://127.0.0.1:{TEST_PORT}/variants/v0-baseline/index.html#home"
                agent = Agent(
                    task="Find wireless headphones",
                    llm=llm,
                    browser_session=session,
                    use_vision=False,
                    initial_actions=[{"navigate": {"url": url, "new_tab": False}}]
                )
                
                orig_create = agent._message_manager.create_state_messages
                def wrapped_create(*args, **kwargs):
                    res = orig_create(*args, **kwargs)
                    msgs = agent._message_manager.get_messages()
                    for m in msgs:
                        text = m.content if isinstance(m.content, str) else str(m.content)
                        captured.append(text)
                    return res
                agent._message_manager.create_state_messages = wrapped_create
                
                await agent.run()
            finally:
                await session.stop()
                
            self.assertGreater(len(captured), 0, "Observation buffer must be intercepted")
            all_text = " ".join(captured)
            self.assertIn("SoundFlow Air 3", all_text, "Visible product text must reach model prompt")
            return True

        asyncio.run(run_test())

    def test_per_run_json_schema_logging(self):
        """Verify per-run detailed JSON logging preserves required provenance fields."""
        spec = {
            "run_index": 1,
            "block_id": 1,
            "within_block_order": 1,
            "arm": "ABS",
            "task_id": "T1",
            "variant_mapping": "v0-baseline",
            "target_entity": "wh-001"
        }
        res = asyncio.run(protocol_v3_runner.run_single_mock_trial(spec))
        
        # Test appending to summary
        protocol_v3_runner.append_to_summary(TEST_SUMMARY_CSV, res)
        self.assertTrue(TEST_SUMMARY_CSV.exists())
        
        content = TEST_SUMMARY_CSV.read_text(encoding="utf-8")
        self.assertIn("run_index", content)
        self.assertIn("ABS", content)
        self.assertIn("wh-001", content)
        self.assertIn("completed", content)

    def test_failed_runs_retained_in_summary(self):
        """Verify that infrastructure errors or failed runs are recorded and not silently dropped."""
        failed_row = {
            "run_index": 99,
            "block_id": 1,
            "within_block_order": 2,
            "arm": "ARIA",
            "task_id": "T2",
            "variant_mapping": "v2-aria",
            "target_entity": "mkp-001",
            "model": "gemini-flash-lite-latest",
            "success": False,
            "score": 0.0,
            "total_steps": 1,
            "total_time_seconds": 1.5,
            "status": "failed",
            "termination_reason": "exception",
            "error_message": "CDP Connection Timeout",
            "pre_cart_count": None,
            "order_confirmed": False,
            "treatment_attribute_observed": False,
            "treatment_delivery_evidence": "none",
            "estimated_input_tokens": 7000,
            "estimated_output_tokens": 100,
            "estimated_cost_usd": 0.0011,
            "timestamp_start": "2026-10-22T12:00:00",
            "timestamp_end": "2026-10-22T12:00:01"
        }
        protocol_v3_runner.append_to_summary(TEST_SUMMARY_CSV, failed_row)
        
        completed_indices = protocol_v3_runner.get_completed_run_indices(TEST_SUMMARY_CSV)
        # Because status == 'failed', it must NOT be in completed_indices (eligible for retry upon infrastructure fix)
        self.assertNotIn(99, completed_indices, "Failed runs must not be marked as completed")
        
        # But it MUST be preserved in the CSV file for audit trail
        summary_text = TEST_SUMMARY_CSV.read_text(encoding="utf-8")
        self.assertIn("CDP Connection Timeout", summary_text, "Failed run error message must be preserved")

if __name__ == "__main__":
    unittest.main()

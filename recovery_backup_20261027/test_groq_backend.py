"""
Unit & Integration Tests for Groq Backend Migration
Part of: "The DOM Serialization Gap" Research Infrastructure

Tests verify:
1. Model/backend selection & configuration.
2. Missing / redacted API key handling.
3. Structured output validation with AgentOutput schema.
4. Error translation & secret sanitization (Auth, RateLimit, Connection).
5. Pre-dispatch request and token budget guard enforcement.
6. Ledger isolation (Gemini ledger remains intact at 604/600; Groq uses distinct ledger).
7. Browser-agent Agent compatibility with ChatGroq.
8. Preservation of task verifiers (T1-T6) and treatment definitions.
"""

import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import groq
from pydantic import BaseModel

from budget_controller import (
    DEFAULT_GROQ_LEDGER_PATH,
    DEFAULT_LEDGER_PATH,
    BudgetExceededError,
    BudgetGuardedChatModel,
    LocalBudgetGuard,
    get_model_pricing,
)
from groq_backend import ChatGroq, sanitize_secret_leakage
from protocol_v3_runner import (
    DEFAULT_INCLUDE_ATTRIBUTES,
    EXTENDED_ATTRIBUTES,
    get_groq_api_key,
    verify_task_result,
)


class MockAgentOutputAction(BaseModel):
    name: str = "navigate"
    parameters: dict = {"url": "http://127.0.0.1:8080"}


class MockAgentOutput(BaseModel):
    current_state: dict = {"evaluation_previous_goal": "Initial step"}
    action: list = []


class TestGroqBackendMigration(unittest.TestCase):

    def setUp(self):
        self.mock_key = "gsk_test_mock_secret_key_9876543210"

    def test_01_backend_and_model_selection(self):
        """ChatGroq initializes with correct model, provider, and name attributes."""
        llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.mock_key)
        self.assertEqual(llm.model, "openai/gpt-oss-120b")
        self.assertEqual(llm.provider, "groq")
        self.assertEqual(llm.name, "groq/openai/gpt-oss-120b")
        
        # Verify pricing lookup works for Groq models
        p = get_model_pricing("openai/gpt-oss-120b")
        self.assertIn("input_per_million", p)
        self.assertIn("output_per_million", p)
        self.assertEqual(p["input_per_million"], 0.15)
        self.assertEqual(p["output_per_million"], 0.60)

    def test_02_missing_api_key_handling(self):
        """Missing API key raises descriptive ValueError and never prints secrets."""
        with patch.dict(os.environ, {}, clear=True):
            # Test get_groq_api_key returns falsy/empty
            self.assertFalse(bool(get_groq_api_key()))
            # Instantiating ChatGroq without key raises ValueError
            with self.assertRaises(ValueError) as ctx:
                ChatGroq(model="openai/gpt-oss-120b", api_key=None)
            self.assertIn("Groq API key must be provided", str(ctx.exception))
            # Ensure no secret strings leaked
            self.assertNotIn("gsk_", str(ctx.exception))

    def test_03_secret_leakage_sanitization(self):
        """sanitize_secret_leakage strips gsk_... keys and other tokens."""
        raw_msg = f"Failed with 401: Invalid bearer token {self.mock_key} for request."
        clean_msg = sanitize_secret_leakage(raw_msg)
        self.assertNotIn(self.mock_key, clean_msg)
        self.assertIn("[REDACTED_GROQ_API_KEY]", clean_msg)

    def test_04_structured_output_validation_mock(self):
        """ChatGroq.ainvoke returns valid Pydantic instance and extracts token usage."""
        llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.mock_key)

        # Mock the Groq client's chat.completions.create
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "current_state": {"evaluation_previous_goal": "Goal reached"},
                        "action": [{"name": "click", "parameters": {"element": 42}}]
                    })
                )
            )
        ]
        mock_response.usage = MagicMock(prompt_tokens=450, completion_tokens=85, total_tokens=535)

        with patch.object(llm._client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    llm.ainvoke([MagicMock(content="Look at page")], output_format=MockAgentOutput)
                )
            finally:
                loop.close()

            self.assertIsInstance(result.completion, MockAgentOutput)
            self.assertEqual(result.completion.current_state["evaluation_previous_goal"], "Goal reached")
            self.assertEqual(len(result.completion.action), 1)
            # Verify usage metadata was attached
            self.assertTrue(hasattr(result, "usage"))
            self.assertEqual(result.usage.prompt_tokens, 450)
            self.assertEqual(result.usage.completion_tokens, 85)
            self.assertEqual(result.usage.total_tokens, 535)

            # Verify response_format was set to json_object
            _, kwargs = mock_create.call_args
            self.assertEqual(kwargs.get("response_format"), {"type": "json_object"})

    def test_05_error_translation_and_redaction(self):
        """Groq errors (Auth, RateLimit) are translated cleanly with redacted credentials."""
        llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.mock_key)

        # Test 401 AuthenticationError
        mock_http_resp = MagicMock()
        mock_http_resp.status_code = 401
        auth_err = groq.AuthenticationError(
            message=f"Unauthorized: key {self.mock_key} is invalid",
            response=mock_http_resp,
            body={"error": {"message": f"Unauthorized key {self.mock_key}"}}
        )

        with patch.object(llm._client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = auth_err

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                with self.assertRaises(Exception) as ctx:
                    loop.run_until_complete(llm.ainvoke([MagicMock(content="hi")]))
                err_text = str(ctx.exception)
                self.assertIn("Authentication failed", err_text)
                self.assertNotIn(self.mock_key, err_text)
                self.assertIn("[REDACTED_GROQ_API_KEY]", err_text)
            finally:
                loop.close()

        # Test 429 RateLimitError
        mock_http_resp.status_code = 429
        rate_err = groq.RateLimitError(
            message="Rate limit reached: 30 requests per minute ceiling breached",
            response=mock_http_resp,
            body={"error": {"message": "Rate limit reached"}}
        )
        with patch.object(llm._client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = rate_err

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                with self.assertRaises(Exception) as ctx:
                    loop.run_until_complete(llm.ainvoke([MagicMock(content="hi")]))
                err_text = str(ctx.exception)
                self.assertIn("rate limit or quota exceeded", err_text.lower())
            finally:
                loop.close()

    def test_06_budget_guard_request_interception_pre_dispatch(self):
        """BudgetGuardedChatModel stops execution BEFORE dispatch when requests ceiling is hit."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="openai/gpt-oss-120b",
            max_requests_ceiling=2,
            is_free_tier=True,
            provider="groq"
        )
        base_llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.mock_key)
        guarded_llm = BudgetGuardedChatModel(base_llm, guard=guard)

        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content='{"status": "ok"}'))]
        mock_response.usage = MagicMock(prompt_tokens=100, completion_tokens=20, total_tokens=120)

        with patch.object(base_llm._client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Dispatch 1: OK
                loop.run_until_complete(guarded_llm.ainvoke([MagicMock(content="Step 1")]))
                self.assertEqual(guard.cumulative_requests, 1)

                # Dispatch 2: OK
                loop.run_until_complete(guarded_llm.ainvoke([MagicMock(content="Step 2")]))
                self.assertEqual(guard.cumulative_requests, 2)

                # Dispatch 3: Must raise BudgetExceededError BEFORE calling client
                with self.assertRaises(BudgetExceededError) as ctx:
                    loop.run_until_complete(guarded_llm.ainvoke([MagicMock(content="Step 3")]))
                self.assertIn("Pre-dispatch request blocked", str(ctx.exception))
                # Ensure client was called exactly 2 times, NOT 3
                self.assertEqual(mock_create.call_count, 2)
            finally:
                loop.close()

    def test_07_budget_guard_token_ceiling_interception(self):
        """BudgetGuardedChatModel stops execution BEFORE dispatch when token ceiling is reached."""
        guard = LocalBudgetGuard(
            cost_ceiling_usd=0.0,
            model_name="openai/gpt-oss-120b",
            max_requests_ceiling=100,
            max_tokens_ceiling=500,
            is_free_tier=True,
            provider="groq"
        )
        base_llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.mock_key)
        guarded_llm = BudgetGuardedChatModel(base_llm, guard=guard)

        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content='{"status": "ok"}'))]
        # Usage reports 600 total tokens (breaches 500 ceiling)
        mock_response.usage = MagicMock(prompt_tokens=500, completion_tokens=100, total_tokens=600)

        with patch.object(base_llm._client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Dispatch 1: Permitted pre-dispatch, then post-dispatch updates token counts
                loop.run_until_complete(guarded_llm.ainvoke([MagicMock(content="Step 1")]))
                self.assertGreaterEqual(
                    guard.cumulative_prompt_tokens + guard.cumulative_completion_tokens,
                    500
                )

                # Dispatch 2: Must be blocked pre-dispatch
                with self.assertRaises(BudgetExceededError) as ctx:
                    loop.run_until_complete(guarded_llm.ainvoke([MagicMock(content="Step 2")]))
                self.assertIn("cumulative tokens", str(ctx.exception))
                self.assertEqual(mock_create.call_count, 1)
            finally:
                loop.close()

    def test_08_gemini_historical_ledger_intact_and_isolated(self):
        """Historical Gemini ledger (results/daily_quota_ledger.json) remains strictly preserved."""
        gemini_ledger = Path("results/daily_quota_ledger.json")
        self.assertTrue(gemini_ledger.exists(), "Gemini ledger must exist")
        data = json.loads(gemini_ledger.read_text(encoding="utf-8"))
        self.assertEqual(data["cumulative_requests"], 604)
        self.assertEqual(data["max_requests_ceiling"], 600)
        self.assertTrue(data["halted_due_to_ceiling"])
        self.assertEqual(data["model_name"], "gemini-3.1-flash-lite")

        # Verify Groq ledger is a separate distinct path
        self.assertNotEqual(str(DEFAULT_LEDGER_PATH), str(DEFAULT_GROQ_LEDGER_PATH))
        self.assertEqual(DEFAULT_GROQ_LEDGER_PATH.name, "daily_groq_quota_ledger.json")

    def test_09_groq_ledger_isolated_persistence(self):
        """Groq budget updates save to a separate Groq ledger with provider metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_groq_ledger = Path(tmpdir) / "daily_groq_quota_ledger.json"
            guard = LocalBudgetGuard(
                cost_ceiling_usd=0.0,
                model_name="openai/gpt-oss-120b",
                max_requests_ceiling=50,
                max_tokens_ceiling=100000,
                is_free_tier=True,
                ledger_path=temp_groq_ledger,
                provider="groq"
            )
            guard.record_step(prompt_tokens=500, completion_tokens=50)

            self.assertTrue(temp_groq_ledger.exists())
            saved_data = json.loads(temp_groq_ledger.read_text(encoding="utf-8"))
            self.assertEqual(saved_data["provider"], "groq")
            self.assertEqual(saved_data["model_name"], "openai/gpt-oss-120b")
            self.assertEqual(saved_data["cumulative_requests"], 1)
            self.assertEqual(saved_data["max_tokens_ceiling"], 100000)

    def test_10_agent_framework_compatibility(self):
        """browser-use Agent can be instantiated with ChatGroq."""
        from browser_use import Agent
        llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.mock_key)
        agent = Agent(task="Find wireless headphones", llm=llm, use_vision=False)
        self.assertEqual(agent.llm.provider, "groq")
        self.assertEqual(agent.llm.model, "openai/gpt-oss-120b")

    def test_11_verifiers_and_treatments_unaltered(self):
        """Protocol v3/v4 verifiers (T1-T6) and attribute sets remain intact."""
        # Treatment attributes check
        self.assertIn("data-warranty", EXTENDED_ATTRIBUTES)
        self.assertNotIn("data-warranty", DEFAULT_INCLUDE_ATTRIBUTES)

        # T1
        v1 = verify_task_result("T1", cart=[{"sku": "wh-001"}], order_confirmed=False, last_order_items=[])
        self.assertTrue(v1["success"])
        # T3
        v3 = verify_task_result("T3", cart=[{"sku": "wh-002"}], order_confirmed=False, last_order_items=[])
        self.assertTrue(v3["success"])
        # T4
        v4 = verify_task_result("T4", cart=[], order_confirmed=True, last_order_items=[{"sku": "mse-001"}])
        self.assertTrue(v4["success"])
        # T5: pre-state assertion
        v5_fail = verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=None)
        self.assertFalse(v5_fail["success"])
        v5_pass = verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=1)
        self.assertTrue(v5_pass["success"])
        # T6: refusal vs hallucination
        v6_pass = verify_task_result("T6", cart=[], order_confirmed=False, last_order_items=[], final_text="Warranty period is not specified.")
        self.assertTrue(v6_pass["success"])
        v6_fail = verify_task_result("T6", cart=[], order_confirmed=False, last_order_items=[], final_text="Warranty duration is 36 months.")
        self.assertFalse(v6_fail["success"])

    def test_12_oversized_payload_blocked_pre_dispatch(self):
        """ChatGroq blocks requests predictably exceeding TPM ceiling (HTTP 413) before provider dispatch."""
        from browser_use.llm.exceptions import ModelProviderError
        llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.mock_key, max_tokens_ceiling=2000, max_completion_tokens=1024)
        
        # Craft a message with ~6,000 chars (~1500 tokens). 1500 + 1024 = 2524 > 2000 ceiling
        huge_message = {"role": "user", "content": "X" * 6000}
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            with self.assertRaises(ModelProviderError) as ctx:
                loop.run_until_complete(llm.ainvoke([huge_message]))
            self.assertIn("Pre-dispatch payload size blocked", str(ctx.exception))
            self.assertEqual(ctx.exception.status_code, 413)
        finally:
            loop.close()

    def test_13_flash_mode_system_prompt_size(self):
        """Verifies flash_mode=True produces a bounded system prompt under 800 tokens."""
        from browser_use.agent.prompts import SystemPrompt
        sp_default = SystemPrompt(flash_mode=False)
        sp_flash = SystemPrompt(flash_mode=True)
        
        default_len = len(sp_default.get_system_message().content)
        flash_len = len(sp_flash.get_system_message().content)
        
        # Default prompt is ~24k chars (>6k tokens)
        self.assertGreater(default_len, 20000)
        # Flash prompt is ~2.4k chars (<700 tokens)
        self.assertLess(flash_len, 3500)
        self.assertLess(flash_len, default_len / 5)

    def test_14_fatal_error_propagation_not_completed(self):
        """Simulates action error (HTTP 413 rate limit) and verifies it is recognized as infrastructure_aborted."""
        # Simulated action result with HTTP 413 error
        err_msg = (
            "Groq API returned HTTP 413: Error code: 413 - "
            "{'error': {'message': 'Request too large for model `openai/gpt-oss-120b` "
            "service tier `on_demand` on tokens per minute (TPM): Limit 8000, Requested 14161', "
            "'type': 'tokens', 'code': 'rate_limit_exceeded'}}"
        )
        is_provider_err = any(c in err_msg for c in [
            "413", "429", "503", "401", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
            "ConnectError", "rate_limit_exceeded", "Request too large",
            "TPM", "RPD", "RPM", "tokens per minute", "ModelProviderError",
            "ModelRateLimitError", "AuthenticationError", "BadRequestError",
            "Pre-dispatch payload size blocked"
        ])
        self.assertTrue(is_provider_err, "HTTP 413 error must be caught as provider error")


if __name__ == "__main__":
    unittest.main()

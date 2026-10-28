"""
Tests for Budget Controller and Defensible Financial Guards
Part of: "The DOM Serialization Gap" Research Infrastructure
"""

import unittest
import sys
from pathlib import Path

# Ensure research_execution_20261018 is on path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from budget_controller import (
    MODEL_PRICING_TABLE,
    BudgetExceededError,
    UnknownModelPricingError,
    get_model_pricing,
    compute_step_cost,
    compute_worst_case_run_cost,
    estimate_preflight_budget,
    LocalBudgetGuard
)

class TestBudgetController(unittest.TestCase):

    def test_01_unknown_model_fails_closed(self):
        """Unknown or unverified models must immediately fail closed."""
        with self.assertRaises(UnknownModelPricingError):
            get_model_pricing("unsupported-mysterious-llm-v99")
            
        with self.assertRaises(UnknownModelPricingError):
            LocalBudgetGuard(cost_ceiling_usd=10.0, model_name="unknown-model")

    def test_02_known_models_return_accurate_pricing(self):
        """Standard benchmark models should have strictly positive pricing."""
        for m in ["gemini-flash-lite-latest", "gemini-1.5-flash", "claude-3-5-sonnet-20241022", "gpt-4o"]:
            p = get_model_pricing(m)
            self.assertIn("input_per_million", p)
            self.assertIn("output_per_million", p)
            self.assertGreater(p["input_per_million"], 0)
            self.assertGreater(p["output_per_million"], 0)

    def test_03_preflight_budget_calculation(self):
        """Preflight budget calculation must bound worst-case and realistically expected costs."""
        # 96 runs, max 15 steps per run
        est = estimate_preflight_budget(
            total_runs=96,
            model_name="gemini-flash-lite-latest",
            cost_ceiling_usd=5.0,
            max_steps=15
        )
        self.assertEqual(est["total_runs"], 96)
        self.assertGreater(est["worst_case_total_usd"], 0)
        self.assertGreater(est["realistic_expected_total_usd"], 0)
        self.assertLess(est["realistic_expected_total_usd"], est["worst_case_total_usd"])
        # Worst case for 96 runs * 15 steps * 10k in ($0.15/1M) = 96 * 15 * 0.0015 = ~$2.16
        # Ceiling is $5.00, so worst case should NOT exceed ceiling
        self.assertFalse(est["worst_case_exceeds_ceiling"])
        # Must clearly indicate it is NOT a guaranteed provider limit
        self.assertFalse(est["guaranteed_provider_limit"])
        self.assertIn("client-side software guardrail", est["disclaimer"])

    def test_04_preflight_fails_when_ceiling_is_too_low(self):
        """If ceiling is set to $1.00 but worst-case is $2.16, preflight flags warning."""
        est = estimate_preflight_budget(
            total_runs=96,
            model_name="gemini-flash-lite-latest",
            cost_ceiling_usd=1.00,
            max_steps=15
        )
        self.assertTrue(est["worst_case_exceeds_ceiling"])

    def test_05_local_guard_accumulates_and_stops_at_ceiling(self):
        """Guard stops execution when cumulative cost reaches or exceeds ceiling."""
        guard = LocalBudgetGuard(cost_ceiling_usd=0.01, model_name="gemini-flash-lite-latest")
        
        # Initial state
        can_dispatch, msg = guard.check_can_dispatch_trial()
        self.assertTrue(can_dispatch)
        
        # Record small step
        guard.record_step(prompt_tokens=1000, completion_tokens=50)
        self.assertFalse(guard.halted_due_to_ceiling)
        
        # Record huge trial that breaches $0.01 ceiling
        # $0.01 / ($0.15/1M) = ~67,000 tokens
        res = guard.record_trial_completion(total_steps=10, provider_prompt_tokens=80000, provider_completion_tokens=5000)
        self.assertTrue(res["halted"])
        self.assertTrue(guard.halted_due_to_ceiling)
        
        # Next trial dispatch check must fail closed
        can_dispatch, msg = guard.check_can_dispatch_trial()
        self.assertFalse(can_dispatch)
        self.assertIn("reached or exceeded ceiling", msg)

    def test_06_guard_fails_closed_on_insufficient_headroom(self):
        """When require_worst_case_headroom is enabled, stops before starting a run if worst-case cannot fit."""
        # Worst-case trial for gemini-flash-lite (15 steps * 10k = 150k in -> $0.0225)
        guard = LocalBudgetGuard(cost_ceiling_usd=0.03, model_name="gemini-flash-lite-latest")
        
        # Spend $0.015, leaving $0.015 remaining (less than $0.0225 needed for worst case)
        guard.record_trial_completion(total_steps=1, provider_prompt_tokens=100000, provider_completion_tokens=0)
        self.assertLess(guard.cost_ceiling_usd - guard.cumulative_cost_usd, 0.02)
        
        # Without headroom check, budget is positive
        can_dispatch, _ = guard.check_can_dispatch_trial(require_worst_case_headroom=False)
        self.assertTrue(can_dispatch)
        
        # With headroom check, fails closed
        can_dispatch, msg = guard.check_can_dispatch_trial(require_worst_case_headroom=True)
        self.assertFalse(can_dispatch)
        self.assertIn("Remaining budget", msg)
        self.assertIn("less than worst-case trial cost", msg)

    def test_07_missing_tokens_fallback_to_conservative_bounds(self):
        """When provider returns None for tokens, guard must not charge $0.00; must use conservative bound."""
        guard = LocalBudgetGuard(cost_ceiling_usd=1.0, model_name="gemini-flash-lite-latest")
        step_cost = guard.record_step(prompt_tokens=None, completion_tokens=None)
        self.assertGreater(step_cost, 0.0)
        self.assertEqual(guard.cumulative_prompt_tokens, 10000)
        self.assertEqual(guard.cumulative_completion_tokens, 500)


if __name__ == "__main__":
    unittest.main()

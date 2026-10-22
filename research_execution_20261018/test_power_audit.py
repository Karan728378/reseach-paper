"""
Test Suite for Statistical Power Audit
=============================================================================
Validates mathematical calculations, edge cases, monotonic properties,
and output structure of reproduce_power_audit.py.
=============================================================================
"""

import unittest
import json
import math
from pathlib import Path

try:
    from reproduce_power_audit import (
        norm_cdf, norm_ppf, two_proportion_analytical_power,
        required_sample_size_superiority, required_sample_size_tost_equivalence,
        design_effect, OUTPUT_JSON
    )
except ModuleNotFoundError:
    from research_execution_20261018.reproduce_power_audit import (
        norm_cdf, norm_ppf, two_proportion_analytical_power,
        required_sample_size_superiority, required_sample_size_tost_equivalence,
        design_effect, OUTPUT_JSON
    )

class TestPowerAudit(unittest.TestCase):
    
    def test_normal_functions_inverses(self):
        """Verify norm_ppf and norm_cdf are accurate inverses."""
        probs = [0.01, 0.05, 0.10, 0.50, 0.90, 0.95, 0.99]
        for p in probs:
            z = norm_ppf(p)
            p_back = norm_cdf(z)
            self.assertAlmostEqual(p, p_back, places=4)

    def test_analytical_power_zero_delta(self):
        """Delta = 0 must return alpha (Type I error rate)."""
        pw = two_proportion_analytical_power(0.50, 0.50, 20, 20, alpha=0.05)
        self.assertAlmostEqual(pw, 0.05, places=3)
        pw_adj = two_proportion_analytical_power(0.50, 0.50, 20, 20, alpha=0.01667)
        self.assertAlmostEqual(pw_adj, 0.01667, places=3)

    def test_analytical_power_monotonicity(self):
        """Power must strictly increase with sample size and effect size."""
        # Increasing sample size
        pw_20 = two_proportion_analytical_power(0.50, 0.80, 20, 20, alpha=0.05)
        pw_40 = two_proportion_analytical_power(0.50, 0.80, 40, 40, alpha=0.05)
        pw_80 = two_proportion_analytical_power(0.50, 0.80, 80, 80, alpha=0.05)
        self.assertLess(pw_20, pw_40)
        self.assertLess(pw_40, pw_80)
        
        # Increasing delta
        pw_small = two_proportion_analytical_power(0.50, 0.65, 40, 20, alpha=0.01667)
        pw_large = two_proportion_analytical_power(0.50, 0.85, 40, 20, alpha=0.01667)
        self.assertLess(pw_small, pw_large)

    def test_sample_size_superiority_bounds(self):
        """Verify required sample size calculations for superiority."""
        # At delta=0.20, alpha=0.01667, power=0.80
        # If p1=0.70, p2=0.90: n ~ 82
        # If p1=0.50, p2=0.70 (max variance): n ~ 124
        n_p70 = required_sample_size_superiority(0.70, 0.90, alpha=0.05/3.0, power=0.80)
        self.assertGreater(n_p70, 80.0)
        self.assertLess(n_p70, 90.0)
        
        n_p50 = required_sample_size_superiority(0.50, 0.70, alpha=0.05/3.0, power=0.80)
        self.assertGreater(n_p50, 120.0)
        self.assertLess(n_p50, 130.0)

    def test_sample_size_tost_bounds(self):
        """Verify required sample size calculations for TOST equivalence."""
        # margin = 0.10, alpha = 0.05, power = 0.80
        # p=0.80 -> n ~ 274
        # p=0.70 -> n ~ 360
        # p=0.50 -> n ~ 428
        n_tost_80 = required_sample_size_tost_equivalence(0.80, margin=0.10, alpha=0.05, power=0.80)
        self.assertGreater(n_tost_80, 260.0)
        self.assertLess(n_tost_80, 290.0)
        
        n_tost_70 = required_sample_size_tost_equivalence(0.70, margin=0.10, alpha=0.05, power=0.80)
        self.assertGreater(n_tost_70, 340.0)
        self.assertLess(n_tost_70, 380.0)

    def test_design_effect_calculation(self):
        """Verify DEFF formula and effective sample size."""
        # m = 4 reps per cluster
        # rho = 0 -> DEFF = 1.0
        self.assertEqual(design_effect(4, 0.0), 1.0)
        # rho = 0.10 -> DEFF = 1.0 + 3*0.10 = 1.30
        self.assertAlmostEqual(design_effect(4, 0.10), 1.30, places=4)
        # rho = 0.20 -> DEFF = 1.0 + 3*0.20 = 1.60
        self.assertAlmostEqual(design_effect(4, 0.20), 1.60, places=4)

    def test_audit_json_file_validity(self):
        """Verify output JSON contains all required reconciled metrics."""
        self.assertTrue(OUTPUT_JSON.exists(), "power_audit_results.json must exist")
        data = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
        
        # Check design counts reconciliation
        counts = data["design_counts"]["sample_size_reconciliation"]
        self.assertEqual(counts["N_total_schedule"], 96)
        self.assertEqual(counts["N_primary_benchmark"], 80)
        self.assertEqual(counts["N_exploratory_probe"], 16)
        self.assertEqual(counts["n_per_arm_primary_T1_T5"], 20)
        self.assertEqual(counts["n_pooled_baseline_primary_T1_T5"], 40)
        
        # Check RCBD simulated power
        rcbd = data["rcbd_simulation_results"]
        p_small = rcbd["Small Effect (Delta=0.20)"]["stratified_cmh_power"]
        # Must be in [0.08, 0.14] (reported 10.85%)
        self.assertGreaterEqual(p_small, 0.08)
        self.assertLessEqual(p_small, 0.14)
        
        p_subtle = rcbd["Subtle Effect (Delta=0.15)"]["stratified_cmh_power"]
        # Must be in [0.04, 0.08] (reported 5.8%)
        self.assertGreaterEqual(p_subtle, 0.04)
        self.assertLessEqual(p_subtle, 0.08)

if __name__ == "__main__":
    unittest.main()

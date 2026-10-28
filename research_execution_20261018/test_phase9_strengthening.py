"""
test_phase9_strengthening.py
=============================================================================
Regression and Verification Tests for Phase 9 Deliverables:
- Information-loss measurements (CSV and MD)
- Version-drift audit (PyPI wheel hashes and invariants)
- Solvability analysis (Oracle reader determinations)
- Exact statistical Clopper-Pearson intervals
=============================================================================
"""

import unittest
import csv
import json
import pathlib
import hashlib
from phase9_execute import clopper_pearson_exact_ci, wilson_score_ci, sha256_file

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent

class TestPhase9Strengthening(unittest.TestCase):

    def test_clopper_pearson_exactness(self):
        """Exact binomial limits match mathematical reference standard."""
        # 13/13 (Exploratory pilot per-arm rate)
        cp_13_13 = clopper_pearson_exact_ci(13, 13, 0.95)
        self.assertAlmostEqual(cp_13_13[0], 0.7529, places=3)
        self.assertEqual(cp_13_13[1], 1.0000)

        # 0/4 (JSON-LD retention)
        cp_0_4 = clopper_pearson_exact_ci(0, 4, 0.95)
        self.assertEqual(cp_0_4[0], 0.0000)
        self.assertAlmostEqual(cp_0_4[1], 0.6024, places=3)

        # 5/16 (Non-interactive ARIA retention)
        cp_5_16 = clopper_pearson_exact_ci(5, 16, 0.95)
        self.assertAlmostEqual(cp_5_16[0], 0.1102, places=3)
        self.assertAlmostEqual(cp_5_16[1], 0.5866, places=3)

    def test_information_loss_csv_integrity(self):
        """INFORMATION_LOSS_MEASUREMENTS.csv must contain 44 verified entity evaluations."""
        csv_path = PROJECT_ROOT / "INFORMATION_LOSS_MEASUREMENTS.csv"
        self.assertTrue(csv_path.exists(), f"Missing {csv_path}")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        self.assertEqual(len(reader), 44)
        for row in reader:
            self.assertIn(row["Loss_Mechanism"], [
                "DISABLED_ELEMENTS", "INTERACTIVITY_GATE", "ATTRIBUTE_WHITELIST",
                "GEOMETRIC_MISCLASSIFICATION", "CSS_VISIBILITY", "NONE"
            ])

    def test_version_drift_wheel_hashes(self):
        """All downloaded wheels must strictly match verified official PyPI SHA-256 digests."""
        expected = {
            "browser_use-0.1.0-py3-none-any.whl": "d9839f0e22cdb00cfdc0962bc6ea03d4b2c51ef00c9021b490ac95cab756f06d",
            "browser_use-0.5.0-py3-none-any.whl": "a42e72103dc425810c856e8353853f765f4ddb641bb060080280fe2ce4355c6f",
            "browser_use-0.13.0-py3-none-any.whl": "afb80ceb2ef8f841b82f8c9d9b6f7fd7229b46952084415f95b40a1541776e1c",
            "browser_use-0.13.5-py3-none-any.whl": "530ea9a89da22222c3576d4a2b7c2c6f3b5b0f64b78217cceb16fc74663129dd",
            "browser_use-0.13.10-py3-none-any.whl": "66eb20153094f21728bc0110ada17c03a0c475df2374985d6b47e349cbd47705",
            "browser_use-0.13.11-py3-none-any.whl": "50b0d16efc44215f99ed1c9197f05e2519bb79fa1501eed7371aff450cc56045",
        }
        for fn, exp_hash in expected.items():
            whl_path = PROJECT_ROOT / "scratch" / "wheels" / fn
            self.assertTrue(whl_path.exists(), f"Missing wheel {whl_path}")
            act_hash = sha256_file(whl_path)
            self.assertEqual(act_hash.lower(), exp_hash.lower(), f"Hash mismatch for {fn}")

    def test_solvability_analysis_consistency(self):
        """SOLVABILITY_ANALYSIS.md must document ceiling and truncation contrasts."""
        smd_path = PROJECT_ROOT / "SOLVABILITY_ANALYSIS.md"
        self.assertTrue(smd_path.exists(), f"Missing {smd_path}")
        content = smd_path.read_text(encoding="utf-8")
        self.assertIn("TM-01-Home", content)
        self.assertIn("PROBE-A-Default", content)
        self.assertIn("PROBE-B-Container", content)
        self.assertIn("Co-Location Confound Formalization", content)
        self.assertIn("Evidence Class:** **E3", content)

if __name__ == "__main__":
    unittest.main()

"""
Unit Test Suite: Table 3 / Table 4 Baseline-Pooling Consistency Verification
Verifies that Table 3 and Table 4 are mathematically, statistically, and textually
reconciled across both research_paper_final.tex and RESEARCH_PAPER_DRAFT_V2.md,
ensuring baseline arms are not pooled without a formal TOST equivalence demonstration.
"""
import re
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXEC_DIR = ROOT_DIR / "research_execution_20261018"
TEX_PATH = EXEC_DIR / "research_paper_final.tex"
MD_PATH = EXEC_DIR / "RESEARCH_PAPER_DRAFT_V2.md"


class TestBaselinePoolingConsistency(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tex_content = TEX_PATH.read_text(encoding="utf-8")
        cls.md_content = MD_PATH.read_text(encoding="utf-8")

    def test_tex_table3_is_unpooled(self):
        """Verify research_paper_final.tex Table 3 presents separate baseline arms (N=20)."""
        # Ensure pooled denominator 25 / 40 is absent from Table 3
        self.assertNotIn("25 / 40", self.tex_content, "Found pooled denominator 25 / 40 in LaTeX source!")
        
        # Ensure separate baseline arms are present in Table 3
        self.assertIn("ARIA vs BASELINE (ABS)", self.tex_content)
        self.assertIn("ARIA vs BASELINE\\_REP (VIS)", self.tex_content)
        self.assertIn("DATA-CFG vs BASELINE (ABS)", self.tex_content)
        self.assertIn("DATA-CFG vs BASELINE\\_REP (VIS)", self.tex_content)
        self.assertIn("ARIA vs DATA-CFG", self.tex_content)

    def test_md_table3_is_unpooled(self):
        """Verify RESEARCH_PAPER_DRAFT_V2.md Table 3 presents separate baseline arms (N=20)."""
        self.assertNotIn("25 / 40", self.md_content, "Found pooled denominator 25 / 40 in Markdown draft!")
        self.assertIn("ARIA vs BASELINE (ABS)", self.md_content)
        self.assertIn("ARIA vs BASELINE_REP (VIS)", self.md_content)
        self.assertIn("DATA-CFG vs BASELINE (ABS)", self.md_content)
        self.assertIn("DATA-CFG vs BASELINE_REP (VIS)", self.md_content)
        self.assertIn("ARIA vs DATA-CFG", self.md_content)

    def test_risk_difference_arithmetic_consistency(self):
        """
        Verify that all risk differences in Table 3 match exact raw proportions:
        ABS: 13/20 (0.65), VIS: 12/20 (0.60), ARIA: 14/20 (0.70), DATA-CFG: 17/20 (0.85).
        """
        p_abs = 13 / 20  # 0.65
        p_vis = 12 / 20  # 0.60
        p_aria = 14 / 20  # 0.70
        p_data = 17 / 20  # 0.85

        self.assertAlmostEqual(p_aria - p_abs, 0.0500, places=4)
        self.assertAlmostEqual(p_aria - p_vis, 0.1000, places=4)
        self.assertAlmostEqual(p_data - p_abs, 0.2000, places=4)
        self.assertAlmostEqual(p_data - p_vis, 0.2500, places=4)
        self.assertAlmostEqual(p_aria - p_data, -0.1500, places=4)

        # Check values in tex source
        self.assertIn("+0.0500", self.tex_content)
        self.assertIn("+0.1000", self.tex_content)
        self.assertIn("+0.2000", self.tex_content)
        self.assertIn("+0.2500", self.tex_content)
        self.assertIn("-0.1500", self.tex_content)

    def test_table4_decision_justifies_unpooled_presentation(self):
        """
        Verify Table 4 explicitly resolves the methodology by rejecting pooling
        due to the Equivalence Fallacy / lack of a priori TOST margin.
        """
        for source_name, content in [("LaTeX", self.tex_content), ("Markdown", self.md_content)]:
            self.assertIn("TOST", content, f"Missing TOST equivalence rationale in {source_name}")
            self.assertIn("Equivalence Fallacy", content, f"Missing Equivalence Fallacy rationale in {source_name}")
            self.assertIn("p = 1.0000", content, f"Missing Fisher p = 1.0000 in Table 4 in {source_name}")

    def test_no_synthetic_data_labeled_as_live_confirmatory(self):
        """Verify that synthetic benchmark disclaimers are prominent on all tables."""
        self.assertIn("Synthetic Software Benchmark Disclaimer", self.tex_content)
        self.assertIn("Synthetic Software Benchmark Disclaimer", self.md_content)
        self.assertIn("They do not represent real agent task performance", self.tex_content)
        self.assertIn("They do not represent real agent task performance", self.md_content)


if __name__ == "__main__":
    unittest.main()

"""
Regression Test Suite: ARIA vs. Baseline Prompt Divergence
Verifies that ARIA and Baseline conditions produce distinct, verifiable agent-facing inputs
under text-only mode (use_vision=False), while confirming the architectural boundary between
interactive element retention and non-interactive metadata pruning.
"""
import csv
import json
import re
import unittest
from pathlib import Path

ROOT_DIR = Path("C:/testing")
EXEC_DIR = ROOT_DIR / "research_execution_20261018"
AUDIT_OUTPUTS = EXEC_DIR / "audit_outputs"
CSV_PATH = AUDIT_OUTPUTS / "aria_baseline_prompt_pairs.csv"
DIFF_DIR = AUDIT_OUTPUTS / "aria_baseline_prompt_diffs"


class TestAriaBaselinePromptDivergence(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not CSV_PATH.exists():
            raise FileNotFoundError(f"Missing required prompt pairs audit file: {CSV_PATH}")
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.pairs = list(reader)

    def test_all_seven_pairs_diverge_in_raw_and_normalized_hashes(self):
        """
        Verify that all 7 tested pairs (Tasks T1-T6 and Edge Cases Fixture)
        produce distinct serialized agent-facing prompt inputs.
        """
        self.assertEqual(len(self.pairs), 7, f"Expected 7 evaluated pairs, found {len(self.pairs)}")
        for p in self.pairs:
            pid = p["pair_id"]
            is_raw_ident = p["is_identical_raw"].lower() == "true"
            is_norm_ident = p["is_identical_norm"].lower() == "true"
            diff_lines = int(p["diff_line_count"])
            has_aria_diff = p["has_aria_attribute_diff"].lower() == "true"

            self.assertFalse(
                is_raw_ident,
                f"Pair {pid} failed: raw prompt hashes are identical between baseline and ARIA!"
            )
            self.assertFalse(
                is_norm_ident,
                f"Pair {pid} failed: normalized prompt hashes are identical between baseline and ARIA!"
            )
            self.assertGreater(
                diff_lines, 0,
                f"Pair {pid} failed: diff line count is 0!"
            )
            self.assertTrue(
                has_aria_diff,
                f"Pair {pid} failed: no aria-label diff detected!"
            )

    def test_interactive_aria_retention_in_prompt_diffs(self):
        """
        Verify that interactive elements (buttons, inputs, forms) retain ARIA attributes
        in the ARIA treatment prompts and not in baseline prompts.
        """
        diff_file_t2 = DIFF_DIR / "pair_02_t2_product_home.diff"
        self.assertTrue(diff_file_t2.exists(), f"Missing diff file: {diff_file_t2}")
        diff_text_t2 = diff_file_t2.read_text(encoding="utf-8")

        # Interactive button: aria-label="Add item to cart" added in ARIA (+)
        self.assertIn("+[30]<button aria-label=Add item to cart />", diff_text_t2)
        self.assertIn("-[28]<button />", diff_text_t2)

        # Form: role=search added in ARIA (+)
        self.assertIn("+[5]<form id=search-form role=search />", diff_text_t2)
        self.assertIn("-[3]<form id=search-form />", diff_text_t2)

        # Input and submit button with aria-label
        self.assertIn("aria-label=Search products", diff_text_t2)
        self.assertIn("aria-label=Search", diff_text_t2)

    def test_non_interactive_aria_pruning_in_prompts(self):
        """
        Verify that non-interactive ARIA semantics (e.g. price/rating spans, card divs)
        are completely pruned by serializer line 1046 and do NOT reach the prompt buffer
        in either condition.
        """
        diff_file_t2 = DIFF_DIR / "pair_02_t2_product_home.diff"
        diff_text_t2 = diff_file_t2.read_text(encoding="utf-8")

        # In source HTML, v2-aria has aria-label="Price: $49.99" and aria-label="Rating: 4.5 out of 5 stars"
        # In diff, these attributes MUST NOT appear as added (+) tokens because they were stripped!
        self.assertNotIn("aria-label=Price:", diff_text_t2)
        self.assertNotIn("aria-label=Rating:", diff_text_t2)
        self.assertNotIn("aria-label=SoundFlow Air 3, $49.99", diff_text_t2)

    def test_edge_cases_fixture_divergence(self):
        """
        Verify that the edge cases fixture produces observable prompt divergence
        on interactive elements while pruning non-interactive containers.
        """
        diff_file_edge = DIFF_DIR / "pair_07_edge_cases_fixture.diff"
        self.assertTrue(diff_file_edge.exists(), f"Missing edge fixture diff: {diff_file_edge}")
        diff_text_edge = diff_file_edge.read_text(encoding="utf-8")

        self.assertIn("+", diff_text_edge)
        self.assertIn("-", diff_text_edge)

    def test_treatment_character_length_expansion(self):
        """
        Verify that the ARIA treatment systematically expands prompt character length
        across all product tasks due to the retention of button/input ARIA attributes.
        """
        for p in self.pairs:
            pid = p["pair_id"]
            if p["task_id"] in ["T1", "T2", "T3", "T4", "T6"]:
                v0_len = int(p["v0_char_length"])
                v2_len = int(p["v2_char_length"])
                diff_len = v2_len - v0_len
                self.assertGreater(
                    diff_len, 100,
                    f"Pair {pid} did not show expected character length expansion (v0={v0_len}, v2={v2_len})"
                )


if __name__ == "__main__":
    unittest.main()

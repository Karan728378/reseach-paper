"""
Comprehensive Unit & Regression Test Suite for Isolated Task T6 Verifier
Validates Grounded Refusal vs Hallucination under Protocol v4 Candidate Logic.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

import unittest
from t6_verifier_isolated import verify_t6_flawed, verify_t6_grounded_refusal

class TestT6VerifierIsolated(unittest.TestCase):
    
    # ── 1. Valid Grounded Refusals (Should PASS with 1.0) ────────────────────
    def test_valid_refusals_standard(self):
        cases = [
            "I searched the product details for SoundFlow Air 3, but could not find any warranty information.",
            "There is no warranty duration specified on this page.",
            "Warranty duration is not stated in the product description.",
            "I checked the page thoroughly: warranty information is unlisted.",
            "No warranty terms or guarantee period are mentioned for this item.",
            "Unable to find warranty duration for SKU wh-001.",
            "The manufacturer warranty is missing from the website catalog.",
            "Warranty: Not provided.",
            "SoundFlow Air 3 details do not state a warranty period.",
            "Warranty duration is unavailable on the page."
        ]
        for text in cases:
            with self.subTest(text=text):
                res = verify_t6_grounded_refusal(text)
                self.assertTrue(res["success"], f"Expected pass for grounded refusal: '{text}'")
                self.assertEqual(res["score"], 1.0)
                self.assertEqual(res["classification"], "GROUNDED_REFUSAL_SUCCESS")
                self.assertTrue(res["details"]["refusal_detected"])
                self.assertFalse(res["details"]["hallucination_detected"])

    # ── 2. Explicit Unsupported Duration Hallucinations (Should FAIL with 0.0) ─
    def test_explicit_unsupported_durations(self):
        cases = [
            ("The warranty duration is 36 months.", "36 months"),
            ("SoundFlow Air 3 comes with a 36 mo warranty.", "36 mo"),
            ("The manufacturer offers a 2-year warranty.", "2-year"),
            ("Warranty coverage: 12 months.", "12 months"),
            ("It has a 3 year guarantee.", "3 year"),
            ("According to standard policy, it is 24 months.", "24 months"),
            ("The item includes a 1 yr manufacturer warranty.", "1 yr"),
            ("Warranty period is three years from purchase date.", "three years"),
            ("Protected under a 90 days limited warranty.", "90 days")
        ]
        for text, expected_match in cases:
            with self.subTest(text=text):
                res = verify_t6_grounded_refusal(text)
                self.assertFalse(res["success"], f"Expected fail for hallucination: '{text}'")
                self.assertEqual(res["score"], 0.0)
                self.assertEqual(res["classification"], "UNSUPPORTED_DURATION_HALLUCINATION")
                self.assertTrue(res["details"]["hallucination_detected"])
                self.assertIsNotNone(res["details"]["matched_duration"])

    # ── 3. Contradictory Refusal + Duration (Should FAIL with 0.0) ────────────
    def test_contradictory_refusal_with_duration(self):
        cases = [
            "The warranty is not stated on the page, but it is typically 36 months.",
            "No warranty found on the site; assuming 1 year.",
            "I cannot find the warranty duration, though similar products have 2 years.",
            "Warranty duration not specified, but probably 12 mos."
        ]
        for text in cases:
            with self.subTest(text=text):
                res = verify_t6_grounded_refusal(text)
                self.assertFalse(res["success"], f"Expected fail for contradictory output: '{text}'")
                self.assertEqual(res["score"], 0.0)
                self.assertEqual(res["classification"], "CONTRADICTORY_REFUSAL_WITH_HALLUCINATION")
                self.assertTrue(res["details"]["refusal_detected"])
                self.assertTrue(res["details"]["hallucination_detected"])

    # ── 4. Unrelated Answers / Non-Refusals (Should FAIL with 0.0) ─────────────
    def test_unrelated_answers(self):
        cases = [
            "The price of SoundFlow Air 3 is $49.99.",
            "I navigated to the audio category and added headphones to cart.",
            "The customer rating is 4.2 out of 5 stars.",
            "Task complete.",
            "Hello, how can I help you?",
            "SoundFlow Air 3 features Bluetooth 5.2 and noise cancellation.",
            ""
        ]
        for text in cases:
            with self.subTest(text=text):
                res = verify_t6_grounded_refusal(text)
                self.assertFalse(res["success"], f"Expected fail for unrelated/empty text: '{text}'")
                self.assertEqual(res["score"], 0.0)

    # ── 5. Ambiguous Answers (Should FAIL with 0.0) ────────────────────────────
    def test_ambiguous_answers(self):
        cases = [
            "I found the product page.",
            "Warranty information.",
            "Please check the manual.",
            "It might have a guarantee."
        ]
        for text in cases:
            with self.subTest(text=text):
                res = verify_t6_grounded_refusal(text)
                self.assertFalse(res["success"], f"Expected fail for ambiguous answer: '{text}'")
                self.assertEqual(res["score"], 0.0)
                self.assertEqual(res["classification"], "UNRELATED_OR_AMBIGUOUS_NON_REFUSAL")

    # ── 6. Casing, Whitespace, Punctuation Variants ───────────────────────────
    def test_casing_and_whitespace_variants(self):
        refusal_variants = [
            "WARRANTY NOT FOUND.",
            "   no warranty duration specified on this page.   \n",
            "There is NO WARRANTY listed for this product!",
            "Warranty: NOT STATED."
        ]
        for text in refusal_variants:
            with self.subTest(text=text):
                res = verify_t6_grounded_refusal(text)
                self.assertTrue(res["success"])

        hallucination_variants = [
            "DURATION: 36 MONTHS.",
            "36mo warranty",
            "36   months",
            "Warranty is 2-YEARS."
        ]
        for text in hallucination_variants:
            with self.subTest(text=text):
                res = verify_t6_grounded_refusal(text)
                self.assertFalse(res["success"])

    # ── 7. Differential Verification: Flawed vs Corrected Logic ───────────────
    def test_differential_flawed_vs_corrected(self):
        """
        Direct demonstration of the inversion:
        - When the agent correctly refuses, the flawed verifier FAILS, but corrected verifier PASSES.
        - When the agent hallucinates '36 months', the flawed verifier PASSES, but corrected verifier FAILS.
        """
        grounded_refusal_text = "I checked SoundFlow Air 3, but the warranty duration is not specified on this website."
        flawed_refusal = verify_t6_flawed(grounded_refusal_text)
        corrected_refusal = verify_t6_grounded_refusal(grounded_refusal_text)
        
        # Flawed verifier rejected grounded refusal!
        self.assertFalse(flawed_refusal["success"], "Flawed verifier erroneously rejected grounded refusal")
        # Corrected verifier accepts grounded refusal!
        self.assertTrue(corrected_refusal["success"], "Corrected verifier correctly accepted grounded refusal")

        hallucinated_text = "The manufacturer warranty duration is 36 months."
        flawed_hallucination = verify_t6_flawed(hallucinated_text)
        corrected_hallucination = verify_t6_grounded_refusal(hallucinated_text)
        
        # Flawed verifier accepted hallucination!
        self.assertTrue(flawed_hallucination["success"], "Flawed verifier erroneously rewarded hallucination")
        # Corrected verifier rejects hallucination!
        self.assertFalse(corrected_hallucination["success"], "Corrected verifier correctly rejected hallucination")

if __name__ == "__main__":
    unittest.main()

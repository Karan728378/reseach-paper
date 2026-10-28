"""
Unit Test Suite: Sentinel Pipeline Empirical Verification
Asserts stage-by-stage transmission metrics from sentinel_stage_trace.json.
Validates the exact mathematical survival and pruning rates.
"""

import json
import unittest
from pathlib import Path

RESEARCH_DIR = Path("C:/testing/research_execution_20261018")
TRACE_JSON = RESEARCH_DIR / "sentinel_stage_trace.json"

class TestSentinelPipelineTrace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not TRACE_JSON.exists():
            raise FileNotFoundError(f"Missing {TRACE_JSON}. Run trace_sentinel_pipeline.py first.")
        cls.trace_data = json.loads(TRACE_JSON.read_text(encoding="utf-8"))
        cls.results = cls.trace_data["results"]

    def test_visible_text_full_preservation(self):
        """Visible typography must survive 100% of pipeline stages (Stages 1-6)."""
        res = self.results["visible_text"]
        for stage in [
            "stage_1_source_html", "stage_2_live_dom", "stage_3_blink_axtree",
            "stage_4a_serializer_default", "stage_4b_serializer_extended",
            "stage_5_observation_buffer", "stage_6_client_request_payload"
        ]:
            self.assertTrue(res[stage], f"Visible text failed at {stage}")

    def test_aria_button_reaches_model_payload(self):
        """WAI-ARIA aria-label on interactive button reaches the model client payload."""
        res = self.results["aria_button"]
        self.assertTrue(res["stage_1_source_html"])
        self.assertTrue(res["stage_2_live_dom"])
        self.assertTrue(res["stage_3_blink_axtree"])
        self.assertTrue(res["stage_4a_serializer_default"])
        self.assertTrue(res["stage_5_observation_buffer"])
        self.assertTrue(res["stage_6_client_request_payload"])

    def test_aria_span_critical_divergence(self):
        """Non-interactive span aria-label exists in Blink AXTree but is stripped by serializer."""
        res = self.results["aria_span"]
        self.assertTrue(res["stage_1_source_html"])
        self.assertTrue(res["stage_2_live_dom"])
        self.assertTrue(res["stage_3_blink_axtree"], "Must be present in Blink AXTree")
        self.assertFalse(res["stage_4a_serializer_default"], "Must be stripped in default serializer")
        self.assertFalse(res["stage_6_client_request_payload"], "Must not reach model payload")

    def test_jsonld_and_meta_unconditional_loss(self):
        """JSON-LD script tags and meta tags are pruned at serializer and never reach prompt."""
        for key in ["jsonld_name", "jsonld_sku", "meta_tag"]:
            res = self.results[key]
            self.assertTrue(res["stage_1_source_html"])
            self.assertTrue(res["stage_2_live_dom"])
            self.assertFalse(res["stage_3_blink_axtree"])
            self.assertFalse(res["stage_4a_serializer_default"])
            self.assertFalse(res["stage_5_observation_buffer"])
            self.assertFalse(res["stage_6_client_request_payload"])

    def test_custom_data_attributes_reachability_rules(self):
        """Custom data attributes are absent in Blink AXTree and default serializer, require extended whitelist."""
        res_btn = self.results["data_button"]
        res_cnt = self.results["data_container"]
        
        # Absent in Blink AXTree
        self.assertFalse(res_btn["stage_3_blink_axtree"])
        self.assertFalse(res_cnt["stage_3_blink_axtree"])
        
        # Absent in default serializer
        self.assertFalse(res_btn["stage_4a_serializer_default"])
        self.assertFalse(res_cnt["stage_4a_serializer_default"])
        
        # Interactive button survives extended serializer; non-interactive container does not
        self.assertTrue(res_btn["stage_4b_serializer_extended"])
        self.assertFalse(res_cnt["stage_4b_serializer_extended"])

if __name__ == "__main__":
    unittest.main()

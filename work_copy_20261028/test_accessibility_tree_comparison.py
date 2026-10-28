import json
import sys
import unittest
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(r"C:\testing")
RESEARCH_DIR = WORKSPACE_ROOT / "research_execution_20261018"
JSON_PATH = RESEARCH_DIR / "accessibility_tree_comparison.json"
MD_PATH = RESEARCH_DIR / "ACCESSIBILITY_TREE_COMPARISON.md"

class TestAccessibilityTreeComparison(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not JSON_PATH.exists():
            raise FileNotFoundError(f"Missing required comparison artifact: {JSON_PATH}")
        cls.data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    def test_tooling_metadata_playwright_unavailability(self):
        """Verifies Playwright unavailability is accurately documented without deception."""
        meta = self.data["tooling_metadata"]
        self.assertFalse(meta["playwright_installed"])
        self.assertIsNone(meta["playwright_version"])
        self.assertFalse(meta["playwright_snapshot_available"])
        self.assertIn("ModuleNotFoundError", meta["playwright_error"])
        self.assertIn("CDP", meta["supported_alternative"])
        self.assertEqual(meta["browser_use_version"], "0.13.10")

    def test_variant_ax_node_counts(self):
        """Verifies node counts for all variants and fixtures."""
        counts = self.data["variant_node_counts"]
        self.assertGreater(counts["v0_baseline_ax_nodes"], 100)
        self.assertGreater(counts["v1_jsonld_ax_nodes"], 100)
        self.assertGreater(counts["v2_aria_ax_nodes"], 100)
        self.assertGreater(counts["v3_data_attrs_ax_nodes"], 100)
        self.assertGreater(counts["edge_cases_ax_nodes"], 20)

    def test_channel_1_jsonld_concordant_loss(self):
        """Verifies JSON-LD is absent in both Chromium AXTree and browser-use prompt."""
        ch1 = self.data["channels"]["channel_1_jsonld"]
        self.assertTrue(ch1["source_html_evidence"]["v1_jsonld_static_script"])
        self.assertTrue(ch1["live_dom_evidence"]["v1_jsonld"])
        self.assertFalse(ch1["chromium_ax_tree_evidence"]["retained_in_ax_tree"])
        self.assertEqual(ch1["chromium_ax_tree_evidence"]["nodes_matching_jsonld"], 0)
        self.assertFalse(ch1["browser_use_serialized_observation"]["retained_in_prompt"])
        self.assertIn("CONCORDANT LOSS", ch1["comparison_verdict"])

    def test_channel_2_button_accessible_names(self):
        """Verifies button accessible names are concordantly retained in AXTree and prompt."""
        ch2 = self.data["channels"]["channel_2_button_accessible_names"]
        self.assertTrue(ch2["source_html_evidence"]["v2_aria"])
        self.assertTrue(ch2["chromium_ax_tree_evidence"]["retained_in_ax_tree"])
        self.assertTrue(ch2["browser_use_serialized_observation"]["retained_in_prompt"])
        self.assertIn("CONCORDANT RETENTION", ch2["comparison_verdict"])
        # Check computed button in v2
        v2_buttons = ch2["chromium_ax_tree_evidence"]["v2_aria_buttons"]
        self.assertTrue(any("Add item to cart" in b["name"] for b in v2_buttons))

    def test_channel_3_non_interactive_aria_critical_divergence(self):
        """Verifies price/rating ARIA is retained in AXTree but stripped in browser-use."""
        ch3 = self.data["channels"]["channel_3_non_interactive_aria"]
        self.assertTrue(ch3["source_html_evidence"]["v2_aria_price_span"])
        self.assertTrue(ch3["chromium_ax_tree_evidence"]["retained_in_ax_tree"])
        self.assertFalse(ch3["browser_use_serialized_observation"]["retained_in_prompt"])
        self.assertIn("CRITICAL DIVERGENCE", ch3["comparison_verdict"])
        # Confirm price node in AX tree
        price_nodes = ch3["chromium_ax_tree_evidence"]["v2_aria_price_nodes"]
        self.assertTrue(len(price_nodes) > 0)
        self.assertEqual(price_nodes[0]["name"], "Price: $49.99")

    def test_channel_4_custom_data_attrs_reversed_divergence(self):
        """Verifies data-* is absent in AXTree but reachable in browser-use under extended whitelist."""
        ch4 = self.data["channels"]["channel_4_custom_data_attributes"]
        self.assertTrue(ch4["source_html_evidence"]["v3_data_attrs"])
        self.assertFalse(ch4["chromium_ax_tree_evidence"]["retained_in_ax_tree"])
        self.assertFalse(ch4["browser_use_serialized_observation"]["default_whitelist_has_data_action"])
        self.assertTrue(ch4["browser_use_serialized_observation"]["extended_whitelist_has_data_action"])
        self.assertIn("REVERSED DIVERGENCE", ch4["comparison_verdict"])

    def test_channel_5_visible_text_concordant_retention(self):
        """Verifies visible text is 100% retained across all representations."""
        ch5 = self.data["channels"]["channel_5_visible_text"]
        self.assertTrue(ch5["source_html_evidence"]["present_in_source"])
        self.assertTrue(ch5["chromium_ax_tree_evidence"]["retained_in_ax_tree"])
        self.assertTrue(ch5["browser_use_serialized_observation"]["retained_in_prompt"])
        self.assertIn("CONCORDANT RETENTION", ch5["comparison_verdict"])

    def test_edge_cases_divergence_assertions(self):
        """Verifies edge cases fixture findings."""
        ec = self.data["channels"]["edge_cases"]
        # Non-interactive container
        self.assertTrue(ec["non_interactive_container_section"]["retained_in_chromium_ax_tree"])
        self.assertFalse(ec["non_interactive_container_section"]["retained_in_browser_use_default"])
        # Non-interactive styled span (>50px, no icon heuristic)
        self.assertTrue(ec["non_interactive_price_span"]["retained_in_chromium_ax_tree"])
        self.assertFalse(ec["non_interactive_price_span"]["retained_in_browser_use_default"])
        # Icon heuristic small span (<50px, triggers icon heuristic in browser-use)
        self.assertTrue(ec["icon_heuristic_small_span"]["retained_in_chromium_ax_tree"])
        self.assertTrue(ec["icon_heuristic_small_span"]["retained_in_browser_use_default"])
        # Interactive data button
        self.assertFalse(ec["interactive_data_button"]["retained_in_chromium_ax_tree"])
        self.assertTrue(ec["interactive_data_button"]["retained_in_browser_use_extended"])

    def test_node_level_correspondence(self):
        """Verifies node correspondence metrics between CDP AXTree and browser-use selector map."""
        self.assertIn("node_level_correspondence", self.data)
        nc = self.data["node_level_correspondence"]
        self.assertIn("v2_aria", nc)
        v2_nc = nc["v2_aria"]
        self.assertEqual(v2_nc["interactive_elements_count"], 34)
        self.assertEqual(v2_nc["interactive_matched_to_ax"], 27)
        self.assertIn("stripped", v2_nc["non_interactive_limitation"])

    def test_markdown_report_integrity(self):
        """Verifies that the generated markdown report is complete and well-formatted."""
        self.assertTrue(MD_PATH.exists())
        text = MD_PATH.read_text(encoding="utf-8")
        self.assertIn("# Independent Accessibility-Tree Comparison Report", text)
        self.assertIn("**Playwright Installed:** `False`", text)
        self.assertIn("Chrome DevTools Protocol (CDP) Accessibility.getFullAXTree", text)
        self.assertIn("CRITICAL DIVERGENCE", text)
        self.assertIn("REVERSED DIVERGENCE", text)
        self.assertIn("Edge Cases Analysis", text)
        self.assertIn("Refutes the \"DOM Pruning == AX Tree\" Assumption", text)

if __name__ == "__main__":
    unittest.main()

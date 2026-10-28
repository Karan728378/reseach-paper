"""
Offline Test Suite: Observation Pipeline 6-Stage Trace
Tests each information channel across:
1. Source HTML
2. Live DOM
3. Chromium Blink Accessibility Tree (AXTree)
4. browser-use Serializer (Default vs Extended Whitelist)
5. Final Model Prompt Buffer
6. Distinguishability from Baseline
"""
import json
import sys
import unittest
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
EXEC_DIR = ROOT_DIR / "research_execution_20261018"
sys.path.insert(0, str(EXEC_DIR))

from bs4 import BeautifulSoup
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES
from browser_use.dom.serializer.serializer import DISABLED_ELEMENTS
import protocol_v3_runner

class TestObservationPipelineStages(unittest.TestCase):

    def setUp(self):
        self.v0_html = (ROOT_DIR / "variants" / "v0-baseline" / "index.html").read_text(encoding="utf-8")
        self.v1_html = (ROOT_DIR / "variants" / "v1-jsonld" / "index.html").read_text(encoding="utf-8")
        self.v2_html = (ROOT_DIR / "variants" / "v2-aria" / "index.html").read_text(encoding="utf-8")
        self.v3_html = (ROOT_DIR / "variants" / "v3-data-attrs" / "index.html").read_text(encoding="utf-8")
        
        ax_json_path = EXEC_DIR / "accessibility_tree_comparison.json"
        self.ax_data = json.loads(ax_json_path.read_text(encoding="utf-8")) if ax_json_path.exists() else {}

    # ── Stage 1 & 2: Source HTML and Serializer Pruning for JSON-LD ───────────
    def test_channel_1_jsonld_pipeline(self):
        """Trace JSON-LD through source HTML, AXTree, and serializer."""
        # Stage 1: Present in Source HTML
        self.assertIn("application/ld+json", self.v1_html)
        self.assertNotIn("application/ld+json", self.v0_html)
        
        # Stage 3: AXTree - Pruned
        ch1 = self.ax_data.get("channels", {}).get("channel_1_jsonld", {})
        self.assertFalse(ch1.get("chromium_ax_tree_evidence", {}).get("retained_in_ax_tree", True))
        
        # Stage 4: Serializer - Pruned by DISABLED_ELEMENTS
        self.assertIn("script", DISABLED_ELEMENTS)
        
        # Stage 5 & 6: Prompt Buffer - 0% Reach, Undistinguishable from Baseline
        self.assertFalse(ch1.get("browser_use_serialized_observation", {}).get("retained_in_prompt", True))
        self.assertIn("CONCORDANT LOSS", ch1.get("comparison_verdict", ""))

    # ── Channel 2: Button ARIA Accessible Names ──────────────────────────────
    def test_channel_2_button_aria_pipeline(self):
        """Trace Button ARIA through source HTML, live DOM rendering, AXTree, and serializer."""
        # Stage 1: Present in Source HTML (static navigation/form buttons)
        self.assertIn('id="search-submit-btn" aria-label="Search"', self.v2_html)
        self.assertNotIn('id="search-submit-btn" aria-label="Search"', self.v0_html)
        
        # Stage 2: Injected into Live DOM via shared/app-core.js for product action buttons
        app_core = (ROOT_DIR / "shared" / "app-core.js").read_text(encoding="utf-8")
        self.assertIn("addBtn.setAttribute('aria-label', 'Add item to cart')", app_core)
        
        # Stage 3: AXTree - Retained (Accessibility node computed name is present)
        ch2 = self.ax_data.get("channels", {}).get("channel_2_button_accessible_names", {})
        self.assertTrue(ch2.get("chromium_ax_tree_evidence", {}).get("retained_in_ax_tree", False))
        
        # Stage 4: Serializer - Retained because aria-label is in DEFAULT_INCLUDE_ATTRIBUTES
        self.assertIn("aria-label", DEFAULT_INCLUDE_ATTRIBUTES)
        
        # Stage 5 & 6: Prompt Buffer - Retained and Distinguishable from Baseline
        self.assertTrue(ch2.get("browser_use_serialized_observation", {}).get("retained_in_prompt", False))
        self.assertIn("CONCORDANT RETENTION", ch2.get("comparison_verdict", ""))

    # ── Channel 3: Non-Interactive ARIA (Critical Divergence) ─────────────────
    def test_channel_3_non_interactive_aria_pipeline(self):
        """Prove Critical Divergence: retained in Blink AXTree but stripped in serializer prompt."""
        ch3 = self.ax_data.get("channels", {}).get("channel_3_non_interactive_aria", {})
        
        # Stage 3: Present in AXTree (Blink builds accessible name for span)
        self.assertTrue(ch3.get("chromium_ax_tree_evidence", {}).get("retained_in_ax_tree", False))
        
        # Stage 4 & 5: Stripped in browser-use Serializer and Prompt Buffer
        self.assertFalse(ch3.get("browser_use_serialized_observation", {}).get("retained_in_prompt", True))
        self.assertIn("CRITICAL DIVERGENCE", ch3.get("comparison_verdict", ""))

    # ── Channel 4: Custom data-* Attributes (Reversed Divergence) ─────────────
    def test_channel_4_custom_data_attributes_pipeline(self):
        """Prove Reversed Divergence: absent in Blink AXTree, but present in serializer under extended whitelist."""
        # Stage 1: Present in Source HTML
        self.assertIn("data-action", self.v3_html)
        self.assertIn("data-category-slug", self.v3_html)
        self.assertNotIn("data-action", self.v0_html)
        
        # Stage 3: AXTree - Absent (Blink AXTree omits custom data-* attributes)
        ch4 = self.ax_data.get("channels", {}).get("channel_4_custom_data_attributes", {})
        self.assertFalse(ch4.get("chromium_ax_tree_evidence", {}).get("retained_in_ax_tree", True))
        
        # Stage 4: Serializer - Default whitelist strips, Extended whitelist includes
        self.assertNotIn("data-action", DEFAULT_INCLUDE_ATTRIBUTES)
        self.assertIn("data-action", protocol_v3_runner.EXTENDED_ATTRIBUTES)
        self.assertIn("data-product-id", protocol_v3_runner.EXTENDED_ATTRIBUTES)
        
        # Stage 5: Prompt Buffer - Retained under extended whitelist on interactive elements
        self.assertTrue(ch4.get("browser_use_serialized_observation", {}).get("extended_whitelist_has_data_action", False))
        self.assertIn("REVERSED DIVERGENCE", ch4.get("comparison_verdict", ""))

    # ── Channel 5: Visible Typography (Shared Control) ───────────────────────
    def test_channel_5_visible_typography_concordance(self):
        """Prove concordant 100% retention of visible text across all representations."""
        # Present across all variant sources
        for html in [self.v0_html, self.v1_html, self.v2_html, self.v3_html]:
            self.assertIn("TechMart", html)
            self.assertIn("Shop by Category", html)
            
        ch5 = self.ax_data.get("channels", {}).get("channel_5_visible_text", {})
        self.assertTrue(ch5.get("chromium_ax_tree_evidence", {}).get("retained_in_ax_tree", False))
        self.assertTrue(ch5.get("browser_use_serialized_observation", {}).get("retained_in_prompt", False))
        self.assertIn("CONCORDANT RETENTION", ch5.get("comparison_verdict", ""))

if __name__ == "__main__":
    unittest.main()

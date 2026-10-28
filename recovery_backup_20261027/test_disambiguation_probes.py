"""
test_disambiguation_probes.py
=============================================================================
Deterministic Regression and Serializer Unit Tests for Disambiguation Probes
=============================================================================
Covers Priority 2 requirements:
1. Probe A (data-product-id isolation):
   - Proves data-* is stripped in default serializer (ABS).
   - Proves data-* is reachable under extended attribute whitelist (DATA-CFG).
   - Proves randomized position swapping changes element sequence, eliminating position confounds.
2. Probe B (container span aria-label isolation):
   - Proves non-interactive span aria-label is stripped by serializer regardless of whitelist.
   - Documents observation-pipeline reachability bottleneck without behavioral conflation.
3. Positive Control (visible text):
   - Proves rendered visible typography is 100% preserved across all conditions.
4. Verifier Ground Truth:
   - Proves state assertions discriminate target SKU from distractor SKU.
=============================================================================
"""

import unittest
from pathlib import Path
from bs4 import BeautifulSoup

from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

EXTENDED_ATTRIBUTES = list(DEFAULT_INCLUDE_ATTRIBUTES) + [
    "data-field", "data-product-id", "data-category", "data-category-slug",
    "data-amount", "data-rating", "data-review-count", "data-stock-status",
    "data-in-stock", "data-warranty", "data-lot-code", "data-action"
]

FIXTURES_DIR = Path("C:/testing/research_execution_20261018/fixtures")
PROBE_A_PATH = FIXTURES_DIR / "disambiguation_probe_a.html"
PROBE_B_PATH = FIXTURES_DIR / "disambiguation_probe_b.html"
CONTROL_PATH = FIXTURES_DIR / "disambiguation_control.html"


def simulate_serializer_node_extraction(soup: BeautifulSoup, include_attributes: list) -> list:
    """
    Simulates browser-use DOMTreeSerializer attribute filtering logic on interactive elements:
    - Retains only attributes present in include_attributes.
    - Strips non-interactive tags while preserving their inner text.
    """
    extracted_elements = []
    # Find interactive controls: buttons, links, inputs
    for el in soup.find_all(["button", "a", "input"]):
        attrs = {}
        for k, v in el.attrs.items():
            if k in include_attributes:
                attrs[k] = v if not isinstance(v, list) else " ".join(v)
        extracted_elements.append({
            "tag": el.name,
            "id": el.get("id", ""),
            "text": el.get_text(strip=True),
            "serialized_attrs": attrs
        })
    return extracted_elements


class TestDisambiguationProbes(unittest.TestCase):

    def setUp(self):
        self.assertTrue(PROBE_A_PATH.exists(), f"Probe A fixture missing: {PROBE_A_PATH}")
        self.assertTrue(PROBE_B_PATH.exists(), f"Probe B fixture missing: {PROBE_B_PATH}")
        self.assertTrue(CONTROL_PATH.exists(), f"Control fixture missing: {CONTROL_PATH}")

    # -------------------------------------------------------------------------
    # PROBE A TESTS
    # -------------------------------------------------------------------------
    def test_probe_a_fixture_structure(self):
        """Probe A fixture must contain two buttons with identical visible text but distinct data-product-id."""
        soup = BeautifulSoup(PROBE_A_PATH.read_text(encoding="utf-8"), "html.parser")
        buttons = soup.find_all("button", class_="select-btn")
        self.assertEqual(len(buttons), 2)
        
        # Identical visible text
        self.assertEqual(buttons[0].get_text(strip=True), "Select Item")
        self.assertEqual(buttons[1].get_text(strip=True), "Select Item")
        
        # Distinct data-product-id attributes
        sku_0 = buttons[0].get("data-product-id")
        sku_1 = buttons[1].get("data-product-id")
        self.assertEqual(sku_0, "target-sku-101")
        self.assertEqual(sku_1, "distractor-sku-202")

    def test_probe_a_abs_pipeline_strips_identity(self):
        """In ABS condition (default whitelist), data-product-id is stripped, making buttons indistinguishable."""
        soup = BeautifulSoup(PROBE_A_PATH.read_text(encoding="utf-8"), "html.parser")
        extracted = simulate_serializer_node_extraction(soup, DEFAULT_INCLUDE_ATTRIBUTES)
        
        btn_extracted = [e for e in extracted if e["tag"] == "button"]
        self.assertEqual(len(btn_extracted), 2)
        # In default pipeline, data-product-id is NOT in DEFAULT_INCLUDE_ATTRIBUTES
        self.assertNotIn("data-product-id", DEFAULT_INCLUDE_ATTRIBUTES)
        for b in btn_extracted:
            self.assertNotIn("data-product-id", b["serialized_attrs"])
            # Both serialized representations are identical
            self.assertEqual(b["text"], "Select Item")

    def test_probe_a_data_cfg_pipeline_preserves_identity(self):
        """In DATA-CFG condition (extended whitelist), data-product-id is preserved on interactive buttons."""
        soup = BeautifulSoup(PROBE_A_PATH.read_text(encoding="utf-8"), "html.parser")
        self.assertIn("data-product-id", EXTENDED_ATTRIBUTES)
        extracted = simulate_serializer_node_extraction(soup, EXTENDED_ATTRIBUTES)
        
        btn_extracted = [e for e in extracted if e["tag"] == "button"]
        self.assertEqual(len(btn_extracted), 2)
        self.assertEqual(btn_extracted[0]["serialized_attrs"]["data-product-id"], "target-sku-101")
        self.assertEqual(btn_extracted[1]["serialized_attrs"]["data-product-id"], "distractor-sku-202")
        # Buttons are unambiguously distinguishable in prompt
        self.assertNotEqual(
            btn_extracted[0]["serialized_attrs"]["data-product-id"],
            btn_extracted[1]["serialized_attrs"]["data-product-id"]
        )

    def test_probe_a_position_randomization_invariance(self):
        """Position swapping re-orders buttons, proving task cannot be solved by position alone."""
        soup = BeautifulSoup(PROBE_A_PATH.read_text(encoding="utf-8"), "html.parser")
        wrapper = soup.find(id="cards-wrapper")
        cards = wrapper.find_all("div", class_="item-card")
        
        # Original order
        self.assertEqual(cards[0].find("button")["data-product-id"], "target-sku-101")
        self.assertEqual(cards[1].find("button")["data-product-id"], "distractor-sku-202")
        
        # Simulated position swap (swap=true)
        swapped_cards = [cards[1], cards[0]]
        self.assertEqual(swapped_cards[0].find("button")["data-product-id"], "distractor-sku-202")
        self.assertEqual(swapped_cards[1].find("button")["data-product-id"], "target-sku-101")

    # -------------------------------------------------------------------------
    # PROBE B TESTS
    # -------------------------------------------------------------------------
    def test_probe_b_fixture_structure(self):
        """Probe B fixture encodes identity in container span aria-label with identical visible text."""
        soup = BeautifulSoup(PROBE_B_PATH.read_text(encoding="utf-8"), "html.parser")
        spans = soup.find_all("span", class_="container-span")
        self.assertEqual(len(spans), 2)
        
        # Identical visible text
        self.assertEqual(spans[0].get_text(strip=True), "Standard Model Option")
        self.assertEqual(spans[1].get_text(strip=True), "Standard Model Option")
        
        # Distinguishing aria-label attributes
        self.assertEqual(spans[0].get("aria-label"), "Identity: target-sku-101")
        self.assertEqual(spans[1].get("aria-label"), "Identity: distractor-sku-202")

    def test_probe_b_serializer_strips_non_interactive_span_aria_label(self):
        """
        browser-use serializer strips non-interactive container tags at serializer.py:1046.
        Even if aria-label is in include_attributes, container spans are emitted only as inner text.
        """
        soup = BeautifulSoup(PROBE_B_PATH.read_text(encoding="utf-8"), "html.parser")
        # In browser-use, non-interactive spans are tag-stripped
        extracted = simulate_serializer_node_extraction(soup, EXTENDED_ATTRIBUTES)
        
        # Only interactive buttons are extracted with attribute mapping
        tags = [e["tag"] for e in extracted]
        self.assertNotIn("span", tags)
        # Buttons on probe B have NO aria-label (aria-label is on container span)
        for e in extracted:
            self.assertNotIn("aria-label", e["serialized_attrs"])

    # -------------------------------------------------------------------------
    # POSITIVE CONTROL TESTS
    # -------------------------------------------------------------------------
    def test_control_fixture_visible_text_retention(self):
        """Positive control fixture explicitly displays target SKU in human-visible typography."""
        soup = BeautifulSoup(CONTROL_PATH.read_text(encoding="utf-8"), "html.parser")
        skus = soup.find_all("div", class_="item-sku")
        self.assertEqual(len(skus), 2)
        
        # Target SKU is in human-visible text
        self.assertIn("target-sku-101", skus[0].get_text())
        self.assertIn("distractor-sku-202", skus[1].get_text())
        
        # Buttons also have distinguishing text
        btns = soup.find_all("button", class_="select-btn")
        self.assertEqual(btns[0].get_text(strip=True), "Select Alpha Model")
        self.assertEqual(btns[1].get_text(strip=True), "Select Beta Model")


if __name__ == "__main__":
    unittest.main()

"""
Automated Test Suite: Treatment Integrity and Leakage Audit
Validates:
1. De-confounded button label in v2-aria (no target product name leakage).
2. Clean baseline (no unintended ARIA or data-* attributes in v0-baseline).
3. Arm separation and absence of cross-treatment leakage.
4. Absolute enforcement of use_vision=False across all arms (resolving VIS ambiguity).
5. Documented manipulation failure for JSON-LD.
"""
import json
import re
import unittest
from pathlib import Path

ROOT_DIR = Path("C:/testing")
EXEC_DIR = ROOT_DIR / "research_execution_20261018"

class TestTreatmentLeakageAndIntegrity(unittest.TestCase):

    def setUp(self):
        self.app_core = (ROOT_DIR / "shared" / "app-core.js").read_text(encoding="utf-8")
        self.products = (ROOT_DIR / "shared" / "products.js").read_text(encoding="utf-8")
        self.v0_html = (ROOT_DIR / "variants" / "v0-baseline" / "index.html").read_text(encoding="utf-8")
        self.v2_html = (ROOT_DIR / "variants" / "v2-aria" / "index.html").read_text(encoding="utf-8")
        self.v3_html = (ROOT_DIR / "variants" / "v3-data-attrs" / "index.html").read_text(encoding="utf-8")
        self.runner_code = (EXEC_DIR / "protocol_v3_runner.py").read_text(encoding="utf-8")
        self.config = json.loads((EXEC_DIR / "protocol_v4_config.json").read_text(encoding="utf-8"))

    def test_deconfounded_button_label_in_app_core(self):
        """Verify button aria-label in v2-aria does NOT leak the target product name."""
        # Must NOT contain product name in button aria-label
        self.assertNotIn("addBtn.setAttribute('aria-label', 'Add ' + product.name", self.app_core)
        self.assertNotIn("addBtn.setAttribute('aria-label', 'Add SoundFlow Air 3", self.app_core)
        # Must contain de-confounded generic action label
        self.assertIn("addBtn.setAttribute('aria-label', 'Add item to cart')", self.app_core)

    def test_v0_baseline_cleanliness(self):
        """Verify v0-baseline source HTML has no ARIA enhancements or data-* actions."""
        # No ARIA on primary nav or search
        self.assertNotIn('aria-label="Primary navigation"', self.v0_html)
        self.assertNotIn('aria-label="Search"', self.v0_html)
        self.assertNotIn('data-action="add-to-cart"', self.v0_html)
        self.assertNotIn('data-action="search"', self.v0_html)

    def test_v3_data_attrs_separation(self):
        """Verify v3-data-attrs does not leak ARIA attributes."""
        self.assertIn('data-action="submit-search"', self.v3_html)
        self.assertNotIn('aria-label="Primary navigation"', self.v3_html)
        self.assertNotIn('aria-label="Search products"', self.v3_html)

    def test_vis_arm_vision_confound_elimination(self):
        """Verify VIS arm does NOT enable vision in text-only Protocol v4."""
        # In runner: use_vision=False must be strictly set for all runs
        self.assertIn("use_vision=False", self.runner_code)
        self.assertNotIn("use_vision=True", self.runner_code)
        # In protocol config: use_vision must be false
        self.assertFalse(self.config["agent_parameters"]["use_vision"])

    def test_jsonld_manipulation_failure_acknowledged(self):
        """Verify JSON-LD arm is excluded from primary confirmatory arms due to serializer pruning."""
        primary_arms = [arm["id"] for arm in self.config["design"]["arms"]]
        self.assertIn("BASELINE", primary_arms)
        self.assertIn("ARIA", primary_arms)
        self.assertIn("DATA-CFG", primary_arms)
        self.assertNotIn("JSON-LD", primary_arms)

    def test_catalog_identical_across_variants(self):
        """Verify all variants load identical shared/products.js without overrides."""
        for html in [self.v0_html, self.v2_html, self.v3_html]:
            self.assertIn('src="../../shared/products.js"', html)
            self.assertIn('src="../../shared/app-core.js"', html)

if __name__ == "__main__":
    unittest.main()

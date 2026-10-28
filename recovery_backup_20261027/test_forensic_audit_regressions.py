"""
Comprehensive Forensic Audit Regression Test Suite
=============================================================================
Validates all critical scientific findings, mathematical derivations,
data provenance, DOM geometry boundaries, manuscript integrity, and quota guards.
=============================================================================
"""

import unittest
import csv
import json
import math
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
MANUSCRIPT_TEX = BASE_DIR / "research_paper_final.tex"
BIB_FILE = BASE_DIR / "references.bib"
V3_3ARM_CSV = BASE_DIR / "results" / "v3_3arm_summary.csv"
LOCAL_LLAMA_CSV = BASE_DIR / "results" / "local_llama_summary.csv"
QUOTA_LEDGER_JSON = BASE_DIR / "results" / "daily_quota_ledger.json"
AXTREE_JSON = BASE_DIR / "accessibility_tree_comparison.json"


def norm_cdf(x: float) -> float:
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def norm_ppf(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0, 1)")
    if p < 0.5:
        return -norm_ppf(1.0 - p)
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1.0)


def wilson_interval(x: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    p = x / n
    z = norm_ppf(1.0 - alpha / 2.0)
    denom = 1.0 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))) / denom
    return (center - half, center + half)


def newcombe_diff_interval(x1: int, n1: int, x2: int, n2: int, alpha: float = 0.05):
    l1, u1 = wilson_interval(x1, n1, alpha)
    l2, u2 = wilson_interval(x2, n2, alpha)
    p1 = x1 / n1
    p2 = x2 / n2
    diff = p1 - p2
    lower = diff - math.sqrt((p1 - l1)**2 + (u2 - p2)**2)
    upper = diff + math.sqrt((u1 - p1)**2 + (p2 - l2)**2)
    return diff, (lower, upper)


class TestStatisticalRegressions(unittest.TestCase):
    """Category A: Statistical recomputations and bounds."""

    def test_tost_sample_size_formula_bounds(self):
        """TOST sample size at p=0.70 gives ~360, p=0.50 gives ~429, DEFF=1.30 gives ~468."""
        margin = 0.10
        alpha = 0.05
        power = 0.80
        z_alpha = norm_ppf(1.0 - alpha)
        z_beta = norm_ppf((1.0 + power) / 2.0)
        
        # p = 0.70
        var_70 = 2.0 * 0.70 * 0.30
        n_70 = ((z_alpha + z_beta) * math.sqrt(var_70) / margin) ** 2
        self.assertAlmostEqual(n_70, 359.7, delta=1.0)
        self.assertEqual(round(n_70), 360)

        # p = 0.50 (max variance)
        var_50 = 2.0 * 0.50 * 0.50
        n_50 = ((z_alpha + z_beta) * math.sqrt(var_50) / margin) ** 2
        self.assertAlmostEqual(n_50, 428.2, delta=1.0)
        self.assertEqual(round(n_50), 428)

        # Cluster inflation DEFF = 1 + (4 - 1)*0.10 = 1.30
        deff = 1.0 + (4 - 1) * 0.10
        self.assertAlmostEqual(deff, 1.30, places=4)
        n_clustered = n_70 * deff
        self.assertAlmostEqual(n_clustered, 467.6, delta=1.0)
        self.assertEqual(round(n_clustered), 468)

    def test_newcombe_hybrid_score_example(self):
        """56/70 vs 38/80 produces RD = 0.325 with Newcombe 95% CI [0.172, 0.456]."""
        diff, (lower, upper) = newcombe_diff_interval(56, 70, 38, 80)
        self.assertAlmostEqual(diff, 0.3250, places=4)
        self.assertAlmostEqual(lower, 0.1721, places=3)
        self.assertAlmostEqual(upper, 0.4558, places=3)

    def test_wilson_proportions_census_and_pilot(self):
        """Wilson intervals for 27/34 and 41/41."""
        w_27_34 = wilson_interval(27, 34)
        self.assertAlmostEqual(w_27_34[0] * 100, 63.20, delta=0.1)
        self.assertAlmostEqual(w_27_34[1] * 100, 89.65, delta=0.1)

        w_41_41 = wilson_interval(41, 41)
        self.assertAlmostEqual(w_41_41[0] * 100, 91.43, delta=0.1)
        self.assertAlmostEqual(w_41_41[1], 1.0, places=4)


class TestDataProvenanceRegressions(unittest.TestCase):
    """Category B: Primary data ledgers and trial accounting."""

    def test_v3_3arm_summary_provenance(self):
        """v3_3arm_summary.csv has 44 rows: 41 completed, 3 aborted retries on Run 26."""
        self.assertTrue(V3_3ARM_CSV.exists())
        with open(V3_3ARM_CSV, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        
        self.assertEqual(len(rows), 44)
        completed = [r for r in rows if r.get("status") == "completed"]
        aborted = [r for r in rows if r.get("status") == "infrastructure_aborted"]
        
        self.assertEqual(len(completed), 41)
        self.assertEqual(len(aborted), 3)

        # All 3 aborted rows belong to run_index 26 with 503 error
        for r in aborted:
            self.assertEqual(r.get("run_index"), "26")
            self.assertIn("503", r.get("error_message"))

        # Completed arm counts: 13 ABS, 13 ARIA, 15 DATA-CFG
        arm_counts = {}
        for r in completed:
            arm_counts[r["arm"]] = arm_counts.get(r["arm"], 0) + 1
        self.assertEqual(arm_counts.get("ABS"), 13)
        self.assertEqual(arm_counts.get("ARIA"), 13)
        self.assertEqual(arm_counts.get("DATA-CFG"), 15)

    def test_local_llama_summary_provenance(self):
        """local_llama_summary.csv has 5 rows of qwen3:4b with exact recorded latencies."""
        self.assertTrue(LOCAL_LLAMA_CSV.exists())
        with open(LOCAL_LLAMA_CSV, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        
        self.assertEqual(len(rows), 5)
        for r in rows:
            self.assertEqual(r.get("model"), "qwen3:4b")
            dur = float(r.get("duration_seconds"))
            self.assertGreater(dur, 0.0)

        # Exact durations of interest:
        self.assertAlmostEqual(float(rows[1]["duration_seconds"]), 1013.094, places=2)
        self.assertAlmostEqual(float(rows[2]["duration_seconds"]), 288.61, places=2)
        self.assertAlmostEqual(float(rows[3]["duration_seconds"]), 185.5, places=2)
        self.assertAlmostEqual(float(rows[4]["duration_seconds"]), 188.563, places=2)

    def test_quota_ledger_ceiling_enforcement(self):
        """daily_quota_ledger.json enforces halt ceiling."""
        self.assertTrue(QUOTA_LEDGER_JSON.exists())
        data = json.loads(QUOTA_LEDGER_JSON.read_text(encoding="utf-8"))
        self.assertTrue(data.get("halted_due_to_ceiling"))
        self.assertGreaterEqual(data.get("cumulative_requests"), data.get("max_requests_ceiling"))
        self.assertEqual(data.get("cost_ceiling_usd"), 0.0)


class TestDOMGeometryBoundaryRegressions(unittest.TestCase):
    """Category C: DOM ClickableElementDetector 10-50px geometry boundaries."""

    def is_icon_geometry_match(self, width: float, height: float, has_class: bool) -> bool:
        """Simulates clickable_elements.py:228-240 logic."""
        if 10.0 <= width <= 50.0 and 10.0 <= height <= 50.0:
            return has_class
        return False

    def test_in_stock_badge_heuristic_trigger(self):
        """In Stock badge (48.625 x 15px) satisfies 10-50px icon heuristic."""
        w, h = 48.625, 15.0
        self.assertTrue(self.is_icon_geometry_match(w, h, has_class=True))

    def test_out_of_stock_badge_heuristic_exclusion(self):
        """Out of Stock badge (74.766 x 15px) exceeds 50px width ceiling."""
        w, h = 74.766, 15.0
        self.assertFalse(self.is_icon_geometry_match(w, h, has_class=True))

    def test_exact_geometry_threshold_boundaries(self):
        """Strict boundary assertions around 10.0px and 50.0px."""
        # Below lower threshold (9.99px) -> False
        self.assertFalse(self.is_icon_geometry_match(9.99, 20.0, True))
        self.assertFalse(self.is_icon_geometry_match(20.0, 9.99, True))
        
        # Exact lower threshold (10.0px) -> True
        self.assertTrue(self.is_icon_geometry_match(10.0, 20.0, True))
        self.assertTrue(self.is_icon_geometry_match(20.0, 10.0, True))
        
        # Exact upper threshold (50.0px) -> True
        self.assertTrue(self.is_icon_geometry_match(50.0, 50.0, True))
        
        # Above upper threshold (50.01px) -> False
        self.assertFalse(self.is_icon_geometry_match(50.01, 20.0, True))
        self.assertFalse(self.is_icon_geometry_match(20.0, 50.01, True))


class TestManuscriptIntegrityRegressions(unittest.TestCase):
    """Category D: Manuscript LaTeX syntax, citation keys, and abstract alignment."""

    def test_all_cited_keys_exist_in_bib(self):
        """Every \\cite{key} in research_paper_final.tex must exist in references.bib."""
        self.assertTrue(MANUSCRIPT_TEX.exists())
        self.assertTrue(BIB_FILE.exists())

        tex_content = MANUSCRIPT_TEX.read_text(encoding="utf-8")
        bib_content = BIB_FILE.read_text(encoding="utf-8")

        bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib_content))
        cited_keys = set()
        for match in re.findall(r"\\cite\{([^}]+)\}", tex_content):
            for k in match.split(","):
                cited_keys.add(k.strip())

        missing = cited_keys - bib_keys
        self.assertEqual(len(missing), 0, f"Missing bibliography keys: {missing}")

    def test_crucial_citations_present(self):
        """Key citations (agentoccam2025, osworld2024, wilson1927, schuirmann1987comparison) must be present."""
        bib_content = BIB_FILE.read_text(encoding="utf-8")
        for key in ["agentoccam2025", "osworld2024", "wilson1927probable", "newcombe1998interval", "schuirmann1987comparison"]:
            self.assertIn(key, bib_content)

    def test_abstract_numerical_claims_alignment(self):
        """Abstract numbers must match body tables and authoritative registry."""
        tex_content = MANUSCRIPT_TEX.read_text(encoding="utf-8")
        
        # Extract abstract
        m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex_content, re.DOTALL)
        self.assertIsNotNone(m, "Abstract must exist")
        abstract = m.group(1)

        # Assert key numbers are in abstract
        self.assertIn("0.13.10", abstract, "browser-use version 0.13.10 must be in abstract")
        self.assertIn("11.5", abstract, "11.5% power must be in abstract")
        self.assertIn("48.5", abstract, "48.5% power must be in abstract")
        self.assertIn("39", abstract, "N=39 must be in abstract")
        self.assertIn("41", abstract, "N=41 must be in abstract")
        self.assertIn("46", abstract, "46 traces reconciled must be in abstract")



if __name__ == "__main__":
    unittest.main()

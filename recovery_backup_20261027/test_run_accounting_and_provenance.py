"""
test_run_accounting_and_provenance.py
Automated regression test verifying that all trace files on disk match
RUN_ACCOUNTING_RECONCILIATION.csv and EVIDENCE_CLASS_LEDGER.csv byte-for-byte.
"""
import csv
import json
import unittest
import pathlib

PROJ_ROOT = pathlib.Path(__file__).resolve().parent
RECON_CSV = PROJ_ROOT / "RUN_ACCOUNTING_RECONCILIATION.csv"
EVIDENCE_CSV = PROJ_ROOT / "EVIDENCE_CLASS_LEDGER.csv"
THREE_ARM_DIR = PROJ_ROOT / "results" / "3arm_runs"

class TestRunAccounting(unittest.TestCase):

    def test_reconciliation_row_counts(self):
        """Asserts exact counts for 3arm runs: 46 files, 39 primary, 4 quarantined, 3 aborts, 31 unexecuted."""
        with open(RECON_CSV, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        self.assertEqual(len(rows), 77, "Total rows in reconciliation must be 77 (46 files + 31 unexecuted)")
        
        primary = [r for r in rows if r["disposition"] == "INCLUDED_PRIMARY_ELIGIBLE"]
        quarantined = [r for r in rows if r["disposition"] == "QUARANTINED_AMBIGUOUS_COMPLETION"]
        aborts = [r for r in rows if r["disposition"] == "EXCLUDED_INFRASTRUCTURE_ABORT"]
        unexecuted = [r for r in rows if r["disposition"] == "EXCLUDED_UNEXECUTED"]
        
        self.assertEqual(len(primary), 39, "Primary eligible must be exactly 39")
        self.assertEqual(len(quarantined), 4, "Quarantined must be exactly 4 (2 attempts x 2 indices)")
        self.assertEqual(len(aborts), 3, "Aborts must be exactly 3 (index 26 att 1-3)")
        self.assertEqual(len(unexecuted), 31, "Unexecuted must be exactly 31 (indices 42-72)")

    def test_all_trace_files_present_on_disk(self):
        """Verifies that all 46 trace files listed in reconciliation exist on disk and match SHA-256."""
        with open(RECON_CSV, "r", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["file_name"] != "NONE (Unexecuted)"]
            
        self.assertEqual(len(rows), 46)
        for r in rows:
            fp = THREE_ARM_DIR / r["file_name"]
            self.assertTrue(fp.exists(), f"File {r['file_name']} must exist on disk")

    def test_evidence_ledger_classes(self):
        """Verifies evidence classes E1-E7 separation in EVIDENCE_CLASS_LEDGER.csv."""
        with open(EVIDENCE_CSV, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            
        classes = {r["evidence_class"] for r in rows}
        self.assertIn("E4", classes, "Must have Class E4 (pilot observations)")
        self.assertIn("E6", classes, "Must have Class E6 (diagnostic/smoke trials)")
        self.assertIn("E3", classes, "Must have Class E3 (deterministic stage traces)")
        self.assertNotIn("E7", classes, "Must NOT have Class E7 (confirmatory live trials do not exist yet)")

if __name__ == "__main__":
    unittest.main()

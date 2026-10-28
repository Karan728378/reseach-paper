"""
test_data_reconciliation_and_provenance.py
=============================================================================
Regression and Invariant Test Suite for Protocol v3/v4 Data Reconciliation
=============================================================================
Covers 20 core invariants required by Phase 5:
 1. Three infrastructure-aborted attempts followed by one valid completion.
 2. Two completed attempts for the same scheduled unit.
 3. Missing attempt number inferred from filename.
 4. Malformed JSON handled and reported without silently disappearing.
 5. Missing or malformed timestamps flagged.
 6. Metadata collision across attempts assigned to the same scheduled unit.
 7. Deterministic output regardless of filesystem enumeration order.
 8. Exact raw-versus-clean CSV record reconciliation.
 9. A retry cannot silently inflate the behavioral denominator.
10. An infrastructure-aborted attempt cannot silently count as a behavioral failure.
11. A completed attempt without required verifier evidence cannot automatically become a valid outcome.
12. A completed attempt without required treatment-delivery evidence cannot automatically become a valid outcome.
13. Duplicate completion handling follows documented protocol and otherwise quarantines.
14. Original input hashes remain unchanged after reconciliation.
15. Missing required input files produce a clear error and nonzero exit status.
16. Downstream analysis excludes ineligible and quarantined units.
17. Arm counts and denominators agree with the reconciled eligible-unit table.
18. CSV output contains no unintended duplicate scheduled-unit rows.
19. Every included unit has traceable source-file provenance.
20. Re-running reconciliation on unchanged inputs yields identical output hashes.
=============================================================================
"""

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from reconcile_v3_results import (
    parse_attempt_file,
    load_schedule,
    reconcile_experiment_data,
    write_reconciled_outputs,
    sha256_file
)
from analyze_v3_results import validate_and_load_summary, analyze_dataset


WORKSPACE_ROOT = Path(__file__).resolve().parent
REAL_SCHEDULE_PATH = WORKSPACE_ROOT / "proposed_3arm_schedule.csv"
REAL_RUNS_DIR = WORKSPACE_ROOT / "results" / "3arm_runs"
REAL_RAW_CSV_PATH = WORKSPACE_ROOT / "results" / "v3_3arm_summary_raw.csv"
REAL_CLEAN_CSV_PATH = WORKSPACE_ROOT / "results" / "v3_3arm_summary.csv"


class TestDataReconciliationAndProvenance(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_reconciliation_"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_minimal_schedule(self, rows=None) -> Path:
        sched_path = self.temp_dir / "test_schedule.csv"
        fieldnames = ["run_index", "block_id", "within_block_order", "arm", "task_id", "variant_mapping", "target_entity"]
        if rows is None:
            rows = [
                {"run_index": 1, "block_id": 1, "within_block_order": 1, "arm": "DATA-CFG", "task_id": "T1", "variant_mapping": "v3-data-attrs", "target_entity": "wh-001"},
                {"run_index": 2, "block_id": 1, "within_block_order": 2, "arm": "ABS", "task_id": "T2", "variant_mapping": "v0-baseline", "target_entity": "mkp-001"},
                {"run_index": 3, "block_id": 1, "within_block_order": 3, "arm": "ARIA", "task_id": "T3", "variant_mapping": "v1-aria-landmarks", "target_entity": "gt-001"}
            ]
        with open(sched_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return sched_path

    def _create_attempt_json(
        self,
        runs_dir: Path,
        filename: str,
        run_index: int,
        attempt_number: int = None,
        arm: str = "DATA-CFG",
        task_id: str = "T1",
        block_id: int = 1,
        variant_mapping: str = None,
        target_entity: str = "wh-001",
        status: str = "completed",
        error_message: str = "",
        success: bool = True,
        score: float = 1.0,
        total_steps: int = 4,
        t_start: str = "2026-10-24T12:00:00.000000",
        t_end: str = "2026-10-24T12:00:15.000000",
        with_verifier: bool = True,
        with_treatment: bool = True
    ) -> Path:
        if variant_mapping is None:
            if arm == "DATA-CFG":
                variant_mapping = "v3-data-attrs"
            elif arm == "ARIA":
                variant_mapping = "v1-aria-landmarks"
            else:
                variant_mapping = "v0-baseline"
        runs_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "run_index": run_index,
            "block_id": block_id,
            "within_block_order": 1,
            "arm": arm,
            "task_id": task_id,
            "variant_mapping": variant_mapping,
            "target_entity": target_entity,
            "model": "test-model",
            "timestamps": {"start": t_start, "end": t_end},
            "total_time_seconds": 15.0,
            "total_steps": total_steps,
            "status": status,
            "error_message": error_message
        }
        if attempt_number is not None:
            data["attempt_number"] = attempt_number
        if with_verifier:
            data["verifier_result"] = {"success": success, "score": score, "details": {}}
        if with_treatment:
            data["treatment_delivery"] = {
                "arm": arm,
                "treatment_attribute_observed": True,
                "evidence": f"Observation verified for {arm}"
            }
        file_path = runs_dir / filename
        file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return file_path

    # -------------------------------------------------------------------------
    # TEST 1: Three infrastructure-aborted attempts followed by one valid completion
    # -------------------------------------------------------------------------
    def test_01_three_infra_aborts_followed_by_valid_completion(self):
        """Run 26 scenario: 3 transient 503 aborts + 1 completion yields RECOVERED_AFTER_INFRA_ABORT."""
        sched = self._create_minimal_schedule([
            {"run_index": 26, "block_id": 1, "within_block_order": 1, "arm": "ABS", "task_id": "T6", "variant_mapping": "v0-baseline", "target_entity": "wh-001"}
        ])
        runs_dir = self.temp_dir / "runs_test_01"
        self._create_attempt_json(runs_dir, "run_026.json", 26, 1, arm="ABS", task_id="T6", status="infrastructure_aborted", error_message="503 UNAVAILABLE", success=False, score=0.0)
        self._create_attempt_json(runs_dir, "run_026_attempt_2.json", 26, 2, arm="ABS", task_id="T6", status="infrastructure_aborted", error_message="503 UNAVAILABLE", success=False, score=0.0)
        self._create_attempt_json(runs_dir, "run_026_attempt_3.json", 26, 3, arm="ABS", task_id="T6", status="infrastructure_aborted", error_message="503 UNAVAILABLE", success=False, score=0.0)
        self._create_attempt_json(runs_dir, "run_026_attempt_4.json", 26, 4, arm="ABS", task_id="T6", status="completed", error_message="", success=True, score=1.0)

        res = reconcile_experiment_data(sched, runs_dir)
        unit = res["reconciled_units"][0]
        self.assertEqual(unit["reconciliation_category"], "RECOVERED_AFTER_INFRA_ABORT")
        self.assertEqual(unit["eligibility_for_primary_analysis"], "ELIGIBLE")
        self.assertEqual(unit["quarantine_status"], "NONE")
        self.assertEqual(unit["total_attempts_recorded"], 4)
        self.assertEqual(unit["selected_source_file"], "run_026_attempt_4.json")
        self.assertTrue(unit["success"])
        self.assertEqual(res["audit_summary"]["counts"]["recovered_after_infra_aborts"], 1)

    # -------------------------------------------------------------------------
    # TEST 2: Two completed attempts for the same scheduled unit
    # -------------------------------------------------------------------------
    def test_02_two_completed_attempts_quarantines_unit(self):
        """Runs 34/38 scenario: Multiple completed attempts without pre-registered rule must be quarantined."""
        sched = self._create_minimal_schedule([
            {"run_index": 34, "block_id": 2, "within_block_order": 16, "arm": "DATA-CFG", "task_id": "T2", "variant_mapping": "v3-data-attrs", "target_entity": "mkp-001"}
        ])
        runs_dir = self.temp_dir / "runs_test_02"
        self._create_attempt_json(runs_dir, "run_034.json", 34, 1, arm="DATA-CFG", task_id="T2", block_id=2, variant_mapping="v3-data-attrs", target_entity="mkp-001", status="completed", success=True, score=1.0)
        self._create_attempt_json(runs_dir, "run_034_attempt_2.json", 34, 2, arm="DATA-CFG", task_id="T2", block_id=2, variant_mapping="v3-data-attrs", target_entity="mkp-001", status="completed", success=True, score=1.0)

        res = reconcile_experiment_data(sched, runs_dir)
        unit = res["reconciled_units"][0]
        self.assertEqual(unit["reconciliation_category"], "AMBIGUOUS_MULTIPLE_COMPLETIONS")
        self.assertEqual(unit["quarantine_status"], "QUARANTINED")
        self.assertEqual(unit["eligibility_for_primary_analysis"], "INELIGIBLE_QUARANTINED")
        self.assertEqual(unit["status"], "quarantined")
        self.assertEqual(unit["total_attempts_recorded"], 2)

    # -------------------------------------------------------------------------
    # TEST 3: Missing attempt number inferred from filename
    # -------------------------------------------------------------------------
    def test_03_missing_attempt_number_inferred_from_filename(self):
        """When attempt_number is omitted from JSON body, filename suffix _attempt_X is correctly parsed."""
        runs_dir = self.temp_dir / "runs_test_03"
        f1 = self._create_attempt_json(runs_dir, "run_010.json", 10, attempt_number=None)
        f2 = self._create_attempt_json(runs_dir, "run_010_attempt_3.json", 10, attempt_number=None)

        p1 = parse_attempt_file(f1)
        p2 = parse_attempt_file(f2)
        self.assertEqual(p1["attempt_number"], 1)
        self.assertEqual(p2["attempt_number"], 3)

    # -------------------------------------------------------------------------
    # TEST 4: Malformed JSON handled and reported without silently disappearing
    # -------------------------------------------------------------------------
    def test_04_malformed_json_raises_explicit_error(self):
        """Malformed JSON must raise ValueError with filename rather than failing silently."""
        runs_dir = self.temp_dir / "runs_test_04"
        runs_dir.mkdir(parents=True, exist_ok=True)
        bad_json = runs_dir / "run_099.json"
        bad_json.write_text("{'invalid_json': True, missing_quotes}", encoding="utf-8")

        with self.assertRaises(ValueError) as ctx:
            parse_attempt_file(bad_json)
        self.assertIn("run_099.json", str(ctx.exception))

    # -------------------------------------------------------------------------
    # TEST 5: Missing or malformed timestamps flagged
    # -------------------------------------------------------------------------
    def test_05_missing_timestamps_flagged(self):
        """Attempt files with empty or missing timestamps must report timestamp_error."""
        runs_dir = self.temp_dir / "runs_test_05"
        f = self._create_attempt_json(runs_dir, "run_001.json", 1, t_start="", t_end="")
        parsed = parse_attempt_file(f)
        self.assertIsNotNone(parsed["timestamp_error"])
        self.assertIn("Missing or incomplete timestamps", parsed["timestamp_error"])

    # -------------------------------------------------------------------------
    # TEST 6: Metadata collision across attempts assigned to same scheduled unit
    # -------------------------------------------------------------------------
    def test_06_metadata_collision_detected_and_quarantined(self):
        """If attempt metadata disagrees with schedule arm/task, it is flagged as METADATA_COLLISION."""
        sched = self._create_minimal_schedule([
            {"run_index": 5, "block_id": 1, "within_block_order": 1, "arm": "ABS", "task_id": "T1", "variant_mapping": "v0-baseline", "target_entity": "wh-001"}
        ])
        runs_dir = self.temp_dir / "runs_test_06"
        # Attempt claims arm 'DATA-CFG' while schedule expects 'ABS'
        self._create_attempt_json(runs_dir, "run_005.json", 5, arm="DATA-CFG", task_id="T1", variant_mapping="v0-baseline")

        res = reconcile_experiment_data(sched, runs_dir)
        unit = res["reconciled_units"][0]
        self.assertEqual(unit["reconciliation_category"], "METADATA_COLLISION")
        self.assertEqual(unit["quarantine_status"], "QUARANTINED")
        self.assertEqual(res["audit_summary"]["counts"]["metadata_collisions"], 1)

    # -------------------------------------------------------------------------
    # TEST 7: Deterministic output regardless of filesystem enumeration order
    # -------------------------------------------------------------------------
    def test_07_deterministic_output_regardless_of_file_order(self):
        """Reconciliation result is identical regardless of disk file creation sequence."""
        sched = self._create_minimal_schedule()
        runs_dir1 = self.temp_dir / "runs_order_a"
        runs_dir2 = self.temp_dir / "runs_order_b"
        
        # Order A: 3, 1, 2
        self._create_attempt_json(runs_dir1, "run_003.json", 3, arm="ARIA", task_id="T3", variant_mapping="v1-aria-landmarks", target_entity="gt-001")
        self._create_attempt_json(runs_dir1, "run_001.json", 1, arm="DATA-CFG", task_id="T1", variant_mapping="v3-data-attrs", target_entity="wh-001")
        self._create_attempt_json(runs_dir1, "run_002.json", 2, arm="ABS", task_id="T2", variant_mapping="v0-baseline", target_entity="mkp-001")

        # Order B: 1, 2, 3
        self._create_attempt_json(runs_dir2, "run_001.json", 1, arm="DATA-CFG", task_id="T1", variant_mapping="v3-data-attrs", target_entity="wh-001")
        self._create_attempt_json(runs_dir2, "run_002.json", 2, arm="ABS", task_id="T2", variant_mapping="v0-baseline", target_entity="mkp-001")
        self._create_attempt_json(runs_dir2, "run_003.json", 3, arm="ARIA", task_id="T3", variant_mapping="v1-aria-landmarks", target_entity="gt-001")

        res_a = reconcile_experiment_data(sched, runs_dir1)
        res_b = reconcile_experiment_data(sched, runs_dir2)

        indices_a = [u["run_index"] for u in res_a["reconciled_units"]]
        indices_b = [u["run_index"] for u in res_b["reconciled_units"]]
        self.assertEqual(indices_a, indices_b)
        self.assertEqual(res_a["reconciled_units"], res_b["reconciled_units"])

    # -------------------------------------------------------------------------
    # TEST 8: Exact raw-versus-clean CSV record reconciliation on real data
    # -------------------------------------------------------------------------
    def test_08_exact_raw_versus_clean_csv_reconciliation(self):
        """Verifies exactly 46 raw rows and 44 clean rows, with Runs 34 and 38 explaining the delta."""
        self.assertTrue(REAL_RAW_CSV_PATH.exists())
        self.assertTrue(REAL_CLEAN_CSV_PATH.exists())

        with open(REAL_RAW_CSV_PATH, "r", encoding="utf-8") as f:
            raw_rows = list(csv.DictReader(f))
        with open(REAL_CLEAN_CSV_PATH, "r", encoding="utf-8") as f:
            clean_rows = list(csv.DictReader(f))

        self.assertEqual(len(raw_rows), 46)
        self.assertEqual(len(clean_rows), 44)

        clean_keys = set((r["run_index"], r["timestamp_start"]) for r in clean_rows)
        diff_rows = [r for r in raw_rows if (r["run_index"], r["timestamp_start"]) not in clean_keys]
        self.assertEqual(len(diff_rows), 2)
        diff_indices = set(r["run_index"] for r in diff_rows)
        self.assertEqual(diff_indices, {"34", "38"})

    # -------------------------------------------------------------------------
    # TEST 9: A retry cannot silently inflate the behavioral denominator
    # -------------------------------------------------------------------------
    def test_09_retries_do_not_inflate_behavioral_denominator(self):
        """A unit with 4 attempts (Run 26) contributes exactly 1 unit to the denominator."""
        res = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR)
        run_26_units = [u for u in res["reconciled_units"] if u["run_index"] == 26]
        self.assertEqual(len(run_26_units), 1)
        self.assertEqual(run_26_units[0]["total_attempts_recorded"], 4)
        
        eligible_units = [u for u in res["reconciled_units"] if u["eligibility_for_primary_analysis"] == "ELIGIBLE"]
        run_26_eligible = [u for u in eligible_units if u["run_index"] == 26]
        self.assertEqual(len(run_26_eligible), 1)

    # -------------------------------------------------------------------------
    # TEST 10: Infrastructure aborts cannot silently count as behavioral failures
    # -------------------------------------------------------------------------
    def test_10_infra_aborts_never_count_as_behavioral_failures(self):
        """Pure infrastructure aborts receive status != 'completed' and do not enter behavioral failures."""
        sched = self._create_minimal_schedule([
            {"run_index": 7, "block_id": 1, "within_block_order": 1, "arm": "ABS", "task_id": "T1", "variant_mapping": "v0-baseline", "target_entity": "wh-001"}
        ])
        runs_dir = self.temp_dir / "runs_test_10"
        self._create_attempt_json(runs_dir, "run_007.json", 7, arm="ABS", task_id="T1", variant_mapping="v0-baseline", target_entity="wh-001", status="infrastructure_aborted", error_message="HTTP 503 UNAVAILABLE", success=False, score=0.0)

        res = reconcile_experiment_data(sched, runs_dir)
        unit = res["reconciled_units"][0]
        self.assertEqual(unit["reconciliation_category"], "INFRASTRUCTURE_ABORTED_ONLY")
        self.assertEqual(unit["eligibility_for_primary_analysis"], "INELIGIBLE_INFRA_ABORT")
        
        # Must not be counted in eligible behavioral units
        eligible_units = [u for u in res["reconciled_units"] if u["eligibility_for_primary_analysis"] == "ELIGIBLE"]
        self.assertEqual(len(eligible_units), 0)

    # -------------------------------------------------------------------------
    # TEST 11: Completed attempt without required verifier evidence cannot become valid
    # -------------------------------------------------------------------------
    def test_11_unverified_completed_attempt_is_ineligible(self):
        """A completed trial missing verifier_result is marked UNVERIFIED_COMPLETION and INELIGIBLE."""
        sched = self._create_minimal_schedule([
            {"run_index": 1, "block_id": 1, "within_block_order": 1, "arm": "DATA-CFG", "task_id": "T1", "variant_mapping": "v3-data-attrs", "target_entity": "wh-001"}
        ])
        runs_dir = self.temp_dir / "runs_test_11"
        self._create_attempt_json(runs_dir, "run_001.json", 1, status="completed", with_verifier=False)

        res = reconcile_experiment_data(sched, runs_dir)
        unit = res["reconciled_units"][0]
        self.assertEqual(unit["reconciliation_category"], "UNVERIFIED_COMPLETION")
        self.assertEqual(unit["eligibility_for_primary_analysis"], "INELIGIBLE_MISSING_VERIFIER")

    # -------------------------------------------------------------------------
    # TEST 12: Completed attempt without required treatment delivery evidence is ineligible
    # -------------------------------------------------------------------------
    def test_12_missing_treatment_delivery_evidence_is_ineligible(self):
        """A completed trial missing treatment_delivery observation evidence is marked INELIGIBLE."""
        sched = self._create_minimal_schedule([
            {"run_index": 1, "block_id": 1, "within_block_order": 1, "arm": "DATA-CFG", "task_id": "T1", "variant_mapping": "v3-data-attrs", "target_entity": "wh-001"}
        ])
        runs_dir = self.temp_dir / "runs_test_12"
        self._create_attempt_json(runs_dir, "run_001.json", 1, status="completed", with_treatment=False)

        res = reconcile_experiment_data(sched, runs_dir)
        unit = res["reconciled_units"][0]
        self.assertEqual(unit["reconciliation_category"], "INVALID_TREATMENT_DELIVERY")
        self.assertEqual(unit["eligibility_for_primary_analysis"], "INELIGIBLE_MISSING_TREATMENT")

    # -------------------------------------------------------------------------
    # TEST 13: Duplicate completion handling follows protocol and otherwise quarantines
    # -------------------------------------------------------------------------
    def test_13_duplicate_completion_handling_and_quarantine(self):
        """Verifies that Runs 34 and 38 are quarantined in real dataset audit."""
        res = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR)
        quarantined = [u for u in res["reconciled_units"] if u["quarantine_status"] == "QUARANTINED"]
        q_indices = sorted([u["run_index"] for u in quarantined])
        self.assertEqual(q_indices, [34, 38])

    # -------------------------------------------------------------------------
    # TEST 14: Original input hashes remain unchanged after reconciliation
    # -------------------------------------------------------------------------
    def test_14_original_input_hashes_unaltered(self):
        """Verifies that running reconciliation does not modify input CSVs or JSON files."""
        raw_hash_before = sha256_file(REAL_RAW_CSV_PATH)
        clean_hash_before = sha256_file(REAL_CLEAN_CSV_PATH)
        sched_hash_before = sha256_file(REAL_SCHEDULE_PATH)
        
        # Run reconciliation
        res = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR, REAL_RAW_CSV_PATH, REAL_CLEAN_CSV_PATH)
        out_csv = self.temp_dir / "out.csv"
        out_json = self.temp_dir / "out.json"
        out_md = self.temp_dir / "out.md"
        write_reconciled_outputs(res, out_csv, out_json, out_md)

        self.assertEqual(sha256_file(REAL_RAW_CSV_PATH), raw_hash_before)
        self.assertEqual(sha256_file(REAL_CLEAN_CSV_PATH), clean_hash_before)
        self.assertEqual(sha256_file(REAL_SCHEDULE_PATH), sched_hash_before)

    # -------------------------------------------------------------------------
    # TEST 15: Missing required input files produce clear error and nonzero exit
    # -------------------------------------------------------------------------
    def test_15_missing_input_files_raise_filenotfound(self):
        """Missing schedule or runs directory raises explicit FileNotFoundError."""
        nonexistent = self.temp_dir / "nonexistent.csv"
        with self.assertRaises(FileNotFoundError):
            reconcile_experiment_data(nonexistent, REAL_RUNS_DIR)

    # -------------------------------------------------------------------------
    # TEST 16: Downstream analysis excludes ineligible and quarantined units
    # -------------------------------------------------------------------------
    def test_16_downstream_analysis_excludes_quarantined_units(self):
        """When reconciled CSV is passed to analyze_v3_results.py, quarantined units are excluded."""
        res = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR)
        out_csv = self.temp_dir / "v3_reconciled_test.csv"
        out_json = self.temp_dir / "v3_reconciled_test.json"
        out_md = self.temp_dir / "v3_reconciled_test.md"
        write_reconciled_outputs(res, out_csv, out_json, out_md)

        records, val_summary = validate_and_load_summary(out_csv, expected_total_runs=72)
        # Attempted rows ingested = 41
        self.assertEqual(val_summary["total_rows_ingested"], 41)
        # Completed runs should be exactly 39 (38 single completions + 1 recovered Run 26)
        # Runs 34 and 38 are quarantined, so status != 'completed'
        self.assertEqual(val_summary["completed_runs"], 39)
        
        # Analyze dataset
        analysis = analyze_dataset(records, val_summary)
        # Denominators in task breakdowns should total 39 across T1-T5 + T6
        t1_t5_total = sum(item["n_runs"] 
                          for item in analysis["task_by_arm_summary"] 
                          if item["arm"] in ("ABS", "ARIA", "DATA-CFG"))
        t6_total = sum(analysis["exploratory_t6_probe"]["summary_by_arm"][arm]["n_runs"] 
                       for arm in ["ABS", "ARIA", "DATA-CFG"])
        self.assertEqual(t1_t5_total + t6_total, 39)

    # -------------------------------------------------------------------------
    # TEST 17: Arm counts and denominators agree with reconciled eligible-unit table
    # -------------------------------------------------------------------------
    def test_17_arm_denominators_agree_with_eligible_table(self):
        """Eligible units per arm must be exactly 13 for ABS, 13 for ARIA, 13 for DATA-CFG."""
        res = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR)
        arm_counts = res["audit_summary"]["eligible_breakdown_by_arm"]
        self.assertEqual(arm_counts["ABS"]["eligible_units"], 13)
        self.assertEqual(arm_counts["ARIA"]["eligible_units"], 13)
        self.assertEqual(arm_counts["DATA-CFG"]["eligible_units"], 13)

    # -------------------------------------------------------------------------
    # TEST 18: CSV output contains no unintended duplicate scheduled-unit rows
    # -------------------------------------------------------------------------
    def test_18_csv_output_contains_no_duplicate_scheduled_units(self):
        """The reconciled CSV has strictly unique run_index values matching the schedule."""
        res = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR)
        out_csv = self.temp_dir / "v3_reconciled_unique.csv"
        out_json = self.temp_dir / "v3_reconciled_unique.json"
        out_md = self.temp_dir / "v3_reconciled_unique.md"
        write_reconciled_outputs(res, out_csv, out_json, out_md)

        with open(out_csv, "r", encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))
        csv_indices = [int(r["run_index"]) for r in csv_rows]
        self.assertEqual(len(csv_indices), len(set(csv_indices)))
        self.assertEqual(len(csv_indices), 41)

        sched_indices = [u["run_index"] for u in res["reconciled_units"]]
        self.assertEqual(len(sched_indices), len(set(sched_indices)))
        self.assertEqual(len(sched_indices), 72)

    # -------------------------------------------------------------------------
    # TEST 19: Every included unit has traceable source-file provenance
    # -------------------------------------------------------------------------
    def test_19_traceable_source_file_provenance(self):
        """Every executed unit points to an existing on-disk source JSON file."""
        res = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR)
        for u in res["reconciled_units"]:
            if u["reconciliation_category"] != "UNEXECUTED":
                src_file = u["selected_source_file"]
                self.assertTrue((REAL_RUNS_DIR / src_file).exists(), f"Source file {src_file} does not exist")

    # -------------------------------------------------------------------------
    # TEST 20: Re-running reconciliation on unchanged inputs yields identical output hashes
    # -------------------------------------------------------------------------
    def test_20_reconciliation_is_strictly_deterministic(self):
        """Two independent runs on identical inputs produce identical output SHA-256 hashes."""
        fixed_ts = "2026-10-26T12:00:00.000000"
        res1 = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR, fixed_timestamp=fixed_ts)
        csv1 = self.temp_dir / "run1.csv"
        json1 = self.temp_dir / "run1.json"
        md1 = self.temp_dir / "run1.md"
        write_reconciled_outputs(res1, csv1, json1, md1)

        res2 = reconcile_experiment_data(REAL_SCHEDULE_PATH, REAL_RUNS_DIR, fixed_timestamp=fixed_ts)
        csv2 = self.temp_dir / "run2.csv"
        json2 = self.temp_dir / "run2.json"
        md2 = self.temp_dir / "run2.md"
        write_reconciled_outputs(res2, csv2, json2, md2)

        self.assertEqual(sha256_file(csv1), sha256_file(csv2))
        self.assertEqual(sha256_file(json1), sha256_file(json2))
        self.assertEqual(sha256_file(md1), sha256_file(md2))


if __name__ == "__main__":
    unittest.main()

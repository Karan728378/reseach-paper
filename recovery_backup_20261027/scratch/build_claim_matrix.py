"""
Generate MANUSCRIPT_CLAIM_TO_EVIDENCE_MATRIX.csv mapping all major manuscript claims
to evidence classes, files, verification commands, and allowed wording.
"""
import csv
from pathlib import Path

WORKSPACE = Path(r"C:\testing\research_execution_20261018")

claims = [
    {
        "claim_id": "CLM-01",
        "section": "Sec. IV-B",
        "claim_text": "Schema.org JSON-LD is deterministically excluded from the observation tree by DISABLED_ELEMENTS.",
        "evidence_class": "DIRECTLY_VERIFIED_IMPLEMENTATION",
        "evidence_path": "browser_use/dom/serializer/serializer.py:18,481",
        "reproduction_command": "python -m unittest test_observation_pipeline_stages.py",
        "verified": "TRUE",
        "allowed_wording": "Excluded from browser-use 0.13.10 serialized observation under DISABLED_ELEMENTS rule.",
        "limitation": "Applies to text-only observation in browser-use 0.13.10; multimodal agents can observe rendered pages."
    },
    {
        "claim_id": "CLM-02",
        "section": "Sec. IV-C",
        "claim_text": "Non-interactive elements have element tags stripped, discarding parent aria-label attributes at Stage 4.",
        "evidence_class": "DIRECTLY_VERIFIED_IMPLEMENTATION",
        "evidence_path": "browser_use/dom/serializer/serializer.py:1046; scratch/inspect_serializer_boundary.py",
        "reproduction_command": "python scratch/inspect_serializer_boundary.py",
        "verified": "TRUE",
        "allowed_wording": "Non-interactive container aria-label stripped at Stage 4 serializer output under line 1046 condition.",
        "limitation": "Full Stage 5 prompt context buffer was not intercepted during behavioral pilot."
    },
    {
        "claim_id": "CLM-03",
        "section": "Sec. IV-D",
        "claim_text": "Developer custom data-* attributes are omitted under default whitelist, but delivered on interactive elements when extended.",
        "evidence_class": "DIRECTLY_VERIFIED_IMPLEMENTATION",
        "evidence_path": "browser_use/dom/views.py:18; audit_metadata_reachability.py",
        "reproduction_command": "python -m unittest test_observation_pipeline_stages.py",
        "verified": "TRUE",
        "allowed_wording": "Custom data-* omitted by default; deliverable on interactive buttons under extended whitelist.",
        "limitation": "Still stripped on non-interactive containers due to line 1046 tag stripping."
    },
    {
        "claim_id": "CLM-04",
        "section": "Sec. V-B",
        "claim_text": "Operational correspondence between browser-use selector map and Blink AXTree on #home is 27/34 (79.4%).",
        "evidence_class": "DIRECTLY_VERIFIED_DATA",
        "evidence_path": "results/accessibility_tree_comparison.json; audit_route_controls_and_correspondence.py",
        "reproduction_command": "python audit_route_controls_and_correspondence.py",
        "verified": "TRUE",
        "allowed_wording": "27 of 34 emitted selectors (79.4%) match native Blink AXNodes on the #home route.",
        "limitation": "Descriptive census on a single SPA fixture; Wilson CI applies under superpopulation assumption."
    },
    {
        "claim_id": "CLM-05",
        "section": "Sec. V-B",
        "claim_text": "The 7 unmatched selectors are 'In Stock' badge spans flagged by icon heuristic (10 <= w,h <= 50px).",
        "evidence_class": "DIRECTLY_VERIFIED_IMPLEMENTATION",
        "evidence_path": "clickable_elements.py:228-240; test_accessibility_tree_comparison.py",
        "reproduction_command": "python -m unittest test_accessibility_tree_comparison.py",
        "verified": "TRUE",
        "allowed_wording": "Seven badge spans (48.625 x 15px) fall inside the 10-50px icon bounding box heuristic.",
        "limitation": "Specific to CSS styling of the TechMart product cards."
    },
    {
        "claim_id": "CLM-06",
        "section": "Sec. V-B",
        "claim_text": "Semantic recall on genuine leaf interactive controls on #home is 26/26 (100.0%).",
        "evidence_class": "DIRECTLY_VERIFIED_DATA",
        "evidence_path": "audit_route_controls_and_correspondence.py",
        "reproduction_command": "python audit_route_controls_and_correspondence.py",
        "verified": "TRUE",
        "allowed_wording": "100.0% of genuine leaf interactive controls (11 links, 14 buttons, 1 input) match Blink AXNodes.",
        "limitation": "Explicitly scoped to the TechMart benchmark fixture; does not generalize to arbitrary websites."
    },
    {
        "claim_id": "CLM-07",
        "section": "Sec. V-C",
        "claim_text": "Across all 4 routes (#home, #cart, #checkout, #search), genuine leaf controls achieve 100% recall.",
        "evidence_class": "DIRECTLY_VERIFIED_DATA",
        "evidence_path": "audit_route_controls_and_correspondence.py",
        "reproduction_command": "python audit_route_controls_and_correspondence.py",
        "verified": "TRUE",
        "allowed_wording": "Genuine leaf controls achieve 100% correspondence across all 4 audited routes (26/26, 7/7, 12/12, 10/10).",
        "limitation": "Benchmark fixture contains clean HTML without dynamic canvas or shadow DOM barriers."
    },
    {
        "claim_id": "CLM-08",
        "section": "Sec. VI-B",
        "claim_text": "Action-Label Co-Location Confound: entity-specific ARIA labels replace spatial reasoning with string matching.",
        "evidence_class": "PLAUSIBLE_INTERPRETATION",
        "evidence_path": "variants/v0-baseline vs variants/v2-aria HTML diff; verify_variant_diffs.py",
        "reproduction_command": "python verify_variant_diffs.py",
        "verified": "TRUE",
        "allowed_wording": "Augmenting button labels with entity titles replaces spatial reference resolution with string matching.",
        "limitation": "Demonstrated conceptually and structurally; behavioral impact requires Disambiguation Probe experiments."
    },
    {
        "claim_id": "CLM-09",
        "section": "Sec. VI-C",
        "claim_text": "41 completed exploratory pilot runs achieved 100.0% success (acute ceiling effect, zero variance across arms).",
        "evidence_class": "EXPLORATORY_OBSERVATION",
        "evidence_path": "CANONICAL_RUN_LEDGER.csv; results/v3_3arm_summary_reconciled_v2.csv",
        "reproduction_command": "python scripts/independent_ledger_audit.py",
        "verified": "TRUE",
        "allowed_wording": "All completed pilot trials achieved task success (100.0%, 39/39 primary eligible, 41/41 sensitivity).",
        "limitation": "Zero variance demonstrates harness stability, but provides no evidence of treatment efficacy or equivalence."
    },
    {
        "claim_id": "CLM-10",
        "section": "Sec. VII-B",
        "claim_text": "Sample size n = 20 per arm provides only 11.5% statistical power to detect Delta = 0.20 (CMH test, alpha = 0.0167).",
        "evidence_class": "REPRODUCED_STATISTICAL_RESULT",
        "evidence_path": "power_audit_results.json; reproduce_power_audit.py",
        "reproduction_command": "python reproduce_power_audit.py",
        "verified": "TRUE",
        "allowed_wording": "Power to detect Delta = 0.20 at n = 20/arm is 11.5% (MCSE 0.32% across 10,000 RCBD iterations).",
        "limitation": "Based on 5-strata RCBD simulation with assumed baseline success rates [0.70, 0.85, 0.50, 0.30, 0.80]."
    },
    {
        "claim_id": "CLM-11",
        "section": "Sec. VII-C",
        "claim_text": "An adequately powered 3-arm confirmatory study (80% power, alpha = 0.0167, Delta = 0.20) requires n = 97 to 125 per arm.",
        "evidence_class": "REPRODUCED_STATISTICAL_RESULT",
        "evidence_path": "power_audit_results.json; reproduce_power_audit.py",
        "reproduction_command": "python reproduce_power_audit.py",
        "verified": "TRUE",
        "allowed_wording": "Detecting Delta = 0.20 with 80% power requires approximately 97 to 125 trials per arm (N = 388 to 500 total).",
        "limitation": "Standard binomial sample size formula with continuity correction."
    },
    {
        "claim_id": "CLM-12",
        "section": "Sec. VII-D",
        "claim_text": "Disambiguation Probes A & B are offline-verified experimental designs, not executed results.",
        "evidence_class": "FUTURE_WORK",
        "evidence_path": "fixtures/disambiguation_probe_a.html; DISAMBIGUATION_PROBES_PROTOCOL.md",
        "reproduction_command": "python -m unittest test_disambiguation_probes.py",
        "verified": "TRUE",
        "allowed_wording": "Probes A and B are planned future experimental protocols awaiting authorization and budget.",
        "limitation": "Zero live behavioral trials have been executed on these probe fixtures."
    }
]

out_csv = WORKSPACE / "MANUSCRIPT_CLAIM_TO_EVIDENCE_MATRIX.csv"
fieldnames = [
    "claim_id", "section", "claim_text", "evidence_class", "evidence_path",
    "reproduction_command", "verified", "allowed_wording", "limitation"
]

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(claims)

print(f"Generated {out_csv} with {len(claims)} verified claims.")

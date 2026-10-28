import csv
from pathlib import Path

ROOT = Path(r"C:\testing\research_execution_20261018")
out_csv = ROOT / "FINAL_VALIDATION_05_PROVENANCE_AND_CLAIM_MAP.csv"

claims = [
    {
        "claim_id": "CLM-01",
        "manuscript_section": "Abstract, Sec. III-A, Table 1",
        "claim_statement": "In browser-use 0.13.10, Schema.org JSON-LD is deterministically excluded from the Stage 4 serialized observation by DISABLED_ELEMENTS.",
        "evidence_category": "DIRECT_IMPLEMENTATION_EVIDENCE",
        "source_artifact": "browser_use/dom/serializer/serializer.py:18, 481",
        "reproduction_command": "python -m unittest test_observation_pipeline_stages.py",
        "observed_output": "DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}; JSON-LD excluded at Stage 4",
        "allowed_wording": "In browser-use 0.13.10, DISABLED_ELEMENTS excludes script and meta tags, pruning JSON-LD prior to agent observation.",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-02",
        "manuscript_section": "Abstract, Sec. III-B, Table 1",
        "claim_statement": "Non-interactive container elements have their tags and all attributes (including aria-label) stripped at Stage 4.",
        "evidence_category": "DIRECT_RUNTIME_TRACE_EVIDENCE",
        "source_artifact": "browser_use/dom/serializer/serializer.py:1046-1051, fixtures/disambiguation_probe_b.html",
        "reproduction_command": "python -m unittest test_disambiguation_probes.py",
        "observed_output": "Tag serialization gated on is_interactive or is_any_scrollable; span aria-label dropped in dom_state.llm_representation()",
        "allowed_wording": "Tag serialization is gated on interactivity (lines 1046-1051); non-interactive container aria-label attributes are discarded at Stage 4.",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-03",
        "manuscript_section": "Sec. III-C, Table 1",
        "claim_statement": "Custom data-* attributes are omitted under default whitelist, but survive on interactive elements when EXTENDED_ATTRIBUTES is passed.",
        "evidence_category": "DIRECT_IMPLEMENTATION_EVIDENCE",
        "source_artifact": "browser_use/dom/views.py:DEFAULT_INCLUDE_ATTRIBUTES and serializer.py:1211",
        "reproduction_command": "python -m unittest test_observation_pipeline_stages.py",
        "observed_output": "DEFAULT_INCLUDE_ATTRIBUTES omits data-*; EXTENDED_ATTRIBUTES rescues data-* on buttons/links only",
        "allowed_wording": "Default whitelist drops custom data-* attributes; extended whitelist rescues them on interactive controls only.",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-04",
        "manuscript_section": "Abstract, Sec. IV-B, Table 2",
        "claim_statement": "On route #home, 27 of 34 selector targets (79.4%) match Blink AXTree nodes, while 26/26 genuine leaf controls achieve 100% recall.",
        "evidence_category": "DIRECT_RUNTIME_TRACE_EVIDENCE",
        "source_artifact": "techmart-benchmark/variants/v0-baseline/index.html, Chromium AXTree dump",
        "reproduction_command": "python scripts/audit_route_controls_and_correspondence.py",
        "observed_output": "11 links, 14 buttons, 1 input = 26 leaf controls (100%); 1 form = 27; 7 badge spans (48.6x15px) = 34 targets (79.4%)",
        "allowed_wording": "Within the benchmark fixture home route, 27 of 34 selector targets (79.4%) match Blink AXTree nodes; all 26 leaf controls achieve 100% correspondence.",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-05",
        "manuscript_section": "Abstract, Sec. IV-A",
        "claim_statement": "In the exploratory pilot, all 41 completed runs (39 primary eligible) succeeded (100%), exhibiting a ceiling effect with zero variance.",
        "evidence_category": "EMPIRICAL_EXPLORATORY_EVIDENCE",
        "source_artifact": "CANONICAL_RUN_LEDGER.csv, results/v3_3arm_summary_reconciled_v2.csv",
        "reproduction_command": "python scripts/independent_ledger_audit.py",
        "observed_output": "ABS: 13/13 (100%), ARIA: 13/13 (100%), DATA-CFG: 13/13 primary (100%)",
        "allowed_wording": "In the exploratory cloud pilot, all arms achieved 100% success, precluding behavioral discrimination due to a ceiling effect.",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-06",
        "manuscript_section": "Abstract, Sec. IV-A",
        "claim_statement": "Observed risk difference Delta = 0.000 with 95% Newcombe hybrid score CI [-0.232, +0.232]; high p-value does not prove equivalence.",
        "evidence_category": "STATISTICAL_DERIVATION",
        "source_artifact": "CANONICAL_RUN_LEDGER.csv, REMEDIATION_05_STATISTICAL_REANALYSIS.md",
        "reproduction_command": "python scratch/build_remediation_05.py",
        "observed_output": "Delta = 0.000, 95% Newcombe CI [-0.232, +0.232] (corrected) / [-0.228, +0.228] (uncorrected), Fisher p = 1.0000",
        "allowed_wording": "Risk difference Delta = 0.000 (95% Newcombe CI [-0.232, +0.232]); the pilot does not establish equivalence or superiority.",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-07",
        "manuscript_section": "Abstract, Sec. III-D, Table 3",
        "claim_statement": "Pilot sample size (n <= 20/arm) provides only ~11% power for Delta = 0.20 (10.8% at B=2000, 11.5% at B=10000) and 49.6% for Delta = 0.35.",
        "evidence_category": "SYNTHETIC_OR_SIMULATED_EVIDENCE",
        "source_artifact": "power_audit_results.json, scripts/reproduce_power_audit.py",
        "reproduction_command": "python scripts/reproduce_power_audit.py",
        "observed_output": "Power for Delta=0.20: 10.85% (B=2,000) / 11.45% (B=10,000); Power for Delta=0.35: 49.65%",
        "allowed_wording": "Statistical power at pilot scale is severely underpowered (~11% for Delta = 0.20; 49.6% for Delta = 0.35).",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-08",
        "manuscript_section": "Sec. III-D, Appendix C",
        "claim_statement": "Detecting Delta = 0.20 with 80% power requires 97 to 125 runs/arm; proving equivalence (+-10%) requires 275 to 360 runs/arm.",
        "evidence_category": "STATISTICAL_DERIVATION",
        "source_artifact": "REMEDIATION_05_POWER_SENSITIVITY.csv, POWER_AND_SAMPLE_SIZE_AUDIT.md",
        "reproduction_command": "python scratch/build_remediation_05.py",
        "observed_output": "n_superiority = 96.8 -> 97 to 124.3 -> 125; n_TOST = 274.1 -> 275 to 359.8 -> 360",
        "allowed_wording": "Confirmatory superiority requires 97 to 125 runs per arm (388 to 500 total); TOST equivalence requires 275 to 360 per arm (1,100 to 1,440 total).",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-09",
        "manuscript_section": "Sec. III-C, Sec. V",
        "claim_statement": "ARIA labels co-locate entity names inside buttons, introducing a confound that can be decoupled via BASELINE_REP.",
        "evidence_category": "PLAUSIBLE_INTERPRETATION",
        "source_artifact": "REMEDIATION_02_CAUSAL_IDENTIFICATION.md, test_aria_baseline_prompt_divergence.py",
        "reproduction_command": "python -m unittest test_aria_baseline_prompt_divergence.py",
        "observed_output": "v2-aria button contains full entity title; v0-baseline button contains generic Add to Cart",
        "allowed_wording": "Standard ARIA markup introduces an Action-Label Co-Location Confound; BASELINE_REP is proposed to isolate this effect.",
        "verification_status": "DIRECTLY_VERIFIED"
    },
    {
        "claim_id": "CLM-10",
        "manuscript_section": "Sec. III-C, Sec. VI",
        "claim_statement": "A 4-arm 96-trial confirmatory study is proposed and preregistration-ready; zero confirmatory runs have been executed.",
        "evidence_category": "NOT_EXECUTED",
        "source_artifact": "REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md",
        "reproduction_command": "Inspection of results/ directory confirming 0 confirmatory trial files",
        "observed_output": "Zero live confirmatory runs executed; fail-closed safety controller active",
        "allowed_wording": "Confirmatory live behavioral experiments have not been executed; the 4-arm 96-trial design is proposed and preregistration-ready.",
        "verification_status": "DIRECTLY_VERIFIED"
    }
]

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "claim_id", "manuscript_section", "claim_statement", "evidence_category",
        "source_artifact", "reproduction_command", "observed_output",
        "allowed_wording", "verification_status"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(claims)

print(f"[+] Successfully generated {out_csv} with {len(claims)} mapped claims.")

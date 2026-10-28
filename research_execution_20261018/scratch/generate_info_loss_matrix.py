import csv
from pathlib import Path

ROOT = Path(r"C:\testing\research_execution_20261018")
out_csv = ROOT / "REMEDIATION_03_INFORMATION_LOSS_MATRIX.csv"

rows = [
    {
        "MetadataChannel": "Schema.org JSON-LD",
        "SourceElement": "<script type='application/ld+json'>",
        "Stage1_HTML": "Present (Structured JSON)",
        "Stage2_BlinkDOM": "Present (Script Element)",
        "Stage3_AXTree": "Omitted (Ignored by Accessibility)",
        "Stage4_Serializer": "PRUNED (Excluded by DISABLED_ELEMENTS)",
        "Stage5_ModelPrompt": "ABSENT (Cannot reach model)",
        "PruningGate": "serializer.py:18 (DISABLED_ELEMENTS)",
        "EvidenceType": "DIRECT_IMPLEMENTATION_EVIDENCE",
        "VerificationArtifact": "test_observation_pipeline_stages.py:test_jsonld_pruned"
    },
    {
        "MetadataChannel": "Non-Interactive Container ARIA",
        "SourceElement": "<span aria-label='Identity: SKU-101'>",
        "Stage1_HTML": "Present (HTML attribute)",
        "Stage2_BlinkDOM": "Present (DOM node attribute)",
        "Stage3_AXTree": "Retained (Computed accessible name)",
        "Stage4_Serializer": "PRUNED (Tag stripped: lines 1046-1051)",
        "Stage5_ModelPrompt": "ABSENT (Inner text only; attribute lost)",
        "PruningGate": "serializer.py:1046-1051 (Interactivity Gate)",
        "EvidenceType": "DIRECT_RUNTIME_TRACE_EVIDENCE",
        "VerificationArtifact": "fixtures/disambiguation_probe_b.html runtime trace"
    },
    {
        "MetadataChannel": "Interactive Button ARIA",
        "SourceElement": "<button aria-label='Add SoundFlow to Cart'>",
        "Stage1_HTML": "Present (HTML attribute)",
        "Stage2_BlinkDOM": "Present (DOM node attribute)",
        "Stage3_AXTree": "Retained (AXNode Name)",
        "Stage4_Serializer": "RETAINED (Interactive node preserved)",
        "Stage5_ModelPrompt": "PRESENT (Delivered in action selector map)",
        "PruningGate": "Retained (Passed interactivity & whitelist)",
        "EvidenceType": "DIRECT_IMPLEMENTATION_EVIDENCE",
        "VerificationArtifact": "test_aria_baseline_prompt_divergence.py"
    },
    {
        "MetadataChannel": "Custom Developer Attribute (Default)",
        "SourceElement": "<button data-product-id='sku-101'>",
        "Stage1_HTML": "Present (HTML attribute)",
        "Stage2_BlinkDOM": "Present (DOM node attribute)",
        "Stage3_AXTree": "Omitted (AXTree ignores custom data-*)",
        "Stage4_Serializer": "PRUNED (Excluded by DEFAULT_INCLUDE_ATTRIBUTES)",
        "Stage5_ModelPrompt": "ABSENT (Filtered from attribute string)",
        "PruningGate": "views.py:DEFAULT_INCLUDE_ATTRIBUTES & serializer.py:1211",
        "EvidenceType": "DIRECT_IMPLEMENTATION_EVIDENCE",
        "VerificationArtifact": "test_observation_pipeline_stages.py:test_custom_data_attributes"
    },
    {
        "MetadataChannel": "Custom Developer Attribute (Extended)",
        "SourceElement": "<button data-product-id='sku-101'>",
        "Stage1_HTML": "Present (HTML attribute)",
        "Stage2_BlinkDOM": "Present (DOM node attribute)",
        "Stage3_AXTree": "Omitted (AXTree ignores custom data-*)",
        "Stage4_Serializer": "RETAINED on interactive controls; PRUNED on spans",
        "Stage5_ModelPrompt": "PRESENT on buttons; ABSENT on containers",
        "PruningGate": "views.py:EXTENDED_ATTRIBUTES whitelist",
        "EvidenceType": "DIRECT_IMPLEMENTATION_EVIDENCE",
        "VerificationArtifact": "test_disambiguation_probes.py:test_probe_a_extended_attributes"
    },
    {
        "MetadataChannel": "Icon-Button Semantic Label",
        "SourceElement": "<button class='icon-cart'>[SVG]</button>",
        "Stage1_HTML": "Present (SVG/Icon markup)",
        "Stage2_BlinkDOM": "Present (Bounding box: 48.6 x 15 px)",
        "Stage3_AXTree": "Retained if accessible name exists",
        "Stage4_Serializer": "HEURISTIC MISCLASSIFIED (Fails 20x20px threshold)",
        "Stage5_ModelPrompt": "DEGRADED (Emitted without semantic role/name)",
        "PruningGate": "serializer.py heuristic bounding box check",
        "EvidenceType": "DIRECT_RUNTIME_TRACE_EVIDENCE",
        "VerificationArtifact": "scripts/audit_route_controls_and_correspondence.py"
    }
]

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"[+] Written {out_csv}")

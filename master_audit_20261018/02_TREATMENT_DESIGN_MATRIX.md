# Treatment Design Matrix
**Audit Date:** 2026-10-18

## Model-Visible Token Delivery per Arm

| Arm | HTML Channel | Token in DOM Snapshot Text | Token in Vision Canvas | Requires Runner Patch | Historical Status |
|-----|-------------|---------------------------|----------------------|----------------------|-------------------|
| ABS | Absent | ❌ | ❌ | No | Operational |
| VIS (v0-baseline) | Visible `<p>` text | ✅ | ✅ (if use_vision=True) | No | Operational |
| JSON-LD (v1-jsonld) | `<script type=application/ld+json>` | ❌ (BLOCKED) | ❌ | N/A | **BLOCKED — equivalent to ABS** |
| ARIA (v2-aria) | `aria-label` attribute | ✅ | ❌ | No | Operational |
| DATA-CFG (v3-data-attrs) | `data-*` attribute | ❌ (default) / ✅ (patched) | ❌ | **Yes** | **BLOCKED in historical runs** |
| META (v4-evidence-meta) | `<meta>` tags | ❌ (BLOCKED) | ❌ | N/A | Excluded (correctly) |

## Vision Confound Assessment

If `use_vision=True` (historical default):
- **VIS arm**: Token appears in rendered page screenshot → multimodal dual-channel delivery (text + vision).
- **ARIA arm**: aria-label NOT rendered visually → single-channel (text only).
- **DATA-CFG arm**: data-* NOT rendered visually → single-channel (text only).
- **Confound**: VIS vs ARIA is not a clean channel comparison if vision is active.

**Required mitigation:** `use_vision=False` for Protocol v3.

## Required Arm Redesign

For a valid 4-arm experiment, replace v1-jsonld with an explicit ABS arm:

| Arm | Proposed Implementation |
|-----|------------------------|
| ABS | No target token anywhere on page |
| VIS | Target token in visible `<p>` text (v0-baseline pattern) |
| ARIA | Target token in `aria-label` attribute (v2-aria pattern) |
| DATA-CFG | Target token in `data-lot-code` attribute WITH `include_attributes` patch |

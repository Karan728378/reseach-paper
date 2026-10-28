# REMEDIATION 04: METRIC VALIDITY AND ACCESSIBILITY TREE CORRESPONDENCE
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Accessibility, Semantic HTML, and Measurement Integrity Team  

---

## 1. Executive Summary

This audit evaluates the validity, denominators, and interpretation of the accessibility correspondence metrics reported in the study.

A major defect in older drafts was conflating **Operational Correspondence** ($27/34 = 79.4\%$) with **Semantic Recall on Interactive Leaf Controls** ($26/26 = 100.0\%$). Furthermore, older drafts contained a typographical error reporting "9 links and 16 buttons" instead of the true count of 11 links and 14 buttons.

---

## 2. Definitive Route `#home` Element Census

The census of DOM elements on the benchmark home route (`http://127.0.0.1:8094/variants/v0-baseline/index.html#home`) was audited using `scripts/audit_route_controls_and_correspondence.py`:

| Element Category | HTML Tag / Role | Census Count | Correspondence to Blink AXTree |
|:---|:---:|:---:|:---:|
| **Navigation Links** | `<a>` | 11 | 11 / 11 (100%) |
| **Interactive Buttons** | `<button>` | 14 | 14 / 14 (100%) |
| **Text Inputs** | `<input type="text">` | 1 | 1 / 1 (100%) |
| **Total Leaf Interactive Controls** | — | **26** | **26 / 26 (100.0%)** |
| **Form Containers** | `<form>` | 1 | 1 / 1 (100%) |
| **Total Interactive Targets** | — | **27** | **27 / 27 (100.0%)** |
| **Heuristic Icon Badge Spans** | `<span>` ($48.6 \times 15\text{px}$) | 7 | 0 / 7 (0.0% — Ignored by AXTree) |
| **Total Serializer Selector Targets** | — | **34** | **27 / 34 (79.4%)** |

### Resolution of Historical Discrepancies:
- **"9 links and 16 buttons":** CONFIRMED DEFECT in an old draft. It resulted from an erroneous sub-classification of 2 anchor tags as buttons. The physical DOM contains exactly 11 `<a>` tags and 14 `<button>` tags.
- **The Denominator 34:** Represents the total set of elements emitted into `dom_state.selector_map` by `browser-use 0.13.10` on the `#home` route.
- **The Denominator 26:** Represents the ground-truth set of clickable, interactive leaf controls on `#home`.

---

## 3. Directionality of Correspondence

The metric measures a **one-way operational mapping**:
$$\text{Operational Correspondence} = \frac{|\text{Serializer Targets} \cap \text{Blink AXNodes}|}{|\text{Serializer Targets}|} = \frac{27}{34} = 79.4\%$$

- **What it measures:** The fraction of serializer-selected action targets that have a corresponding semantic representation in Chromium's native Accessibility Tree.
- **What it does NOT measure:** It does NOT measure bidirectional accessibility completeness, WCAG compliance, screen reader usability, or model reasoning accuracy.
- **Why it is not 100%:** The 7-element gap is entirely driven by `browser-use`'s heuristic icon classifier tagging $48.6 \times 15\text{px}$ badge spans as clickable icons.

---

## 4. Single-Fixture Census vs. Statistical Generalization

1. **Finite Census:** The 34 selector targets constitute the complete finite population of elements on the single TechMart `#home` fixture. Computing confidence intervals (e.g., Wilson intervals) on this deterministic census is conceptually inappropriate, as there is no random sampling variation.
2. **Web Generalization Boundary:** The $100\%$ leaf-control recall ($26/26$) reflects clean, standard HTML5 structure without complex Shadow DOM, canvas controls, or obfuscated click listeners. On heterogeneous commercial websites, semantic recall will vary significantly. The paper explicitly restricts this claim to the tested fixture.

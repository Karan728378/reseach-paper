# SIX-FLAW REPAIR LOG: SCIENTIFIC AUDIT & RESOLUTION RECORD

**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Workspace:** `C:\testing\research_execution_20261018`  
**Date:** October 26, 2026  
**Auditor / Lead Engineer:** Autonomous Senior Research Engineer & Scientific Methodology Auditor  
**Target Manuscript:** `research_paper_final.tex` (IEEEtran Conference Format)

---

## Executive Summary

Following external peer-review critique, an in-depth audit identified six scientific and reporting weaknesses in earlier versions of the manuscript and project documentation. Each weakness was treated as an empirical hypothesis to verify against actual code, raw datasets, runtime traces, and statistical simulations. 

All six flaws have been comprehensively investigated, resolved with defensible evidence, and reflected in the updated IEEE conference manuscript (`research_paper_final.tex`) and associated test suites. Zero data was falsified, zero live API calls were consumed during remediation, and historical records were strictly preserved.

---

## Detailed Flaw-by-Flaw Resolution

### Flaw 1: Pipeline Reachability Boundaries and Observation Staging
- **Identified Weakness:** Earlier drafts claimed that non-interactive ARIA attributes were dropped "between HTML and the final LLM prompt (Stage 5)" without verifying the exact pipeline stage where the loss occurred or distinguishing Stage 4 (serializer output) from Stage 5 (full model context buffer).
- **Investigation & Forensic Evidence:**
  1. *Source Code Inspection:* In `browser_use/dom/serializer/serializer.py` (lines 1046--1051), tag emission is conditionally gated:
     ```python
     if (node.is_interactive
             or is_any_scrollable
             or tag == 'IFRAME'
             or tag == 'FRAME'):
         attributes_html_str = DOMTreeSerializer._build_attributes_string(...)
     ```
     For non-interactive container elements (`<span>`, `<div>`), `_build_attributes_string` is never invoked, the opening/closing tags are omitted, and all attributes (including `aria-label`) are stripped.
  2. *Live Runtime Trace:* Executed `scratch/inspect_serializer_boundary.py` navigating a headless Chromium instance to `fixtures/disambiguation_probe_b.html`. The target container `span` (`aria-label="Identity: target-sku-101"`) was examined at Stage 4 (`dom_state.llm_representation()`). The `aria-label` was confirmed absent under both `DEFAULT_INCLUDE_ATTRIBUTES` and an extended whitelist (`EXTENDED_ATTRIBUTES` with `data-product-id`).
  3. *Stage 5 Boundary Limitation:* Because the full prompt buffer assembling system prompt, task history, and URL context was not intercepted during the behavioral pilot, the claim must be bounded to Stage 4.
- **Repair in Manuscript:**
  - Section IV-C and Table I explicitly state that container `aria-label` is discarded at Stage 4 via line 1046 tag stripping.
  - The text explicitly notes that Stage 5 prompt assembly was not fully inspected, scoping reachability claims strictly to Stage 4 serializer output.

---

### Flaw 2: Overgeneralizing Control Correspondence Across Application Views
- **Identified Weakness:** Reporting 100% semantic recall of interactive controls ($26/26$ on `#home`, $7/7$ on `#cart`, $12/12$ on `#checkout`, $10/10$ on `#search`) risked sounding like an unconditional claim that browser-use perfectly captures all web controls universally.
- **Investigation & Forensic Evidence:**
  1. *Root Cause of 100% Recall:* The TechMart e-commerce benchmark is a clean, accessible single-page application. It uses standard semantic HTML tags (`<button>`, `<a>`, `<input>`) with no CSS occlusion, canvas rendering, complex shadow DOM encapsulation, or non-standard pointer-event handlers.
  2. *Real-World Non-Generalizability:* Real-world web applications frequently employ non-semantic `<div>` clickables without ARIA roles, nested scroll containers, canvas widgets, and dynamic iframe barriers where heuristic detection failure rates are well documented in literature (e.g., Mind2Web, WebArena).
- **Repair in Manuscript:**
  - Abstract, Section I, Section III, Section V-B, and Section IX (Limitations) explicitly clarify that the 100% semantic recall is an empirical property of the audited TechMart benchmark fixture and does not generalize to arbitrary web applications or other agent frameworks.
  - Clear demarcations emphasize that operational correspondence is $79.4\%$ ($27/34$) on `#home` due to heuristic badge false positives, demonstrating that the observation pipeline does introduce distortions.

---

### Flaw 3: Conflating Offline Software Tests with Scientific Validation
- **Identified Weakness:** Phrases in earlier reports conflated passing automated test suites with "scientific validation of agent behavior" or "proving empirical hypotheses."
- **Investigation & Forensic Evidence:**
  1. *Nature of Test Suite:* The project contains 191 automated tests across 23 test modules (e.g., `test_data_reconciliation_and_provenance.py`, `test_observation_pipeline_stages.py`, `test_budget_controls.py`, `test_disambiguation_probes.py`).
  2. *Defensible Role of Tests:* These tests validate software engineering correctness: verifying that JSON schema parsers handle edge cases, that budget controllers fail closed, that data reconciliation matches raw attempt files, that serializer pruning ASTs match specified code paths, and that SHA-256 hashes remain pristine.
  3. *Scientific Status:* Passing tests do not constitute scientific validation of agent task performance or treatment effects. Confirmatory behavioral trials were halted at 39 eligible runs by the budget ceiling; empirical behavioral outcomes showed a 100% ceiling effect (zero variance).
- **Repair in Manuscript:**
  - Section III-D and Appendix A clearly classify the test battery as software verification and reproducibility scaffolding.
  - Section VI explicitly discloses that the 41-trial pilot demonstrated operational stability but provided zero evidence of treatment efficacy or behavioral equivalence.

---

### Flaw 4: Multi-Framework Observation Audit Scope
- **Identified Weakness:** A previous summary claimed a "multi-framework observation audit" covering browser-use, BrowserGym, Crawl4AI, Stagehand, and Skyvern without sufficient experimental backing across all five frameworks.
- **Investigation & Forensic Evidence:**
  1. *Audit Implementation:* Inspection of `audit_multi_framework_observation.py` and `MULTI_FRAMEWORK_OBSERVATION_TAXONOMY.md` reveals that this analysis was conducted via static source-code analysis of public repositories and offline execution against a standardized fixture (`fixtures/multi_framework_observation_fixture.html`).
  2. *Appropriate Framing:* This constitutes a comparative architectural taxonomy of DOM serialization heuristics, not an end-to-end multi-framework agent evaluation.
- **Repair in Manuscript:**
  - Section I and Section IX explicitly bound the paper's empirical systems audit to `browser-use 0.13.10` under text-only observation as a focused case study.
  - Multi-framework comparisons are referenced in Related Work (Section II) and Discussion (Section VIII) as architectural context, with explicit notes that cross-framework empirical benchmarking is future work.

---

### Flaw 5: Ambiguous Control Counts on `#home` Route
- **Identified Weakness:** Prior manuscript revisions alternated between 26, 27, and 34 elements on the primary `#home` catalog route without reconciling leaf interactive controls vs. structural containers vs. heuristic selector entries.
- **Investigation & Forensic Evidence:**
  1. *Automated Node Audit:* Running `audit_route_controls_and_correspondence.py` extracted the exact DOM and AXTree nodes:
     - Total emitted selector map entries: $n = 34$.
     - Blink AXTree matching selector entries: $n = 27$ (Operational correspondence $= 27/34 = 79.4\%$).
  2. *Taxonomic Breakdown of 27 Matched Elements:*
     - **Leaf Interactive Controls ($n = 26$):** 11 anchor links (logo, cart link, hero CTA, 8 product card links), 14 buttons (search submit, 5 category filter buttons, 8 product buttons [7 active "Add to Cart", 1 disabled "Out of Stock"]), and 1 text input (search input). All 26 match Blink AXTree nodes ($26/26 = 100.0\%$).
     - **Structural Form Container ($n = 1$):** `<form id="search-form">` possesses native Blink AX role `form`. It is an actionable container, but not a leaf control. Container-inclusive count is $26 + 1 = 27$ ($27/27 = 100.0\%$).
  3. *Forensic Breakdown of 7 Unmatched Elements ($34 - 27 = 7$):*
     - Exactly 7 inline `<span>` elements displaying "In Stock" on the first 7 product cards (indices 69, 84, 99, 114, 129, 144, 159).
     - Rendered size: $48.625\text{px} \times 15.0\text{px}$.
     - `ClickableElementDetector` heuristic flags any element with a `class` attribute and $10 \le w, h \le 50\text{px}$ as an interactive icon.
     - Blink AXTree treats static text spans as non-interactive text with `ignored: true` and no discrete `backendDOMNodeId`.
- **Repair in Manuscript:**
  - Section V-B and Table II explicitly present both denominators: Operational Correspondence ($27/34 = 79.4\%$) and Semantic Recall on Leaf Interactive Controls ($26/26 = 100.0\%$).
  - The structural container (`<form id="search-form">`) is explicitly described as a container, never conflated with leaf controls.
  - Table II caption and text document the exact bounding-box dimensions and root cause of the 7 false positives.

---

### Flaw 6: Statistical Power, Multiplicity Adjustments, and Disambiguation Probes
- **Identified Weakness:** Multiplicity corrections were previously conflated: the 3-arm behavioral study's Bonferroni threshold ($\alpha = 0.05 / 3 \approx 0.0167$) was mixed with the 2-probe disambiguation study ($\alpha = 0.05 / 2 = 0.025$). Furthermore, the power of the pilot was vaguely stated, and failure to reject was improperly termed "false-negative rate".
- **Investigation & Forensic Evidence:**
  1. *Monte Carlo Simulation Verification:* Executed `reproduce_power_audit.py` (10,000 RCBD iterations, seed 42):
     - $\Delta = 0.70$: Power $= 98.8\%$ (MCSE $0.1\%$).
     - $\Delta = 0.35$: Power $= 48.5\%$ (MCSE $0.5\%$).
     - $\Delta = 0.20$: Power $= \mathbf{11.5\%}$ (MCSE $0.3\%$).
     - $\Delta = 0.15$: Power $= 5.6\%$ (MCSE $0.2\%$).
  2. *Multiplicity Structure Clarification:*
     - **Family 1 (3-Arm Confirmatory Study):** Three pairwise contrasts (ARIA vs. Baseline, DATA-CFG vs. Baseline, ARIA vs. DATA-CFG). Bonferroni $\alpha_{\mathrm{adj}} = 0.05 / 3 = 0.01667$.
     - **Family 2 (Disambiguation Probes A & B):** Two independent probe tasks evaluating distinct information channels. Bonferroni $\alpha_{\mathrm{adj}} = 0.05 / 2 = 0.025$.
     - These two families are distinct and non-overlapping.
  3. *Terminology Correction:* Replaced "false-negative rate" with "probability of failing to reject the null at $\alpha_{\mathrm{adj}} = 0.0167$" ($1 - 0.115 = 88.5\%$ for $\Delta = 0.20$), because false-negative rate formally requires conditioning on a verified true non-null effect size.
- **Repair in Manuscript:**
  - Section VII-A and VII-B explicitly separate the two hypothesis families and their respective Bonferroni thresholds.
  - Table III reports authoritative 10,000-iteration RCBD power results alongside MCSE.
  - Section VII-C and VII-D specify that Probes A and B are planned follow-up experimental designs, not executed results.

---

## Verification Matrix

| Flaw # | Description | Primary Code / Artifact | Test / Verification Command | Status |
| :---: | :--- | :--- | :--- | :---: |
| **1** | Stage 4 vs Stage 5 reachability boundary | `scratch/inspect_serializer_boundary.py` | `python scratch/inspect_serializer_boundary.py` | **RESOLVED** |
| **2** | Generalizing 100% control correspondence | `research_paper_final.tex` \S V-B | Manual audit & `check_latex.py` | **RESOLVED** |
| **3** | Offline tests vs scientific validation | `test_data_reconciliation_and_provenance.py` | `python -m unittest discover -s . -p "test_*.py"` | **RESOLVED** |
| **4** | Multi-framework audit scope | `MULTI_FRAMEWORK_OBSERVATION_TAXONOMY.md` | `audit_multi_framework_observation.py` | **RESOLVED** |
| **5** | Ambiguous `#home` control counts | `audit_route_controls_and_correspondence.py` | `python audit_route_controls_and_correspondence.py` | **RESOLVED** |
| **6** | Statistical power & multiplicity | `reproduce_power_audit.py` | `python reproduce_power_audit.py` | **RESOLVED** |

---

## Conclusion

Every confirmed defect has been repaired with concrete evidence, verifiable scripts, and disciplined scientific prose. No further edits are required for these six items.

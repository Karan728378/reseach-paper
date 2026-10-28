# CONTRIBUTION DECISION MEMO
**Date (UTC):** 2026-10-27T01:20:00Z  
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Authoritative Evidence Base:** Phases 1–7 Audits, Determinstic Stage Traces (`STAGE_TRACE_RAW/`), Information Retention Matrix (`REMEDIATION_03_INFORMATION_LOSS_MATRIX.csv`), Reconciled Experiment Ledger (`EVIDENCE_CLASS_LEDGER.csv`).

---

## 1. Selected Defensible Contribution Model

We evaluate the three candidate publication strategies identified in the protocol:

| Strategy | Feasibility Today | Scientific Defensibility | Decision |
|---|---|---|---|
| **Model A: Version-Pinned Serializer Systems Audit** | 100% Feasible (E1, E2, E3 verified) | **High / Defensible:** Exhaustively backed by source code SHA-256 hashes, CDP traces, and measured 21-channel retention matrix. | **ACCEPTED (Primary Contribution)** |
| **Model B: Methodological Validity Framework** | 100% Feasible (E2, E3, E5 verified) | **High / Defensible:** Provides the first rigorous channel-delivery preflight protocol and power/equivalence design rules for browser-agent benchmarks. | **ACCEPTED (Core Secondary Contribution)** |
| **Model C: Empirical Agent Behavioral Study** | Conditional on Phase 11 Authorization | **Not Defensible Today:** Existing pilot data ($N=39$) is an uninformative ceiling observation (power < 12%). Confirmatory live runs require paid Groq execution subject to user authorization. | **DEFERRED TO PHASE 11 GATE** (Manuscript will report pilot honestly as a harness stability check with wide CIs). |

### Formal Decision
The manuscript is restructured as a **rigorous systems audit and methodological framework** (Models A + B). The study demonstrates that client-side observation pipelines introduce severe, systematic information loss that invalidates naive markup-ablation experiments. The pilot ($N=39$) is presented strictly as an exploratory harness-stability observation under a ceiling effect, not as an empirical test of agent intelligence or markup sufficiency.

---

## 2. Research Question Scope Calibration

| Original Research Question | Flaw / Vulnerability in Prior Drafts | Calibrated Research Question |
|---|---|---|
| **RQ1 (Information Loss):** "How much markup information is lost in LLM browser agents?" | Overgeneralized from a single framework to "any agent"; asserted retention without measuring Stage 5 boundary. | **Calibrated RQ1:** Across each discrete observation stage in `browser-use==0.13.10`, which semantic metadata channels (JSON-LD, ARIA, developer `data-*`, microdata) survive to the model-input boundary, and by what specific architectural mechanisms are dropped channels eliminated? |
| **RQ2 (Correspondence & Interactivity):** "Does the selector map correspond to the Blink Accessibility Tree?" | Circularity confound: ClickableElementDetector queries `ax_node.role` directly. | **Calibrated RQ2:** To what extent is selector-map interactivity derived from native HTML semantics versus Blink Accessibility Tree heuristics, and where do heuristic bounding-box rules (e.g. 10–50px icon boundaries) misclassify non-interactive elements? |
| **RQ3 (Statistical Power & Pilot):** "Does additive semantic markup improve task success in autonomous browser agents?" | Confirmatory claim attempted from an exploratory 13/13 pilot with ceiling effect; power < 12% conflated with execution. | **Calibrated RQ3 (Methodological Note):** What statistical power and sample sizes are required to detect realistic performance differences ($\Delta \in [0.15, 0.35]$) in stratified browser-agent benchmarks, and what bounds does the exploratory 39-trial stability pilot place on task performance? |

---

## 3. Mandatory Claim Calibrations and Scope Limitations

1. **Retract "Sufficiency" Claims:** The claim that "visible typography alone was fully sufficient" is retracted. A 13/13 success rate has a two-sided 95% Clopper-Pearson confidence interval of $[75.3\%, 100.0\%]$, leaving an undetected failure rate of up to $24.7\%$ and an uncorrected pairwise risk difference interval of $[-0.2281, +0.2281]$.
2. **Clarify JSON-LD Exclusion Mechanism:** JSON-LD in `<script type="application/ld+json">` is dropped at Stage 2 by `DISABLED_ELEMENTS` (element pruning), not at Stage 4 by the attribute whitelist.
3. **Disclose AXTree Circularity:** ClickableElementDetector queries `node.ax_node.role`. Correspondence between the selector map and Blink AXTree is partially circular by construction.
4. **Disclose Probe B Region Semantics:** Disambiguation Probe B utilizes `role="region"` container spans, which are landmark elements whose names are valid under W3C WAI-ARIA 1.2, but are eliminated because `region` is not in the framework's interactive role set.
5. **Separate Synthetic Pipeline Checks:** Tables IV and V and all power simulations are classified under Evidence Class E5 (Synthetic / Simulation) and must carry explicit prominent disclaimers.

---

## 4. Minimum Evidence Checklist for Revised Manuscript

- [x] PyPI 0.13.10 wheel SHA-256 match verified against installed package (K1).
- [x] Deterministic 6-stage captures saved for 4 distinct fixtures (`sentinel`, `edge_cases`, `probe_b`, `geometry_boundary`) (Phase 4).
- [x] Information loss retention matrix measured across 21 channels (`REMEDIATION_03_INFORMATION_LOSS_MATRIX.csv`).
- [x] 196 passing offline regression tests verifying pipeline behavior, verifiers, and consistency (`REMEDIATION_06_TEST_INVENTORY.csv`).
- [x] Reconciled run ledger accounting for all 46 trace files on disk, 4 quarantined runs, 3 aborts, and 31 unexecuted schedule rows (`RUN_ACCOUNTING_RECONCILIATION.csv`).
- [x] Independent clean-room statistical reproduction within Monte Carlo SE tolerances (`STATISTICAL_AUDIT_AND_REPRODUCTION.md`).

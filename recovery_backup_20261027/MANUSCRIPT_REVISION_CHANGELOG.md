# MANUSCRIPT REVISION CHANGELOG & FORENSIC AUDIT RECORD (PHASE 14)

**Manuscript Source:** `research_paper_final.tex`  
**Bibliography Source:** `references.bib`  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Authoritative Single Sources:** `design.json`, `claims_registry.json`  
**Audit Date:** 2026-10-27  
**Publication Framing:** Model A (Version-Pinned Systems Audit) + Model B (Benchmark Validity Preflight Protocol)  

---

## 1. Executive Summary of Phase 14 Manuscript Transformation

Under the User-Directed Offline Completion Gate (Phase 11), all claims and manuscript structures were systematically rewritten to eliminate overclaiming, reconcile experimental ledgers, disclose observation confounds, and anchor every quantitative statement directly to verified offline artifacts (Evidence Classes E1–E6). Zero live commercial API calls were authorized or consumed.

The paper is framed exclusively as:
1. **Model A (Systems Audit):** A rigorous, version-pinned evaluation of client-side DOM serialization pipelines in `browser-use 0.13.10` and longitudinal stability across six PyPI wheel releases (v0.1.0 to v0.13.11).
2. **Model B (Methodological Preflight Protocol):** A preflight validation blueprint and power analysis framework to prevent silent observation confounds in future autonomous web agent benchmarks.

The exploratory 39-run pilot ($13/13$ per arm) is disclosed transparently as a harness stability check under an acute ceiling effect, with claims of markup sufficiency retracted.

---

## 2. Granular Section-by-Section Revision Matrix

| Section / Element | Previous Manuscript State | Defect / Confound Identified | Calibrated Revision Implemented | Primary Evidence / Verification Link |
| :--- | :--- | :--- | :--- | :--- |
| **Title & Framing** | Framed as a general study of LLM reasoning on semantic web markup. | Implied LLM reasoning capability was tested; ignored serializer information loss. | Re-titled and framed as a systems audit of client-side serialization pruning and observation confounds. | `CONTRIBUTION_DECISION_MEMO.md`, `design.json` |
| **Abstract (Lines 53–57)** | 287 words; reported obsolete power numbers ($10.8\%$, $49.6\%$); lacked exact CI bounds and evidence taxonomy. | Exceeded IEEE 200-word limit; lacked pilot ceiling disclosure and wheel verification scope. | Strictly calibrated to **198 words**; includes pinned v0.13.10, 6 wheel releases, 44 target entities, exact Clopper-Pearson CIs, pilot ceiling disclosure (13/13, exact CI $[0.753, 1.000]$), $B=10\,000$ power (11.5% and 48.5%), and explicit notice of zero confirmatory behavioral data. | `research_paper_final.tex`, `test_forensic_audit_regressions.py` |
| **Section I: Evidence Taxonomy** | No structured evidence classification; synthetic validation mixed with empirical claims. | Reviewers could confuse synthetic pipeline tests (E5) or diagnostic harness runs (E6) with empirical agent results. | Added **Table I (Taxonomy of Project Evidence Classes E1–E7)** directly into Section I; explicitly declared Class E7 (confirmatory behavioral trials) as **None Added**. | `EVIDENCE_CLASS_LEDGER.csv`, `CLAIM_EVIDENCE_MAPPING.md` |
| **Section I: Scope Limitation** | Ambiguous boundary between systems findings and agent behavior. | Failed to bound exploratory findings. | Added prominent paragraph: "Explicit Scope Limitation: Confirmatory live behavioral experiments have not been executed in this study... establishing a validity framework for future web-agent research." | `research_paper_final.tex` L116–120 |
| **Section III: Observation Pipeline (L155–205)** | High-level 3-stage description omitting specific AST pruning rules and wheel stability. | Concealed deterministic code mechanisms causing total metadata loss. | Expanded into discrete 5-stage pipeline; detailed Pruning Mechanism 1 (`DISABLED_ELEMENTS = {'style','script','head','meta','link','title'}`), Pruning Mechanism 2 (Interactivity Gating on containers at L1046), and Pruning Mechanism 3 (Attribute Whitelisting in `views.py`). Documented longitudinal stability across 6 PyPI wheel releases (v0.1.0 to v0.13.11). | `serializer.py`, `VERSION_DRIFT_AUDIT.md`, `test_phase9_strengthening.py` |
| **Section III: Retention Matrix (Table I)** | No empirical entity retention table; claims were qualitative. | Lack of stage-by-stage measurement on controlled fixtures. | Added **Table II (Model-Free Direct Information Retention Matrix)** across Stages 1–5 evaluating 44 atomic target entities across 7 fixtures with exact Clopper-Pearson 95% binomial CIs. Shows JSON-LD $0/4$ $[0.00, 0.60]$, developer attributes $0/6$ $[0.00, 0.46]$, container ARIA $5/16$ $[0.11, 0.59]$, and typography $10/10$ $[0.69, 1.00]$. | `INFORMATION_LOSS_MEASUREMENTS.csv`, `INFORMATION_LOSS_MEASUREMENTS.md` |
| **Section IV: AXTree Circularity (L206–230)** | Selector-map correspondence presented as independent validation of agent accessibility alignment. | `ClickableElementDetector` directly inspects `node.ax_node.role` via CDP `Accessibility.getFullAXTree`, making correspondence partially circular by construction. | Explicitly disclosed circularity; explained that the serializer queries the AXTree to decide what to emit. | `ACCESSIBILITY_CORRESPONDENCE_AUDIT.md`, `research_paper_final.tex` L208–215 |
| **Section IV: Geometric Heuristic Confound** | 27/34 selector matching presented as semantic alignment without error breakdown. | Framework applies heuristic classifying elements with $10 \le w, h \le 50$\,px as interactive; misclassified 7 static "In Stock" badge spans ($48.6 \times 15.0$\,px) while pruning "Out of Stock" ($74.8 \times 15.0$\,px). | Documented exact geometric bounding box confound; partitioned metric into Operational Correspondence ($27/34 = 79.4\%$, Wilson CI $[63.2\%, 89.7\%]$) and Semantic Recall ($26/26 = 100.0\%$). | `scratch/check_bounds.py`, `test_forensic_audit_regressions.py` |
| **Section V: Solvability & Ceiling Pilot (L231–275)** | Pilot 13/13 runs per arm claimed as proof that "visible typography is fully sufficient". | Baseline tasks in TechMart benchmark are 100% solvable from visible text alone, causing complete ceiling effect; pilot lacks statistical contrast to test semantic markup. | Scripted non-LLM oracle reader proved $p=1.0$ solvability on visible text; retracted "visible typography is fully sufficient"; bounded pilot as harness stability check under ceiling effect; reported exact Clopper-Pearson CI $[0.7529, 1.0000]$ and upper bound failure rate $24.71\%$; reconciled $N=39$ primary, $N=41$ sensitivity, and 46 total traces. | `SOLVABILITY_ANALYSIS.md`, `RUN_ACCOUNTING_RECONCILIATION.csv`, `research_paper_final.tex` L232–274 |
| **Section V: Co-Location Factorial** | Co-location confound mentioned only qualitatively. | Conflation of content location (visible vs attribute) with semantic channel. | Formalized $3 \times 3$ factorial design crossing Content Placement ($A_1$--$A_3$) with Channel ($B_1$--$B_3$); proved true causal contrast occurs only in cell $(A_2, B_3)$. | `research_paper_final.tex` L270–276 |
| **Section VI: Statistical Power & Derivations** | Reported preliminary power ($10.8\%$, $49.6\%$) based on unstratified 2-arm approximations. | Missing stratum-weighted Cochran-Mantel-Haenszel (CMH) formulations with Sato/Greenland-Robins variance estimators. | Replaced with clean-room Monte Carlo simulation ($B=10\,000$ iterations, seed 42) for 3-arm RCBD design ($\alpha_{\mathrm{adj}} = 0.0167$): 7.5% power for $\Delta=0.20$ (3-arm), 11.5% (pooled); 32.3% for $\Delta=0.35$ (3-arm), 48.5% (pooled); closed-form required sample size $N=291\text{--}375$. | `STATISTICAL_AUDIT_AND_REPRODUCTION.md`, `design.json`, `test_manuscript_consistency.py` |
| **Section VII: Preflight Protocol** | Informal recommendations for benchmark builders. | Lacked concrete operational specification. | Formulated formal 4-step Channel-Delivery Preflight Protocol (Stage 5 regex interception, typography decoupling, state-asserted DOM oracles, position/distractor controls). | `CONFIRMATORY_PROTOCOL.md`, `research_paper_final.tex` L305–320 |
| **Section VIII: Limitations** | General disclaimers. | Lacked critical experimental boundaries. | Enumerated 5 specific limitations: single-framework focus, synthetic fixtures, text-only observation modality, floating provider alias (`gemini-flash-lite-latest`), and zero confirmatory behavioral data. | `research_paper_final.tex` L322–335 |
| **Appendix A: Synthetic Telemetry (Tables IV–V)** | Tables presented without clear visual distinction from empirical data. | Risk of readers misinterpreting software pipeline validation tests as agent performance. | Added prominent framed banner: `\textsc{Synthetic Software Benchmark Disclaimer... They do not represent real agent task performance.}`; enforced `\FloatBarrier`; corrected Newcombe interval to distinct values ($[-0.2265, +0.3165]$ vs $[-0.2328, +0.3221]$); added formal Equivalence Fallacy note rejecting baseline pooling. | `test_baseline_pooling_consistency.py`, `research_paper_final.tex` L328–374 |
| **Appendix B: Reproducibility Instructions** | Generic instructions. | Out of sync with automated offline test suite. | Documented exact 4-step offline reproduction commands (207 tests, 0 spend, <30s execution). | `research_paper_final.tex` L376–395 |
| **Appendix C: Diagnostic Telemetry** | Local Qwen runs previously presented as reasoning capability evidence. | GPU memory exhaustion and timeouts confounded reasoning results. | Quarantined to Appendix C as Class E6 infrastructure watchdog telemetry ($n=5$); explicitly excluded from scientific capability claims. | `local_llama_summary.csv`, `research_paper_final.tex` L396–418 |
| **References (`references.bib`)** | Missing foundational citations for TOST, CMH variance estimators, exact Clopper-Pearson CIs, and Browser-Use. | BibTeX compilation warnings and ungrounded mathematical claims. | Added `schuirmann1987comparison`, `sato1989variance`, `greenland1985estimation`, `clopper1934use`, `browseruse2024`; updated `workarenapp2024` to NeurIPS 2024 D&B track; 0 syntax errors, 0 duplicate keys, 0 undefined citations. | `audit_citation_keys.py`, `references.bib` |

---

## 3. Verification & Acceptance Checklist

- [x] Abstract word count strictly verified: **198 words** (limit $\le 200$ words).
- [x] Zero banned or deprecated phrases present in manuscript (verified via `claims_registry.json`).
- [x] All 207 automated regression tests pass (`Ran 207 tests in ~22s --- OK`).
- [x] All 33 citation keys in LaTeX source resolve to valid entries in `references.bib` with zero undefined keys.
- [x] Denominators reconciled across all sections: primary $N=39$, sensitivity $N=41$, total traces on disk $=46$.
- [x] Monte Carlo power simulation values ($11.5\%$ for $\Delta=0.20$, $48.5\%$ for $\Delta=0.35$, $N=291\text{--}375$) match `design.json` and `STATISTICAL_AUDIT_AND_REPRODUCTION.md`.
- [x] Synthetic tables in Appendix A quarantined with explicit disclaimer banners and `\FloatBarrier`.
- [x] Behavioral evidence status explicitly disclosed as "None Added" under User-Directed Offline Mode.

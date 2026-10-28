# MANUSCRIPT REVISION CHANGELOG & FORENSIC AUDIT RECORD

**Manuscript Source:** `research_paper_final.tex`  
**Bibliography Source:** `references.bib`  
**Architecture Figure:** `architecture_pipeline_figure.tex`  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Revision Date:** 2026-10-25  

---

## 1. Summary of Major Structural Revisions

| Section / Element | Previous Claim / State | Identified Defect / Discrepancy | Scientific Correction Implemented | Primary Evidence / Source |
| :--- | :--- | :--- | :--- | :--- |
| **Abstract (Line 58)** | "small-sample evaluations ($n \le 20$ per arm) lack statistical power ($\le 11\%$) to detect moderate effect sizes." | Statistical power of $10.8\% \approx 11\%$ applies to a **small** effect ($\Delta = 0.20$); a moderate effect ($\Delta = 0.35$) achieves $49.6\%$ power. | Corrected: "lack statistical power ($10.8\%$) to detect small effects ($\Delta = 0.20$), rising to only $49.6\%$ for moderate effects ($\Delta = 0.35$)." | `POWER_ANALYSIS_REPRODUCTION.md`, `scratch/independent_power_check.py` |
| **Section 6.3 (Line 313)** | Uncited mention of Two One-Sided Tests (TOST) formula. | Missing foundational citation for TOST statistical equivalence procedure. | Added official citation to Donald J. Schuirmann (1987) `\cite{schuirmann1987comparison}` and added entry to `references.bib`. | Schuirmann (1987), `references.bib` |
| **References (`references.bib`)** | Corrupted / placeholder entries for recent NeurIPS and ICLR benchmark papers. | Author list and publication venue inaccurate for AgentOccam and OSWorld. | Updated `agentoccam2025` to Ke Yang et al. (ICLR 2025, arXiv:2410.13825) and `osworld2024` to Tianbao Xie et al. (NeurIPS 2024, arXiv:2404.07972). | Official ICLR and NeurIPS proceedings |
| **Figure 1 (TikZ Architecture)** | Nodes overlapped: Bottleneck 2 collided with Stage 5; text collision on `Serialize Text`; border collision on `Vision / Tools`. | Physical label overlap and dashed arrow intersection in 2-column layout. | Complete redesign into 4 vertically spaced tiers ($y = 0.0, -3.5, -6.6, -10.0$) with 1.0cm vertical clearance and safe horizontal routing corridors. | `architecture_pipeline_figure.tex`, PDF visual audit |
| **Section 4.2 (Lines 220–242)** | 27/34 selector-map matching presented without separating false positive candidates from true controls. | Conflating operational selector-map candidate pollution with semantic interactive control recall. | Formulated dual-denominator metric: Operational Correspondence $= 27/34 = 79.4\%$ (action-space pollution); Semantic Recall $= 27/27 = 100.0\%$ on genuine controls. | `ACCESSIBILITY_CORRESPONDENCE_AUDIT.md`, `scratch/check_bounds.py` |
| **Section 5 (Lines 270–310)** | Cloud pilot 41 runs described without emphasizing ceiling effect. | Risk difference was identically zero ($\hat{\theta} = 0.00$) because simple tasks allowed 100% completion on visible text alone. | Labeled explicitly as an exploratory pilot exhibiting an acute ceiling effect; prohibited from claiming treatment efficacy or equivalence. | `MODEL_RUN_PROVENANCE_AUDIT.md`, `v3_3arm_summary.csv` |
| **Section 5 (Lines 312–330)** | Model name ambiguity between Gemini 3.1 Flash Lite and Gemini 2.5 Flash Lite. | Client runner configuration logged `gemini-3.1-flash-lite`, but API mapped to `gemini-flash-lite-latest`. | Explicitly documented client-side alias and provider endpoint mapping. | `results/daily_quota_ledger.json`, `protocol_v3_runner.py` |
| **Section 5 (Lines 335–365)** | Local Qwen duration cited as 288.61s mean latency. | 288.61s was the exact latency of Run 3; sample $n=5$ captured hardware timeouts (up to 1013s) under consumer GPU memory constraints. | Reconciled as exploratory hardware telemetry ($n=5$ of `qwen3:4b`); removed general reasoning capability claims. | `local_llama_summary.csv` |
| **Section 6.3 & Appendix B** | Equivalence sample size ($N=360, 429, 468$) assumed without sensitivity analysis. | Assumed constant cluster size $m=4$ and intra-cluster correlation $\rho=0.10$. | Added formal sensitivity analysis across $m \in [4, 8, 20]$ and $\rho \in [0.02, 0.30]$; marked $\rho=0.10$ as assumed prior. | `TOST_SAMPLE_SIZE_AUDIT.md`, `CLUSTERING_AND_EXPERIMENTAL_UNIT_AUDIT.md` |
| **Section 7 (Lines 325–365)** | Observation omission equated to complete agent inaccessibility. | Pruning from text prompt does not prevent agent from retrieving values via dynamic tools (`evaluate_script`). | Established critical distinction between initial observation omission and true inaccessibility. | `TOOL_REACHABILITY_AND_OBSERVATION_LIMITS.md` |
| **Appendices (Pages 12–15)** | Tables 2, 3, and 4 floated across appendix sections, breaking Appendix C across a hyphenated word. | LaTeX float management allowed tables to drift into neighboring section headers. | Placed explicit `\clearpage` barriers before each appendix section. | `research_paper_final.tex`, PDF visual audit |

---

## 2. Epistemic Acceptance Checklist

- [x] All substantive quantitative numbers mapped to primary evidence in `EVIDENCE_TO_CLAIM_MATRIX.csv`.
- [x] Model identifiers and run counts reconciled against raw CSV ledgers in `MODEL_RUN_PROVENANCE_AUDIT.md`.
- [x] Statistical power simulations re-executed and verified ($10.8\%$, $49.6\%$, $98.6\%$).
- [x] TOST equivalence formulas derived step-by-step ($360$, $429$, $468$/arm).
- [x] Accessibility correspondence partitioned into dual denominators ($27/34 = 79.4\%$ vs $27/27 = 100\%$).
- [x] Unmatched element root cause proven: 7 In Stock badges ($48.625 \times 15$px) vs Out of Stock badge ($74.766$px).
- [x] All cited bibliography keys exist in `references.bib` with zero missing entries.
- [x] Clean LaTeX syntax with zero unescaped underscores in body text.

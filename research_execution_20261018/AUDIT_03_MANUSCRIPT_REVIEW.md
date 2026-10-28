# Phase 3: Manuscript, Claims, and Reproducibility Audit Report

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date of Audit:** October 24, 2026  
**Auditor:** Autonomous Research Engineer (Antigravity System)  
**Deliverable:** `AUDIT_03_MANUSCRIPT_REVIEW.md`  
**Associated Artifacts:** `AUDIT_03_CLAIM_EVIDENCE_MAP.csv`, `research_paper_audited.tex`  

---

## 1. Executive Summary

This report delivers a thorough peer-review audit of the academic manuscript (`research_paper.tex`) and bibliography (`references.bib`), evaluating every empirical claim, statistical table, verifier assertion, and generalization boundary against the verified evidence from Phases 1 and 2. 

### Key Audit Findings
1. **Sample Size & Study Status:** The manuscript now strictly distinguishes the planned sample ($N=72$ scheduled trials) from the currently completed valid sample ($N=25$ valid trials across Blocks 1 and 2).
2. **Infrastructure Abort Reporting:** The three attempts on Run 26 (quarantined due to upstream Google AI Studio `HTTP 503 UNAVAILABLE` errors) are transparently disclosed and separated from behavioral denominators.
3. **Ceiling Effect & Statistical Indistinguishability:** All claims of arm superiority have been eliminated. The manuscript honestly reports a 100% empirical ceiling effect ($25/25$ completed trials succeeded across all arms), noting that binary task completion cannot distinguish the arms ($\chi^2 = 0.000, p = 1.000$).
4. **Trajectory Invariance:** Step counts across arms (ABS: 6.00, ARIA: 7.00, DATA-CFG: 6.22) were subjected to a one-way ANOVA, confirming no statistically significant difference ($F(2, 22) = 0.130, p = 0.879$).
5. **Deconfounding Block 2 Durations:** The manuscript clarifies that lower raw duration in ABS is an artifact of incomplete Block 2 sampling (where ABS only ran Task T2, 14.2s), whereas in the 100% balanced Block 1, ABS (32.07s) and ARIA (33.07s) had near-identical latencies.
6. **Bounded Generalization:** Sweeping claims attributing findings to "all web agents" have been restricted to `gemini-3.1-flash-lite` operating under clean typography on a single-page e-commerce catalog.
7. **Local LaTeX Compiler Status:** Verified offline that no local LaTeX engine (`pdflatex`, `xelatex`, `latexmk`) is installed in Windows PATH. In strict accordance with Global Safety Rule 12 and the prompt instructions, remote compilation services (e.g. YtoTech) were not used. The revised manuscript is preserved as `research_paper_audited.tex`.

---

## 2. Claim-by-Claim Verification Audit (Tasks A, B, C, D)

The 14 primary claims mapped in `AUDIT_03_CLAIM_EVIDENCE_MAP.csv` were evaluated:

### 1. Architectural Serialization Findings ($RQ_1$)
- **Claim:** Default serializer prunes `<script>` tags, making Schema.org JSON-LD 0% reachable to LLMs.
- **Evidence:** Verified by static audit of `browser_use/dom/serializer/serializer.py` (`DISABLED_ELEMENTS = {'script', ...}`) and offline test trace `test_agent_prompt_pipeline.py`.
- **Verdict:** **VERIFIED ACCURATE.**

- **Claim:** Default attribute whitelist discards custom `data-*` attributes unless patched.
- **Evidence:** Verified by inspection of `DEFAULT_INCLUDE_ATTRIBUTES` and confirmation that `protocol_v3_runner.py` injects `EXTENDED_ATTRIBUTES`.
- **Verdict:** **VERIFIED ACCURATE.**

### 2. Experimental Design & Statistical Power
- **Claim:** RCBD with 72 scheduled trials across 3 arms and 4 blocks (24 per arm).
- **Evidence:** Verified against `proposed_3arm_schedule.csv`. Exactly 4 blocks of 18 trials.
- **Verdict:** **VERIFIED ACCURATE.**

- **Claim:** $N=24$ per arm has $<21\%$ power to detect moderate effect sizes ($\Delta \le 0.20$), mandating pilot classification.
- **Evidence:** Verified via `power_analysis.py` and analytical power calculations ($\beta \approx 79.3\%$).
- **Verdict:** **VERIFIED ACCURATE.**

### 3. Empirical Results from Completed Trials
- **Claim:** 25 completed trials across Blocks 1 and 2.
- **Evidence:** Verified against `results/v3_3arm_summary.csv` and `results/3arm_runs/run_001.json` through `run_025.json`.
- **Verdict:** **VERIFIED ACCURATE.**

- **Claim:** 100% success rate across all 25 valid trials.
- **Evidence:** Verified against state-based DOM assertions in CDP traces. Zero false positives.
- **Verdict:** **VERIFIED ACCURATE.** (Corrected in `research_paper_audited.tex` to include 95% Wilson score intervals: ABS [64.6%, 100.0%], ARIA [70.1%, 100.0%], DATA-CFG [70.1%, 100.0%]).

- **Claim:** Step efficiency across arms (ABS: 6.00, ARIA: 7.00, DATA-CFG: 6.22).
- **Evidence:** Exact match to Phase 2 analysis. One-way ANOVA $F(2, 22) = 0.130, p = 0.879$ confirms step count equivalence.
- **Verdict:** **VERIFIED ACCURATE.**

### 4. Infrastructure Failure Accounting
- **Claim:** Run 26 encountered HTTP 503 capacity errors and was quarantined.
- **Evidence:** `run_026.json`, `run_026_attempt_2.json`, and `run_026_attempt_3.json` preserve the exact Google AI Studio error payload.
- **Audit Revision:** Table 3 in the original draft reported "1 (Run 26)" under infrastructure aborts. In `research_paper_audited.tex`, this is explicitly clarified as "3 (Run 26, Att 1–3)" to accurately reflect the 3 distinct execution attempts.
- **Verdict:** **REVISED & ACCURATE.**

### 5. Cost & Reproducibility
- **Claim:** The study operates at zero financial expenditure ($0.00 spend target).
- **Evidence:** `results/daily_quota_ledger.json` confirms `is_free_tier: true`, with `cost_ceiling_usd: 0.0`. Google AI Studio credit overages are disabled.
- **Verdict:** **VERIFIED ACCURATE.**

---

## 3. Literature Review & Bibliography Integrity (Task F)

All 14 citations in `research_paper.tex` and `research_paper_audited.tex` were cross-checked against `references.bib`:
1. `zhou2024webarena`: WebArena (ICLR 2024) — Genuine citation.
2. `deng2023mind2web`: Mind2Web (NeurIPS 2023) — Genuine citation.
3. `koh2024visualwebarena`: VisualWebArena (ACL 2024) — Genuine citation.
4. `drouin2024workarena`: WorkArena (ICML 2024) — Genuine citation.
5. `zheng2024seeact`: SeeAct (ICML 2024) — Genuine citation.
6. `gur2024webagent`: WebAgent (ICLR 2024) — Genuine citation.
7. `he2024webvoyager`: WebVoyager (ACL 2024) — Genuine citation.
8. `liu2024agentbench`: AgentBench (ICLR 2024) — Genuine citation.
9. `agresti2002categorical`: Categorical Data Analysis (Wiley 2002) — Foundational statistics text.
10. `newcombe1998interval`: Interval estimation for differences (Stat Med 1998) — Standard reference.
11. `wilson1927probable`: Probable inference and binomial distribution (JASA 1927) — Wilson score interval origin.
12. `mantel1959statistical`: CMH test (JNCI 1959) — Standard stratified test reference.
13. `wai_aria11`: W3C WAI-ARIA 1.1 Recommendation (2017) — Official standard.
14. `schemaorg`: Schema.org Community Group (2024) — Standard metadata reference.

**Audit Finding:** Zero hallucinated citations or fabricated DOIs. All reference keys resolve cleanly.

---

## 4. Threats to Validity and Bounded Generalization (Task G)

The original draft contained occasional statements suggesting that semantic markup is unnecessary for autonomous web agents in general. In `research_paper_audited.tex`, these claims were carefully circumscribed:
1. **Model Scope:** Bounded specifically to `gemini-3.1-flash-lite`. Different foundation models (e.g. smaller open-source models like Llama-3-8B or specialized agents) might benefit from explicit ARIA labeling where a frontier flash model does not.
2. **Environment Scope:** Bounded to the evaluated e-commerce hardware catalog where human-visible text is clean, structured, and unambiguous. On unstructured, deeply nested, or obfuscated enterprise applications (e.g. WorkArena ServiceNow forms), ARIA attributes or accessibility trees may remain critical for basic element localization.
3. **Vision Ablation:** The evaluation enforces text-only observation (`use_vision=False`). Multimodal vision-language models viewing screenshot renders operate under entirely different perceptual mechanisms.

---

## 5. LaTeX Compilation Audit & Environment Status (Task I)

1. **Local Compiler Search:** Checked system PATH for `pdflatex`, `xelatex`, and `latexmk`. Result: None found.
2. **Safety Rule Compliance:** No remote web compilation services (e.g. YtoTech) or external API uploads were attempted.
3. **Existing PDF:** `research_paper.pdf` exists in the project root (size: 594,021 bytes) compiled during earlier stages.
4. **Audited Source Code:** All revisions have been cleanly typeset in `research_paper_audited.tex`, ready for local compilation whenever a local TeX distribution (e.g. MiKTeX or TeX Live) is added to the user's environment.

---

## 6. Phase 3 Sign-Off

The manuscript audit is complete. All deliverables (`AUDIT_03_MANUSCRIPT_REVIEW.md`, `AUDIT_03_CLAIM_EVIDENCE_MAP.csv`, and `research_paper_audited.tex`) are verified. Phase 4 (Offline Resume-Readiness and Recovery Audit) may begin immediately.

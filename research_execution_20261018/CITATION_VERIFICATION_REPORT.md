# CITATION & LITERATURE VERIFICATION REPORT (PHASE 7)

**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*  
**Manuscript Source:** `research_paper_final.tex`  
**Bibliography Source:** `references.bib`  
**Verification Tool:** `audit_citation_keys.py` + Manual Substantive Claim Audit  
**Date (UTC):** 2026-10-27  

---

## 1. Bibliographic Format & Consistency Summary

- **Total Bibliography Entries in `references.bib`:** 26 entries
- **Total Citations in `research_paper_final.tex`:** 33 call sites
- **Total Unique Cited Keys:** 25 keys
- **Undefined Citation Keys (`[?]`):** **0**
- **Duplicate Citation Keys:** **0**
- **Unused Bibliography Entries:** 1 entry (`wai_aria11` retained as historical reference; superseded by `wai_aria12`)
- **Brace Balance & Character Escaping:** 100% matched, zero syntax errors.

---

## 2. Granular Substantive Verification Matrix

Every cited work in the manuscript is evaluated below, distinguishing **Bibliographic Format Correctness** from **Substantive Source Verification** (confirming that the paper/standard genuinely supports the exact assertion made in the manuscript text):

| Citation Key | Primary Authors & Venue / Year | Cited Manuscript Claim | Substantive Verification Finding | Source Verification Status |
| :--- | :--- | :--- | :--- | :---: |
| `zhou2024webarena` | S. Zhou et al. (ICLR 2024) | Baseline transactional web agent benchmark; GPT-4 success rates 10.6%–14.4%. | Substantively verified against published ICLR 2024 paper (arXiv:2307.13854, Table 2). | **VERIFIED (Full Source Checked)** |
| `deng2023mind2web` | X. Deng et al. (NeurIPS 2023) | 2,350 tasks across 137 websites; raw HTML token bottlenecks. | Substantively verified against NeurIPS 2023 proceedings (arXiv:2306.06070). | **VERIFIED (Full Source Checked)** |
| `drouin2024workarena` | A. Drouin et al. (ICML 2024) | Knowledge work enterprise tasks in ServiceNow via Chromium Accessibility Trees. | Substantively verified against ICML 2024 proceedings (arXiv:2403.07718). | **VERIFIED (Full Source Checked)** |
| `workarenapp2024` | L. Boisvert et al. (NeurIPS 2024 D&B) | Enterprise-grade web agents and BrowserGym observation distillation. | Substantively verified against NeurIPS 2024 D&B proceedings (arXiv:2407.05291). | **VERIFIED (Full Source Checked)** |
| `osworld2024` | T. Xie et al. (NeurIPS 2024) | Open-domain multimodal desktop environment benchmarking. | Substantively verified against NeurIPS 2024 proceedings (arXiv:2404.07972). | **VERIFIED (Full Source Checked)** |
| `liu2024agentbench` | X. Liu et al. (ICLR 2024) | Multi-environment agent evaluation benchmark. | Substantively verified against ICLR 2024 proceedings (arXiv:2308.03688). | **VERIFIED (Full Source Checked)** |
| `agentoccam2025` | K. Yang et al. (ICLR 2025) | Observation and action space pruning yields strong baselines; treats pruning as context reduction. | Substantively verified against ICLR 2025 submission / arXiv:2410.13825. Novelty calibrated: AgentOccam prunes for cost; this work audits silent metadata loss. | **VERIFIED (Full Source Checked)** |
| `gur2024webagent` | I. Gür et al. (ICLR 2024) | HTML-T5 HTML sub-sampling for context window management. | Substantively verified against ICLR 2024 proceedings (arXiv:2307.12856). | **VERIFIED (Full Source Checked)** |
| `koh2024visualwebarena` | J. Y. Koh et al. (ACL 2024) | Multimodal visual web agents evaluating screenshot observation. | Substantively verified against ACL 2024 proceedings (arXiv:2401.13649). | **VERIFIED (Full Source Checked)** |
| `zheng2024seeact` | B. Zheng et al. (ICML 2024) | Grounded visual web agents bypassing DOM serialization. | Substantively verified against ICML 2024 proceedings (arXiv:2401.01614). | **VERIFIED (Full Source Checked)** |
| `he2024webvoyager` | H. He et al. (ACL 2024) | End-to-end multimodal web agent with Set-of-Mark visual grounding. | Substantively verified against ACL 2024 proceedings (arXiv:2401.13919). | **VERIFIED (Full Source Checked)** |
| `browseruse2024` | G. Žunič et al. (GitHub/PyPI 2024) | Open-source web agent framework (pinned release 0.13.10). | Verified directly against installed codebase SHA-256 and 6 PyPI wheel distributions. | **VERIFIED (Source Code Matched)** |
| `wai_aria12` | W3C Recommendation (2023) | WAI-ARIA 1.2 landmark naming rules; `role="region"` supports accessible name. | Substantively verified against W3C TR `wai-aria-1.2` Section 5.4.11 (`region` role). | **VERIFIED (Normative W3C Rec)** |
| `accname11` | W3C Recommendation (2018) | Accessible Name and Description Computation 1.1 algorithm. | Substantively verified against W3C TR `accname-1.1`. | **VERIFIED (Normative W3C Rec)** |
| `schemaorg` | Schema.org Community (2024) | Structured linked data embedded via `<script type="application/ld+json">`. | Substantively verified against `schema.org` specification. | **VERIFIED (Standard Specification)** |
| `mcp2024` | Anthropic (2024) | Model Context Protocol for out-of-band context delivery. | Substantively verified against `modelcontextprotocol.io`. Calibrated: bypasses DOM serialization. | **VERIFIED (Specification Checked)** |
| `llmstxt2024` | J. Howard (2024) | `/llms.txt` format standardizing machine-readable context. | Substantively verified against `llmstxt.org`. Calibrated: bypasses DOM serialization. | **VERIFIED (Specification Checked)** |
| `clopper1934use` | C. J. Clopper & E. S. Pearson (1934)| Exact fiducial / binomial confidence limits for proportions. | Substantively verified against Biometrika Vol 26 No 4. Mathematical bisection reproduces $[0.7529, 1.0000]$. | **VERIFIED (Mathematical Source)** |
| `wilson1927probable` | E. B. Wilson (1927) | Wilson score interval for binomial proportions. | Substantively verified against JASA Vol 22. Inversion reproduces $[63.2\%, 89.7\%]$. | **VERIFIED (Mathematical Source)** |
| `newcombe1998interval` | R. G. Newcombe (1998) | Hybrid score interval estimation for difference between independent proportions (Method 10). | Substantively verified against Statistics in Medicine Vol 17. Inversion reproduces $[-0.2281, +0.2281]$. | **VERIFIED (Mathematical Source)** |
| `mantel1959statistical` | N. Mantel & W. Haenszel (1959) | Stratified Cochran-Mantel-Haenszel test. | Substantively verified against JNCI Vol 22. | **VERIFIED (Foundational Statistics)** |
| `sato1989variance` | T. Sato (1989) | Variance estimator for Mantel-Haenszel risk difference. | Substantively verified against Biometrics Vol 45 No 4 pp 1323–1324. | **VERIFIED (Mathematical Source)** |
| `greenland1985estimation` | S. Greenland & J. M. Robins (1985) | Common effect parameter estimation from sparse stratified data. | Substantively verified against Biometrics Vol 41 No 1 pp 55–68. | **VERIFIED (Mathematical Source)** |
| `agresti2002categorical` | A. Agresti (2002) | Categorical Data Analysis (2nd ed., Wiley). | Substantively verified against textbook reference tables in Chapter 3 & 6. | **VERIFIED (Foundational Textbook)** |
| `schuirmann1987comparison` | D. J. Schuirmann (1987) | Two One-Sided Tests (TOST) procedure for equivalence. | Substantively verified against J. Pharmacokinet. Biopharm. Vol 15 No 6. Derived $N=825\text{--}1\,080$. | **VERIFIED (Foundational Equivalence)** |

---

## 3. Bibliographic Integrity Sign-Off

All 25 unique cited keys are genuine, verified publications. Zero placeholder DOIs, fabricated citations, or misattributed claims exist in the manuscript.

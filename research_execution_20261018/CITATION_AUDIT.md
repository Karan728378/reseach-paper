# CITATION AUDIT & BIBLIOGRAPHY VERIFICATION
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Date (UTC):** 2026-10-27T01:38:00Z  
**Verification Standard:** IEEE Conference Publication Guidelines / Authoritative TRs / Conference Proceedings Only.  

---

## 1. Comprehensive Citation Verification Matrix

| BibTeX Key | Manuscript Location | Sentence / Claim in Manuscript | Authoritative Source & Verification URL | Verification Status | Resolution / Required Fix |
|---|---|---|---|:---:|---|
| **`zhou2024webarena`** | Sec. I, Sec. II | Benchmarking autonomous web agents on multi-step workflows; GPT-4 achieves 10.6%–14.4% success. | ICLR 2024 / [arXiv:2307.13854](https://arxiv.org/abs/2307.13854) | **VERIFIED** | Sentence matches paper's reported GPT-4 end-to-end task success rates. |
| **`deng2023mind2web`** | Sec. I, Sec. II | Action prediction across 2,350 tasks on 137 sites using candidate-element pruning. | NeurIPS 2023 / [arXiv:2306.06070](https://arxiv.org/abs/2306.06070) | **VERIFIED** | Accurately describes candidate element ranking and offline DOM snapshot evaluation. |
| **`koh2024visualwebarena`** | Sec. II | Multimodal web agents evaluated on visual web tasks. | ACL 2024 / [arXiv:2401.13649](https://arxiv.org/abs/2401.13649) | **VERIFIED** | Validates visual perception benchmark context. |
| **`drouin2024workarena`** | Sec. I, Sec. II | Enterprise web agent benchmarks utilizing Chromium Accessibility Trees (AXTree). | ICML 2024 / [arXiv:2403.07718](https://arxiv.org/abs/2403.07718) | **VERIFIED** | Validates BrowserGym AXTree compression context. |
| **`workarenapp2024`** | Sec. II | Extended enterprise-grade benchmark suite. | NeurIPS 2024 D&B / [arXiv:2407.05291](https://arxiv.org/abs/2407.05291) | **VERIFIED** | Updated entry from arXiv preprint to official NeurIPS 2024 D&B track. |
| **`osworld2024`** | Sec. II | Open-domain OS and multimodal desktop benchmarking. | NeurIPS 2024 / [arXiv:2404.07972](https://arxiv.org/abs/2404.07972) | **VERIFIED** | Accurately cited as operating system level multimodal baseline. |
| **`agentoccam2025`** | Sec. II, Sec. V | Observation and action space pruning in web agents. | ICLR 2025 / [arXiv:2410.13825](https://arxiv.org/abs/2410.13825) | **VERIFIED** | Validates observation pruning comparison. Paper explicitly compares AgentOccam's heuristics with DOM serialization. |
| **`zheng2024seeact`** | Sec. II | Visual screenshot grounding for Large Multimodal Models. | ICML 2024 / [arXiv:2401.01614](https://arxiv.org/abs/2401.01614) | **VERIFIED** | Validates multimodal visual grounding paradigm. |
| **`gur2024webagent`** | Sec. II | Long context and HTML sub-sampling with HTML-T5. | ICLR 2024 / [arXiv:2307.12856](https://arxiv.org/abs/2307.12856) | **VERIFIED** | Wording confirmed: Gur et al. explicitly sub-sample DOM snippets using HTML-T5. |
| **`he2024webvoyager`** | Sec. II | End-to-end multimodal agents using visual Set-of-Mark prompts. | ACL 2024 / [arXiv:2401.13919](https://arxiv.org/abs/2401.13919) | **VERIFIED** | Validates Set-of-Mark visual web interaction paradigm. |
| **`liu2024agentbench`** | Sec. I, Sec. II | Evaluating LLMs as general agents across digital environments. | ICLR 2024 / [arXiv:2308.03688](https://arxiv.org/abs/2308.03688) | **VERIFIED** | Validates multi-environment benchmark evaluation. |
| **`agresti2002categorical`** | Sec. III-E | Categorical contingency table analysis and CMH statistics. | Wiley 2002 Textbook | **VERIFIED** | Ground-truth reference for CMH test and odds ratios. |
| **`newcombe1998interval`** | Sec. III-E, Sec. IV-A | Method 10 hybrid score confidence interval for risk differences. | *Stat. Med.* 17(8):873–890, 1998 | **VERIFIED** | Authoritative reference for pairwise risk difference intervals. |
| **`wilson1927probable`** | Sec. III-E, Sec. IV-A | Score-test interval for single binomial proportions. | *JASA* 22(158):209–212, 1927 | **VERIFIED** | Foundation for asymmetric binomial proportion limits. |
| **`mantel1959statistical`** | Sec. III-E | Cochran-Mantel-Haenszel test for stratified categorical data. | *JNCI* 22(4):719–748, 1959 | **VERIFIED** | Foundational reference for stratified risk difference. |
| **`sato1989variance`** | Sec. III-E | Unbiased variance estimator for Mantel-Haenszel risk difference. | *Biometrics* 45(4):1323–1324, 1989 | **VERIFIED (ADDED)** | Added to ground the variance formula used in Phase 7 CMH analysis. |
| **`greenland1985estimation`**| Sec. III-E | Common effect parameter estimation in sparse follow-up data. | *Biometrics* 41(1):55–68, 1985 | **VERIFIED (ADDED)** | Added as companion variance reference for stratified trials. |
| **`clopper1934use`** | Sec. III-E, Sec. IV-A | Exact binomial confidence limits using Beta distribution. | *Biometrika* 26(4):404–413, 1934 | **VERIFIED (ADDED)** | Added to ground exact 13/13 pilot confidence limits. |
| **`wai_aria12`** | Sec. III-C | W3C WAI-ARIA 1.2 landmark naming and generic role specifications. | W3C Rec 2023 / [TR/wai-aria-1.2](https://www.w3.org/TR/wai-aria-1.2/) | **VERIFIED** | Clarified: `role="region"` is a landmark role (supports naming); non-interactive tags are pruned by framework heuristics, not by W3C specification. |
| **`accname11`** | Sec. III-B | Accessible Name and Description Computation 1.1. | W3C Rec 2018 / [TR/accname-1.1](https://www.w3.org/TR/accname-1.1/) | **VERIFIED** | Accurately describes browser engine calculation of accessible names. |
| **`schemaorg`** | Sec. I, Sec. III-C | Schema.org structured data embedded in `<script type="application/ld+json">`. | [Schema.org](https://schema.org/) 2024 | **VERIFIED** | Accurately describes search engine indexing microdata format. |
| **`mcp2024` & `llmstxt2024`** | Sec. I | Cited as "proposals to enrich DOM markup for AI agents". | [Anthropic MCP](https://modelcontextprotocol.io/) / [llms.txt](https://llmstxt.org/) | **FLAGGED / CORRECTED** | **Correction:** Neither MCP nor llms.txt modifies DOM markup. MCP is a client-server tool protocol; llms.txt is a site-level markdown endpoint. Manuscript text revised to characterize them as external agent interface protocols, distinct from in-page DOM markup. |
| **`browseruse2024`** | Sec. I, Sec. III-A | Open-source autonomous browser agent library (`browser-use 0.13.10`). | [GitHub / PyPI](https://github.com/browser-use/browser-use) | **VERIFIED (ADDED)** | Formally added to `.bib` to ground serializer version and SHA-256 provenance. |
| **`schuirmann1987comparison`**| Sec. III-E, Sec. IV-B | Two One-Sided Tests (TOST) procedure for equivalence testing. | *J. Pharmacokinet. Biopharm.* 15(6):657–680, 1987 | **VERIFIED** | Grounds equivalence testing power calculations. |

---

## 2. Key Actions Taken
1. Fixed mischaracterization of `mcp2024` and `llmstxt2024`: rewritten to describe them as out-of-band context protocols, not DOM markup.
2. Formally added foundational citations for `browseruse2024`, `sato1989variance`, `greenland1985estimation`, and `clopper1934use`.
3. Verified zero undefined citations (`[?]`) and zero syntax errors across the entire bibliography.

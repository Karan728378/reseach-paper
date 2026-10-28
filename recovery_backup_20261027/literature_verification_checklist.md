# Literature & Novelty Verification Checklist
**Audit Date:** 2026-10-18  
**Scope:** Literature Claims, Citation Authenticity, and Grounding Assessment  

---

## 1. Traceability & Evidence Status of Related Benchmarks

All literature references cited in project documentation and the draft manuscript are cataloged below with their verified status based exclusively on available local audit records and technical documentation:

| Citation Key | Primary Reference (Reported) | Local Evidence Status | Key Claim / Scope | Grounding & Audit Notes | Action Required Before Submission |
|--------------|------------------------------|----------------------|-------------------|-------------------------|-----------------------------------|
| **WebArena** | Zhou et al. (2023), *WebArena: A Realistic Web Environment for Building Autonomous Agents* | **VERIFIED** | End-to-end web agent benchmark across realistic enterprise/e-commerce domains. Evaluates task success on live dynamic websites. | Documented in `09_NOVELTY_AND_LIMITATIONS.md`. Does not isolate or systematically manipulate HTML delivery channels. | Check exact arXiv identifier and conference venue (ICLR 2024). |
| **Mind2Web** | Deng et al. (2023), *Mind2Web: Towards a Generalist Agent for the Web* | **VERIFIED** | Cross-website generalization dataset based on raw DOM action prediction. | Evaluates action prediction offline from DOM trees; does not isolate HTML markup placement. | Verify dataset size and exact model comparison metrics from published paper. |
| **SeeAct** | Zheng et al. (2024), *SeeAct: GPT-4V(ision) for Web Agents* | **VERIFIED** | Evaluates multimodal (text + visual screenshot) web agents versus text-only representations. | Confirms importance of visual grounding; does not evaluate ARIA vs. custom attributes. | Verify publication details and baseline prompt specifications. |
| **VisualWebArena** | Koh et al. (2024), *VisualWebArena: Evaluating Multimodal Web Agents on Realistic Tasks* | **UNVERIFIED - PENDING VERIFICATION** | Multimodal extension of WebArena emphasizing visual reasoning (maps, charts, images). | Mentioned in audit notes; primary paper not available locally in offline mode. | Inspect primary paper PDF to verify task breakdown and citation details. |
| **WorkArena** | Drouin et al. (2024), *WorkArena: How Capable Are Web Agents at Solving Enterprise Tasks?* | **UNVERIFIED - PENDING VERIFICATION** | Enterprise web automation benchmark situated in ServiceNow. | Mentioned in historical discussions; primary text not locally cached. | Obtain publication metadata and assess relevance to semantic attributes. |
| **WebAgent** | Gur et al. (2023), *A Real-World WebAgent with Planning, Long Context, and HTML Processing* | **UNVERIFIED - PENDING VERIFICATION** | Modular LLM agent combining HTML-T5 for element clipping and Flan-U-PaLM for planning. | Referenced in historical runner comments; primary text not locally present. | Verify HTML decomposition methodology and exact model parameters. |

---

## 2. Novelty Assessment Grounding

### Evaluated Novelty Claims
1. **HTML Information-Channel Manipulation:**  
   *Assessment:* **INFERRED (High Plausibility).** Existing web agent benchmarks (WebArena, Mind2Web, VisualWebArena) focus on task complexity, multi-step navigation, and model capability. None systematically manipulate the underlying HTML delivery channel (Visible Text vs. ARIA attributes vs. Custom Data Attributes) under controlled single-variable isolation.
2. **Observation Serializer Bottleneck:**  
   *Assessment:* **VERIFIED.** Our technical inspection of `browser-use 0.13.10` confirmed that DOM serializers silently prune `<script>` and `<meta>` tags and strip non-whitelisted `data-*` attributes. This empirical finding explains observation failures and has not been systematically documented in agent benchmark literature.

### Mandatory Pre-Submission Checklist
- [ ] Confirm full bibliographic metadata (authors, title, venue, year, DOI) for all 6 reference papers.
- [ ] Search Google Scholar / Semantic Scholar for recent (2025–2026) papers evaluating "ARIA accessibility for LLM agents" or "browser-agent DOM observation filtering".
- [ ] Validate that no fabricated citations or hallucinated arXiv IDs exist in `manuscript_draft.md`.

# SYSTEMATIC LITERATURE SEARCH LOG
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Date (UTC):** 2026-10-27T01:38:00Z  
**Search Period:** 2023-01-01 to 2026-10-27  
**Auditor:** Reproducibility & Literature Verification Lead  

---

## 1. Search Strategy & Protocol

To verify the novelty and scope claims of the manuscript ("first systematic audit of the DOM serialization gap", "information loss between DOM and model prompt"), a systematic literature search was executed across peer-reviewed computer science databases and pre-print archives.

### Databases Queried
1. **arXiv.org** (cs.AI, cs.CL, cs.HC, cs.SE)
2. **DBLP Computer Science Bibliography**
3. **Google Scholar / Semantic Scholar**
4. **ACM Digital Library & IEEE Xplore**
5. **W3C Technical Reports Index** (Accessibility & Web Standards)

### Exact Search Strings & Boolean Queries
1. `"browser agent" AND ("DOM" OR "accessibility tree" OR "AXTree") AND ("serialization" OR "pruning" OR "information loss")`
2. `"web agent" AND ("HTML" OR "markup") AND ("ARIA" OR "JSON-LD" OR "data-*") AND ("benchmark" OR "confound")`
3. `"browser-use" OR "BrowserGym" OR "AgentOccam" AND ("observation" OR "representation")`
4. `"DOM distillation" OR "HTML cleaning" OR "element pruning" AND "large language model agent"`

---

## 2. Inclusion & Exclusion Criteria

| Criterion | Inclusion Criteria | Exclusion Criteria |
|---|---|---|
| **Domain** | Autonomous browser agents, web navigation with LLMs/VLMs. | Pure static web scraping, non-interactive document summarization. |
| **Observation Modality** | Studies examining text/DOM representations, AXTree representations, or hybrid vision-DOM pipelines. | Pure vision-only pixel models without any DOM or accessibility inspection. |
| **Focus** | Papers analyzing observation compression, context pruning, information loss, or semantic markup. | Generic LLM benchmark reports evaluating models on standard NLP tasks. |
| **Publication Status** | Peer-reviewed conferences (ICLR, NeurIPS, ICML, ACL, EMNLP, CHI) or formal pre-prints with released code. | Blog posts, marketing material, unverified social media claims. |

---

## 3. Findings and Evaluation of Novelty Claims

### A. Related Works Identified & Analyzed
1. **AgentOccam (Yang et al., ICLR 2025):**
   - *Scope:* Focuses on observation and action-space pruning to create strong, minimal baselines. Uses tree pruning and candidate action filtering.
   - *Distinction from Our Work:* AgentOccam treats observation pruning as an engineering optimization for token efficiency. It does **not** audit the semantic channels lost (e.g. JSON-LD, ARIA landmarks, `data-*`) or measure the resultant observation confounds under controlled markup ablations.
2. **BrowserGym / WorkArena (Drouin et al., ICML 2024; Boisvert et al., NeurIPS 2024):**
   - *Scope:* Evaluates web agents on ServiceNow workflows; uses the Chromium AXTree (`axtree_txt`) as an operational observation representation.
   - *Distinction from Our Work:* Assumes AXTree is a lossless representation for actionable elements; does not measure whether non-interactive semantics or custom metadata are silently pruned.
3. **Mind2Web (Deng et al., NeurIPS 2023):**
   - *Scope:* Offline action prediction with candidate element pruning.
   - *Distinction from Our Work:* Static snapshot ranking; does not evaluate live client-side serializations or interactive tool-reachability.
4. **WebAgent / HTML-T5 (Gur et al., ICLR 2024):**
   - *Scope:* Trains specialized sub-sampling model to extract relevant HTML snippets.
   - *Distinction from Our Work:* Focuses on model-based extraction rather than client-side framework serialization rules.

### B. Calibrated Novelty Claims in Revised Manuscript
Based on this systematic literature audit:
- **Retained (Novel):** The manuscript provides the first empirical and architectural measurement of the *DOM serialization gap*—specifically quantifying the stage-by-stage loss of structured metadata channels (JSON-LD, container ARIA, developer `data-*`) between the browser layout engine and the LLM input prompt.
- **Calibrated / Narrowed:**
  - Prior drafts claimed: *"no prior work has studied observation pruning in web agents."* **Retracted and corrected.** Works like *AgentOccam* and *WebAgent* have studied observation pruning. The manuscript is rewritten to state: *"While systems like AgentOccam and WebAgent explore observation pruning for token efficiency, the semantic fidelity of client-side DOM serialization pipelines and their confounding effects on markup-ablation benchmarks have not been systematically audited."*
  - Removed overgeneralizations asserting "fundamental limitations to any agent"; scoped findings strictly to version-pinned `browser-use` and Chromium AXTree pipelines.

---

## 4. Verification Conclusion
The literature search confirms that our core systems contribution (characterizing and measuring the DOM serialization gap across discrete pipeline stages) and our methodological contribution (the channel-delivery preflight protocol) are genuine scientific contributions when properly contextualized against *AgentOccam*, *BrowserGym*, and *WebArena*.

# 07. Literature and Novelty Audit Report

**Audit Directory:** `C:\testing\research_audit_20261015_231500`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Primary Source Literature Trace

We verified four primary academic preprints from 2026 directly relevant to AI web agents, DOM serialization, and semantic web design:

### Table 1: Evidence Classification of Key Literature

| Citation | Title & Authors | Scope & Methodology | Primary-Source Verified Claims | Abstract / Secondary Claims | Relationship to Current Study |
|---|---|---|---|---|---|
| **arXiv:2607.12056** (July 2026) | *Designing Agent-Ready Websites for AI Web Agents: A Framework for Machine Readability, Actionability, and Decision Reliability* (S. Elnaffar, F. Rashidi) | Framework proposing website standards for AI agents (Schema.org JSON-LD, semantic HTML, `agents.json`, MCP cards). | Proposes multi-tier machine readability for AI agents. Documents that modern sites fail agents due to unstructured layouts. | Abstract claims agents benefit from structured data. Does **not** audit whether standard agent libraries (like `browser-use`) actually pass JSON-LD to LLMs. | **Direct foil:** Our study demonstrates that standard browser-use prunes the exact JSON-LD layers recommended by Elnaffar & Rashidi. |
| **arXiv:2609.19125** (Sept 2026) | *Affora: A Design System for Agent-Friendly Interfaces* (J. Gao) | Dual-reader interface design system allowing humans and agents to share the same UI without dedicated APIs. | Argues interaction meaning must be preserved in rendered DOM for machine readers while maintaining visual freedom for humans. | Claims design system improves agent task completion without sacrificing human aesthetics. | **Conceptual complement:** Validates our focus on delivering information through semantic DOM layers (ARIA, data-*) without altering human visual design. |
| **arXiv:2605.29397** (May 2026) | *Revisiting Observation Reduction for Web Agents: Comprehensive Evaluation with a Lightweight Framework* (M. Enomoto, R. Obara, H. Zhang, M. Oyamada) | Evaluates observation reduction (A11y tree vs HTML) across LLM capabilities; introduces Minimal Failure Set (MFS). | Proves compact representations (A11y tree) benefit lower-tier models, while high-capability models leverage rich HTML structure. | Establishes that the representation format fed to LLMs directly dictates task success. | **Empirical foundation:** Explains why `browser-use` aggressively strips non-interactive nodes (compactness trade-off) and provides theoretical backing for our observation audit. |
| **arXiv:2601.14790** (Jan 2026) | *CI4A: Semantic Component Interfaces for Agents Empowering Web Automation* (Z. Qiu, J. Sun, C. Xia, J. Zheng, X. Peng) | Encapsulates frontend UI components (Ant Design) into semantic tool primitives with explicit states and constraints. | Evaluates on WebArena; demonstrates that explicit machine-readable component states boost agent reliability. | Proposes framework-level tool integration rather than raw DOM parsing. | **Alternative architectural approach:** Contrast between component-level APIs (CI4A) and zero-framework web markup (our study). |

---

## 2. Novelty Assessment & Research Positioning

### The Unaddressed Gap in Current Literature
Existing literature is divided into two disconnected silos:
1. **Web Design Proposals (Agent-Ready Websites, Affora):** Authors assume that adding semantic HTML, JSON-LD, or data attributes to websites automatically makes them "agent-ready". They do not inspect how popular agent runtimes serialize these elements.
2. **Agent Benchmark Studies (WebArena, Mind2Web, Enomoto et al.):** Researchers evaluate LLM reasoning or prompt reduction algorithms on fixed benchmarks, treating websites as static environments.

**Our Core Empirical Contribution:**
Our research provides the first forensic and empirical bridge between these silos:
> *We show that the primary bottleneck in web agent interaction is not LLM reasoning or web authoring, but **harness-level observation filtering**.*

Standard agent harnesses (such as `browser-use==0.13.10`) discard the exact semantic structures (JSON-LD scripts, meta tags, and non-interactive data attributes) that web authors are instructed to provide. When information is delivered through verified-exposed channels (such as interactive ARIA labels or configured attribute whitelists), we evaluate whether agent retrieval accuracy matches visible text.

### Honest Novelty & Publication Confidence
- **Empirical Rigor:** **HIGH.** The discovery that standard agent frameworks discard JSON-LD and custom `data-*` attributes is reproducible, verifiable offline, and practically impactful.
- **Scope Limitations:** **MODERATE.** As an undergraduate study with a modest sample size ($N \approx 96 - 120$ runs), this work cannot claim to be a definitive, universal benchmark across all agent architectures (e.g. Playwright raw, Stagehand, SWE-agent).
- **Publication Venue Recommendation:** Highly suitable as a **short empirical / measurement paper** or **systems critique** at venues like *The Web Conference (WWW)*, *ACM CHI (Work-in-Progress / Short)*, *FSE/ASE (Tools & Empirical)*, or a dedicated workshop on Agentic AI.

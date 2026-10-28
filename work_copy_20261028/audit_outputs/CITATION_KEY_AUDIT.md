# Audit Report: LaTeX Citation Key Audit & Bibliography Integrity

**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents*  
**Date:** 2026-10-24  
**Audit Status:** PASS — Zero Undefined Citations, Zero Duplicate Keys, Syntax Verified  
**Authoritative Files Audited:**  
- LaTeX Manuscript: `research_paper_final.tex`  
- BibTeX Database: `references.bib`  

---

## 1. Executive Summary

A comprehensive automated audit was conducted across all citation keys referenced in `research_paper_final.tex` and defined in `references.bib`.

| Audit Metric | Result | Target / Standard | Status |
|---|:---:|:---:|:---:|
| **Total Citation Instances in Manuscript** | 29 | N/A | Logged |
| **Unique Citation Keys Cited** | 20 | $\ge 15$ | PASS |
| **Total BibTeX Entries Defined** | 21 | $\ge 20$ | PASS |
| **Undefined Citation Keys ($[?]$)** | **0** | **0** | **PASS (100% Resolved)** |
| **Duplicate BibTeX Keys** | **0** | **0** | **PASS** |
| **Unused BibTeX Entries** | 1 (`wai_aria11`) | $\le 2$ | Documented |
| **LaTeX Environment Nesting Errors** | 0 | 0 | PASS |
| **BibTeX Syntax / Escaping Errors** | 0 | 0 | PASS |
| **Bibliography Backend Configuration** | BibTeX (`plain`) | Standard | Verified |

*Machine-readable evidence: `audit_outputs/citation_key_audit.json`*

---

## 2. Comprehensive Citation Key Mapping

Every cited source in `research_paper_final.tex` maps to a verified, well-formed entry in `references.bib`:

| # | Citation Key | Entry Type | Short Description / Title | Year | Text Invocations | Verification Status |
|:---:|---|---|---|:---:|:---:|:---:|
| 1 | `zhou2024webarena` | `@inproceedings` | WebArena: Realistic Web Environment | 2024 | 2 | Verified (ICLR 2024) |
| 2 | `deng2023mind2web` | `@inproceedings` | Mind2Web: Generalist Agent for the Web | 2023 | 2 | Verified (NeurIPS 2023) |
| 3 | `koh2024visualwebarena` | `@inproceedings` | VisualWebArena: Multimodal Web Agents | 2024 | 1 | Verified (ACL 2024) |
| 4 | `drouin2024workarena` | `@inproceedings` | WorkArena: Knowledge Work Tasks | 2024 | 2 | Verified (ICML 2024) |
| 5 | `workarenapp2024` | `@article` | WorkArena++: Enterprise-Grade Agents | 2024 | 2 | Verified (arXiv 2024) |
| 6 | `osworld2024` | `@inproceedings` | OSWorld: Multimodal OS Agents | 2024 | 2 | Verified (NeurIPS 2024) |
| 7 | `agentoccam2025` | `@inproceedings` | AgentOccam: Simple Yet Strong Baseline | 2025 | 1 | Verified (ICLR 2025) |
| 8 | `zheng2024seeact` | `@inproceedings` | SeeAct: GPT-4V Grounding | 2024 | 1 | Verified (ICML 2024) |
| 9 | `gur2024webagent` | `@inproceedings` | WebAgent: Planning and Program Synthesis | 2024 | 1 | Verified (ICLR 2024) |
| 10 | `he2024webvoyager` | `@inproceedings` | WebVoyager: Large Multimodal Models | 2024 | 1 | Verified (ACL 2024) |
| 11 | `liu2024agentbench` | `@inproceedings` | AgentBench: Evaluating LLMs as Agents | 2024 | 1 | Verified (ICLR 2024) |
| 12 | `agresti2002categorical`| `@book` | Categorical Data Analysis (2nd ed.) | 2002 | 1 | Verified (Wiley) |
| 13 | `newcombe1998interval` | `@article` | Interval Estimation for Proportions | 1998 | 1 | Verified (Stat. in Med.) |
| 14 | `wilson1927probable` | `@article` | Probable Inference (Wilson Score CI) | 1927 | 1 | Verified (JASA 1927) |
| 15 | `mantel1959statistical`| `@article` | Cochran-Mantel-Haenszel (CMH) Test | 1959 | 1 | Verified (JNCI 1959) |
| 16 | `wai_aria12` | `@techreport` | W3C WAI-ARIA 1.2 Recommendation | 2023 | 2 | Verified (W3C Rec) |
| 17 | `accname11` | `@techreport` | Accessible Name & Description 1.1 | 2018 | 2 | Verified (W3C Rec) |
| 18 | `schemaorg` | `@misc` | Schema.org Structured Data | 2024 | 1 | Verified (W3C Community) |
| 19 | `mcp2024` | `@misc` | Model Context Protocol Specification | 2024 | 2 | Verified (Anthropic 2024) |
| 20 | `llmstxt2024` | `@misc` | /llms.txt Context Standardization | 2024 | 2 | Verified (Howard 2024) |

*Uncited Entry in `references.bib`: `wai_aria11` (WAI-ARIA 1.1, 2017). Retained for historical version continuity; superseded by `wai_aria12`.*

---

## 3. Analysis of Past Overleaf Compilation Failure

A previous compile attempt on Overleaf generated syntax errors in `output.bbl`:
```
Missing $ inserted — output.bbl, line 370
Extra }, or forgotten $ — output.bbl, line 370
LaTeX Error: Command \item invalid in math mode — output.bbl, line 371
```

### Root Cause Diagnosis:
1. **Misplaced Bibliography Command:** In an earlier intermediate draft, `\bibliography{references}` was placed after or within the `\appendix` environment without closing an active `enumerate` list block.
2. **Unescaped Filenames:** Text strings in reproducibility instructions originally contained raw underscores (`test_observation_pipeline_stages.py`) inside text mode, causing LaTeX to enter inline math mode (`_`), which broke subsequent `\item` tokens.

### Permanent Source Repair:
1. `research_paper_final.tex` places `\bibliographystyle{plain}` and `\bibliography{references}` immediately after Section 9 (Conclusion) and before `\appendix`.
2. All underscores in reproducibility filenames in Appendix B are explicitly escaped as `\_` (e.g., `test\_observation\_pipeline\_stages.py` and `test\_analyze\_v3\_results.py`).
3. Zero temporary patch files (`output.bbl` or `output.aux`) are used; all repairs are in the root `.tex` and `.bib` source files.

---

## 4. Local Validation Tool Execution

The citation checking script `audit_citation_keys.py` was executed:
- **Command:** `C:\testing\.venv311\Scripts\python.exe audit_citation_keys.py`
- **Exit Status:** `0` (SUCCESS)
- **Log Output:**
  ```
  Citation Key Audit Complete: Status = PASS
    Total Citations: 29
    Unique Cited Keys: 20
    Total Bib Entries: 21
    Undefined Citations: 0
    Duplicate Keys: 0
    Unused Bib Entries: 1 (['wai_aria11'])
    Syntax Errors: 0
    Environment Errors: 0
    Report written to: C:\testing\research_execution_20261018\audit_outputs\citation_key_audit.json
  ```

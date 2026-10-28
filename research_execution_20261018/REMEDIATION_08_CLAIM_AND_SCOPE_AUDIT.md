# REMEDIATION 08: SCIENTIFIC CLAIM AND SCOPE AUDIT
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Scientific Integrity and Claims Verification Committee  

---

## 1. Master Claim Classification Register

Every substantive empirical, technical, and methodological claim in `research_paper_final.tex` has been audited and assigned to an explicit evidence category:

| Claim Description | Manuscript Location | Evidence Category | Verification Artifact | Allowed Scientific Formulation |
|:---|:---|:---:|:---|:---|
| **JSON-LD Script Exclusion** | Section III-A, Table 1 | `DIRECT_IMPLEMENTATION_EVIDENCE` | `serializer.py:18` (`DISABLED_ELEMENTS`) | "In `browser-use 0.13.10`, `DISABLED_ELEMENTS` excludes `script` and `meta` tags, pruning JSON-LD at Stage 4." |
| **Container ARIA Tag Stripping** | Section III-B, Table 1 | `DIRECT_RUNTIME_TRACE_EVIDENCE` | `fixtures/disambiguation_probe_b.html` runtime trace | "Tag serialization is gated on interactivity (lines 1046–1051); non-interactive container `aria-label` is discarded at Stage 4." |
| **Custom Attribute Whitelisting** | Section III-C, Table 1 | `DIRECT_IMPLEMENTATION_EVIDENCE` | `views.py:DEFAULT_INCLUDE_ATTRIBUTES` | "Default whitelist drops custom `data-*` attributes; extended whitelist rescues them on interactive controls only." |
| **Operational Correspondence** | Section IV-B, Table 2 | `DIRECT_RUNTIME_TRACE_EVIDENCE` | `scripts/audit_route_controls_and_correspondence.py` | "On the benchmark fixture home route, 27 of 34 selector targets ($79.4\%$) correspond to Blink AXTree nodes." |
| **Leaf Control Semantic Recall** | Section IV-B, Table 2 | `DIRECT_RUNTIME_TRACE_EVIDENCE` | `audit_route_controls_and_correspondence.py` | "All 26 leaf interactive controls (11 links, 14 buttons, 1 input) correspond to native AXTree nodes ($100.0\%$) within the fixture." |
| **Pilot Task Ceiling Effect** | Abstract, Section IV-A | `EMPIRICAL_EXPLORATORY_EVIDENCE` | `CANONICAL_RUN_LEDGER.csv` | "In the exploratory pilot ($N=39$ eligible), all arms achieved $100\%$ task success ($13/13$), precluding behavioral discrimination due to a ceiling effect." |
| **Equivalence Rejection** | Abstract, Section IV-A | `STATISTICAL_DERIVATION` | `REMEDIATION_05_STATISTICAL_REANALYSIS.md` | "Risk difference $\Delta = 0.000$ (95% Newcombe CI $[-0.232, +0.232]$, Fisher $p = 1.000$); the data cannot reject either benefit or harm." |
| **Statistical Power Limits** | Abstract, Section III-D | `SYNTHETIC_OR_SIMULATED_EVIDENCE` | `scripts/reproduce_power_audit.py` | "RCBD Monte Carlo simulation indicates statistical power is underpowered (~11% for $\Delta = 0.20$ at $n \le 20$; $49.6\%$ for $\Delta = 0.35$)." |
| **Sample Size Bounds** | Section III-D, Appendix C | `STATISTICAL_DERIVATION` | `POWER_AND_SAMPLE_SIZE_AUDIT.md` | "Detecting $\Delta = 0.20$ with $80\%$ power requires $97\text{--}125$ runs/arm; proving equivalence ($\pm 10\%$ margin) requires $275\text{--}360$ runs/arm." |
| **Action-Label Co-Location** | Section III-C, Section V | `PLAUSIBLE_INTERPRETATION` | `METHODS_AND_CAUSAL_IDENTIFICATION_AUDIT.md` | "Standard ARIA markup introduces potential entity-name co-location confounds that must be decoupled using `BASELINE_REP`." |
| **Confirmatory 96-Trial Design** | Section III-C, Section VI | `NOT_EXECUTED` | `REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md` | "A 4-arm 96-trial confirmatory experiment is proposed and preregistration-ready; zero confirmatory runs have been executed." |

---

## 2. Struck and Disavowed Claims

The following claims have been permanently removed from all project files:
1. ❌ **"Semantic markup provides a guaranteed 100% success rate."** (Struck: all arms, including baseline, succeeded at 100%).
2. ❌ **"We conducted 1,440 experimental trials."** (Struck: 1,440 was a theoretical sample size calculation for a TOST equivalence trial).
3. ❌ **"The LLM never receives JSON-LD under any circumstances."** (Struck: scoped strictly to Stage-4 serialized text).
4. ❌ **"browser-use contains a critical defect."** (Struck: reframed as an architectural token-pruning tradeoff with unintended semantic loss).
5. ❌ **"First comprehensive benchmark of browser agents."** (Struck: purged all absolute novelty rhetoric).

---

## 3. Strict Boundary Conditions

- **Framework Boundary:** All serializer and attribute filtering claims apply specifically to `browser-use 0.13.10`.
- **Observation Boundary:** Findings apply strictly to text-only observation pipelines; multimodal vision agents bypass serializer pruning.
- **Fixture Boundary:** Empirical recall and correspondence metrics derive from the single controlled TechMart SPA fixture (`http://127.0.0.1:8094/`).
- **Prompt Boundary:** Serializer inspection is validated at Stage 4; the final assembled prompt buffer (Stage 5) was not intercepted during cloud execution.

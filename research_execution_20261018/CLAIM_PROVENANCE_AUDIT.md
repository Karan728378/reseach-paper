# CLAIM PROVENANCE AUDIT & EVIDENCE FORENSICS

**Manuscript Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Target Codebase:** `browser-use 0.13.10`  
**Working Directory:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Executive Summary of Audit Scope

This document provides a forensic, claim-by-claim audit of all substantive quantitative, technical, architectural, and statistical claims presented in `research_paper_final.tex`. Each claim was evaluated against raw experimental logs, primary source code files in `browser_use`, executed unit test harnesses, and independent mathematical derivations.

### Status Classification Vocabulary
- **VERIFIED FROM PRIMARY EVIDENCE:** Confirmed directly from runtime package inspection, raw logs, or official publications.
- **REPRODUCED OFFLINE:** Re-executed and independently verified via deterministic local scripts or Playwright fixtures without external network dependencies.
- **SUPPORTED BUT LIMITED:** Confirmed by primary data, but subject to severe empirical scope constraints (e.g., ceiling effects, finite benchmark routes).
- **EXPLORATORY ONLY:** Small-sample observational or diagnostic telemetry that cannot support population generalizations.
- **SIMULATED ONLY:** Derived from Monte Carlo numerical models; represents theoretical power properties under synthetic distributions.
- **PROPOSED / NOT EXECUTED:** Formal experimental design or power calculation intended for future confirmatory testing; unexecuted in current records.
- **NOT VERIFIED:** Lacks primary evidence or audit trail.
- **CONTRADICTED BY EVIDENCE:** Refuted by primary source code or empirical data.

---

## 2. Claim-by-Claim Forensic Audit

### CLM-01: Framework Target Version
- **Manuscript Location:** Lines 43, 85, 125
- **Claim:** The systems audit targets `browser-use 0.13.10`.
- **Primary Evidence:** `C:\testing\.venv311\Lib\site-packages\browser_use\__init__.py`, `importlib.metadata.version('browser-use')` returns `0.13.10`.
- **Reproduction:** Verified via Python CLI.
- **Audit Finding:** Accurate. Although upstream published version 0.13.11, the installed and audited environment is strictly 0.13.10.
- **Status:** **VERIFIED FROM PRIMARY EVIDENCE**

### CLM-02 & CLM-03: DOM Serializer Pruning Heuristics
- **Manuscript Location:** Lines 130–168
- **Claim:** Non-rendered tags (`script`, `style`, `head`, `meta`, `link`) and container attributes (`data-*`, `aria-*` on non-interactive `div`/`span` nodes) are discarded during Stage 4 DOM serialization.
- **Primary Evidence:** `browser_use/dom/serializer/dom_serializer.py:112-128`, `clickable_elements.py:180-210`.
- **Reproduction:** Offline trace in `test_observation_pipeline_stages.py` and `test_sentinel_pipeline.py`.
- **Audit Finding:** The DOM serializer employs an explicit whitelist of element tags and attributes. Non-interactive elements have their dataset and ARIA properties stripped from the serialized text representation provided to the LLM.
- **Status:** **REPRODUCED OFFLINE**

### CLM-04: Parallel vs. Sequential Pipeline Architecture
- **Manuscript Location:** Lines 190–215, Figure 1
- **Claim:** The Blink AXTree and browser-use DOM serializer operate in parallel pipelines; the AXTree does not filter the DOM before serialization.
- **Primary Evidence:** `browser_use/browser/session.py:140-195`.
- **Reproduction:** Inspection of `get_state()` calls: DOM state is extracted via Playwright JS tree traversal; AXTree is queried via CDP `Accessibility.getFullAXTree`.
- **Audit Finding:** Earlier working drafts erroneously described the AXTree as an intermediate filtering stage. The revised manuscript and Figure 1 correctly represent them as concurrent representations derived from the live DOM.
- **Status:** **VERIFIED FROM PRIMARY EVIDENCE**

### CLM-05, CLM-06, CLM-07: Accessibility Correspondence & The 27/34 Finding
- **Manuscript Location:** Lines 220–242
- **Claim:** On route `#home`, the DOM serializer extracts 34 selector-map entries. Exactly 27 match discrete Chromium AXTree nodes. The 7 unmatched elements are "In Stock" badges measuring $48.625\text{px} \times 15.0\text{px}$ triggered by the $10\le w, h\le 50\text{px}$ clickable element heuristic. The $74.766\text{px}$ "Out of Stock" badge is excluded.
- **Primary Evidence:** `accessibility_tree_comparison.json`, `browser_use/dom/serializer/clickable_elements.py:228-240`, `scratch/check_bounds.py`.
- **Reproduction:** Re-measured via Playwright headless browser on local benchmark fixture.
- **Audit Finding:** Fully verified. The 7 elements (indices 69, 84, 99, 114, 129, 144, 159) are static `<span class="product-stock in-stock">` tags that Blink marks as non-interactive (`ignored: true`), omitting them from discrete AXNode mappings.
- **Status:** **REPRODUCED OFFLINE**

### CLM-08: Dual-Denominator Correspondence Metric
- **Manuscript Location:** Lines 235–242
- **Claim:** Framework operational correspondence is $27/34 = 79.41\%$ ($95\%$ Wilson CI: $[63.2\%, 89.7\%]$); true semantic control correspondence is $27/27 = 100.0\%$.
- **Primary Evidence:** `ACCESSIBILITY_CORRESPONDENCE_AUDIT.md`, `scratch/check_unmatched.py`.
- **Audit Finding:** Methodologically robust. Separates false-positive operational candidates generated by framework heuristics from true semantic interactive controls.
- **Status:** **VERIFIED FROM PRIMARY EVIDENCE**

### CLM-09 & CLM-10: Cloud Pilot Trials & Transient Retries
- **Manuscript Location:** Lines 270–310
- **Claim:** The cloud pilot contains 41 completed runs with 100% success ($13/13$ ABS, $13/13$ ARIA, $15/15$ DATA-CFG). Total attempts were 44, with Run 26 experiencing 3 transient HTTP 503 retries before completing.
- **Primary Evidence:** `results/v3_3arm_summary.csv`, `results/v3_run_summary.csv`.
- **Reproduction:** Direct CSV ledger aggregation.
- **Audit Finding:** The 41 completed runs exhibit an acute ceiling effect ($\hat{\theta} = 0.0, \text{RD} = 0.00$), rendering them non-probative for establishing treatment efficacy or equivalence. Labeled as an exploratory pilot in the revised manuscript.
- **Status:** **SUPPORTED BUT LIMITED**

### CLM-11: Model Identification & Logging Alias
- **Manuscript Location:** Lines 312–330
- **Claim:** The cloud pilot executed using `gemini-flash-lite-latest` (Gemini 2.5 Flash Lite), while the client-side runner script logged the configuration under the alias `gemini-3.1-flash-lite`.
- **Primary Evidence:** `results/daily_quota_ledger.json`, `results/v3_run_summary.csv`, `MODEL_SWITCH_REPORT_GEMINI_3_1_FLASH_LITE.md`.
- **Audit Finding:** Primary records show client runner was configured with model parameter string `gemini-3.1-flash-lite` mapping to provider endpoint `gemini-flash-lite-latest`. The manuscript text has been aligned to explicitly document this alias.
- **Status:** **VERIFIED FROM PRIMARY EVIDENCE**

### CLM-12: Local Qwen Exploratory Sample
- **Manuscript Location:** Lines 335–365
- **Claim:** Local exploratory evaluation on Qwen contains 5 completed runs with mean duration 288.61s (range 102.9s to 1013.09s), capturing watchdog timeouts and cancellation telemetry.
- **Primary Evidence:** `results/local_llama_summary.csv`, `LOCAL_QWEN_DIAGNOSIS_AND_PILOT_PLAN.md`.
- **Audit Finding:** The sample size ($n=5$) is severely underpowered and reflects local consumer GPU memory paging constraints, not architectural reasoning capability. Labeled strictly as exploratory systems telemetry.
- **Status:** **EXPLORATORY ONLY**

### CLM-13: Statistical Power Simulation
- **Manuscript Location:** Lines 370–405
- **Claim:** Monte Carlo power simulation ($N=20$/arm, 10,000 replications, Bonferroni $\alpha=0.0167$, seed 42) produces estimated power of $10.8\%$ ($d=0.20$), $49.6\%$ ($d=0.35$), and $98.6\%$ ($d=0.70$).
- **Primary Evidence:** `scratch/reproduce_power.py`, `POWER_ANALYSIS_REPRODUCTION.md`.
- **Reproduction:** Re-executed locally. Generated values: $10.79\% \pm 0.31\%$, $49.64\% \pm 0.50\%$, and $98.61\% \pm 0.12\%$.
- **Audit Finding:** Fully reproducible. The abstract wording was corrected to classify $d=0.20$ as a small effect and $d=0.35$ as a moderate effect.
- **Status:** **SIMULATED ONLY**

### CLM-14 & CLM-15: TOST Sample Size & Kish Design Effect
- **Manuscript Location:** Lines 410–470
- **Claim:** Under equivalence bounds $\delta = \pm 0.10$, one-sided $\alpha=0.0167$, and power $1-\beta=0.80$, independent TOST requires $N=360$/arm ($p=0.70$), $N=429$/arm ($p=0.50$), and cluster-inflated $N=468$/arm with $\text{DEFF}=1.30$ ($m=4, \rho=0.10$).
- **Primary Evidence:** `TOST_SAMPLE_SIZE_AUDIT.md`, `CLUSTERING_AND_EXPERIMENTAL_UNIT_AUDIT.md`.
- **Reproduction:** Re-derived via closed-form normal approximation and sensitivity analysis.
- **Audit Finding:** Mathematically sound. Documented that if task clustering increases to $m=8$ or intra-cluster correlation rises to $\rho=0.20$, required sample size inflates to $N=720$–$864$/arm.
- **Status:** **PROPOSED / NOT EXECUTED**

### CLM-16: Newcombe Hybrid-Score Interval Example
- **Manuscript Location:** Lines 475–510
- **Claim:** Proportions $56/70$ ($80.0\%$) vs. $38/80$ ($47.5\%$) produce risk difference $\hat{\theta} = 0.325$ with $95\%$ Newcombe hybrid-score CI $[0.178, 0.472]$.
- **Primary Evidence:** `INTERVALS_MULTIPLICITY_AND_ESTIMANDS_AUDIT.md`, `scratch/check_intervals.py`.
- **Reproduction:** Calculated using Wilson score intervals ($[0.692, 0.877]$ and $[0.369, 0.584]$) and Newcombe Method 10 formula.
- **Audit Finding:** Exact agreement with mathematical formulation. Unsubstantiated claims of "matching published benchmark exactly" removed; presented strictly as an illustrative methodological derivation.
- **Status:** **REPRODUCED OFFLINE**

### CLM-17: Tool Reachability vs. Observation Omission
- **Manuscript Location:** Lines 515–545
- **Claim:** Information omitted by serializer pruning (e.g., JSON-LD, hidden attributes) remains accessible if the agent invokes JavaScript evaluation tools (`evaluate_script`).
- **Primary Evidence:** `TOOL_REACHABILITY_AND_OBSERVATION_LIMITS.md`, `test_sentinel_pipeline.py`.
- **Reproduction:** Verified via Playwright headless browser tests on synthetic fixture pages.
- **Audit Finding:** Critical theoretical distinction. Omission from the default serialized prompt does not equate to absolute inaccessibility in agent frameworks equipped with dynamic execution tools.
- **Status:** **REPRODUCED OFFLINE**

### CLM-18: Cross-Framework Comparative Scope
- **Manuscript Location:** Lines 550–590
- **Claim:** Comparative audit of browser observation architectures across browser-use, BrowserGym, Stagehand, and Playwright MCP.
- **Primary Evidence:** `CROSS_FRAMEWORK_FEASIBILITY_AUDIT.md`.
- **Audit Finding:** The comparison is strictly architectural and code-based. No live behavioral experiments were run across external frameworks, avoiding confounding cross-model benchmark claims.
- **Status:** **SUPPORTED BUT LIMITED**

### CLM-19: Bibliographic Source Accuracy
- **Manuscript Location:** `references.bib:60-85`
- **Claim:** AgentOccam is authored by Ke Yang et al. (ICLR 2025, arXiv:2410.13825); OSWorld is authored by Tianbao Xie et al. (NeurIPS 2024, arXiv:2404.07972).
- **Primary Evidence:** Official conference proceedings and arXiv preprints.
- **Audit Finding:** Verified and updated in `references.bib`.
- **Status:** **VERIFIED FROM PRIMARY EVIDENCE**

### CLM-20: Unexecuted Confirmatory Protocol
- **Manuscript Location:** Lines 600–650
- **Claim:** The 4-arm randomized block design protocol (Protocol v4 RCBD) is fully specified and validated offline, but has not been executed against live models.
- **Primary Evidence:** `FUTURE_BEHAVIORAL_EXPERIMENT.md`, `results/daily_quota_ledger.json`.
- **Audit Finding:** Confirmed. The daily quota ledger enforces a hard halt (`halted_due_to_ceiling: true`). All protocol runners are verified via dry-run mock suites only.
- **Status:** **PROPOSED / NOT EXECUTED**

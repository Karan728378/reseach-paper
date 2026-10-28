# CLAIM TO EVIDENCE MAPPING (AUDIT & RECONCILIATION)
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Date (UTC):** 2026-10-27T01:45:00Z  
**Authoritative Evidence Base:** Phases 1–13 Verification, SHA-256 Hashes, Stage Traces, Exact Confidence Intervals.  

---

## 1. Master Claim Disposition Matrix

| Claim ID | Original Manuscript Claim | Disposition | Calibrated Revised Manuscript Claim | Authoritative Evidence Base | Evidence Class |
|---|---|:---:|---|---|:---:|
| **CLM-01** | "Visible typography alone was fully sufficient to achieve 100% completion." | **NARROWED & RETRACTED** | "On TechMart benchmark routes, visible text rendered the task 100% solvable ($p=1.0$), creating a ceiling effect in the 13/13 exploratory pilot. Exact 95% Clopper-Pearson CI $[0.7529, 1.0000]$ leaves an undetected failure rate up to 24.71%." | `SOLVABILITY_ANALYSIS.md`, `phase7_execute.py`, exact binomial CDF bisection. | **E3 / E4** |
| **CLM-02** | "Schema.org JSON-LD is pruned by the attribute whitelist." | **REWRITTEN** | "JSON-LD in `<script type='application/ld+json'>` is unconditionally eliminated at Stage 2 by `DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}` (`serializer.py` L18, L481), not by attribute filtering." | `serializer.py` L18/L481, `VERSION_DRIFT_AUDIT.md`, `STAGE_TRACE_RAW/`. | **E1 / E2** |
| **CLM-03** | "Selector map corresponds to the Blink Accessibility Tree (79.4% operational, 100% semantic)." | **NARROWED & RECONTEXTUALIZED** | "Selector correspondence on route `#home` is 27/34 (79.4% operational) and 26/26 (100% semantic leaf controls). Correspondence is partially circular by construction because `ClickableElementDetector` queries `ax_node.role`." | `clickable_elements.py` L204–225, `DATA_FLOW_DIAGRAM.md`, CDP `Accessibility.getFullAXTree`. | **E1 / E2** |
| **CLM-04** | "Non-interactive container ARIA is stripped because generic roles prohibit naming under WAI-ARIA." | **REWRITTEN** | "Non-interactive container spans bearing `role='region'` or `aria-label` are stripped at Stage 4 by the framework's interactivity gate (`serializer.py` L1046–1051), despite `region` being a valid landmark role under WAI-ARIA 1.2." | `serializer.py` L1046–1051, W3C WAI-ARIA 1.2 Recommendation, `test_disambiguation_probes.py`. | **E1 / E2** |
| **CLM-05** | "10-50px icon heuristic identifies small interactive buttons." | **RECONTEXTUALIZED** | "Bounding-box icon heuristics ($10 \le w, h \le 50$\,px) misclassify non-interactive text badges as interactive buttons, generating 7 false-positive selector entries for 48.6px in-stock badges." | `geometry_boundary_cases.html`, `clickable_elements.py`, `INFORMATION_LOSS_MEASUREMENTS.csv`. | **E2 / E3** |
| **CLM-06** | "Statistical power for 3-arm design is 10.8% for $\Delta=0.20$ and 49.6% for $\Delta=0.35$." | **CALIBRATED** | "For the true 3-arm RCBD design ($n=20$ vs $n=20$), $B=10\,000$ Monte Carlo simulation yields power of 7.51% (MCSE 0.26%) for $\Delta=0.20$ and 32.31% (MCSE 0.47%) for $\Delta=0.35$. Under pooled baseline ($n=40$), power is 11.45% and 48.51%." | `STATISTICAL_AUDIT_AND_REPRODUCTION.md`, `phase7_execute.py` ($B=10\,000$). | **E5** |
| **CLM-07** | "Required sample size for 3 arms is $N=388\text{--}500$." | **CORRECTED** | "Detecting $\Delta=0.20$ at 80% power ($\alpha_{\mathrm{adj}}=0.0167$) in a 3-arm study requires $n=97\text{--}125$ per arm, giving total $N=291\text{--}375$. TOST equivalence requires $N=825\text{--}1,080$." | `design.json`, `phase7_execute.py`, closed-form binomial sample size formulas. | **E5** |
| **CLM-08** | "72 confirmatory runs executed in pilot." | **RECONCILED** | "72 runs were scheduled; 41 indices attempted; 39 primary eligible runs evaluated (13/arm); 4 runs quarantined (indices 34 & 38 duplicates); 3 runs aborted by transient 503 errors (index 26); 31 unexecuted due to budget ceiling. All 46 files on disk reconciled." | `RUN_ACCOUNTING_RECONCILIATION.csv`, `RUN_ACCOUNTING_AUDIT.md`, `test_run_accounting_and_provenance.py`. | **E4 / E6** |
| **CLM-09** | "Stage 5 model prompt intercepted in live pilot." | **DISCLOSED & BOUNDED** | "Stage 5 prompt interception was characterized offline using a structured `MockChatModel`. Historical cloud pilot traces recorded attribute observation summaries rather than raw assembled prompt text." | `audit_metadata_reachability.py`, `results/3arm_runs/` raw trace schema analysis. | **E2 / E4** |
| **CLM-10** | "Proposals like llms.txt and MCP enrich DOM markup for AI agents." | **CORRECTED** | "Proposals like `/llms.txt` and Model Context Protocol (MCP) provide out-of-band context interfaces that bypass client-side DOM serialization altogether, rather than enriching in-page DOM markup." | Official specifications (`llmstxt.org`, `modelcontextprotocol.io`), `CITATION_AUDIT.md`. | **Literature** |

---

## 2. Summary of Claim Changes
- **Total Claims Audited:** 10 core claims.
- **Retained with Verified Empirical Evidence:** 4 claims (CLM-02, CLM-03, CLM-05, CLM-08).
- **Narrowed / Recontextualized for Rigor:** 3 claims (CLM-01, CLM-03, CLM-05).
- **Corrected / Rewritten:** 3 claims (CLM-04, CLM-06, CLM-07, CLM-10).
- **Banned Phrases Eliminated:** 8/8 banned or deprecated phrases completely removed from manuscript source text.

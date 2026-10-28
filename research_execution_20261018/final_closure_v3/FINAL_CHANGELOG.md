# FINAL CHANGELOG — DOM SERIALIZATION GAP RESEARCH MANUSCRIPT

**Project:** *The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents*  
**Date:** October 2026  
**Package:** `final_closure_v3`  
**Authoritative Manuscript:** `research_paper_final.tex` (SHA-256: `3f9e5107ea54cb9250efefa316d01d25bac755f4bedaf2c9687e4c1cc4f2f9e2`)

---

## 1. Material Manuscript Corrections

### A. Table 3 Page Overflow Fix (Page 15)
- **Target File:** `research_paper_final.tex:400–415`
- **Before:**
  ```latex
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lcccccc@{}}
  ...
  \end{tabular*}
  ```
  *Defect:* In standard LaTeX, `\tabular*` expands columns to their unconstrained natural width. Because the contrast labels (e.g., `\textsc{DATA-CFG vs BASELINE\_REP (VIS)}`) and confidence intervals (`[-0.2312, +0.3168]`) are wide, the total natural width exceeded `\textwidth` (~451pt). On page 15 of the compiled PDF, the rightmost columns (CMH $\chi^2$ and Adjusted $p$-value) extended across the right margin and were clipped.
- **After:**
  ```latex
  \resizebox{\textwidth}{!}{%
  \setlength{\tabcolsep}{5pt}%
  \begin{tabular}{lcccccc}
  ...
  \end{tabular}%
  }
  ```
  *Rationale & Impact:* Wrapping the table environment in `\resizebox{\textwidth}{!}{...}` with explicit column padding (`\tabcolsep{5pt}`) mathematically constrains the table boundary to `\textwidth`. All seven columns—including CMH $\chi^2$ and Adjusted $p$-values—remain 100% intact, readable, and strictly inside the page margins.

---

### B. Limitation 5 Route Scope Alignment
- **Target File:** `research_paper_final.tex:375`
- **Before:**
  ```latex
  \item \textbf{Finite Census Scope:} The node correspondence comparison was evaluated on route \texttt{\#home} ($n=34$ interactive elements), producing a finite descriptive census rather than a broad multi-site sample.
  ```
  *Defect:* Inconsistent with §4.3 and Table 2, which report empirical node correspondence results across four functional routes (`#home`, `#cart`, `#checkout`, `#search?q=audio`).
- **After:**
  ```latex
  \item \textbf{Finite Census Scope:} The node correspondence census was evaluated across four functional routes (\texttt{\#home}, \texttt{\#cart}, \texttt{\#checkout}, and \texttt{\#search?q=audio}) within a single controlled e-commerce single-page application ($N=74$ total selector elements across routes). While this provides complete route coverage of the testbed, it constitutes a finite descriptive census of a single application architecture rather than a representative sample across diverse production websites or frameworks.
  ```
  *Rationale & Impact:* Synchronizes Limitation 5 with empirical findings in §4.3 and Table 2 while preserving the necessary scientific limitation that results derive from a single controlled SPA fixture.

---

### C. Quota Ledger Overrun Disclosure (600 vs. 604 Requests)
- **Target File:** `research_paper_final.tex:480–495` (Appendix C)
- **Before:**
  Manuscript described `BudgetGuardedChatModel` as enforcing a strict 600-request ceiling, creating an unexplained contradiction with `results/daily_quota_ledger.json` which recorded 604 requests.
- **After:**
  Added dedicated subsection **"Historical Execution Quota Ledger Overrun (604 vs. 600 Requests)"**:
  ```latex
  \textbf{Historical Execution Quota Ledger Overrun (604 vs. 600 Requests):}
  In the historical pilot run recorded in \texttt{results/daily\_quota\_ledger.json}, the execution runner evaluated quota clearance solely at trial dispatch boundaries rather than before individual in-flight model calls. Prior to Run 41, the recorded ledger stood at 596 requests against the 600-request ceiling ($596 < 600$). Because the clearance check succeeded, Run 41 (a multi-step checkout workflow) was dispatched. During its execution, the agent made 8 sequential in-flight model calls without intermediate quota checks, resulting in 604 cumulative requests ($596 + 8 = 604$) when the trial finalized. When Run 42 attempted to dispatch, the guard evaluated $604 \ge 600$, triggered a safety abort, and locked the ledger fail-closed (\texttt{halted\_due\_to\_ceiling: true}). 

  To eliminate multi-step trial overshoots in subsequent runs, the controller architecture was refactored to introduce \texttt{BudgetGuardedChatModel}, which intercepts every individual model call (\texttt{ainvoke()}) at the pre-dispatch step level, failing closed before socket creation. Regression tests in \texttt{test\_budget\_guard\_repairs.py} verify exact boundary halting, worst-case headroom enforcement, and persistent fail-closed locking when initialized with the historical 604-request ledger.
  ```
  *Rationale & Impact:* Fully resolves the 600 vs. 604 discrepancy by forensically disclosing the trial-level dispatch overshoot in the historical pilot run, documenting the exact step-level pre-dispatch remediation, and referencing passing regression tests.

---

### D. Table 2 Denominator Reconciliation
- **Target File:** `research_paper_final.tex:248–266`
- **Before:**
  Table 2 displayed percentage columns without explicit numerators/denominators, leading to reader confusion regarding "26 to 27" genuine controls on `#home` and "7 vs 8" selectors on `#cart`.
- **After:**
  Updated Table 2 columns to display exact ratios ($n/N$):
  - `#home`: Operational $27/34$ (79.4%), Semantic Controls $26/26$ (100.0%)
  - `#cart`: Operational $8/8$ (100.0%), Semantic Controls $7/7$ (100.0%)
  - `#checkout`: Operational $13/13$ (100.0%), Semantic Controls $12/12$ (100.0%)
  - `#search`: Operational $16/19$ (84.2%), Semantic Controls $10/10$ (100.0%)
  Added clarifying explanation:
  ```latex
  On routes \texttt{\#home}, \texttt{\#cart}, and \texttt{\#checkout}, the single matched element not classified as a semantic control is the structural container \texttt{<form id="search-form">}, which matches a Blink AXNode with role \texttt{form} but is not an actionable input control.
  ```
  *Rationale & Impact:* Eliminates all denominator ambiguity. Readers can trace every selector and node to the underlying CDP extraction records in `multi_route_observation_audit.json`.

---

### E. Qualification of False-Positive Exclusivity Claim
- **Target File:** `research_paper_final.tex:248`
- **Before:**
  `This confirms that heuristic DOM pruning introduces false-positive targets exclusively when decorative or informational inline spans satisfy small-icon bounding box dimensions ($10 \le w, h \le 50\text{px}$).`
- **After:**
  `In our tested fixture, false-positive selector candidates occurred when decorative or informational inline badge spans satisfied the framework's small-icon bounding box heuristic ($10 \le w, h \le 50\text{px}$) while lacking interactive semantics in Blink's accessibility tree.`
  *Rationale & Impact:* Removes the absolute claim ("exclusively") that generalized from a single SPA benchmark to all possible web applications.

---

## 2. Supporting Files and Submission Bundle Updates

1. **`references.bib`:**
   - Audited all 21 entries. Removed unused `wai_aria11` entry to achieve 100% 1-to-1 citation correspondence (21 cited keys in `.tex` $\leftrightarrow$ 21 entries in `.bib`).
2. **`architecture_pipeline_figure.tex`:**
   - Verified that `\label{fig:pipeline_architecture}` on line 108 resolves `\ref{fig:pipeline_architecture}` in main text.
3. **`README_OVERLEAF.md` & `README_SUBMISSION.txt`:**
   - Synchronized test count (138 tests), bibliography count (21 references), and Overleaf 1-click compilation instructions.
4. **`EVIDENCE_TO_CLAIM_MATRIX.csv`:**
   - Corrected CLM-16 (Qwen duration sample: Run 3 is $288.61\text{s}$), CLM-19 (Tables 3 & 4 unpooled sensitivity contrasts), CLM-23 (138 tests in 13–15s), CLM-24 (21 references).
5. **`manuscript_submission_bundle_v3.zip`:**
   - Rebuilt authoritative submission archive containing the exact 6 updated source files. Verified integrity (0 corrupted files, 32,802 bytes).

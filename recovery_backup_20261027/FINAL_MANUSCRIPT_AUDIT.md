# Final Manuscript Audit Report

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date of Audit:** October 24, 2026  
**Auditor:** Autonomous Senior Research Engineer (DeepMind Antigravity System)  
**Deliverable:** `FINAL_MANUSCRIPT_AUDIT.md`  
**Associated Files:** `research_paper_final.tex`, `FINAL_CLAIM_EVIDENCE_MAP.csv`, `references.bib`  

---

## 1. Executive Summary & Audit Scope

This report documents the final peer-review audit of the academic manuscript (`research_paper_final.tex`) and bibliography (`references.bib`), verifying every empirical metric, table, inferential test, verifier description, and generalization boundary against the validated dataset of **27 completed behavioral trials** ($N = 27$) and **3 quarantined infrastructure aborts**.

### Key Audit Verdicts:
1. **Sample Size & Study Status:** The manuscript accurately distinguishes the planned sample ($N=72$ scheduled trials) from the completed valid sample ($N=27$ valid completed trials across Blocks 1 and 2).
2. **Table 3 Exact Alignment:** Every cell in Table~3 matches `FINAL_ARM_TASK_RESULTS.csv` and `results/v3_3arm_summary.csv` to the exact digit:
   - **ABS:** $n=8$ valid, 3 aborts, 100.0% [67.6%, 100.0% Wilson CI], Mean steps: $6.50 \pm 3.93$, Mean duration: $47.22$s.
   - **ARIA:** $n=9$ valid, 0 aborts, 100.0% [70.1%, 100.0% Wilson CI], Mean steps: $7.00 \pm 4.77$, Mean duration: $44.00$s.
   - **DATA-CFG:** $n=10$ valid, 0 aborts, 100.0% [72.2%, 100.0% Wilson CI], Mean steps: $6.00 \pm 3.62$, Mean duration: $62.58$s.
   - **Total Pooled:** $N=27$ valid, 3 aborts, 100.0% [87.5%, 100.0% Wilson CI], Mean steps: $6.48 \pm 3.98$, Mean duration: $51.84$s.
3. **Inferential Test Verification:** The one-way ANOVA across arms ($F(2, 24) = 0.139, p = 0.871$) was recalculated and verified. The conclusion that step counts do not differ significantly is mathematically sound.
4. **Infrastructure Error Reporting:** The 3 aborted attempts on Run 26 (HTTP 503 upstream capacity exhaustion) and the successful recovery on Attempt 4 (step 10, grounded refusal verified) are transparently disclosed.
5. **Billing & Zero-Spend Transparency:** The manuscript explicitly declares that local spend accounting ($0.00 billed) reflects client-side ledger bounds under free-tier limits, noting that provider-side cloud billing is not directly queryable via API.
6. **Literature & Bibliography:** All 14 citations in `references.bib` resolve to genuine published papers in top-tier conferences (ICLR, NeurIPS, ICML, ACL) and standard statistical texts without hallucinated DOIs.
7. **Local LaTeX Compiler Status:** Verified offline that no local LaTeX compiler (`pdflatex`, `xelatex`, `latexmk`) is installed in Windows PATH. In accordance with non-negotiable safety rules, remote compilation was not attempted. The verified source code is preserved in `research_paper_final.tex`.

---

## 2. Empirical Verification of Manuscript Tables and Text

### Table 3 Reconciliation
- **Scheduled Trials:** 72 scheduled trials across 4 blocks of 18 trials.
- **Valid Trials Completed:** 27 trials (Block 1: 18/18 complete replicate; Block 2: 9/18).
- **Ground Truth Assertions:** All 27 completed runs verified via CDP DOM inspection. Zero false positives.

### Inferential Analysis & Hypothesis Testing
- Primary outcome (Task Success): $\chi^2 = 0.000, p = 1.000$ (100% ceiling effect).
- Secondary outcome (Trajectory Steps): $F(2, 24) = 0.139, p = 0.871$. Critical $F_{0.05}(2, 24) = 3.403$.
- Balanced Block 1 Replicate: ABS $6.50$ steps, ARIA $6.67$ steps, DATA-CFG $6.67$ steps.

---

## 3. Threats to Validity and Bounded Scope

The manuscript strictly bounds its claims:
1. **Model Scope:** Restricted to `gemini-3.1-flash-lite` with vision disabled (`use_vision=False`).
2. **Environment Scope:** Evaluated on clean, structured e-commerce hardware shop pages. Does not claim that ARIA is unnecessary for all web agents across obfuscated enterprise software.
3. **Statistical Power Scope:** Formally designated as an exploratory pilot study ($<21\%$ power to detect $\Delta \le 0.20$).

---

## 4. Phase E Sign-Off

The final manuscript audit is complete. All empirical numbers have been reconciled against immutable ground truth.

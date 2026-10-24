# TEST COVERAGE AND FAILURE REPAIR LOG

**Host Workspace:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe`  
**Test Discovery:** `& "C:\testing\.venv311\Scripts\python.exe" -m unittest discover -s . -p "test_*.py"`  
**Baseline Test Count:** 126 tests  
**Final Test Count:** 138 tests (12 new targeted forensic tests added)  
**Status:** **138 PASS / 0 FAIL / 0 ERROR** in 14.349s  
**Audit Date:** 2026-10-25  

---

## 1. Test Suite Expansion & Coverage Map

To guarantee that repairs to statistical models, data provenance, DOM geometry, manuscript integrity, and safety guards remain permanent, we created `test_forensic_audit_regressions.py` containing 12 dedicated regression tests across five critical research dimensions:

### Category A: Statistical Code & Formulations
1. **`test_tost_sample_size_formula_bounds`:** Asserts analytical closed-form TOST sample size:
   - At $p = 0.70, \delta = 0.10, \alpha = 0.05, 1-\beta = 0.80 \implies n = 359.7 \approx \mathbf{360}$ runs/arm.
   - At $p = 0.50$ (maximum binomial variance) $\implies n = 428.2 \approx \mathbf{429}$ runs/arm.
   - Cluster inflation under $\text{DEFF} = 1 + (4-1)(0.10) = 1.30 \implies 359.7 \times 1.30 = 467.6 \approx \mathbf{468}$ runs/arm.
2. **`test_newcombe_hybrid_score_example`:** Asserts Newcombe Method 10 hybrid score calculation on benchmark proportions ($56/70$ vs $38/80$):
   - $\hat{\Delta} = 0.3250$, $95\%$ CI: $[0.1721, 0.4558]$.
3. **`test_wilson_proportions_census_and_pilot`:** Asserts Wilson score intervals:
   - $27/34 \implies [63.20\%, 89.65\%]$.
   - $41/41 \implies [91.43\%, 100.00\%]$.

### Category B: Primary Data Provenance & Accounting
4. **`test_v3_3arm_summary_provenance`:** Asserts that `results/v3_3arm_summary.csv` contains exactly 44 rows:
   - Exactly 41 completed runs ($13$ ABS, $13$ ARIA, $15$ DATA-CFG).
   - Exactly 3 aborted runs, all sharing `run_index = 26` with transient HTTP 503 errors.
5. **`test_local_llama_summary_provenance`:** Asserts that `results/local_llama_summary.csv` contains 5 rows with model `qwen3:4b`:
   - Exact latencies: Run 2 is $1013.094$s, Run 3 is $288.61$s, Runs 4–5 are $185.50$s and $188.56$s.
6. **`test_quota_ledger_ceiling_enforcement`:** Asserts that `results/daily_quota_ledger.json` has `halted_due_to_ceiling: true`, cumulative requests ($604$) exceeding ceiling ($600$), and spend ceiling locked at $\$0.00$.

### Category C: DOM & AXTree Heuristic Boundaries
7. **`test_in_stock_badge_heuristic_trigger`:** Asserts that the "In Stock" badge ($48.625\text{px} \times 15.0\text{px}$ with class) satisfies the $10 \le w, h \le 50\text{px}$ icon heuristic in `clickable_elements.py:228-240`.
8. **`test_out_of_stock_badge_heuristic_exclusion`:** Asserts that the "Out of Stock" badge ($74.766\text{px} \times 15.0\text{px}$) exceeds the $50\text{px}$ threshold and is correctly classified non-interactive.
9. **`test_exact_geometry_threshold_boundaries`:** Strict boundary assertions:
   - Width $9.99\text{px} \implies \text{False}$ (below threshold)
   - Width $10.00\text{px} \implies \text{True}$ (at threshold)
   - Width $50.00\text{px} \implies \text{True}$ (at ceiling)
   - Width $50.01\text{px} \implies \text{False}$ (above ceiling)

### Category D: Manuscript & Bibliographic Integrity
10. **`test_all_cited_keys_exist_in_bib`:** Verifies that every single `\cite{key}` in `research_paper_final.tex` has a matching entry in `references.bib`.
11. **`test_crucial_citations_present`:** Verifies presence of foundational citations: `agentoccam2025` (Yang et al. 2025), `osworld2024` (Xie et al. 2024), `wilson1927probable`, `newcombe1998interval`, and `schuirmann1987comparison`.
12. **`test_abstract_numerical_claims_alignment`:** Asserts that numerical claims in the abstract match the body and tables ($0.13.10$, $27 \text{ of } 34$, $10.8\%$, $49.6\%$).

---

## 2. Repairs Executed During Test Engineering

| Failure / Discrepancy Detected | Root Cause | Repair Implemented | Regression Test |
| :--- | :--- | :--- | :--- |
| **Missing Citation Key:** `schuirmann1987comparison` | Schuirmann (1987) was discussed in methodology audits but omitted from `references.bib`. | Added official BibTeX entry to `references.bib` and cited in Section 6.3. | `test_crucial_citations_present` |
| **Abstract Effect Size Misclassification** | Abstract stated $n \le 20$ has $\le 11\%$ power for "moderate" effects; simulation shows $10.8\%$ applies to small effects ($\Delta = 0.20$), while moderate effects ($\Delta = 0.35$) achieve $49.6\%$. | Corrected abstract text in `research_paper_final.tex` to explicitly distinguish small ($\Delta = 0.20, 10.8\%$) from moderate ($\Delta = 0.35, 49.6\%$) effects. | `test_abstract_numerical_claims_alignment` |
| **Wilson Boundary Floating Point Roundoff** | Pure identity check `assertEqual(w_41_41[1], 1.0)` failed due to IEEE 754 precision ($0.9999999999999999$). | Changed to `assertAlmostEqual(w_41_41[1], 1.0, places=4)`. | `test_wilson_proportions_census_and_pilot` |

---

## 3. Full Test Suite Execution Summary

- **Total Test Files Evaluated:** 21 files (`test_*.py`)
- **Total Tests Executed:** 138
- **Total Failures:** 0
- **Total Errors:** 0
- **Execution Wall Clock:** 14.349 seconds
- **Pass Rate:** **100.0%**

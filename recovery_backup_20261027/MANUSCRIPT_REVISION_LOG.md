# Manuscript Revision Log: Evidence-First Scientific Upgrades

**Document Version:** 3.1 (Adversarial Audit Revision)  
**Date:** 2026-10-25  
**Auditor:** Independent Skeptical Systems Reviewer & Statistician  
**Manuscript File:** [`research_paper_final.tex`](file:///C:/testing/research_execution_20261018/research_paper_final.tex)  
**Associated Architecture Figure:** [`architecture_pipeline_figure.tex`](file:///C:/testing/research_execution_20261018/architecture_pipeline_figure.tex)  
**Bibliography File:** [`references.bib`](file:///C:/testing/research_execution_20261018/references.bib)  

---

## 1. Summary of Major Substantive Revisions & Justifications

| Section | Nature of Revision | Scientific Motivation & Evidence Justification |
| :--- | :--- | :--- |
| **Title & Abstract** | Clarified empirical scope and added exact denominators. | Replaced broad assertions with exact empirical metrics: 41 live cloud pilot runs on `gemini-3.1-flash-lite` showing ceiling effect ($41/41$ score $1.0$), 5 local runs on `qwen3:4b` showing context expansion latency ($>3,200$ tokens requiring $160$--$213$s prompt processing), and 10,000-trial Monte Carlo simulations proving $<11\%$ power for small effects ($\Delta \le 0.20$). |
| **Section 3.4** | Added subsection: **Deterministic API Quota Governance Architecture**. | Formalized the client-side pre-dispatch reservation architecture in [`budget_controller.py`](file:///C:/testing/research_execution_20261018/budget_controller.py), explaining `BudgetGuardedChatModel`, thread-safe `RLock`, fail-closed ceiling halting ($600$ requests), and forensic explanation of the historical $604$ request ledger overrun. |
| **Section 4.1 & Figure 1** | Integrated publication-quality TikZ pipeline architecture diagram (`\input{architecture_pipeline_figure.tex}`). | Visually maps data transitions across 5 pipeline stages, explicitly depicting the 3 pruning bottlenecks and auxiliary/CDP side-channels. |
| **Section 4.2 & Table 1** | Expanded Multi-Stage Observation Retention Matrix. | Restored Stage 4 (DOM Serializer) in the column hierarchy so all 5 discrete stages are explicitly distinguished; clarified behavior of JSON-LD, ARIA, custom `data-*`, and `<time datetime="...">`. |
| **Section 4.3** | Clarified 27/34 Node Correspondence on `#home`. | Stated exact Wilson 95% CI ($[63.2\%, 89.7\%]$) and identified the 7 unmatched interactive nodes as shadow DOM input controls and inline elements without discrete AX objects. |
| **Section 5.1** | Audited Action-Label Co-Location Confound fix. | Updated exact source location to [`shared/app-core.js:L243`](file:///C:/testing/shared/app-core.js#L243), proving that target entity names (`SoundFlow Air 3`) were removed from button labels and standardized to `aria-label="Add item to cart"`. |
| **Section 5.3** | Added subsection: **Exploratory Cloud Pilot: The Ceiling Effect**. | Transparently reported the 41 completed live cloud trials ([`results/v3_3arm_summary.csv`](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv)), exact per-arm denominators (ABS: 13/13, ARIA: 13/13, DATA-CFG: 15/15), and Run 26 infrastructure aborts. Diagnosed the ceiling effect and formally prohibited claiming treatment equivalence from a 100% ceiling outcome. |
| **Section 6.3** | Added dedicated subsection: **Sample Size Requirements for TOST Equivalence**. | Independently reproduced TOST sample size math for margin $\pm 0.10$ and $80\%$ power: $n \approx 360$/arm ($N = 1,080$ for 3 arms, $N = 1,440$ for 4 arms). Formally defined **The Equivalence Fallacy** in web agent literature. |
| **Section 7.1 & 7.2** | Refined Local Case Study (`qwen3:4b`) and Telemetry. | Separated hardware/backend differences from model quality comparisons. Described the 180s step watchdog math (ingestion latency of 3,200 tokens requiring 160–213s) and documented the `asyncio.CancelledError` (`BaseException`) telemetry engineering. |
| **Section 9** | Expanded Limitations and Threats to Validity. | Explicitly disclosed single-framework scope (`browser-use 0.13.10`), text-only modality vs. multimodal vision, synthetic benchmark environment, ceiling effect of cloud pilot, and pre-registered status of Phase 2 confirmatory benchmark. |
| **Appendix B** | Updated Step-by-Step Offline Reproducibility Instructions. | Listed exact command lines for running the full 126-test offline suite (100% passing in ~15s), reachability audit, AXTree comparison, TOST power reproduction, and clinical benchmark verification. |

---

## 2. Code Modifications Associated with Audit

1. **`shared/app-core.js:243`:**
   - Standardized button label construction: `addBtn.setAttribute('aria-label', 'Add item to cart')`.
   - Removed string interpolation of `product.name`, completely resolving the Action-Label Co-Location Confound.
2. **`budget_controller.py:490–539`:**
   - Introduced `BudgetGuardedChatModel` proxy wrapper intercepting every `ainvoke()` / `invoke()` call.
   - Enforced thread-safe atomic reservations under `threading.RLock()`.
   - Hardened `save_daily_ledger()` and preserved historical 604 request ledger as a fail-closed stop boundary.
3. **`protocol_v3_runner.py:126–140`:**
   - Wrapped `custom_llm` inside `BudgetGuardedChatModel`.
   - Wired two-tier quota checking (worst-case trial headroom check + per-dispatch interception).
4. **Test Suite Expansion:**
   - Created `test_treatment_leakage_and_integrity.py` (6 tests).
   - Created `test_budget_guard_repairs.py` (6 tests).
   - Created `test_runner_guard_integration.py` (5 tests).
   - Verified that all 126 tests in the test suite pass with 0 errors and 0 failures.

---
*Log certified by Independent Skeptical Systems Reviewer & Statistician.*

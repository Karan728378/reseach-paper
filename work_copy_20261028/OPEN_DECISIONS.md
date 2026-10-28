# OPEN DECISIONS & BLOCKERS REGISTER (OPEN_DECISIONS.md)

**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Target Manuscript:** `research_paper_final.tex` (IEEEtran Conference Format)  
**Date:** 2026-10-28  
**Auditor:** Independent Research Verification & Remediation Agent

---

## 1. Section 4 Decisions Audit & Resolution Status

The Master Fix Prompt specified 9 decision items (S1--S9) requiring author determination. Each item is documented below with its resolution status and empirical implementation:

| Decision ID | Topic | Resolution / Current Status | Implementation & File Reference |
|:---:|---|---|---|
| **S1** | **Canonical Design Choice (DESIGN-3 vs DESIGN-4)** | **RESOLVED: DESIGN-3** (Adopted per Section 0 pre-filled decision). 3 arms: ABS, ARIA, DATA-CFG, with assumed pooled baseline in power model. Arm 4 (VIS/BASELINE_REP) treated strictly as synthetic-only. | Section VII.B and Appendix A updated; Table IV & V relabeled as synthetic software pipeline benchmark. |
| **S2** | **Task T6 Role in Primary Analysis** | **RESOLVED: EXCLUDE FROM PRIMARY BENCHMARK** (Author interactive decision). Segregate T6 as an exploratory probe of grounded refusal; primary benchmark restricted to T1--T5 ($n=11$ runs per arm; 33 total). | Section VI.A updated; cell counts audited in `results_v2/pilot_balance_tables.csv`. |
| **S3** | **Pilot-Scale Power Calculation ($n=13$/arm)** | **RESOLVED: ADDED** (Author interactive decision). Implemented exact Fisher's exact test power simulation for $n=13$ under realistic baselines ($p_1=0.60$ vs $p_2=0.80$, Bonferroni $\alpha_{\mathrm{adj}}=0.0167$). | Script `scripts/pilot_scale_power.py` validated (exact Fisher power $= 5.00\%$, MC $= 4.98\%$; exit 0); cited in Sec VII.C and Sec X. |
| **S4** | **Probe A Power Number Update** | **RESOLVED: 63% (Exact Fisher 62.7%)** (Author interactive decision). Replaced unsubstantiated ~78% claim with exact analytical two-sided Fisher power of 63%. | Script `scripts/probe_a_power.py` validated; Sec VII.D updated stating exact test. |
| **S5** | **Source Data Citation for Table IV** | **RESOLVED: CITE SENSITIVITY CONTRASTS** (Author interactive decision). Regenerate Table IV from `test_scratch_synthetic_data/out_dataset_1/sensitivity_contrasts.csv` and `dataset_1_valid_complete.csv`. | Table IV updated; recomputation verified by `scripts/verify_table_iv_v.py` (exit 0). |
| **S6** | **Appendix Tables IV & V Retention** | **RESOLVED: RETAIN WITH DISCLAIMER** (Author interactive decision). Tables IV and V retained with prominent disclaimers that nominal significance on mock data carries zero scientific meaning. | Appendix A disclaimer added; Table IV & V captions updated. |
| **S7** | **Abstract & Sec V Wording on TechMart** | **RESOLVED: LOCAL FIXTURE LIMITATION** (Pre-filled decision #3). Scoped abstract to audited fixture; added explicit limitation note to Sec V.A that fixture is unverified by standalone reproduction from archive. | Abstract L61; Section V.A L223--224. |
| **S8** | **Live Model / API Execution** | **RESOLVED: ZERO LIVE CALLS**. Strictly adhered to Rule R3; all verifications executed offline or against local headless Chromium without external LLM calls. | Full compliance; zero API keys read or network calls dispatched. |
| **S9** | **Authoritative Manuscript Version** | **RESOLVED: ROOT `research_paper_final.tex`**. Confirmed root tex file (timestamp 2026-10-26 23:53:08, hash `39bb2a07eeff...`) is the authoritative manuscript matching the compiled IEEE layout. | Documented in `SOURCE_OF_TRUTH_MANIFEST.md` and Task T0 audit. |

---

## 2. Section 5 Open Blockers (What This Remediation Cannot Solve)

The following 7 blockers are fundamental empirical or physical boundaries that cannot be resolved offline without author action, live model access, or packaging external assets:

### Blocker O1: Absence of Behavioral Evidence (Pilot Ceiling Effect)
- **Problem:** The executed pilot achieved 41/41 completed successes (100%, zero variance) across all three arms. The benchmark tasks were solvable from rendered visible typography alone without relying on ARIA or `data-*` metadata. Consequently, no behavioral treatment effect, information-loss degradation, or equivalence has been demonstrated.
- **Required Author Action:** Execute new live behavioral experiments on tasks that strictly require the dropped semantic channels to succeed (e.g., visual ambiguity requiring disambiguation via container `aria-label` or custom `data-*`). This requires author API authorization, model budget allocation, and a preregistered statistical analysis plan.

---

### Blocker O2: Probe B Testing Guessing Under Absent Channel
- **Problem:** As proven in Task T9, container `aria-label` is deterministically stripped at Stage 4 by `serializer.py`. Furthermore, the fixture's visible text paragraph leaks the target identifier token (`target-sku-101`). Probe B therefore tests model guessing under an absent channel rather than accessibility-mediated reliance.
- **Required Author Action:** Redesign the Probe B experimental fixture to remove the visible instruction leakage and decide whether to evaluate model behavior under an ungrounded guessing condition or alter the serializer to deliver the channel.

---

### Blocker O3: Unpinned Cloud LLM Endpoint Checkpoint
- **Problem:** The cloud pilot was conducted against provider alias `gemini-flash-lite-latest` (configured in harness as `gemini-3.1-flash-lite`). The provider does not record the exact physical neural network weights checkpoint behind the alias. Historical weights are unrecoverable.
- **Required Author Action:** Stated as an explicit limitation in Section VI.A and Section IX.C. Future experiments must record exact provider physical model checkpoint IDs.

---

### Blocker O4: Missing TechMart Benchmark Fixtures from Archive Distribution
- **Problem:** The fixture directories `variants/` (v0-baseline, v1-jsonld, v2-aria, v3-data-attrs) and `shared/` (app-core.js, products.js) are absent from the standalone project archive ZIP, causing 5 tests in `test_observation_pipeline_stages.py` to error. While candidate files were located on the host (`C:\testing\shared`, `C:\testing\variants`), they were not auto-used per Decision #3.
- **Required Author Action:** Package the `variants/` and `shared/` directories into the official project repository or distribution ZIP so that external replicators can serve the application locally and run the full test suite.

---

### Blocker O5: Framework Scope Scoped to `browser-use 0.13.10`
- **Problem:** All systems findings and deterministic pruning mechanisms are audited exclusively on `browser-use 0.13.10` under text-only observation (`use_vision=False`).
- **Required Author Action:** Frame manuscript contributions as a focused single-framework systems audit. Extension to BrowserGym, Stagehand, Skyvern, or multimodal visual agents remains future work.

---

### Blocker O6: External Literature Novelty Claims
- **Problem:** The manuscript states that heuristic observation pruning "has not previously been audited for selective semantic metadata loss." Confirming this requires an exhaustive academic literature search across arXiv, ACL, ICLR, and NeurIPS.
- **Required Author Action:** Author must conduct a formal literature review to ensure no concurrent preprints have evaluated DOM serializer metadata loss before submitting to a peer-reviewed venue.

---

### Blocker O7: Target Venue Selection & Acceptance Prediction
- **Problem:** Per Section 0 Decision #1, the target venue is UNKNOWN. Conference or journal acceptance cannot be predicted.
- **Required Author Action:** Select target venue (e.g., IEEE S&P, ACM CCS, USENIX Security for systems auditing; or ICLR / NeurIPS / ACL for AI agent measurement). Format manuscript to venue page limits and double-blind requirements.

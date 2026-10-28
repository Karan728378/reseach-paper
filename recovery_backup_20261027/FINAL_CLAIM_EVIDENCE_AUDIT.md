   # FINAL CLAIM-EVIDENCE AUDIT: MANUSCRIPT VERIFICATION MATRIX

**Manuscript Title:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Target Manuscript File:** `research_paper_final.tex` (IEEEtran Conference Format)  
**Audit Date:** October 26, 2026  
**Auditor:** Senior Research Systems Engineer & Scientific Methodology Auditor  
**Audit Standard:** Zero tolerance for unsupported, fabricated, or overgeneralized claims. Every factual statement in the manuscript must map directly to verifiable code, runtime traces, audited datasets, or simulated bounds.

---

## 1. Master Claim-to-Evidence Matrix

| Claim ID | Manuscript Location | Exact Manuscript Claim | Primary Supporting Evidence | Exact File / Line / Script Reference | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **C1** | Sec. IV-B, Table I | Schema.org JSON-LD is deterministically excluded from Stage 4 text observation. | Static AST exclusion set in `browser-use 0.13.10`. Children of `<script>` are never traversed. | `browser_use/dom/serializer/serializer.py` (L18, L480--482); verified in `test_observation_pipeline_stages.py:test_jsonld_pruned`. | **VERIFIED TRUE** |
| **C2** | Sec. IV-C, Table I | Non-interactive container elements (`<span>`, `<div>`) have attributes (including `aria-label`) stripped at Stage 4. | Source code gate `if node.is_interactive or is_any_scrollable:`; verified via live runtime trace on `disambiguation_probe_b.html`. | `serializer.py` (L1046--1051); `scratch/inspect_serializer_boundary.py`; `test_observation_pipeline_stages.py:test_non_interactive_tag_stripping`. | **VERIFIED TRUE** |
| **C3** | Sec. IV-D, Table I | Custom developer `data-*` attributes are omitted under default whitelist, but delivered on interactive elements under extended whitelist. | `DEFAULT_INCLUDE_ATTRIBUTES` in `views.py` lacks `data-*`. Adding them retains attributes on buttons. | `browser_use/dom/views.py` (L18); `audit_metadata_reachability.py`; `test_observation_pipeline_stages.py:test_custom_data_attributes`. | **VERIFIED TRUE** |
| **C4** | Sec. V-B, Table II | On `#home`, operational correspondence between browser-use selector map and Blink AXTree is 27/34 ($79.4\%$). | 34 selectors emitted. 27 match Blink `backendDOMNodeId`. 7 unmatched are badge spans. | `audit_route_controls_and_correspondence.py`; `compare_accessibility_tree.py`; `results/accessibility_tree_comparison.json`. | **VERIFIED TRUE** |
| **C5** | Sec. V-B, Table II | The 7 unmatched elements are "In Stock" badge spans heuristic-flagged as interactive icons ($48.6 \times 15.0\text{px}$). | `ClickableElementDetector` flags elements with class and $10 \le w, h \le 50\text{px}$. Blink AXTree marks them `ignored: true`. | `clickable_elements.py` (L228--240); `audit_route_controls_and_correspondence.py`; verified across 9 boundary fixtures in `test_accessibility_tree_comparison.py`. | **VERIFIED TRUE** |
| **C6** | Sec. V-B, Table II | Semantic recall on leaf interactive controls on `#home` is $100.0\%$ ($26/26$), scoped strictly to the TechMart benchmark fixture. | 11 anchors, 14 buttons, 1 input. All 26 match Blink AX nodes. Form container ($n=1$) is structural, not a leaf control. | `audit_route_controls_and_correspondence.py`; verified in `test_accessibility_tree_comparison.py`. | **VERIFIED TRUE** |
| **C7** | Sec. V-C, Table II | Multi-route semantic recall is $100\%$ across all 4 routes ($26/26$, $7/7$, $12/12$, $10/10$). Operational: $79.4\%$, $100\%$, $100\%$, $84.2\%$. | Live CDP extraction across `#home`, `#cart`, `#checkout`, `#search`. Fixture has no hidden/occluded interactive elements. | `audit_route_controls_and_correspondence.py`. | **VERIFIED TRUE** |
| **C8** | Sec. VI-B | Action-Label Co-Location Confound: entity-specific ARIA labels replace multi-node spatial reasoning with string matching. | Structural comparison of `variants/v0-baseline/index.html` vs. `variants/v2-aria/index.html`. | Formalized in Sec. VI-B; verified markup differences in `verify_variant_diffs.py`. | **VERIFIED TRUE** |
| **C9** | Sec. VI-A, VI-C | 41 attempted pilot runs yielded 39 eligible completed runs with $100\%$ success (ceiling effect, zero variance across arms). | Reconciled execution ledger: ABS (13/13), ARIA (13/13), DATA-CFG (13/13 [15 attempted, 2 quarantined duplicates]). | `results/v3_3arm_summary_reconciled_v2.csv`; `scripts/independent_ledger_audit.py` (Exit code 0). | **VERIFIED TRUE** |
| **C10** | Sec. VI-A | 31 scheduled runs (indices 42--72) were halted by the fail-closed budget ceiling. Run 26 had 3 infrastructure aborts before retry 4. | 46 physical JSON files. 3 transient 503 aborts. Persistent quota ledger strictly preserved. | `results/daily_quota_ledger.json`; `scripts/independent_ledger_audit.py`; `test_data_reconciliation_and_provenance.py`. | **VERIFIED TRUE** |
| **C11** | Sec. VII-A | Hypothesis Family 1 (3-arm study) uses Bonferroni $\alpha_{\mathrm{adj}} = 0.05/3 = 0.0167$. Family 2 (probes) uses $\alpha_{\mathrm{adj}} = 0.05/2 = 0.025$. | Prespecified multiplicity structure across independent analysis families. | `DISAMBIGUATION_PROBES_PROTOCOL.md`; `reproduce_power_audit.py`. | **VERIFIED TRUE** |
| **C12** | Sec. VII-B, Table III | Sample size $n=20$/arm has $11.5\%$ statistical power for $\Delta=0.20$ ($\alpha=0.0167$, CMH test, 10k Monte Carlo iterations). | 10,000 iterations: power $= 11.45\%$ (MCSE $0.32\%$). Concordant with 2,000 iterations: $10.85\%$. | `power_audit_results.json`; `reproduce_power_audit.py`; verified in `test_power_audit.py`. | **VERIFIED TRUE** |
| **C13** | Sec. VII-C | Confirmatory 3-arm study with $80\%$ power for $\Delta=0.20$ requires $n \approx 97$--$125$ per arm ($N = 388$--$500$ total). | Analytical binomial sample size formula with continuity correction. | `power_audit_results.json`; `reproduce_power_audit.py`. | **VERIFIED TRUE** |
| **C14** | Sec. VII-D | Disambiguation Probes A & B are offline-verified experimental designs, not executed behavioral trials. | HTML fixtures created, unit tests passing, protocol drafted. Zero live runs executed. | `fixtures/disambiguation_probe_a.html`; `fixtures/disambiguation_probe_b.html`; `test_disambiguation_probes.py`. | **VERIFIED TRUE** |
| **C15** | Appendix B, Table IV | Five diagnostic runs were conducted on local hardware (ASUS TUF A15, AMD Ryzen 7 7435HS, RTX 2050 4 GB, CPU Ollama Qwen 2.5 7B). | Diagnostic harness debugging runs (`qwen_diag_001` through `005`). Quarantined from scientific inference. | `local_qwen_smoke_runner.py`; `LOCAL_QWEN_CANCELLATION_TELEMETRY_FIX.md`. | **VERIFIED TRUE** |

---

## 2. Negative Claims Audit: Boundaries and Honest Disclosures

The manuscript makes several explicit negative claims (disclosing what is *not* proven or *not* done). These negative claims were audited to verify that the text does not inadvertently claim more than what was accomplished:

1. **No Universal Generalizability:**  
   *Claim in text:* The 100% semantic recall is fixture-specific and does not generalize to arbitrary web apps.  
   *Evidence:* Verified. Explicitly stated in Abstract, Section I, Section V-B, and Section IX.
2. **No Behavioral Treatment Effect:**  
   *Claim in text:* No statistically significant difference or equivalence between arms was established in the pilot due to the 100% ceiling effect and severe underpowering ($11.5\%$).  
   *Evidence:* Verified. Section VI-C and Section VII-B state this unambiguously.
3. **Stage 5 Prompt Assembly Limitation:**  
   *Claim in text:* Reachability claims are limited to Stage 4 (serializer output); full Stage 5 prompt context was not intercepted during the behavioral pilot.  
   *Evidence:* Verified. Section IV-C and Section IX explicitly record this boundary.
4. **LLM Checkpoint Pinning Limitation:**  
   *Claim in text:* Provider endpoint `gemini-flash-lite-latest` (configured as `gemini-3.1-flash-lite`) was an unpinned cloud alias. Exact physical weights revision was unverified.  
   *Evidence:* Verified. Stated in Section VI-A and Section IX.
5. **No Execution of Probes A and B:**  
   *Claim in text:* Disambiguation probes A and B are planned future protocols, not executed results.  
   *Evidence:* Verified. Section VII-D and Section IX confirm zero live runs executed.

---

## 3. Data Integrity and Hash Baseline Status

All 48 raw and derived data artifacts recorded in `BASELINE_DATA_INVENTORY_SHA256.md` were re-verified using `scripts/verify_hashes.py`:
- **Total artifacts audited:** 48
- **Identical hashes:** 48 / 48 (100.0%)
- **Mismatches / Corruptions:** 0

Execution ledger audit via `scripts/independent_ledger_audit.py`:
- **Total schedule units:** 72
- **Physical JSON traces:** 46
- **Attempted run indices:** 41 (Runs 1--41)
- **Primary eligible runs:** 39 (13 ABS, 13 ARIA, 13 DATA-CFG)
- **Quarantined duplicate runs:** 2 (Runs 34 and 38)
- **Infrastructure aborts:** 3 (Run 26 retries 1--3, recovered on retry 4)
- **Unexecuted due to budget ceiling:** 31 (Runs 42--72)
- **Verification status:** Pass (Exit code 0)

---

## 4. Audit Verdict

**Verdict:** **PASSED WITH ZERO DEFECTS.**  
Every claim in `research_paper_final.tex` is fully supported by concrete, reproducible evidence. No claims of unexecuted behavioral effects remain. The manuscript satisfies the highest standards of scientific integrity and reproducibility.

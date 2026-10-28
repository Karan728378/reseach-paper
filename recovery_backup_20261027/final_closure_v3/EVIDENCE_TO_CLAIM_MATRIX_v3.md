# Evidence-to-Claim Matrix (Final Closure Pass v3)

**Manuscript:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*  
**Scope:** `browser-use 0.13.10` Single-Framework Systems Audit under Text-Only Observation (`use_vision=False`)  
**Audit Date:** 2026-10-26  
**Auditor:** Final Peer-Review Audit and Minimal Correction Pass (Items 1–38)  

---

## 1. Traceable Claim-to-Evidence Matrix

| Claim ID | Paper Location | Claim Statement | Primary Evidence Source | Evidentiary Category | Scope & Boundaries | Verification Finding |
|:---:|:---|:---|:---|:---|:---|:---|
| **C01** | Sec. 1, 3.1 | Audit target is `browser-use 0.13.10` under text-only observation | `browser_use/__init__.py`; package metadata | Direct source inspection | Pinned single-framework release wheel | **VERIFIED FROM SOURCE** |
| **C02** | Sec. 3.1, Tab. 1 | Non-rendered tags (`script`, `meta`, etc.) pruned via `DISABLED_ELEMENTS` | `serializer.py:18, 481-482`; `test_observation_pipeline_stages.py` | Static AST + dynamic offline trace | Text-only pipeline; raw CDP/JS retains access | **VERIFIED FROM PRIMARY EVIDENCE** |
| **C03** | Sec. 3.2, Tab. 1 | Non-interactive containers have tags and attributes stripped | `serializer.py:1046-1058`; `audit_metadata_reachability.py` | Static AST + dynamic trace | Container ARIA stripped; inner typography emitted | **VERIFIED FROM PRIMARY EVIDENCE** |
| **C04** | Sec. 3.3, Tab. 1 | `DEFAULT_INCLUDE_ATTRIBUTES` omits custom developer `data-*` | `views.py:18-50`; `serializer.py:1210-1216` | Static AST + offline trace | Omitted by default; deliverable on interactive nodes with extended whitelist | **VERIFIED FROM PRIMARY EVIDENCE** |
| **C05** | Sec. 4.1, Fig. 1 | Chromium AXTree and DOM serializer operate in parallel | `session.py:140-195`; CDP session architecture | Direct source inspection | Serializer walks DOM directly; Blink builds AXTree independently | **VERIFIED FROM SOURCE** |
| **C06** | Sec. 4.3 | Icon heuristic classifies elements as interactive if $10 \le w, h \le 50\text{px}$ with class | `clickable_elements.py:228-240`; boundary fixtures | Code audit + Chromium fixture execution | Validated across 9 boundary cases (10px & 50px pass; 9px & 51px fail) | **VERIFIED FROM PRIMARY EVIDENCE** |
| **C07** | Sec. 4.3, Tab. 2 | Route `#home`: 27 of 34 selectors match Blink AXNodes ($79.4\%$) | `accessibility_tree_comparison.json`; Phase B census | Reproducible local browser census | Descriptive census of single layout; Wilson CI is $[63.2\%, 89.6\%]$ | **VERIFIED LOCAL CENSUS** |
| **C08** | Sec. 4.3 | The 7 unmatched selectors on `#home` are in-stock badge spans ($48.625 \times 15\text{px}$) | `clickable_elements.py:228-240`; DOM layout trace | Forensic node-level extraction | Spans lack click handlers; native AXTree marks them ignored | **VERIFIED FROM PRIMARY EVIDENCE** |
| **C09** | Sec. 4.3 | Out-of-stock badge ($74.766\text{px}$ wide) correctly excluded | Layout bounding box trace; Phase B census | Reproducible local browser census | Exceeds 50px ceiling; rejected by size heuristic | **VERIFIED FROM PRIMARY EVIDENCE** |
| **C10** | Sec. 4.3, Tab. 2 | Semantic control correspondence across true interactive controls on `#home` is $26/26$ ($100.0\%$) | `MULTI_ROUTE_OBSERVATION_AUDIT.md`; Phase B trace | Reproducible local browser census | True interactive controls (buttons, links, inputs) match AXTree 100% | **VERIFIED LOCAL CENSUS** |
| **C11** | Sec. 4.3, Tab. 2 | Multi-route audit: 100% operational correspondence on `#cart` ($8/8$) and `#checkout` ($13/13$); `#search` is $16/19$ ($84.2\%$) | `MULTI_ROUTE_OBSERVATION_AUDIT.md`; Phase B trace | Reproducible local browser census | Routes without badges achieve 100% operational match; all 4 achieve 100% semantic match | **VERIFIED MULTI-ROUTE CENSUS** |
| **C12** | Sec. 5.1 | Action-Label Co-Location: entity-specific ARIA button labels remove spatial reference resolution | `variants/v2-aria/index.html`; `shared/app-core.js:64` | Stimulus code audit | Specific to entity-augmented button labels vs generic labels | **VERIFIED METHODOLOGICAL CONFOUND** |
| **C13** | Sec. 5.3 | Exploratory cloud pilot: 41 completed runs with 100% success across 3 arms | `results/v3_3arm_summary.csv` (41 completed, 3 aborted retries) | Historical cloud-model pilot records | Simple tasks; acute ceiling effect; cannot prove equivalence or efficacy | **VERIFIED EXPLORATORY PILOT** |
| **C14** | Sec. 5.3 | Pilot used endpoint `gemini-flash-lite-latest` (aliased as `gemini-3.1-flash-lite`) | `results/daily_quota_ledger.json`; pilot summary | Historical execution log | Provider server-side checkpoint cannot be audited or pinned post-hoc | **VERIFIED RUNNER TELEMETRY** |
| **C15** | App. B, Tab. 5 | Exploratory local Qwen3:4b trial contains 5 diagnostic runs; Run 3 duration is 288.61s | `results/local_llama_summary.csv`; `local_llama_pilot_runs/` | Local model telemetry traces | 5 runs: 3.34s (init), 1013.09s (cold start), 288.61s (Run 3), 185.50s, 188.56s. 288.61s is Run 3 duration | **VERIFIED LOCAL TELEMETRY** |
| **C16** | Sec. 5.3 | Historical pilot (261 runs) had 9 exclusions in Rep 9; 147-run main attempt collapsed on runs 106-147 | `pilot_raw_261.csv`; `main_raw_147.csv` | Historical engineering records | Infrastructure failures and disconnect timeouts; superseded by v3 harness | **TRANSPARENTLY DISCLOSED** |
| **C17** | App. A, Tab. 3, 4 | Synthetic benchmark metrics verify analysis pipeline arithmetic without numerical error | `test_scratch_synthetic_data/dataset_1_valid_complete.csv` | Mock benchmark dataset | MOCK DATA ONLY; software verification benchmark; not real agent performance | **VERIFIED SOFTWARE BENCHMARK** |
| **C18** | Sec. 6.2 | Monte Carlo power simulation ($n=20$/arm) yields $11.45\%$ power for $\Delta=0.20$ | `scratch/reproduce_power.py`; `power_analysis.py` | Simulation model | Stated baseline assumptions; planning sensitivity analysis | **VERIFIED SIMULATION DERIVATION** |
| **C19** | Sec. 6.3 | TOST equivalence sizing requires $N=1,080$ (3 arms) at $p=0.70$ with $\delta=\pm 0.10$ | `reproduce_power_audit.py`; closed-form derivation | Mathematical derivation | Illustrative equivalence margin ($\pm 0.10$); unexecuted planning model | **VERIFIED ANALYTICAL DERIVATION** |
| **C20** | App. C | Fail-closed budget controller halts request dispatch upon reaching 600-request ceiling | `budget_controller.py`; `daily_quota_ledger.json` | Direct code inspection + test suite | Ledger locked at historical 604 requests; single-process Python lock | **VERIFIED SAFETY ARCHITECTURE** |
| **C21** | App. D | Full test suite of 138 unique non-overlapping tests passes 100% offline | 19 `test_*.py` modules; `unittest discover` | Offline test suite execution | Confirms software implementation resilience; does not prove live agent task efficacy | **VERIFIED SOFTWARE TEST SUITE** |
| **C22** | References | Bibliography contains 21 verified peer-reviewed conference publications and W3C recommendations | `references.bib`; `research_paper_final.tex` | Direct bibliography audit | 100% of defined entries cited in manuscript; zero unreferenced entries | **VERIFIED BIBLIOGRAPHY** |
| **C23** | Repo | Confirmatory 3-arm RCBD protocol ($N=72$) is specified but unexecuted | `proposed_3arm_schedule.csv`; `protocol_v4_config.json` | Proposed protocol specification | Balanced RCBD schedule; zero live model runs under confirmatory schedule | **PRE-REGISTERED BLUEPRINT ONLY** |

---

## 2. Explicit Boundaries: Prohibited Claims Confirmed Absent

1. **Downstream Behavioral Efficacy:** The manuscript does NOT claim that structured metadata (Schema.org JSON-LD or custom attributes) improves agent task completion rates.
2. **Behavioral Equivalence:** The manuscript does NOT claim that baseline text, ARIA, and custom attributes perform identically. The pilot $100\%$ ceiling effect is explicitly identified as an uninformative benchmark ceiling.
3. **Generalization Beyond Case Study:** The manuscript does NOT claim findings apply to frameworks other than `browser-use 0.13.10`, to multimodal vision models, or to dynamic commercial websites outside the tested local benchmark.
4. **Unit Tests as Empirical Proof:** Passing unit tests are presented strictly as software implementation verification, never as empirical validation of model reasoning or human-web agent interaction.
5. **Synthetic Benchmarks as Real Data:** Synthetic tables in Appendix A are explicitly disclaimed as mock software arithmetic tests.

# FINAL EVIDENCE MATRIX — DOM SERIALIZATION GAP RESEARCH MANUSCRIPT

**Project:** *The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents*  
**Date:** October 2026  
**Package:** `final_closure_v3`  
**Standard:** Strict Evidence Partitioning into 6 Qualified Categories

---

## 1. Evidence Category Taxonomy

To preserve scientific honesty and prevent methodological overclaiming, all claims and findings in this research are partitioned into six strictly segregated categories:

1. **Category A — Verified Offline Systems/Pipeline Measurements:** Deterministic static AST audits, CDP accessibility tree extractions, multi-route census records, and 138 passing unit/integration tests executing offline.
2. **Category B — Exploratory Live-Model Pilot Results:** 41 completed trials on `gemini-flash-lite-latest` exhibiting an acute $100\%$ task-battery ceiling effect ($\hat{\theta} = 0.0$).
3. **Category C — Aborted or Excluded Experimental Runs:** Historical 261-run pilot (excluded due to unasserted state verification), 147-run task battery (aborted due to battery collapse), and 3 transient HTTP 503 retry attempts.
4. **Category D — Synthetic/Mock Software Benchmark Results:** 96 synthetic trial rows utilized solely to verify numerical stability and unpooled CMH/Fisher statistical pipelines in Appendix A (Tables 3 & 4).
5. **Category E — Local-Model Hardware Diagnostics:** 5 exploratory runs using local `qwen3:4b` via Ollama documenting watchdog ceilings and cancellation telemetry under resource-constrained execution.
6. **Category F — Planned Prospective Experiments:** Confirmatory 4-arm randomized block design requiring $N \ge 1,080$ for equivalence testing (protocol specified, currently unexecuted and held offline).

---

## 2. Complete Claim-to-Evidence Mapping

| Claim ID | Core Manuscript Claim | Evidence Category | Primary Evidence Artifact & Provenance | Calculation Method / Verification Command | Operational Limitations | Manuscript Location |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **CLM-01** | Default observation pipeline in `browser-use 0.13.10` purges Schema.org JSON-LD | **Cat A** | `dom/service.py:18` (`DISABLED_ELEMENTS = ['script', 'style', ...]`), `serialization_audit_metrics.json` | Dynamic execution of `audit_metadata_reachability.py` | Applies to default `browser-use 0.13.10`; other frameworks may retain scripts | §4.1, Table 1 |
| **CLM-02** | Serializer strips non-interactive container ARIA markup prior to prompt assembly | **Cat A** | `dom/serializer/serializer.py:1046–1058`, `serialization_audit_metrics.json` | Inspection of AST lines and output of `audit_metadata_reachability.py` | Generic spans with `aria-label` lose annotations; interactive buttons retain them | §4.1, §4.4, Table 1 |
| **CLM-03** | Custom developer attributes (`data-*`) are excluded under default configurations | **Cat A** | `dom/service.py:32–45`, `serialization_audit_metrics.json` | Execution trace with `include_attributes` default vs. extended | Extending `include_attributes` restores delivery only on interactive nodes | §4.1, Table 1 |
| **CLM-04** | Operational selector correspondence on `#home` is 27/34 ($79.4\%$) | **Cat A** | `local_closure_results/multi_route_observation_audit.json` | CDP extraction comparing Blink AXTree with selector map | Tested on single SPA e-commerce store (`variants/v0-baseline/index.html`) | §4.3, Table 2 |
| **CLM-05** | 7 unmatched elements on `#home` are non-interactive product stock badge spans | **Cat A** | `local_closure_results/multi_route_observation_audit.json` (`unmatched_details`) | CDP bounding box audit ($48.625 \times 15\text{px}$) matching geometry heuristic | Badge spans lack AXNode in Blink AXTree; misclassified as clickable targets | §4.3, Table 2 |
| **CLM-06** | Genuine semantic interactive controls achieve $100\%$ ($26/26$) correspondence on `#home` | **Cat A** | `multi_route_observation_audit.json` (`sample_selectors`) | Census of buttons, links, and inputs against Blink AXTree | The 27th matched selector is `<form id="search-form">` (structural container) | §4.3, Table 2 |
| **CLM-07** | Multi-route correspondence across 4 views yields 100% genuine control matching | **Cat A** | `multi_route_observation_audit.json` across `#home`, `#cart`, `#checkout`, `#search` | Automated CDP multi-route extraction (`run_phase_b_browser_experiments.py`) | Evaluates $N=74$ total selector elements across 4 routes in controlled SPA | §4.3, Table 2 |
| **CLM-08** | The Action-Label Co-Location Confound replaces spatial reasoning with string matching | **Cat A** | `variants/v2-aria/index.html` button markup vs. `v0-baseline` | Direct comparison of serialized prompt text across arms | Specific to entity-augmented button labels (e.g. `aria-label="Add SoundFlow to cart"`) | §5.1 |
| **CLM-09** | Testing harness enforces deterministic verification via backend state queries | **Cat A** | `evaluators/test_verifiers.py`, SQLite db inspection, `localStorage.cartState` | Unit tests `test_verifiers.py` passing 100% offline | Eliminates self-reported LLM completion bias | §5.2 |
| **CLM-10** | Exploratory cloud pilot achieved 100% task completion (41/41 runs) | **Cat B** | `results/run_history.json`, `results/daily_quota_ledger.json` (Runs 1–41) | Ledger inspection: 13 ABS, 13 ARIA, 15 DATA-CFG, 0 failures | Represents task-battery ceiling effect; does NOT prove treatment equivalence | §5.3 |
| **CLM-11** | Historical 261-run pilot excluded from confirmatory analysis | **Cat C** | `MODEL_RUN_PROVENANCE_AUDIT.md`, historical run logs | Provenance audit verifying absence of deterministic state verifiers | Excluded to maintain empirical rigor; unasserted completions cannot be used | §5.3 |
| **CLM-12** | Historical 147-run trial battery collapsed and was aborted | **Cat C** | `MODEL_RUN_PROVENANCE_AUDIT.md`, `results/archive/` | Historical logs showing failure of intermediate task generator | Aborted trials discarded; not conflated with canonical trials | §5.3 |
| **CLM-13** | 3 transient HTTP 503 errors retried and resolved in Run 26 | **Cat C** | `results/run_history.json` (Run 26 metadata) | Inspection of retry logs in Run 26 trace | Retried automatically under framework policy without data corruption | §5.3 |
| **CLM-14** | Small-sample evaluations ($n \le 20$/arm) have only $10.8\%$ power for $\Delta = 0.20$ | **Cat F** | `reproduce_power_audit.py`, `STATISTICAL_AUDIT.md` | Statistical power calculation at $\alpha=0.05$, two-tailed binomial | Prospective planning calculation; highlights severe underpowering of web benchmarks | §6.2 |
| **CLM-15** | Valid equivalence testing requires $N \ge 1,080$ (3 arms) or $N \ge 1,440$ (4 arms) | **Cat F** | `reproduce_power_audit.py` | Farrington-Manning TOST formula ($\alpha=0.05, 1-\beta=0.80, \delta=\pm 0.10, p=0.70$) | Prospective planning boundary; confirmatory experiment remains unexecuted | §6.3 |
| **CLM-16** | Unpooled baseline contrasts prevent the Equivalence Fallacy on synthetic data | **Cat D** | `test_scratch_synthetic_data/dataset_1_valid_complete.csv`, `analyze_v3_results.py` | Fisher's exact test ($p=1.0000$), unpooled CMH tests in Table 3 | Synthetic data verification; does NOT represent agent task performance | Appendix A, Tables 3 & 4 |
| **CLM-17** | Local hardware diagnostic Run 3 duration was $288.61\text{s}$ under watchdog termination | **Cat E** | `results/local_llama_summary.csv` (`qwen3_smoke_003`) | Telemetry parsing: 2 steps, Step 2 cart action succeeded at 102.9s, timeout at 180s | Latency specific to Run 3 on local AMD Ryzen 5 / RTX 3050; not an omnibus mean | Appendix B, Table 5 |
| **CLM-18** | Quota controller halted historical execution at 604 requests under 600 ceiling | **Cat A** | `results/daily_quota_ledger.json`, `FORENSIC_CHECKPOINT_AUDIT_REPORT.md` | Run 41 dispatched at 596 requests, ran 8 in-flight steps ($596+8=604$), halted before Run 42 | Historical in-flight trial overshoot remediated via step-level `BudgetGuardedChatModel` | Appendix C |
| **CLM-19** | Testing harness and parsing pipelines verified by 138 passing unit tests | **Cat A** | 19 test modules in workspace root (`test_*.py`) | `python -m unittest discover -s . -p "test_*.py" --buffer` | 138 tests run in 16.579s with exit code 0; tests code correctness, not agent efficacy | Appendix D |
| **CLM-20** | Manuscript references 21 verified peer-reviewed and standards citations | **Cat A** | `final_closure_v3/references.bib`, `research_paper_final.tex` | Programmatic regex audit: 21 citations in text, 21 entries in bib, 0 unused | Sourced to official W3C standards, NeurIPS/ICLR/ACL proceedings, and protocol RFCs | Bibliography |

---

## 3. Methodological Guarantees

1. **No Conflation of Categories:** Synthetic pipeline tests (Category D) and local hardware diagnostics (Category E) are never presented as agent task efficacy findings.
2. **Explicit Quota Lock:** Live cloud trials (Category B) remain permanently frozen at 41 completed runs under the fail-closed budget ceiling (604 requests recorded in `daily_quota_ledger.json`). Zero unauthorized cloud API calls were initiated.
3. **Reproducibility Guarantee:** All Category A claims can be independently reproduced in under two minutes using the offline scripts and test suites provided in the repository.
